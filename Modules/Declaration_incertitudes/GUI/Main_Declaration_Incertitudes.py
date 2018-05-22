# -*- coding: utf-8 -*-

"""
Module implementing MainDeclaration_Incertitudes.
"""

from PyQt4.QtCore import pyqtSlot, QDate, QModelIndex, SIGNAL
from PyQt4.QtGui import QMainWindow, QTableWidgetItem, QCheckBox, QMessageBox, QFileDialog

from .Ui_Main_Declaration_Incertitudes import Ui_MainDeclaration_Incertitudes
from Modules.Declaration_incertitudes.Package.AccesBdd import AccesBdd
from Modules.Declaration_incertitudes.GUI.Select_Etalons import Select_Etalon 
from Modules.Declaration_incertitudes.GUI.Select_CE import Select_CE
from Modules.Declaration_incertitudes.GUI.Select_Generateur import Select_Generateurs 
from Modules.Declaration_incertitudes.GUI.Select_Caracterisation import Select_Caracterisation
from Modules.Declaration_incertitudes.Report.Rapport import Rapport
import numpy as np
from  decimal import *
from itertools import  product
import json
#import pickle

#from PyQt4.QtCore import SIGNAL

class MainDeclaration_Incertitudes(QMainWindow, Ui_MainDeclaration_Incertitudes):
    """
    Class documentation goes here.
    """
    def __init__(self, engine, meta, parent=None):
        """
        Constructor
        
        @param parent reference to the parent widget (QWidget)
        """
        super(MainDeclaration_Incertitudes, self).__init__(parent)
        self.setupUi(self)
        
        self.dateEdit.setDate(QDate.currentDate())
        
        self.db = AccesBdd(engine, meta)

        self.remplissage_tableau_recap()
        self.ini_tableau_incertitude()
        #cte
        self.list_poly_select = []
        self.list_carac_select = []
        
        self.actionMise_jour.setEnabled(False)
        self.actionEnregistrement.setEnabled(False)
    
    def closeEvent(self, event):
        """ Fermeture de la bdd"""
        
        self.db.__del__()
       
    
    def remplissage_tableau_recap(self):
        """Rempli le tableau recap avec les donnees de la table incertitudes_moyens_mesure """
        
        self.u_declarees = self.db.recup_table_incertitudes_moyens_mesure()
        
        for ligne in reversed(range(self.tableWidget.rowCount())):
            self.tableWidget.removeRow(ligne)
        
        for decla in reversed(self.u_declarees) : 
            self.tableWidget.insertRow(0)
            #id
            item_0 = QTableWidgetItem(str(decla[0]))
            self.tableWidget.setItem(0, 0, item_0)
            #Date
            item_1 = QTableWidgetItem(str(decla[1]))
            self.tableWidget.setItem(0, 1, item_1)
            #Type declaration
            item_2 = QTableWidgetItem(str(decla[2]))
            self.tableWidget.setItem(0, 2, item_2)
            
            
            #○Archivage
            check_box = QCheckBox (self.tableWidget)
            self.tableWidget.setCellWidget(0, 3, check_box)
            if decla[3] == True:
                check_box.setChecked(True)
#                check_box.setEnabled(True)
                
            else:
                check_box.setChecked(False)
                
            check_box.setEnabled(False)
            #↨commentaire
            item_4 = QTableWidgetItem(str(decla[23]))
            self.tableWidget.setItem(0, 4, item_4)
            #♦ufinal
            item_5 = QTableWidgetItem(str(decla[22]))
            self.tableWidget.setItem(0, 5, item_5)
#            print(len(decla))
            
#                print(a)
#                print(a["Fuite_Thermique_Etalon"])
                
    def ini_tableau_incertitude(self):
        """rempli le tableau incertitudes avec des valeurs de bases"""
        value_tableau_incertitudes = [0, 0, 0.001, 0, 0, 0, 0.006, 0, 0, 0, 0, 0.001, 0.004]

        for ligne  in range(len(value_tableau_incertitudes)):
            item = QTableWidgetItem(value_tableau_incertitudes[ligne].__format__(".12f"))
            self.tableWidget_incertitudes.setItem(ligne, 0, item)
    
    
    @pyqtSlot(QModelIndex)
    def on_tableWidget_doubleClicked(self, index):
        """
        recupere les donnees de la liste selectioonnee et affiche les donnees et le graphique dans les onglet 2 et 3
        
        """
        self.tabWidget.setCurrentIndex(1)
        self.actionMise_jour.setEnabled(True)
        self.actionEnregistrement.setEnabled(False)
        self.actionArchivage.setEnabled(False)
        
        #recuperation des donnees
        ligne_select = self.tableWidget.currentRow()
        donnees_ligne = self.u_declarees[ligne_select]
#        print(donnees_ligne)

        #remplissage onglet saisies :
        
        date = donnees_ligne[1]
        self.dateEdit.setDate(date)
        
        id_decla = donnees_ligne[0]
        self.lineEdit_id_decla.setText(str(id_decla))
        
        commentaire = donnees_ligne[23]
        self.textEdit_commentaire.setPlainText(commentaire)
        
        type_declaration = donnees_ligne[2]
        index = self.comboBox_type_declaration.findText(type_declaration)
        if index  != -1:
            self.comboBox_type_declaration.setCurrentIndex(index)
            
        
