import nltk # Library nltk
import string # Library string
import re # Library regex
from nltk.tokenize import word_tokenize 

import nltk

from  Sastrawi.Stemmer.StemmerFactory import StemmerFactory
from Sastrawi.StopWordRemover.StopWordRemoverFactory import StopWordRemoverFactory

class PraprosesController() :

    def __init__(self, dataPraproses=""):
        self.dataPraproses = dataPraproses

    def loadData(self, memang=""):
        model = Praproses(storage=CONN)

        loadData = model.getData()
        return loadData
    
    def caseFolding(self):
        sentenceLower = self.dataPraproses.lower()
        return sentenceLower

    def deleteNumber(self):
        cleanNumber = re.sub(r"\d+", "", self.dataPraproses) 
        return cleanNumber
    
    def deletePunctuation(self):
        cleanPunctuation = self.dataPraproses.translate(str.maketrans("","",string.punctuation))
        return cleanPunctuation

    def deleteWhiteSpace(self):
        cleanWhiteSpace = self.dataPraproses.strip() 
        cleanWhiteSpace = re.sub('\s+',' ',cleanWhiteSpace)
        return cleanWhiteSpace

    def stopWords(self):
        factory = StopWordRemoverFactory()
        
        more_stopword = ['per', 'an'] #menambahkan stopword

        factory = StopWordRemoverFactory()
        stopword = factory.create_stop_word_remover()

        p1 = self.dataPraproses.translate(str.maketrans('','',string.punctuation)).lower() 
        stopWord = stopword.remove(p1)

        return stopWord

    def stemming(self):
        factory = StemmerFactory()
        stemmer = factory.create_stemmer()

        dataSteam = stemmer.stem(self.dataPraproses) 

        return dataSteam

    def allPraproses(self):
        self.dataPraproses = self.caseFolding()
        self.dataPraproses = self.deleteNumber()
        self.dataPraproses = self.deletePunctuation()
        self.dataPraproses = self.deleteWhiteSpace()
        self.dataPraproses = self.stopWords()
        self.dataPraproses = self.stemming()

        return self.dataPraproses
    
