# -*- coding: utf-8 -*-

"""
Module implementing Exploitation_Centrales.
"""

from PyQt4.QtCore import pyqtSlot, SIGNAL, QDate, pyqtSignal, QThread
from PyQt4.QtGui import QMainWindow, QFileDialog, QTableWidgetItem, QComboBox, QMessageBox

from .Ui_Interface_Centrales import Ui_Exploitation_Centrales
from Modules.Cartographie.Package.AccesBdd import AccesBdd, Carto_BDD
from datetime import datetime
from matplotlib.widgets import Cursor
#from matplotlib.ticker import MaxNLocator
from itertools import repeat
import pendulum
import pandas as pd
import numpy as np
import  decimal
from Modules.Cartographie.Report.Rapport import Rapport
from collections import OrderedDict

import matplotlib.dates

#from itertools import zip_longest


class Exploitation_Centrales(QMainWindow, Ui_Exploitation_Centrales):
    """
    Class documentation goes here.
    """
    
    fermeture_reouverture = pyqtSignal()
    
    def __init__(self, engine, parent=None):
        """
        Constructor        
        @param parent reference to the parent widget (QWidget)
        """
        super(Exploitation_Centrales, self).__init__(parent)
        self.setupUi(self)
        
        self.engine =engine
#        self.meta = meta
        
        self.tupple_index = None
        
        self.demarrage()
        
        self.dateEdit.setDate(QDate.currentDate())
        
        self.annexe_simulation = False
        
        self.lineEdit_consigne.setStyleSheet(
                """QLineEdit { background-color: red }""")
                
        self.lineEdit_enceinte.setStyleSheet(
                """QLineEdit { background-color: red }""")
#        
#        comboBox_responsable_mesure
    
    def demarrage(self):
        """gere les donnees necessaire à l'ouverture"""
        self.db = AccesBdd(self.engine)
        
        self.centrales = self.db.centrales()
        self.centrales.sort()
        self.sondes_centrales = self.db.sondes_centrales()
        self.sondes_centrales.sort()
        modeles = list(set([x[3] for x in self.centrales]))

        modeles.sort()

        self.comboBox_centrale.addItems(modeles)
        
        date_du_jour = pendulum.now('Europe/Paris')
#        print(date_du_jour)
        self.dateEdit.setDate(date_du_jour)

        #Parc des enceintes:
#        self.parc = self.db.parc_enceintes()
#
#        self.lineEdit_enceinte.mise_a_jour_completerList([x.IDENTIFICATION for x in self.parc])
#
#        self.lineEdit_designation_litt.mise_a_jour_completerList([x.DESIGNATION_LITTERALE for x in self.parc])
#        self.tableView_donnees_fichier.installEventFilters(self) 

        #cmr
        self.db.cmr(self.comboBox_responsable_mesure)
        
        self.on_comboBox_application_currentIndexChanged("Conservation CGR")
    
    def closeEvent(self, event):
        """ Fermeture de la bdd"""
        
        self.db.__del__()
        

    @pyqtSlot()
    def on_pushButton_open_file_clicked(self):
        """
        Slot documentation goes here.
        """
        # TODO: not implemented yet
        fichier =QFileDialog.getOpenFileNames(self, "Choisir le fichier de donnees", "Y:/1.METROLOGIE/0.ARCHIVES ETALONNAGE-VERIFICATIONS/3-CARTOS-SIMULATION")
        
        if fichier:
            
            self.graph_total.canvas.ax.clear()
            self.graph_total.canvas.draw()
            self.graph_zoom.canvas.ax.clear()
            self.graph_zoom.canvas.draw()

            if self.comboBox_centrale.currentText()== "EBI 10-T":
                self.df = pd.read_excel(fichier[0], 0, 0)
                
                self.df.drop(self.df.filter(regex ="Unnamed"), axis = 1,  inplace = True)

                list_n_serie_sondes = self.df.iloc[0, list(range(1, self.df.shape[1], 2))].keys()

                for ele in list_n_serie_sondes:
                    try:
                        nom_sonde = next(x[1] for x in self.sondes_centrales if x[4] == str(ele))#                    
                        for ligne in range(self.tableWidget_sondes_centrale.rowCount()):
                            if self.tableWidget_sondes_centrale.item(ligne, 0).text() == nom_sonde:                            
                                item_num_serie_sonde =  QTableWidgetItem(str(ele))
                                self.tableWidget_sondes_centrale.setItem(ligne, 2, item_num_serie_sonde)
                    except StopIteration:
                        pass

            elif self.comboBox_centrale.currentText()== "FD5-15"  :                
                
                def date_fd5(d):
                    """convertie les dates du fichier fd5 en datetime attention à minuit le format change"""
                    try:
                        date=  pendulum.from_format(d, '%d/%m/%Y %H:%M')
                    except ValueError:
                        try:
                            date= pendulum.from_format(d, '%d/%m/%Y %H:%M:%S')
                        except ValueError:
                            d_bis = d.replace(",", ".")
                            date = pendulum.from_format(d_bis, '%d/%m/%Y %H:%M:%S.%f')

                    return date

                try:
                    self.df = pd.read_csv(fichier[0], sep="\t", decimal =",")#, false_values = ["Err.02", "Err.06", "Err.12", "Err.13"])#, converters ={"Date":to_datetime})
                except UnicodeDecodeError:

                    self.df = pd.read_csv(fichier[0], sep="\t", encoding = "cp1252", decimal =",")#, false_values = ["Err.02", "Err.06", "Err.12", "Err.13"])#, converters ={"Date":to_datetime})

                try:
                    if "Date" in list(self.df): #le mote date est ds le fichier sinon ca veut dire que c'est heure
                        self.df["Date"] = self.df["Date"].apply(lambda d : date_fd5(d))
                    else:
                        
                        self.df.rename(columns={"Heure":"Date"}, inplace = True)
                        res = QMessageBox.question(
                            self,
                            self.tr("Verification Date Cartographie"),
                            self.tr("""La cartographie a ete réalise sur une journee\nLa date indiquee dans le calendrier correspond t-elle à celle de la cartographie?"""),
                            QMessageBox.StandardButtons(
                                QMessageBox.No |
                                QMessageBox.Yes))
    #                        print(res)
                        if res == 16384:                        
                            self.df["Date"] = self.df["Date"].apply(lambda d : pendulum.parse(self.dateEdit.date().toString("yyyy-MM-dd") + " "+ str(d).replace(",", ".")))
                        else: 
                            raise ValueError

                    list_nom_sondes_fichier = [x for x in list(self.df) if x not in["Date", "M", "N°", "Heure"]]
                    list_nom_sondes_fichier.insert(0, "*")

                    
                    for ligne in range(self.tableWidget_sondes_centrale.rowCount()):
                        combobox_nom_fichier = QComboBox(self.tableWidget_sondes_centrale)
                        self.tableWidget_sondes_centrale.setCellWidget(ligne, 2, combobox_nom_fichier)
                       
                        combobox_nom_fichier.addItems(list_nom_sondes_fichier)
                        
#                        pos_carto = self.tableWidget_sondes_centrale.cellWidget(ligne, 1).currentText()
                        nom_voie_bdd = self.tableWidget_sondes_centrale.item(ligne, 0).text()
                        nom_voie_bdd_split = nom_voie_bdd.split()
#                        print(nom_voie_bdd_split)
                        
                        
                        for i in range(1, len(nom_voie_bdd_split)):
                            index=0
                            for ele in list_nom_sondes_fichier:
#                                print("nom sonde fichier {}".format(ele))
#                            
#                                print("decoupage {}".format(nom_voie_bdd_split[i]))
                                if "v" not in nom_voie_bdd_split[i]or "V" not in nom_voie_bdd_split[i]:
#                                    print("pas dedans")
                                    if nom_voie_bdd_split[i] in ele or nom_voie_bdd_split[i].upper() in str(ele).upper() :
#                                        print(" ele good {}".format(ele))
                                        combobox_nom_fichier.setCurrentIndex(index)
                                    else:
                                        pass
                                index +=1
      
                    self.tableWidget_sondes_centrale.resizeColumnsToContents()
#                    print(self.df)    
                except ValueError:
                    pass
                        
            elif self.comboBox_centrale.currentText()== "SA32":

                try:
#                    print("la pyutain")
                    self.df = pd.read_csv(fichier[0], sep="\t", decimal =",")#, false_values = ["Err.02", "Err.06", "Err.12"])

                    if len(list(self.df))<2:
                        self.df = pd.read_csv(fichier[0], sep="\t", decimal =",", header = 1)#, false_values = ["Err.02", "Err.06", "Err.12"])

                    if "Inter" in list(self.df):
                        self.df.drop("Inter", axis = 1,  inplace = True) 
                    if"Inter." in list(self.df):
                        self.df.drop("Inter.", axis = 1,  inplace = True) 
                    if "Cycle " in list(self.df):
                        self.df.drop("Cycle ", axis = 1,  inplace = True) 
                    if "Date  " in list(self.df):                        
                        self.df.rename(columns={"Date  ": "Date"}, inplace  = True)
                    if 'Heure 'in list(self.df):                        
                        self.df.rename(columns={'Heure ': "Heure"}, inplace  = True)

                        
                    self.df.drop(self.df.columns[len(list(self.df))-1], axis = 1,  inplace = True)  #enleve la derniere colonne qui n'est que des none

                    list_date = []
                    for ligne in range(len(self.df["Date"])) :
                        date = datetime.strptime(str(self.df["Date"][ligne]) +" " +str(self.df["Heure"][ligne]), '%d/%m/%y %H:%M:%S') 
                        list_date.append(date)

                    self.df["Date"] = list_date
                    if "Heure" in list(self.df): 
                        self.df.drop("Heure", axis = 1,  inplace = True) 

                    list_nom_sondes_fichier = [x for x in list(self.df) if x !="Date"]
                    list_nom_sondes_fichier.insert(0, "*")
                    
                    for ligne in range(self.tableWidget_sondes_centrale.rowCount()):
                        combobox_nom_fichier = QComboBox(self.tableWidget_sondes_centrale)
                        self.tableWidget_sondes_centrale.setCellWidget(ligne, 2, combobox_nom_fichier)
                       
                        combobox_nom_fichier.addItems(list_nom_sondes_fichier)
                        

                        nom_voie_bdd = self.tableWidget_sondes_centrale.item(ligne, 0).text().split("-")[1]

                        index=0
                        for ele in list_nom_sondes_fichier:
                            
                            if nom_voie_bdd in ele or nom_voie_bdd.upper() in ele.upper():#or str(ele).upper() in str(nom_voie_bdd).upper():
                                combobox_nom_fichier.setCurrentIndex(index)
                                                                       
                                        
                            else:     
