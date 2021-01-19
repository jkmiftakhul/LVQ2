from flask import render_template, request, redirect, url_for, flash,  session, abort, make_response, send_file

from app import app

import mysql.connector
import csv
import pickle
import timeit
import json
from math import sqrt
from random import randrange
from random import seed
from csv import reader
import numpy as np
import pandas as pd
#=============================================================================================================================#
db = mysql.connector.connect(
  host="localhost",
  user="root",
  passwd="",
  database="db_deteksiristi"
)

if db.is_connected():
  print("Berhasil terhubung ke database")

#=============================================================================================================================#
@app.route('/login', methods=['GET', 'POST'])
def login():
    # Output message if something goes wrong...
    msg = ''
    # Check if "username" and "password" POST requests exist (user submitted form)
    if request.method == 'POST'and 'username' in request.form and 'password' in request.form:
        # Create variables for easy access
        username = request.form['username']
        password = request.form['password']
        # Check if account exists using MySQL
        cursor = db.cursor()
        cursor.execute('SELECT * FROM admin WHERE username = %s AND password = %s', (username, password))
        # Fetch one record and return result
        account = cursor.fetchone()
        # If account exists in accounts table in out database
        if account:
            # Create session data, we can access this data in other routes
            session['loggedin'] = True
            session['id'] = account[0]
            session['username'] = account[1]
            # Redirect to home page
            return redirect(url_for('home'))
        else:
            # Account doesnt exist or username/password incorrect
            msg = 'Incorrect username/password!'
    # Show the login form with message (if any)
    return render_template('login.html', msg=msg)
#=============================================================================================================================#
@app.route('/dashboard') #index BACKEND
def home():
# Check if user is loggedin
    if 'loggedin' in session:
        # User is loggedin show them the home page
        return render_template('dashboard.html', username=session['username'], active='dashboard')
    # User is not loggedin redirect to login page
    return redirect(url_for('login'))
#=============================================================================================================================#
@app.route('/') #index FRONTEND
def index2():
    return render_template("indexhome.html")
		
#=============================================================================================================================#
#@app.route('/index')
#def index():
    #pageData = {
        #"breadcrumb": "Dashboard",
        #"pageHeader": "Dashboard",
        #"pages": "dashboard.html"
    #}
    #return render_template("index.html", pageData=pageData)
	
#=============================================================================================================================#
@app.route('/jst')
def jst():
    return render_template("jst.html")
	
