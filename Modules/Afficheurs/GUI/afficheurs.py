# -*- coding: utf-8 -*-

"""
Module implementing Afficheurs.
"""

from PyQt4.QtCore import pyqtSlot
from PyQt4.QtGui import QMainWindow
from PyQt4 import QtGui
from PyQt4 import QtCore
from PyQt4.QtGui import QStandardItemModel, QStandardItem 
from PyQt4.QtGui import QMessageBox
from PyQt4.QtGui import QFileDialog
from PyQt4.QtGui import QInputDialog
from .Ui_afficheurs import Ui_MainWindow
from Modules.Afficheurs.Package.AccesBdd import AccesBdd
from Modules.Afficheurs.Package.RapportAfficheur import RapportAfficheur
import decimal
import numpy as np
from Modules.Afficheurs.GUI.creation_emt import Creation_emt
from Modules.Afficheurs.GUI.creation_afficheur import Creation_afficheur
from Modules.Afficheurs.GUI.select_afficheur import Select_afficheur
from Modules.Afficheurs.GUI.modification_afficheur import Modification_afficheur
from PyQt4.QtCore import SIGNAL

class Afficheurs(QMainWindow, Ui_MainWindow):
    """
    Class documentation goes here.
    """
    def __init__(self, engine, meta, parent=None):
        """
        Constructor
        
        @param parent reference to the parent widget (QWidget)
        """
        super().__init__(parent)
        self.setupUi(self)
        
        
        #gestion date
        self.dateEdit.setDate(QtCore.QDate.currentDate())
        
        
        #gestion onglet :
        self.onglet = [self.tab, self.tab_2, self.tab_3, self.tab_4]
        self.nbr_pt =self.spinBox.value()
        i=0
        for i in range(self.nbr_pt+1): #+1 car s'arrete avant la derniere valeur
            self.onglet[3-i].setEnabled(False)
           
        #bdd
        self.engine = engine
        self.meta = meta
        self.db = AccesBdd(engine, meta)
        
        list_cmr = self.db.recensement_cmr()
        list_cmr.sort()
        
        #insertion combobox
        
        self.comboBox_cmr.installEventFilter(self)
        model = QStandardItemModel()

        for i,word in enumerate(list_cmr):
            item = QStandardItem(word)
            model.setItem(i, 0, item)

        self.comboBox_cmr.setModel(model)
        self.comboBox_cmr.setModelColumn(0)
        
        #configuration largeur colonnes tablewidget
        self.tableWidget.setColumnWidth(0,300)
        self.tableWidget.setColumnWidth(1,300)
        self.tableWidget.setColumnWidth(2,300)
        
        self.tableWidget_2.setColumnWidth(0,300)
        self.tableWidget_2.setColumnWidth(1,300)
        self.tableWidget_2.setColumnWidth(2,300)
        
        self.tableWidget_3.setColumnWidth(0,300)
        self.tableWidget_3.setColumnWidth(1,300)
        self.tableWidget_3.setColumnWidth(2,300)
        
        #Gestion polynome de l'etalon:
        self.ordre_poly_etalon = 0
        self.coeff_a_poly_etalon = 0
        self.coeff_b_poly_etalon = 0
        self.coeff_c_poly_etalon = 0
        
        #gestion bouton
        self.actionMise_jour.setEnabled(False)
        self.actionArchivage.setEnabled(False)
        
        #gestion n°ce si demande de modification / annule et remplace
        self.n_ce_pour_modification = ""
#        self.valeur_numerique_emt = ""
        self.n_ce_annule_remplace = ""
        
        self.type_ouverture = 0 #ouverture pour une saisie normale
        
    @pyqtSlot(str)
    def on_comboBox_famille_afficheur_activated(self, p0):
        """
        lors de la selection d'une famille d'afficheurs on va chercher topute
        cette famille dans la base et on tire par rapport au site du cmr
        """

        nom_cmr = self.comboBox_cmr.currentText().split() #list avec nom et prenom
        
        type_afficheur = str(self.comboBox_famille_afficheur.currentText())
        referentiel = self.db.recensement_referentiel_emt(type_afficheur)
        
        #nettoyage combobox emt
        self.comboBox_EMT.clear()
        self.comboBox_EMT_2.clear()
        self.comboBox_EMT_3.clear()
        self.lineEdit_site.clear()
        self.lineEdit_service.clear()
        self.lineEdit_constructeur.clear()
        self.lineEdit_type.clear()
        self.textEdit_n_serie.clear()
        self.textEdit_renseignement_complementaire.clear()
        self.textEdit_commentaire.clear()
        
        
        
#        #recherche domaine de mesure pour etalons
        if type_afficheur == "Sonde alarme température" or type_afficheur == "Afficheur de température":
            domaine_mesure = "Température"
            designation_etalon = "Chaîne de mesure de température"
#            self.comboBox_EMT.addItems(self.EMT_temperature)
#            self.comboBox_EMT_2.addItems(self.EMT_temperature)
#            self.comboBox_EMT_3.addItems(self.EMT_temperature)
#
        elif type_afficheur == "Afficheur de temps":
            domaine_mesure = "Temps-Fréquence"
            designation_etalon = "Chronomètre/minuterie de travail"
#            self.comboBox_EMT.addItems(self.EMT_temps)
#            self.comboBox_EMT_2.addItems(self.EMT_temps)
#            self.comboBox_EMT_3.addItems(self.EMT_temps)            
#            
        elif type_afficheur == "Afficheur de vitesse":
            domaine_mesure = "Vitesse"
            designation_etalon = "Tachymetre Optique"
        nom_ref = [x[0] for x in referentiel]
        self.comboBox_EMT.addItems(nom_ref)
        self.comboBox_EMT_2.addItems(nom_ref)
        self.comboBox_EMT_3.addItems(nom_ref)
            
        #tri des afficheurs/etalons
        service_site = self.db.recuperation_site_service_cmr(nom_cmr[0], nom_cmr[1])
        
        if service_site[0]not in ["LMS", "SNA", "ANG", "LRY", "LAV", "ST Herblain"]:           
            
            afficheurs_nts = self.db.recensement_afficheurs(type_afficheur, "*", "Nantes")            
            afficheurs_nts_nord = self.db.recensement_afficheurs(type_afficheur, "*", "NTSNO")
            afficheurs = list(set(afficheurs_nts+afficheurs_nts_nord))
        
            etalons_nts = self.db.recensement_etalons(domaine_mesure, "*", "Nantes", designation_etalon)
            etalons_nts_nord = self.db.recensement_etalons(domaine_mesure, "*", "NTSNO", designation_etalon)
            etalons = list(set( etalons_nts + etalons_nts_nord))
        
        else:
            afficheurs = self.db.recensement_afficheurs(type_afficheur, "*", service_site[0])
            etalons = self.db.recensement_etalons(domaine_mesure, "*", service_site[0], designation_etalon)
        
        
        if type_afficheur == "Afficheur de vitesse":
            etalons = self.db.recensement_etalons_vitesse(designation_etalon)
        
        afficheurs.sort()
        etalons.sort()
        
        self.comboBox_identification.clear()
        self.comboBox_ident_etalon.clear()
        
        self.comboBox_identification.installEventFilter(self)
        model = QStandardItemModel()

        for i,word in enumerate(afficheurs):
            item = QStandardItem(word)
            model.setItem(i, 0, item)

        self.comboBox_identification.setModel(model)
        self.comboBox_identification.setModelColumn(0)
        
        self.comboBox_ident_etalon.installEventFilter(self)
        model = QStandardItemModel()

        for i,word in enumerate(etalons):
            item = QStandardItem(word)
            model.setItem(i, 0, item)

        self.comboBox_ident_etalon.setModel(model)
        self.comboBox_ident_etalon.setModelColumn(0)
        
#        self.comboBox_identification.addItems(afficheurs)
#        self.comboBox_ident_etalon.addItems(etalons)        

            
    
    @pyqtSlot(int)
    def on_comboBox_identification_activated(self, index):
        """
        Slot documentation goes here.
        """
        # TODO: not implemented yet
                #Recherche n°serie 
        identification = self.comboBox_identification.currentText()
        
        caract_afficheur = self.db.caract_afficheur(identification)
        n_serie = caract_afficheur[0]
        constructeur = caract_afficheur[1]
        type = caract_afficheur[2]
        renseignement_complementaire = caract_afficheur[3]
        self.lineEdit_site.setText(caract_afficheur[6])
        self.lineEdit_service.setText(caract_afficheur[5])        

        
        self.textEdit_n_serie.clear()
        self.textEdit_n_serie.append(n_serie)
        
        self.lineEdit_constructeur.clear()
        self.lineEdit_constructeur.setText (constructeur)
        
        self.lineEdit_type.clear()
        self.lineEdit_type.setText(type)
        
        self.textEdit_renseignement_complementaire.clear()
        self.textEdit_renseignement_complementaire.append(renseignement_complementaire)
    
    @pyqtSlot(int)
    def on_spinBox_valueChanged(self, p0):
        """
        fct qui autorise l'ecriture des onglet en fct du nbr selectionné
        """        
        self.nbr_pt =self.spinBox.value()
        
        for i in range(self.nbr_pt+1):
             self.onglet[i].setEnabled(True)
        
        for i in range(self.nbr_pt+1, 4): #+1 car s'arrete avant la derniere valeur
           self.onglet[i].setEnabled(False)
    
    @pyqtSlot(int)
    def on_comboBox_ident_etalon_activated(self, index):
        """
        Slot documentation goes here.
        """

        etalon_select = self.comboBox_ident_etalon.currentText()
        donnee_poly = self.db.recuperation_polynomes_etal(etalon_select)

        mise_en_forme_combobox = []
        for ele in donnee_poly:
            donnee = str(ele[0] +" "+ "du" +" "+ ele[1].strftime("%d/%m/%y"))

            mise_en_forme_combobox.append(donnee)

        self.comboBox_ce_etal.clear()
        self.comboBox_ce_etal.addItems(mise_en_forme_combobox)
        
        if len(mise_en_forme_combobox) != 0 :
            self.on_comboBox_ce_etal_activated(0)
            
    @pyqtSlot(int)
    def on_comboBox_ce_etal_activated(self, index):
        """
        fct qui va chercher les donnees du poly selectionne sur le combobox
        """

        ce_select = self.comboBox_ce_etal.currentText()