#                                print("ele {} nom {}".format(ele, nom_voie_bdd))
#                                test = ele in nom_voie_bdd
#                                print(test)
                                pass 
                            index +=1
  
                    self.tableWidget_sondes_centrale.resizeColumnsToContents()
                
            

                except UnicodeDecodeError:
#                    print("coucou")

                    self.df = pd.read_csv(fichier[0], sep="\t", encoding = "cp1252", decimal =",")#, false_values = ["Err.02", "Err.06", "Err.12"])
                    
                    if len(list(self.df))<2:
                        self.df = pd.read_csv(fichier[0], sep="\t", decimal =",",  encoding = "cp1252", header = 1)#, false_values = ["Err.02", "Err.06", "Err.12"])
                        
                    if "Inter" in list(self.df):
                        self.df.drop("Inter", axis = 1,  inplace = True) 
                    if"Inter." in list(self.df):
                        self.df.drop("Inter.", axis = 1,  inplace = True) 
                    if "Cycle" in list(self.df):
                        self.df.drop("Cycle", axis = 1,  inplace = True) 
                    if "Date  " in list(self.df):                        
                        self.df.rename(columns={"Date  ": "Date"}, inplace  = True)
                    if 'Heure 'in list(self.df):                        
                        self.df.rename(columns={'Heure ': "Heure"}, inplace  = True)

                        
                    self.df.drop(self.df.columns[len(list(self.df))-1], axis = 1,  inplace = True)  #enleve la derniere colonne qui n'est que des none
                    
                    
                    list_date = []
                    for ligne in range(len(self.df["Date"])) :
                        date = datetime.strptime(str(self.df["Date"][ligne]) +" " +str(self.df["Heure"][ligne]), '%d/%m/%y %H:%M:%S') 
                        list_date.append(date)

                    self.df["Date"] = list_date
                    if "Heure" in list(self.df): 
                        self.df.drop("Heure", axis = 1,  inplace = True) 

                    list_nom_sondes_fichier = [x for x in list(self.df) if x !="Date"]
                    list_nom_sondes_fichier.insert(0, "*")
                    
                    for ligne in range(self.tableWidget_sondes_centrale.rowCount()):
                        combobox_nom_fichier = QComboBox(self.tableWidget_sondes_centrale)
                        self.tableWidget_sondes_centrale.setCellWidget(ligne, 2, combobox_nom_fichier)
                       
                        combobox_nom_fichier.addItems(list_nom_sondes_fichier)
                        
#                        pos_carto = self.tableWidget_sondes_centrale.cellWidget(ligne, 1).currentText()
                        nom_voie_bdd = self.tableWidget_sondes_centrale.item(ligne, 0).text()
                        nom_voie_bdd_split = nom_voie_bdd.split()
#                        print(nom_voie_bdd_split)
                        index=0
                        for ele in list_nom_sondes_fichier:
                            
                            if nom_voie_bdd in ele or nom_voie_bdd.upper() in ele.upper():#or str(ele).upper() in str(nom_voie_bdd).upper():
                                combobox_nom_fichier.setCurrentIndex(index)
                                                                       
                                        
                            else:     

                                pass 
                            index +=1
  
                    self.tableWidget_sondes_centrale.resizeColumnsToContents()
                    

    
    def plage_select_souris(self, value):
        """ fct permettant de realiser les calculs de carto 
        2 possibilité en utilisant le cursor zoom ==true ou directement avec les comboboxs zoom == false"""
        self.nettoyage_onglet_simu()
        valeur_proche_debut = np.abs( pd.Series([pd.Timestamp(index, tz="UTC")  - pd.Timestamp(value[0], tz="UTC") for index in self.copy_data["Date"]]))
        index_deb = np.argmin(valeur_proche_debut)

        valeur_proche_fin = np.abs( pd.Series([pd.Timestamp(index, tz="UTC")  - pd.Timestamp(value[1], tz="UTC") for index in self.copy_data["Date"]]))
        index_fin = np.argmin(valeur_proche_fin)+1
        
        self.tupple_index = (index_deb, index_fin)
        
        self.comboBox_debut_zone.setCurrentIndex(index_deb)
        self.comboBox_fin_zone.setCurrentIndex(index_fin)
        
#        self.resultats((index_deb, index_fin))
        

        
    def resultats(self, value_tupple_index):
        """fct qui calcul les resultats à partir du debut et fin de zone """
        self.graph_zoom.canvas.ax.clear()
#        self.graph_zoom.draw()
        index_deb = value_tupple_index[0]
#        print("debut {}".format(index_deb))
        
        index_fin = value_tupple_index[1]

        for clef in self.copy_data.keys():
#            print(clef)
            if clef !="Date":
              self.graph_zoom.canvas.ax.plot(self.copy_data[index_deb: index_fin]["Date"], self.copy_data[index_deb: index_fin][clef],'-',  label =clef, linewidth=1)
              self.graph_zoom.canvas.ax.legend(frameon=False, fontsize=9)

        xfmt= matplotlib.dates.DateFormatter('%y-%m-%d %H:%M:%S')
        self.graph_zoom.canvas.ax.xaxis.set_major_formatter(xfmt)

#        labels = self.graph_zoom.canvas.ax.get_xticklabels()
#        for label in labels:
#            label.set_rotation(6)
        self.graph_zoom.canvas.draw()

    
        index = [key for key in self.copy_data.keys() if key != "Date"]

        index_bis = ("HAD", "HAG", "HPD", "HPG", "CENTRE", "BAD", "BAG", "BPD"
                            ,"BPG", "CA","CB", "CD", "CG", "CH", "CP")
        
        index_result = [ sonde for sonde in index_bis if sonde in index]

        result = pd.DataFrame(index = index_result , columns = ["Voie","Moyenne", "Ecart Type", "Minimum", "Maximum"
                                                                                    , "Delta", "Resolution", "Derive", "Etalonnage",
                                                                                    "u_cj", "u_mj", "U_mj", 
                                                                                    "θ + Umj", "θ - Umj"])
#        print(self.copy_data[index_deb: index_fin].diff())
        vitesse_dict={}
        accelration_dict={}
        moyenne_pandas = pd.DataFrame(index = ["Vitesse", "Acceleration"])
        for nom in self.copy_data.keys():
            self.copy_data[nom].replace(["Err.02", "Err.06", "Err.13", "Err.72"], np.nan)
            
#            if nom == "BAG":
#                print(self.copy_data[nom])
#                for el in self.copy_data[nom]:
#                    print(el)
#            try:
            if nom != "Date":
#                print(nom)
                ####Regime etabli :
                vitesse_dict[nom] = np.diff(self.copy_data[index_deb: index_fin][nom].astype(float).as_matrix(columns=None))
                accelration_dict[nom] = np.diff(vitesse_dict[nom])                
#                a =[]
#                index_dtat= 
                moyenne_pandas[nom] = [np.mean(vitesse_dict[nom]), np.mean(accelration_dict[nom])]
#                moyenne_dict[str(nom + "_"+"acceleration")]= 
                
#                print(test)
                ####Calcul
                moyenne = np.nanmean(self.copy_data[index_deb: index_fin][nom].astype(float).as_matrix(columns=None))
                moyenne_round = np.around(moyenne, decimals = 2)

                ecartype = np.nanstd(self.copy_data[index_deb: index_fin][nom].astype(float).as_matrix(columns=None), ddof = 1)
                ecartype_round = np.around(ecartype, decimals = 2)
                
                min = np.nanmin(self.copy_data[index_deb: index_fin][nom].astype(float).as_matrix(columns=None))
                min_round = np.around(min, decimals = 2)
                
                max = np.nanmax(self.copy_data[index_deb: index_fin][nom].astype(float).as_matrix(columns=None))
                max_round = np.around(max, decimals = 2)
                
                delta = np.abs(max-min)
                delta_round = np.around(delta, decimals = 2)
                
#                resolution = 0.01
#                u_resolution =  resolution/(2*np.sqrt(3))
#                
#                derive = 0.15
#                u_derive = derive/(np.sqrt(3))
                
                #etalonnage
                for ligne in range(self.tableWidget_sondes_centrale.rowCount()):
                    if self.tableWidget_sondes_centrale.cellWidget (ligne,1).currentText() == nom:
                        U_etal = float(self.tableWidget_sondes_centrale.item(ligne, 6).text())                        
                        U_etal_round = float(decimal.Decimal(str(U_etal)).quantize(decimal.Decimal(str(0.01)),rounding = decimal.ROUND_UP))
                        u_etal = U_etal/2
                        
                        resolution = float(self.tableWidget_sondes_centrale.item(ligne, 9).text())
                        u_resolution =  resolution/(2*np.sqrt(3))
                        
                        derive = float(self.tableWidget_sondes_centrale.item(ligne, 10).text())
                        u_derive = derive/(np.sqrt(3))
                        
                u_cj = np.sqrt(np.power(u_etal, 2) + np.power(u_resolution, 2) + np.power(u_derive, 2))
                u_mj = np.sqrt(np.power(u_cj, 2) + np.power(ecartype, 2))
                
                U_mj = 2 * u_mj                
                U_mj_round = decimal.Decimal(str(U_mj)).quantize(decimal.Decimal(str(resolution)),rounding = decimal.ROUND_UP)
                
                moyenne_plus_U_mj = moyenne_round + float(U_mj_round)
#                print(moyenne_plus_U_mj)
#                moyenne_plus_U_mj_round =  np.around(moyenne_plus_U_mj ,  decimals = 2)
                
                moyenne_moins_U_mj = moyenne_round - float(U_mj_round)
#                moyenne_moins_U_mj_round =  np.around(moyenne_moins_U_mj ,  decimals = 2)
                
                result.loc[nom] = (nom, moyenne_round, ecartype_round, min_round, max_round, 
                                        delta_round, resolution, derive, U_etal_round, u_cj, u_mj, U_mj_round,  
                                        moyenne_plus_U_mj, moyenne_moins_U_mj)
#        print(moyenne_pandas)
#        print(accelration_dict)
        
        self.tableView_vitesse.remplir(pd.DataFrame(vitesse_dict))
        self.tableView_vitesse.resizeColumnsToContents()
        self.tableView_acceleration.remplir(pd.DataFrame(accelration_dict))
        self.tableView_acceleration.resizeColumnsToContents()
        
