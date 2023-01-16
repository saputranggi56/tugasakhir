from flask import Flask, render_template, request, session, url_for, redirect

from controller.PraprosesController import PraprosesController
from controller.ModelingController import ModelingController
from controller.DataBeritaController import DataBeritaController
from controller.VisualisasiController import VisualisasiController
import socket

import psycopg2
import psycopg2.extras
import numpy as np, pandas as pd
from pandas import DataFrame
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.naive_bayes import MultinomialNB
from sklearn.pipeline import make_pipeline
from sklearn.metrics import confusion_matrix, accuracy_score
from sklearn.model_selection import train_test_split
import array
from urllib.parse import urlsplit, urlunsplit, urlparse
from config.dbconfig import connection_kwargs


app = Flask(__name__)
app.config["SECRET_KEY"] = "TugasAkhir3411171120"


@app.route("/visualisasi")
def visualisasi():
    mycon    = psycopg2.connect(**connection_kwargs)

    visualisasi = VisualisasiController(connection=mycon)
    data = visualisasi.worldCloud()

    url = request.base_url
    split_url   = urlsplit(url)

    scheme      = split_url.scheme 
    netloc      = split_url.netloc
    port        = split_url.port

    baseUrl = scheme+'://'+netloc

    dataAll = visualisasi.loadDataPercentage()

    dataCnbc = visualisasi.loadDataPercentage('CNBC')
    dataDetik = visualisasi.loadDataPercentage('DETIK')
    dataTempo = visualisasi.loadDataPercentage('TEMPO')
    
    total_data = visualisasi.loadTotalData()

    dataReturn = {}
    dataReturn['all'] = dataAll
    dataReturn['cnbc'] = dataCnbc
    dataReturn['detik'] = dataDetik
    dataReturn['tempo'] = dataTempo
    

    featureData = visualisasi.loadDataByFeature()

    return render_template('visualization.html', data=dataReturn, fiturdata=featureData, baseUrl=baseUrl, total=total_data)

@app.route("/detailclass")
def detailclass():
    url = request.base_url
    split_url   = urlsplit(url)

    scheme      = split_url.scheme 
    netloc      = split_url.netloc
    port        = split_url.port

    baseUrl = scheme+'://'+netloc

    flagging_b = request.args.get('class')
    portal     = request.args.get('portal')

    flagging=flagging_b
    if flagging == 'negatif':
        flagging = '2'
    if flagging == 'positif':
        flagging = '1'
    if flagging == 'netral':
        flagging = '0'

    mycon    = psycopg2.connect(**connection_kwargs)

    visualisasi = VisualisasiController(connection=mycon)
    data = visualisasi.loadDataClassFlagging(flagging, portal)
    return render_template("detailclass.html", data=data,baseUrl=baseUrl, flagging=flagging_b, portal=portal)
    # return data

@app.route("/detailBerita")
def detailBerita():
    berita_id = request.args.get('berita')
    mycon    = psycopg2.connect(**connection_kwargs)

    visualisasi = VisualisasiController(connection=mycon)
    data = visualisasi.loadDataBeritaById(berita_id)
    # return data
    return render_template('berita.phtml', data=data)

@app.route('/formklasifikasi')
def formklasifikasi():
    return render_template('formklasifikasi.html')

@app.route('/parsing/<int:nilaiku>')
def parsingku(nilaiku):
    return "nilai adalah : {}".format(nilaiku)

@app.route("/parsingargument")
def ayopasing():
    data = request.args.get("nilai")
    return "nilai : {}".format(data)

@app.route("/halaman/<int:nilai>")
def session_1(nilai):
    session["nilaiku"] = nilai
    return "nilai berrhasil"

@app.route("/halaman/lihat")
def view_session_1():
    try:
        data = session["nilaiku"]
        return "nilai session : {}".format(data)
    except:
        return "session habis"

@app.route('/halaman/logout')
def logout_session_1():
    session.pop("nilaiku")
    return "berhasil logout"

@app.route("/")
def index():
    return render_template('index.html')
   
@app.route("/redirect")
def ayo_redirect():
    return redirect(url_for("about"))   

