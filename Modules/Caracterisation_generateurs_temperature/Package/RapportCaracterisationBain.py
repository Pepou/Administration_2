import win32com.client
import os

class RapportCaracterisationBain():
    '''Class permettant d'exporter les donnees dans la feuille saisie sous excel'''
    
    def __init__(self, path_sauvegarde, nom_fichier):
        
        self.path = path_sauvegarde #os.path.abspath("C:/Labo_Temp/AppData/")
        self.nom_fichier = nom_fichier
        self.feuille_saisie = os.path.abspath("Modules/Caracterisation_generateurs_temperature/Report/PDLPILSURMETFO004.xlsm")
        
        self.xl = win32com.client.DispatchEx('Excel.Application')
        
        self.classeur = self.xl.Workbooks.Open(self.feuille_saisie)
        self.xl.Visible = False
        
        self.classeur.SaveAs(self.path + "/"+  self.nom_fichier)
        
    def mise_en_forme(self, donnees):
        """utilse donnees pour les mettre dans les cells"""
        
        self.xl.Visible = True
        onglet_1 = self.classeur.Worksheets(1)   
      

        #donnees administrative :
            #bain
        onglet_1.Range("B10").Value = donnees["ADMIN"]["NOM"]
        onglet_1.Range("F10").Value = donnees["ADMIN"]["DATE"]
        onglet_1.Range("F12").Value = donnees["ADMIN"]["OPERATEUR"]
        
        onglet_1.Range("B12").Value = donnees["ADMIN"]["MARQUE"]
        onglet_1.Range("B14").Value = donnees["ADMIN"]["N_SERIE"]
        onglet_1.Range("B16").Value = donnees["ADMIN"]["MODEL"]
        onglet_1.Range("B18").Value = donnees["ADMIN"]["HUILE"]
        onglet_1.Range("F18").Value = donnees["ADMIN"]["PB"]
        
        onglet_1.Range("C20").Value = donnees["ADMIN"]["SONDES"][0]
        onglet_1.Range("F20").Value = donnees["ADMIN"]["SONDES"][1]
        
        onglet_1.Range("C24").Value = donnees["RESULTATS"]["u_generateur"]
        
        onglet_1.Range("A29").Value = donnees["ADMIN"]["COMMENTAIRE"]
        
        #○stab
        for decalage in range(len(donnees["STAB"]["TEMPERATURE"])):
            self.classeur.ActiveSheet.Cells(51+decalage, 1).Value = donnees["STAB"]["TEMPERATURE"][decalage]
            self.classeur.ActiveSheet.Cells(51+decalage, 4).Value = donnees["STAB"]["MIN"][decalage]
            self.classeur.ActiveSheet.Cells(51+decalage, 5).Value = donnees["STAB"]["MAX"][decalage]
            self.classeur.ActiveSheet.Cells(51+decalage, 6).Value = donnees["STAB"]["DELTA"][decalage]
            
            
         #homogeneite
  
        nbr_temp = len(donnees["HOM"])
        cell_model_resultat = onglet_1.Range("A59:G105")
        
        for i in range(0, nbr_temp):
            cellule_arrivee = onglet_1.Cells((59 + 46*i),1)
            
            if i> 0:
                cell_model_resultat.Copy()               
                onglet_1.Range(cellule_arrivee, cellule_arrivee).Select()
                onglet_1.Paste()
            else:
                pass    
            
            self.classeur.ActiveSheet.Cells(61+ 46*i , 5).Value = donnees["HOM"][i]["TEMPERATURE"]
            
            for n_mesure  in range(len(donnees["HOM"][i]["MIN_1"])):
