
#-*-coding:Latin-1 -*
#import time
import win32com.client
#import os
import datetime
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
        
    def export_temperature(self, temperature, afficheur, delais, list_expedition_reception_temperature,list_reception_expedition_temperature, \
                                    list_expedition_reception_afficheurs, list_reception_expedition_afficheurs):
        """"""
#        try:
            
        #instruments etalonnes temperature
        self.classeur.ActiveSheet.Name = "instruments_etalonnes_temp"
        
        self.classeur.ActiveSheet.Cells(1,1).Value = "Identification"
        self.classeur.ActiveSheet.Cells(1,1).Font.Bold = True
        
        self.classeur.ActiveSheet.Cells(1,2).Value = "Date etalonnage"
        self.classeur.ActiveSheet.Cells(1,2).Font.Bold = True
        
        self.classeur.ActiveSheet.Cells(1,3).Value = "Conformite"
        self.classeur.ActiveSheet.Cells(1,3).Font.Bold = True
        
        self.classeur.ActiveSheet.Cells(1,4).Value = "Client"
        self.classeur.ActiveSheet.Cells(1,4).Font.Bold = True
        
        self.classeur.ActiveSheet.Cells(1,5).Value = "Affectation"
        self.classeur.ActiveSheet.Cells(1,5).Font.Bold = True
        
        self.classeur.ActiveSheet.Cells(1,6).Value = "Site"
        self.classeur.ActiveSheet.Cells(1,6).Font.Bold = True

        
        nbr_instruments = len(temperature)
        mise_en_forme_temperature = [(x[1], str(x[2]),x[3], x[4], x[5], x[6]) for x in temperature ]
        self.classeur.ActiveSheet.Range(self.classeur.ActiveSheet.Cells(2,1), self.classeur.ActiveSheet.Cells(nbr_instruments +1,6)).value = mise_en_forme_temperature
            
            
                        
        #    Afficheurs etalonnes
        self.classeur.Sheets.Add()
        self.classeur.ActiveSheet.Name = "afficheurs_etalonnes"
        
        self.classeur.ActiveSheet.Cells(1,1).Value = "Identification"
        self.classeur.ActiveSheet.Cells(1,1).Font.Bold = True
        
        self.classeur.ActiveSheet.Cells(1,2).Value = "Date etalonnage"
        self.classeur.ActiveSheet.Cells(1,2).Font.Bold = True
        
        self.classeur.ActiveSheet.Cells(1,3).Value = "Conformite"
        self.classeur.ActiveSheet.Cells(1,3).Font.Bold = True
        
        self.classeur.ActiveSheet.Cells(1,4).Value = "Client"
        self.classeur.ActiveSheet.Cells(1,4).Font.Bold = True
        
        self.classeur.ActiveSheet.Cells(1,5).Value = "Affectation"
        self.classeur.ActiveSheet.Cells(1,5).Font.Bold = True
        
        self.classeur.ActiveSheet.Cells(1,6).Value = "Site"
        self.classeur.ActiveSheet.Cells(1,6).Font.Bold = True
        

        nbr_afficheurs = len(afficheur)
        mise_en_forme_afficheur = [(x[0], str(x[1]), x[2], x[3], x[4], x[5]) for x in afficheur ]
        
        self.classeur.ActiveSheet.Range(self.classeur.ActiveSheet.Cells(2,1), self.classeur.ActiveSheet.Cells(nbr_afficheurs +1,6)).value = mise_en_forme_afficheur


            
        #delais

        designation =[x for x in delais.keys()]
        designation.sort()
        for ele in designation:
            if len(delais[ele]) !=0:
                self.classeur.Sheets.Add()
                if len (ele)<30:
                    self.classeur.ActiveSheet.Name = str(ele.replace("/", "_"))
                else:
                    self.classeur.ActiveSheet.Name = str(ele[0:29].replace("/", "_"))
                    
                self.classeur.ActiveSheet.Cells(1,1).Value = "Identification"
                self.classeur.ActiveSheet.Cells(1,1).Font.Bold = True
                
                self.classeur.ActiveSheet.Cells(1,2).Value = "Date reception"
                self.classeur.ActiveSheet.Cells(1,2).Font.Bold = True
                
                self.classeur.ActiveSheet.Cells(1,3).Value = "Date expedition"
                self.classeur.ActiveSheet.Cells(1,3).Font.Bold = True
                
                self.classeur.ActiveSheet.Cells(1,4).Value = "Delais d'immobilisation"
                self.classeur.ActiveSheet.Cells(1,4).Font.Bold = True
                
                self.classeur.ActiveSheet.Cells(1,5).Value = "Client"
                self.classeur.ActiveSheet.Cells(1,5).Font.Bold = True
                
                self.classeur.ActiveSheet.Cells(1,6).Value = "Affectation"
                self.classeur.ActiveSheet.Cells(1,6).Font.Bold = True
                
                self.classeur.ActiveSheet.Cells(1,7).Value = "Site"
                self.classeur.ActiveSheet.Cells(1,7).Font.Bold = True
                
                
                
                
                mise_en_forme_delais = [(x[0], str(x[1]), str(x[2]), str(x[3]), x[4], x[5], x[6]) for x in delais[ele]]
                nbr_indicateur = len(delais[ele])
                self.classeur.ActiveSheet.Range(self.classeur.ActiveSheet.Cells(2,1), self.classeur.ActiveSheet.Cells(nbr_indicateur +1,7)).value = mise_en_forme_delais
                
