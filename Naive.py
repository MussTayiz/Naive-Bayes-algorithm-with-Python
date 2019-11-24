#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import pandas as pd
from pandas import DataFrame
from math import sqrt
from math import pi
from math import e
from termcolor import cprint


def Main(sinifAdi):
    dataset = pd.read_csv("data_naive.csv");
    df = DataFrame (dataset)
    liste = df.values.tolist()  ## veri setini listeye donustur [[],[]]
    
    ##{no = [35.5, 'no', 'yes', 'no', 'no', 'no', 'no', 'no'],...}
    if(sinifAdi == 'Renal Nefrit'):
        sinifaGoreAyrilmisVeriler = sinifaGoreAyir(liste, -1)
    elif(sinifAdi == 'Idrar Kesesi Iltihabi'):
        sinifaGoreAyrilmisVeriler = sinifaGoreAyir(liste, -2)
    
    ## ilk sutundaki sayısal veriler için
    evetOrt, evetSSapma = (ortalamaVeSSapma(sinifaGoreAyrilmisVeriler["yes"]))
    hayirOrt, hayirSSapma = (ortalamaVeSSapma(sinifaGoreAyrilmisVeriler["no"]))
    #print("Evet Ortalama : "+str(evetOrt) + "\nEvet Standart Sapma : " + str(evetSSapma))
    #print("Hayır Ortalama : "+str(hayirOrt) + "\nHayır Standart Sapma : " + str(hayirSSapma))
    ## sozel niteliklerde bu işlem yapılacak frekans tablosu gibi 
    
    testVerisi = liste[1]
    
    evetSicaklikDegeri = gaussDagilimHesapla(evetOrt, evetSSapma, testVerisi[0])
    #print(evetSicaklikDegeri)
    hayirSicaklikDegeri = gaussDagilimHesapla(hayirOrt, hayirSSapma, testVerisi[0])
    #print(hayirSicaklikDegeri)
     
    evetIcinCarpilacakDegerler, hayirIcinCarpilacakDegerler = sinifOranBulma(sinifaGoreAyrilmisVeriler, testVerisi, df)
    evetIcinCarpilacakDegerler.append(evetSicaklikDegeri)
    hayirIcinCarpilacakDegerler.append(hayirSicaklikDegeri)
    
    print("Evet için Carpılacak Degerler : "+str(evetIcinCarpilacakDegerler))
    print("Hayır için Carpılacak Degerler : "+str(hayirIcinCarpilacakDegerler))
    
    print("*" * 25)
    cprint("Test Verisi : "+str(testVerisi), "blue", "on_white", attrs=['bold'])
    if(sinifAdi == 'Renal Nefrit'):
        cprint("Renal pelvis kökenli nefrit sonucu : " + sonucKontrol(evetIcinCarpilacakDegerler, hayirIcinCarpilacakDegerler) ,"red", "on_white", attrs=['bold'])
    elif(sinifAdi == 'Idrar Kesesi Iltihabi'):
        cprint("İdrar Kesesi İltihabı sonucu : " + sonucKontrol(evetIcinCarpilacakDegerler, hayirIcinCarpilacakDegerler), "red", "on_white", attrs=['bold'])
    print("*" * 25)

def sonucKontrol(evetDizi, hayirDizi):
    evetSonuc = 1
    hayirSonuc = 1
    for i in evetDizi:
        evetSonuc *= i
        
    for i in hayirDizi:
        hayirSonuc *= i
    
    print("Evet Sınıfı için Hesaplanan Olasılık : " + str(evetSonuc))
    print("Hayır Sınıfı için Hesaplanan Olasılık : " + str(hayirSonuc))
    if (hayirSonuc > evetSonuc):
        return "Hayır"
    elif(evetSonuc > hayirSonuc):
        return "Evet"

def gaussDagilimHesapla(ort, ss, ornek):
    # 1/(kok(2*pi)*ss)
    ilkAsama = 1/(sqrt(2*pi)*ss)
    #print("ilk asama : " + str(ilkAsama))
    # e^((-1.2) * ((x-ort)/ss)**2)
    ikinciAsama = e**((-1/2) * (ornek-ort)**2/ss**2)
    #print(ikinciAsama)
    return (ilkAsama*ikinciAsama)
    
    # evet ve hayır için carpilacak oranlar bulunur 