#        self.tableView_moyenne_vitesse_acceleration.horizon_header (["Vitesse", "Acceleration"])
        self.tableView_moyenne_vitesse_acceleration.remplir(moyenne_pandas)
        
        self.tableView_moyenne_vitesse_acceleration.resizeColumnsToContents()
        
        for clef in vitesse_dict.keys():
            self.graph_vitesse.canvas.ax.plot([x for x in range(len(vitesse_dict[clef]))], vitesse_dict[clef],'-',  label =clef, linewidth=1)
        for clef in accelration_dict.keys():
            self.graph_acceleration.canvas.ax.plot([x for x in range(len(accelration_dict[clef]))], accelration_dict[clef],'-',  label =clef, linewidth=1)
        self.graph_vitesse.canvas.draw()
        self.graph_acceleration.canvas.draw()
        #gestion  conformite graph et declaration: pass
       
        try:
            temp_desiree = float(self.lineEdit_condition_des.text())
        except ValueError:
            temp_desiree = 0.0
        try : 
            emt = float(self.comboBox_emt.currentText())
        except ValueError:
            emt = 0.0
        
        
#        print("haute {} basse {}".format(valeur_haute, valeur_basse))
        
        list_conf_sonde = []
#        self.tableWidget_conf_par_capteur.clear()
        
        for ligne in reversed(range(self.tableWidget_conf_par_capteur.rowCount())):
            self.tableWidget_conf_par_capteur.removeRow(ligne)
        
        self.graph_resultat.canvas.ax.clear()
#        self.graph_resultat.draw()
        
        for i  in range(0, len(index_result)):
            
            y = float(result.loc[index_result[i]]["Moyenne"])
            err = float(result.loc[index_result[i]]["U_mj"])

            self.graph_resultat.canvas.ax.margins(0.04, 0.06) 
            self.graph_resultat.canvas.ax.errorbar(i, y, yerr=err, fmt='o')

            #conformite :

            if self.comboBox_signe_emt.currentText() == "±":
                valeur_haute = temp_desiree + emt
                valeur_basse = temp_desiree - emt
                
                if ( y + err ) < valeur_haute and ( y - err ) > valeur_basse:
                    conforme = True
                    resultat_conf = "{} : {}".format(index_result[i],"Conforme")                
                elif y> valeur_haute or y< valeur_basse:
                    conforme = False
                    resultat_conf = "{} : {}".format(index_result[i],"Non Conforme")
                
                elif ( y + err ) >= valeur_haute or ( y - err ) <= valeur_basse:
                    conforme = False
                    resultat_conf = "{} : {}".format(index_result[i],"Conforme avec Risque")
                    
            elif self.comboBox_signe_emt.currentText() == "+":
                valeur_haute = temp_desiree + emt
                valeur_basse = None
                if ( y + err ) < valeur_haute :
                    conforme = True
                    resultat_conf = "{} : {}".format(index_result[i],"Conforme")                
                elif y> valeur_haute:
                    conforme = False
                    resultat_conf = "{} : {}".format(index_result[i],"Non Conforme")
                elif ( y + err ) >= valeur_haute :
                    conforme = False
                    resultat_conf = "{} : {}".format(index_result[i],"Conforme avec Risque")
                
            elif self.comboBox_signe_emt.currentText() == "-":
                valeur_haute = None
#                print(( y + err ))
                valeur_basse = temp_desiree - emt
                if ( y - err ) > valeur_basse:
                    conforme = True
                    resultat_conf = "{} : {}".format(index_result[i],"Conforme")                
                elif y< valeur_basse:
                    conforme = False
                    resultat_conf = "{} : {}".format(index_result[i],"Non Conforme")
                elif ( y - err ) <= valeur_basse:
                    conforme = False
                    resultat_conf = "{} : {}".format(index_result[i],"Conforme avec Risque")
            

                

            item = QTableWidgetItem(str(resultat_conf))
#            print("resultat conf {}".format(resultat_conf))
            if i <=3:
                self.tableWidget_conf_par_capteur.insertRow(i)
                self.tableWidget_conf_par_capteur.setItem(i, 0, item)
            elif i> 3 and i<=7:
              self.tableWidget_conf_par_capteur.setItem(i-4, 1, item)
            elif i>7 and i<=11:
                self.tableWidget_conf_par_capteur.setItem(i-8, 2, item)
            elif i>11 and i<=16:
                self.tableWidget_conf_par_capteur.setItem(i-12, 3, item)
            
            self.tableWidget_conf_par_capteur.resizeColumnsToContents()
            list_conf_sonde.append(conforme)            
            
            
        if False in list_conf_sonde:
            self.textEdit_conclusion_generale.setPlainText("Enceinte non Conforme")
        else:
            self.textEdit_conclusion_generale.setPlainText("Enceinte Conforme")
            
        if (valeur_haute and valeur_basse) or (valeur_haute and valeur_basse == 0) or (valeur_haute == 0 and valeur_basse ):
            self.graph_resultat.canvas.ax.plot(list(range(len(index_result))), list(repeat(valeur_haute, len(index_result))), 
                                                            color='red',  linewidth=2)
            self.graph_resultat.canvas.ax.plot(list(range(len(index_result))), list(repeat(valeur_basse, len(index_result))),
                                                            color='red',  linewidth=2)
        elif valeur_haute and not valeur_basse:
            self.graph_resultat.canvas.ax.plot(list(range(len(index_result))), list(repeat(valeur_haute, len(index_result))), 
                                                            color='red',  linewidth=2)
        elif not valeur_haute and valeur_basse:
            self.graph_resultat.canvas.ax.plot(list(range(len(index_result))), list(repeat(valeur_basse, len(index_result))),
                                                            color='red',  linewidth=2)
            
        self.graph_resultat.canvas.ax.set_xticks(np.array(np.arange(0, len(index_result), 1)))
        self.graph_resultat.canvas.ax.set_xticklabels(index_result)
        self.graph_resultat.canvas.draw()
        
        #calcul moyenne air         
        max_u_cj = result["u_cj"].max()
        max_u_cj2 = np.power(max_u_cj, 2)
        
        #sr = max(sj)
        sr = result["Ecart Type"].max()
#        print("sr {}".format(sr))
        teta_air = result["Moyenne"].mean()
#        print("teta air {}".format(teta_air))
        
        teta_air_round = np.around(teta_air, decimals = 2)
#        print("teta air arrondie{}".format(teta_air_round))
        
        self.lineEdit_teta_air.setText(str(teta_air_round))
        
        result["(Xmj-Xair)2"] = result.apply(lambda row: np.power((row['Moyenne']-teta_air), 2), axis=1)
        #∑(Xmj-Xair)2
        somme_xmj_xair_2 = result["(Xmj-Xair)2"].sum()
#        print("Xmj-Xair)2 {}".format(somme_xmj_xair_2))
        
        #sr 2(1-1/n)
        sr2_1_1div_n = np.power(sr, 2) * (1-1/len(self.copy_data[index_deb: index_fin]))
#        print("sr 2(1-1/n) {}".format(sr2_1_1div_n))
        
        # 1/N-1∑(Xmj-Xair)2
#        print(f"""{len(result["Voie"])}""")
#        print(f""" test sur : {len(result["Voie"])-1}""")
        un_N_un_somme_xmj_xair2 = (1/(len(result["Voie"])-1))*somme_xmj_xair_2
#        print("1/N-1∑(Xmj-Xair)2 {}".format(un_N_un_somme_xmj_xair2))

       #sR
        sR = np.sqrt(sr2_1_1div_n + un_N_un_somme_xmj_xair2)
#        print("sR {}".format(sR))
        
        sR2 = np.power(sR, 2)
#        print("sR² {}".format(sR2))
        U_air = 2 * np.sqrt((sR2 + max_u_cj2))
        
#        print("Uair {}".format(U_air))
        U_air_round = decimal.Decimal(str(U_air)).quantize(decimal.Decimal(str(resolution)),rounding = decimal.ROUND_UP)
#        print("U_air arrondie {}".format(U_air_round))
        
        self.lineEdit_U_air.setText(str(U_air_round))
#        print("moyenne air {} +- {}".format(teta_air_round, U_air_round))
                
        #Moyenne maximum et min avec incertitudes :
        m_max = result["θ + Umj"].max()
        m_max_round = np.around(m_max, decimals= 2)
        self.lineEdit_moy_max.setText(str(m_max_round))
        
        m_min = result["θ - Umj"].min()
        m_min_round = np.around(m_min, decimals= 2)
        self.lineEdit_moy_min.setText(str(m_min_round))
        
        #hmogeneite: "θ + Umj", "θ - Umj"
        hom = np.abs(result["θ + Umj"].max() - result["θ - Umj"].min())
        hom_round = np.around(hom, decimals=2)
        self.lineEdit_homogeneite.setText(str(hom_round))
        
        #stab:
        stab = result["Delta"].max()
        stab_round = np.round(stab, decimals=2)
        index_sonde = result["Delta"].argmax()
        
#        print("index sonde {}".format(index_sonde))
        self.lineEdit_stabilite.setText(str(stab_round))
        self.lineEdit_capteur_stab.setText(str(index_sonde))
        
        #delta consigne
        if self.comboBox_type_consigne.currentText() != "*":
            if self.lineEdit_consigne.text():
                consigne = float(self.lineEdit_consigne.text())
            else:
                consigne = 0
            ecart = consigne - teta_air
            ecart_round = np.around(ecart, decimals=2)
            self.lineEdit_ecart_consigne.setText(str(ecart_round))
        else:
            self.lineEdit_ecart_consigne.setText("Na")
#        nom_sonde = 
        for ele in result.index:
            if ele not in list(self.copy_data):
                result.drop( [ele], axis = 0, inplace =True)
#        print(result)

        self.tableView_resultats.remplir(result)
