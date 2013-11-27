'''
Created on 19/nov/2013

@author: michele
'''

import re
import datetime
import pdf2txt
import sys
from bs4 import BeautifulSoup as bs
from urllib2 import urlopen

mesi_map = {'GENNAIO':1,
            'FEBBRAIO':2,
            'MARZO':3,
            'APRILE':4,
            'MAGGIO':5,
            'GIUGNO':6,
            'LUGLIO':7,
            'AGOSTO':8,
            'SETTEMBRE':9,
            'OTTOBRE':10,
            'NOVEMBRE':11,
            'DICEMBRE':12
            }

ex = re.compile("\s+per\s+(?P<gsett>[^\s]+)\s+(?P<gg>\d+)\s+(?P<mese>[^\s]+)\s+(?P<anno>\d+)\s+dalle\s+ore\s+(?P<s_ore>\d+)[\.\:](?P<s_min>\d{2})\s+alle\s+ore\s+(?P<f_ore>\d+)[\.\:](?P<f_min>\d{2})",re.MULTILINE)

def get_start_end(txt):
    r = ex.search(txt)
    d = r.groupdict() if r else None
    if d:
        start = datetime.datetime(int(d['anno']),mesi_map[d['mese']],int(d['gg']),
                                    int(d['s_ore']),int(d['s_min']))
        end = datetime.datetime(int(d['anno']),mesi_map[d['mese']],int(d['gg']),
                                    int(d['f_ore']),int(d['f_min']))
        return start,end
    return None

def get_odg(txt):
    odg = txt.split("ordine del giorno:",1)[1].split("Distinti saluti",1)[0]
    ret = []
    i = 1
    for x in re.split('\d+\)\s*',odg.strip()):
        arg = x.strip()
        if arg:
            ret.append((i,re.sub("\s+", " ", arg)))
            i += 1
    return ret

def get_url_convocazione(url):
    return bs(urlopen(url)).find('span', class_="title", 
                                     text="Programma del Consiglio Prossima seduta:").parent.a['href']

url='http://www.comune.milano.it/portale/wps/portal/!ut/p/c1/04_SB8K8xLLM9MSSzPy8xBz9CP0os_hAc8OgAE8TIwMDJ2MzAyMPIzdfHw8_Y28jQ_1wkA6zeD9_o1A3E09DQwszV0MDIzMPEyefME8DdxdjiLwBDuBooO_nkZ-bql-QnZ3m6KioCADL1TNQ/dl2/d1/L2dJQSEvUUt3QS9ZQnB3LzZfQU01UlBJNDIwT1RTMzAySEtMVEs5TTMwMDA!/?WCM_GLOBAL_CONTEXT=/wps/wcm/connect/ContentLibrary/in+comune/in+comune/i+consigli+di+zona/zona+6/2+in+comune_zona6_pagina+zona'

if __name__ == '__main__':
    print get_url_convocazione(url)
    for v in sys.argv[1:]:
        convocazione = pdf2txt.pdf2txt(file(v,"rb"))
        inizio,fine = get_start_end(convocazione)
        odg = get_odg(convocazione)
        print "CdZ %s-%s con il seguente OdG"%(str(inizio),str(fine))
        print '\n'.join(["%d) %s"%(i,a) for i,a in odg])
        
        