#=============================================================================================================================#	
def pelatihan (alfa,alfa_minimal,MaxEpoch,Epoch,window,dataLatih,target):

	#variabel array untuk data Risti dan non Risti
	dataRisti = []
	dataNonRisti = []

	#memisahkan kelas bobot 1 dan 2
	for i in range(len(dataLatih)):
		if(target[i]==1):
			dataRisti.append(i)
		elif(target[i]==0):
			dataNonRisti.append(i)

	#print(dataRisti)
	#print(dataNonRisti)

	bobotRisti=[]
	bobotNonRisti=[]

	t=0
	i=0
	while (t<=9):
		bobotRisti.append(0.5) #bobotRisti = [0.5,0.5,0.5,0.5,0.5,.5,0.5,0.5,0.5,0.5]
		bobotNonRisti.append(0.5) #bobotNonRisti = [0.5,0.5,0.5,0.5,0.5,0.5,0.5,0.5,0.5,0.5]
		t = t+1


	#inRisti = 0
	#inNonRisti = 50

	#bobotRisti = dataLatih[0]
	#bobotNonRisti = dataLatih[50]

	print(bobotRisti)
	print(bobotNonRisti)


	while ((Epoch < MaxEpoch) and (alfa>alfa_minimal)):
		for t in range (len(dataLatih)):
			dataHtg = np.delete(dataLatih[t], 10)
			#RistiHtg = np.delete(bobotRisti,10)
			#NonRistiHtg = np.delete(bobotNonRisti,10)
			d1=sqrt(sum([(a-b)**2 for a,b in zip (dataHtg, bobotRisti)]))
			d2=sqrt(sum([(a-b)**2 for a,b in zip (dataHtg, bobotNonRisti)]))
			 
			#print(dataHtg)
			#print(d1)
			#print(d2)


			if(d1<=d2): #di<=d2?
				menang = "risti"
				Cj = 1
			else:
				menang = "nonristi"
				Cj = 0
				#Selesai mendapatkan j minimum
			#Update bobot
			target = dataLatih[t][10]                                                                                                       
			#Cek Kondisi T=Cj untuk Update Bobot wj
			if(target==Cj):
				if(menang=="risti"):
					print("ini",len(dataHtg))
					print("itu",len(bobotRisti))
					#bobotRisti
					for i in range(len(dataHtg)):
						bobotRisti[i]=bobotRisti[i]+(alfa*(dataHtg[i]-bobotRisti[i]))
				else:
					#bobotNonRisti
					for i in range(len(dataHtg)):
						bobotNonRisti[i]=bobotNonRisti[i]+(alfa*(dataHtg[i]-bobotNonRisti[i]))
			#else:
				#print ("eeee")
			#Cek Kondisi T=!Cj 			
			else:
				if(d1<=d2): #di<=d2?
					menang = "risti"
					dc=d1
					dr=d2
					Cj = 1
				else:
					menang = "nonristi"
					dc=d2
					dr=d1
					Cj = 0
					
			#print(bobotRisti)
			#print(bobotRisti)

			#kondisi jika T!=Cj, lakukan :
			#cek kondisi window
				if(((dc/dr)>(1-window)) and ((dr/dc)<(1+window))) :
				#window true 
				#update w1 dan w2
				#wj yang tidak merepresentasikan kelas vektor input x
				#wj yang merepresentasikan kelas vektor input x
					for i in range(len(dataHtg)):
						if(menang=="risti"):
						#bobotRisti
							bobotRisti[i]= bobotRisti[i]-(alfa*(dataHtg[i]-bobotRisti[i]))
							bobotNonRisti[i]= bobotNonRisti[i]+(alfa*(dataHtg[i]-bobotNonRisti[i]))				
							
						else:
						#bobotNonRisti
							bobotRisti[i]=bobotRisti[i]+(alfa*((dataHtg[i]-bobotRisti[i])))
							bobotNonRisti[i]=bobotNonRisti[i]-(alfa*(dataHtg[i]-bobotNonRisti[i]))				
						#wj yang merepresentasikan kelas vektor input x
						#selesai window true
						
				else:
				#Jika window false, maka lakukan update bobot pada wj:
					if(menang=="risti"):
						#bobotRisti
						for i in range(len(dataHtg)):
							bobotRisti[i]=bobotRisti[i]-(alfa*(dataHtg[i]-bobotRisti[i]))
					else:
						#bobotNonRisti
						for i in range(len(dataHtg)):
							bobotNonRisti[i]=bobotNonRisti[i]-(alfa*(dataHtg[i]-bobotNonRisti[i]))
		#selesai per data
						
		#break
		#print("Epoch ke - ", Epoch,"\n")
		alfa = alfa-(0.1*alfa)
		alfa_akhir = alfa
		#print("alfa akhir : ", alfa_akhir)
					
		#print("\nUpdatee:")
		#print(bobotRisti)
		#print("\n")
		#print(bobotNonRisti)
		#print("\n\n\n")
		Epoch = Epoch + 1
		epoch_akhir = Epoch

	return(bobotRisti,bobotNonRisti, epoch_akhir)
#=============================================================================================================================#