#        print(ce_select)

        n_ce = ce_select[:len(ce_select)-12]

        donnee_poly = self.db.recuperation_polynome_etal_num_ce(n_ce)
#        print("donnee polynome {}".format(donnee_poly))
        
        self.ordre_poly_etalon = donnee_poly[0][2]
        self.coeff_a_poly_etalon = donnee_poly[0][3]
        self.coeff_b_poly_etalon = donnee_poly[0][4]
        self.coeff_c_poly_etalon = donnee_poly[0][5]



        #preparation des spinbox resolution
        identification = self.comboBox_identification.currentText()
        
        caract_afficheur = self.db.caract_afficheur(identification)
       
        resolution = caract_afficheur[4]
        
        self.doubleSpinBox_resolution.setValue(float(resolution))
        self.doubleSpinBox_resolution_2.setValue(float(resolution))
        self.doubleSpinBox_resolution_3.setValue(float(resolution))
    
    @pyqtSlot(int, int)
    def on_tableWidget_cellChanged(self, row, column):
        """
        fct qui calcul valeur corrigée de l'etalon si on ecrit dans la colonne etal brute
        """       
        #gestion donnees etalon brute
        try:
            colonne = self.tableWidget.currentColumn()
            ligne = self.tableWidget.currentRow()
          
            if colonne == 0:                
                valeur_etal_brute = decimal.Decimal(self.tableWidget.item(ligne, 0).text())
                
                if self.ordre_poly_etalon == 1:                
                    correction = self.coeff_a_poly_etalon*valeur_etal_brute + self.coeff_b_poly_etalon
                                            
                elif self.ordre_poly_etalon == 2:
                    correction = self.coeff_a_poly_etalon*(valeur_etal_brute * valeur_etal_brute)\
                                        + self.coeff_b_poly_etalon * valeur_etal_brute + self.coeff_c_poly_etalon
                
                valeur_etal_corri = valeur_etal_brute + correction 
    
          
                #on reaffect les lignes et colonnes de reference afin d'eviter une boucle infinie
                self.ecriture_tableau(self.tableWidget, ligne, 1, valeur_etal_corri, 'white')
                
                self.calculs(self.tableWidget, self.lineEdit_moyenne_etalon, self.lineEdit_moyenne_etalon_arrondie, 
                        self.lineEdit_moyenne_afficheur, self.lineEdit_moyenne_afficheur_arrondie, 
                        self.lineEdit_correction, self.lineEdit_correction_arrondie, 
                        self.lineEdit_ecartype, self.lineEdit_incertitude, self.lineEdit_incertitude_arrondie, 
                        self.doubleSpinBox_resolution)
                            
                self.conformite(self.comboBox_EMT, self.lineEdit_correction, 
                                self.lineEdit_incertitude, self.lineEdit_conformite, 
                                self.doubleSpinBox_resolution, self.lineEdit_moyenne_etalon, 
                                self.textEdit_commentaire_conformite, self.lineEdit_valeur_emt)
                
            elif colonne == 2:                
                string_valeur_afficheur = self.tableWidget.item(ligne, 2).text()
                self.ecriture_tableau(self.tableWidget, ligne, 2, string_valeur_afficheur, 'white')
                
                decimal.Decimal(self.tableWidget.item(ligne, 2).text()) # permet de detecter erreur de saisie tru except
                
                self.calculs(self.tableWidget, self.lineEdit_moyenne_etalon, self.lineEdit_moyenne_etalon_arrondie, 
                        self.lineEdit_moyenne_afficheur, self.lineEdit_moyenne_afficheur_arrondie, 
                        self.lineEdit_correction, self.lineEdit_correction_arrondie, 
                        self.lineEdit_ecartype, self.lineEdit_incertitude, self.lineEdit_incertitude_arrondie, 
                        self.doubleSpinBox_resolution)
                            
                self.conformite(self.comboBox_EMT, self.lineEdit_correction, self.lineEdit_incertitude, 
                                self.lineEdit_conformite, self.doubleSpinBox_resolution, 
                                self.lineEdit_moyenne_etalon, self.textEdit_commentaire_conformite, self.lineEdit_valeur_emt)            
            
            else:
                pass                        

            
        except decimal.InvalidOperation:            
            if colonne == 0:                
                self.ecriture_tableau(self.tableWidget, ligne, 1, "Erreur de Saisie donnees etalon brute", 'red')            
            elif colonne == 2:
                self.ecriture_tableau(self.tableWidget, ligne, colonne, string_valeur_afficheur, 'red')

            self.calculs(self.tableWidget, self.lineEdit_moyenne_etalon, self.lineEdit_moyenne_etalon_arrondie, 
                    self.lineEdit_moyenne_afficheur, self.lineEdit_moyenne_afficheur_arrondie, 
                    self.lineEdit_correction, self.lineEdit_correction_arrondie, 
                    self.lineEdit_ecartype, self.lineEdit_incertitude, self.lineEdit_incertitude_arrondie, 
                    self.doubleSpinBox_resolution) 
                
    
    
    @pyqtSlot(int, int)
    def on_tableWidget_2_cellChanged(self, row, column):
        """
        Slot documentation goes here.
        """
        # TODO: not implemented yet
                
        #gestion donnees etalon brute
        try:
            colonne = self.tableWidget_2.currentColumn()
            ligne = self.tableWidget_2.currentRow()
          
            if colonne == 0:                
                valeur_etal_brute = decimal.Decimal(self.tableWidget_2.item(ligne, 0).text())
                
                if self.ordre_poly_etalon == 1:                
                    correction = self.coeff_a_poly_etalon*valeur_etal_brute + self.coeff_b_poly_etalon
                    
                        
                elif self.ordre_poly_etalon == 2:
                    correction = self.coeff_a_poly_etalon*(valeur_etal_brute * valeur_etal_brute)\
                                        + self.coeff_b_poly_etalon * valeur_etal_brute + self.coeff_c_poly_etalon
                
                valeur_etal_corri = valeur_etal_brute + correction                
          
                #on reaffect les lignes et colonnes de reference afin d'eviter une boucle infinie
                self.ecriture_tableau(self.tableWidget_2, ligne, 1, valeur_etal_corri, 'white')
                
                self.calculs(self.tableWidget_2, self.lineEdit_moyenne_etalon_2, self.lineEdit_moyenne_etalon_2_arrondie, 
                        self.lineEdit_moyenne_afficheur_2, self.lineEdit_moyenne_afficheur_2_arrondie, 
                        self.lineEdit_correction_2, self.lineEdit_correction_2_arrondie, 
                        self.lineEdit_ecartype_2, self.lineEdit_incertitude_2, self.lineEdit_incertitude_2_arrondie, 
                        self.doubleSpinBox_resolution_2)
                        
                self.conformite(self.comboBox_EMT_2, self.lineEdit_correction_2, 
                                self.lineEdit_incertitude_2, self.lineEdit_conformite_2, 
                                self.doubleSpinBox_resolution_2, self.lineEdit_moyenne_etalon_2, 
                                self.textEdit_commentaire_conformite_2, self.lineEdit_valeur_emt_2)
                        
                
                
            elif colonne == 2:                
                string_valeur_afficheur = self.tableWidget_2.item(ligne, 2).text()
                self.ecriture_tableau(self.tableWidget_2, ligne, 2, string_valeur_afficheur, 'white')
                
                decimal.Decimal(self.tableWidget_2.item(ligne, 2).text()) # permet de detecter erreur de saisie tru except
                
                self.calculs(self.tableWidget_2, self.lineEdit_moyenne_etalon_2, self.lineEdit_moyenne_etalon_2_arrondie, 
                        self.lineEdit_moyenne_afficheur_2, self.lineEdit_moyenne_afficheur_2_arrondie, 
                        self.lineEdit_correction_2, self.lineEdit_correction_2_arrondie, 
                        self.lineEdit_ecartype_2, self.lineEdit_incertitude_2, self.lineEdit_incertitude_2_arrondie, 
                        self.doubleSpinBox_resolution_2)
                     
                self.conformite(self.comboBox_EMT_2, self.lineEdit_correction_2, 
                                self.lineEdit_incertitude_2, self.lineEdit_conformite_2, 
                                self.doubleSpinBox_resolution_2, self.lineEdit_moyenne_etalon_2, 
                                self.textEdit_commentaire_conformite_2, self.lineEdit_valeur_emt_2)
                        
                
            else:
                pass                        

            
        except decimal.InvalidOperation:            
            if colonne == 0:                
                self.ecriture_tableau(self.tableWidget_2, ligne, 1, "Erreur de Saisie donnees etalon brute", 'red')            
            elif colonne == 2:
                self.ecriture_tableau(self.tableWidget_2, ligne, colonne, string_valeur_afficheur, 'red')

            self.calculs(self.tableWidget_2, self.lineEdit_moyenne_etalon_2, self.lineEdit_moyenne_etalon_2_arrondie, 
                        self.lineEdit_moyenne_afficheur_2, self.lineEdit_moyenne_afficheur_2_arrondie, 
                        self.lineEdit_correction_2, self.lineEdit_correction_2_arrondie, 
                        self.lineEdit_ecartype_2, self.lineEdit_incertitude_2, self.lineEdit_incertitude_2_arrondie, 
                        self.doubleSpinBox_resolution_2)   
    
    @pyqtSlot(int, int)
    def on_tableWidget_3_cellChanged(self, row, column):
        """
        Slot documentation goes here.
        """
        # TODO: not implemented yet
            #gestion donnees etalon brute
            
        try:
            colonne = self.tableWidget_3.currentColumn()
            ligne = self.tableWidget_3.currentRow()
          
            if colonne == 0:                
                valeur_etal_brute = decimal.Decimal(self.tableWidget_3.item(ligne, 0).text())
                
                if self.ordre_poly_etalon == 1:                
                    correction = self.coeff_a_poly_etalon*valeur_etal_brute + self.coeff_b_poly_etalon
                    
                        
                elif self.ordre_poly_etalon == 2:
                    correction = self.coeff_a_poly_etalon*(valeur_etal_brute * valeur_etal_brute)\
                                        + self.coeff_b_poly_etalon * valeur_etal_brute + self.coeff_c_poly_etalon
                
                valeur_etal_corri = valeur_etal_brute + correction                
          
                #on reaffect les lignes et colonnes de reference afin d'eviter une boucle infinie
                self.ecriture_tableau(self.tableWidget_3, ligne, 1, valeur_etal_corri, 'white')
                
                self.calculs(self.tableWidget_3, self.lineEdit_moyenne_etalon_3,self.lineEdit_moyenne_etalon_3_arrondie,  
                        self.lineEdit_moyenne_afficheur_3, self.lineEdit_moyenne_afficheur_3_arrondie,  
                        self.lineEdit_correction_3, self.lineEdit_correction_3_arrondie, 
                        self.lineEdit_ecartype_3, self.lineEdit_incertitude_3, 
                        self.lineEdit_incertitude_3_arrondie, self.doubleSpinBox_resolution_3)
                        
                self.conformite(self.comboBox_EMT_3, self.lineEdit_correction_3, 
                                self.lineEdit_incertitude_3, self.lineEdit_conformite_3, 
                                self.doubleSpinBox_resolution_3, self.lineEdit_moyenne_etalon_3, 
                                self.textEdit_commentaire_conformite_3, self.lineEdit_valeur_emt_3)

                
            elif colonne == 2:                
                string_valeur_afficheur = self.tableWidget_3.item(ligne, 2).text()
                self.ecriture_tableau(self.tableWidget_3, ligne, 2, string_valeur_afficheur, 'white')
                
                decimal.Decimal(self.tableWidget_3.item(ligne, 2).text()) # permet de detecter erreur de saisie tru except
                
                self.calculs(self.tableWidget_3, self.lineEdit_moyenne_etalon_3,self.lineEdit_moyenne_etalon_3_arrondie,  
                        self.lineEdit_moyenne_afficheur_3, self.lineEdit_moyenne_afficheur_3_arrondie,  
                        self.lineEdit_correction_3, self.lineEdit_correction_3_arrondie, 
                        self.lineEdit_ecartype_3, self.lineEdit_incertitude_3, 
                        self.lineEdit_incertitude_3_arrondie, self.doubleSpinBox_resolution_3)
         
                self.conformite(self.comboBox_EMT_3, self.lineEdit_correction_3, 
                                self.lineEdit_incertitude_3, self.lineEdit_conformite_3, 
                                self.doubleSpinBox_resolution_3, self.lineEdit_moyenne_etalon_3, 
                                self.textEdit_commentaire_conformite_3, self.lineEdit_valeur_emt_3)
            
            else:
                pass                        

            
        except decimal.InvalidOperation:            
            if colonne == 0:                
                self.ecriture_tableau(self.tableWidget_3, ligne, 1, "Erreur de Saisie donnees etalon brute", 'red')            
            elif colonne == 2:
                self.ecriture_tableau(self.tableWidget_3, ligne, colonne, string_valeur_afficheur, 'red')

            self.calculs(self.tableWidget_3, self.lineEdit_moyenne_etalon_3,self.lineEdit_moyenne_etalon_3_arrondie,  
                        self.lineEdit_moyenne_afficheur_3, self.lineEdit_moyenne_afficheur_3_arrondie,  
                        self.lineEdit_correction_3, self.lineEdit_correction_3_arrondie, 
                        self.lineEdit_ecartype_3, self.lineEdit_incertitude_3, 
                        self.lineEdit_incertitude_3_arrondie, self.doubleSpinBox_resolution_3)
    

    
    
    
    def ecriture_tableau(self, nom_tableau_, ligne, colonne, valeur, color):
        '''fct pour ecrire dans une case du tableau si une erreur fond case rouge'''
        
        nom_tableau_.setCurrentCell (1,1)
        item = QtGui.QTableWidgetItem(str(valeur))
        item.setBackground(QtGui.QColor(color))
        nom_tableau_.setItem(ligne, colonne, item)
        if colonne == 1:
            nom_tableau_.setCurrentCell ((ligne + 1),(colonne - 1))
        else:
            nom_tableau_.setCurrentCell ((ligne + 1),colonne)
    
    def nettoyage_tableaux(self):
        
        nom_tableaux = [self.tableWidget, self.tableWidget_2, self.tableWidget_3]
        for nom in nom_tableaux:
            nom.clear()
            
            item = QtGui.QTableWidgetItem("Etalon")
            nom.setHorizontalHeaderItem(0, item)
            item = QtGui.QTableWidgetItem("Etalon corrigé")
            nom.setHorizontalHeaderItem(1, item)
            item = QtGui.QTableWidgetItem("Afficheur")
            nom.setHorizontalHeaderItem(2, item)

        
    def calculs(self, nom_tableau, nom_lineedit_moyenne_etalon, nom_lineedit_moyenne_etalon_arrondie,
                nom_lineedit_moyenne_afficheur, nom_lineedit_moyenne_afficheur_arrondie, 
                nom_lineedit_correction, nom_lineedit_correction_arrondie, 
                nom_lineedit_ecartype, nom_lineedit_incertitude, nom_lineedit_incertitude_arrondie, 
                nom_doublespinbox):
        '''fct pour calculer moyenne etalon,moyenne afficheurs ,....'''       
        try:
            #preparation des donnees issues du doublespinbox
            nom_doublespinbox.setDecimals(2) #permet de pas avoir de valeur float non exact sur spin box
            resolution_text = str(nom_doublespinbox.value())
            a = str(resolution_text.replace(",", "."))
            if a == "1.0":
                a = "1."
            elif  a == "2.0":
                a = "2."
                
            #calcul automatique moyenne etalon corrigé
            valeurs_etalon_corriges = []
            valeurs_afficheur = []
            nbr_mesure = self.spinBox_2.value()
           
            for i in range (0, nbr_mesure):
                if nom_tableau.item(i, 1) is not None:
                    valeurs_etalon_corriges.append(decimal.Decimal(nom_tableau.item(i, 1).text()))
                else:
                    pass
            
            moyenne_etal_corri = np.mean(valeurs_etalon_corriges)
            nom_lineedit_moyenne_etalon.setText(str(moyenne_etal_corri))
            
            #arrondi moyenne etalon            
            conversion_b = str(moyenne_etal_corri)
            moyenne_etal_corri_arrondie = decimal.Decimal(conversion_b).quantize(decimal.Decimal(a), rounding=decimal.ROUND_HALF_EVEN)
            nom_lineedit_moyenne_etalon_arrondie.setText(str(moyenne_etal_corri_arrondie))
    #            print("resolution {}".format(resolution_text))
                
            # calcul moyenne afficheur:            
            for i in range(0, nbr_mesure):
                if nom_tableau.item(i, 2) is not None:
                    valeurs_afficheur.append(decimal.Decimal(nom_tableau.item(i, 2).text()))
                else:
                    pass
            
            moyenne_afficheur = np.mean(valeurs_afficheur)
            nom_lineedit_moyenne_afficheur.setText(str(moyenne_afficheur))    
            
            #arrondi moyenne afficheur
            conversion_b = str(moyenne_afficheur)
            moyenne_afficheur_arrondie = decimal.Decimal(conversion_b).quantize(decimal.Decimal(a), rounding=decimal.ROUND_HALF_EVEN)
            nom_lineedit_moyenne_afficheur_arrondie.setText(str(moyenne_afficheur_arrondie))
            
            
            #Corrections , moyenne des corrections,ecart type_afficheur:
            
            corrections =[]
            for i in range(0, nbr_mesure):
                if nom_tableau.item(i, 1) is not None and nom_tableau.item(i, 2) is not None:
                    corrections.append(decimal.Decimal(nom_tableau.item(i, 1).text())- decimal.Decimal(nom_tableau.item(i, 2).text()))
                else:
                    pass
            moyenne_corrections = np.mean(corrections)
            if len(corrections) >1:
                ecartype_corrections = np.std(corrections , ddof=1)
            else:
                ecartype_corrections = 0
            nom_lineedit_correction.setText(str(moyenne_corrections))
            nom_lineedit_ecartype.setText(str(ecartype_corrections))
            
            #arrondi correction
            conversion_b = str(moyenne_corrections)
            moyenne_correction_arrondie = decimal.Decimal(conversion_b).quantize(decimal.Decimal(a), rounding=decimal.ROUND_HALF_EVEN)
            nom_lineedit_correction_arrondie.setText(str(moyenne_correction_arrondie))
                        
                        
            
            #Incertitudes:
                #SAT#
                ####################################################################################################c
            if self.comboBox_famille_afficheur.currentText() == "Sonde alarme température" or self.comboBox_famille_afficheur.currentText() == "Afficheur de température":
                    #etalon
                    ############################################
                        #uetalonnage
                identification_etalon = self.comboBox_ident_etalon.currentText()
                ce_select = self.comboBox_ce_etal.currentText()
                n_ce = ce_select[:len(ce_select)-12]
                
                U_etalonnage_etalon = self.db.incertitude_etalonnage_temperature(identification_etalon, n_ce)
                
                if len(U_etalonnage_etalon) == 0:#permet de voir si etalonnage nn fait sur labotemp
                    U_etalonnage_etalon = self.db.incertitude_etalonnage_temperatre_bis(identification_etalon, n_ce)
                
                max_u_etalonnage = float(np.amax(U_etalonnage_etalon)/2)
                
                        #umodelisation                
                table_etal_tlue_correction = self.db.recuperation_corrections_etalonnage_temp(identification_etalon, n_ce)
                
                if len(table_etal_tlue_correction) == 0:
                    table_etal_tlue_correction = self.db.recuperation_corrections_etalonnage_temp_bis(identification_etalon, n_ce)
                
                tlue_etalonnage = [x[0] for x in table_etal_tlue_correction ]
                correction_etalonnage = [decimal.Decimal(x[1]) for x in table_etal_tlue_correction ]
    
                if self.ordre_poly_etalon == 1:
                    correction_modelisee = [decimal.Decimal(x * self.coeff_a_poly_etalon + self.coeff_b_poly_etalon) for x in tlue_etalonnage]
                else:                    
                    correction_modelisee = [decimal.Decimal(x * x* self.coeff_a_poly_etalon + x * self.coeff_b_poly_etalon +self.coeff_c_poly_etalon) for x in tlue_etalonnage]
    
                residu = []
                for i in range(0, len(correction_etalonnage)):
                    valeur_residu = correction_etalonnage[i]-correction_modelisee[i]
                    residu.append(valeur_residu)
                max_residu_absolu = np.amax([np.abs(x) for x in residu])
                                
                u_modelisation = np.array(max_residu_absolu, dtype=np.float)/np.sqrt(3)
                
                        #uresolution
                resolution_etalon = float(self.db.recuperation_resolution_etalon(identification_etalon))                
                u_resolution_etalon = resolution_etalon/(2*np.sqrt(3))
                
                        #uderive (pour linstant 0.15)
                u_derive = 0.15/np.sqrt(3)
                                
                    #sat/aft
                    #####################################################################################
                        #uresolution
    
                resolution = nom_doublespinbox.value()#float(self.db.recuperation_resolution_etalon(ident_sat))
                
                u_resolution = resolution/(2*np.sqrt(3))
                
                        #ufidelite
                u_fidelite = float(ecartype_corrections)
                
                    #milieu de comparaison
                    ##################################################################################
                        #stabilite
                u_stab =np.std(np.array(valeurs_etalon_corriges, dtype=np.float), ddof=1)
                
                if nbr_mesure > 1:
                    U_final = 2*np.sqrt(np.power(max_u_etalonnage, 2)+ np.power(u_modelisation, 2)+
                        np.power(u_resolution_etalon, 2) + np.power(u_derive, 2) + np.power(u_resolution, 2)+
                        np.power(u_fidelite, 2) + np.power(u_stab, 2))
                else:
                    U_final = 2*np.sqrt(np.power(max_u_etalonnage, 2)+ np.power(u_modelisation, 2)+
                        np.power(u_resolution_etalon, 2) + np.power(u_derive, 2) + np.power(u_resolution, 2))
                nom_lineedit_incertitude.setText(str(U_final))
                
                #arrondi U
                conversion_b = str(U_final)
                U_arrondie = decimal.Decimal(conversion_b).quantize(decimal.Decimal(a), rounding=decimal.ROUND_UP)
                nom_lineedit_incertitude_arrondie.setText(str(U_arrondie))
    
        
            elif self.comboBox_famille_afficheur.currentText() == "Afficheur de vitesse":
                
                #etalon
                    ############################################
                        #uetalonnage
                identification_etalon = self.comboBox_ident_etalon.currentText()
                
                ce_select = self.comboBox_ce_etal.currentText()
                n_ce = ce_select[:len(ce_select)-12]
                
                U_etalonnage_etalon = self.db.incertitude_etalonnage_vitesse(identification_etalon, n_ce)
              
                max_u_etalonnage = float(np.amax(U_etalonnage_etalon)/2)
                
    #                print("u etal  {}".format(max_u_etalonnage))
    
                
                        #umodelisation                
                table_etal_tlue_correction = self.db.recuperation_corrections_etalonnage_vitesse(identification_etalon, n_ce)
                tlue_etalonnage = [x[0] for x in table_etal_tlue_correction ]
                correction_etalonnage = [decimal.Decimal(x[1]) for x in table_etal_tlue_correction ]
    
                if self.ordre_poly_etalon == 1:
                    correction_modelisee = [decimal.Decimal(x * self.coeff_a_poly_etalon + self.coeff_b_poly_etalon) for x in tlue_etalonnage]
                else:                    
                    correction_modelisee = [decimal.Decimal(x * x* self.coeff_a_poly_etalon + x * self.coeff_b_poly_etalon +self.coeff_c_poly_etalon) for x in tlue_etalonnage]
    
                residu = []
                for i in range(0, len(correction_etalonnage)):
                    valeur_residu = correction_etalonnage[i]-correction_modelisee[i]
                    residu.append(valeur_residu)
                max_residu_absolu = np.amax([np.abs(x) for x in residu])
                                
                u_modelisation = np.array(max_residu_absolu, dtype=np.float)/np.sqrt(3)
                
    #                print("umodelisation {}".format(u_modelisation))
                
                        #uresolution
                resolution_etalon = float(self.db.recuperation_resolution_etalon(identification_etalon))                
                u_resolution_etalon = resolution_etalon/(2*np.sqrt(3))
                
    #                print("u_resolution_etalon {}".format(u_resolution_etalon))
                
                        #uderive (pour linstant 0.15)
                u_derive = 2/np.sqrt(3)  #;valeur max trouvé sur tac 1
                                    #sat/aft
                #####################################################################################
                        #uresolution
    
                resolution = nom_doublespinbox.value()#float(self.db.recuperation_resolution_etalon(ident_sat))
                
                u_resolution = resolution/(2*np.sqrt(3))
                
    #                print("u_resolution {}".format(u_resolution))
                
                        #ufidelite
                u_fidelite = float(ecartype_corrections)                
    
    #                print("u_fidelite {}".format(u_fidelite))
                U_final = 2*np.sqrt(np.power(max_u_etalonnage, 2)+ np.power(u_modelisation, 2)+
                    np.power(u_resolution_etalon, 2) + np.power(u_derive, 2) + np.power(u_resolution, 2)+
                    np.power(u_fidelite, 2))
    #                print("U_final {}".format(U_final))
                nom_lineedit_incertitude.setText(str(U_final))
                
                #arrondi U
                conversion_b = str(U_final)
                U_arrondie = decimal.Decimal(conversion_b).quantize(decimal.Decimal(a), rounding=decimal.ROUND_UP)
                nom_lineedit_incertitude_arrondie.setText(str(U_arrondie))
                
                
                
            elif self.comboBox_famille_afficheur.currentText() == "Afficheur de temps":
                                #etalon
                    ############################################
                        #uetalonnage
                identification_etalon = self.comboBox_ident_etalon.currentText()
                                
                ce_select = self.comboBox_ce_etal.currentText()
                n_ce = ce_select[:len(ce_select)-12]
    
                U_etalonnage_etalon = 1 #(1s) #self.db.incertitude_etalonnage_vitesse(identification_etalon, n_ce)
              
                max_u_etalonnage = float(np.amax(U_etalonnage_etalon)/2)
    
                
                        #umodelisation                
                table_etal_tlue_correction = self.db.recuperation_corrections_etalonnage_vitesse(identification_etalon, n_ce)
                tlue_etalonnage = [x[0] for x in table_etal_tlue_correction ]
                correction_etalonnage = [decimal.Decimal(x[1]) for x in table_etal_tlue_correction ]
    
                if self.ordre_poly_etalon == 1:
                    correction_modelisee = [decimal.Decimal(x * self.coeff_a_poly_etalon + self.coeff_b_poly_etalon) for x in tlue_etalonnage]
                else:                    
                    correction_modelisee = [decimal.Decimal(x * x* self.coeff_a_poly_etalon + x * self.coeff_b_poly_etalon +self.coeff_c_poly_etalon) for x in tlue_etalonnage]
    
                residu = []
                for i in range(0, len(correction_etalonnage)):
                    valeur_residu = correction_etalonnage[i]-correction_modelisee[i]
                    residu.append(valeur_residu)
                max_residu_absolu = np.amax([np.abs(x) for x in residu])
                                
                u_modelisation = np.array(max_residu_absolu, dtype=np.float)/np.sqrt(3)
                
                        #uresolution
                resolution_etalon = float(self.db.recuperation_resolution_etalon(identification_etalon))                
                u_resolution_etalon = resolution_etalon/(2*np.sqrt(3))
                
                        #uderive (pour linstant 0.15)
                u_derive = 1/np.sqrt(3)  #incertitude etalonnage
                                    #sat/aft
                #####################################################################################
                        #uresolution
    
                resolution = nom_doublespinbox.value()#float(self.db.recuperation_resolution_etalon(ident_sat))
                
                u_resolution = resolution/(2*np.sqrt(3))
                
                        #ufidelite
                u_fidelite = float(ecartype_corrections)                
    
                
                U_final = 2*np.sqrt(np.power(max_u_etalonnage, 2)+ np.power(u_modelisation, 2)+
                    np.power(u_resolution_etalon, 2) + np.power(u_derive, 2) + np.power(u_resolution, 2)+
                    np.power(u_fidelite, 2))
                
                nom_lineedit_incertitude.setText(str(U_final))
                
                #arrondi U
                conversion_b = str(U_final)
                U_arrondie = decimal.Decimal(conversion_b).quantize(decimal.Decimal(a), rounding=decimal.ROUND_UP)
                nom_lineedit_incertitude_arrondie.setText(str(U_arrondie))
                
                
        except decimal.InvalidOperation:            
            affichage = "Erreur dans les saisies effectuées"
            nom_lineedit_moyenne_etalon.setText(affichage)
    
    def conformite(self, nom_comboBox_EMT, nom_lineEdit_correction, 
                    nom_lineedit_incertitude, nom_lineEdit_conformite, 
                    nom_doublespinbox_resolution, nom_lineEdit_moyenne_etalon, 
                    nom_commentaire_referentiel, nom_lineEdit_valeur_emt):
        '''fct qui gere la declaration de conformite'''
        try:
            nom_doublespinbox_resolution.setDecimals(2) #permet de pas avoir de valeur float non exact sur spin box
            resolution = str(nom_doublespinbox_resolution.value())
            nom_commentaire_referentiel.clear()        
                
            if resolution == "1.0":
                resolution = "1."
            elif  resolution == "2.0":
                resolution = "2."        
            