#        for i in range(4)
        #etalonnage etalon
        if donnees_ligne[4]:
            item_etal_etalon = QTableWidgetItem(str(donnees_ligne[4]))
            self.tableWidget_incertitudes.setItem(0, 0, item_etal_etalon)
            item_u_etal_etalon = QTableWidgetItem(str(donnees_ligne[13]))
            self.tableWidget_incertitudes.setItem(0, 2, QTableWidgetItem(item_u_etal_etalon))
        else:
            item_etal_etalon = QTableWidgetItem(str(0))
            self.tableWidget_incertitudes.setItem(0, 0, item_etal_etalon)            
            self.tableWidget_incertitudes.setItem(0, 2, QTableWidgetItem(str(0)))
            
            
        #modelisation poly etalon
        if donnees_ligne[5]:
            item_modelisation = QTableWidgetItem(str(donnees_ligne[5]))
            self.tableWidget_incertitudes.setItem(1, 0,  item_modelisation)    

        else:
            item_modelisation = QTableWidgetItem(str(0))
            self.tableWidget_incertitudes.setItem(1, 0,  item_modelisation)    

        #resolution_etalon
        if donnees_ligne[6]:
            item_resolution = QTableWidgetItem(str(donnees_ligne[6]))
            self.tableWidget_incertitudes.setItem(2, 0,  item_resolution)    
            
        else:
            item_resolution = QTableWidgetItem(str(0.001))
            self.tableWidget_incertitudes.setItem(2, 0,  item_resolution)
        
        #derive etalon
        if donnees_ligne[7]:
            item_resolution = QTableWidgetItem(str(donnees_ligne[7]))
            self.tableWidget_incertitudes.setItem(3, 0,  item_resolution)    
            
        else:
            item_resolution = QTableWidgetItem(str(0.026))
            self.tableWidget_incertitudes.setItem(3, 0,  item_resolution)
        
        #fuite therique etalon
        if donnees_ligne[8]:
            item_fuite_thermique= QTableWidgetItem(str(donnees_ligne[8]))
            item_u_fuite_thermique = QTableWidgetItem(str(donnees_ligne[17]))
            self.tableWidget_incertitudes.setItem(4, 0,  item_fuite_thermique)    
            self.tableWidget_incertitudes.setItem(4, 2, item_u_fuite_thermique)
        else:
            item_fuite_thermique= QTableWidgetItem(str(0))
            item_u_fuite_thermique = QTableWidgetItem(str(0))
            self.tableWidget_incertitudes.setItem(4, 0,  item_fuite_thermique)    
            self.tableWidget_incertitudes.setItem(4, 2, item_u_fuite_thermique)
            
         #autoechauffement etalon
        if donnees_ligne[9]:
            item_autoechauffement= QTableWidgetItem(str(donnees_ligne[9]))
            item_u_autoechauffement = QTableWidgetItem(str(donnees_ligne[18]))
            self.tableWidget_incertitudes.setItem(5, 0,  item_autoechauffement)    
            self.tableWidget_incertitudes.setItem(5, 2, item_u_autoechauffement)
        else:
            item_autoechauffement= QTableWidgetItem(str(0))
            item_u_autoechauffement = QTableWidgetItem(str(0))
            self.tableWidget_incertitudes.setItem(5, 0,  item_autoechauffement)    
            self.tableWidget_incertitudes.setItem(5, 2, item_u_autoechauffement)

        #gestion tableau etalon et tableau generateur
        if donnees_ligne[24]:
            
            for ele in donnees_ligne[24]:

                poly = self.db.return_polys_by_id(ele)
                
                self.tableWidget_recap_select_etalons.insertRow(0)
                item_date= QTableWidgetItem(str(poly[0]))
                self.tableWidget_recap_select_etalons.setItem(0, 0, item_date)
                item_n_ce= QTableWidgetItem(str(poly[1]))
                self.tableWidget_recap_select_etalons.setItem(0, 1, item_n_ce)
                item_etalon= QTableWidgetItem(str(poly[2]))
                self.tableWidget_recap_select_etalons.setItem(0, 2, item_etalon)
                
                self.list_poly_select.append(ele)
        
        else: # veuille saisie
            if donnees_ligne[5] == donnees_ligne[14]:
                item_loi_disti_modeli = QTableWidgetItem(str("/"))
                self.tableWidget_incertitudes.setItem(1, 1, item_loi_disti_modeli)
                #u modelisation                
                item_u_modelisation = QTableWidgetItem(str(donnees_ligne[14]))
                self.tableWidget_incertitudes.setItem(1, 2, item_u_modelisation)
                
                
        if donnees_ligne[25]:
            
            for ele in donnees_ligne[25]:
#                print(ele)
                carac = self.db.return_carac_by_id(ele)
                designation = self.db.return_designation_by_id(carac[3])
                if designation == "Enceinte climatique":

                    item_loi_disti_stab = QTableWidgetItem(str("s/√10"))
                    self.tableWidget_incertitudes.setItem(7, 1, item_loi_disti_stab)
                    
                elif designation == "Bain d'etalonnage":
                    item_loi_disti_stab = QTableWidgetItem(str("2*√3"))
                    self.tableWidget_incertitudes.setItem(7, 1, item_loi_disti_stab)
                
                elif designation =="Bain de Glace Fondante":
                    item_loi_disti_stab = QTableWidgetItem(str("2"))
                    self.tableWidget_incertitudes.setItem(7, 1, item_loi_disti_stab)
                    item_loi_disti_hom = QTableWidgetItem(str("/"))
                    self.tableWidget_incertitudes.setItem(8, 1, item_loi_disti_hom)
                    
                