#pengujian
def pengujian(datauji,bobotFRisti,bobotFNonRisti):

	#inialisasi confusion matriks
	TP = 0
	FN = 0
	FP = 0
	TN = 0

	#Lakukan pengujian lvq2 untuk setiap data uji
	for t in range(len(datauji)): #($t=1;$t<=$jumlah_data_uji;$t++){
	#Menghitung euclidean distance
		dataHtg = np.delete(datauji[t], 10)
		d1=sqrt(sum([(a-b)**2 for a,b in zip (dataHtg, bobotFRisti)]))
		d2=sqrt(sum([(a-b)**2 for a,b in zip (dataHtg, bobotFNonRisti)]))
		 
		#print(dataHtg)
		#print(d1)
		#print(d2)


		if(d1<=d2): #di<=d2?
			menang = "risti"
			Cj = 1
		else:
			menang = "nonristi"
			Cj = 0                                                                                     
		#Selesai mendapatkan j minimum
		
		#print("\ndatauji ke-",t)
		#print("target :",datauji[t][10])
		#print("klasifikasi",Cj)
		
		#confusion matriks
		if((datauji[t][10]==1)and(Cj==1)):
			TP=TP+1
		elif((datauji[t][10]==1)and(Cj==0)):
			FN=FN+1
		elif((datauji[t][10]==0)and(Cj==1)):
			FP=FP+1
		else:
			TN=TN+1
		
		#selesai confusion matrix

	#Selesai Pengujian lvq2

	#performansi dalam 1 fold
	akurasi=((TP+TN)/(TP+FN+FP+TN))*100
	error=((FP+FN)/(TP+FN+FP+TN))*100
	sensitivitas=((TP)/(TP+FN))*100
	spesifisitas=((TN)/(FP+TN))*100
	#selesai akurasi dan error 1 fold 

	return(akurasi,error,sensitivitas,spesifisitas)
#=============================================================================================================================#
#Normal
def MinMax(dats,dataMin,dataMax) :
	
	#Mencari min dan max dalam variabel dan menyiapkan perhitungan lain
	doldol = 1 - 0
	daldal = dataMax - dataMin
		
	yeah =  0.8*(dats - dataMin)
	haha = ((yeah/daldal)*doldol)+0.1

	dataBaru = haha
	
	return dataBaru

def konversi_label(data) :
	labeldata = [] #bentuk list
	for i in range(len(data)):
		if (data[i][7].lower() == "tidak aborsi"):
			data[i][7] = 1
		elif(data[i][7].lower()=="aborsi"):
			data[i][7] = 0
		else:
			data[i][7] = 5
			
		if (data[i][9].lower() == "tidak ada riwayat"):
			data[i][9] = 0
		elif(data[i][9].lower()=="ada riwayat"):
			data[i][9] = 1
		else:
			data[i][9] = 5
			
		if (data[i][10].lower() == "tidak risiko"):
			data[i][10] = 1
		elif(data[i][10].lower()=="risiko"):
			data[i][10] = 2
		else:
			data[i][10] = 5

	return labeldata #bentuk list
	
#=============================================================================================================================#
@app.route('/pelatihandanpengujian') 
def form_proses():
    # Check if user is loggedin
	if 'loggedin' in session:
		#User is loggedin show them the page
		return render_template('pelatihandanpengujian.html', active='proses')
	# User is not loggedin redirect to login page
	return redirect(url_for('login'))
#=============================================================================================================================#
	