#            print("resolution {}".format(resolution))
            
            U = nom_lineedit_incertitude.text()
            U_arrondie = decimal.Decimal(U).quantize(decimal.Decimal(resolution), rounding=decimal.ROUND_UP)
#            print("U_arrondie {}".format(U_arrondie))
            
            moyenne_corrections = nom_lineEdit_correction.text()
            moyenne_corrections_arrondie = decimal.Decimal(moyenne_corrections).quantize(decimal.Decimal(resolution), rounding=decimal.ROUND_HALF_EVEN)

            
            somme_u_correction = np.abs(float(moyenne_corrections_arrondie)) + float(U_arrondie)
            somme_u_correction_arrondie = decimal.Decimal(somme_u_correction).quantize(decimal.Decimal(resolution), rounding=decimal.ROUND_HALF_EVEN)
            

            if self.comboBox_famille_afficheur.currentText() == "Sonde alarme température" or self.comboBox_famille_afficheur.currentText() == "Afficheur de température":
                nom_brute_emt = nom_comboBox_EMT.currentText()
                commentaire = self.db.commentaire_referentiel(nom_brute_emt)
                nom_commentaire_referentiel.append(commentaire)
                terme_emt = self.db.valeur_emt(nom_brute_emt)
                terme_cte = float(terme_emt[0][0])
