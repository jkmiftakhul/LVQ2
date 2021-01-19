# -*- coding: utf-8 -*-
"""
Created on Fri Sep 21 22:05:22 2018

@author: USER
"""
import numpy as np
import csv
import pandas as pd
import random
import math
import time

#dataClass = [[[1.0,1.0,0.0,0.0],0],[[0.0,0.0,0.0,1.0],1]]
#dataTraining = [[[0.0,0.0,1.0,1.0],1],[[1.0,0.0,0.0,0.0],0],[[0.0,1.0,1.0,0.0],1]]

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
	while (t<=8):
		bobotRisti.append(0.5) #bobotRisti = [0.5,0.5,0.5,0.5,0.5,.5,0.5,0.5,0.5,0.5]
		bobotNonRisti.append(0.5) #bobotNonRisti = [0.5,0.5,0.5,0.5,0.5,0.5,0.5,0.5,0.5,0.5]
		t = t+1


	#inRisti = 0
	#inNonRisti = 50

	#bobotRisti = dataLatih[0]
	#bobotNonRisti = dataLatih[50]

	#print(bobotRisti)
	#print(bobotNonRisti)


	while ((Epoch < MaxEpoch) and (alfa>alfa_minimal)):
		for t in range (len(dataLatih)):
			dataHtg = np.delete(dataLatih[t], 10)
			#RistiHtg = np.delete(bobotRisti,10)
			#NonRistiHtg = np.delete(bobotNonRisti,10)
			d1=math.sqrt(sum([(a-b)**2 for a,b in zip (dataHtg, bobotRisti)]))
			d2=math.sqrt(sum([(a-b)**2 for a,b in zip (dataHtg, bobotNonRisti)]))
			 
			print(dataHtg)
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

	return(bobotRisti,bobotNonRisti)

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
		d1=math.sqrt(sum([(a-b)**2 for a,b in zip (dataHtg, bobotFRisti)]))
		d2=math.sqrt(sum([(a-b)**2 for a,b in zip (dataHtg, bobotFNonRisti)]))
		 
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
	