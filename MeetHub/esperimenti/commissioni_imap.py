'''
Created on 02/dic/2013

@author: damico
'''
import imaplib
import email
import re
import mysecret
import logging
import chardet
from bs4 import BeautifulSoup as bs

subject_re = re.compile(".*\s+Commissioni\s+Istruttorie\s+Zonali\s+-\s+(?P<azzione>.*\n*.*)Convocazione\s+Nr\s+(?P<id>\d+)\s+in\s+Data: (?P<data>\d{2}/\d{2}/\d{4})",re.MULTILINE)

def get_text(msg):
    text = ""
    if msg.is_multipart():
        html = None
        for part in msg.get_payload():
            charset = part.get_content_charset()
            if charset is None:
                charset = chardet.detect(str(part))['encoding']
            if part.get_content_type() == 'text/plain':
                text = unicode(part.get_payload(decode=True),str(charset),"ignore").encode('utf8','replace')
            if part.get_content_type() == 'text/html':
                html = unicode(part.get_payload(decode=True),str(charset),"ignore").encode('utf8','replace')
        if html is None:
            return text.strip()
        else:
            return html.strip()
    else:
        text = unicode(msg.get_payload(decode=True),msg.get_content_charset(),'ignore').encode('utf8','replace')
        return text.strip()

cfg = {"address":"imap.gmail.com",
       "user":mysecret.user,
       "pwd":mysecret.pwd,
       "folders":["inbox"]#,"M5S/Consiglio di Zona"]
       }


mail = imaplib.IMAP4_SSL(cfg["address"])
_res,_desc = mail.login(cfg["user"], cfg["pwd"])

azzioni = set()
for f in cfg["folders"]:
    _res,_desc = mail.select(f)
    _res,uid = mail.uid('search', None, '(HEADER Subject "Commissioni Istruttorie Zonali")')
    uid = uid[0].split(' ')
    
    '''Scarichiamo tutti i subject e parsiamoli'''
    _res,data = mail.uid("fetch", ",".join(uid), '(BODY[HEADER.FIELDS (SUBJECT)])')
    for x in data:
        if ")" == x :
            continue
        _m,sub = x
        print sub
        s = subject_re.search(sub)
        if s is not None:
            d = s.groupdict()
            print d
            azzione = re.sub("\s+"," ",d["azzione"]).strip()
            azzioni.add(azzione)
        else:
            logging.error('Non sono riuscito a parsare il soggetto "%s"'%sub)

    for i in uid:
        rawm = mail.uid('fetch', i, '(RFC822)')[1][0][1]
        print "uid = " + i
        print bs(get_text(email.message_from_string(rawm))).text
        #email_message = email.message_from_string(rawm)
        #print get_first_text_block(None,email_message)

for a in azzioni:
    print a