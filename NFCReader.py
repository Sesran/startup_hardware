#!/usr/local/bin/python
#-*-coding: utf-8 -*-


import nxppy
import time 
import requests
import json
import random
import pygame.mixer
#import RPi.GPIO as GPIO

###SETUP GPIO######
#GPIO.setmode(GPIO.BOARD)
#GPIO.setup(40,GPIO.OUT)


#GPIO.setup(12, GPIO.OUT, initial=GPIO.LOW)


moyenPaiement = ["espece", "carte", "cheque"]
articles = [
    { "nom" : "pain",  "prix_unitaire" : 0.8, "quantite" : 1, "montant" : 0.8, "categorie" : "alimentaire"},
    { "nom" : "eau 1L",  "prix_unitaire" : 0.3, "quantite" : 6, "montant" : 1.8, "categorie" : "alimentaire"},
    { "nom" : "camembert",  "prix_unitaire" : 3.0, "quantite" : 1, "montant" : 3.0, "categorie" : "alimentaire"},
    { "nom" : "banane",  "prix_unitaire" : 0.4, "quantite" : 5, "montant" : 2.0, "categorie" : "alimentaire"},
    { "nom" : "shampoing",  "prix_unitaire" : 1.50, "quantite" : 1, "montant" : 1.5, "categorie" : "hygiene"},
    { "nom" : "dentifrice",  "prix_unitaire" : 2.0, "quantite" : 1, "montant" : 2.0, "categorie" : "hygiene"},
    { "nom" : "deodorant",  "prix_unitaire" : 3.0, "quantite" : 2, "montant" : 6.0, "categorie" : "hygiene"},
    { "nom" : "mouchoirs",  "prix_unitaire" : 0.8, "quantite" : 1, "montant" : 0.8, "categorie" : "hygiene"},
    { "nom" : "pelle",  "prix_unitaire" : 20.0, "quantite" : 1, "montant" : 20.0, "categorie" : "loisir"},
    { "nom" : "ballon",  "prix_unitaire" : 15.0, "quantite" : 1, "montant" : 15.0, "categorie" : "loisir"},
    { "nom" : "raquette",  "prix_unitaire" : 50.0, "quantite" : 1, "montant" : 50.0, "categorie" : "loisir"},
    { "nom" : "roman",  "prix_unitaire" : 15.0, "quantite" : 1, "montant" : 15.0, "categorie" : "loisir"},
    { "nom" : "bonnet",  "prix_unitaire" : 10.0, "quantite" : 1, "montant" : 1.0, "categorie" : "vetement"},
    { "nom" : "t-shirt",  "prix_unitaire" : 15.0, "quantite" : 2, "montant" : 30.0, "categorie" : "vetement"},
    { "nom" : "jean",  "prix_unitaire" : 25.0, "quantite" : 1, "montant" : 25.0, "categorie" : "vetement"},
    { "nom" : "chaussure",  "prix_unitaire" : 30.0, "quantite" : 1, "montant" : 30.0, "categorie" : "vetement"}
    ]

magasins = ["Leclerc", "Auchan", "Carrefour", "Monoprix", "Match", "Lidl"]

def generateProductList():
    global articles
    numbers = []
    numbers.append(random.randrange(0,len(articles)-1,1))
    while len(numbers) < 8:
        nb = random.randrange(0,len(articles),1)
        if nb not in numbers:
            numbers.append(nb)

    total = 0
    produits = []
    for nb in numbers:
        produits.append(articles[nb])
        total += articles[nb]["montant"]
    return produits, total

def reZo():
    global magasins
    produits, total = generateProductList()
    obj = {
        "nom_magasin" : magasins[random.randrange(0,len(magasins)-1,1)],
        "total" : round(total,2),
        "date" : "01/12/2018",
        "lieu" : "Lens",
        "moyen_paiement" : "espece",
        "articles" : produits
    }
    # print(obj)
    print(json.dumps(obj))
    # headers = {"Content-type": "application/json", "Accept": "text/plain"}
    r = requests.post("http://192.168.43.21:5000/add/transaction",json=json.dumps(obj))
    print("OK")

def detectionNFC(mifare):

    uid = mifare.select()
    #ndef_data = mifare.read_ndef()
    #ndef_records = list(ndef_data.message_decoder(ndef_data))
    #print(ndef_records)
    
    return uid

"""def buzzer():
    print("lol")

    GPIO.output(40, GPIO.HIGH)
    #pygame.mixer.music.load("~/home/pi/bip/beep.ogg")   # chargement de la musique
    #print("lol")

    #pygame.mixer.music.play()   # la musique est jouée
    time.sleep(1)
    GPIO.output(40, GPIO.LOW)
    #print("lol")
"""    



mifare = nxppy.Mifare()


while True :
    
    try :
        detect = detectionNFC(mifare)
        if detect != None : 
            print(detect)
            #buzzer()
            reZo()
           
            time.sleep(2)

    except :
        pass
