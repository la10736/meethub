'''
Created on 19/nov/2013

@author: damico
'''

import sys
from pdfminer.pdfinterp import PDFResourceManager, process_pdf
from pdfminer.converter import TextConverter
from pdfminer.layout import LAParams
import cStringIO

def pdf2txt(fp, pagenos=set(), caching=True, codec = 'utf-8',
            password=''):
    outfp = cStringIO.StringIO()
    laparams = LAParams()
    rsrcmgr = PDFResourceManager(caching=caching)
    device = TextConverter(rsrcmgr, outfp, codec=codec, laparams=laparams)
    process_pdf(rsrcmgr, device, fp, pagenos, password=password,
                    caching=caching, check_extractable=True)
    return outfp.getvalue()

if __name__ == '__main__':
    for v in sys.argv[1:]:
        print pdf2txt(file(v,"rb"))