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
        try:
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
            arrResult['code']  = 0
            arrResult['judul'] = judul
            arrResult['arr_kalimat'] = arr_kalimat

            return arrResult
        except Exception as e:
            arrResult = {}
            arrResult['code']  = 404
            arrResult['message']  = str(e)
            return arrResult

    def getNewsDetik(self, url):
        try:
            url = url+'?single=1'
            page_berita     = requests.get(url)
            detail_berita   = BeautifulSoup(page_berita.content, 'html.parser')
            judul           = detail_berita.select('h1')

            if len(judul) > 0:
                judul           = judul[0].text.strip()
            else:
                judul = None


            body_berita = detail_berita.select('p')

            i = 0
            paragraph = ''
            while i < len(body_berita):

                text = body_berita[i].text.strip()
                if text.find('Ayo share cerita pengalaman dan upload photo album travelingmu di sini.') > -1:
                    text = ''

                if text.find('ADVERTISEMENT') > -1:
                    text = ''

                if text.find('selanjutnya...') > -1:
                    text = ''
                if text.find('SCROLL TO RESUME CONTENT') > -1:
                    text = ''
                if text.find('Gambas:Video') > -1:
                    text = ''

                if text != '':
                    text =  text.replace("'", '"')
                    paragraph += text+' '
                i+=1
            

            arr_kalimat = sent_tokenize(paragraph)
            words = ["advertisement"]

            for i,val in enumerate(arr_kalimat):

                if any(s in val.lower() for s in words):
                    arr_kalimat.remove(val)
            
            arrResult = {}
            arrResult['code']  = 0
            arrResult['judul'] = judul
            arrResult['arr_kalimat'] = arr_kalimat

            return arrResult
        except Exception as e:
            arrResult = {}
            arrResult['code']  = 404
            arrResult['message']  = str(e)
            return arrResult
    
    def getNewsTempo(self, url):
        try:
            page_berita     = requests.get(url)
            detail_berita   = BeautifulSoup(page_berita.content, 'html.parser')

            tag_judul       = detail_berita.select('h1')
            judul           = tag_judul[0].text.strip()
            
            all_cerita   = detail_berita.select('article.detail-artikel')
            cerita = all_cerita[0]
            arr_isi_cerita =  cerita.select('p')

            isi_cerita = ''

            for isi in arr_isi_cerita:
                paragraph = isi.text.strip()

                if paragraph != '' :
                    paragraph = paragraph.replace("'", '"')
                    isi_cerita += paragraph+' '

            arr_kalimat = sent_tokenize(isi_cerita)
            words = ["advertisement"]

            for i,val in enumerate(arr_kalimat):

                if any(s in val.lower() for s in words):
                    arr_kalimat.remove(val)
      
            arrResult = {}
            arrResult['code']  = 0
            arrResult['judul'] = judul
            arrResult['arr_kalimat'] = arr_kalimat


            return arrResult
        except Exception as e:
            arrResult = {}
            arrResult['code']  = 404
            arrResult['message']  = str(e)
            return arrResult
