import timeit

if __name__ == '__main__':
	from lvqmifta import *
	
	#1 Menginisialisasi nilai alfa, epsilon, epoch, maxepoch, window
	alfa = 0.04 #=float(input("Masukkan alfa : ")
	alfa_minimal = float(input("Masukkan alfa_minimal : "))
	MaxEpoch= 500
	Epoch = 0
	window = 0.3

	#Mengupload file csv 
	data1 = pd.read_csv('data_bumil2.csv', header=None) # Data Training
	
	#memisahkan data target kelas pada data pelatihan
	target = data1.iloc[:,10] #target ada di kolom ke 10
	target = target.tolist() #membuat list 
	dataset = np.array(data1) #membuat array

	#KFOLD
	kf = 4  #int(input("Masukkan K : "))
	
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

	###3.Bikin list sejumlah K
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

	#print(KFold)

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
		#print("dataset : \n",train)

		###5.3 melakukan pelatihan dan pengetesan
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

		(bobotFRisti,bobotFNonRisti) = pelatihan(alfa,alfa_minimal,MaxEpoch,Epoch,window,dataTrain,targetTrain)
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

	for i in range(len(akur)):
		print("\nFold-",i+1,"== Akurasi :",akur[i],"%, Sensitifitas :",sensi[i],"%, Spesifisitas :",spesi[i], "%")
	print('\nRata-rata Akurasi : %.2f' % np.average(akur),'%')
	print('Rata-rata Sensitifitas : %.2f' % np.average(sensi),'%')
	print('Rata-rata Spesifisitas : %.2f' % np.average(spesi),'%')
	print('\nwaktunya : ',jadinya)
