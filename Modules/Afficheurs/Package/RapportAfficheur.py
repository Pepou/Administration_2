
#-*-coding:Latin-1 -*
import os
import win32com.client as win32
import decimal
import numpy
import shutil

import time
import json


class RapportAfficheur:
    '''Classe permettant de recuperer un fichier CVR pret defini (s); de le ou les remplir avec les donnees d'etalonnage et de sauvegarder le tout'''
   
    def __init__(self, type_rapport) :
        
        
        with open("config_bdd.json") as json_file:
            config_bdd = json.load(json_file)        
        site = config_bdd["site"]
        
        if site == "LMS":
            fichier_ce = "Modules/Afficheurs/AppData/Documents/LMS/model_ce.docx"
            fichier_rapport_qualif = "Modules/Afficheurs/AppData/Documents/LMS/model_rapport de qualification.docx"
        elif site == "ORLS":
            fichier_ce = "Modules/Afficheurs/AppData/Documents/ORLS/model_ce.docx"
            fichier_rapport_qualif = "Modules/Afficheurs/AppData/Documents/ORLS/model_rapport de qualification.docx"
            
       #On recupere les chemins des documents :
        self.path = os.path.abspath("Modules/Afficheurs/AppData/")           

        if type_rapport == "Certificat d'étalonnage":    
            self.ce = os.path.abspath(fichier_ce) #permet de recuperer le chemin absolu du fichier le test ne marche pas sinon
            shutil.copy2(self.ce,self.path )
            self.ce_travail = os.path.abspath("Modules/Afficheurs/AppData/model_ce.docx")
            
        elif type_rapport == "Rapport de qualification":
            self.ce = os.path.abspath(fichier_rapport_qualif)
            shutil.copy2(self.ce,self.path)
            self.ce_travail = os.path.abspath("Modules/Afficheurs/AppData/model_rapport de qualification.docx")
            
        #on copie le ce afin de pas l'ecraser
#        shutil.copy2(self.ce,self.path )

    
        
    
################################################################################################

    def mise_en_forme_ce(self, donnees, path,  nom_fichier):
#    def mise_en_forme_ce(self, donnees):
        '''fonction qui charge le document demandé et ecrit les donnees à passer sous forme de dictionnaire aux signets presents dans le doc
        Il arrondi à la resolution les donnees grace à la fonction traitement des donneees et traitement U'''
        
        word = win32.gencache.EnsureDispatch('Word.Application')
        word.Visible = True
        doc = word.Documents.Open(self.ce_travail)
        
#        print("nom {}".format(nom_fichier))
     #Traitement du CE 

        doc.Bookmarks("n_certificat").Range.Text = donnees["n_certificat"]  #permet de se deplacer sur les signets et attribuer un string
        doc.Bookmarks("n_certificat_2").Range.Text = donnees["n_certificat"]
        
        if donnees["affectation"] != "Neant":
            doc.Bookmarks("societe").Range.Text = donnees["societe"] +" "+ "(" + donnees["affectation"] + ")"
            
        else:
            doc.Bookmarks("societe").Range.Text = donnees["societe"] 
            

        doc.Bookmarks("adresse").Range.Text = donnees["adresse"]
        doc.Bookmarks("code_postal_ville").Range.Text = str(donnees["code_postal"]) +" "+ donnees["ville"]
        
                
        doc.Bookmarks("identification_instrument").Range.Text = donnees["identification_instrument"]
        doc.Bookmarks("identification_instrument_2").Range.Text = donnees["identification_instrument"]
                
        doc.Bookmarks("n_serie").Range.Text = donnees["n_serie"] 
        doc.Bookmarks("n_serie_2").Range.Text = donnees["n_serie"]
                
        
        doc.Bookmarks("constructeur").Range.Text = donnees["constructeur"]
        doc.Bookmarks("constructeur_2").Range.Text = donnees["constructeur"]
                
        doc.Bookmarks("designation").Range.Text = donnees["designation"]
        doc.Bookmarks("designation_2").Range.Text = donnees["designation"]
        
        if donnees["designation"] == "Sonde alarme température" or donnees["designation"] == "Afficheur de température":
            unite = "°C"
        elif donnees["designation"] == "Afficheur de temps":
            unite = "s"
        elif donnees["designation"] == "Afficheur de vitesse":
            unite = " tr/min"
                
        doc.Bookmarks("type").Range.Text = donnees["type"]
                
        doc.Bookmarks("resolution").Range.Text = str(numpy.amax(donnees["resolution"])) + " " + unite
                
        doc.Bookmarks("date_etalonnage").Range.Text = donnees["date_etalonnage"]
        doc.Bookmarks("ville").Range.Text = str(donnees["ville"])
                
