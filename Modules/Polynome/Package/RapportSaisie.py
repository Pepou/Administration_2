
#-*-coding:Latin-1 -*
#import time
import win32com.client
import os
import numpy
#import datetime
import shutil
from PyQt4.QtGui import QMessageBox
from PyQt4 import QtCore
#----------------------------------------------------------------------
class RapportSaisie():
    '''Class permettant d'exporter les donnees dans la feuille saisie sous excel'''
    
    def __init__(self):
        self.path = os.path.abspath("C:/Labo_Temp/AppData/")
        
        self.feuille_saisie = os.path.abspath("AppData/Documents/RapportPolynome.xlsx")
#        self.nom_campagne = nom_campagne
        
        #Afin de pas ecarser le rappor vierge copie du fichier dans le repertoir appdata pour traitement
        shutil.copy2(self.feuille_saisie, self.path)
        
        self.feuille_saisie_travail = os.path.abspath(self.path+"/RapportPolynome.xlsx")
        
    def mise_en_forme(self, dossier, donnees_instrument, donnees_etalonnage, donnees_poly, nom_fichier):
        """"""
        try:
            
            xl = win32com.client.DispatchEx('Excel.Application')
            classeur = xl.Workbooks.Open(self.feuille_saisie_travail)
            onglet = classeur.Worksheets(1)     
            xl.Visible = True            
            
            classeur.ActiveSheet.Cells(8,2).Value = donnees_instrument["IDENTIFICATION"]
            classeur.ActiveSheet.Cells(9,2).Value = donnees_instrument["CONSTRUCTEUR"]
            classeur.ActiveSheet.Cells(8,5).Value = donnees_instrument["MODEL"]
            classeur.ActiveSheet.Cells(9,5).Value = donnees_instrument["N_SERIE"]
                        
            nbr_ligne = len(donnees_etalonnage)
            for i in range(nbr_ligne):
                classeur.ActiveSheet.Cells((16+i),1).Value = donnees_etalonnage[i]["ORDRE_APPARITION"]
                classeur.ActiveSheet.Cells((16+i),2).Value = donnees_etalonnage[i]["MOYENNE_ETALON_CORRI"]
                classeur.ActiveSheet.Cells((16+i),3).Value = donnees_etalonnage[i]["MOYENNE_INSTRUM"]
                classeur.ActiveSheet.Cells((16+i),4).Value = donnees_etalonnage[i]["CORRECTION"]
                classeur.ActiveSheet.Cells((16+i),5).Value = donnees_etalonnage[i]["ERREUR"]
                classeur.ActiveSheet.Cells((16+i),6).Value = donnees_etalonnage[i]["INCERTITUDE"]
            
            if donnees_poly["ORDRE_POLY"] == 1 :
                classeur.ActiveSheet.Cells((nbr_ligne + 18),1).Value = "ax"
                classeur.ActiveSheet.Cells((nbr_ligne + 19),1).Value = donnees_poly["COEFF_A"]
                
                classeur.ActiveSheet.Cells((nbr_ligne + 18),2).Value = "b"
                classeur.ActiveSheet.Cells((nbr_ligne + 19),2).Value = donnees_poly["COEFF_B"]
                
                classeur.ActiveSheet.Cells((nbr_ligne + 21),1).Value = "Residu max"
                classeur.ActiveSheet.Cells((nbr_ligne + 22),1).Value = donnees_poly["RESIDU_MAX"]
                
                classeur.ActiveSheet.Cells((nbr_ligne + 24),1).Value = "u_modelisation"
                classeur.ActiveSheet.Cells((nbr_ligne + 25),1).Value = donnees_poly["MODELISATION"]
            
            elif donnees_poly["ORDRE_POLY"] == 2:
                classeur.ActiveSheet.Cells((nbr_ligne + 18),1).Value = "ax²"
                classeur.ActiveSheet.Cells((nbr_ligne + 19),1).Value = donnees_poly["COEFF_A"]
                
                classeur.ActiveSheet.Cells((nbr_ligne + 18),2).Value = "bx"
                classeur.ActiveSheet.Cells((nbr_ligne + 19),2).Value = donnees_poly["COEFF_B"]
                
                classeur.ActiveSheet.Cells((nbr_ligne + 18),3).Value = "c"
                classeur.ActiveSheet.Cells((nbr_ligne + 19),3).Value = donnees_poly["COEFF_C"]
            
                classeur.ActiveSheet.Cells((nbr_ligne + 21),1).Value = "Residu max"
                classeur.ActiveSheet.Cells((nbr_ligne + 22),1).Value = donnees_poly["RESIDU_MAX"]
                
                
                classeur.ActiveSheet.Cells((nbr_ligne + 24),1).Value = "u_modelisation"
                classeur.ActiveSheet.Cells((nbr_ligne + 25),1).Value = donnees_poly["MODELISATION"]
            
            classeur.ActiveSheet.Cells(12,2).Value = donnees_poly["NUM_CERTIFICAT"]
            classeur.ActiveSheet.Cells(12,5).Value = donnees_poly["DATE_ETAL"]
    
            
            fichier = dossier + "/"+ nom_fichier
            classeur.SaveAs(fichier)
            classeur.ExportAsFixedFormat(0,fichier )
            
        except:
#            objet = 
            QMessageBox.critical(None, 
                    QtCore.QObject.trUtf8(QtCore.QObject(None),"Export Polynome"), 
                    QtCore.QObject.trUtf8(QtCore.QObject(None),"Une erreur est survenue lors de l'export")) 
            pass
            
            
    def fermeture(self):
        
        xl = win32com.client.Dispatch('Excel.Application')
        xl.Application.Quit()
        