#                
                terme_variable = float(terme_emt[0][1])
#                
                valeur_emt = round((float(nom_lineEdit_moyenne_etalon.text()) * (terme_variable/100) + terme_cte), 2)                
                
#                                
                if commentaire == "Déclaration de conformité selon ISO 14 253-1 (prise en compte de U)":
                    if float(somme_u_correction_arrondie) <= valeur_emt:
                        nom_lineEdit_conformite.setText("Conforme")
                    else:
                        nom_lineEdit_conformite.setText("Non Conforme")
                elif commentaire == "Déclaration de conformité sans prise en compte de U":
                    
                    if np.abs(float(moyenne_corrections_arrondie)) <= valeur_emt:
                        nom_lineEdit_conformite.setText("Conforme")
                    else:
                        nom_lineEdit_conformite.setText("Non Conforme")
                    
            elif self.comboBox_famille_afficheur.currentText() == "Afficheur de vitesse":
                nom_brute_emt = nom_comboBox_EMT.currentText()
                commentaire = self.db.commentaire_referentiel(nom_brute_emt)
                nom_commentaire_referentiel.append(commentaire)
                terme_emt = self.db.valeur_emt(nom_brute_emt)
                terme_cte = float(terme_emt[0][0])
                terme_variable = float(terme_emt[0][1])