@app.route('/hasilpelatihandanpengujian', methods=['POST'])
def pelatihandanpengujian():
	if request.method == 'POST':
		alfa = float(request.form['alfa'])
		alfa_minimal = float(request.form['alfa_minimal'])
		MaxEpoch = int(request.form['Max_Epoch'])
		window = float(request.form['Window'])
		
		#1 Menginisialisasi nilai alfa, epsilon, epoch, maxepoch, window
		Epoch = 0
		
		#Mengupload file csv
		data1 = pd.read_csv('data_bumil.csv', header=None) # Data Training

		#memisahkan data target kelas pada data pelatihan
		target = data1.iloc[:,10] #target ada di kolom ke 10
		target = target.tolist() #membuat list
		dataset = np.array(data1) #membuat array

		#KFOLD
		kf = int(request.form['kfold'])
		
		cursor = db.cursor()
		cursor.execute("INSERT INTO data_hasil(id_datahasil, kfold, alfa, eps, window, max_epoch, w1_akhir, w2_akhir) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)",('',kf,alfa,alfa_minimal, window, MaxEpoch,'',''))
		id_ini = cursor.lastrowid
		db.commit()
		
		mulai_waktu = timeit.default_timer()
		
		####1.MISAHIN DATA SESUAI LABEL
		#variabel array untuk data Risti dan non Risti
		dataRisti = []
		dataNonRisti = []

		#memisahkan kelas bobot 1 dan 2
		for i in range(len(dataset)):
			if(target[i]==1):
				dataRisti.append(i)
			elif(target[i]==0):
				dataNonRisti.append(i)

		###3.Membuat list sejumlah K
		KFold = []
		for i in range(kf):
			KFold.append([])

		###4. mendistribusikan risti dan nonristi ke wadah
		#dataRisti
		j = 0
		for i in range(len(dataRisti)):
			if (j != (kf-1)):
				KFold[j].append(dataRisti[i])
				j = j + 1
			else:
				KFold[j].append(dataRisti[i])
				j = 0

		#dataNonRisti
		o = 0
		for i in range(len(dataNonRisti)):
			if (o != (kf-1)):
				KFold[o].append(dataNonRisti[i])
				o = o + 1
			else:
				KFold[o].append(dataNonRisti[i])
				o = 0

		###5. masuk perulangan, menentukan mana data test mana data training, lalu di training dan testing
		k = 0
		akur = []
		sensi = []
		spesi = []
		err = []
		while(k != kf):
			###5.1 menentukan data test
			test = KFold[k]
			#print("fold ke-",k+1)
			#print("datatest : \n",test)

			###5.2 menentukan data training
			train = []
			for i in range(kf):
				if(i != k):
					train = train + KFold[i]

			###5.3 melakukan pelatihan dan pengujian
			dataTrain = []
			targetTrain = []
			for i in range(len(train)):
				dataTrain.append(dataset[train[i]])
				targetTrain.append(target[train[i]])
			dataTrain = np.array(dataTrain)
			targetTrain = np.array(targetTrain)

			datauji = []
			for i in range(len(test)):
				datauji.append(dataset[test[i]])

			datauji = np.array(datauji)

			(bobotFRisti,bobotFNonRisti, epoch_akhir) = pelatihan(alfa,alfa_minimal,MaxEpoch,Epoch,window,dataTrain,targetTrain)
			(akurasi,error,sensitivitas,spesifisitas) = pengujian(datauji,bobotFRisti,bobotFNonRisti)

			akur.append(round(akurasi))
			sensi.append(round(sensitivitas))
			spesi.append(round(spesifisitas))
			err.append(round(error))
			#print("\n\n")

			#untuk ganti fold
			k = k + 1

		selesai_waktu = timeit.default_timer()
		jadinya = round(selesai_waktu - mulai_waktu ,4)
		epoch_akhir = epoch_akhir
		print ("epoch terakhir: \n \n ", epoch_akhir)
		
		hasilnya = np.average(akur)
		hasilnya2 = np.average(sensi)
		hasilnya3 = np.average(spesi)
		hasilnya4 = np.average(err)
		#print (kf, alfa, alfa_minimal)
		
		rtakurasi = float(hasilnya.item())
		rtsensi = float(hasilnya2.item())
		rtspesi = float(hasilnya3.item())
		rterror = float(hasilnya4.item())
		
		bobotFRisti = json.dumps(bobotFRisti)
		bobotFNonRisti = json.dumps(bobotFNonRisti)
		
		cursor = db.cursor()
		cursor.execute("UPDATE data_hasil SET akurasi=%s, spesivitas=%s, sensitivitas=%s, error_rate=%s, w1_akhir=%s, w2_akhir=%s, total_epoch = %s, runtime=%s WHERE id_datahasil=%s",( rtakurasi, rtspesi, rtsensi, rterror, bobotFRisti, bobotFNonRisti, epoch_akhir, jadinya, id_ini))
		db.commit()
		
		akur = json.dumps(akur)
		err = json.dumps(err)
		sensi = json.dumps(sensi)
		spesi = json.dumps(spesi)
		
		cursor = db.cursor()
		cursor.execute("INSERT INTO kfold(id_datahasil, akurasi, errorrate, sensitivitas, spesifitas) VALUES (%s, %s, %s, %s, %s)",(id_ini, akur, err, sensi, spesi))
		db.commit()
		
		bobotFRisti = np.array(json.loads(bobotFRisti))
		bobotFNonRisti = np.array(json.loads(bobotFNonRisti))
		akur = np.array(json.loads(akur))
		err = np.array(json.loads(err))
		sensi = np.array(json.loads(sensi))
		spesi = np.array(json.loads(spesi))
		
		return render_template('hasilpelatihandanpengujian.html', akur = hasilnya, listakur = akur,
            sensi = hasilnya2, listsensi = sensi, spesi = hasilnya3, listspesi = spesi, err = hasilnya4, listerror = err, kfold = kf, alfa = alfa, alfa_minimal= alfa_minimal, Max_Epoch = MaxEpoch, Window = window, listbobotFRisti=bobotFRisti ,listbobotFNonRisti=bobotFNonRisti, runtime = jadinya)

