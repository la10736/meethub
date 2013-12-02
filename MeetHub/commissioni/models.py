from django.db import models

from events.models import Event
from sources.models import Source
import re
from bs4 import BeautifulSoup as bs
from urllib2 import urlopen
import locale
from datetime import datetime
import urlparse
from esperimenti import retrivelink
from django.core.files.base import ContentFile
import pyPdf
import urllib
import logging

"""Espressione regolare per leggere le info della commissione"""
_ex_info_comm = re.compile("Commissione n\.\s*(?P<nr>\d{2})\s*\:?\s*Prossima seduta\s*\:\s*((?P<data>[^\s]+\s\d{1,2}\s[^\s]+\s\d{4})\sdalle ore (?P<inizio>\d{2}\.\d{2}) alle ore (?P<fine>\d{2}\.\d{2})(congiunta con (?P<congiunta>[^\n]+))?)?",
          re.MULTILINE)


class Commissione(Event):
    cls_tag = "commissione"
    
    """Il numero della commissione fatto di due cifre"""
    nr = models.CharField(max_length=2)
    """Indirizzo della pagina relativa alla commissione"""
    url = models.URLField(max_length=500)
    """Indica se la commissione con chi e' congiunta"""
    congiunta = models.CharField(max_length=200)
    """Ordine del giorno: i punti sono separati con la chiave indicata in _odg_sep"""
    _odg_sep = "++**++**++"
    odg = models.TextField()
    """Convocazione: pdf originale della convocazione"""
    pdf = models.FileField(upload_to="commissioni/%Y/%m/%d")
    
    @classmethod
    def list2odg(cls,l):
        '''Da una lista rende il formato del campo ODG'''
        return cls._odg_sep.join(l)
    
    @classmethod
    def odg2list(cls,odg):
        '''Prende il campo ODG e lo rende come una lista ordianta di stringhe'''
        return odg.split(cls._odg_sep)
    
    def get_odg_list(self):
        return self.odg2list(self.odg)
    
    def set_odg_list(self,l):
        self.odg = self.list2odg(l)

    def _fill_by_div(self,div):
        nome = div.p.a.string.strip()
        if nome.startswith("Commissione"):
            nome = nome[len("Commissione"):].strip() 
        self.title = nome
        self.url = urlparse.urljoin(self.url, div.p.a["href"].replace(" ","+"))
        div.p.a.decompose()
        text = str(div.p)
        d = _ex_info_comm.search(text).groupdict()
        self.nr = d["nr"]
        if d["data"]:
            self.start_date = self.get_datetime(d["data"],d["inizio"])
            self.end_date = self.get_datetime(d["data"],d["fine"])
        detail = bs(urlopen(self.url))
        url_convocazione = detail.find("a", text=re.compile("Ordine del giorno"))["href"]
        pdf = ContentFile(retrivelink.fetch_link(self.url, url_convocazione))
        self.pdf.save("Convocazione-%s"%self.title,pdf)
        self.pdf.close()
        self._fill_body_place_and_odg()
        
    @staticmethod
    def __get_place(txt):
        ss = re.split("\s+presso\s+",txt,1)
        if len(ss):
            pp = ss[1][len("il "):] if ss[1].startswith("il ") else ss[1]
            return re.split("\s+Sono\s+all'ordine\s+del\s+giorno",pp,1)[0].strip()
        return "Sconoscuto... non sono riuscito a capirlo"
    
    @staticmethod
    def __get_odg(txt):
        odg = txt.split("ordine del giorno i seguenti argomenti:",1)[1]
        odg = re.split("Distinti [sS]aluti",odg,1)[0]
        ret = []
        for x in re.split('\d+\)\s*',odg.strip()):
            arg = x.strip()
            if arg:
                ret.append(re.sub("\s+", " ", arg))
        return ret

    def _fill_body_place_and_odg(self):
        pdf = file(self.pdf.path)
        pp = pyPdf.PdfFileReader(pdf)
        txt = pp.getPage(0).extractText()
        self.body = txt
        self.place = self.__get_place(txt)
        self.set_odg_list(self.__get_odg(txt))
        
    def fill(self):
        """Riempie i campi della commissione a partire dall'url"""
        detail = bs(urlopen(self.url))
        url_convocazione = detail.find("a", text=re.compile("Ordine del giorno"))["href"]
        p = urlopen(urlparse.urljoin(self.url, url_convocazione).replace(" ","+")).read()
        pdf = ContentFile(p)
        self.pdf.save("Convocazione-%s"%self.title,pdf)
        self.pdf.close()
        self._fill_body_place_and_odg()

class CdZ(Source):
    cls_tag = "CdZ"
    zona = models.CharField(max_length=60)
    """Pagina dove ricercare le commissioni"""
    url = models.URLField()
    
    @staticmethod
    def get_datetime(data,ora):
        locale.setlocale(locale.LC_ALL, 'it_IT.utf8')
        fmt = "%A %d %B %Y %H.%M"
        return datetime.strptime("%s %s"%(data,ora), fmt)
    
    def get_prossime_commisioni_from_url(self):
        """Ritorna una lista di commissioni 
        come dizzionari che ci sono nella pagina home.
        """
        ret = []
        now = datetime.now()
        for div in bs(urlopen(self.url)).find_all('div', class_="commissioni"):
            c = {}
            nome = div.p.a.string.strip()
            if nome.startswith("Commissione"):
                nome = nome[len("Commissione"):].strip()
            c["nome"] = nome
            c["url"] = urlparse.urljoin(self.url, div.p.a["href"].replace(" ","+"))
            div.p.a.decompose()
            text = str(div.p)
            c.update(_ex_info_comm.search(text).groupdict())
            if c["data"]:
                c["start_date"] = self.get_datetime(c["data"],c["inizio"])
                c["end_date"] = self.get_datetime(c["data"],c["fine"])
                c["old"] = False
                if c["start_date"] <= now:
                    c["old"] = True
                ret.append(c)
                """Controlliamo se e nuova o un aggiornamento"""
                cc = Commissione.objects.filter(start_date__gt=now,nr=c["nr"])
                if cc:
                    if len(cc)>1:
                        logging.error("Piu' di una commissime prevista IMPOSSIBILE")
                    prev = cc[0]
                    c["ref"] = prev
                    if prev.start_date != c["start_date"] or prev.end_date != c["end_date"]:
                        c["changed"] = True
        return ret

    def _nuova_commissione(self, nr, nome, url, data, inizio, fine , congiunta=""):
        """Visita la pagina della commissione e in base al pdf della convocazione
        crea l'evento"""
        title = "%s Commissione [%s] %s"%(self.zona,nr,nome)
        start_date = self.get_datetime(data,inizio)
        end_date = self.get_datetime(data,fine)
        if congiunta:
            title += " congiunta " + congiunta
        commissione = Commissione(nr=nr, title=title, url=url, congiunta=congiunta, 
                           start_date=start_date, end_date=end_date)
        commissione.fill()
        self._event_generated(commissione)
        
