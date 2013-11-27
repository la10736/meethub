'''
Created on 16/nov/2013

@author: michele
'''

from bs4 import BeautifulSoup as bs
from urllib2 import urlopen
import re
import locale
from datetime import datetime
import urllib2
import urlparse

url='http://www.comune.milano.it/portale/wps/portal/!ut/p/c1/04_SB8K8xLLM9MSSzPy8xBz9CP0os_hAc8OgAE8TIwMDJ2MzAyMPIzdfHw8_Y28jQ_1wkA6zeD9_o1A3E09DQwszV0MDIzMPEyefME8DdxdjiLwBDuBooO_nkZ-bql-QnZ3m6KioCADL1TNQ/dl2/d1/L2dJQSEvUUt3QS9ZQnB3LzZfQU01UlBJNDIwT1RTMzAySEtMVEs5TTMwMDA!/?WCM_GLOBAL_CONTEXT=/wps/wcm/connect/ContentLibrary/in+comune/in+comune/i+consigli+di+zona/zona+6/2+in+comune_zona6_pagina+zona'
ex=re.compile("Commissione n\.\s*(?P<nr>\d{2})\s*\:?\s*Prossima seduta\s*\:\s*((?P<data>[^\s]+\s\d{1,2}\s[^\s]+\s\d{4})\sdalle ore (?P<inizio>\d{2}\.\d{2}) alle ore (?P<fine>\d{2}\.\d{2})(?P<congiunta> congiunta con [^\n]+)?)?",
              re.MULTILINE)

def get_commissioni(url):
    return bs(urlopen(url)).find_all('div', class_="commissioni")

def get_datetime(data,ora):
    locale.setlocale(locale.LC_ALL, 'it_IT.utf8')
    fmt = "%A %d %B %Y %H.%M"
    return datetime.strptime("%s %s"%(data,ora), fmt)

def get_soup(url):
    return bs(urlopen(url))

def get_place(txt):
    ss = re.split("\s+presso\s+",txt,1)
    if len(ss):
        pp = ss[1][len("il "):] if ss[1].startswith("il ") else ss[1]
        return re.split("\s+Sono\s+all'ordine\s+del\s+giorno",pp,1)[0].strip()
    return "Sconoscuto... non sono riuscito a capirlo"

def get_odg(txt):
    odg = txt.split("ordine del giorno i seguenti argomenti:",1)[1]
    odg = re.split("Distinti [sS]aluti",odg,1)[0]
    ret = []
    i = 1
    for x in re.split('\d+\)\s*',odg.strip()):
        arg = x.strip()
        if arg:
            ret.append((i,re.sub("\s+", " ", arg)))
            i += 1
    return ret

if __name__ == '__main__':
    ret=[]
    for c in get_commissioni(url):
        d={}
        d["name"] = c.p.a.string.strip()
        if d["name"].startswith("Commissione"):
            d["name"] = d["name"][len("Commissione"):].strip() 
        print "name = " + d["name"]
        d["link"] = c.p.a["href"]
        c.p.a.decompose()
        text = str(c.p)
        d.update(ex.search(text).groupdict())
        if d["data"]:
            d["datetime_start"] = get_datetime(d["data"],d["inizio"])
            d["datetime_end"] = get_datetime(d["data"],d["fine"])
        ret.append(d)
    
    import retrivelink
    import pdf2txt
    import cStringIO
    for c in ret:
        if c.has_key("datetime_start"):
            detail_url = urlparse.urljoin(url, c["link"].replace(" ","+"))
            detail = get_soup(detail_url)
            convocazione_link = detail.find("a", text=re.compile("Ordine del giorno"))["href"]
            print "===================================================================="
            print "La prossima commissione per %s [%s] e' il %s [%s]" %\
                (c["name"],c["nr"],c["datetime_start"].strftime("%D-%T"),
                 c["datetime_end"].strftime("%D-%T"))
            print "===================================================================="
            print "Convocazione:"
            pdf = cStringIO.StringIO()
            pdf.write(retrivelink.fetch_link(detail_url, convocazione_link))
            #print pdf2txt.pdf2txt(pdf)
            import pyPdf
            pp = pyPdf.PdfFileReader(pdf)
            txt = pp.getPage(0).extractText()
            print txt
            print "LUOGO: "+get_place(txt)
            print "OdG:"
            print '\n'.join(["%d) %s"%(i,a) for i,a in get_odg(txt)])
