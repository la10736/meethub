'''
Created on 02/dic/2013

@author: damico
'''
import imaplib
import email

def get_first_text_block(self, email_message_instance):
    maintype = email_message_instance.get_content_maintype()
    if maintype == 'multipart':
        for part in email_message_instance.get_payload():
            if part.get_content_maintype() == 'text':
                return part.get_payload()
    elif maintype == 'text':
        return email_message_instance.get_payload()

__pwd = None
mail = imaplib.IMAP4_SSL('imap.gmail.com')
_res,_desc = mail.login('michele.damico@gmail.com', __pwd)
_res,_desc = mail.select("inbox")
_res,uid = mail.uid('search', None, '(HEADER Subject "Commissioni Istruttorie Zonali")')
uid = uid[0].split(' ')


for i in uid:
    rawm = mail.uid('fetch', i, '(RFC822)')[1][0][1]
    email_message = email.message_from_string(rawm)
    print email_message.items()
    print get_first_text_block(None,email_message)