#                emt = float(terme_emt[0][1]) #on enleve signe +- et %
                valeur_emt = int(float(float(nom_lineEdit_moyenne_etalon.text())) * (terme_variable/100) + terme_cte)
    
                if commentaire == "Déclaration de conformité selon ISO 14 253-1 (prise en compte de U)":
                    if float(somme_u_correction_arrondie) <= valeur_emt:
                        nom_lineEdit_conformite.setText("Conforme")
                    else:
                        nom_lineEdit_conformite.setText("Non Conforme")
                elif commentaire == "Déclaration de conformité sans prise en compte de U":
                    if np.abs(float(moyenne_corrections_arrondie)) <= valeur_emt:
                        nom_lineEdit_conformite.setText("Conforme")
                    else:
                        nom_lineEdit_conformite.setText("Non Conforme")
        
            elif self.comboBox_famille_afficheur.currentText() == "Afficheur de temps":
                nom_brute_emt = nom_comboBox_EMT.currentText()
                commentaire = self.db.commentaire_referentiel(nom_brute_emt)
                nom_commentaire_referentiel.append(commentaire)
                terme_emt = self.db.valeur_emt(nom_brute_emt)
                terme_cte = float(terme_emt[0][0])
                terme_variable = float(terme_emt[0][1])
                valeur_emt = int(float(nom_lineEdit_moyenne_etalon.text()) * (terme_variable/100) + terme_cte)
                
                if commentaire == "Déclaration de conformité selon ISO 14 253-1 (prise en compte de U)":
                    if float(somme_u_correction_arrondie) <= valeur_emt:
                        nom_lineEdit_conformite.setText("Conforme")
                    else:
                        nom_lineEdit_conformite.setText("Non Conforme")
                elif commentaire == "Déclaration de conformité sans prise en compte de U":
                    if np.abs(float(moyenne_corrections_arrondie)) <= valeur_emt:
                        nom_lineEdit_conformite.setText("Conforme")
                    else:
                        nom_lineEdit_conformite.setText("Non Conforme")
                        
            nom_lineEdit_valeur_emt.setText(str(valeur_emt))
            
        except ValueError:
            nom_lineEdit_conformite.setText("Non applicable")
            pass
            
    @pyqtSlot()
    def on_actionEnregistrement_triggered(self):
        """
        fct qui enregistre les resultats dans la bdd et genere le rapport
        """
        if self.comboBox_type_rapport.currentText() != "*":
            dossier = QFileDialog.getExistingDirectory(None ,  "Selectionner le dossier de sauvegarde des Rapports", 'y:/1.METROLOGIE/0.ARCHIVES ETALONNAGE-VERIFICATIONS/4-AFFICHEURS/')
        
            if dossier !="":         
                afficheur = self.lecture_saisie()
            
            
                afficheur["type_rapport"] = self.comboBox_type_rapport.currentText()
                afficheur["annule_remplace"] = self.n_ce_annule_remplace
                afficheur["n_certificat"] = self.db.sauvegarde_table_afficheur_ctrl_admin(afficheur)            
                
                QMessageBox.information(self, 
                        self.trUtf8("N° Certificat"), 
                        self.trUtf8(afficheur["n_certificat"]))            
                
                afficheur["valeur_numerique_emt"] = self.calcul_valeur_numerique_emt()
                
                type_rapport = self.comboBox_type_rapport.currentText()
                
                cvr = RapportAfficheur(type_rapport)
                cvr.mise_en_forme_ce(afficheur, dossier, afficheur["n_certificat"]) 
                
                #nettoyage
                self.nettoyage_gui()
    #            self.valeur_numerique_emt = ""
                self.doubleSpinBox_resolution.setValue(float(0.1))
                self.doubleSpinBox_resolution_2.setValue(float(0.1))
                self.doubleSpinBox_resolution_3.setValue(float(0.1))
                
                self.n_ce_annule_remplace = ""
                
                self.type_ouverture = 0
            else:
                pass
        
        else:
            QMessageBox.warning(self, 
                        self.trUtf8("Attention"), 
                        self.trUtf8("Merci de selectionner \n un type de rapport de mesure.")) 
        
        
        
    @pyqtSlot(str)
    def on_comboBox_EMT_3_activated(self, p0):
        """
        si changement EMT on recalcul tout
        """
        self.calculs(self.tableWidget_3, self.lineEdit_moyenne_etalon_3,self.lineEdit_moyenne_etalon_3_arrondie,  
                        self.lineEdit_moyenne_afficheur_3, self.lineEdit_moyenne_afficheur_3_arrondie,  
                        self.lineEdit_correction_3, self.lineEdit_correction_3_arrondie, 
                        self.lineEdit_ecartype_3, self.lineEdit_incertitude_3, 
                        self.lineEdit_incertitude_3_arrondie, self.doubleSpinBox_resolution_3)
                        
        self.conformite(self.comboBox_EMT_3, self.lineEdit_correction_3, self.lineEdit_incertitude_3,
                        self.lineEdit_conformite_3, self.doubleSpinBox_resolution_3, 
                        self.lineEdit_moyenne_etalon_3, self.textEdit_commentaire_conformite_3, self.lineEdit_valeur_emt_3)

    
    @pyqtSlot(str)
    def on_comboBox_EMT_2_activated(self, p0):
        """
        si changement EMT on recalcul tout
        """
        self.calculs(self.tableWidget_2, self.lineEdit_moyenne_etalon_2, self.lineEdit_moyenne_etalon_2_arrondie, 
                        self.lineEdit_moyenne_afficheur_2, self.lineEdit_moyenne_afficheur_2_arrondie, 
                        self.lineEdit_correction_2, self.lineEdit_correction_2_arrondie, 
                        self.lineEdit_ecartype_2, self.lineEdit_incertitude_2, self.lineEdit_incertitude_2_arrondie, 
                        self.doubleSpinBox_resolution_2)
                        
        self.conformite(self.comboBox_EMT_2, self.lineEdit_correction_2, self.lineEdit_incertitude_2, 
                        self.lineEdit_conformite_2, self.doubleSpinBox_resolution_2, self.lineEdit_moyenne_etalon_2,
                        self.textEdit_commentaire_conformite_2, self.lineEdit_valeur_emt_2)
   
    @pyqtSlot(str)
    def on_comboBox_EMT_activated(self, p0):
        """
        si changement EMT on recalcul tout
        """
        if self.type_ouverture == 0:
            reponse = QMessageBox.question(self, 
                    self.trUtf8("Information"), 
                    self.trUtf8("Voulez-vous appliquer ce referentiel à tous les points ?"), 
                    QtGui.QMessageBox.Yes, QtGui.QMessageBox.No)
            
            if reponse == QtGui.QMessageBox.Yes:
                id_ref = self.comboBox_EMT.currentIndex()
                self.comboBox_EMT_2.setCurrentIndex(id_ref)
                self.comboBox_EMT_3.setCurrentIndex(id_ref)
            else:
                pass
        else:
            pass
        self.calculs(self.tableWidget, self.lineEdit_moyenne_etalon, self.lineEdit_moyenne_etalon_arrondie, 
                        self.lineEdit_moyenne_afficheur, self.lineEdit_moyenne_afficheur_arrondie, 
                        self.lineEdit_correction, self.lineEdit_correction_arrondie, 
                        self.lineEdit_ecartype, self.lineEdit_incertitude, self.lineEdit_incertitude_arrondie, 
                        self.doubleSpinBox_resolution)
                            
        self.conformite(self.comboBox_EMT, self.lineEdit_correction, self.lineEdit_incertitude,
                        self.lineEdit_conformite, self.doubleSpinBox_resolution, 
                        self.lineEdit_moyenne_etalon, self.textEdit_commentaire_conformite, self.lineEdit_valeur_emt)
    
    @pyqtSlot(str)
    def on_comboBox_cmr_activated(self, p0):
        """
        Slot documentation goes here.
        """

        self.lineEdit_site.clear()
        self.lineEdit_service.clear()
        



    
    
    @pyqtSlot()
    def on_actionCreation_EMT_triggered(self):
        """
        ouverture d'un widget pour la creation d'emt et enregistrement dans la bdd
        """
        
        self.creation_emt = Creation_emt()
        self.connect(self.creation_emt, SIGNAL("fermeturequelclient(PyQt_PyObject)"), self.db.insertion_ref_emt)
        self.creation_emt.setWindowModality(QtCore.Qt.ApplicationModal)
        self.creation_emt.show()
        
        #on actualise les emt
        type_afficheur = str(self.comboBox_famille_afficheur.currentText())
        referentiel = self.db.recensement_referentiel_emt(type_afficheur)
        #nettoyage combobox emt
        self.comboBox_EMT.clear()
        self.comboBox_EMT_2.clear()
        self.comboBox_EMT_3.clear()
        nom_ref = [x[0] for x in referentiel]
        self.comboBox_EMT.addItems(nom_ref)
        self.comboBox_EMT_2.addItems(nom_ref)
        self.comboBox_EMT_3.addItems(nom_ref)
    
    @pyqtSlot()
    def on_actionCreation_afficheur_triggered(self):
        """
        Slot documentation goes here.
        """
        # TODO: not implemented yet
        code_client = self.db.recuperation_code_client()
        code_client.sort()
        
        constructeurs = self.db.recuperation_constructeurs()
        constructeurs.sort()
        
        service = self.db.recuperation_service()
        service.sort()
        
        self.creation_afficheur = Creation_afficheur(code_client, constructeurs, service)
        self.connect(self.creation_afficheur, SIGNAL("fermeturecreationafficheur(PyQt_PyObject)"), self.gestion_nouveau_afficheur)
        
        self.creation_afficheur.setWindowModality(QtCore.Qt.ApplicationModal)
        self.creation_afficheur.show()
        
    
    
    def gestion_nouveau_afficheur(self, afficheur):
        '''fct qui gere l'insertion dans la bdd d'un nouvelle afficheur
        recupere son nom et l'affiche dans un qmessagebox'''
        
        reference_new_afficheur = self.db.insertion_afficheur(afficheur)
           
        QMessageBox.information(self, 
                    self.trUtf8("N°afficheur créé"), 
                    self.trUtf8(reference_new_afficheur))
    
    @pyqtSlot()
    def on_actionModification_de_saisie_triggered(self):
        """
        Fct pour modifier un etalonnage d'afficheur
        """
        self.type_ouverture = 1
        self.actionEnregistrement.setEnabled(False)
        self.actionMise_jour.setEnabled(True)
        self.actionArchivage.setEnabled(False)
        
        self.spinBox.setEnabled(False)
        self.spinBox_2.setEnabled(False)
        
        #recuperation des donnees
        num_ce = self.db.recuperation_n_ce_actif()
        n_ce = QInputDialog.getItem(self, 
                       self.trUtf8("Numero certificats"), 
                       self.trUtf8("Choisir un numero"),
                       num_ce)

        if n_ce[1] == True:
            saisie = self.db.recuperation_etalonnage_saisie(n_ce[0])
            
            #affectation du n°ce sur la variable de classe pour mise à jour
            self.n_ce_pour_modification = n_ce[0]
            if saisie["annule_remplace"] != None:
                self.n_ce_annule_remplace = saisie["annule_remplace"]
                
           #Appel fct de reaffectation des donnees
            self.reaffectation_donnees_saisie(saisie)   
        else:
            pass

    @pyqtSlot()
    def on_actionValidation_triggered(self):
        """
        Slot documentation goes here.
        """
        # TODO: not implemented yet
        self.type_ouverture = 1
        self.actionEnregistrement.setEnabled(False)
        self.actionMise_jour.setEnabled(False)
        self.actionArchivage.setEnabled(True)
        
        #recuperation des donnees
        num_ce = self.db.recuperation_n_ce_actif()
        n_ce = QInputDialog.getItem(self, 
                       self.trUtf8("Numero certificats"), 
                       self.trUtf8("Choisir un numero"),
                       num_ce)

        if n_ce[1] == True:
            
            saisie = self.db.recuperation_etalonnage_saisie(n_ce[0])

            #affectation du n°ce sur la variable de classe pour mise à jour
            self.n_ce_pour_modification = n_ce[0]
           
           #Appel fct de reaffectation des donnees
