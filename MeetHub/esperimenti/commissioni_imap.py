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

def getcharsets(msg):
    charsets = set({})
    for c in msg.get_charsets():
        if c is not None:
            charsets.update([c])
    return charsets

def handleerror(errmsg, emailmsg,cs):
    print()
    print(errmsg)
    print("This error occurred while decoding with ",cs," charset.")
    print("These charsets were found in the one email.",getcharsets(emailmsg))
    print("This is the subject:",emailmsg['subject'])
    print("This is the sender:",emailmsg['From'])

def getbodyfromemail(msg, re_sub=''):
    body = None
    #Walk through the parts of the email to find the text body.    
    if msg.is_multipart():    
        for part in msg.walk():

            # If part is multipart, walk through the subparts.            
            if part.is_multipart(): 

                for subpart in part.walk():
                    if subpart.get_content_type() == 'text/plain':
                        # Get the subpart payload (i.e the message body)
                        body = subpart.get_payload(decode=True) 
                        #charset = subpart.get_charset()

            # Part isn't multipart so get the email body
            elif part.get_content_type() == 'text/plain':
                body = part.get_payload(decode=True)
                #charset = part.get_charset()

    # If this isn't a multi-part message then get the payload (i.e the message body)
    elif msg.get_content_maintype() == 'text':
        body = msg.get_payload(decode=True) 

    if re_sub:
        print repr(body)
        body = re.sub(re_sub, '', body)
        
    # No checking done to match the charset with the correct part. 
    for charset in getcharsets(msg):
        try:
            body = body.decode(charset)
        except UnicodeDecodeError:
            handleerror("UnicodeDecodeError: encountered.",msg,charset)
        except AttributeError:
            handleerror("AttributeError: encountered" ,msg,charset)
    return body  
 
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
        print bs(getbodyfromemail(email.message_from_string(rawm),r"\!\r\n")).text
        #email_message = email.message_from_string(rawm)
        #print get_first_text_block(None,email_message)

for a in azzioni:
    print a