#        model = PandasModel(result) 
#        self.tableView_resultats.setModel(model)
#        self.tableView_resultats.resizeColumnsToContents()

        
        if self.radioButton_correction_non.isChecked():
            correction_donnees = False
        else:
            correction_donnees = True
        
        self.annexe ={"DATE": self.dateEdit.date(), 
                            "DONNEES":self.copy_data,
                            "CORRECTION_DONNEES" : correction_donnees ,  
                            "INDEX_DEBUT": index_deb, 
                            "INDEX_FIN": index_fin -1, #permet de tenir compte du rajout +1 pour les calculs sinon la derniere valeur n'est pas pris en compte c'est une liste
                            "RESULTATS": result, 
                            "LIEU": self.lineEdit_affectation.text(), 
                            "ENCEINTE": self.lineEdit_enceinte.text(),  
                            "CENTRALE" : self.comboBox_nom_centrale.currentText()
                            }
                        
                    
                
               
            
    
    @pyqtSlot(int)
    def on_comboBox_centrale_currentIndexChanged(self, index):
        """
        Slot documentation goes here.
        """
        model = self.comboBox_centrale.currentText()
        list_central = [x[1] for x in self.centrales if x[3] == model]

        self.comboBox_nom_centrale.clear()
        self.comboBox_nom_centrale.addItems(list_central)
    
    @pyqtSlot(int)
    def on_comboBox_nom_centrale_currentIndexChanged(self, index):
        """
        Slot documentation goes here.
        """
        try:
            nom_centrale = self.comboBox_nom_centrale.currentText()
            id_centrale = next(x[0] for x in self.centrales if x[1] == nom_centrale)
            list_sondes = (x[1] for x in self.sondes_centrales if x[6] == id_centrale)
            
            list_pos = ["*","HAD", "HAG", "HPD", "HPG", "CENTRE", "BAD", "BAG", "BPD"
                                ,"BPG", "CA","CB", "CD", "CG", "CH", "CP"]
            
            #gestion tableau tableWidget_sondes_centrale
            nbr_ligne= self.tableWidget_sondes_centrale.rowCount()
            for ligne in reversed(range(nbr_ligne)):
                self.tableWidget_sondes_centrale.removeRow(ligne)
                
            for sonde in list_sondes:
                self.tableWidget_sondes_centrale.insertRow(0)
                item_nom =  QTableWidgetItem(str(sonde))
                self.tableWidget_sondes_centrale.setItem(0, 0, item_nom)
                
                #combobox position carto 
                combobox_pos_carto = QComboBox(self.tableWidget_sondes_centrale)
                self.tableWidget_sondes_centrale.setCellWidget(0, 1, combobox_pos_carto)            
                combobox_pos_carto.addItems(list_pos)
                
                index = 0
                for ele in list_pos:
                    if ele in sonde or ele in str(sonde).upper():
                        combobox_pos_carto.setCurrentIndex(index)
                    index +=1
    
                #gestion des polynomes
                poly = self.db.polynome(sonde)
#                print("poly {}".format(poly))
                item_ax2 =  QTableWidgetItem(str(poly[0]))
                self.tableWidget_sondes_centrale.setItem(0, 3, item_ax2)
                item_bx =  QTableWidgetItem(str(poly[1]))
                self.tableWidget_sondes_centrale.setItem(0, 4, item_bx)
                item_c =  QTableWidgetItem(str(poly[2]))
                self.tableWidget_sondes_centrale.setItem(0, 5, item_c)
                
                u_etal =   self.db.u_etal(sonde)
                item_u_etal =  QTableWidgetItem(str(u_etal))
                self.tableWidget_sondes_centrale.setItem(0, 6, item_u_etal)
                
                item_nom_ce = QTableWidgetItem(str(poly[3]))
                self.tableWidget_sondes_centrale.setItem(0, 7, item_nom_ce)
                
                date_fr = poly[4].strftime('%d/%m/%Y')
#                print(date_fr)
                item_date_ce = QTableWidgetItem(str(date_fr))
                self.tableWidget_sondes_centrale.setItem(0, 8, item_date_ce)
                
                item_resolution = QTableWidgetItem(str(0.01))
                self.tableWidget_sondes_centrale.setItem(0, 9, item_resolution)
                
                item_derive = QTableWidgetItem(str(0.15))
                self.tableWidget_sondes_centrale.setItem(0, 10, item_derive)
                
        except (StopIteration, TypeError):
            pass
  
    
    @pyqtSlot()
    def on_commandLinkButton_affiche_donnees_clicked(self):
        """
        Slot documentation goes here.
        """
        try:
            pd.options.mode.chained_assignment = None
            
            self.comboBox_debut_zone.clear()
            self.comboBox_fin_zone.clear()        
            self.comboBox_debut_zone_2.clear()
            self.comboBox_fin_zone_2.clear()
            
#            self.copy_data = pd.DataFrame()
            self.copy_data = self.df.copy() #permet de ne pas toucher aux valeurs de bases pour reaffectation
#            self.copy_data.is_copy= False

            if self.radioButton_correction_non.isChecked():
                #Donnnees non corrigees:            
                if self.comboBox_centrale.currentText()== "EBI 10-T":
                    self.mise_en_forme_ebro()    
    
                elif self.comboBox_centrale.currentText()== "FD5-15" or self.comboBox_centrale.currentText() == "SA32":
                    self.mise_en_forme_fd5()
    
            
            else: #donnees à corriger
                if self.comboBox_centrale.currentText()== "EBI 10-T":
                    self.mise_en_forme_ebro()     
                        
                elif self.comboBox_centrale.currentText()== "FD5-15" or  self.comboBox_centrale.currentText() == "SA32":                
                    self.mise_en_forme_fd5()
    
                self.copy_data = self.copy_data.apply(self.appli_correction,  axis=0)
    #        false_values = ["Err.02", "Err.06", "Err.12", "Err.13"]
    
    
    #        self.copy_data[self.copy_data.str.contains("Err"), na=False)] #=np.nan 
            self.copy_data.replace(to_replace = "Err?", value =np.nan, regex= True, inplace = True)
    
    
            self.copy_data.replace({"," : ".", " ":"", "  ":"", "    ":"" }, 
                                            regex = True, inplace=True)
                                            
#            print("replace {}".format(self.copy_data))
            if len(list(self.copy_data)):
                self.tableView_donnees_fichier.remplir(self.copy_data)
        
                dates = [str(date) for date in self.copy_data["Date"]]

                self.comboBox_debut_zone.addItems(dates)
                self.comboBox_fin_zone.addItems(dates)        
                self.comboBox_debut_zone_2.addItems(dates)
                self.comboBox_fin_zone_2.addItems(dates)
        
                self.plot_graph_total(self.copy_data)
            else:
                QMessageBox.critical(self, 
                    self.trUtf8("Selection"), 
                    self.trUtf8("vous n'avez pas selectionné de sondes"))
            
            
            
        except AttributeError:
            pass   

    def plot_graph_total(self, dataframe):
        
        self.graph_total.canvas.ax.clear()
#        self.graph_total.draw()
        
#        print(dataframe["Date"])
#        for ele in dataframe["Date"]:
#            print(type(ele))
#        dates = 
#(dataframe["Date"])
#        print(dates)
        for clef in dataframe.keys():
          if clef !="Date": 
            self.graph_total.canvas.ax.plot(dataframe["Date"], dataframe[clef],'-',  label =clef, linewidth=1)
            self.graph_total.canvas.ax.legend(frameon=False, fontsize=10)

        self.cursor = Cursor(self.graph_total.canvas.ax, useblit=True, color='red', linewidth=2)
            
        xfmt= matplotlib.dates.DateFormatter('%y-%m-%d %H:%M:%S')
        self.graph_total.canvas.ax.xaxis.set_major_formatter(xfmt)

        labels = self.graph_total.canvas.ax.get_xticklabels()
        for label in labels:
            label.set_rotation(6)

        self.graph_total.canvas.draw()
        
#            Cursor(self.graph_total.canvas.ax, useblit=True, color='red', linewidth=2)
        
        
        self.connect(self.graph_total.canvas, SIGNAL("zoom(PyQt_PyObject)"), self.plage_select_souris)
    
    
    def appli_correction(self, mesure_brute):
        """fct utilise par la dtataframe pour corriger les donnees qui recupere le polynome dans le tableau  tableWidget_sondes_centrale en fct de la position de la sonde 
        et retourne la valeur corrigée a integrer dans la dtataframe copy"""
#        print(mesure_brute.name)
        if mesure_brute.name !="Date" :
            for ligne in range(self.tableWidget_sondes_centrale.rowCount()):
                pos = self.tableWidget_sondes_centrale.cellWidget(ligne, 1).currentText()
                try:
                    if pos == mesure_brute.name and self.tableWidget_sondes_centrale.item(ligne, 2).text() != "*":                
                        coeff_a = float(self.tableWidget_sondes_centrale.item(ligne, 3).text())
                        coeff_b = float(self.tableWidget_sondes_centrale.item(ligne, 4).text())
                        coeff_c = float(self.tableWidget_sondes_centrale.item(ligne, 5).text())
                    
                        poly=(coeff_a, coeff_b, coeff_c)
                except:
#                    print("except correction")
                    if pos == mesure_brute.name and self.tableWidget_sondes_centrale.cellWidget(ligne, 2).currentText() != "*":                
                        coeff_a = float(self.tableWidget_sondes_centrale.item(ligne, 3).text())
                        coeff_b = float(self.tableWidget_sondes_centrale.item(ligne, 4).text())
                        coeff_c = float(self.tableWidget_sondes_centrale.item(ligne, 5).text())
                    
                        poly=(coeff_a, coeff_b, coeff_c)

                
            try:
                mesure_corrigee = mesure_brute + poly[0]* np.power(mesure_brute, 2) + poly[1] * mesure_brute + poly[2]  

                return mesure_corrigee
            except:
                return mesure_brute
        else:
            return mesure_brute
    
    def mise_en_forme_ebro(self):
        """met les donnees de selfcopy en forme"""
        self.copy_data.drop(list(range(6)),axis = 0,  inplace=True)

        self.copy_data.drop(self.df.columns[list(range(2, self.df.shape[1], 2))],axis = 1,  inplace=True)
        
        dict_new_column_name ={}


        for ligne in range(self.tableWidget_sondes_centrale.rowCount()):
            if self.tableWidget_sondes_centrale.item(ligne, 2):
                if self.tableWidget_sondes_centrale.cellWidget(ligne, 1).currentText() != "*" :

                    nom_sonde_carto = self.tableWidget_sondes_centrale.cellWidget(ligne, 1).currentText()

                    nom_sonde_fichier = int(self.tableWidget_sondes_centrale.item(ligne, 2).text())

                    dict_new_column_name[nom_sonde_fichier]  =   nom_sonde_carto
                else:
                    self.copy_data.drop( int(self.tableWidget_sondes_centrale.item(ligne, 2).text()),
                                                             axis =1, inplace=True)
            else:
                pass
        dict_new_column_name["Numéro de série"] = "Date"
        
        self.copy_data.drop([x for x in list(self.copy_data) if x not in dict_new_column_name.keys()],
                            axis=1,inplace=True)
        self.copy_data.rename(columns= dict_new_column_name, inplace=True)
        
        
#        list_pos = ["*","HAD", "HAG", "HPD", "HPG", "CENTRE", "BAD", "BAG", "BPD"
#                    ,"BPG", "CA","CB", "CD", "CG", "CH", "CP"]
#        for clef in self.copy_data.keys():
#            if clef not in list_pos and clef !="Date":
#                self.copy_data.drop(clef,axis = 1,  inplace=True)             
                
        def date_ebro(d):
            """convertie les dates du fichier ebro en datetime attention à minuit le format change"""
