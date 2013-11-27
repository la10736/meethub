'''
Created on 18/nov/2013

@author: michele
'''
import urlparse
import urllib2
import logging
from bs4 import BeautifulSoup as bs
import re


logging.getLogger().setLevel(logging.DEBUG)

def fetch_link(url,link,dest=None):
    if link:
        url = urlparse.urljoin(url, link.replace(" ","+"))
    resp = urllib2.urlopen(url)
    if resp.code != 200:
        raise IOError("Cannot fetch %s"%(url))
    ret = resp.read()
    if dest:
        opt = ""
        if not "text" in resp.headers["content-type"]:
            opt = "b"
        out = file(dest,"w"+opt)
        out.write(ret)
    return ret

url='http://www.comune.milano.it/portale/wps/portal/!ut/p/c1/04_SB8K8xLLM9MSSzPy8xBz9CP0os_hAc8OgAE8TIwMDJ2MzAyMPIzdfHw8_Y28jQ_1wkA6zeD9_o1A3E09DQwszV0MDIzMPEyefME8DdxdjiLwBDuBooO_nkZ-bql-QnZ3m6KioCADL1TNQ/dl2/d1/L2dJQSEvUUt3QS9ZQnB3LzZfQU01UlBJNDIwT1RTMzAySEtMVEs5TTMwMDA!/?WCM_GLOBAL_CONTEXT=/wps/wcm/connect/ContentLibrary/in+comune/in+comune/i+consigli+di+zona/zona+6/2+in+comune_zona6_pagina+zona'

if __name__ == '__main__':
    import commissioni
    for c in commissioni.get_commissioni(url):
        name = c.p.a.string.strip()
        details_url = urlparse.urljoin(url, c.p.a["href"])
        commissione = bs(urllib2.urlopen(details_url.replace(" ","+")))
        odg_link = commissione.find("a", text=re.compile("Ordine del giorno"))
        if odg_link:
            outfile = name.replace(" ","_")+".pdf"
            logging.info("Salvo OdG commissione %s in %s"%(name,outfile))
            odg = fetch_link(details_url, odg_link["href"],
                             outfile)
            
        else:
            logging.info("Nessuna commissione in vista per "+name)
            