'''
Created on 02/dic/2013

@author: damico
'''
import imaplib
import email
import re
import mysecret
import logging

subject_re = re.compile(".*\s+Commissioni\s+Istruttorie\s+Zonali\s+-\s+(?P<azzione>.*\n*.*)Convocazione\s+Nr\s+(?P<id>\d+)\s+in\s+Data: (?P<data>\d{2}/\d{2}/\d{4})",re.MULTILINE)

def get_first_text_block(self, email_message_instance):
    maintype = email_message_instance.get_content_maintype()
    if maintype == 'multipart':
        for part in email_message_instance.get_payload():
            if part.get_content_maintype() == 'text':
                return part.get_payload()
    elif maintype == 'text':
        return email_message_instance.get_payload()

cfg = {"address":"imap.gmail.com",
       "user":mysecret.user,
       "pwd":mysecret.pwd,
       "folders":["inbox","M5S/Consiglio di Zona"]
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
        #email_message = email.message_from_string(rawm)
        #print get_first_text_block(None,email_message)

for a in azzioni:
    print a