#            print(saisie)
            self.reaffectation_donnees_saisie(saisie)  
        else:
            pass
        
        
    def lecture_saisie(self):
        '''fct qui recuper les saisies effectué sur la gui'''
        resolution_afficheur_list = [self.doubleSpinBox_resolution.value(), self.doubleSpinBox_resolution_2.value(), self.doubleSpinBox_resolution_3.value()]
        moyenne_etalon_list = [self.lineEdit_moyenne_etalon.text(), self.lineEdit_moyenne_etalon_2.text(), self.lineEdit_moyenne_etalon_3.text()]
        moyenne_afficheur_list = [self.lineEdit_moyenne_afficheur.text(), self.lineEdit_moyenne_afficheur_2.text(), self.lineEdit_moyenne_afficheur_3.text()]
        moyenne_corrections_list = [self.lineEdit_correction.text(), self.lineEdit_correction_2.text(), self.lineEdit_correction_3.text()]
        ecartype_corrections_list = [self.lineEdit_ecartype.text(), self.lineEdit_ecartype_2.text(), self.lineEdit_ecartype_3.text()]
        U_list = [self.lineEdit_incertitude.text(), self.lineEdit_incertitude_2.text(), self.lineEdit_incertitude_3.text()]
#            referentiel_conformite_list = [self.comboBox_EMT.currentText(), self.comboBox_EMT_2.currentText(), self.comboBox_EMT_3.currentText()]
        conformite_list = [self.lineEdit_conformite.text(), self.lineEdit_conformite_2.text(), self.lineEdit_conformite_3.text()]
        emt_list = [self.comboBox_EMT.currentText(), self.comboBox_EMT_2.currentText(), self.comboBox_EMT_3.currentText()]
        commentaire_referentiel = [self.textEdit_commentaire_conformite.toPlainText(), self.textEdit_commentaire_conformite_2.toPlainText(), self.textEdit_commentaire_conformite_3.toPlainText()]
        
        afficheur = {}
        client = self.db.recuperation_code_client_affectation(self.comboBox_identification.currentText())
#        afficheur["n_certificat"] = 
        
        afficheur["societe"] = client[0]
        afficheur["affectation"] = client[1]
        afficheur["adresse"] = client[2]
        afficheur["code_postal"] = client[3]
        afficheur["ville"] = client[4]
        
        afficheur["identification_instrument"] = self.comboBox_identification.currentText()
        afficheur["n_serie"] = self.textEdit_n_serie.toPlainText ()
        afficheur["constructeur"] = self.lineEdit_constructeur.text()
        afficheur["designation"] = self.comboBox_famille_afficheur.currentText()
        afficheur["type"] = self.lineEdit_type.text()
        afficheur["resolution"] = resolution_afficheur_list 
        afficheur["date_etalonnage"] = self.dateEdit.date().toString('dd/MM/yyyy')
        afficheur["annee_ctrl"]= self.dateEdit.date().year()
        afficheur["type_rapport"] = self.comboBox_type_rapport.currentText()
        afficheur["num_doc_provisoire"] = self.dateEdit.date().toString('yyyyMM')
        afficheur["operateur"] = self.comboBox_cmr.currentText()
        
          
        if self.comboBox_famille_afficheur.currentText() == "Sonde alarme température":
            afficheur["n_mode_operatoire"] = "/006"
        else:
            afficheur["n_mode_operatoire"] = "/002"

        afficheur["etalon"] = self.comboBox_ident_etalon.currentText()
        afficheur["ce_etalon"] = self.comboBox_ce_etal.currentText()
        afficheur["operateur"] = self.comboBox_cmr.currentText()
        afficheur["renseignement_complementaire"] = self.textEdit_renseignement_complementaire.toPlainText()
                    
        afficheur["commentaire"] = self.textEdit_commentaire.toPlainText()
        
        afficheur["moyenne_etalon_corri"] = moyenne_etalon_list
        afficheur["moyenne_instrum"] = moyenne_afficheur_list
        afficheur["moyenne_correction"] = moyenne_corrections_list
        afficheur["U"] = U_list
        
        afficheur["conformite"] = conformite_list
        afficheur["emt"] = emt_list
        afficheur["commentaire_referentiel"] = commentaire_referentiel
        
        afficheur["nbr_pt_etalonnage"] = self.spinBox.value()
        
        #recuperation donneees dans les tableaux
        nom_tableau = [self.tableWidget, self.tableWidget_2, self.tableWidget_3]
        nbr_mesure = self.spinBox_2.value()
        
        list_valeurs_etalon_non_corriges = []
        list_valeurs_etalon_corriges = []
        list_valeurs_afficheur = []
        item = QtGui.QTableWidgetItem()

        for i in range(0, afficheur["nbr_pt_etalonnage"]):
            valeurs_etalon_non_corriges = []
            valeurs_etalon_corriges = []
            valeurs_afficheur = []
            
            for j in range (0, nbr_mesure):                    
                valeurs_etalon_non_corriges.append(decimal.Decimal(nom_tableau[i].item(j, 0).text()))                     
                valeurs_etalon_corriges.append(decimal.Decimal(nom_tableau[i].item(j, 1).text()))                   
                valeurs_afficheur.append(decimal.Decimal(nom_tableau[i].item(j, 2).text()))  
            
            list_valeurs_etalon_non_corriges.append(valeurs_etalon_non_corriges)
            list_valeurs_etalon_corriges.append(valeurs_etalon_corriges)
            list_valeurs_afficheur.append(valeurs_afficheur)
       

        afficheur["valeurs_etalon_nc"] = list_valeurs_etalon_non_corriges
        afficheur["valeurs_etalon_c"] = list_valeurs_etalon_corriges
        afficheur["valeurs_afficheur"] = list_valeurs_afficheur            
        afficheur["commentaire_resultats"] = self.textEdit_renseignementresultat.toPlainText()
#            afficheur["n_certificat"] = self.db.sauvegarde_table_afficheur_ctrl_admin(afficheur)
       
        return afficheur
        
        
    def reaffectation_donnees_saisie(self, saisie):
        '''fct permettant de reaffecter les donnees recuperees dans la bdd'''
                #reaffectation : 
#        print(saisie)

#        print("cmr{}".format(saisie["nom_cmr"]))
        index_cmr = self.comboBox_cmr.findText(saisie["nom_cmr"])
#        print("id cmr {}".format(index_cmr))
        self.comboBox_cmr.setCurrentIndex(index_cmr)
        self.on_comboBox_cmr_activated(saisie["nom_cmr"])
        
#        print("famille aff combobox {}".format(saisie["famille_afficheur"]))
        index_famille_afficheur = self.comboBox_famille_afficheur.findText(saisie["famille_afficheur"])
#        print("id famille combobox {}".format(index_famille_afficheur))        
        self.comboBox_famille_afficheur.setCurrentIndex(index_famille_afficheur)
        self.on_comboBox_famille_afficheur_activated(saisie["famille_afficheur"])
        