#                print("carac {}".format(carac))
                
                self.tableWidget_recap_caracterisation.insertRow(0)
                item_date= QTableWidgetItem(str(carac[0]))
                self.tableWidget_recap_caracterisation.setItem(0, 0, item_date)
                item_id= QTableWidgetItem(str(carac[1]))
                self.tableWidget_recap_caracterisation.setItem(0, 1, item_id)
                item_nom= QTableWidgetItem(str(carac[2]))
                self.tableWidget_recap_caracterisation.setItem(0, 2, item_nom)
                
                self.list_carac_select.append(ele)

        else: #cas d'un rapatriement de veilles valeurs
            item_loi_disti_stab = QTableWidgetItem(str("/"))
            self.tableWidget_incertitudes.setItem(7, 1, item_loi_disti_stab)
            item_loi_disti_hom = QTableWidgetItem(str("/"))
            self.tableWidget_incertitudes.setItem(8, 1, item_loi_disti_hom)
        
        
        #stab generateur
        if donnees_ligne[11]:
            item_stab_generateur = QTableWidgetItem(str(donnees_ligne[11]))
            item_u_stab_generateur = QTableWidgetItem(str(donnees_ligne[20]))
            self.tableWidget_incertitudes.setItem(7, 0,  item_stab_generateur)    
            self.tableWidget_incertitudes.setItem(7, 2, item_u_stab_generateur)
        else:
            item_stab_generateur= QTableWidgetItem(str(0))
            item_u_stab_generateur = QTableWidgetItem(str(0))
            self.tableWidget_incertitudes.setItem(7, 0,  item_stab_generateur)    
            self.tableWidget_incertitudes.setItem(7, 2, item_u_stab_generateur)
            
         #hom generateur
        if donnees_ligne[12]:
            item_hom_generateur = QTableWidgetItem(str(donnees_ligne[12]))
            item_u_hom_generateur = QTableWidgetItem(str(donnees_ligne[21]))
            self.tableWidget_incertitudes.setItem(8, 0,  item_hom_generateur)    
            self.tableWidget_incertitudes.setItem(8, 2, item_u_hom_generateur)
        else:
            item_hom_generateur= QTableWidgetItem(str(0))
            item_u_hom_generateur = QTableWidgetItem(str(0))
            self.tableWidget_incertitudes.setItem(8, 0,  item_hom_generateur)    
            self.tableWidget_incertitudes.setItem(8, 2, item_u_hom_generateur)   
        #u moyen
        if donnees_ligne[26]:
            item_u_moyen = QTableWidgetItem(str(donnees_ligne[26]))
            item_u_moyen_bis = QTableWidgetItem(str(donnees_ligne[26]))
            self.tableWidget_incertitudes.setItem(9, 0,  item_u_moyen)    
            self.tableWidget_incertitudes.setItem(9, 2, item_u_moyen_bis)
        else:
            item_u_moyen= QTableWidgetItem(str(0))
            item_u_moyen_bis = QTableWidgetItem(str(0))
            self.tableWidget_incertitudes.setItem(9, 0,  item_u_moyen)    
            self.tableWidget_incertitudes.setItem(9, 2, item_u_moyen_bis)
           
         #donnees clientes
        if donnees_ligne[28] :            
            dict_donnees = json.loads(donnees_ligne[28] )

            item_rayonnement= QTableWidgetItem(str(dict_donnees["Rayonnement"]["Valeur"]))
            item_u_rayonnement = QTableWidgetItem(str(dict_donnees["Rayonnement"]["u (k = 1)"]))
            self.tableWidget_incertitudes.setItem(10, 0,  item_rayonnement)    
            self.tableWidget_incertitudes.setItem(10, 2, item_u_rayonnement)
            
            item_resolution_chaine_cliente= QTableWidgetItem(str(dict_donnees["Resolution_Chaine_Cliente"]["Valeur"]))
            item_u_resolution_chaine_cliente = QTableWidgetItem(str(dict_donnees["Resolution_Chaine_Cliente"]["u (k = 1)"]))
            self.tableWidget_incertitudes.setItem(11, 0,  item_resolution_chaine_cliente)    
            self.tableWidget_incertitudes.setItem(11, 2, item_u_resolution_chaine_cliente)
            
            item_Fuite_Thermique_client= QTableWidgetItem(str(dict_donnees["Fuite_Thermique_Chaine_Cliente"]["Valeur"]))
            item_u_Fuite_Thermique_client = QTableWidgetItem(str(dict_donnees["Fuite_Thermique_Chaine_Cliente"]["u (k = 1)"]))
            self.tableWidget_incertitudes.setItem(12, 0,  item_Fuite_Thermique_client)    
            self.tableWidget_incertitudes.setItem(12, 2, item_u_Fuite_Thermique_client)

        
#        item_valeur_modelisation = QTableWidgetItem(str(donnees_ligne[14])) #QTableWidgetItem(str(float(donnees_ligne[4]) * np.sqrt(3)))
        
        
    @pyqtSlot()
    def on_pushButton_select_etalons_clicked(self):
        """
        Slot documentation goes here.
        """

        list_etalons = [x[1] for x in self.db.etalons()]
        
        self.select_etalon = Select_Etalon(list_etalons)
        self.connect(self.select_etalon, SIGNAL("fermetureSelect_Etalon(PyQt_PyObject)"), self.ce_etalons_selection)
        self.select_etalon.show()
#        print(self.select_etalon)
    
    def ce_etalons_selection(self, list_etalons):
        """ recupere l'ensemble des CE des etalons choisis"""
#        print(list_etalons)
        self.poly = self.db.return_polys_etalon(list_etalons)
#        print(poly)
    
    @pyqtSlot()
    def on_pushButton_select_CE_clicked(self):
        """
        recupere les donnees de self.poly les tries pour garde n°CE et date et affiche le tout dans un widget
        """
        try:
            self.list_poly_select = []
            if self.poly:
    #            list_poly =[(x[4], x[3]) for x in self.poly]
                gen_poly = ((x[1], x[4], x[3], x[10]) for x in self.poly)
    #            
    #            print(self.poly)
    #            print(list_poly)
                self.select_ce = Select_CE(gen_poly)
                self.connect(self.select_ce, SIGNAL("fermetureSelect_CE(PyQt_PyObject)"), self.selection_des_ce)
                self.select_ce.show()
        except AttributeError:
            pass
    
    def selection_des_ce(self, list_ce):
        """ fct qui gere l'affichage dans le tableau recap des ce selectionnes"""
        
        #mise en place loi distri pour la modelisation 
        item_loi_disti_modelisation = QTableWidgetItem(str("√3"))
        self.tableWidget_incertitudes.setItem(1, 1, item_loi_disti_modelisation)
        
        nbr_ligne = self.tableWidget_recap_select_etalons.rowCount()
        
        for ligne in reversed(range(nbr_ligne)):
            self.tableWidget_recap_select_etalons.removeRow(ligne)