#            print("date {} typedate {}".format(d, type(d)))
            try:
                
                date= pendulum.from_format(d, '%d/%m/%Y %H:%M:%S')
            except ValueError:
                date= pendulum.from_format(d, '%d/%m/%Y')
            except TypeError:
                date = np.nan
            return date
            
        self.copy_data["Date"] = self.copy_data["Date"].apply(lambda d: date_ebro(d))#,  inplace=True)
#        print(self.copy_data)
        self.copy_data = self.copy_data.dropna()
        
#        new_index = [x for x in range(len(self.copy_data))]
#        print(new_index)
        self.copy_data.reset_index(inplace = True)
#        self.copy_data.drop("index",axis = 1,  inplace=True)         
##        print("reset_index {}".format(self.copy_data))
#        self.copy_data.reindex(new_index)
#        print("reindex {}".format(self.copy_data))
#                
                
    def mise_en_forme_fd5(self):
        """met les donnees de selfcopy en forme"""
        dict_new_column_name ={}
#        print(self.copy_data)
        if "M"  in list(self.copy_data):
            self.copy_data.drop("M",axis = 1,  inplace=True)
        if "N°" in  list(self.copy_data):
            self.copy_data.drop("N°",axis = 1,  inplace=True)
            
        for ligne in range(self.tableWidget_sondes_centrale.rowCount()):
            if self.tableWidget_sondes_centrale.cellWidget(ligne, 2).currentText() != "*"  :
                if self.tableWidget_sondes_centrale.cellWidget(ligne, 1).currentText() != "*":
    
                    nom_sonde_carto = self.tableWidget_sondes_centrale.cellWidget(ligne, 1).currentText()
                    nom_sonde_fichier = self.tableWidget_sondes_centrale.cellWidget(ligne, 2).currentText()
                    dict_new_column_name[nom_sonde_fichier]  =   nom_sonde_carto
                else:
                    self.copy_data.drop( self.tableWidget_sondes_centrale.cellWidget(ligne, 2).currentText(),
                                                             axis =1, inplace=True)    #where 1 is the axis number (0 for rows and 1 for columns.)
            else:
                pass
        

        
        dict_new_column_name["Date"] = "Date"
        
        
        self.copy_data.drop([x for x in list(self.copy_data) if x not in dict_new_column_name.keys()],
                            axis=1,inplace=True)
        
        self.copy_data.rename(columns= dict_new_column_name, inplace=True)
        
        
        
#        print("copy data {}".format(self.copy_data))
    
#    @pyqtSlot()
#    def on_actionRapport_Carto_triggered(self):
#        """
#        permet d'exporter un rapport de carto avec annexe
#        """
#        try:
#            sauvegarde = self.donnees_rapport()
#            
#            file = QFileDialog.getSaveFileName(None ,  "Selectionner le dossier de sauvegarde de l'annexe", "y:/1.METROLOGIE/0.ARCHIVES ETALONNAGE-VERIFICATIONS/3-CARTOS-SIMULATION", '*.pdf' )
#    
#            if file !="":            
#    #            annexe = Rapport(file)
#    #            annexe.annexe(self.sauvegarde)
#                
#                rapport = Rapport(file)
#                rapport.rapport_carto(sauvegarde)
#        except AttributeError:
#            pass

    def donnees_rapport(self):
        """fct qui encapsule les donnees pour les rapports :"""
        sauvegarde = {}
        administratif = {}
        resultat = {}
        sauv_simulation = {}
        sauvegarde["annexe"] = self.annexe
        
        #gestion enceinte:
        administratif["ident_enceinte"]= self.lineEdit_enceinte.text()
        administratif["design_litt"] = self.lineEdit_designation_litt.text()
        administratif["constructeur_enceinte"]= self.lineEdit_constructeur.text()
        administratif["model_enceinte"]= self.lineEdit_model.text()
        administratif["nserie_enceinte"]= self.lineEdit_n_serie.text()
        
        
#        self.db.client(self, code_client)
        
        #client et localisation enceinte
        administratif["client"]= self.lineEdit_code.text()
        client = self.db.client(administratif["client"])
        administratif["nom_client"]= client[0]
        administratif["adresse_client"]= client[1]
        administratif["ville_client"]= client[2]
        administratif["code_postal_client"]= client[3]
        
        administratif["site"]= self.lineEdit_site.text()
        administratif["localisation"]= self.lineEdit_localisation.text()
        administratif["affectation"]= self.lineEdit_affectation.text()
        administratif["sous_affectation"]= self.lineEdit_sous_affect.text()
        administratif["responsable_mesure"] = self.comboBox_responsable_mesure.currentText()
        
        #gestion application
        administratif["application"] = self.comboBox_application.currentText()
        administratif["emt_processus"] = self.comboBox_emt.currentText()
#        try:
#            float(self.lineEdit_condition_des.text())
        administratif["condition_desiree"] = self.lineEdit_condition_des.text()
#        except:
#            QMessageBox.critical(self, 
#                    self.trUtf8("Condition désirée"), 
#                    self.trUtf8("La condition désirée saisie est incorrect"))
        administratif["signe_EMT"] = self.comboBox_signe_emt.currentText()
#        try:
#            float(self.lineEdit_consigne.text())
        administratif["temp_consign"] = self.lineEdit_consigne.text()
        administratif["type_consign"] = self.comboBox_type_consigne.currentText()
        
#        except:
#            QMessageBox.critical(self, 
#                    self.trUtf8("Temperature de consigne"), 
#                    self.trUtf8("La temperature de consigne saisie est incorrect"))
        
        #gestion donnees à envoyer au rapport:
        nom_centrale = self.comboBox_nom_centrale.currentText()
        administratif["model_centrale"] = self.comboBox_centrale.currentText()
        administratif["nom_centrale"] = nom_centrale
        administratif["marque"] = next(x[2] for x in self.centrales if x[1] == nom_centrale)
        administratif["n_serie"] = next(x[4] for x in self.centrales if x[1] == nom_centrale)
        
        tableau_sondes_centrale = []
        for ligne in range(self.tableWidget_sondes_centrale.rowCount()):
            if not self.tableWidget_sondes_centrale.cellWidget(ligne, 2):
                if self.tableWidget_sondes_centrale.cellWidget(ligne, 1).currentText() != "*" \
                    and self.tableWidget_sondes_centrale.item(ligne, 2): ###### probleme pour centrale et EBEOR vs DATALOG
                                    
                    nom_voie = self.tableWidget_sondes_centrale.item(ligne, 0).text()
                    emplacement = self.tableWidget_sondes_centrale.cellWidget(ligne, 1).currentText()                
                    try:
                        nom_fichier = self.tableWidget_sondes_centrale.item(ligne, 2).text()              
                    except:
                        nom_fichier =self.tableWidget_sondes_centrale.cellWidget(ligne, 2).currentText()
                        
                    u_etal = decimal.Decimal(str(self.tableWidget_sondes_centrale.item(ligne, 6).text()))\
                                        .quantize(decimal.Decimal(str(0.01)),rounding = decimal.ROUND_UP)
                                        
                    n_ce = self.tableWidget_sondes_centrale.item(ligne, 7).text()
                    date_etal = self.tableWidget_sondes_centrale.item(ligne, 8).text()
                    
                    resolution = self.tableWidget_sondes_centrale.item(ligne, 9).text()
                    derive = self.tableWidget_sondes_centrale.item(ligne, 10).text()
                    
                    tableau_sondes_centrale.append([nom_voie, emplacement,nom_fichier, 
                                                    u_etal, n_ce, date_etal,  resolution, derive])
            else:
                if self.tableWidget_sondes_centrale.cellWidget(ligne, 1).currentText() != "*" \
                    and self.tableWidget_sondes_centrale.cellWidget(ligne, 2).currentText() !="*": ###### probleme pour centrale et EBEOR vs DATALOG
                                    
                    nom_voie = self.tableWidget_sondes_centrale.item(ligne, 0).text()
                    emplacement = self.tableWidget_sondes_centrale.cellWidget(ligne, 1).currentText()                
                    try:
                        nom_fichier = self.tableWidget_sondes_centrale.item(ligne, 2).text()              
                    except:
                        nom_fichier =self.tableWidget_sondes_centrale.cellWidget(ligne, 2).currentText()
                        
                    u_etal = decimal.Decimal(str(self.tableWidget_sondes_centrale.item(ligne, 6).text()))\
                                        .quantize(decimal.Decimal(str(0.01)),rounding = decimal.ROUND_UP)
                                        
                    n_ce = self.tableWidget_sondes_centrale.item(ligne, 7).text()
                    date_etal = self.tableWidget_sondes_centrale.item(ligne, 8).text()
                    
                    resolution = self.tableWidget_sondes_centrale.item(ligne, 9).text()
                    derive = self.tableWidget_sondes_centrale.item(ligne, 10).text()
                    
                    tableau_sondes_centrale.append([nom_voie, emplacement,nom_fichier, 
                                                    u_etal, n_ce, date_etal,  resolution, derive])
                 
#        print(f"tableau avant bdd {tableau_sondes_centrale}")
        
        administratif["tableau_centrale"] = tableau_sondes_centrale
        sauvegarde["administratif"] = administratif
        
        tableau_resultat =[]
        for ligne in range(self.tableView_resultats.rowCount()):
            donnees_ligne = self.tableView_resultats.return_row(ligne)
            voie = donnees_ligne["Voie"]
            moyenne = np.around(donnees_ligne["Moyenne"], decimals = 2)
            ecart_type = np.around(donnees_ligne["Ecart Type"], decimals = 2)
            min = np.around(donnees_ligne["Minimum"], decimals = 2)
            max = np.around(donnees_ligne["Maximum"], decimals = 2)
            delta = np.around(donnees_ligne["Delta"], decimals = 2)
            resolution = donnees_ligne["Resolution"]
            derive = donnees_ligne["Derive"]
            u_cj = donnees_ligne["u_cj"]
            u_mj = donnees_ligne["u_mj"]
            U_mj = donnees_ligne["U_mj"]
            tableau_resultat.append([voie, moyenne, ecart_type, 
                                                min, max, delta, resolution, derive, resolution, 
                                                u_cj, u_mj, U_mj])
        
        resultat["tableau_resultats"] = tableau_resultat
        
        resultat["temp_air"] = self.lineEdit_teta_air.text()
        resultat["U_temp_air"] = self.lineEdit_U_air.text()
        if self.lineEdit_ecart_consigne.text() != "Na":
            resultat["ecart_consigne"] = self.lineEdit_ecart_consigne.text()
        else:
            resultat["ecart_consigne"] = None
            
        resultat["moy_max"] = self.lineEdit_moy_max.text()
        resultat["moy_min"] = self.lineEdit_moy_min.text()
        resultat["homogeneite"] = self.lineEdit_homogeneite.text()
        resultat["stab"] = self.lineEdit_stabilite.text()
        resultat["position_stab"] = self.lineEdit_capteur_stab.text()
        
        #sauvegarde graph resultat
        imgdata = self.graph_resultat.sauvegarde()
        
        
        resultat["graph_result"] =imgdata