#=============================================================================================================================#

@app.route('/hasilpelatihandanpengujian')
def hasilpelatihandanpengujian():	
	# Check if user is loggedin
	if 'loggedin' in session:
		# User is loggedin show them the home page
		return render_template("hasilpelatihandanpengujian.html")    
    # User is not loggedin redirect to login page
	return redirect(url_for('login'))

#=============================================================================================================================#
@app.route('/hapus_hasil/<string:id_datahasil>', methods=['GET'])
def hapus_hasil(id_datahasil):
	cursor = db.cursor()
	cursor.execute("DELETE FROM data_hasil WHERE id_datahasil=%s",(id_datahasil,))
	db.commit()
	cursor.close()
	
	flash('Informasi hasil proses berhasil dihapus!')
	return redirect('/riwayathasil')
	
#==========================================================================================================================#
@app.route("/riwayathasil") #Simpan
def riwayat_hasil():
	# Check if user is loggedin
	if 'loggedin' in session:
		# User is loggedin show them the home page
		cursor = db.cursor()
		cursor.execute("SELECT * from data_hasil ORDER BY id_datahasil desc")
		results = cursor.fetchall()
		cursor.close()
		
		return render_template('riwayat_hasil.html', data=results, active='riwayat')
	# User is not loggedin redirect to login page
	return redirect(url_for('login'))
#=============================================================================================================================#

@app.route('/lihat_detail/<string:id_datahasil>', methods=['GET'])
def lihat_detail(id_datahasil):
	cursor = db.cursor()
	cursor.execute("SELECT * from kfold WHERE id_datahasil=%s", (id_datahasil,))
	daftar = cursor.fetchone()
	
	akurasi = daftar[2]
	errorrate= daftar[3]
	sensitivitas = daftar[4]
	spesifisitas= daftar[5]
	
	akur = np.array(json.loads(akurasi))
	err = np.array(json.loads(errorrate))
	sensi = np.array(json.loads(sensitivitas))
	spesi = np.array(json.loads(spesifisitas))
	
	cursor = db.cursor()
	cursor.execute("SELECT * from data_hasil WHERE id_datahasil=%s", (id_datahasil,))
	daftar = cursor.fetchone()
	
	kfold = daftar[1]
	alfa = daftar[2]
	eps = daftar[3]
	window = daftar[4]
	max_epoch = daftar[5]
	bobotFRisti = daftar[6]
	bobotFNonRisti = daftar[7]
	rtakurasi = daftar[8]
	rterror = daftar[9]
	rtsensi = daftar[11]
	rtspesi = daftar[10]
	runtime = daftar[13]
	
	bobotFRisti = np.array(json.loads(bobotFRisti))
	bobotFNonRisti = np.array(json.loads(bobotFNonRisti))
	db.commit()
	cursor.close()
	
	
	
	return render_template("lihat_detail.html", listakur = akur, listsensi = sensi, listerror = err, listspesi = spesi, akur=rtakurasi, err = rterror, sensi = rtsensi, spesi=rtspesi, listbobotFRisti=bobotFRisti ,listbobotFNonRisti=bobotFNonRisti, runtime = runtime, kfold=kfold, alfa=alfa, eps=eps, window=window, max_epoch=max_epoch)

#=============================================================================================================================#

#=============================================================================================================================#	
@app.route('/lihat_bobot')
def pilihbobotdeteksi2():
	cursor = db.cursor()
	sql = ("SELECT * from data_hasil")
	cursor.execute(sql)
	results = cursor.fetchall()
	cursor.close()
	
	return render_template("lihat_bobot.html", data=results)
#=============================================================================================================================#	

@app.route('/bobotterpilih2/<string:id_datahasil>', methods=["GET"])
def bobotterpilih2(id_datahasil):
	cursor = db.cursor()
	cursor.execute("UPDATE data_hasil SET status=%s WHERE id_datahasil=%s", ("sudah",id_datahasil,))
	daftar = cursor.fetchone()

	db.commit()
	cursor.close()
	
	flash('Bobot Deteksi Telah Terpilih!')
	return redirect('/lihat_bobot?id_datahasil='+str(id_datahasil)+'&status=sudah')
	