#        print("liste ds ce {}".format(list_ce))
        for ce in list_ce:          #list_ce.=((etalon, date, n_ce),(etalon, date, n_ce)....)
            self.tableWidget_recap_select_etalons.insertRow(0)
            
            item_date_ce = QTableWidgetItem(str(ce[1]))
            self.tableWidget_recap_select_etalons.setItem(0, 0, item_date_ce)
            
            item_ce = QTableWidgetItem(str(ce[2]))
            self.tableWidget_recap_select_etalons.setItem(0, 1, item_ce)
            
            nom_etalon = ce[0]

            item_nom_etalon = QTableWidgetItem(str(nom_etalon))
            self.tableWidget_recap_select_etalons.setItem(0, 2, item_nom_etalon)

        #gestion incertitudes d'etalonnage etalon(s)               
        list_nom_ce = [x[2] for x in list_ce]
        list_residu = [float(x[10]) if x[10] else 0 for x in self.poly if x[3] in list_nom_ce]
        max_residu = np.amax(list_residu)
        list_u_modelisation =  [float(x[11]) if x[11] else 0 for x in self.poly if x[3] in list_nom_ce]
        max_u_modelisation =np.amax(list_u_modelisation)
        
        item_max_residu = QTableWidgetItem(max_residu.__format__(".12f"))        
        self.tableWidget_incertitudes.setItem(1, 0, item_max_residu)
        item_max_modelisation = QTableWidgetItem(max_u_modelisation.__format__(".12f"))        
        self.tableWidget_incertitudes.setItem(1, 2, item_max_modelisation)
        
        list_id_poly = [x[0] for x in self.poly if x[3] in list_nom_ce]        
        list_U_etal = self.db.incertitude_etal_list_id_poly(list_id_poly)
        if list_U_etal:
            max_U_etal = np.amax(list_U_etal)
        else:
            max_U_etal = 0
            
        item_max_U_etal = QTableWidgetItem(max_U_etal.__format__(".12f"))        
        self.tableWidget_incertitudes.setItem(0, 0, item_max_U_etal)
        item_u_etal = QTableWidgetItem((max_U_etal/2).__format__(".12f"))        
        self.tableWidget_incertitudes.setItem(0, 2, item_u_etal)
#       
        nom_ce = [x[2] for x in list_ce]

        self.list_poly_select = [x[0] for x in self.poly if x[3] in nom_ce]
#        print("self.lis_poly_select {}".format(self.list_poly_select))
        
    @pyqtSlot(int, int)
    def on_tableWidget_incertitudes_cellChanged(self, row, column):
        """        Gestion des calculs lors de la modification d'une cellule
        """

        nbr_ligne =self.tableWidget_incertitudes.rowCount()

        if column == 2:
            try : 
                u = float(self.tableWidget_incertitudes.item(row, 2).text())
                u_2 = np.power(u , 2)
                item_u_etal_2 = QTableWidgetItem(u_2.__format__(".12f"))        
                self.tableWidget_incertitudes.setItem(row, 3, item_u_etal_2)
                
            except ValueError:
                u = 0
                item_u = QTableWidgetItem(u.__format__(".12f"))        
                self.tableWidget_incertitudes.setItem(row, 2, item_u)
                
                u_2 = np.power(0 , 2)
                item_u_etal_2 = QTableWidgetItem(u_2.__format__(".12f"))        
                self.tableWidget_incertitudes.setItem(row, 3, item_u_etal_2)
            
        elif column == 0:
            loi = self.tableWidget_incertitudes.item(row, 1).text()
            if loi == "2":
                diviseur = 2                   
            
            elif loi == "2*√3":
                diviseur = 2*np.sqrt(3)
                
            elif loi == "√3":
                diviseur = np.sqrt(3)
#                print(diviseur)
                
            elif loi == "/":
                diviseur = 1
            elif loi == "s/√10":
                diviseur = np.sqrt(10)
                
                
            try:
                value = float(self.tableWidget_incertitudes.item(row, 0).text())
#                print(value)
                item_u = QTableWidgetItem((value/diviseur).__format__(".12f"))
                self.tableWidget_incertitudes.setItem(row, 2, item_u)
                
            except ValueError:
                value = 0
#                diviseur = 1
                item_u = QTableWidgetItem((0).__format__(".12f"))
                self.tableWidget_incertitudes.setItem(row, 2, item_u)

        list_u2= []
        for ligne in range(nbr_ligne):
            if self.tableWidget_incertitudes.item(ligne, 3):
                u2 = float(self.tableWidget_incertitudes.item(ligne, 3).text())
                list_u2.append(u2)
#        print(list_u2) 
        somme_u2_avec_client = np.sum(list_u2)
        u_client = np.sqrt(somme_u2_avec_client)
        U_client = 2* u_client
#        print(U_client)
        #arrondi
        if U_client> 0.1 :
            resolution = str(0.1)
        else:
            resolution = str(0.01)