#        doc.Bookmarks("milieu").Range.Text = donnees["milieu"]
                
#        doc.Bookmarks("n_mode_operatoire").Range.Text = donnees["n_mode_operatoire"]
                
#        operateur_utf_8 = donnees["operateur"].decode("utf-8")
        doc.Bookmarks("operateur").Range.Text = donnees["operateur"]
                       

        doc.Bookmarks("etalon").Range.Text = donnees["etalon"] + " "+donnees["ce_etalon"]
        
        doc.Bookmarks("renseignemment_complementaire").Range.Text = donnees["renseignement_complementaire"]
        doc.Bookmarks("Etat_reception").Range.Text = donnees["commentaire"]
        
        #referentiel conformite
        
        for i in reversed(range(donnees["nbr_pt_etalonnage"])):
            doc.Bookmarks("referentiel_conformite").Range.Text = str(donnees["emt"][i]) +" "+ ":" +str(donnees["commentaire_referentiel"][i]) + "\n"
        
        #gestion resultat : insertion tableau
        position_resultat =  doc.Bookmarks("resultat").Range
        position_resultat.ParagraphFormat.Alignment = win32.constants.wdAlignParagraphCenter
        
        nbr_ligne = donnees["nbr_pt_etalonnage"] + 1
        

            
        nbr_colonne = 6
    
        table = doc.Tables.Add(position_resultat, nbr_ligne, nbr_colonne)
        table.Borders.Enable = True            

        
        table.Cell(1,1).Range.Text= "Etalon" + " " + "(" + unite +")"
        table.Cell(1,1).VerticalAlignment = win32.constants.wdCellAlignVerticalCenter
        
        table.Cell(1,2).Range.Text = "Mesure" +  " " + "(" + unite +")"
        table.Cell(1,2).VerticalAlignment = win32.constants.wdCellAlignVerticalCenter
        
        table.Cell(1,3).Range.Text = "Correction" +  " " + "(" + unite +")"
        table.Cell(1,3).VerticalAlignment = win32.constants.wdCellAlignVerticalCenter
        
        table.Cell(1,4).Range.Text = "Incertitude k = 2" +  " " + "(" + unite +")"
        table.Cell(1,4).VerticalAlignment = win32.constants.wdCellAlignVerticalCenter
        
        table.Cell(1,5).Range.Text= "EMT"  +  " " + "(" + unite +")"
        table.Cell(1,5).VerticalAlignment = win32.constants.wdCellAlignVerticalCenter
        
        table.Cell(1,6).Range.Text= "Conformité"
        table.Cell(1,6).VerticalAlignment = win32.constants.wdCellAlignVerticalCenter
        
        i = 0
        while i < nbr_ligne -1 : 
            etalon = self.mise_en_forme_donnees(numpy.amax(donnees["resolution"]), donnees["moyenne_etalon_corri"][i])
            
            instrument = self.mise_en_forme_donnees(numpy.amax(donnees["resolution"]), donnees["moyenne_instrum"][i])
            
            correction = self.mise_en_forme_donnees(numpy.amax(donnees["resolution"]), donnees["moyenne_correction"][i])
            
            U = self.mise_en_forme_U(numpy.amax(donnees["resolution"]),donnees["U"][i])
                        
     
            table.Cell((i+2),1).Range.Text = str(etalon)
            
            table.Cell((i+2),2).Range.Text= str(instrument)
            
            table.Cell((i+2),3).Range.Text= str(correction)
            
            table.Cell((i+2),4).Range.Text= str(U)
            
            table.Cell((i+2),5).Range.Text= "±" + str(donnees["valeur_numerique_emt"][i])
            
            table.Cell((i+2),6).Range.Text= donnees["conformite"][i]
            i+=1
        
        if donnees["commentaire_resultats"] != "":     
            doc.Bookmarks("commentaire_resultats").Range.Text = donnees["commentaire_resultats"]