#        print(imgdata)
        
        resultat["objet_remarques"] = self.textEdit_objet_remarques.toPlainText()
        resultat["conclusion_generale"] = self.textEdit_conclusion_generale.toPlainText()
        resultat["conseils"] = self.textEdit_conseils.toPlainText()
        
        tableau_conf_par_capteur = []        
        for ligne in range(self.tableWidget_conf_par_capteur.rowCount()):
            list_ligne = []
            if self.tableWidget_conf_par_capteur.item(ligne, 0): 
                list_ligne.append(self.tableWidget_conf_par_capteur.item(ligne, 0).text())
            else: list_ligne.append("")
            
            if self.tableWidget_conf_par_capteur.item(ligne, 1): 
                list_ligne.append(self.tableWidget_conf_par_capteur.item(ligne, 1).text())
            else: list_ligne.append("")
            
            if self.tableWidget_conf_par_capteur.item(ligne, 2): 
                list_ligne.append(self.tableWidget_conf_par_capteur.item(ligne, 2).text())
            else: list_ligne.append("")
            
            if self.tableWidget_conf_par_capteur.item(ligne, 3): 
                list_ligne.append(self.tableWidget_conf_par_capteur.item(ligne, 3).text())
            else: list_ligne.append("")
            tableau_conf_par_capteur.append(list_ligne)    
        
        resultat["tableau_conformite_par_capteur"] = tableau_conf_par_capteur
#        id_centrale = next(x[0] for x in self.centrales if x[1] == nom_centrale)
        
        sauvegarde["resultats"] = resultat
        
        
        
        #gestion de la simulation
#        print(self.annexe_simulation)
        if self.annexe_simulation:
            sauv_simulation["simulation"] = True
            
            sauv_simulation["donnees_simu"] = self.simulation
            #sauvegarde graph simulation
            imgdata = self.graph_zoom_2.sauvegarde()          
            sauv_simulation["graph_simulation"] = imgdata
            
            imgdata_2 = self.graph_resultat_2.sauvegarde()          
            sauv_simulation["graph_simulation_resultat"] = imgdata_2
            
            sauv_simulation["conclusion_generale"] = self.textEdit_conclusion_generale_2.toPlainText()
        else:
            sauv_simulation["simulation"] = False

            
        sauvegarde["simulation"]= sauv_simulation
#        print(sauvegarde)
        return sauvegarde
    
    @pyqtSlot(str)
    def on_comboBox_fin_zone_currentIndexChanged(self, p0):
        """
        Slot documentation goes here.
        """
#        print("coucou")
#        print("index combobox {}".format( self.comboBox_fin_zone.currentIndex()))
        try:
            index_combo= self.comboBox_fin_zone.currentIndex()
            if index_combo == 0 or index_combo == -1:
                raise IndexError
#                print(self.comboBox_fin_zone.currentText())
        
            else:
                self.nettoyage_onglet_simu()
                index_debut = self.comboBox_debut_zone.currentIndex()
#                debut_date_time = datetime.strptime(debut, '%Y-%m-%d %H:%M:%S')
                index_fin = self.comboBox_fin_zone.currentIndex() + 1 #permet de prendre en compte la derniier valeur selectionnee dans les calculs car c'est une liste
#                print(index_fin)
#                print(self.comboBox_fin_zone.currentText())
#                print(self.copy_data)
#                fin_date_time =datetime.strptime(fin, '%Y-%m-%d %H:%M:%S')
                self.tupple_index = (index_debut, index_fin)
                self.resultats(self.tupple_index)
                

                
        except IndexError :
            
            pass
    
    @pyqtSlot(QDate)
    def on_dateEdit_dateChanged(self, date):
        """
        Slot documentation goes here.
        """

        self.date_calendrier = pendulum.parse(self.dateEdit.date().toString("yyyy-MM-dd"))#, 'Europe/Paris')

    
    @pyqtSlot(str)
    def on_comboBox_fin_zone_2_currentIndexChanged(self, p0):
        """
        permet de reduire la zone totale
        """
        try:
            index_combo=self.comboBox_fin_zone_2.currentIndex()
            if index_combo == 0:
                raise IndexError
        
            else:
                

                index_deb = int(self.comboBox_debut_zone_2.currentIndex())
                index_fin = int(self.comboBox_fin_zone_2.currentIndex())

                self.copy_data = self.copy_data.loc[index_deb:index_fin]
                
#                new_index = [x for x in range(len(self.copy_data))]

                self.copy_data.reset_index(inplace = True)
#                print(f"reset {self.copy_data.index.tolist()}")
#                self.copy_data.drop("index",axis = 1,  inplace=True)
#                print(f"drop {self.copy_data.index.tolist()}")
#
#                self.copy_data.reindex(new_index)
                

                
#                print("redecoupe {}".format( self.copy_data))
#                print(f"nex index {self.copy_data.index.tolist()}")
                

                self.plot_graph_total(self.copy_data)
                
                self.tableView_donnees_fichier.remplir(self.copy_data)

                dates = [str(date) for date in self.copy_data["Date"]]        

                self.comboBox_debut_zone.clear()
                self.comboBox_fin_zone.clear()    
                self.comboBox_debut_zone.addItems(dates)
                self.comboBox_fin_zone.addItems(dates)          
         
                self.comboBox_debut_zone_2.addItems(dates)
                self.comboBox_fin_zone_2.addItems(dates)

        except IndexError :            
            pass
    
    @pyqtSlot()
    def on_commandLinkButton_affiche_donnees_simulation_clicked(self):
        """
        Slot documentation goes here.
        """
        
        self.annexe_simulation = True
        
        index_deb = self.tupple_index[0]
        index_fin = self.tupple_index[1]
 
        self.dict_simulation = OrderedDict()
        
        
        def calcul_simulation_bis(donnees):
            """calcul les donnees de temperature simulees donnees =  self.copy_data[colonne]
            et renvoie un dict : {nom_emplacement : listdes donnees}"""
            list_donnees_simul = []
            for ligne in range(index_deb,  index_fin):
                if ligne == index_deb:
                    valeur = (28*donnees.mean()+donnees[index_deb])/(28+1)
                    list_donnees_simul.append(valeur)
                else:
                    valeur = (28*list_donnees_simul[ligne-index_deb-1]+ donnees[ligne])/(28+1)
                    list_donnees_simul.append(valeur)
            self.dict_simulation[donnees.name]=list_donnees_simul

        
        for colonne in list(self.copy_data):
            if colonne !="Date":
                calcul_simulation_bis(self.copy_data[colonne][index_deb:index_fin])
            else : 
                self.dict_simulation["Date"] = list(self.copy_data["Date"][index_deb:index_fin])

        self.simulation = pd.DataFrame(data = self.dict_simulation)

        self.tableView_donnees_fichier_2.remplir(self.simulation)

        self.graph_zoom_2.canvas.ax.clear()
#        self.graph_zoom_2.draw()
        
        
        for clef in self.simulation.keys():
            if clef !="Date":
              self.graph_zoom_2.canvas.ax.plot_date(self.simulation["Date"], self.simulation[clef],'-',  label =clef, linewidth=1)
              self.graph_zoom_2.canvas.ax.legend(frameon=False, fontsize=9)
              self.graph_zoom_2.canvas.draw()
              
              
        index = [key for key in self.simulation.keys() if key != "Date"]

        index_bis = ("HAD", "HAG", "HPD", "HPG", "CENTRE", "BAD", "BAG", "BPD"
                            ,"BPG", "CA","CB", "CD", "CG", "CH", "CP")
        
        index_result = [ sonde for sonde in index_bis if sonde in index]

        result = pd.DataFrame(index = index_result , columns = ["Voie","Moyenne", "Ecart Type", "Minimum", "Maximum"
                                                                                    , "Delta", "Resolution", "Derive", "Etalonnage",
                                                                                    "u_cj", "u_mj", "U_mj", 
                                                                                    "θ + Umj", "θ - Umj"])

        for nom in self.simulation.keys():
            if nom != "Date":
#                moyenne = self.simulation[nom].mean()
                moyenne = np.nanmean(self.simulation[nom].astype(float).as_matrix(columns=None))               
                moyenne_round = np.around(moyenne, decimals = 2)

                ecartype = np.nanstd(self.simulation[nom].astype(float).as_matrix(columns=None), ddof = 1)
#                ecartype = self.simulation[nom].std()
                ecartype_round = np.around(ecartype, decimals = 2)
                
                min = np.nanmin(self.simulation[nom].astype(float).as_matrix(columns=None))
#                min = self.simulation[nom].min()
                min_round = np.around(min, decimals = 2)
                
                max = np.nanmax(self.simulation[nom].astype(float).as_matrix(columns=None))
#                max = self.simulation[nom].max()
                max_round = np.around(max, decimals = 2)
                
                delta = np.abs(max-min)
                delta_round = np.around(delta, decimals = 2)
                
#                resolution = 0.01
#                u_resolution =  resolution/(2*np.sqrt(3))
#                
#                derive = 0.15
#                u_derive = derive/(np.sqrt(3))
#                
                #etalonnage
                for ligne in range(self.tableWidget_sondes_centrale.rowCount()):
                    if self.tableWidget_sondes_centrale.cellWidget (ligne,1).currentText() == nom:
                        U_etal = float(self.tableWidget_sondes_centrale.item(ligne, 6).text())                        
                        U_etal_round = float(decimal.Decimal(str(U_etal)).quantize(decimal.Decimal(str(0.01)),rounding = decimal.ROUND_UP))
                        u_etal = U_etal/2
                        
                        resolution = float(self.tableWidget_sondes_centrale.item(ligne, 9).text())
                        u_resolution =  resolution/(2*np.sqrt(3))
                        
                        derive = float(self.tableWidget_sondes_centrale.item(ligne, 10).text())
                        u_derive = derive/(np.sqrt(3))
                        
                u_cj = np.sqrt(np.power(u_etal, 2) + np.power(u_resolution, 2) + np.power(u_derive, 2))
                u_mj = np.sqrt(np.power(u_cj, 2) + np.power(ecartype, 2))
                
                U_mj = 2 * u_mj                
                U_mj_round = decimal.Decimal(str(U_mj)).quantize(decimal.Decimal(str(resolution)),rounding = decimal.ROUND_UP)
                
                moyenne_plus_U_mj = moyenne_round + float(U_mj_round)
#                print(moyenne_plus_U_mj)
#                moyenne_plus_U_mj_round =  np.around(moyenne_plus_U_mj ,  decimals = 2)
                
                moyenne_moins_U_mj = moyenne_round - float(U_mj_round)