#        arrondi_u_client = Decimal(str(u_client)).quantize(Decimal(resolution),rounding = ROUND_UP)
        arrondi_U_client = Decimal(str(U_client)).quantize(Decimal(resolution),rounding = ROUND_UP)
        
        list_u2_sans_client = []
        for ligne in range(11):
            if self.tableWidget_incertitudes.item(ligne, 3):
                u2 = float(self.tableWidget_incertitudes.item(ligne, 3).text())
                list_u2_sans_client.append(u2)
            
        somme_u2 = np.sum(list_u2_sans_client)
        u = np.sqrt(somme_u2)
        U = 2*u
        
        self.lineEdit_u2.setText(somme_u2.__format__(".12f"))
        self.lineEdit_u.setText(u.__format__(".12f"))        
        self.lineEdit_U.setText(U.__format__(".12f"))
        
        self.lineEdit_u2_client.setText(str(somme_u2_avec_client))
        self.lineEdit_u_client.setText(str(u_client))
        
        if len(str(arrondi_U_client))<4:
            arrondi_U_client = str(arrondi_U_client) + str(0)
            
        self.lineEdit_U_client.setText(str(arrondi_U_client))
    
        self.tableWidget_incertitudes.resizeColumnsToContents()
        
    @pyqtSlot()
    def on_pushButton_select_generateurs_clicked(self):
        """
        Slot documentation goes here.
        """
        list_generateurs = [x[1] for x in self.db.generateurs()]
        list_generateurs.sort()
        self.select_generateur = Select_Generateurs(list_generateurs)
        self.connect(self.select_generateur, SIGNAL("fermetureSelect_Generateurs(PyQt_PyObject)"), self.caracterisation)
        self.select_generateur.show()
        
    def caracterisation(self, list_generateur):
        '''fct qui retroune l'ensemble des qualifs de la list des generateurs selectionnes'''

        self.designation_generateur = [x[6] for x in  self.db.generateurs() if x[1] in list_generateur]
#        print("designation {}".format(self.designation_generateur))
        if "Enceinte climatique" in self.designation_generateur :
            self.comboBox_type_declaration.setCurrentIndex(5)
            item_loi_disti_stab = QTableWidgetItem(str("s/√10"))
            self.tableWidget_incertitudes.setItem(7, 1, item_loi_disti_stab)
            
        elif "Bain de Glace Fondante" in self.designation_generateur:
            self.comboBox_type_declaration.setCurrentIndex(0)
            item_loi_disti_stab = QTableWidgetItem(str("2"))
            self.tableWidget_incertitudes.setItem(7, 1, item_loi_disti_stab)
            
        else:
            item_loi_disti_stab = QTableWidgetItem(str("2*√3"))
            self.tableWidget_incertitudes.setItem(7, 1, item_loi_disti_stab)
        
        
        id_generateur = [x[0]for x in  self.db.generateurs() if x[1] in list_generateur]
        self.carac = self.db.return_caracterisations_list_generateurs(id_generateur)
#        print(self.carac)
    
    @pyqtSlot()
    def on_pushButton_select_caract_clicked(self):
        """
        Slot documentation goes here.
        """
        try:
#        print(self.carac)
#        list_carac =[(x[0], str(x[2])) for x in self.carac]
            list_id_carac = [x[0] for x in self.carac]
            list_incertitude_caracterisation = self.db.incertitude_caracterisation(list_id_carac)
            list_carac = [(x[0], str(x[2]),  y[3], z[1]) for x , y, z  in product(self.carac, list_incertitude_caracterisation, self.db.generateurs()) 
                                if x[0] == y[4] and x[1] == z[0]]
#            print(list_carac)
            
            self.selec_caracterisation = Select_Caracterisation(list_carac)
            self.connect(self.selec_caracterisation, SIGNAL("fermetureSelect_Caracterisation(PyQt_PyObject)"), self.gestion_caracterisation)
            self.selec_caracterisation.show()
        except:
            pass


    def gestion_caracterisation(self, liste_caract):

        id_caract = [x[1] for x in liste_caract]
        self.list_carac_select = id_caract
        valeur_caract = self.db.incertitude_caracterisation(id_caract)
        u_generateur_max = np.amax([float(x[3]) for x in valeur_caract])
#        print("valeur_caract {}".format(valeur_caract))
        
#        ecartype_carac = [float(x[2]) for x in valeur_caract]
        if "Enceinte climatique" in self.designation_generateur :
#           print(valeur_caract)
           stab= [float(x[2]) for x in valeur_caract if float(x[3]) == u_generateur_max][0]
           stab_max = stab
           id_caract_max = [x[4] for x in valeur_caract if float(x[3]) == u_generateur_max][0]
           u_moyens_mesure = self.db.u_moyens_mesure(id_caract_max)
           
        else:
           stab= [float(x[0]) for x in valeur_caract if float(x[3]) == u_generateur_max][0]
           stab_max = np.amax(stab)
           u_moyens_mesure = 0
        item_stab_max = QTableWidgetItem(stab_max.__format__(".12f"))
        self.tableWidget_incertitudes.setItem(7, 0, item_stab_max)
        
        hom = [float(x[1]) for x in valeur_caract  if float(x[3]) == u_generateur_max][0]
        hom_max = hom
        item_hom_max = QTableWidgetItem(hom_max.__format__(".12f"))
        self.tableWidget_incertitudes.setItem(8, 0, item_hom_max)
        
        item_u_moyen= QTableWidgetItem(str(u_moyens_mesure))
        self.tableWidget_incertitudes.setItem(9, 0, item_u_moyen)
        
        nbr_ligne = self.tableWidget_recap_caracterisation.rowCount()
        
        for ligne in reversed(range(nbr_ligne)):
            self.tableWidget_recap_caracterisation.removeRow(ligne)
        
        for carac in liste_caract:          
            self.tableWidget_recap_caracterisation.insertRow(0)
            
            item_date_carac = QTableWidgetItem(str(carac[0]))
            self.tableWidget_recap_caracterisation.setItem(0, 0, item_date_carac)
            
            item_id_caract = QTableWidgetItem(str(carac[1]))
            self.tableWidget_recap_caracterisation.setItem(0, 1, item_id_caract)
            

            id_generateur = [ x[1] for x in self.carac if x[0] == int(carac[1])][0]

            nom_generateur = [ x[1]for x in  self.db.generateurs() if x[0] == id_generateur][0]
            item_nom_generateur = QTableWidgetItem(str(nom_generateur))
            self.tableWidget_recap_caracterisation.setItem(0, 2, item_nom_generateur)
  
        
        self.list_carac_select = [int(x) for x in id_caract]
    
    @pyqtSlot(int)
    def on_tabWidget_currentChanged(self, index):
        """
        Slot documentation goes here.
        """
        
        
        if self.tabWidget.currentIndex() == 0:
