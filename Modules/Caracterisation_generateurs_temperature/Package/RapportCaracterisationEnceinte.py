

#import time
import win32com.client
import os
#import numpy
#import datetime
#import shutil
#----------------------------------------------------------------------
class RapportCaracterisationEnceinte():
    '''Class permettant d'exporter les donnees dans la feuille saisie sous excel'''
    
    def __init__(self, path_sauvegarde, nom_fichier):
        
        self.path = path_sauvegarde #os.path.abspath("C:/Labo_Temp/AppData/")
        self.nom_fichier = nom_fichier
        self.feuille_saisie = os.path.abspath("Report/PDLPILSURMETFO009.xlsx")
        
        self.xl = win32com.client.DispatchEx('Excel.Application')
        
        self.classeur = self.xl.Workbooks.Open(self.feuille_saisie)
        self.xl.Visible = False
        
        self.classeur.SaveAs(self.path + "/"+  self.nom_fichier)
        
#        shutil.copy2(self.feuille_saisie, self.path)
#        
#        self.feuille_saisie_travail = os.path.abspath(self.path+"/PDLPILSURMETFO009.xlsx.xlsm")
        
    
        
    
    def mise_en_forme(self, donnees):
        """"""
#        try:
        self.xl.Visible = True
        onglet_1 = self.classeur.Worksheets(1)   
      
#    'admin': {'TYPE_CARACTERISATION': 'TOTALE', 'ID_GENERATEUR': 2249, 'OPERATEUR': 1}, 'moyens_mesure': {'ID_SONDES_CENTRALE': [1016], 'ID_CENTRALE': 999, 'TABLEAU_U_CENTRALE': [0.034615667054, 0.034615667054, 8.0, 0.0], 'TABLEAU_U_ETALON': [0.012, 0.004833413959, 0.001, 5.0, 0.007, 0.006], 'ID_POLYNOME': 2387, 'ID_CARACTERISATION': 65, 'ID_ETALON': 1113}}  
#        
#        print("donnees passees {}".format(donnees))
        #donnees administrative :
            #enceinte
        onglet_1.Range("B9").Value = donnees["rapport"]["enceinte"][0]
        onglet_1.Range("B11").Value = donnees["rapport"]["enceinte"][1]
        onglet_1.Range("B13").Value = donnees["rapport"]["enceinte"][3]
        onglet_1.Range("B15").Value = donnees["rapport"]["enceinte"][2]        
        
        onglet_1.Range("I9").Value = donnees["admin"]["DATE"]
        onglet_1.Range("I11").Value = "na"
        onglet_1.Range("I13").Value = donnees["rapport"]["operateur"]
        
        
        onglet_1.Range("A30").Value = donnees["admin"]["COMMENTAIRE"]
        
            #etalon        
        onglet_1.Range("C18").Value = donnees["rapport"]["etalon"][0]
        onglet_1.Range("G18").Value = float(donnees["rapport"]["etalon"][1])
        onglet_1.Range("H18").Value = float(donnees["rapport"]["etalon"][2])
        onglet_1.Range("I18").Value = float(donnees["rapport"]["etalon"][3])
        
            #centrale
        onglet_1.Range("C20").Value = donnees["rapport"]["centrale"]

            #Incertitudes moyens de mesure
#        print(donnees["moyens_mesure"]["TABLEAU_U_ETALON"])
        ligne = 6
        for ele in donnees["moyens_mesure"]["TABLEAU_U_ETALON"]:
            self.classeur.ActiveSheet.Cells(ligne, 13).Value = str(ele).replace(".", ",")
            ligne += 1
#        onglet_1.Range("M6:M11").Value = [(x) for x in donnees["moyens_mesure"]["TABLEAU_U_ETALON"]]

        ligne = 13
        for ele in donnees["moyens_mesure"]["TABLEAU_U_CENTRALE"]:
#        onglet_1.Range("M13:M16").Value = donnees["moyens_mesure"]["TABLEAU_U_CENTRALE"]
            self.classeur.ActiveSheet.Cells(ligne, 13).Value = str(ele).replace(".", ",")
            ligne += 1
        
            #uenceintes
        onglet_1.Range("D25").Value = donnees["rapport"]["u_enceinte"]        
        
        if  donnees["rapport"]["enceinte"][0] == 'Etuve ESPEC  N° 1':
            onglet_1.Range("D27").Value = donnees["rapport"]["u_enceinte_max"]
            onglet_1.Range("F27").Value = donnees["rapport"]["u_enceinte_autre_max"]
        else:
            onglet_1.Range("D27").Value = donnees["rapport"]["u_enceinte_autre_max"]
            onglet_1.Range("F27").Value = donnees["rapport"]["u_enceinte_max"]
        
        onglet_1.Range("D28").Value = 'na'   
        
        cell_model_resultat = onglet_1.Range("A41:I59")
        nbr_temperature = donnees["admin"]["NBR_TEMP_HOMOGENEITE"]
        
        for i in range(0, nbr_temperature):
            cellule_arrivee = onglet_1.Cells((41 + 21*i),1)
            
            if i> 0:
                cell_model_resultat.Copy()               
                onglet_1.Range(cellule_arrivee, cellule_arrivee).Select()
                onglet_1.Paste()
            else:
                pass                

            #mise en forme des donnees
            cellule_arrivee.Value = donnees[str(i+1)][0]["TEMPERATURE"]
            
                #donnees des tableaux
            list_emplacement = ["CENTRE", "HAD", "HAG", "HPD", "HPG", "BAD", "BAG", "BPD", "BPG",
                            "ETALON", "ETALON Corrigé"]
            decalage = 0                
            for sonde in list_emplacement :
                listedonnees = [(x["MIN"], x["MAX"],  x["MOYENNE"],  x["ECART_TYPE"],  x["STABILITE"],  x["DELTA"], x["U_MOYENS"], x["U_HOM"])
                                   for x in  donnees[str(i+1)] if x["EMPLACEMENT_MESURE"] == sonde]
                if listedonnees:
#                    print(listedonnees[0])
                    cellule_debut_resultats = onglet_1.Cells((44 + 21*i + decalage),2)
                    cellule_fin_resultats = onglet_1.Cells((44 + 21*i + decalage), 9)
                    
                    onglet_1.Range(cellule_debut_resultats, cellule_fin_resultats).Value = listedonnees[0]
                    
                decalage +=1

                
                
        self.classeur.Save()        
                
                

    def fermeture(self):
        
#        xl = win32com.client.DispatchEx('Excel.Application')
        self.xl.Application.Quit()
        del self.xl

