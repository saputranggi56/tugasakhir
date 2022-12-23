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
from urllib.parse import urlsplit, urlunsplit


app = Flask(__name__)
app.config["SECRET_KEY"] = "TugasAkhir3411171120"
# app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///example.sqlite"
DB_HOST = "localhost"
DB_NAME = "skripsi"
DB_USER = "postgres"
DB_PASS = ""

conn    = psycopg2.connect(dbname=DB_NAME, user=DB_USER, password=DB_PASS, host=DB_HOST)

@app.route("/index")
def indexku():
    cur = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
    s = "SELECT * FROM temp_flagging"
    cur.execute(s)
    data = cur.fetchall()
    # print('masuk')
    
    nilaiku = 100

    hari = ['senin', 'selasa', 'rabu', 'kamis', 'jumat', 'sabtu', 'minggu']
    return render_template("indexold.html", value=hari, data=data)


@app.route("/visualisasi")
def visualisasi():
    visualisasi = VisualisasiController()
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
    
    dataReturn = {}
    dataReturn['all'] = dataAll
    dataReturn['cnbc'] = dataCnbc
    dataReturn['detik'] = dataDetik
    dataReturn['tempo'] = dataTempo
    

    featureData = visualisasi.loadDataByFeature()

    return render_template('visualisasi.html', data=dataReturn, fiturdata=featureData, baseUrl=baseUrl)

@app.route("/detailclass")
def detailclass():
    url = request.base_url
    split_url   = urlsplit(url)

    scheme      = split_url.scheme 
    netloc      = split_url.netloc
    port        = split_url.port

    baseUrl = scheme+'://'+netloc

    flagging = request.args.get('class')

    if flagging == 'negatif':
        flagging = '2'
    if flagging == 'positif':
        flagging = '1'
    if flagging == 'netral':
        flagging = '0'

    visualisasi = VisualisasiController()
    data = visualisasi.loadDataClassFlagging(flagging)
    return render_template("detailclass.html", data=data,baseUrl=baseUrl)
    # return data

@app.route("/detailBerita")
def detailBerita():
    berita_id = request.args.get('berita')

    return berita_id
    
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
    return render_template("index.html")

@app.route("/redirect")
def ayo_redirect():
    return redirect(url_for("about"))   

@app.route("/cek")
def coba(): 
    visualisasi = VisualisasiController()
    data = visualisasi.worldCloud()
    # print('masuk')
    return data

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
        model = ModelingController()

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