#            print("couocou")
            self.actionEnregistrement.setEnabled(False)
            self.actionMise_jour.setEnabled(False)
            self.actionArchivage.setEnabled(True)
            
            #nettoyage onglet saisie:
            self.lineEdit_id_decla.clear()
            self.dateEdit.setDate(QDate.currentDate())
            self.comboBox_type_declaration.setCurrentIndex(0)
            self.textEdit_commentaire.clear()
            
            item_loi_disti_modelisation = QTableWidgetItem(str("√3"))
            self.tableWidget_incertitudes.setItem(1, 1, item_loi_disti_modelisation)
            item_loi_disti_hom = QTableWidgetItem(str("√3"))
            self.tableWidget_incertitudes.setItem(8, 1, item_loi_disti_hom)
            
            item_loi_disti_stab = QTableWidgetItem(str("2*√3"))
            self.tableWidget_incertitudes.setItem(7, 1, item_loi_disti_stab)
            
            self.ini_tableau_incertitude()
            
            for ligne in reversed(range(self.tableWidget_recap_select_etalons.rowCount())):
                self.tableWidget_recap_select_etalons.removeRow(ligne)
                
            for ligne in reversed(range(self.tableWidget_recap_caracterisation.rowCount())):
                self.tableWidget_recap_caracterisation.removeRow(ligne)
        
            self.list_poly_select = []
            self.list_carac_select = []        
        
        if self.tabWidget.currentIndex() == 1 :
#            print(self.lineEdit_id_decla.text())
            if  self.lineEdit_id_decla.text():                
                self.actionArchivage.setEnabled(False) 
            else:
                self.actionArchivage.setEnabled(False)
                self.actionEnregistrement.setEnabled(True)
        
        if self.tabWidget.currentIndex() == 2:
#            self.actionMise_jour.setEnabled(False)
            self.actionArchivage.setEnabled(False)
            self.PlotFunc()
        
        self.tableWidget_incertitudes.resizeColumnsToContents()
        
    def PlotFunc(self):
        
        labels = []
        sizes = []
        for ligne in range(10):

            if self.lineEdit_u:     
                somme = float(self.lineEdit_u.text())
                
                if self.tableWidget_incertitudes.item(ligne, 2):
                    
                    if float(self.tableWidget_incertitudes.item(ligne, 2).text()) !=0:
                        u = float(self.tableWidget_incertitudes.item(ligne, 2).text())
                        pourcentage = u * 100 /somme
                        sizes.append(pourcentage)
                        
                        labels.append( self.tableWidget_incertitudes.verticalHeaderItem(ligne).text())
                    else:
                        pass
                else:
                    pass
                
            else:
                pass

        self.graphique.canvas.ax.clear()
        self.graphique.canvas.nom_graphique("Répartition des sources d'incertitudes")
        
        self.graphique.canvas.ax.pie(sizes, labels=labels, 
                                                autopct='%1.1f%%', shadow=True, startangle=90)
                                                
        self.graphique.canvas.ax.axis('equal')
        self.graphique.canvas.draw()
        

    
    @pyqtSlot()
    def on_actionEditer_une_rapport_triggered(self):
        """
        Slot documentation goes here.
        """
        try:
            if self.comboBox_type_declaration.currentText() == "*":
                raise ValueError("type d'incertitude non valide")
            
            
            file = QFileDialog.getSaveFileName(None ,  "Selectionner le dossier de sauvegarde du Rapports", '''y:/1.METROLOGIE/DECLARATION D'INCERTITUDES/''', '*.pdf' )
    #        print("file {}".format(file))
            if file !="":
                list_tableau = []
                for ligne in range(self.tableWidget_incertitudes.rowCount()):
                    
                    list_ligne= []
                    parametre_incertitude =  self.tableWidget_incertitudes.verticalHeaderItem(ligne).text()             
                    
                    if self.tableWidget_incertitudes.item(ligne, 0)  :
                        valeur = self.tableWidget_incertitudes.item(ligne, 0).text()
                    else:
                        valeur = 0
        #            list_valeur.append(valeur)
                    
                    if self.tableWidget_incertitudes.item(ligne, 1):
                        loi = self.tableWidget_incertitudes.item(ligne, 1).text()
                    else:
                        loi="normale"
                    
                    if self.tableWidget_incertitudes.item(ligne, 2):
                        u = self.tableWidget_incertitudes.item(ligne, 2).text()
                    else:
                        u= "0"
                    if self.tableWidget_incertitudes.item(ligne, 2):
                        u_power = float(self.tableWidget_incertitudes.item(ligne, 3).text())
                    else:
                        u_power=0
                    
                    list_ligne = [parametre_incertitude, valeur, loi, u, u_power] 
                   
                    list_tableau.append(list_ligne) 
                
                resultats_u = {"Somme u²" : self.lineEdit_u2.text(), 
                                                                "u final" : self.lineEdit_u.text(), 
                                                                "U final" : self.lineEdit_U.text(), 
                                                                "Somme u² declaree" : self.lineEdit_u2_client.text(), 
                                                                "u declaree" : self.lineEdit_u_client.text(), 
                                                                "U declaree": self.lineEdit_U_client.text()}
                
                
                #administration
                
                #etalon
                list_etalon = []
                for ligne in range(self.tableWidget_recap_select_etalons.rowCount()):
                    date = self.tableWidget_recap_select_etalons.item(ligne, 0).text()
                    n_ce = self.tableWidget_recap_select_etalons.item(ligne, 1).text()
                    nom = self.tableWidget_recap_select_etalons.item(ligne, 2).text()
                    
                    list_etalon.append([date, n_ce, nom])
                list_etalon.insert(0, ["Date", "N° CE", "Nom"])
                
                list_generateur= []
                for ligne in range(self.tableWidget_recap_caracterisation.rowCount()):
                    date = self.tableWidget_recap_caracterisation.item(ligne, 0).text()
                    id_carac = self.tableWidget_recap_caracterisation.item(ligne, 1).text()
                    nom = self.tableWidget_recap_caracterisation.item(ligne, 2).text()
                    
                    list_generateur.append([date, id_carac, nom])
                list_generateur.insert(0, ["Date", "ID_Caract", "Nom"])
                
                commentaire = self.textEdit_commentaire.toPlainText()
                administration = {"DATE": self.dateEdit.date().toString("yyyy-MM-dd"), 
                                        "TYPE": self.comboBox_type_declaration.currentText(),
                                       "COMMENTAIRE": commentaire, 
                                       "LIST_GENERATEUR": list_generateur, 
                                       "LIST_ETALON": list_etalon}
                
                
                Rapport(administration, list_tableau, resultats_u, file)
                
        except ValueError:
            QMessageBox.critical (self,"Attention"
                    ,  "Merci de selectionner un type de declaration d'incertitudes")
    
    @pyqtSlot()
    def on_actionEnregistrement_triggered(self):
        """
        Slot documentation goes here.
        """
        try:
            if self.comboBox_type_declaration.currentText() == "*":
                raise ValueError("type d'incertitude non valide")
                
            if self.list_poly_select and self.list_carac_select:
                list_valeur = []
                list_u = []
                for ligne in range(self.tableWidget_incertitudes.rowCount()):
        #            print(ligne)
                    if self.tableWidget_incertitudes.item(ligne, 0):
                        valeur = float(self.tableWidget_incertitudes.item(ligne, 0).text())
                    else:
                        valeur = 0
                    list_valeur.append(valeur)      
                    if self.tableWidget_incertitudes.item(ligne, 2):
                        u = float(self.tableWidget_incertitudes.item(ligne, 2).text())
                    else:
                        u=0
                    list_u.append(u)
        #        print("dtae {}".format(str(self.dateEdit.date())))
                commentaire = self.textEdit_commentaire.toPlainText()
                
                donnees_en_array = {}                
                for ligne in range(self.tableWidget_incertitudes.rowCount()):
                    nom_ligne = self.tableWidget_incertitudes.verticalHeaderItem(ligne).text()
                    nom_ligne = self.tableWidget_incertitudes.verticalHeaderItem(ligne).text()
                    nom_colonne_0= self.tableWidget_incertitudes.horizontalHeaderItem (0).text()
                    nom_colonne_1 = self.tableWidget_incertitudes.horizontalHeaderItem (1).text()
                    nom_colonne_2= self.tableWidget_incertitudes.horizontalHeaderItem (2).text()
                
                    donnees_en_array[nom_ligne]= {
                                            nom_colonne_0: self.tableWidget_incertitudes.item(ligne, 0).text(),                                                       
                                            nom_colonne_1: self.tableWidget_incertitudes.item(ligne, 1).text(),
                                            nom_colonne_2: self.tableWidget_incertitudes.item(ligne, 2).text()
                                            }
                                            