#=============================================================================================================================#
#=============================================================================================================================#	
@app.route('/pilihbobot')
def pilihbobotdeteksi():
	# Check if user is loggedin
	if 'loggedin' in session:
		# User is loggedin show them the home page
		cursor = db.cursor()
		sql = ("SELECT * from data_hasil")
		cursor.execute(sql)
		results = cursor.fetchall()
		cursor.close()
		
		return render_template("pilihbobot.html", data=results, active='pilih')
	# User is not loggedin redirect to login page
	return redirect(url_for('login'))
#=============================================================================================================================#
@app.route('/bobotterpilih/<string:id_datahasil>', methods=["GET"])
def bobotterpilih(id_datahasil):
	cursor = db.cursor()
	cursor.execute("SELECT * from data_hasil WHERE id_datahasil=%s", (id_datahasil,))
	daftar = cursor.fetchone()
	
	bobotFRistiF = daftar[6]
	bobotFNonRistiRistiF = daftar[7]
	print (bobotFRistiF)
	print (bobotFRistiF)
	print ("\n", id_datahasil)
	
	
	db.commit()
	cursor.close()
	
	#cursor = db.cursor()
	#cursor.execute("INSERT INTO bobot_terpilih(id_datahasil, w1_terpilih, w2_terpilih) VALUES (%s, %s, %s)",(id_datahasil, bobotFRistiF, bobotFNonRistiRistiF))
	#db.commit()
	#cursor.close()

	cursor = db.cursor()
	cursor.execute("UPDATE bobot_terpilih SET id_datahasil=%s, w1_terpilih=%s, w2_terpilih=%s WHERE id_bobot=0",(id_datahasil, bobotFRistiF, bobotFNonRistiRistiF))
	db.commit()
	cursor.close()
	
	flash('Bobot Deteksi Telah Terpilih!')
	return redirect('/pilihbobot')

#=============================================================================================================================#
@app.route('/tampilbobotterpilih')
def tampilkanbobot():
	# Check if user is loggedin
	if 'loggedin' in session:
		# User is loggedin show them the home page
		cursor = db.cursor()
		cursor.execute("SELECT d.kfold, alfa, eps, window, max_epoch, akurasi, error_rate, spesivitas, sensitivitas, runtime, b.w1_terpilih, w2_terpilih FROM data_hasil d, bobot_terpilih b WHERE d.id_datahasil = b.id_datahasil ")
		results = cursor.fetchall()
		cursor.close()
		
		return render_template("bobotterpilih.html", data = results, active='tampil')
	# User is not loggedin redirect to login page
	return redirect(url_for('login'))
#=============================================================================================================================#
@app.route('/form_deteksi')
def formdeteksi():
	return render_template("form_deteksi.html")
