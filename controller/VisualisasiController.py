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

class VisualisasiController():
    
    def worldCloud(self):
        model             = Datalatih(CONN)
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
        model             = Datalatih(CONN)
        loadData          = model.getDataPercentage(portal=portal)

        return loadData

    def loadDataByFeature(self):
        model       = Datalatih(CONN)
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