#        print("nom aff combobox {}".format(saisie["identification_afficheur"]))
        index_afficheur = self.comboBox_identification.findText(saisie["identification_afficheur"])
#        print("id aff combobox {}".format(index_afficheur))
        
        self.comboBox_identification.setCurrentIndex(index_afficheur)
        self.on_comboBox_identification_activated(index_afficheur)
        
        self.dateEdit.setDate(saisie["date_etalonnage"])
        
        index_etalon = self.comboBox_ident_etalon.findText(saisie["identification_etalon"])
        self.comboBox_ident_etalon.setCurrentIndex(index_etalon)
        
        self.on_comboBox_ident_etalon_activated(index_etalon)
        
        index_ce_etalon = self.comboBox_ce_etal.findText(saisie["n_ce_etalon"])
        
        
        if index_ce_etalon < 0:
            self.comboBox_ce_etal.addItem(saisie["n_ce_etalon"])
            index_ce_etalon = self.comboBox_ce_etal.findText(saisie["n_ce_etalon"])
        
        self.comboBox_ce_etal.setCurrentIndex(index_ce_etalon)
        self.on_comboBox_ce_etal_activated(index_ce_etalon)
        
        self.spinBox.setValue(saisie["nb_pt_ctrl"])
        self.spinBox_2.setValue(saisie["nbr_mesure"])    
        self.on_spinBox_2_valueChanged(saisie["nbr_mesure"])
        
        index_type_rapport = self.comboBox_type_rapport.findText( saisie["type_rapport"])
        self.comboBox_type_rapport.setCurrentIndex(index_type_rapport)
#        print("mesure {}".format(saisie["mesures"]))
#        print()
        list_tableau = [self.tableWidget, self.tableWidget_2, self.tableWidget_3]
        for i in range(saisie["nb_pt_ctrl"]):
#            print("i {}".format(i))
            #etalon (on le fait en deux fois à cause des modification de cells dans tableau
            for j in range(saisie["nbr_mesure"]):
#                print("j {}".format(j))
                self.ecriture_tableau(list_tableau[i], j, 0, saisie["mesures"][(i+1)][0][j], 'white') #valeur etalon
                if i == 0:
                    list_tableau[i].setCurrentCell (j, 0)
                    self.on_tableWidget_cellChanged(j, 0)
                elif i == 1:
                    list_tableau[i].setCurrentCell (j, 0)
                    self.on_tableWidget_2_cellChanged(j, 0)
                elif i == 2:                    
                    list_tableau[i].setCurrentCell (j, 0)
                    self.on_tableWidget_3_cellChanged(j, 0)
            #afficheur
            for j in range(saisie["nbr_mesure"]):
                self.ecriture_tableau(list_tableau[i], j, 2, saisie["mesures"][(i+1)][1][j], 'white') #valeur etalon
                if i == 0:
                    list_tableau[i].setCurrentCell (j, 2)
                    self.on_tableWidget_cellChanged(j, 2)
                elif i == 1:
                    list_tableau[i].setCurrentCell (j, 2)
                    self.on_tableWidget_2_cellChanged(j, 2)
                elif i == 2:                    
                    list_tableau[i].setCurrentCell (j, 2)
                    self.on_tableWidget_3_cellChanged(j, 2)
        
        list_combobox_emt = [self.comboBox_EMT, self.comboBox_EMT_2, self.comboBox_EMT_3]
        
        for i in range(len(saisie["referentiel_conformite"])):
#            print("nom ref {}".format(saisie["referentiel_conformite"][i]))
            index_ref_emt = list_combobox_emt[i].findText(saisie["referentiel_conformite"][i])
#            print("index ref {}".format(index_ref_emt))
            list_combobox_emt[i].setCurrentIndex(index_ref_emt)
            if i ==0:
                self.on_comboBox_EMT_activated(saisie["referentiel_conformite"][i])
            elif i == 1:
                self.on_comboBox_EMT_2_activated(saisie["referentiel_conformite"][i])
            elif i == 2:
                self.on_comboBox_EMT_3_activated(saisie["referentiel_conformite"][i])
        self.textEdit_renseignementresultat.setText(saisie["commentaire_resultats"])
        
    @pyqtSlot()
    def on_actionMise_jour_triggered(self):
        """
        maj des donnees dans la bdd
        """
        afficheur = self.lecture_saisie()
        self.db.mise_a_jour_donnees_saisie(afficheur, self.n_ce_pour_modification)
        
        dossier = QFileDialog.getExistingDirectory(None ,  "Selectionner le dossier de sauvegarde des Rapports", 'y:/1.METROLOGIE/0.ARCHIVES ETALONNAGE-VERIFICATIONS/4-AFFICHEURS/')
        
        if dossier !="":      
            
            afficheur["valeur_numerique_emt"] = self.calcul_valeur_numerique_emt()
            
            if self.n_ce_annule_remplace == "":
                afficheur["n_certificat"] = self.n_ce_pour_modification 
            else:
                afficheur["n_certificat"] = self.n_ce_pour_modification + "\n" + "Annule et remplace" +\
                                            " "+self.n_ce_annule_remplace
            
            type_rapport = self.comboBox_type_rapport.currentText()
            
            cvr = RapportAfficheur(type_rapport)            
            cvr.mise_en_forme_ce(afficheur, dossier, afficheur["n_certificat"])
            
            self.nettoyage_gui()
            
            self.n_ce_pour_modification = ""
            self.n_ce_annule_remplace = ""
    #        self.valeur_numerique_emt = ""
            
            self.actionEnregistrement.setEnabled(True)
            self.actionArchivage.setEnabled(False)
            self.actionMise_jour.setEnabled(False)
            
            self.spinBox.setEnabled(True)
            self.spinBox_2.setEnabled(True)
            
            self.type_ouverture = 0
        else:
            pass
    def nettoyage_gui(self):
        '''nettoie tout'''
        self.ordre_poly_etalon = 0
        self.coeff_a_poly_etalon = 0
        self.coeff_b_poly_etalon = 0
        self.coeff_c_poly_etalon = 0
        
        self.doubleSpinBox_resolution.setValue(float(0.1))
        self.doubleSpinBox_resolution_2.setValue(float(0.1))
        self.doubleSpinBox_resolution_3.setValue(float(0.1))
        
        
        
        list_combobox_emt = [self.comboBox_EMT, self.comboBox_EMT_2 , self.comboBox_EMT_3]
        for ele in list_combobox_emt:
            ele.clear()
        
        list_lineedit = [self.lineEdit_moyenne_etalon, self.lineEdit_moyenne_etalon_2, 
                            self.lineEdit_moyenne_etalon_3, self.lineEdit_moyenne_etalon_arrondie, 
                            self.lineEdit_moyenne_etalon_2_arrondie, self.lineEdit_moyenne_etalon_3_arrondie, 
                            self.lineEdit_moyenne_afficheur, self.lineEdit_moyenne_afficheur_2, self.lineEdit_moyenne_afficheur_3, 
                            self.lineEdit_moyenne_afficheur_arrondie, self.lineEdit_moyenne_afficheur_2_arrondie, 
                            self.lineEdit_moyenne_afficheur_2_arrondie, self.lineEdit_moyenne_afficheur_3_arrondie, 
                            self.lineEdit_correction, self.lineEdit_correction_2, self.lineEdit_correction_3, 
                            self.lineEdit_correction_arrondie, self.lineEdit_correction_2_arrondie, self.lineEdit_correction_3_arrondie, 
                            self.lineEdit_ecartype, self.lineEdit_ecartype_2, self.lineEdit_ecartype_3, 
                            self.lineEdit_incertitude, self.lineEdit_incertitude_2, self.lineEdit_incertitude_3, 
                            self.lineEdit_incertitude_arrondie, self.lineEdit_incertitude_2_arrondie, self.lineEdit_incertitude_3_arrondie, 
                            self.lineEdit_conformite, self.lineEdit_conformite_2, self.lineEdit_conformite_3]
        
        for ele in list_lineedit:
            ele.clear()
            
        
        #gestion onglet conf 
        self.comboBox_type_rapport.setCurrentIndex(0)
        self.comboBox_cmr.setCurrentIndex(0)
        self.comboBox_famille_afficheur.setCurrentIndex(0)
        
        list_onglet_conf = [self.comboBox_identification, self.lineEdit_site, self.lineEdit_service, self.lineEdit_constructeur, self.lineEdit_type, 
                            self.textEdit_n_serie, self.textEdit_renseignement_complementaire, 
                            self.textEdit_commentaire, self.comboBox_ident_etalon, self.comboBox_ce_etal]
                            
        for ele in list_onglet_conf:
            ele.clear()
        
        
        self.spinBox.setValue(1)
        self.spinBox_2.setValue(1)
        self.on_spinBox_2_valueChanged(1)
        self.tabWidget.setCurrentIndex(0)
        self.textEdit_renseignementresultat.clear()
        
        self.nettoyage_tableaux()
        
    @pyqtSlot()
    def on_actionArchivage_triggered(self):
        """
        Slot documentation goes here.
        """
        
        
        self.db.validation_ce(self.n_ce_pour_modification)
        
        self.nettoyage_gui()
        
        self.n_ce_pour_modification = ""
        
        self.actionEnregistrement.setEnabled(True)
        self.actionArchivage.setEnabled(False)
        self.actionMise_jour.setEnabled(False)
        
        self.type_ouverture = 0
        
    def calcul_valeur_numerique_emt(self):
        '''calcul la valeur num emt'''
        #calcul valeur numerique de l'emt        
            
        
#        nom_doublespinbox_resolution = [self.doubleSpinBox_resolution, self.doubleSpinBox_resolution_2, 
#                                        self.doubleSpinBox_resolution_3]
#        nom_comboBox_EMT = [self.comboBox_EMT, self.comboBox_EMT_2, self.comboBox_EMT_3]
#        nom_lineEdit_moyenne_etalon = [self.lineEdit_moyenne_etalon, self.lineEdit_moyenne_etalon_2, 
#                                        self.lineEdit_moyenne_etalon_3]
        valeur_numerique_emt=[]
        list_line_edit_emt = [self.lineEdit_valeur_emt, self.lineEdit_valeur_emt_2, self.lineEdit_valeur_emt_3]
        for i in range(0, self.spinBox.value()):
            valeur_numerique_emt.append(list_line_edit_emt[i].text())