def sinifOranBulma(sinifaGoreAyrilmisVeriler, testVerisi, df):
    toplamVeri = len(sinifaGoreAyrilmisVeriler["yes"]) + len(sinifaGoreAyrilmisVeriler["no"])
    evetOrani = len(sinifaGoreAyrilmisVeriler["yes"]) / toplamVeri # 50/120
    hayirOrani = len(sinifaGoreAyrilmisVeriler["no"]) / toplamVeri # 70/120  
    """
    print("evet oran : " + str(evetOrani))
    print("hayir oran : " + str(hayirOrani))
    print("Toplam yes : " + str(len(sinifaGoreAyrilmisVeriler["yes"])))
    print("Toplam no : " + str(len(sinifaGoreAyrilmisVeriler["no"])))
    """
    # nitel ozellikler icin calisir
    evetIcinCarpilacakDegerler = list()
    for i in range(1,6):
        #print(str(df.columns[i]))
        oranlar = sinifaGoreOzellikOranları(sinifaGoreAyrilmisVeriler, i, evetOrani, hayirOrani)
        #print(oranlar)
        if(testVerisi[i] == 'no'):
            evetIcinCarpilacakDegerler.append(oranlar['no|yes'])
        elif(testVerisi[i] == 'yes'):
            evetIcinCarpilacakDegerler.append(oranlar['yes|yes'])
            
    evetIcinCarpilacakDegerler.append(evetOrani)
    
    hayirIcinCarpilacakDegerler = list()
    for i in range(1,6):
        oranlar = sinifaGoreOzellikOranları(sinifaGoreAyrilmisVeriler, i, evetOrani, hayirOrani)
        if(testVerisi[i] == 'no'):
            hayirIcinCarpilacakDegerler.append(oranlar['no|no'])
        elif(testVerisi[i] == 'yes'):
            hayirIcinCarpilacakDegerler.append(oranlar['yes|no'])
    hayirIcinCarpilacakDegerler.append(hayirOrani)
    
    return evetIcinCarpilacakDegerler, hayirIcinCarpilacakDegerler
    
    
def sinifaGoreOzellikOranları(sinifaGoreAyrilmisVeriler, sutunNo, evetOrani, hayirOrani):
    # her sutun için yapılacak işler (sayısal olmayan sutunlar için)
    sonuclar = dict()
    noSay = 0
    yesSay = 0
    toplamYes = len(sinifaGoreAyrilmisVeriler["yes"])
    toplamNo = len(sinifaGoreAyrilmisVeriler["no"])
    # ---------- YES Sınıfı için -----------
    for i in sinifaGoreAyrilmisVeriler["yes"]:
        if(i[sutunNo] == "no"):
            noSay += 1
        elif(i[sutunNo] == "yes"):
            yesSay += 1
    
    # 0 durumlarını ortadan kaldırmak
    if(yesSay == 0):
        yesSay = evetOrani
        sonuclar["yes|yes"] = yesSay/(toplamYes+1)
    else:
        sonuclar["yes|yes"] = yesSay/toplamYes
    if(noSay == 0):    
        noSay = evetOrani
        sonuclar["no|yes"] = noSay/(toplamYes+1)
    else:
        sonuclar["no|yes"] = noSay/toplamYes
    
    # ---------- NO Sınıfı için -----------
    noSay = 0
    yesSay = 0
    for i in sinifaGoreAyrilmisVeriler["no"]:
        if(i[sutunNo] == "no"):
            noSay += 1
        elif(i[sutunNo] == "yes"):
            yesSay += 1
    # 0 durumlarını ortadan kaldırmak
    if(yesSay == 0):
        yesSay = hayirOrani
        sonuclar["yes|no"] = yesSay/(toplamNo+1)
    else:
        sonuclar["yes|no"] = yesSay/toplamNo
    if(noSay == 0):    
        noSay = hayirOrani
        sonuclar["no|no"] = noSay/(toplamNo+1)
    else:
        sonuclar["no|no"] = noSay/toplamNo
    
    return sonuclar
    
def ortalamaVeSSapma(dataset):
    ort = 0
    ss = 0
    for i in dataset:
        ort += i[0]
    ort = ort/len(dataset)
    
    for i in dataset:
        ss += (i[0]-ort)**2
    ss = ss/(len(dataset)-1)
    
    return ort, (sqrt(ss))

## 1 renal neftir, 2 idrar kesesi iltihabı
def sinifaGoreAyir(dataset, sinifNo):
	sinifaGoreAyrilmisVeri = dict()
	for i in range(len(dataset)):
		satir = dataset[i]
		sinifDegeri = satir[sinifNo]
		if (sinifDegeri not in sinifaGoreAyrilmisVeri):
			sinifaGoreAyrilmisVeri[sinifDegeri] = list()
		sinifaGoreAyrilmisVeri[sinifDegeri].append(satir)
	return sinifaGoreAyrilmisVeri


Main('Idrar Kesesi Iltihabi')
Main('Renal Nefrit')