#                moyenne_moins_U_mj_round =  np.around(moyenne_moins_U_mj ,  decimals = 2)
                
                result.loc[nom] = (nom, moyenne_round, ecartype_round, min_round, max_round, 
                                        delta_round, resolution, derive, U_etal_round, u_cj, u_mj, U_mj_round,  
                                        moyenne_plus_U_mj, moyenne_moins_U_mj)

        #Affichage de result
        
        self.tableView_resultats_simu.remplir(result)
        
        
        
        
        #gestion  conformite graph et declaration: pass       
        try:
            temp_desiree = float(self.lineEdit_condition_des.text())
        except ValueError:
            temp_desiree = 0.0
        try : 
            emt = float(self.comboBox_emt.currentText())
        except ValueError:
            emt = 0.0
        
        valeur_haute = temp_desiree + emt
        valeur_basse = temp_desiree - emt
#        print("haute {} basse {}".format(valeur_haute, valeur_basse))
        
        list_conf_sonde = []
#        self.tableWidget_conf_par_capteur.clear()
        self.graph_resultat_2.canvas.ax.clear()
#        self.graph_resultat_2.draw()
        for i  in range(0, len(index_result)):
            
            y= float(result.loc[index_result[i]]["Moyenne"])
            err = float(result.loc[index_result[i]]["U_mj"])
            self.graph_resultat_2.canvas.ax.margins(0.04, 0.06) 
            self.graph_resultat_2.canvas.ax.errorbar(i, y, yerr=err, fmt='o')
            
            #conformite :
            if self.comboBox_signe_emt.currentText() == "±":
                valeur_haute = temp_desiree + emt
                valeur_basse = temp_desiree - emt
                
                if ( y + err ) < valeur_haute and ( y + err ) > valeur_basse:
                    conforme = True
#                    resultat_conf = "{} : {}".format(index_result[i],"Conforme")                
                elif y> valeur_haute or y< valeur_basse:
                    conforme = False
#                    resultat_conf = "{} : {}".format(index_result[i],"Non Conforme")
                elif ( y + err ) >= valeur_haute or ( y + err ) <= valeur_basse:
                    conforme = False
#                    resultat_conf = "{} : {}".format(index_result[i],"Conforme avec Risque")
                    
            elif self.comboBox_signe_emt.currentText() == "+":
                valeur_haute = temp_desiree + emt
                valeur_basse = None
                if ( y + err ) < valeur_haute :
                    conforme = True
#                    resultat_conf = "{} : {}".format(index_result[i],"Conforme")                
                elif y> valeur_haute:
                    conforme = False
#                    resultat_conf = "{} : {}".format(index_result[i],"Non Conforme")
                elif ( y + err ) >= valeur_haute :
                    conforme = False
#                    resultat_conf = "{} : {}".format(index_result[i],"Conforme avec Risque")
                
            elif self.comboBox_signe_emt.currentText() == "-":
                valeur_haute = None
                valeur_basse = temp_desiree - emt
                if ( y + err ) > valeur_basse:
                    conforme = True
#                    resultat_conf = "{} : {}".format(index_result[i],"Conforme")                
                elif y< valeur_basse:
                    conforme = False
#                    resultat_conf = "{} : {}".format(index_result[i],"Non Conforme")
                elif ( y + err ) <= valeur_basse:
                    conforme = False
#                    resultat_conf = "{} : {}".format(index_result[i],"Conforme avec Risque")

#            print(conforme)
            list_conf_sonde.append(conforme)            
#        print(list_conf_sonde)
            
        if False in list_conf_sonde:
            self.textEdit_conclusion_generale_2.setPlainText("La simulation de la température à coeur est non conforme")
        else:
            self.textEdit_conclusion_generale_2.setPlainText("La simulation de la température à coeur est conforme")
            
        
        self.graph_resultat_2.canvas.ax.plot(list(range(len(index_result))), list(repeat(valeur_haute, len(index_result))), 
                                                        color='red',  linewidth=2)
        self.graph_resultat_2.canvas.ax.plot(list(range(len(index_result))), list(repeat(valeur_basse, len(index_result))),
                                                        color='red',  linewidth=2)
        
        self.graph_resultat_2.canvas.ax.set_xticks(np.array(np.arange(0, len(index_result), 1)))
        self.graph_resultat_2.canvas.ax.set_xticklabels(index_result)
        self.graph_resultat_2.canvas.draw()
    
    @pyqtSlot(str)
    def on_lineEdit_designation_litt_textChanged(self, designat_lit):
        """permet de faire une recherche dans la base directement avec la saisie de l'utilisateur"""

        enceintes = self.db.recherche_enceintes_par_saisie_designat_litt(designat_lit)
        self.lineEdit_designation_litt.completer_list([x.DESIGNATION_LITTERALE for x in next(enceintes)])
    
    @pyqtSlot(str)
    def on_lineEdit_enceinte_textChanged(self, enceinte):
        """permet de faire une recherche dans la base directement avec la saisie de l'utilisateur"""

        enceintes = self.db.recherche_enceintes_par_saisie(enceinte)
        self.lineEdit_enceinte.completer_list([x.IDENTIFICATION for x in next(enceintes)])


    
    @pyqtSlot()
    def on_lineEdit_enceinte_returnPressed(self):
        """
        Slot documentation goes here.
        """
        try:
            self.lineEdit_enceinte.setStyleSheet(
                """QLineEdit { background-color: white }""")
                
            enceinte = self.lineEdit_enceinte.text()
            
#            recupe_donnees_enceinte = self.db.recup_enceinte_par_ident()
            
            designation_litt = next(self.db.recup_designation_litt_par_ident(enceinte))
            self.lineEdit_designation_litt.setText(designation_litt)
            
            constructeur = next(self.db.recup_constructeur_par_ident(enceinte))
            self.lineEdit_constructeur.setText(constructeur)
            
            model = next(self.db.recup_ref_constructeur_par_ident(enceinte))
            self.lineEdit_model.setText(model)
            
            n_serie = next(self.db.recup_n_serie_par_ident(enceinte))
            self.lineEdit_n_serie.setText(n_serie)
            
            code_client = next(self.db.recup_code_par_ident(enceinte))
            self.lineEdit_code.setText(code_client)
            
            site = next(self.db.recup_site_par_ident(enceinte))
            self.lineEdit_site.setText(site)
            
            localisation = next(self.db.recup_localisation_par_ident(enceinte))
            self.lineEdit_localisation.setText(localisation)
            
            affectation = next(self.db.recup_affect_par_ident(enceinte))
            self.lineEdit_affectation.setText(affectation)
            
            
            sous_affectation = next(self.db.recup_sous_affect_par_ident(enceinte))
            self.lineEdit_sous_affect.setText(sous_affectation)
        
        except (IndexError, StopIteration):
            QMessageBox.critical(self, 
                    self.trUtf8("Selection"), 
                    self.trUtf8("L'enceinte selectionnée est inconnue \n Merci de modifier votre selection"))
            
            self.lineEdit_enceinte.setStyleSheet(
                """QLineEdit { background-color: red }""")
    @pyqtSlot()
    def on_lineEdit_designation_litt_returnPressed(self):
        """
        Slot documentation goes here.
        """
        try:
#            print(f" test {self.lineEdit_enceinte.text()}")
            self.lineEdit_designation_litt.setStyleSheet(
                """QLineEdit { background-color: white }""")
            designation_litt = self.lineEdit_designation_litt.text()
            
            enceinte = next(self.db.recherche_ident_enceinte_par_saisie_designat_litt(designation_litt))
            self.lineEdit_enceinte.setText(enceinte)
            
            self.on_lineEdit_enceinte_returnPressed()
            

        
        except (IndexError, StopIteration):
            QMessageBox.critical(self, 
                    self.trUtf8("Selection"), 
                    self.trUtf8("L'enceinte selectionnée est inconnue \n Merci de modifier votre selection"))
        
            self.lineEdit_designation_litt.setStyleSheet(
                """QLineEdit { background-color: red }""")
    
    @pyqtSlot(str)
    def on_comboBox_application_currentTextChanged(self, p0):
    
        application = p0
#        print("coucuoc")
        
        if application != "Conservation CGR":

            
            self.tab_simu.setEnabled(False)
            self.nettoyage_onglet_simu()
    
    
    @pyqtSlot(str)
    def on_comboBox_application_currentIndexChanged(self, p0):
        """
        Slot documentation goes here.
        """
        application = p0
        
        if application == "Conservation CGR":
#            self.comboBox_condition_desiree.addItem("4")
            self.comboBox_emt.setCurrentIndex(2)
            self.comboBox_signe_emt.setCurrentIndex(0)
            self.lineEdit_condition_des.setText("4")
            self.tab_simu.setEnabled(True)
            
        elif application == "Conservation Plaquettes":
#            self.comboBox_condition_desiree.addItem("22")
            self.comboBox_emt.setCurrentIndex(2)
            self.comboBox_signe_emt.setCurrentIndex(0)
            self.lineEdit_condition_des.setText("22")
            
            self.tab_simu.setEnabled(False)
            self.nettoyage_onglet_simu()
        
        elif application == "Conservation Plasmas":
#            self.comboBox_condition_desiree.addItem("-30")
            self.comboBox_emt.setCurrentIndex(2)
            self.comboBox_signe_emt.setCurrentIndex(0)
            self.lineEdit_condition_des.setText("-25")
            
            self.tab_simu.setEnabled(False)
            self.nettoyage_onglet_simu()
            
        elif application == "Conservation Réactifs":