#        #gestion des delta receptionné expedies
        self.classeur.Sheets.Add()
        self.classeur.ActiveSheet.Name = "Pb_expe_recep_temp"
        self.classeur.ActiveSheet.Cells(1,1).Value = "Identification"
        self.classeur.ActiveSheet.Cells(1,1).Font.Bold = True
        
        self.classeur.ActiveSheet.Cells(1,2).Value = "Date"
        self.classeur.ActiveSheet.Cells(1,2).Font.Bold = True
    
        mise_en_forme_list_expedition_reception_temperature =[(x[0], str(x[1])) for x in list_expedition_reception_temperature]
        nbr = len(mise_en_forme_list_expedition_reception_temperature)
        self.classeur.ActiveSheet.Range(self.classeur.ActiveSheet.Cells(2,1), self.classeur.ActiveSheet.Cells(nbr +1,2)).value = mise_en_forme_list_expedition_reception_temperature
        
        
        
        self.classeur.Sheets.Add()
        self.classeur.ActiveSheet.Name = "Pb_recep_expe_temp"
        self.classeur.ActiveSheet.Cells(1,1).Value = "Identification"
        self.classeur.ActiveSheet.Cells(1,1).Font.Bold = True
        
        self.classeur.ActiveSheet.Cells(1,2).Value = "Date"
        self.classeur.ActiveSheet.Cells(1,2).Font.Bold = True
    
        mise_en_forme_list_reception_expedition_temperature =[(x[0], str(x[1])) for x in list_reception_expedition_temperature]
        nbr = len(mise_en_forme_list_reception_expedition_temperature)
        self.classeur.ActiveSheet.Range(self.classeur.ActiveSheet.Cells(2,1), self.classeur.ActiveSheet.Cells(nbr +1,2)).value = mise_en_forme_list_reception_expedition_temperature
        
        
        self.classeur.Sheets.Add()
        self.classeur.ActiveSheet.Name = "Pb_expe_recep_Aff"
        self.classeur.ActiveSheet.Cells(1,1).Value = "Identification"
        self.classeur.ActiveSheet.Cells(1,1).Font.Bold = True
        
        self.classeur.ActiveSheet.Cells(1,2).Value = "Date"
        self.classeur.ActiveSheet.Cells(1,2).Font.Bold = True
    
        mise_en_forme_list_expedition_reception_afficheurs =[(x[0], str(x[1])) for x in list_expedition_reception_afficheurs]
        nbr = len(mise_en_forme_list_expedition_reception_afficheurs)
        self.classeur.ActiveSheet.Range(self.classeur.ActiveSheet.Cells(2,1), self.classeur.ActiveSheet.Cells(nbr +1,2)).value = mise_en_forme_list_expedition_reception_afficheurs
        
        
        
        self.classeur.Sheets.Add()
        self.classeur.ActiveSheet.Name = "Pb_recep_expe_Aff"
        self.classeur.ActiveSheet.Cells(1,1).Value = "Identification"
        self.classeur.ActiveSheet.Cells(1,1).Font.Bold = True
        
        self.classeur.ActiveSheet.Cells(1,2).Value = "Date"
        self.classeur.ActiveSheet.Cells(1,2).Font.Bold = True
    
        mise_en_forme_list_reception_expedition_afficheurs =[(x[0], str(x[1])) for x in list_reception_expedition_afficheurs]
        nbr = len(mise_en_forme_list_reception_expedition_afficheurs)
        self.classeur.ActiveSheet.Range(self.classeur.ActiveSheet.Cells(2,1), self.classeur.ActiveSheet.Cells(nbr +1,2)).value = mise_en_forme_list_reception_expedition_afficheurs
        
      
    

    def export_instruments(self, list_instruments):
        '''fct qui export sous un fichier excel les instruments'''
        
        self.classeur.ActiveSheet.Name = "list_instruments"
        
        self.classeur.ActiveSheet.Cells(1,1).Value = "Identification"
        self.classeur.ActiveSheet.Cells(1,1).Font.Bold = True
        
        self.classeur.ActiveSheet.Cells(1,2).Value = "Domaine de mesure"
        self.classeur.ActiveSheet.Cells(1,2).Font.Bold = True
        
        self.classeur.ActiveSheet.Cells(1,3).Value = "Designation"
        self.classeur.ActiveSheet.Cells(1,3).Font.Bold = True
        
        self.classeur.ActiveSheet.Cells(1,4).Value = "Code client"
        self.classeur.ActiveSheet.Cells(1,4).Font.Bold = True
        
        self.classeur.ActiveSheet.Cells(1,5).Value = "Affectation"
        self.classeur.ActiveSheet.Cells(1,5).Font.Bold = True
        
        nbr_instrumens = len(list_instruments)
                
        self.classeur.ActiveSheet.Range(self.classeur.ActiveSheet.Cells(2,1), self.classeur.ActiveSheet.Cells(nbr_instrumens +1,5)).value = list_instruments
        
        
        
    def fermeture(self):
        
        xl = win32com.client.Dispatch('Excel.Application')
        xl.Application.Quit()
        

