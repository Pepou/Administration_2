
#-*-coding:Latin-1 -*
#import time
import win32com.client
#import os
import datetime
import json
#import numpy
#import datetime
#import shutil
#----------------------------------------------------------------------
class Export_excel():
    '''Class permettant d'exporter les donnees dans la feuille saisie sous excel'''
    
    def __init__(self):
            self.xl = win32com.client.DispatchEx('Excel.Application')
            self.classeur = self.xl.Workbooks.Add()
            self.onglet = self.classeur.Worksheets(1)     
            self.xl.Visible = True 
        
    def export_bl(self, instruments, adresse):
        """"""
        
        with open("config_bdd.json") as json_file:
            config_bdd = json.load(json_file)        
        site = config_bdd["site"]
        
        if site == "LMS":
            nom = "Etablissement Français du sang Centre Pays de la Loire"
            labo = "Laboratoire de Metrologie Site Le Mans"
            adresse_labo = "194 Avenue Rubillard - CS 81835"
            ville = "72018 Le Mans CEDEX 2"
            tel = "Tel : 0243391743"
            fax = "Tel : 0243399499"
            courriel = "Mail : metro.lemans@efs.sante.fr"
        elif site == "ORLS":
            nom = "Etablissement Français du sang Centre Pays de la Loire"
            labo = "Laboratoire de Metrologie Site d'Orléans"
            adresse_labo = "Point rose 1er étage 14 Av de l'hôpital"
            ville = "45072 ORLEANS CEDEX"
            tel = "Tel : 0238499303"
            fax = "Tel : na"
            courriel = "Mail : metrologie.efsca@efs.sante.fr"
         
        nbr_onglets = self.classeur.Sheets.count

        if nbr_onglets < len(instruments):
            
            for i in range(len(instruments)-nbr_onglets):
                self.classeur.Sheets.Add()
#            nbr_onglets +=1
            
        onglet =1
        for nom_onglet in instruments.keys():
            self.classeur.Sheets(onglet).Select()
            if len(nom_onglet)<31:
                self.classeur.ActiveSheet.Name = nom_onglet.replace("/", "_")
            else:
                self.classeur.ActiveSheet.Name = nom_onglet[:29].replace("/", "_")
            #adresse 
            self.classeur.ActiveSheet.Cells(1,1).Value = nom
            self.classeur.ActiveSheet.Cells(2,1).Value = labo
            self.classeur.ActiveSheet.Cells(3,1).Value = adresse_labo
            self.classeur.ActiveSheet.Cells(4,1).Value = ville
            self.classeur.ActiveSheet.Cells(5,1).Value = tel
            self.classeur.ActiveSheet.Cells(6,1).Value = fax
            self.classeur.ActiveSheet.Cells(7,1).Value = courriel
            
            self.classeur.ActiveSheet.Cells(1,6).Value = adresse[nom_onglet][0]
            self.classeur.ActiveSheet.Cells(2,6).Value = adresse[nom_onglet][1]
            self.classeur.ActiveSheet.Cells(3,6).Value = str(adresse[nom_onglet][2]) +" "+ str(adresse[nom_onglet][3])

            
            
            self.classeur.ActiveSheet.Cells(10,1).Value = "Date d'expedition"
            self.classeur.ActiveSheet.Cells(10,2).Value = "Code Client"
            self.classeur.ActiveSheet.Cells(10,3).Value = "Site"
            self.classeur.ActiveSheet.Cells(10,4).Value = "Service"
            self.classeur.ActiveSheet.Cells(10,5).Value = "Instrument(s)"
            self.classeur.ActiveSheet.Cells(10,6).Value = "Numero(s) Rapport(s) "
            self.classeur.ActiveSheet.Cells(10,7).Value = "Date(s) rapport(s)"
            
            i = 1
            for instrum in instruments[nom_onglet]:
#                print(instrum)
                self.classeur.ActiveSheet.Cells((10 + i),1).Value = "'" + str(instrum[0])#.strftime("%d-%m-%Y" )
                self.classeur.ActiveSheet.Cells((10 + i),2).Value = instrum[1]
                self.classeur.ActiveSheet.Cells((10 + i),3).Value = instrum[5] 
                self.classeur.ActiveSheet.Cells((10 + i),4).Value = instrum[6] 
                self.classeur.ActiveSheet.Cells((10 + i),5).Value = instrum[2]
                self.classeur.ActiveSheet.Cells((10 + i),6).Value = instrum[3]
                self.classeur.ActiveSheet.Cells((10 + i),7).Value = "'"+str(instrum[4])#.strftime("%d-%m-%Y" )
                
                i+=1
            onglet +=1
        
    def fermeture(self):
        
        xl = win32com.client.Dispatch('Excel.Application')
        xl.Application.Quit()
        