#            self.comboBox_condition_desiree.addItem("-30")
            self.comboBox_emt.setCurrentIndex(3)
            self.comboBox_signe_emt.setCurrentIndex(0)
            self.lineEdit_condition_des.setText("5")
            
            self.tab_simu.setEnabled(False)
            self.nettoyage_onglet_simu()

        else:
            self.tab_simu.setEnabled(False)
            self.nettoyage_onglet_simu()

            
        if self.tupple_index:
            self.resultats(self.tupple_index)
    
    @pyqtSlot(str)
    def on_comboBox_emt_currentIndexChanged(self, p0):
        try:
            float(self.comboBox_emt.currentText())
            if self.tupple_index:
                self.resultats(self.tupple_index)
        except ValueError:
            QMessageBox.critical(self, 
                    self.trUtf8("EMT"), 
                    self.trUtf8("La valeur d'EMT saisie n'est pas conforme"))
    @pyqtSlot(str)
    def on_comboBox_signe_emt_currentIndexChanged(self, p0):
        
        if self.tupple_index:
            self.resultats(self.tupple_index)
    
    @pyqtSlot(str)
    def on_lineEdit_condition_des_textChanged(self, p0):
        if self.lineEdit_condition_des.text()!="-":
            try:
                float(self.lineEdit_condition_des.text())
                self.lineEdit_condition_des.setStyleSheet(
                """QLineEdit { background-color: white }""")
                
                if self.tupple_index:
                    self.resultats(self.tupple_index)
                    
            except ValueError:
                QMessageBox.critical(self, 
                        self.trUtf8("Condition Désirée"), 
                        self.trUtf8("La valeur de la condition désirée saisie n'est pas conforme"))
                self.lineEdit_condition_des.setStyleSheet(
                """QLineEdit { background-color: red }""")
                
    @pyqtSlot(str)
    def on_lineEdit_consigne_textChanged(self, p0):
        
        if self.lineEdit_consigne.text() !="-":
            try:
                float(self.lineEdit_consigne.text())
    #            if self.tupple_index:
    #                self.resultats(self.tupple_index)
                self.lineEdit_consigne.setStyleSheet(
                """QLineEdit { background-color: white }""")
                    
            except ValueError:
                QMessageBox.critical(self, 
                        self.trUtf8("Température de Consigne"), 
                        self.trUtf8("La valeur de la température de consigne saisie n'est pas conforme"))
                        
                self.lineEdit_consigne.setStyleSheet(
                """QLineEdit { background-color: red }""")
                    
    def nettoyage_onglet_simu(self):
        """ fonction qui efface l'onglet simulation"""
        
        self.annexe_simulation = False
#        try:
        self.tableView_donnees_fichier_2.remplir(pd.DataFrame())
        #Affichage de result
        
        self.tableView_resultats_simu.remplir(pd.DataFrame())
        
#        except:
#            pass
#        try:
        self.graph_zoom_2.canvas.ax.clear()
        self.graph_zoom_2.canvas.draw()  
#        self.graph_resultat_2.clf()
        self.graph_resultat_2.canvas.ax.clear()
        self.graph_resultat_2.canvas.draw()
        self.textEdit_conclusion_generale_2.clear()
#        except:
#            print("erreur")
#            pass
        
    @pyqtSlot()
    def on_actionSauvegarder_triggered(self):
        """
        Slot documentation goes here.
        """
        if self.tupple_index:
            sauvegarde = self.donnees_rapport()
#            print(sauvegarde)
    #############test a faire voir sil ne manque paq des donnees
            carto_bdd = Carto_BDD(self.engine)
            sauvegarde["administratif"]["num_rapport"] = carto_bdd.insertion_nvlle_carto(sauvegarde)
            
            
            if not(issubclass(type(sauvegarde["administratif"]["num_rapport"]), BaseException)): # permet de tester si le retunr fct n'est pas une erreur
                QMessageBox.information(
                    self,
                    self.trUtf8("Numero Cartographie"),
                    self.trUtf8(f"""Le numero de la cartographie est {sauvegarde["administratif"]["num_rapport"]}"""))
    
                
                res = QMessageBox.question(
                    self,
                    self.trUtf8("Rapport"),
                    self.trUtf8("""Voulez vous exporter un rapport de cartographie"""),
                    QMessageBox.StandardButtons(
                        QMessageBox.No |
                        QMessageBox.Yes))
                if  res == QMessageBox.Yes:
                    try:
    #                    sauvegarde = self.donnees_rapport()
                        
    #                    file = QFileDialog.getSaveFileName(None ,  "Selectionner le dossier de sauvegarde de l'annexe", "y:/1.METROLOGIE/0.ARCHIVES ETALONNAGE-VERIFICATIONS/3-CARTOS-SIMULATION", '*.pdf' )
                        file = str(QFileDialog.getExistingDirectory(self, "Choisir le repertoire de sauvegarde",
                                                "y:/1.METROLOGIE/0.ARCHIVES ETALONNAGE-VERIFICATIONS/3-CARTOS-SIMULATION/",
                                                QFileDialog.ShowDirsOnly))
                        if file !="":            
        
                            nom = file +"/"+ sauvegarde["administratif"]["num_rapport"]
                        try:
                            rapport = Rapport(nom)
                            rapport.rapport_carto(sauvegarde)
                            self.close()
                        except Exception as e:                        
                            QMessageBox.critical(self,
                            self.tr("Rapport"), 
                                self.tr(f"Le rapport n'a pu etre sauvé : {e}"))
                            pass
                    except AttributeError:
                        pass

                self.nettoyage_gui()
            else:
                QMessageBox.critical(
                    self,
                    self.trUtf8("Enregistrement Cartographie"),
                    self.trUtf8(f"""La cartographie n'a pu etre sauvée dans la base {sauvegarde["administratif"]["num_rapport"]}"""))
        
    def nettoyage_gui(self):
        """fct qui efface toutes les onglets et se met sur l'onglet 1"""
        self.close()
        self.fermeture_reouverture.emit()

#        
        
class Affichage_graphThread(QThread):

    def __init__(self, dataframe, widget_graph):
        QThread.__init__(self)
        
        
        self.dataframe = dataframe
        self.graph_total = widget_graph

    def __del__(self):
        self.wait()
        
        
        
    def run(self):        
        
        
        self.graph_total.canvas.ax.clear()

        for clef in self.dataframe.keys():
          if clef !="Date": 
            self.graph_total.canvas.ax.plot(self.dataframe["Date"], self.dataframe[clef],'-',  label =clef, linewidth=1)
            self.graph_total.canvas.ax.legend(frameon=False, fontsize=10)

#        self.cursor = Cursor(self.graph_total.canvas.ax, useblit=True, color='red', linewidth=2)
            
        xfmt= matplotlib.dates.DateFormatter('%y-%m-%d %H:%M:%S')
        self.graph_total.canvas.ax.xaxis.set_major_formatter(xfmt)

        labels = self.graph_total.canvas.ax.get_xticklabels()
        for label in labels:
            label.set_rotation(6)

        self.graph_total.canvas.draw()
        
#            Cursor(self.graph_total.canvas.ax, useblit=True, color='red', linewidth=2)
        
        
#        self.connect(self.graph_total.canvas, SIGNAL("zoom(PyQt_PyObject)"), self.plage_select_souris)
        
        
        
        
class Calcul_Carto_Thread(QThread):
    
    signalResultats_ok = pyqtSignal(pd.DataFrame)
    signalIndexResultat = pyqtSignal(list)
        
    def __init__(self, dataframe, tableWidget_sondes_centrale):
        QThread.__init__(self)
        
        
        self.copy_data = dataframe
        self.tableWidget_sondes_centrale = tableWidget_sondes_centrale

    def __del__(self):
        self.wait()
        
        
        
    def run(self):
        
        index = [key for key in self.copy_data.keys() if key != "Date"]

        index_bis = ("HAD", "HAG", "HPD", "HPG", "CENTRE", "BAD", "BAG", "BPD"
                            ,"BPG", "CA","CB", "CD", "CG", "CH", "CP")
        
        index_result = [ sonde for sonde in index_bis if sonde in index]

        result = pd.DataFrame(index = index_result , columns = ["Voie","Moyenne", "Ecart Type", "Minimum", "Maximum"
                                                                                    , "Delta", "Resolution", "Derive", "Etalonnage",
                                                                                    "u_cj", "u_mj", "U_mj", 
                                                                                    "θ + Umj", "θ - Umj"])
        
        for nom in self.copy_data.keys():
            self.copy_data[nom].replace(["Err.02", "Err.06", "Err.13", "Err.72"], np.nan)
            
#            if nom == "BAG":
#                print(self.copy_data[nom])
#                for el in self.copy_data[nom]:
#                    print(el)
#            try:
            if nom != "Date":


                ####Calcul
                moyenne = np.nanmean(self.copy_data[nom].astype(float).as_matrix(columns=None))
                moyenne_round = np.around(moyenne, decimals = 2)

                ecartype = np.nanstd(self.copy_data[nom].astype(float).as_matrix(columns=None), ddof = 1)
                ecartype_round = np.around(ecartype, decimals = 2)
                
                min = np.nanmin(self.copy_data[nom].astype(float).as_matrix(columns=None))
                min_round = np.around(min, decimals = 2)
                
                max = np.nanmax(self.copy_data[nom].astype(float).as_matrix(columns=None))
                max_round = np.around(max, decimals = 2)
                
                delta = np.abs(max-min)
                delta_round = np.around(delta, decimals = 2)
                
                
                
                #etalonnage
                for ligne in range(self.tableWidget_sondes_centrale.rowCount()):
                    if self.tableWidget_sondes_centrale.cellWidget (ligne,1).currentText() == nom:
                        U_etal = float(self.tableWidget_sondes_centrale.item(ligne, 6).text())                        
                        U_etal_round = float(decimal.Decimal(str(U_etal)).quantize(decimal.Decimal(str(0.01)),rounding = decimal.ROUND_UP))
                        u_etal = U_etal/2
                        
                        resolution = float(self.tableWidget_sondes_centrale.item(ligne, 9).text())
                        u_resolution =  resolution/(2*np.sqrt(3))
                        
                        derive = float(self.tableWidget_sondes_centrale.item(ligne, 10).text())
                        u_derive = derive/(np.sqrt(3))
                        
                u_cj = np.sqrt(np.power(u_etal, 2) + np.power(u_resolution, 2) + np.power(u_derive, 2))
                u_mj = np.sqrt(np.power(u_cj, 2) + np.power(ecartype, 2))
                
                U_mj = 2 * u_mj                
                U_mj_round = decimal.Decimal(str(U_mj)).quantize(decimal.Decimal(str(resolution)),rounding = decimal.ROUND_UP)
                
                moyenne_plus_U_mj = moyenne_round + float(U_mj_round)
#                print(moyenne_plus_U_mj)
#                moyenne_plus_U_mj_round =  np.around(moyenne_plus_U_mj ,  decimals = 2)
                
                moyenne_moins_U_mj = moyenne_round - float(U_mj_round)
#                moyenne_moins_U_mj_round =  np.around(moyenne_moins_U_mj ,  decimals = 2)
                
                result.loc[nom] = (nom, moyenne_round, ecartype_round, min_round, max_round, 
                                        delta_round, resolution, derive, U_etal_round, u_cj, u_mj, U_mj_round,  
                                        moyenne_plus_U_mj, moyenne_moins_U_mj)
                
                max = np.nanmax(self.copy_data[nom].astype(float).as_matrix(columns=None))
                

                
                max_round = np.around(max, decimals = 2)
                
                delta = np.abs(max-min)
                delta_round = np.around(delta, decimals = 2)

        self.signalResultats_ok.emit(result) 
        self.signalIndexResultat.emit([result, index_result])




















