@app.route("/feature")
def feature(): 
    mycon    = psycopg2.connect(**connection_kwargs)

    p_sentence     = request.args.get('sentence')
    p_portal       = request.args.get('portal')
    p_class        = request.args.get('class')

    visualisasi = VisualisasiController(connection=mycon)

    data = visualisasi.loadDataSentence(sentence=p_sentence, p_class=p_class, p_portal=p_portal)
    # return data
    return render_template('detailfeature.html', data=data, sentence=p_sentence, p_class=p_class, p_portal=p_portal)

@app.route('/handle_klasifikasi_url', methods=['POST'])
def handle_klasifikasi_url():
    if request.method == 'POST':
        url_berita = request.form['url_berita']

        parsed = urlparse(url_berita)
        netloc = parsed.netloc

        controllerBerita = DataBeritaController()
        
        if netloc == 'www.cnbcindonesia.com':
            dataBerita = controllerBerita.getNewscnbc(url=url_berita)
            
        else:
            return 'Hanya bisa mengakses url CNBC, Detik, dan Tempo'

        mycon    = psycopg2.connect(**connection_kwargs)
        model = ModelingController(connection=mycon)

        array_result = []
        objHeader = {}
        objHeader['total_kalimat'] = len(dataBerita['arr_kalimat'])
        objHeader['total_positif'] = 0
        objHeader['total_negatif'] = 0
        objHeader['total_netral']  = 0
        
        i=0

        text_berita = '<p class="text-justify h4 p-3" style="line-height: 1.5">'

        for x in dataBerita['arr_kalimat']:
            action = model.classfication(x)
            arrayTemp = {}
            
            arrayTemp['no']              = i+1
            arrayTemp['kalimat']         = x
            arrayTemp['flagging']        = action['flagging']
            arrayTemp['after_praproses'] = action['after_praproses']

            if action['flagging'] == 'Positif':
                tmp_text =  '<span class="bg-primary text-white">'+x.strip()+'</span>'
                objHeader['total_positif'] += 1

            if action['flagging'] == 'Negatif':
                tmp_text =  '<span class="bg-danger text-white">'+x.strip()+'</span>'
                objHeader['total_negatif'] += 1

            if action['flagging'] == 'Netral':
                tmp_text =  '<span class="bg-info text-white">'+x.strip()+'</span>'
                objHeader['total_netral'] += 1

            text_berita = text_berita+' '+tmp_text

            array_result.insert(i, arrayTemp)
            i+=1

        text_berita  = text_berita+'</p>'

    return render_template("handleklasifikasi.phtml", data=array_result, dataHeader=objHeader, text_berita=text_berita)

@app.route('/handleklasifikasi', methods=['POST'])
def handle_klasifikasi():
    afterPraproses = 'ada'
    if request.method == 'POST':

        kalimat_berita = request.form['kalimat_berita']
        # print(kalimat_berita)
        controllerBerita = DataBeritaController()
        array_kalimat    = controllerBerita.tokenize(data=kalimat_berita)

        # controllerPraProses = PraprosesController()
        # array_result = []

        mycon    = psycopg2.connect(**connection_kwargs)
        visualisasi = VisualisasiController(connection=mycon)

        model = ModelingController(connection=mycon)

        array_result = []
        objHeader = {}
        objHeader['total_kalimat'] = len(array_kalimat)
        objHeader['total_positif'] = 0
        objHeader['total_negatif'] = 0
        objHeader['total_netral']  = 0

        i=0

        for x in array_kalimat:

            action = model.classfication(x)
            arrayTemp = {}
            
            arrayTemp['no']              = i+1
            arrayTemp['kalimat']         = x
            arrayTemp['flagging']        = action['flagging']
            arrayTemp['after_praproses'] = action['after_praproses']

            if action['flagging'] == 'Positif':
                objHeader['total_positif'] += 1
            if action['flagging'] == 'Negatif':
                objHeader['total_negatif'] += 1
            if action['flagging'] == 'Netral':
                objHeader['total_netral'] += 1

            array_result.insert(i, arrayTemp)
            i+=1
            
        model.worldCLoud(kalimat_berita=kalimat_berita)

    return render_template("handleklasifikasi.html", data=array_result, dataHeader=objHeader)

if __name__ == "__main__":
    app.run(debug=True)