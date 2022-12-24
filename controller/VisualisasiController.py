from config.dbconfig import CONN
from model.Datalatih import Datalatih
from controller.DataBeritaController import DataBeritaController
from collections import defaultdict

from wordcloud import WordCloud, ImageColorGenerator
from PIL import Image
import matplotlib.pyplot as plt
import re # Library regex

import pandas as pd
import numpy as np
from nltk import FreqDist
from cryptography.fernet import Fernet
from Crypto.Cipher import DES
import base64

class VisualisasiController():

    KEY = '3411171120'
    IV = 'AnggiSaputra'    
    
    G_CONN = ''

    def __init__(self, connection=""):
        VisualisasiController.G_CONN = connection
        # print(connection)

    def worldCloud(self):
        model             = Datalatih(VisualisasiController.G_CONN)
        loadDataPostif    = model.getDataByLabel(flagging="1")
        loadDataNegatif   = model.getDataByLabel(flagging="2")
        loadDataNetral    = model.getDataByLabel(flagging="0")

        rome_corpus = ""

        for x in loadDataPostif:
            rome_corpus =rome_corpus+" "+x[0]

        wc = WordCloud().generate_from_text(rome_corpus)
        wc.to_file('static/Positif.png')
        
        rome_corpus = ""
        for x in loadDataNegatif:
            rome_corpus =rome_corpus+" "+x[0]
        wc = WordCloud().generate_from_text(rome_corpus)
        wc.to_file('static/Negatif.png')

        rome_corpus = ""
        for x in loadDataNetral:
            rome_corpus =rome_corpus+" "+x[0]

        wc = WordCloud().generate_from_text(rome_corpus)
        wc.to_file('static/Netral.png')
           

        return 'success'

    def loadDataPercentage(self, portal=""):
        model             = Datalatih(VisualisasiController.G_CONN)
        loadData          = model.getDataPercentage(portal=portal)

        return loadData
        
    def get_baseurl(self):
        return self._base_url

    def loadDataByFeature(self):
        model       = Datalatih(VisualisasiController.G_CONN)
        loadData    = model.getData()

        counts = defaultdict(int)

        for x in loadData :
            dataPraproses = x[9]
            flagging      = x[7]

            helper = {}
            word_list = dataPraproses.split()
            
            for word in word_list:
                counts[word] += 1
        
        arrSorted = (sorted(counts.items(), key=lambda x: x[1]))
        tenBig    = np.array(arrSorted[-10:])
        tenBigWords = tenBig[:,0]
        # print(tenBigWords)
        tenBigWords = tenBigWords[::-1]
        
        dataResult = {}
        dataResult['words'] = tenBigWords.tolist()
        
        arrPositif = []
        arrNegatif = []
        arrNetral  = []

        for x in tenBigWords:
            positif = (model.getDataByLabelAndWord('1', x))
            kalimatPositif = [" ".join(x) for x in positif]        
            kalimatPositif = " ".join(kalimatPositif)
            
            arrPositif.append(kalimatPositif.count(x))

            netral = (model.getDataByLabelAndWord('0', x))
            kalimatNetral = [" ".join(x) for x in netral]        
            kalimatNetral = " ".join(kalimatNetral)
            
            arrNetral.append(kalimatNetral.count(x))

            negatif = (model.getDataByLabelAndWord('2', x))
            kalimatNegatif = [" ".join(x) for x in negatif]        
            kalimatNegatif = " ".join(kalimatNegatif)
            
            arrNegatif.append(kalimatNegatif.count(x))

        dataTotal = []
        dataTotal.append(arrPositif)
        dataTotal.append(arrNegatif)
        dataTotal.append(arrNetral)

        dataResult['total'] = dataTotal
        # print(dataResult)
        return dataResult

    def loadDataClassFlagging(self, flagging='', portal=''):
        model   = Datalatih(VisualisasiController.G_CONN)
        dataByClass = model.getAllDataByClass(flagging, portal)
             
        for idx, x in enumerate(dataByClass):
            dataByClass[idx][6] = self.encrypt(sample_string=str(dataByClass[idx][6]))
           
        return dataByClass

    def loadDataBeritaById(self, berita_id=""):
        berita_id = self.decrypt(base64_string=berita_id)
        model   = Datalatih(VisualisasiController.G_CONN)
        dataBerita = model.getDataBeritaById(berita_id)

        berita_data = {}
        berita_data['judul'] = dataBerita[0][3]
        berita_data['portal'] = dataBerita[0][1]

        berita_data['total_kalimat'] = 0
        berita_data['total_kalimat_positif']   = 0
        berita_data['total_kalimat_negatif']   = 0
        berita_data['total_kalimat_netral']    = 0

        text_berita = '<p class="text-justify h4 p-3" style="line-height: 1.5">'

        for x in dataBerita:
            if str(x[7]) == '1' :
                tmp_text =  '<span class="bg-primary text-white">'+x[6].strip()+'</span>'
                berita_data['total_kalimat_positif'] += 1
            if str(x[7]) == '2' :
                tmp_text =  '<span class="bg-danger text-white">'+x[6].strip()+'</span>'
                berita_data['total_kalimat_negatif'] += 1
            if str(x[7]) == '0' :
                tmp_text =  '<span class="bg-info text-white">'+x[6].strip()+'</span>'
                berita_data['total_kalimat_netral'] += 1

            berita_data['total_kalimat'] += 1
            
            
            text_berita = text_berita+' '+tmp_text

        text_berita  = text_berita+'</p>'
        berita_data['text_berita'] = text_berita

        return berita_data

    def encrypt(self, sample_string=""):
        sample_string_bytes = sample_string.encode("ascii")
        base64_bytes = base64.b64encode(sample_string_bytes)
        base64_string = base64_bytes.decode("ascii")
        return base64_string

    def decrypt(self, base64_string=""):
        base64_bytes = base64_string.encode("ascii")
        sample_string_bytes = base64.b64decode(base64_bytes)
        sample_string = sample_string_bytes.decode("ascii")    
        return sample_string
