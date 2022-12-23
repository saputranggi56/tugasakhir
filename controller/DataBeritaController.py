from nltk import sent_tokenize

class DataBeritaController(object):

    def __init__(self, kalimat='', flagging=''):
        self.kalimat = kalimat
        self.flagging = flagging


    def as_dict(self):
        return {'kalimat': self.kalimat, 'flagging': self.flagging}

    def tokenize(self, data=''):
        arr_kalimat = sent_tokenize(data)
        return arr_kalimat