#=============================================================================================================================#
@app.route('/hasildeteksi', methods=['POST'])
def deteksi():
	if request.method == 'POST':
		umur = float(request.form['umur'])
		hamilke = float(request.form['hamilke'])
		riwayatabor = float(request.form['riwayatabor'])
		lila = float(request.form['lila'])
		tb = float(request.form['tb'])
		bb = float(request.form['bb'])
		jp = float(request.form['jp'])
		cp = float(request.form['cp'])
		hb = float(request.form['hb'])
		rp = float(request.form['rp'])
		
	hasil_umur = MinMax(umur, 18, 44)
	hasil_hamilke = MinMax(hamilke, 1, 8)
	hasil_riwayatabor = MinMax(riwayatabor, 0, 3)
	hasil_lila = MinMax(lila, 22,40)
	hasil_tb = MinMax(tb, 143, 165)
	hasil_bb = MinMax(bb, 39.6, 95)
	hasil_jp = MinMax(jp, 0, 216)
	hasil_cp = cp
	hasil_hb = MinMax(jp, 8.2, 16.4)
	hasil_rp = rp
	
	
	cursor = db.cursor()
	cursor.execute("SELECT * from bobot_terpilih WHERE id_bobot=0")
	daftar = cursor.fetchone()
	
	bobotFRistiF = daftar[2]
	bobotFNonRistiF = daftar[3]
	
	#print("\n ini Risti dari db: ",bobotFRistiF)
	#print("\n ini Non Risti dari db: ",bobotFNonRistiF)
	
	bobotFRisti = np.array(json.loads(bobotFRistiF))
	bobotFNonRisti = np.array(json.loads(bobotFNonRistiF))
	
	#print("\n ini setelah di JSON: ",bobotFRisti)
	#print("\n ini setelah di JSON: ",bobotFNonRisti)
	
	data = [hasil_umur, hasil_hamilke, hasil_riwayatabor, hasil_lila, hasil_tb, hasil_bb, hasil_jp, hasil_cp, hasil_hb, hasil_rp]
	print ("\n ini data deteksi: ",data)
	datadeteksi = np.array(data)
	print ("\n ini data deteksi: ",datadeteksi)
	d1=sqrt(sum([(a-b)**2 for a,b in zip (datadeteksi, bobotFRisti)]))
	d2=sqrt(sum([(a-b)**2 for a,b in zip (datadeteksi, bobotFNonRisti)]))
	
	if(d1<=d2): #di<=d2?
		menang = "Kehamilan Berisiko Tinggi"
		Cj = 2
	else:
		menang = "Kehamilan Tidak Berisiko Tinggi"
		Cj = 1                                                                                     
		#Selesai mendapatkan j minimum
	
	print("klasifikasi",Cj)
	
	hasil = menang
	
	return render_template("hasildeteksi.html", tampilkan = hasil)
#=============================================================================================================================#

#=============================================================================================================================#
# http://localhost:5000/python/logout - this will be the logout page
@app.route('/logout')
def logout():
    # Remove session data, this will log the user out
   session.pop('loggedin', None)
   session.pop('id', None)
   session.pop('username', None)
   # Redirect to login page
   return redirect(url_for('login'))
#=============================================================================================================================#	
@app.route('/tentangkami')
def tentangkami():
    return render_template("tentangkami.html")
	
#=============================================================================================================================#
@app.route('/lihatdata')
def lihatdatagejala():
	# Check if user is loggedin
	if 'loggedin' in session:
	# User is loggedin show them the page
		cursor = db.cursor()
		sql = "SELECT * FROM bumil"
		cursor.execute(sql)
		results = cursor.fetchall()
		cursor.close()
		return render_template("datagejala.html", data=results, active='lihatdata')
	# User is not loggedin redirect to login page
	return redirect(url_for('login'))
#=============================================================================================================================#

@app.route('/upload')
def upload():
    return render_template("upload.html")

#=============================================================================================================================#

@app.route('/gantipassword', methods=["GET, POST"] )
def ganti():
	msg = ''
	# Check if user is loggedin
	if request.method == 'POST' :
		password = request.form['password']
		
		cursor = db.cursor()
		cursor.execute('SELECT * FROM admin WHERE username = "admin" AND password = %s', ( password))
		# Fetch one record and return result
		account = cursor.fetchone()
		
		id = account[0]
		#username =
		if account:
            # Create session data, we can access this data in other routes
			session['loggedin'] = True
			session['id'] = account[0]
			session['username'] = account[1]
			cursor = db.cursor()
			cursor.execute("UPDATE admin SET password=%s WHERE id=account[0] ", (account[0]))
			daftar = cursor.fetchone()
			
			db.commit()
			cursor.close()
            # Redirect to home page
			flash('Password telah diganti!')
			return redirect('/kelolaakun', active='akun')
		else:
            # Account doesnt exist or username/password incorrect
			msg = 'Ulangi ganti password!'
		# Show kelolaakun form with message (if any
			return render_template('kelolaakun.html', msg=msg)
        
		#return render_template("kelolaakun.html", active='akun')
	
	# User is not loggedin redirect to login page
	#return redirect(url_for('login'))

#=============================================================================================================================#
@app.route('/kelolaakun' )
def akun():
	# Check if user is loggedin
	return render_template("kelolaakun.html", active='akun')
	
		#return render_template("kelolaakun.html", active='akun')
	
	# User is not loggedin redirect to login page
	#return redirect(url_for('login'))

#=============================================================================================================================#
@app.errorhandler(404)
def notfound(error):
    return render_template("404.html")