#                print(donnees_en_array)
                convert_donnees_en_array = json.dumps(donnees_en_array)                           
#                print(convert_donnees_en_array)
#                print(json.load(json.dumps(donnees_en_array)))
                    
                declaration_incertitudes = {"DATE": self.dateEdit.date().toString("yyyy-MM-dd"), 
                                                        "TYPE": self.comboBox_type_declaration.currentText(), 
                                                        "ARCHIVAGE": False, 
                                                        "ETALONNAGE_ETAL": list_valeur[0], 
                                                        "ERREUR_MODELISATION_ETAL" : list_valeur[1], 
                                                        "RESOLUTION_ETAL": list_valeur[2], 
                                                        "DERIVE_ETAL": list_valeur[3] , 
                                                        "FUITE_THERMIQUE_ETAL": list_valeur[4], 
                                                        "AUTOECHAUFFEMENT": list_valeur[5], 
                                                        "TEMP_AMBIANTE_ETAL": list_valeur[6], 
                                                        "STAB_GENERATEUR": list_valeur[7], 
                                                        "HOM_GENERATEUR": list_valeur[8],
                                                        "u_MOYENS_CARAC" : list_valeur[9], 
                                                        "u_ETALONNAGE_ETAL": list_u[0], 
                                                        "u_ERREUR_MODELISATION_ETAL": list_u[1], 
                                                        "u_RESOLUTION_ETAL": list_u[2], 
                                                        "u_DERIVE_ETAL": list_u[3],
                                                        "u_FUITE_THERMIQUE_ETAL": list_u[4], 
                                                        "u_AUTOECHAUFFEMENT": list_u[5], 
                                                        "u_TEMP_AMBIANTE": list_u[6], 
                                                        "u_STAB_GENERATEUR": list_u[7], 
                                                        "u_HOM_GENERATEUR": list_u[8], 
                                                        "u_FINALE": float(self.lineEdit_u.text()), 
                                                        "COMMENTAIRE": commentaire, 
                                                        "POLY_ETALON": self.list_poly_select, 
                                                        "CARACT_GENERATEUR": self.list_carac_select, 
                                                        "U_DECLARATION": float(self.lineEdit_U_client.text()), 
                                                        "DONNEES_EN_ARRAY" : convert_donnees_en_array }
                                                        
                self.db.insertion_declaration_incertitudes(declaration_incertitudes)
        
                self.tabWidget.setCurrentIndex(0)
                self.remplissage_tableau_recap()
            else:
                QMessageBox.critical (self,"Attention"
                    ,  "Merci de selectionner les etalons et/ou les generateurs")
                    
        except ValueError:
            QMessageBox.critical (self,"Attention"
                    ,  "Merci de selectionner un type de declaration d'incertitudes")
            
    @pyqtSlot()
    def on_actionMise_jour_triggered(self):
        """
        Slot documentation goes here.
        
        """