#                print(donnees["HOM"][i])
                
                
                self.classeur.ActiveSheet.Cells(64+ 46*i + 11 *n_mesure, 2).Value = donnees["ADMIN"]["SONDES"][0]
                self.classeur.ActiveSheet.Cells(64+ 46*i + 11 *n_mesure, 3).Value = donnees["ADMIN"]["SONDES"][1]
                self.classeur.ActiveSheet.Cells(64+ 46*i + 11 *n_mesure, 5).Value = donnees["ADMIN"]["SONDES"][1]
                self.classeur.ActiveSheet.Cells(64+ 46*i + 11 *n_mesure, 6).Value = donnees["ADMIN"]["SONDES"][0]
                
                
                self.classeur.ActiveSheet.Cells(66+ 46*i + 11 *n_mesure, 2).Value = donnees["HOM"][i]["MIN_1"][n_mesure]
                self.classeur.ActiveSheet.Cells(66+ 46*i + 11 *n_mesure, 3).Value = donnees["HOM"][i]["MIN_2"][n_mesure]
                self.classeur.ActiveSheet.Cells(66+ 46*i + 11 *n_mesure, 5).Value = donnees["HOM"][i]["MIN_4"][n_mesure]
                self.classeur.ActiveSheet.Cells(66+ 46*i + 11 *n_mesure, 6).Value = donnees["HOM"][i]["MIN_5"][n_mesure]
                
                self.classeur.ActiveSheet.Cells(67+ 46*i + 11 *n_mesure, 2).Value = donnees["HOM"][i]["MAX_1"][n_mesure]
                self.classeur.ActiveSheet.Cells(67+ 46*i + 11 *n_mesure, 3).Value = donnees["HOM"][i]["MAX_2"][n_mesure]
                self.classeur.ActiveSheet.Cells(67+ 46*i + 11 *n_mesure, 5).Value = donnees["HOM"][i]["MAX_4"][n_mesure]
                self.classeur.ActiveSheet.Cells(67+ 46*i + 11 *n_mesure, 6).Value = donnees["HOM"][i]["MAX_5"][n_mesure]
                
                self.classeur.ActiveSheet.Cells(68+ 46*i + 11 *n_mesure, 2).Value = donnees["HOM"][i]["MOY_1"][n_mesure]
                self.classeur.ActiveSheet.Cells(68+ 46*i + 11 *n_mesure, 3).Value = donnees["HOM"][i]["MOY_2"][n_mesure]
                self.classeur.ActiveSheet.Cells(68+ 46*i + 11 *n_mesure, 5).Value = donnees["HOM"][i]["MOY_4"][n_mesure]
                self.classeur.ActiveSheet.Cells(68+ 46*i + 11 *n_mesure, 6).Value = donnees["HOM"][i]["MOY_5"][n_mesure]
                
                self.classeur.ActiveSheet.Cells(69+ 46*i + 11 *n_mesure, 2).Value = donnees["HOM"][i]["S_1"][n_mesure]
                self.classeur.ActiveSheet.Cells(69+ 46*i + 11 *n_mesure, 3).Value = donnees["HOM"][i]["S_2"][n_mesure]
                self.classeur.ActiveSheet.Cells(69+ 46*i + 11 *n_mesure, 5).Value = donnees["HOM"][i]["S_4"][n_mesure]
                self.classeur.ActiveSheet.Cells(69+ 46*i + 11 *n_mesure, 6).Value = donnees["HOM"][i]["S_5"][n_mesure]
                
#                self.classeur.ActiveSheet.Cells(70+ 46*i + 11 *n_mesure, 2).Value = donnees["HOM"][i]["DELTA_1"][n_mesure]
#                self.classeur.ActiveSheet.Cells(70+ 46*i + 11 *n_mesure, 5).Value = donnees["HOM"][i]["DELTA_2"][n_mesure]
#                
#                self.classeur.ActiveSheet.Cells(71+ 46*i + 11 *n_mesure, 2).Value = donnees["HOM"][i]["EPSILONE"][n_mesure]
#                self.classeur.ActiveSheet.Cells(72+ 46*i + 11 *n_mesure, 2).Value = donnees["HOM"][i]["EPSILONE_U"][n_mesure]
        self.classeur.Save() 
