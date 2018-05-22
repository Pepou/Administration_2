#-*- coding: utf-8 -*-

import pickle
import numpy 
from PyQt4.QtGui import QMessageBox
from PyQt4.QtCore import QCoreApplication
def traitement_fichier_etalon(filename):
    '''Gestion de l'importation des donnees TXT et de leur mise en forme'''
    try:        
        with open(filename, 'r') as fichier_etalon:
            donnees_etalon = fichier_etalon.readlines()
                    
        ligne = []
        for texte in donnees_etalon :
            ligne.append(texte)
            
        #nbr de lignes du fichier
        nbr_lignes_fichier = len(donnees_etalon)
        
        
        #gestion test sur le nbr d'etalons (lignes: 5 à 10)
        i = 0
        nbr_etalon = 1
        while i <= 4 :
            
            lettres=[lettre for lettre in ligne[i+5]]
            
            if lettres[0]=="T":
                
                nbr_etalon += 1
                
            i+=1
        
        premiere_donnees = 4+nbr_etalon + 3
        
        i = premiere_donnees
        valeurs={}
        nbr_colonne = 2* nbr_etalon+2
        j=0
        donnees_fichier=[]
           
        #mise en place des donnees du fichier en dictionnaire : indice = colonne de mesure et valeur list de toutes les donnees en colonnes
        #indice 0= n° mesure, indice 1=datage mesure , indice 2=etal1,indice3=etal 3..... 
                
        while i<= nbr_lignes_fichier-1:
            
            ligne_valeurs = ligne[i].split()
            donnees_fichier.append(ligne[i].split())
           
            while j< nbr_colonne :
                valeurs[j]=[]
                j+=1
                
            for indice , elements in enumerate(ligne_valeurs) :
                valeurs[indice].append(elements)
                
            i+=1
        return valeurs
    except :
        pass

def mise_enforme_saisies(textedit):
        ''' Fonction recuperant les valeur dans un text edit et convertie en float ;saisie de base avec une virgule'''
                
#        try :
            
        mesures = []
        mise_en_forme = textedit.toPlainText().split("\n")
       
#        if len(mise_en_forme) == 1:
#            raise ValueError
        #Mise en forme de list et sous forme convertible des donnees de qtextedit
        for element in mise_en_forme :
            if element  == "\n" or element == "":
                raise ValueError
            else:

                mesures.append(float(element.replace(",", ".")))
        
        return mesures
        
#        except ValueError :
#            raise ValueError

            
           
#            break
    
def sauvegarde_onglet_saisie(donnees , nom_fichier):
    ''''fonction recuperant les donnees de l'onglet saisi et les sauvent dans un pickler '''
    
    path="C:/Labo_Temp/AppData/"+str(nom_fichier)
    with open(path, 'wb') as fichier :
        mon_pickler = pickle.Pickler(fichier)
        mon_pickler.dump(donnees)
        
def lecture_onglet_saisie(nom_fichier):
    ''''fonction recuperant des donnees d'un onglet saisi dans un pickler '''
    
    path="C:/Labo_Temp/AppData/"+nom_fichier
    with open(path, 'rb') as fichier :
        mon_unpickler = pickle.Unpickler(fichier)
        onglet = mon_unpickler.load()
#        print(onglet)
    return onglet 

def calcul_polynome(x , y , ordre):
    '''Fonction qui calcul un polynome :
    x et y doivent etre des lists et ordre un entier'''
    
    poly = numpy.polyfit(x, y, ordre)
    
    return poly