#        nom_fichier.replace("\n", "_")
        
#        print(str(nom_fichier).replace("\n", " "))
        time.sleep(15)
        sauvegarde_docx = path + "/" + str(nom_fichier).replace("\n", " ") +".docx"
        sauvegarde_pdf = path + "/" + str(nom_fichier).replace("\n", " ") +".pdf"
                
        doc.SaveAs(sauvegarde_docx)
        doc.SaveAs(sauvegarde_pdf, FileFormat= 17) #17 =PDF
        doc.Close()
        word.Application.Quit()
            

#######################################################################

#    def mise_en_forme_ce_annule_remplace(self, donnees, path,  num_ce, nom_fichier):
#        '''fonction qui charge le document demandé et ecrit les donnees à passer sous forme de dictionnaire aux signets presents dans le doc
#        Il arrondi à la resolution les donnees grace à la fonction traitement des donneees et traitement U
#        Attention ne sert que pour la reemission '''
#        
#        word = win32.gencache.EnsureDispatch('Word.Application')
#        word.Visible = False
#        doc = word.Documents.Open(self.ce_travail)
#        
#        
#     #Traitement du CE 
#
#        doc.Bookmarks("n_certificat").Range.Text = num_ce  #permet de se deplacer sur les signets et attribuer un string
#        doc.Bookmarks("n_certificat_2").Range.Text = num_ce
#        
#        if donnees["affectation"] != "Neant":
#            doc.Bookmarks("societe").Range.Text = donnees["societe"] +" "+ "(" + donnees["affectation"] + ")"
#            
#        else:
#            doc.Bookmarks("societe").Range.Text = donnees["societe"] 
#            
#
#        doc.Bookmarks("adresse").Range.Text = donnees["adresse"]
#        doc.Bookmarks("code_postal_ville").Range.Text = str(donnees["code_postal"]) +" "+ donnees["ville"]
#                
#        doc.Bookmarks("identification_instrument").Range.Text = donnees["identification_instrument"]
#        doc.Bookmarks("identification_instrument_2").Range.Text = donnees["identification_instrument"]
#                
#        doc.Bookmarks("n_serie").Range.Text = donnees["n_serie"] 
#        doc.Bookmarks("n_serie_2").Range.Text = donnees["n_serie"]
#                
#        
#        doc.Bookmarks("constructeur").Range.Text = donnees["constructeur"]
#        doc.Bookmarks("constructeur_2").Range.Text = donnees["constructeur"]
#                
#        doc.Bookmarks("designation").Range.Text = donnees["designation"]
#        doc.Bookmarks("designation_2").Range.Text = donnees["designation"]
#                
#        doc.Bookmarks("type").Range.Text = donnees["type"]
#                
#        doc.Bookmarks("resolution").Range.Text = donnees["resolution"]
#                
#        doc.Bookmarks("date_etalonnage").Range.Text = donnees["date_etalonnage"]
#                
#        doc.Bookmarks("milieu").Range.Text = donnees["milieu"]
#                
#        doc.Bookmarks("n_mode_operatoire").Range.Text = donnees["n_mode_operatoire"]
#                
#        doc.Bookmarks("operateur").Range.Text = donnees["operateur"]
#                
#        #preparation donnees generateurs
#        nbr_generateur = len(donnees["generateur"])
#        i = 0
#        while i< nbr_generateur:
#            donnees["generateur"].insert((i+1),"," )
#            i+=2
#        for ele in donnees["generateur"]:
#            doc.Bookmarks("generateur").Range.Text = " "+str(ele)
#            
#        #preparation donnees etalons
#        nbr_etalon = len(donnees["etalon"])
#        i = 0
#        while i< nbr_etalon:
#            donnees["etalon"].insert((i+1),"," ) #permet d'inserer une virgule
#            i+=2
#        print(donnees[etalon])
#        for ele in donnees["etalon"]:
#            doc.Bookmarks("etalon").Range.Text = " "+str(ele)
#        
#        doc.Bookmarks("renseignemment_complementaire").Range.Text = donnees["renseignement_complementaire"]
#        doc.Bookmarks("Etat_reception").Range.Text = donnees["Etat_reception"]
#        
#        #gestion resultat : insertion tableau
#        position_resultat =  doc.Bookmarks("resultat").Range
#        position_resultat.ParagraphFormat.Alignment = win32.constants.wdAlignParagraphCenter
#        
#        nbr_ligne = donnees["nbr_pt_etalonnage"] + 1
#        
#        if donnees["milieu"] == "LIQUIDE":
#            
#            nbr_colonne = 5
#        
#            table = doc.Tables.Add(position_resultat, nbr_ligne, nbr_colonne)
#            table.Borders.Enable = True
#            
#            table.Cell(1,1).Range.Text= "Profondeur d'immersion (mm)"
#            table.Cell(1,1).VerticalAlignment = win32.constants.wdCellAlignVerticalCenter
#            
#            table.Cell(1,2).Range.Text= "Température étalon (°C)"
#            table.Cell(1,2).VerticalAlignment = win32.constants.wdCellAlignVerticalCenter
#            
#            table.Cell(1,3).Range.Text = "T°C chaine de mesure (°C)"
#            table.Cell(1,3).VerticalAlignment = win32.constants.wdCellAlignVerticalCenter
#            
#            table.Cell(1,4).Range.Text = "Correction (°C)"
#            table.Cell(1,4).VerticalAlignment = win32.constants.wdCellAlignVerticalCenter
#            
#            table.Cell(1,5).Range.Text = "Incertitude (°C)"
#            table.Cell(1,5).VerticalAlignment = win32.constants.wdCellAlignVerticalCenter
#            
#            i = 0
#            while i < nbr_ligne -1 : 
#                etalon = self.mise_en_forme_donnees(donnees["resolution"], donnees["moyenne_etalon_corri"][i])
#                
#                instrument = self.mise_en_forme_donnees(donnees["resolution"], donnees["moyenne_instrum"][i])
#                
#                correction = self.mise_en_forme_donnees(donnees["resolution"], donnees["moyenne_correction"][i])
#                
#                U = self.mise_en_forme_U(donnees["resolution"],donnees["U"][i])
#                            
#                table.Cell((i+2),1).Range.Text = str(donnees["immersion"][i])
#
#                table.Cell((i+2),2).Range.Text = str(etalon)
#                
#                table.Cell((i+2),3).Range.Text= str(instrument)
#                
#                table.Cell((i+2),4).Range.Text= str(correction)
#                
#                table.Cell((i+2),5).Range.Text= str(U)
#                
#                i+=1
#            
#        else:
#            nbr_colonne = 4
#        
#            table = doc.Tables.Add(position_resultat, nbr_ligne, nbr_colonne)
#            table.Borders.Enable = True
#            
#            table.Cell(1,1).Range.Text= "Température étalon (°C)"
#            table.Cell(1,1).VerticalAlignment = win32.constants.wdCellAlignVerticalCenter
#            
#            table.Cell(1,2).Range.Text = "T°C chaine de mesure (°C)"
#            table.Cell(1,2).VerticalAlignment = win32.constants.wdCellAlignVerticalCenter
#            
#            table.Cell(1,3).Range.Text = "Correction (°C)"
#            table.Cell(1,3).VerticalAlignment = win32.constants.wdCellAlignVerticalCenter
#            
#            table.Cell(1,4).Range.Text = "Incertitude (°C)"
#            table.Cell(1,4).VerticalAlignment = win32.constants.wdCellAlignVerticalCenter
#            
#            i = 0
#            while i < nbr_ligne -1 : 
#                etalon = self.mise_en_forme_donnees(donnees["resolution"], donnees["moyenne_etalon_corri"][i])
#                
#                instrument = self.mise_en_forme_donnees(donnees["resolution"], donnees["moyenne_instrum"][i])
#                
#                correction = self.mise_en_forme_donnees(donnees["resolution"], donnees["moyenne_correction"][i])
#                
#                U = self.mise_en_forme_U(donnees["resolution"],donnees["U"][i])
#                            
# 
#                table.Cell((i+2),1).Range.Text = str(etalon)
#                
#                table.Cell((i+2),2).Range.Text= str(instrument)
#                
#                table.Cell((i+2),3).Range.Text= str(correction)
#                
#                table.Cell((i+2),4).Range.Text= str(U)
#                
#                i+=1
#        
#        sauvegarde_docx = path + "/" + str(nom_fichier) +".docx"
#        sauvegarde_pdf = path + "/" + str(nom_fichier) +".pdf"
#                
#        doc.SaveAs(sauvegarde_docx)
#        doc.SaveAs(sauvegarde_pdf, FileFormat= 17) #17 =PDF
#        doc.Close()
#        word.Application.Quit()
#    
#    
#    
#    def mise_en_forme_cv_annule_remplace(self, donnees, path,  num_cv, nom_fichier_cv):
#        
#        word = win32.gencache.EnsureDispatch('Word.Application')
#        word.Visible = False
#        doc = word.Documents.Open(self.cv_travail)
#             
#        #Traitement du CV
#        
#        doc.Bookmarks("n_certificat").Range.Text = num_cv  #permet de se deplacer sur les signets et attribuer un string
#                 
#        if donnees["affectation"] != "Neant":
#            doc.Bookmarks("societe").Range.Text = donnees["societe"] +" "+ "(" + donnees["affectation"] + ")"
#        else:
#            doc.Bookmarks("societe").Range.Text = donnees["societe"] 
#
#        doc.Bookmarks("adresse").Range.Text = donnees["adresse"]
#        doc.Bookmarks("code_postal_ville").Range.Text = str(donnees["code_postal"]) +" "+ donnees["ville"]
#        
#        doc.Bookmarks("identification_instrument").Range.Text = donnees["identification_instrument"]
#
#        doc.Bookmarks("n_serie").Range.Text = donnees["n_serie"] 
#        
#        doc.Bookmarks("constructeur").Range.Text = donnees["constructeur"]
#        
#        doc.Bookmarks("designation").Range.Text = donnees["designation"]
#        
#        doc.Bookmarks("type").Range.Text = donnees["type"]
#        
#        doc.Bookmarks("referentiel_emt").Range.Text = donnees["referentiel_emt"]
#        
#        doc.Bookmarks("date_etalonnage").Range.Text = donnees["date_etalonnage"]
#        
#        doc.Bookmarks("milieu").Range.Text = donnees["milieu"]
#        
#        doc.Bookmarks("n_mode_operatoire").Range.Text = donnees["n_mode_operatoire"]
#        
#        doc.Bookmarks("conformite").Range.Text = donnees["conformite"]
#        
#        #gestion de la plage de verification
#        if len(donnees["temps_consignes"]) > 1:
#            list_temp = []
#            for ele in donnees["temps_consignes"]:
#                list_temp.append(int(ele))
#            min = str(numpy.amin(list_temp))
#            max = str(numpy.amax(list_temp))
#            doc.Bookmarks("renseignement_lie_verif").Range.Text = "Plage de Vérification de {}°C à {}°C".format(min, max)
#            
#        else:
#            for ele in donnees["temps_consignes"]:
#                temp_consign = int(ele)
#            doc.Bookmarks("renseignement_lie_verif").Range.Text = "Temperature de Vérification {}°C".format(temp_consign)
#            
#        
#        doc.SaveAs(path + "/" + nom_fichier_cv)
#        doc.SaveAs(path + "/" + nom_fichier_cv, FileFormat= 17) #17 =PDF
#        doc.Close()
#        word.Application.Quit()
    
    
    def mise_en_forme_donnees(self, resolution,  mesure):
        '''fonction qui arrondie à la resolution pres les donnees qu'on lui passe'''
        resolution_text = str(resolution)
        a = str(resolution_text.replace(",", "."))
        if a == "1.0":
                a = "1."
        elif  a == "2.0":
                a = "2."
#        b = str(round(mesure, 4))
        conversion_b = str(mesure)
#        print(b)
        valeur = decimal.Decimal(conversion_b).quantize(decimal.Decimal(a), rounding=decimal.ROUND_HALF_EVEN)
        
        return valeur
        
########################################################################

    def mise_en_forme_U(self, resolution,  U):
        '''fonction qui arrondie à la resolution mais superieur pres les donnees qu'on lui passe'''
        resolution_text = str(resolution)
        a = str(resolution_text.replace(",", "."))
        if a == "1.0":
                a = "1."
        elif  a == "2.0":
                a = "2."
        b = str(U)
        valeur = decimal.Decimal(b).quantize(decimal.Decimal(a), rounding=decimal.ROUND_UP)
        
        return valeur
