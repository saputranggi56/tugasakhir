from nltk import sent_tokenize
import requests
from bs4 import BeautifulSoup
from nltk import sent_tokenize
import numpy as np, pandas as pd

class DataBeritaController(object):

    def __init__(self, kalimat='', flagging=''):
        self.kalimat = kalimat
        self.flagging = flagging

    def as_dict(self):
        return {'kalimat': self.kalimat, 'flagging': self.flagging}

    def tokenize(self, data=''):
        arr_kalimat = sent_tokenize(data)
        return arr_kalimat

    def getNewscnbc(self, url):
        page_berita   = requests.get(url)
        page_berita   = BeautifulSoup(page_berita.content, 'html.parser')
    
        judul_html = page_berita.select('h1')
        judul      = judul_html[0].text.strip()

        body_berita = page_berita.select('p')
        
        isi_cerita = ''

        for i in body_berita :
            tempText = i.text.strip()
            
            if tempText :
                isi_cerita += tempText + ' '

        arr_kalimat = sent_tokenize(isi_cerita)
        words = ["advertisement"]

        for i,val in enumerate(arr_kalimat):

            if any(s in val.lower() for s in words):
                arr_kalimat.remove(val)
        
        arrResult = {}
        arrResult['judul'] = judul
        arrResult['arr_kalimat'] = arr_kalimat

        return arrResult