#        try:
        if self.comboBox_type_declaration.currentText() == "*":
                raise ValueError("type d'incertitude non valide")
        if self.list_poly_select and self.list_carac_select:
            id = int(self.lineEdit_id_decla.text())
            list_valeur = []
            list_u = []
            for ligne in range(self.tableWidget_incertitudes.rowCount()):
    #            print(ligne)
                if self.tableWidget_incertitudes.item(ligne, 0):
                    valeur = float(self.tableWidget_incertitudes.item(ligne, 0).text())
                else:
                    valeur = 0
                list_valeur.append(valeur)      
                if self.tableWidget_incertitudes.item(ligne, 2):
                    u = float(self.tableWidget_incertitudes.item(ligne, 2).text())
                else:
                    u=0
                list_u.append(u)
    #        print("dtae {}".format(str(self.dateEdit.date())))
            commentaire = self.textEdit_commentaire.toPlainText()
            
            donnees_en_array = {}                
            for ligne in range(self.tableWidget_incertitudes.rowCount()):
                nom_ligne = self.tableWidget_incertitudes.verticalHeaderItem(ligne).text()
                nom_colonne_0= self.tableWidget_incertitudes.horizontalHeaderItem (0).text()
                nom_colonne_1 = self.tableWidget_incertitudes.horizontalHeaderItem (1).text()
                nom_colonne_2= self.tableWidget_incertitudes.horizontalHeaderItem (2).text()
                
                donnees_en_array[nom_ligne]= {
                                        nom_colonne_0: self.tableWidget_incertitudes.item(ligne, 0).text(),                                                       
                                        nom_colonne_1: self.tableWidget_incertitudes.item(ligne, 1).text(),
                                        nom_colonne_2: self.tableWidget_incertitudes.item(ligne, 2).text()
                                        }
            
#            print(donnees_en_array)
            convert_donnees_en_array = json.dumps(donnees_en_array)                           
#                print(convert_donnees_en_array)
#                print(json.load(json.dumps(donnees_en_array)))
            declaration_incertitudes = {"DATE": self.dateEdit.date().toString("yyyy-MM-dd"), 
                                                    "TYPE": self.comboBox_type_declaration.currentText(), 
                                                    "ARCHIVAGE": False, 
                                                    "ETALONNAGE_ETAL": list_valeur[0], 
                                                    "ERREUR_MODELISATION_ETAL" : list_valeur[1], 
                                                    "RESOLUTION_ETAL": list_valeur[2], 
                                                    "DERIVE_ETAL": list_valeur[3] , 
                                                    "FUITE_THERMIQUE_ETAL": list_valeur[4], 
                                                    "AUTOECHAUFFEMENT": list_valeur[5], 
                                                    "TEMP_AMBIANTE_ETAL": list_valeur[6], 
                                                    "STAB_GENERATEUR": list_valeur[7], 
                                                    "HOM_GENERATEUR": list_valeur[8],
                                                    "u_MOYENS_CARAC" : list_valeur[9],  
                                                    "u_ETALONNAGE_ETAL": list_u[0], 
                                                    "u_ERREUR_MODELISATION_ETAL": list_u[1], 
                                                    "u_RESOLUTION_ETAL": list_u[2], 
                                                    "u_DERIVE_ETAL": list_u[3],
                                                    "u_FUITE_THERMIQUE_ETAL": list_u[4], 
                                                    "u_AUTOECHAUFFEMENT": list_u[5], 
                                                    "u_TEMP_AMBIANTE": list_u[6], 
                                                    "u_STAB_GENERATEUR": list_u[7], 
                                                    "u_HOM_GENERATEUR": list_u[8], 
                                                    "u_FINALE": float(self.lineEdit_u.text()), 
                                                    "COMMENTAIRE": commentaire, 
                                                    "POLY_ETALON": self.list_poly_select, 
                                                    "CARACT_GENERATEUR": self.list_carac_select, 
                                                    "U_DECLARATION": float(self.lineEdit_U_client.text()), 
                                                    "DONNEES_EN_ARRAY" : convert_donnees_en_array }
                                                    
            self.db.update_declaration_incertitudes(declaration_incertitudes, id)
    
            self.tabWidget.setCurrentIndex(0)
            self.remplissage_tableau_recap()
        else : 
            QMessageBox.critical (self,"Attention"
                ,  "Merci de selectionner les etalons et/ou les generateurs")
                    
#        except ValueError:
#            QMessageBox.critical (self,"Attention"
#                    ,  "Merci de selectionner un type de declaration d'incertitudes")
    
    @pyqtSlot()
    def on_actionArchivage_triggered(self):
        """
        Slot documentation goes here.
        """
        # TODO: not implemented yet
#        raise NotImplementedError
#        print("current Row {}".format(self.tableWidget.currentRow()))
        if self.tableWidget.currentRow() >=0:
            reponse = QMessageBox.question (self,"Demande"
                , "Voulez vous archivez cette declaration?", QMessageBox.Yes, QMessageBox.No )
                
#            print(reponse)
            
            if reponse == QMessageBox.Yes:
                ligne =self.tableWidget.currentRow()
                id = int( self.tableWidget.item(ligne, 0).text())
                self.db.archivage_declaration(id)
                
                self.remplissage_tableau_recap()
                
            
        else:
            QMessageBox.critical (self,"Attention"
                ,  "Merci de selectionnner une ligne de declaration")
