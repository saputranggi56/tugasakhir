

# from config.dbconfig import CONN
from model.Datalatih import Datalatih
from controller.DataBeritaController import DataBeritaController
from controller.PraprosesController import PraprosesController

import numpy as np, pandas as pd
from pandas import DataFrame

from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.naive_bayes import MultinomialNB
from sklearn.pipeline import make_pipeline
from sklearn.metrics import confusion_matrix, accuracy_score
from sklearn.model_selection import train_test_split

from wordcloud import WordCloud, ImageColorGenerator
from PIL import Image
import matplotlib.pyplot as plt
import _pickle as cPickle

class ModelingController():
    G_CONN = ''

    def __init__(self, dataPraproses="", connection=""):
        self.dataPraproses = dataPraproses
        ModelingController.G_CONN = connection


    def getDataLatih(self):
        model       = Datalatih(ModelingController.G_CONN)
        loadData    = model.getData()
        
        return  loadData

    def modelingAction(self):
        dataLatih = self.getDataLatih()

        list_data_latih = [DataBeritaController(x[6],x[7]) for x in dataLatih]

        df = pd.DataFrame([x.as_dict() for x in list_data_latih])
        df.head()

        y_train = df.loc[:,"flagging"]
        X_train = df.loc[:,"kalimat"] 

        model = make_pipeline(TfidfVectorizer(), MultinomialNB())

        model.fit(X_train, y_train)
        
        return model
    
    def classfication(self, dataUji=""):
        classResult = ['Netral', 'Positif', 'Negatif']

        praproses = PraprosesController(dataPraproses=dataUji)
        afterPraproses = praproses.allPraproses()
        
        with open('model_nb.pkl', 'rb') as fid:
            model_loaded = cPickle.load(fid)

        # pred = model.predict([afterPraproses])
        pred = model_loaded.predict([afterPraproses])
        
        dataReturn = {}
        dataReturn['after_praproses']   = afterPraproses
        dataReturn['flagging']          = classResult[int(pred[0])]
        return dataReturn
    
    def worldCLoud(self, kalimat_berita=""):
        praproses = PraprosesController(dataPraproses=kalimat_berita)
        rome_corpus = praproses.allPraproses()
        
        wc = WordCloud().generate_from_text(rome_corpus)
        wc.to_file('static/Classification.png')
        
        return praproses
        