#            nom_doublespinbox_resolution[i].setDecimals(2) #permet de pas avoir de valeur float non exact sur spin box
#            resolution = str(nom_doublespinbox_resolution[i].value())
#            if resolution == "1.0":
#                resolution = "1."
#            elif  resolution == "2.0":
#                resolution = "2."
#            
#            
#            if self.comboBox_famille_afficheur.currentText() == "Sonde alarme température" or self.comboBox_famille_afficheur.currentText() == "Afficheur de température":
#                nom_brute_emt = nom_comboBox_EMT[i].currentText()
#                terme_emt = self.db.valeur_emt(nom_brute_emt)
#                terme_cte = float(terme_emt[0][0])
#                terme_variable = float(terme_emt[0][1])
#                
#                valeur_emt = float(float(nom_lineEdit_moyenne_etalon[i].text())) * (terme_variable/100) + terme_cte
#                conversion_b = str(valeur_emt)
##                valeur_emt_arrondie = decimal.Decimal(conversion_b).quantize(decimal.Decimal(resolution), rounding=decimal.ROUND_HALF_EVEN)
#            
#            elif self.comboBox_famille_afficheur.currentText() == "Afficheur de vitesse":
#                nom_brute_emt = nom_comboBox_EMT[i].currentText()
#                terme_emt = self.db.valeur_emt(nom_brute_emt)
#                terme_cte = float(terme_emt[0][0])
#                terme_variable = float(terme_emt[0][1])
#                
#                valeur_emt = float(float(nom_lineEdit_moyenne_etalon[i].text())) * (terme_variable/100) + terme_cte
#                conversion_b = str(valeur_emt)
##                valeur_emt_arrondie = decimal.Decimal(conversion_b).quantize(decimal.Decimal(resolution), rounding=decimal.ROUND_HALF_EVEN)
#            
#            elif self.comboBox_famille_afficheur.currentText() == "Afficheur de temps":
#                nom_brute_emt = nom_comboBox_EMT[i].currentText()
#                terme_emt = self.db.valeur_emt(nom_brute_emt)                
#                terme_cte = float(terme_emt[0][0])
#                terme_variable = float(terme_emt[0][1])
#                
#                valeur_emt = float(float(nom_lineEdit_moyenne_etalon[i].text())) * (terme_variable/100) + terme_cte
#                conversion_b = str(valeur_emt)
##                valeur_emt_arrondie = decimal.Decimal(conversion_b).quantize(decimal.Decimal(resolution), rounding=decimal.ROUND_HALF_EVEN)
            
#            valeur_numerique_emt.append(conversion_b)
            
#        print("terme_emt {}".format(valeur_numerique_emt))
        
        return valeur_numerique_emt
    

        
        
    
    @pyqtSlot(float)
    def on_doubleSpinBox_resolution_2_valueChanged(self, p0):
        """
        Slot documentation goes here.
        """
        self.calculs(self.tableWidget_2, self.lineEdit_moyenne_etalon_2, self.lineEdit_moyenne_etalon_2_arrondie, 
                        self.lineEdit_moyenne_afficheur_2, self.lineEdit_moyenne_afficheur_2_arrondie, 
                        self.lineEdit_correction_2, self.lineEdit_correction_2_arrondie, 
                        self.lineEdit_ecartype_2, self.lineEdit_incertitude_2, self.lineEdit_incertitude_2_arrondie, 
                        self.doubleSpinBox_resolution_2)
                        
        self.conformite(self.comboBox_EMT_2, self.lineEdit_correction_2, self.lineEdit_incertitude_2, 
                        self.lineEdit_conformite_2, self.doubleSpinBox_resolution_2, 
                        self.lineEdit_moyenne_etalon_2, self.textEdit_commentaire_conformite_2, self.lineEdit_valeur_emt_2)
    
    @pyqtSlot(float)
    def on_doubleSpinBox_resolution_3_valueChanged(self, p0):
        """
        Slot documentation goes here.
        """
        # TODO: not implemented yet
        self.calculs(self.tableWidget_3, self.lineEdit_moyenne_etalon_3,self.lineEdit_moyenne_etalon_3_arrondie,  
                        self.lineEdit_moyenne_afficheur_3, self.lineEdit_moyenne_afficheur_3_arrondie,  
                        self.lineEdit_correction_3, self.lineEdit_correction_3_arrondie, 
                        self.lineEdit_ecartype_3, self.lineEdit_incertitude_3, 
                        self.lineEdit_incertitude_3_arrondie, self.doubleSpinBox_resolution_3)
                        
        self.conformite(self.comboBox_EMT_3, self.lineEdit_correction_3, 
                        self.lineEdit_incertitude_3, self.lineEdit_conformite_3, 
                        self.doubleSpinBox_resolution_3, self.lineEdit_moyenne_etalon_3, 
                        self.textEdit_commentaire_conformite_3, self.lineEdit_valeur_emt_3)
    
    @pyqtSlot(float)
    def on_doubleSpinBox_resolution_valueChanged(self, p0):
        """
        Slot documentation goes here.
        """
        self.calculs(self.tableWidget, self.lineEdit_moyenne_etalon, self.lineEdit_moyenne_etalon_arrondie, 
                        self.lineEdit_moyenne_afficheur, self.lineEdit_moyenne_afficheur_arrondie, 
                        self.lineEdit_correction, self.lineEdit_correction_arrondie, 
                        self.lineEdit_ecartype, self.lineEdit_incertitude, self.lineEdit_incertitude_arrondie, 
                        self.doubleSpinBox_resolution)
                            
        self.conformite(self.comboBox_EMT, self.lineEdit_correction, 
                        self.lineEdit_incertitude, self.lineEdit_conformite, 
                        self.doubleSpinBox_resolution, self.lineEdit_moyenne_etalon, 
                        self.textEdit_commentaire_conformite, self.lineEdit_valeur_emt)
    
    @pyqtSlot()
    def on_actionModification_Afficheur_triggered(self):
        """
        Slot documentation goes here.
        """
        afficheurs = self.db.recensement_afficheurs_complet()    
        
        self.afficheur_a_modif = Select_afficheur(afficheurs)
#        afficheur = ""
        self.connect(self.afficheur_a_modif, SIGNAL("fermetureselectafficheur(PyQt_PyObject)"), self.modification_afficheur)
        self.afficheur_a_modif.setWindowModality(QtCore.Qt.ApplicationModal)
        self.afficheur_a_modif.show()
    
    def modification_afficheur(self, n_afficheur):
        '''fct appel la gui pour modif'''
        code_client = self.db.recuperation_code_client()
        constructeurs = self.db.recuperation_constructeurs()
        service = self.db.recuperation_service()
        
        
        caracteristique_afficheur = self.db.caract_afficheur_modif(n_afficheur)
        
        
        
        self.afficheur_a_modifier = Modification_afficheur(caracteristique_afficheur, 
                                                            code_client, constructeurs, service)
        
        self.connect(self.afficheur_a_modifier, SIGNAL("fermeturemodifafficheur(PyQt_PyObject)"), self.sauvegarde_modification_afficheur)
        
        self.afficheur_a_modifier.setWindowModality(QtCore.Qt.ApplicationModal)
        self.afficheur_a_modifier.show()
        
        
    def sauvegarde_modification_afficheur(self, afficheur):
        
        self.db.mise_a_jour_afficheur(afficheur)
    
    @pyqtSlot(int)
    def on_spinBox_2_valueChanged(self, p0):
        """
        Slot documentation goes here.
        """
        tableaux = [self.tableWidget, self.tableWidget_2, self.tableWidget_3]
        nbr_ligne_souhaite = self.spinBox_2.value()
        for i in range(len(tableaux)):
            nbr_ligne_tableau  = tableaux[i].rowCount()
            
            if nbr_ligne_tableau > nbr_ligne_souhaite:
                for j in range(nbr_ligne_tableau - nbr_ligne_souhaite):
                    tableaux[i].removeRow(nbr_ligne_tableau - j-1)
            elif nbr_ligne_tableau < nbr_ligne_souhaite:
                for j in range(nbr_ligne_souhaite - nbr_ligne_tableau):
                    tableaux[i].insertRow(nbr_ligne_tableau + j)
            elif nbr_ligne_tableau == nbr_ligne_souhaite:
                pass
    
    @pyqtSlot()
    def on_actionAnnule_et_Remplace_triggered(self):
        """
        Gestion des annule et remplace
        """
        self.type_ouverture = 1
        self.actionEnregistrement.setEnabled(True)
        self.actionMise_jour.setEnabled(False)
        self.actionArchivage.setEnabled(False)
        
        self.spinBox.setEnabled(True)
        self.spinBox_2.setEnabled(True)
        
        #recuperation des donnees
        num_ce = self.db.recuperation_n_ce()
        n_ce = QInputDialog.getItem(self, 
                       self.trUtf8("Numero certificats"), 
                       self.trUtf8("Choisir un numero"),
                       num_ce)

        if n_ce[1] == True:
            saisie = self.db.recuperation_etalonnage_saisie(n_ce[0])
            
            #affectation du n°ce sur la variable de classe pour mise à jour
            self.n_ce_annule_remplace = n_ce[0]
           
           #Appel fct de reaffectation des donnees
            self.reaffectation_donnees_saisie(saisie)   
        else:
            pass
    
    @pyqtSlot(int)
    def on_tabWidget_currentChanged(self, index):
        """
        Slot documentation goes here.
        """
        
        if self.tabWidget.currentIndex() != 0:
            
            if self.comboBox_type_rapport.currentText() == "*":
                QMessageBox.warning(self, 
                            self.trUtf8("Attention"), 
                            self.trUtf8("Merci de selectionner \n un type de rapport de mesure.")) 
    
    
    
            if self.lineEdit_site.text() == ""  or self.lineEdit_service.text() == "" :
                 QMessageBox.warning(self, 
                            self.trUtf8("Attention"), 
                            self.trUtf8("Merci de selectionner \n un afficheur.")) 
                
            if self.comboBox_ce_etal.currentText() == "":
                QMessageBox.warning(self, 
                            self.trUtf8("Attention"), 
                            self.trUtf8("Merci de selectionner \n un etalon et/ou son CE.")) 

