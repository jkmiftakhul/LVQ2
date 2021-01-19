import numpy as np
import pandas as pd
import math as ma
import timeit
from random import *

if __name__ == '__main__':
	from library.preprocess import *
	from library.svmseq import SVMTraining,SVMTesting,laporanNilai

	####BACA DATA
	#dataset = pd.read_csv('data/kanker1881_100_1096.csv',delimiter=';')
	dataset = pd.read_csv('1881_dtset_baru_hasilranking.csv')

	#dataX = dataset.iloc[:,1:]
	dataX = dataset.iloc[:,:1881]
	dataX = np.array(dataX)
	dataX = MinMax(dataX,0,1)
	#print(dataX)

	#labelX = dataset.iloc[:,0]
	labelX = dataset.iloc[:,1881]
	labelX = np.array(labelX)

	####KONVERSI LABEL
	label = konversi_label(labelX,"breast","normal")
	#print(label)

	mulai_waktu = timeit.default_timer()

	####INPUTAN
	gammas = 0.0005#float(input("Masukkan Gamma : ")) #kecepatan training, ga ngaruh
	lamdas = 0.05#float(input("Masukkan Lamda : ")) #??, but ngaruh
	Cs = 0.0005#float(input("Masukkan C : ")) #C -> penalti, makin besar C nya, makin besar penaltinya
	epsilons = 0.000001#float(input("Masukkan Epsilon(Max Error) : "))
	
	###KFOLD
	kf =  10 #int(input("Masukkan K : "))
	####1.MISAHIN DATA SESUAI LABEL
	dataPos = []
	dataNeg = []
	#dataPos
	for i in range(len(dataX)):
		if ((label[i] == 1)):
			dataPos.append(i)
	dataPos = np.array(dataPos) #berisi index data2 yang berlabel positif
	print("banyak data label 1 :",len(dataPos))

	#dataNeg
	for i in range(len(dataX)):
		if (label[i] == -1):
			dataNeg.append(i)
	dataNeg = np.array(dataNeg) #berisi index data2 yang berlabel negatif
	print("banyak data label 2 :",len(dataNeg))

	###2. Ngeshuffle datanya
	# dataPos = list(dataPos)
	# dataPos = sample(dataPos, len(dataPos))
	# dataNeg = list(dataNeg)
	# dataNeg = sample(dataNeg, len(dataNeg))

	###3.Bikin list sejumlah K
	KFold = []
	for i in range(kf):
		KFold.append([])

	###4. mendistribusikan + dan - ke wadah
	#dataPos
	j = 0
	for i in range(len(dataPos)):
		if (j != (kf-1)):
			KFold[j].append(dataPos[i])
			j = j + 1
		else:
			KFold[j].append(dataPos[i])
			j = 0

	#dataNeg
	o = 0
	for i in range(len(dataNeg)):
		if (o != (kf-1)):
			KFold[o].append(dataNeg[i])
			o = o + 1
		else:
			KFold[o].append(dataNeg[i])
			o = 0

	#print(KFold)

	###5. masuk perulangan, menentukan mana data test mana data training, lalu di training dan testing
	k = 0
	akur = []
	sensi = []
	spesi = []
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
		#print("dataset : \n",train)

		###5.3 melakukan pelatihan dan pengetesan
		dataTrain = []
		labelTrain = []
		for i in range(len(train)):
			dataTrain.append(dataX[train[i]])
			labelTrain.append(label[train[i]])
		dataTrain = np.array(dataTrain)
		labelTrain = np.array(labelTrain)

		dataTest = []
		labelTest = []
		#Scan label test untuk sub dataset yg baru
		dataPositif = [] #berisi index test data2 yang berlabel positif
		dataNegatif = [] #berisi index test data2 yang berlabel negatif

		for i in range(len(test)):
			dataTest.append(dataX[test[i]])
			labelTest.append(label[test[i]])

			if (label[test[i]] == 1) :
				dataPositif.append(i) #bentuk list
			else :
				dataNegatif.append(i) #bentuk list

		dataTest = np.array(dataTest)
		labelTest = np.array(labelTest)

		(support,alpha) = SVMTraining(dataTrain,labelTrain,gammas,lamdas,Cs,epsilons,500)
		(Accur,predic) = SVMTesting(dataTrain,labelTrain,dataTest,labelTest,alpha,support,lamdas)
		(sensit,spesif,EL) = laporanNilai(predic,labelTest,dataPositif,dataNegatif)

		akur.append(round(Accur))
		sensi.append(round(sensit))
		spesi.append(round(spesif))
		#print("\n\n")
		
		k = k + 1

	selesai_waktu = timeit.default_timer()
	jadinya = round(selesai_waktu - mulai_waktu ,4)

	for i in range(len(akur)):
		print("\nFold-",i+1,"== Akurasi :",akur[i],"%, Sensitifitas :",sensi[i],"%, Spesifisitas :",spesi[i], "%")
	print('\nRata-rata Akurasi : %.2f' % np.average(akur),'%')
	print('Rata-rata Sensitifitas : %.2f' % np.average(sensi),'%')
	print('Rata-rata Spesifisitas : %.2f' % np.average(spesi),'%')
	print('\nwaktunya : ',jadinya)
	print('treshold : 0')
