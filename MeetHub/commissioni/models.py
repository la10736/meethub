from django.db import models

from sources.models import Source

from bs4 import BeautifulSoup as bs
from urllib2 import urlopen
import re
import locale
from datetime import datetime


class CommissioniSource(Source):
    cls_tag = "commissioni"
    
    page_link = models.URLField(max_length=500)



class Commissione(object):
    
    def __init__(self,link):
        self.link = link
        
    
    def _get_pdf(self):
            