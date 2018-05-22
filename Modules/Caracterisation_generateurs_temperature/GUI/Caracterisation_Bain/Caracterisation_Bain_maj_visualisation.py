# -*- coding: utf-8 -*-

"""
Module implementing Caracterisation_Bain_Maj.
"""

from PyQt4.QtCore import pyqtSlot, SIGNAL, Qt
from PyQt4.QtGui import QMainWindow,  QTableWidgetItem, QFont, QMenu, QAction, QApplication, QMessageBox, QFileDialog
import numpy as np
from .Ui_Caracterisation_Bain_maj_visualisation import Ui_Caracterisation_Bain_Maj
from Modules.Caracterisation_generateurs_temperature.Package.AccesBdd_caracterisation_bain import AccesBdd_caracterisation_Bain

from Modules.Caracterisation_generateurs_temperature.Package.RapportCaracterisationBain import RapportCaracterisationBain

class Caracterisation_Bain_Maj(QMainWindow, Ui_Caracterisation_Bain_Maj):
    """
    Class documentation goes here.
    
    """    
#    visualisation = True
    
    def __init__(self,  engine, meta, id, visualisation = True,  parent=None):
        """
        Constructor
        
        @param parent reference to the parent widget (QWidget)
        """
        super(Caracterisation_Bain_Maj, self).__init__(parent)
        self.setupUi(self)
        self.visualisation = visualisation
        self.nb_temp_stab = self.spinBox_nb_temp_stab.value()
#        print(self.nb_temp_stab)

        self.engine = engine
        self.meta = meta
        self.remplissage_combobox()
        
        self.id_caract =int(id)
        self.lineEdit_id_carac.setText(id)
        
        
        self.onglet_admin()
        self.onglet_stab()
        self.onglet_hom()
        
        if self.visualisation == True:
            self.menuBar.hide()
            self.spinBox_n_temp_hom.setMaximum(self.nb_temp_hom)
            self.setWindowTitle ("Visualisation")
        else:
            self.menuBar.show()
            
        
        
        
        
        
        
    def remplissage_combobox(self):
        self.db_carac = AccesBdd_caracterisation_Bain(self.engine, self.meta)
        
        self.generateurs = self.db_carac.generateurs_liquide()
        self.comboBox_ident_generateur.addItems([x[1] for x in self.generateurs]) #nom generateur
        
        self.operateurs = self.db_carac.techniciens()

        self.comboBox_operateur.addItems([x[1] for x in self.operateurs]) #visa operateurs
    
    def onglet_admin(self):
        
        self.sauvegarde_admin = {}
        admin = next(self.db_carac.recup_caracterisation_generateurs_admin(self.id_caract))

        id_generateur = admin[1]
        nom_generateur = next(x[1] for x in self.generateurs if x[0] == id_generateur)
        index = self.comboBox_ident_generateur.findText(nom_generateur)
        self.comboBox_ident_generateur.setCurrentIndex(index)
        self.on_comboBox_ident_generateur_currentIndexChanged(index)
        
        date= admin[2]
        self.dateEdit.setDate(date)
        
        type_caract = admin[4]
        index = self.comboBox_type_caracterisation.findText(type_caract)
        self.comboBox_type_caracterisation.setCurrentIndex(index)
        
        index_operateur = admin[3]
        nom_operateur = next(x[1] for x in self.operateurs if x[0] == index_operateur)
        index = self.comboBox_operateur.findText(nom_operateur)
        self.comboBox_operateur.setCurrentIndex(index)
        
        commentaire = admin[5]
        self.textEdit_commentaire.setText(commentaire)
        
        fluide =admin[9]
        if fluide :
            index = self.comboBox_fluide.findText(fluide)
            self.comboBox_fluide.setCurrentIndex(index)
        
        reglage = admin[10]
        self.textEdit_reglage_spe.setText(reglage)

        #gestion moyens de mesure
        self.on_pushButton_gui_moyens_caract_clicked()
        #remplissage tableau
        moyens = next(self.db_carac.recup_caracterisation_moyens_utilises(self.id_caract)) 
        nom_moyens = [x[1] for x in (self.etalons + self.sondes_centrales) if x[0] in moyens]
        for ele in nom_moyens:
            self.comboBox_ident_sonde_stabi.addItem(ele)
            
            if ele in [x[1] for x in self.sondes_centrales]:
                self.tableWidget_moyens_select.insertRow(0)
                item_nom = QTableWidgetItem(str(ele))
                item_n_serie =   QTableWidgetItem(str([x[4] for x in self.centrales if x[0] == 
                                                                     [x[6] for x in self.sondes_centrales if x[1] == ele][0]][0]))
                item_id = QTableWidgetItem(str([x[0] for x in self.sondes_centrales if x[1] == ele][0]))
            
                self.tableWidget_moyens_select.setItem(0,0, item_nom)
                self.tableWidget_moyens_select.setItem(0, 1, item_n_serie)
                self.tableWidget_moyens_select.setItem(0,2,  item_id)
            
            else:
                self.tableWidget_moyens_select.insertRow(0)
                item_nom = QTableWidgetItem(str(ele))
                item_n_serie =   QTableWidgetItem(str([x[4] for x in self.etalons if x[1] == ele][0]))
                item_id = QTableWidgetItem(str([x[0] for x in self.etalons if x[1] == ele][0]))
            
                self.tableWidget_moyens_select.setItem(0,0, item_nom)
                self.tableWidget_moyens_select.setItem(0, 1, item_n_serie)
                self.tableWidget_moyens_select.setItem(0,2,  item_id)
                
            if self.tableWidget_moyens_select.rowCount()>=2:
                for ligne_table in range(2):
                    nom = self.tableWidget_moyens_select.item(ligne_table, 0).text()
                    self.comboBox_ident_sonde_stabi.addItem(nom)
    
                    for ligne in range(8):
                        coeff = 11* ligne
                        item_min_1 = QTableWidgetItem(nom)                               
                        self.tableWidget_hom.setItem(2 + coeff, (ligne_table+1), item_min_1)
                        
                        item_min_2 = QTableWidgetItem(nom)                               
                        self.tableWidget_hom.setItem(2 + coeff, (4+ ligne_table), item_min_2)

        
    @pyqtSlot(int)
    def on_comboBox_ident_generateur_currentIndexChanged(self, index):
        """
        Fct qui va remplir les linedit en rapport avec le generateur carcaterisé self.generateur = 
        [table.c.ID_INSTRUM, table.c.IDENTIFICATION,table.c.CONSTRUCTEUR, table.c.REFERENCE_CONSTRUCTEUR, \
                            table.c.N_SERIE, table.c.ETAT_UTILISATION]
        """
        nom_generateur_select =self.comboBox_ident_generateur.currentText()
        self.id_generateur = next((x[0] for x in self.generateurs if x[1] == nom_generateur_select))

        marque = next((x[2] for x in self.generateurs if x[1] == nom_generateur_select))
        self.lineEdit_marque.setText(marque)
        
        model = next((x[3] for x in self.generateurs if x[1] == nom_generateur_select))
        self.lineEdit_model.setText(model)
        
        n_serie = next((x[4] for x in self.generateurs if x[1] == nom_generateur_select))
        self.lineEdit_n_serie.setText(n_serie)
        

    @pyqtSlot()
    def on_pushButton_gui_moyens_caract_clicked(self):
        """
        Slot documentation goes here.
        """
        self.etalons= self.db_carac.etalons()
        self.centrales = self.db_carac.centrales()
        self.sondes_centrales = self.db_carac.sondes_centrales()
        
        moyens = next(self.db_carac.recup_caracterisation_moyens_utilises(self.id_caract)) # on recupere ce que l'on doit cocher c'est une list
        nom_moyens = [x[1] for x in (self.etalons + self.sondes_centrales) if x[0] in moyens]
#        print(nom_moyens)

        self.menu =  QMenu(self)
        for ele in ([x[1] for x in self.etalons] + [x[1] for x in self.centrales]):
            if ele in [x[1] for x in self.centrales]:
                self.Act1 = QAction(ele, self.menu)
                self.Act1.setCheckable(True)
                
                if ele in nom_moyens: #gestion des moyens de mesures
                    self.Act1.setChecked (True)
#                    self.gestion_select(ele)                   
                
                
                self.sous_menu = QMenu(self)                
                id_centrale = next(x[0] for x in self.centrales if x[1] == ele)
                sondes_a_afficher = [x[1] for x in self.sondes_centrales if x[6] == id_centrale]

                for sondes in sondes_a_afficher:
                    self.sous_act =QAction(sondes, self.sous_menu)
                    self.sous_act.setCheckable(True)   
                    
                    if sondes in nom_moyens : #gestion de sonde utilisés
                        self.sous_act.setChecked (True)
#                        self.gestion_select(ele)
                        
                    self.sous_menu.addAction(self.sous_act)

                self.Act1.setMenu(self.sous_menu)
  
            else:
                self.Act1 = QAction(ele, self.menu)
                self.Act1.setCheckable(True)
                if ele in nom_moyens: #gestion des moyens de mesures
                    self.Act1.setChecked (True)
                    
                    
                
                
            self.menu.addAction(self.Act1)

        self.pushButton_gui_moyens_caract.setMenu(self.menu)
        self.menu.triggered.connect(self.gestion_select)
    
    def gestion_select(self, value):
        """ fct qui gere le tableau select mesure : ajoute une ligne si coché et enleve la ligne sinon
            gere la mise en place combobox etalon pour stab
            et la repartition des sondes pour l'homogeneité
            """
#        print("value check {}".format(value.text()))
        if value.isChecked():
            if value.text() in [x[1] for x in self.sondes_centrales]:
                self.tableWidget_moyens_select.insertRow(0)
                item_nom = QTableWidgetItem(str(value.text()))
                item_n_serie =   QTableWidgetItem(str([x[4] for x in self.centrales if x[0] == 
                                                                     [x[6] for x in self.sondes_centrales if x[1] == value.text()][0]][0]))
                item_id = QTableWidgetItem(str([x[0] for x in self.sondes_centrales if x[1] == value.text()][0]))
            
                self.tableWidget_moyens_select.setItem(0,0, item_nom)
                self.tableWidget_moyens_select.setItem(0, 1, item_n_serie)
                self.tableWidget_moyens_select.setItem(0,2,  item_id)
            
            else:
                self.tableWidget_moyens_select.insertRow(0)
                item_nom = QTableWidgetItem(str(value.text()))
                item_n_serie =   QTableWidgetItem(str([x[4] for x in self.etalons if x[1] == value.text()][0]))
                item_id = QTableWidgetItem(str([x[0] for x in self.etalons if x[1] == value.text()][0]))
            
                self.tableWidget_moyens_select.setItem(0,0, item_nom)
                self.tableWidget_moyens_select.setItem(0, 1, item_n_serie)
                self.tableWidget_moyens_select.setItem(0,2,  item_id)
#            
        else:
            nbr_ligne =self.tableWidget_moyens_select.rowCount()
            ligne_a_supp = next(ligne for ligne in range(nbr_ligne) 
                                        if  self.tableWidget_moyens_select.item(ligne, 0).text() == value.text()) 

            self.tableWidget_moyens_select.removeRow(ligne_a_supp)

        self.comboBox_ident_sonde_stabi.clear()
#       
        if self.tableWidget_moyens_select.rowCount()>=2:
            for ligne_table in range(2):
                nom = self.tableWidget_moyens_select.item(ligne_table, 0).text()
                self.comboBox_ident_sonde_stabi.addItem(nom)
    
                for ligne in range(8):
                    coeff = 11* ligne
                    item_min_1 = QTableWidgetItem(nom)                               
                    self.tableWidget_hom.setItem(2 + coeff, (ligne_table+1), item_min_1)
                    
                    item_min_2 = QTableWidgetItem(nom)                               
                    self.tableWidget_hom.setItem(2 + coeff, (4+ ligne_table), item_min_2)
                    
                    
    
    
    def keyPressEvent(self, event):
        """gestion du copier coller dans le tableau homogeneite"""
       
        items_tableWidget_hom = self.tableWidget_hom.selectedIndexes()
        items_tableWidget_stab = self.tableWidget_stab.selectedIndexes()
        clavier = event.key()
        
        if len(items_tableWidget_hom) != 0 and self.tabWidget.currentIndex() == 2:
            list_n_ligne = list(set([item.row() for item in items_tableWidget_hom]))
            list_n_ligne.sort()
            list_n_colonne = list(set([item.column() for item in items_tableWidget_hom]))
            list_n_colonne.sort()
            nbr_ligne_select = len(list_n_ligne)
            nbr_colonne_select = len(list_n_colonne)
                            
            if clavier == 86: #"86: correspond à ctrl+V
                presse_papier =  QApplication.clipboard()

                read_press_papier = presse_papier.text()
                press_papier_list = read_press_papier.split("\n")
                list_donnees = [tuple(x.split("\t")) for x in press_papier_list if x] 

                nbr_ligne_a_copier = len(list_donnees) 
                nbr_colonne_a_copier = len(list_donnees[0])
                
                if nbr_ligne_a_copier>= nbr_ligne_select and nbr_colonne_a_copier>= nbr_colonne_select:
                    for l in  range(nbr_ligne_select):
                        for c in range(nbr_colonne_select):
                                                 
                            ligne =list_n_ligne[l]
                            colonne = list_n_colonne[c]

                            if colonne in  [1, 2, 4, 5]:
                                item = QTableWidgetItem(str(list_donnees[l][c].replace(",", ".")))                               
                                self.tableWidget_hom.setItem(ligne, colonne, item)
                else:
                    for nbr in  range(nbr_ligne_a_copier):
                        ligne = items_tableWidget_hom[nbr].row()
                        colonne = items_tableWidget_hom[nbr].column()
                        
                        item = QTableWidgetItem(str(press_papier_list[nbr].replace(",", ".")))                               
                        self.tableWidget_hom.setItem(ligne, colonne, item)
            
        elif len(items_tableWidget_stab) != 0 and self.tabWidget.currentIndex() == 1:
            list_n_ligne = list(set([item.row() for item in items_tableWidget_stab]))
            list_n_colonne = list(set([item.column() for item in items_tableWidget_stab]))
            nbr_ligne_select = len(list_n_ligne)
            nbr_colonne_select = len(list_n_colonne)
                            
            if clavier == 86: #"86: correspond à ctrl+V
                presse_papier =  QApplication.clipboard()

                read_press_papier = presse_papier.text()
                press_papier_list = read_press_papier.split("\n")
                list_donnees = [tuple(x.split("\t")) for x in press_papier_list if x] #
#                print(list_donnees)

                nbr_ligne_a_copier = len(list_donnees) 
                nbr_colonne_a_copier = len(list_donnees[0])
                
                if nbr_ligne_a_copier>= nbr_ligne_select and nbr_colonne_a_copier>= nbr_colonne_select:
                    for l in  range(nbr_ligne_select):
                        for c in range(nbr_colonne_select):                        
                            ligne =list_n_ligne[l]
                            colonne = list_n_colonne[c]

                            if colonne in  [0, 1, 2]:
                                item = QTableWidgetItem(str(list_donnees[l][c].replace(",", ".")))                               
                                self.tableWidget_stab.setItem(ligne, colonne, item)
                else:
                    for nbr in  range(nbr_ligne_a_copier):
                        ligne = items_tableWidget_stab[nbr].row()
                        colonne = items_tableWidget_stab[nbr].column()
                        
                        item = QTableWidgetItem(str(press_papier_list[nbr].replace(",", ".")))                               
                        self.tableWidget_stab.setItem(ligne, colonne, item)
    
    
    
    def onglet_stab(self):
        """recupere et affiche les donnees dans l'onglet stab """
        
        self.sauvegarde_stab = {}
        stab = next(self.db_carac.recup_stab(self.id_caract))
#        print("stabe  {}".format(stab))
        gen_temp = (x for x in stab[6])
        nbr_temp = len(stab[6])
#        print(stab[6])
#        print("len {}".format(nbr_temp))
        gen_min = (x for x in stab[2])
        gen_max = (x for x in stab[3])
        
        self.spinBox_nb_temp_stab.setValue(nbr_temp)
        self.on_spinBox_nb_temp_stab_valueChanged(nbr_temp)
#        
        for ligne in range(nbr_temp):
            
            item_temp = QTableWidgetItem(str(next(gen_temp)))
            self.tableWidget_stab.setItem(ligne, 0, item_temp)
            
            item_min = QTableWidgetItem(str(next(gen_min)))
            self.tableWidget_stab.setItem(ligne, 1, item_min)
            
            item_max = QTableWidgetItem(str(next(gen_max)))
            self.tableWidget_stab.setItem(ligne, 2, item_max)
            
            
        #gestion moyen mesure 
        id= stab[5]
#        print("id instrum stab {}".format(id))
        if id in (x[0] for x in self.etalons):
            nom = next(x[1] for x in self.etalons if x[0] == id)
        else:
            nom = next(x[1] for x in self.sondes_centrales if x[0] == id)
            
#        print(nom)
        index = self.comboBox_ident_sonde_stabi.findText(nom)
        self.comboBox_ident_sonde_stabi.setCurrentIndex(index)
        
        
        
            
    @pyqtSlot(int, int)
    def on_tableWidget_stab_cellChanged(self, row, column):
        """
        Slot documentation goes here.
        """
        try:
            list_colonne_min_max = [1, 2]
            if column in list_colonne_min_max:
                if self.tableWidget_stab.item(row , 1):
                    min = float(self.tableWidget_stab.item(row , 1).text())                                
                else:
                    min = 0                
                if self.tableWidget_stab.item(row , 2):
                    max = float(self.tableWidget_stab.item(row, 2).text())                                
                else:
                    max = 0 
                delta = max-min
                
                item = QTableWidgetItem(str(delta.__format__(".4f")))            
                self.tableWidget_stab.setItem(row, 3, item)
                self.tableWidget_stab.item(row, 3).setBackground(Qt.gray)
                self.tableWidget_stab.item(row, 3).setTextAlignment(Qt.AlignVCenter | Qt.AlignHCenter)
                self.tableWidget_stab.item(row, 3).setFlags(Qt.ItemIsSelectable |Qt.ItemIsEnabled )
                self.tableWidget_stab.item(row , 3).setTextColor (Qt.red)
                font = QFont()
                font.setBold(True)
                self.tableWidget_stab.item(row, 3).setFont(font)
                
                list_delta = []
                for ligne in range(self.tableWidget_stab.rowCount()):
                    if  self.tableWidget_stab.item(ligne , 3):
                        list_delta.append(np.abs(float(self.tableWidget_stab.item(ligne , 3).text())))
                    else:
                        list_delta.append(0)
                        
                max_delta = np.amax(list_delta)
                self.lineEdit_stab_max.setText(str(max_delta.__format__(".4f")))
                
            #gestion sauvegarde
            nbr_de_ligne = self.tableWidget_stab.rowCount()
    
            temp = (self.tableWidget_stab.item(ligne, 0).text()  if self.tableWidget_stab.item(ligne, 0) else None for ligne in range(nbr_de_ligne))
    
            minimum= (float(self.tableWidget_stab.item(ligne, 1).text()).__format__ (".4f") if self.tableWidget_stab.item(ligne, 1) else None for ligne in range(nbr_de_ligne))
    
            maximum= (float(self.tableWidget_stab.item(ligne, 2).text()).__format__ (".4f") if self.tableWidget_stab.item(ligne, 2) else None for ligne in range(nbr_de_ligne))
    
            delta= (float(self.tableWidget_stab.item(ligne, 3).text()).__format__ (".4f") if self.tableWidget_stab.item(ligne, 3) else None for ligne in range(nbr_de_ligne))
    
            self.sauvegarde_stab["TEMP"] = temp
            self.sauvegarde_stab["MIN"] = minimum
            self.sauvegarde_stab["MAX"] = maximum
            self.sauvegarde_stab["DELTA"] = delta
    #        print( next(self.sauvegarde_stab["MIN"]))
            if  self.comboBox_ident_sonde_stabi.currentText() in (x[1]for x in self.etalons):
                id_sonde = next(x[0] for x in  self.etalons if x[1] == self.comboBox_ident_sonde_stabi.currentText())
            else:
                
                id_sonde = next(x[0] for x in self.sondes_centrales if x[1] == self.comboBox_ident_sonde_stabi.currentText())
    
            
            self.sauvegarde_stab["MOYEN_MESURE"] = id_sonde
        except:
            pass

        
    @pyqtSlot(int)
    def on_spinBox_nb_temp_stab_valueChanged(self, p0):
        """
        Slot documentation goes here.
        """
        if self.spinBox_nb_temp_stab.value() > self.nb_temp_stab:
            nbr_ligne_a_inserer = self.spinBox_nb_temp_stab.value() - self.nb_temp_stab
            
            for ligne in range(nbr_ligne_a_inserer):
                ligne_tableau_stab = self.tableWidget_stab.rowCount()
                self.tableWidget_stab.insertRow(ligne_tableau_stab - 1)
                
            self.nb_temp_stab = self.spinBox_nb_temp_stab.value()
            
        elif self.spinBox_nb_temp_stab.value() < self.nb_temp_stab:
            nbr_ligne_a_supp = self.nb_temp_stab - self.spinBox_nb_temp_stab.value() 
            
            for ligne in range(nbr_ligne_a_supp):
                ligne_tableau_stab = self.tableWidget_stab.rowCount()
                self.tableWidget_stab.removeRow(ligne_tableau_stab-1)
            self.nb_temp_stab = self.spinBox_nb_temp_stab.value()
#        
#       
    def onglet_hom(self):
        """gestion des donnees a afficher dans l'onglet hom"""
        
        self.sauvegarde_hom = {}
        self.sauvegarde_hom = self.db_carac.recup_caracterisation_bains_homogeneite(self.id_caract)
        self.nb_temp_hom = len(self.sauvegarde_hom)
        
        self.reaffectation_tab_hom()
        
    @pyqtSlot()
    def on_pushButton_pt_suivant_hom_clicked(self):
        """
        Slot documentation goes here.
        """
        n_pt_a_sauvegarder = self.spinBox_n_temp_hom.value()
        
        if self.visualisation !=True : 
            self.sauvegarde_onglet_hom(n_pt_a_sauvegarder)
    
            self.reaffectation_tab_hom(n_pt_a_sauvegarder + 1)
            self.spinBox_n_temp_hom.setValue(n_pt_a_sauvegarder + 1)
        else:
            if self.spinBox_n_temp_hom.value() < self.nb_temp_hom:
                self.reaffectation_tab_hom(n_pt_a_sauvegarder + 1)
                self.spinBox_n_temp_hom.setValue(n_pt_a_sauvegarder + 1)

        
    @pyqtSlot()
    def on_pushButton_pt_precedent_hom_clicked(self):
        """
        Slot documentation goes here.
        """
        n_pt_a_sauvegarder = self.spinBox_n_temp_hom.value()
        
        if self.visualisation !=True :            
           
            self.sauvegarde_onglet_hom(n_pt_a_sauvegarder)
            self.reaffectation_tab_hom(n_pt_a_sauvegarder - 1)
            self.spinBox_n_temp_hom.setValue(n_pt_a_sauvegarder - 1)
            
        else:
            if self.spinBox_n_temp_hom.value() <= self.nb_temp_hom and self.spinBox_n_temp_hom.value()>1:
                self.reaffectation_tab_hom(n_pt_a_sauvegarder - 1)
                self.spinBox_n_temp_hom.setValue(n_pt_a_sauvegarder - 1)

    def sauvegarde_onglet_hom(self, n_pt = 1):
        """ fct qui enregistre le tableau à l'ecran
        chaque colonne est sauvegarde sous forme de generateurs:
        min_1 = generateur colonne 1 sur les min
        min_2 = generateur colonne 2 sur les min ...
        min_4 = colonne4
        max_1
        max_2 ...
        """
        
        min_1 = [float(self.tableWidget_hom.item(ligne, 1).text()).__format__ (".4f") if self.tableWidget_hom.item(ligne, 1) else None
                       for  ligne in range(4, 44, 11)]                       
        min_2 = [float(self.tableWidget_hom.item(ligne, 2).text()).__format__ (".4f") if self.tableWidget_hom.item(ligne, 2) else None
                       for  ligne in range(4, 44, 11)]        
        min_4 = [float(self.tableWidget_hom.item(ligne, 4).text()).__format__ (".4f") if self.tableWidget_hom.item(ligne, 4) else None
                       for  ligne in range(4, 44, 11)]        
        min_5 =[float(self.tableWidget_hom.item(ligne, 5).text()).__format__ (".4f") if self.tableWidget_hom.item(ligne, 5) else None
                       for  ligne in range(4, 44, 11)]
                       
        max_1 = [float(self.tableWidget_hom.item(ligne, 1).text()).__format__ (".4f") if self.tableWidget_hom.item(ligne, 1) else None
                       for  ligne in range(5, 44, 11)]
        max_2 = [float(self.tableWidget_hom.item(ligne, 2).text()).__format__ (".4f") if self.tableWidget_hom.item(ligne, 2) else None
                       for  ligne in range(5, 44, 11)]        
        max_4 = [float(self.tableWidget_hom.item(ligne, 4).text()).__format__ (".4f") if self.tableWidget_hom.item(ligne, 4) else None
                       for  ligne in range(5, 44, 11)]        
        max_5 = [float(self.tableWidget_hom.item(ligne, 5).text()).__format__ (".4f") if self.tableWidget_hom.item(ligne, 5) else None
                       for  ligne in range(5, 44, 11)]
                       
        moy_1 = [float(self.tableWidget_hom.item(ligne, 1).text()).__format__ (".4f") if self.tableWidget_hom.item(ligne, 1) else None
                       for  ligne in range(6, 44, 11)]
        moy_2 = [float(self.tableWidget_hom.item(ligne, 2).text()).__format__ (".4f") if self.tableWidget_hom.item(ligne, 2) else None
                       for  ligne in range(6, 44, 11)]        
        moy_4 = [float(self.tableWidget_hom.item(ligne, 4).text()).__format__ (".4f") if self.tableWidget_hom.item(ligne, 4) else None
                       for  ligne in range(6, 44, 11)]        
        moy_5 = [float(self.tableWidget_hom.item(ligne, 5).text()).__format__ (".4f") if self.tableWidget_hom.item(ligne, 5) else None
                       for  ligne in range(6, 44, 11)]               
                       
        s_1 = [float(self.tableWidget_hom.item(ligne, 1).text()).__format__ (".12f") if self.tableWidget_hom.item(ligne, 1) else None
                       for  ligne in range(7, 44, 11)]
        s_2 = [float(self.tableWidget_hom.item(ligne, 2).text()).__format__ (".12f") if self.tableWidget_hom.item(ligne, 2) else None
                       for  ligne in range(7, 44, 11)]        
        s_4 = [float(self.tableWidget_hom.item(ligne, 4).text()).__format__ (".12f") if self.tableWidget_hom.item(ligne, 4) else None
                       for  ligne in range(7, 44, 11)]        
        s_5 = [float(self.tableWidget_hom.item(ligne, 5).text()).__format__ (".12f") if self.tableWidget_hom.item(ligne, 5) else None
                       for  ligne in range(7, 44, 11)]              
                       
        
        delta_1 = [float(self.tableWidget_hom.item(ligne, 1).text()).__format__ (".4f") if self.tableWidget_hom.item(ligne, 1) else None
                       for  ligne in range(8, 44, 11)]
        delta_2 = [float(self.tableWidget_hom.item(ligne, 4).text()).__format__ (".4f") if self.tableWidget_hom.item(ligne, 4) else None
                       for  ligne in range(8, 44, 11)]
                       
        epsilone = [float(self.tableWidget_hom.item(ligne, 1).text()).__format__ (".12f") if self.tableWidget_hom.item(ligne, 1) else None
                       for  ligne in range(9, 44, 11)]
         
        epsilone_u = [float(self.tableWidget_hom.item(ligne, 1).text()).__format__ (".12f") if self.tableWidget_hom.item(ligne, 1) else None
                       for  ligne in range(10, 44, 11)]
        

        if self.lineEdit_temp_hom:
            temp = self.lineEdit_temp_hom.text()
        else:
            temp = None
        self.sauvegarde_hom[n_pt]= {"MIN_1": min_1, "MIN_2": min_2, "MIN_4": min_4, "MIN_5": min_5,
                                                 "MAX_1": max_1, "MAX_2": max_2, "MAX_4": max_4, "MAX_5": max_5,
                                                 "MOY_1": moy_1, "MOY_2": moy_2, "MOY_4": moy_4, "MOY_5": moy_5,
                                                 "S_1": s_1, "S_2": s_2, "S_4": s_4, "S_5": s_5,
                                                 "DELTA_1":delta_1, "DELTA_2":delta_2, 
                                                 "EPSILONE":epsilone, "EPSILONE_U":epsilone_u, 
                                                 "TEMPERATURE":temp.replace("°C", "")}
        
#        print(self.sauvegarde_hom[n_pt])
        self.tableWidget_hom.nettoyage()
        self.lineEdit_temp_hom.clear()
        self.tableWidget_hom.resizeColumnsToContents()

    
    def reaffectation_tab_hom(self, n_pt = 1):
        """fct, qui va réaffecter les donnees dans le tableau 
        donnéees sont dans self.sauvegarde_hom
        self.sauvegarde_hom[str(n_pt_a_sauvegarder)] = {1:
        {1: {'epsilone': ['0.000000000000', '0.000000000000', '0.000000000000', '0.000000000000'],
        'min_4': ['110.4616', '110.4616', '110.4616', '110.4616'], 'moy_1': ['110.4630', '110.4630', '110.4630', '110.4630'], 
        'max_5': ['110.4730', '110.4730', '110.4730', '110.4730'], 'max_2': ['110.4730', '110.4730', '110.4730', '110.4730'], 
        'Temp': '', 'moy_2': ['110.4718', '110.4718', '110.4718', '110.4718'], 
        'moy_4': ['110.4630', '110.4630', '110.4630', '110.4630'], 
        'delta_1': ['0.0088', '0.0088', '0.0088', '0.0088'], 
        'epsilone_u': ['0.001331665624', '0.001331665624', '0.001331665624', '0.001331665624'], 
        'min_5': ['110.4704', '110.4704', '110.4704', '110.4704'], 
        'delta_2': ['-0.0088', '-0.0088', '-0.0088', '-0.0088'], 
        'moy_5': ['110.4718', '110.4718', '110.4718', '110.4718'],
        'min_2': ['110.4704', '110.4704', '110.4704', '110.4704'], 
        's_1': ['0.0006', '0.0006', '0.0006', '0.0006'], 'max_4': ['110.4640', '110.4640', '110.4640', '110.4640'], 
        's_2': ['0.0006', '0.0006', '0.0006', '0.0006'], 'max_1': ['110.4640', '110.4640', '110.4640', '110.4640'], 
        's_4': ['0.0006', '0.0006', '0.0006', '0.0006'], 'min_1': ['110.4616', '110.4616', '110.4616', '110.4616'],
        's_5': ['0.0006', '0.0006', '0.0006', '0.0006']}
        2:}
        """
#        print("pt a reaffecter {}".format(n_pt))
        
        try:
#            print("sauvegarde {} pt {}".format(self.sauvegarde_hom[n_pt], n_pt))
            self.lineEdit_temp_hom.setText(self.sauvegarde_hom[n_pt]["TEMPERATURE"])
            
            indexe = 0
            for ligne in range(4, 44, 11):
                
                min_1  = self.sauvegarde_hom[n_pt]["MIN_1"][indexe]
                item = QTableWidgetItem(str(min_1))
                self.tableWidget_hom.setItem(ligne, 1, item)
                
                min_2  = self.sauvegarde_hom[n_pt]["MIN_2"][indexe]
                item = QTableWidgetItem(str(min_2))
                self.tableWidget_hom.setItem(ligne, 2, item)
                
                min_4  = self.sauvegarde_hom[n_pt]["MIN_4"][indexe]
                item = QTableWidgetItem(str(min_4))
                self.tableWidget_hom.setItem(ligne, 4, item)
                
                min_5  = self.sauvegarde_hom[n_pt]["MIN_5"][indexe]
                item = QTableWidgetItem(str(min_5))
                self.tableWidget_hom.setItem(ligne, 5, item)
                
                max_1  = self.sauvegarde_hom[n_pt]["MAX_1"][indexe]
                item = QTableWidgetItem(str(max_1))
                self.tableWidget_hom.setItem(ligne + 1 , 1, item)
                
                max_2  = self.sauvegarde_hom[n_pt]["MAX_2"][indexe]
                item = QTableWidgetItem(str(max_2))
                self.tableWidget_hom.setItem(ligne + 1, 2, item)
                
                max_4  = self.sauvegarde_hom[n_pt]["MAX_4"][indexe]
                item = QTableWidgetItem(str(max_4))
                self.tableWidget_hom.setItem(ligne + 1, 4, item)
                
                max_5  = self.sauvegarde_hom[n_pt]["MAX_5"][indexe]
                item = QTableWidgetItem(str(max_5))
                self.tableWidget_hom.setItem(ligne + 1 , 5, item)
                
                moy_1  = self.sauvegarde_hom[n_pt]["MOY_1"][indexe]
                item = QTableWidgetItem(str(moy_1))
                self.tableWidget_hom.setItem(ligne + 2 , 1, item)
                
                moy_2  = self.sauvegarde_hom[n_pt]["MOY_2"][indexe]
                item = QTableWidgetItem(str(moy_2))
                self.tableWidget_hom.setItem(ligne + 2, 2, item)
                
                moy_4  = self.sauvegarde_hom[n_pt]["MOY_4"][indexe]
                item = QTableWidgetItem(str(moy_4))
                self.tableWidget_hom.setItem(ligne + 2, 4, item)
                
                moy_5  = self.sauvegarde_hom[n_pt]["MOY_5"][indexe]
                item = QTableWidgetItem(str(moy_5))
                self.tableWidget_hom.setItem(ligne + 2, 5, item)
                
                s_1  = self.sauvegarde_hom[n_pt]["S_1"][indexe]
                item = QTableWidgetItem(str(s_1))
                self.tableWidget_hom.setItem(ligne + 3 , 1, item)
                
                s_2  = self.sauvegarde_hom[n_pt]["S_2"][indexe]
                item = QTableWidgetItem(str(s_2))
                self.tableWidget_hom.setItem(ligne + 3, 2, item)
                
                s_4  = self.sauvegarde_hom[n_pt]["S_4"][indexe]
                item = QTableWidgetItem(str(s_4))
                self.tableWidget_hom.setItem(ligne + 3, 4, item)
                
                s_5  = self.sauvegarde_hom[n_pt]["S_5"][indexe]
                item = QTableWidgetItem(str(s_5))
                self.tableWidget_hom.setItem(ligne + 3, 5, item)
                
                indexe +=1
                
    
                
            self.tableWidget_hom.resizeColumnsToContents()
        
        
        except KeyError:

            pass
            
            
    @pyqtSlot(int, int)
    def on_tableWidget_hom_cellChanged(self, row, column):
        """
        Slot documentation goes here.
        """
        try:
            self.tableWidget_hom.resizeColumnsToContents()
            list_moyenne = [(6, 1), (17, 1), (28, 1), (39, 1), 
                                    (6, 2), (17, 2), (28, 2), (39, 2), 
                                    (6, 4), (17, 4), (28, 4), (39, 4), 
                                    (6, 5), (17, 5), (28, 5), (39, 5)]
                                    
            list_ecartype = [(7, 1), (18, 1), (29, 1), (40, 1), 
                                    (7, 2), (18, 2), (29, 2), (40, 2), 
                                    (7, 4), (18, 4), (29, 4), (40, 4), 
                                    (7, 5), (18, 5), (29, 5), (40, 5)]
    
            
            if row in [x[0] for x in list_moyenne] :#or row in [x[0] for x in list_ecartype]:
                
                #calcul des deltas:
                if self.tableWidget_hom.item(row, 1):
                    m1 = float(self.tableWidget_hom.item(row, 1).text())                                
                else:
                    m1 = 0
                    
                if self.tableWidget_hom.item(row, 2):
                    m2 = float(self.tableWidget_hom.item(row, 2).text())                
                else:
                    m2 = 0
                    
                if self.tableWidget_hom.item(row, 5):
                    m3 = float(self.tableWidget_hom.item(row, 5).text())
                else:
                    m3 = 0
                    
                if self.tableWidget_hom.item(row, 4):
                    m4 = float(self.tableWidget_hom.item(row, 4).text())
                else:
                    m4 =0           
                
                
                #gestion ecart type
                if self.tableWidget_hom.item(row + 1, 1):
                        s1 = float(self.tableWidget_hom.item(row + 1, 1).text())
                else:
                        s1 = 0
                        
                if self.tableWidget_hom.item(row + 1, 2):
                        s2 = float(self.tableWidget_hom.item(row + 1, 2).text())
                else:
                        s2 = 0
                        
                if self.tableWidget_hom.item(row + 1, 5):
                        s3 = float(self.tableWidget_hom.item(row + 1, 5).text())
                else:
                        s3 = 0
                        
                if self.tableWidget_hom.item(row + 1, 4):
                        s4 = float(self.tableWidget_hom.item(row + 1, 4).text())
                else:
                        s4 = 0
                    
                delta_1 = m2 - m1
                delta_2 = m4 - m3
           
            
                epsilone = np.abs((delta_1 + delta_2)/2)        
                U_epsilone = np.sqrt(4*(np.power((0.001/(2*np.sqrt(3))), 2))+np.power(s1, 2)+np.power(s2, 2)+np.power(s3, 2)+np.power(s4, 2))            
                somme_epsilone_U = epsilone + U_epsilone
                
                
                #affichage des resultats dans le tableau
                item = QTableWidgetItem(str(delta_1.__format__(".4f")))
                self.tableWidget_hom.setItem(row +2, 1, item)
                self.tableWidget_hom.item(row +2, 1).setTextAlignment(Qt.AlignVCenter | Qt.AlignHCenter)
                self.tableWidget_hom.item(row +2, 1).setFlags(Qt.ItemIsSelectable |Qt.ItemIsEnabled )
                self.tableWidget_hom.item(row +2, 1).setTextColor (Qt.red)
                font = QFont()
                font.setBold(True)
                self.tableWidget_hom.item(row +2, 1).setFont(font)
                
                item = QTableWidgetItem(str(delta_2.__format__(".4f")))            
                self.tableWidget_hom.setItem(row +2, 4, item)
                self.tableWidget_hom.item(row +2, 4).setTextAlignment(Qt.AlignVCenter | Qt.AlignHCenter)
                self.tableWidget_hom.item(row +2, 4).setFlags(Qt.ItemIsSelectable |Qt.ItemIsEnabled )
                self.tableWidget_hom.item(row +2, 4).setTextColor (Qt.red)
                font = QFont()
                font.setBold(True)
                self.tableWidget_hom.item(row +2, 4).setFont(font)
                
                item = QTableWidgetItem(str(epsilone.__format__(".12f")))            
                self.tableWidget_hom.setItem(row +3, 1, item)
                self.tableWidget_hom.item(row +3, 1).setBackground(Qt.gray)
                self.tableWidget_hom.item(row +3, 1).setTextAlignment(Qt.AlignVCenter | Qt.AlignHCenter)
                self.tableWidget_hom.item(row +3, 1).setFlags(Qt.ItemIsSelectable |Qt.ItemIsEnabled )
                self.tableWidget_hom.item(row +3, 1).setTextColor (Qt.red)
                font = QFont()
                font.setBold(True)
                self.tableWidget_hom.item(row +3, 1).setFont(font)
                
                item = QTableWidgetItem(str(somme_epsilone_U.__format__(".12f")))            
                self.tableWidget_hom.setItem(row +4, 1, item)
                self.tableWidget_hom.item(row +4, 1).setBackground(Qt.gray)
                self.tableWidget_hom.item(row +4, 1).setTextAlignment(Qt.AlignVCenter | Qt.AlignHCenter)
                self.tableWidget_hom.item(row +4, 1).setFlags(Qt.ItemIsSelectable |Qt.ItemIsEnabled )
                self.tableWidget_hom.item(row +4, 1).setTextColor (Qt.red)
                font = QFont()
                font.setBold(True)
                self.tableWidget_hom.item(row +4, 1).setFont(font)
            
            elif row in [x[0] for x in list_ecartype]:            
                if self.tableWidget_hom.item(row , 1):
                        s1 = float(self.tableWidget_hom.item(row , 1).text())
                else:
                        s1 = 0
                        
                if self.tableWidget_hom.item(row , 2):
                        s2 = float(self.tableWidget_hom.item(row , 2).text())
                else:
                        s2 = 0
                        
                if self.tableWidget_hom.item(row , 5):
                        s3 = float(self.tableWidget_hom.item(row , 5).text())
                else:
                        s3 = 0
                        
                if self.tableWidget_hom.item(row , 4):
                        s4 = float(self.tableWidget_hom.item(row , 4).text())
                else:
                        s4 = 0
                #gestion des moyennes
                if self.tableWidget_hom.item(row - 1 , 1):
                    m1 = float(self.tableWidget_hom.item(row - 1, 1).text())                                
                else:
                    m1 = 0
                    
                if self.tableWidget_hom.item(row - 1, 2):
                    m2 = float(self.tableWidget_hom.item(row - 1, 2).text())                
                else:
                    m2 = 0
                    
                if self.tableWidget_hom.item(row - 1, 5):
                    m3 = float(self.tableWidget_hom.item(row- 1, 5).text())
                else:
                    m3 = 0
                    
                if self.tableWidget_hom.item(row - 1, 4):
                    m4 = float(self.tableWidget_hom.item(row - 1, 4).text())
                else:
                    m4 =0
                
                delta_1 = m2 - m1
                delta_2 = m4 - m3
           
                
                epsilone = np.abs((delta_1 + delta_2)/2)        
                U_epsilone = np.sqrt(4*(np.power((0.001/(2*np.sqrt(3))), 2))+np.power(s1, 2)+np.power(s2, 2)+np.power(s3, 2)+np.power(s4, 2))            
                somme_epsilone_U = epsilone + U_epsilone
                
                
                
                #affichage des resultats dans le tableau
                item = QTableWidgetItem(str(delta_1.__format__(".4f")))
                self.tableWidget_hom.setItem(row +1, 1, item)
                self.tableWidget_hom.item(row +1, 1).setTextAlignment(Qt.AlignVCenter | Qt.AlignHCenter)
                self.tableWidget_hom.item(row +1, 1).setFlags(Qt.ItemIsSelectable |Qt.ItemIsEnabled )
                self.tableWidget_hom.item(row +1, 1).setTextColor (Qt.red)
                font = QFont()
                font.setBold(True)
                self.tableWidget_hom.item(row +1, 1).setFont(font)
                
                item = QTableWidgetItem(str(delta_2.__format__(".4f")))            
                self.tableWidget_hom.setItem(row +1, 4, item)
                self.tableWidget_hom.item(row +1, 4).setTextAlignment(Qt.AlignVCenter | Qt.AlignHCenter)
                self.tableWidget_hom.item(row +1, 4).setFlags(Qt.ItemIsSelectable |Qt.ItemIsEnabled )
                self.tableWidget_hom.item(row +1, 4).setTextColor (Qt.red)
                font = QFont()
                font.setBold(True)
                self.tableWidget_hom.item(row +1, 4).setFont(font)
                
                item = QTableWidgetItem(str(epsilone.__format__(".12f")))            
                self.tableWidget_hom.setItem(row +2, 1, item)
                self.tableWidget_hom.item(row +2, 1).setBackground(Qt.gray)
                self.tableWidget_hom.item(row +2, 1).setTextAlignment(Qt.AlignVCenter | Qt.AlignHCenter)
                self.tableWidget_hom.item(row +2, 1).setFlags(Qt.ItemIsSelectable |Qt.ItemIsEnabled )
                self.tableWidget_hom.item(row +2, 1).setTextColor (Qt.red)
                font = QFont()
                font.setBold(True)
                self.tableWidget_hom.item(row +2, 1).setFont(font)
                
                item = QTableWidgetItem(str(somme_epsilone_U.__format__(".12f")))            
                self.tableWidget_hom.setItem(row + 3, 1, item)
                self.tableWidget_hom.item(row + 3, 1).setBackground(Qt.gray)
                self.tableWidget_hom.item(row +3, 1).setTextAlignment(Qt.AlignVCenter | Qt.AlignHCenter)
                self.tableWidget_hom.item(row +3, 1).setFlags(Qt.ItemIsSelectable |Qt.ItemIsEnabled )
                self.tableWidget_hom.item(row +3, 1).setTextColor (Qt.red)
                font = QFont()
                font.setBold(True)
                self.tableWidget_hom.item(row +3, 1).setFont(font)
        
        except ValueError : 
            pass
    
    @pyqtSlot()
    def on_actionMaj_triggered(self):
        """
        Slot documentation goes here.
        """
        n_pt_a_sauvegarder = self.spinBox_n_temp_hom.value()
        
        self.sauvegarde_onglet_hom(n_pt_a_sauvegarder)
        
        id_generateur = next((x[0] for x in  self.generateurs if x[1] == self.comboBox_ident_generateur.currentText()))
        self.sauvegarde_admin["ID_GENERATEUR"] = id_generateur
        
        id_operateur = next((x[0] for x in  self.operateurs if x[1] == self.comboBox_operateur.currentText()))
        self.sauvegarde_admin["OPERATEUR"] = id_operateur
        
        self.sauvegarde_admin["COMMENTAIRE"] = self.textEdit_commentaire.toPlainText ()
        self.sauvegarde_admin["ARCHIVAGE"] = False
        
        self.sauvegarde_admin["NBR_TEMP_STABILITE"] = self.tableWidget_stab.rowCount()
        self.sauvegarde_admin["NBR_TEMP_HOMOGENEITE"] = len(self.sauvegarde_hom)
        
        self.sauvegarde_admin["DATE"] = self.dateEdit.date().toString(Qt.ISODate)
        self.sauvegarde_admin["TYPE_CARACTERISATION"] = self.comboBox_type_caracterisation.currentText()
        
        self.sauvegarde_admin["FLUIDE"] = self.comboBox_fluide.currentText()
        self.sauvegarde_admin["REGLAGE"] = self.textEdit_reglage_spe.toPlainText()
        
        self.db_carac.caracterisation_generateurs_admin_update(self.id_caract, self.sauvegarde_admin)
        
        #####Gestion table resultats:
        delta_stab = [float(x) for x in self.sauvegarde_stab["DELTA"]]
        stab = np.amax(delta_stab)
                
        for ligne in range (self.tableWidget_stab.rowCount()):
            if float(self.tableWidget_stab.item(ligne, 3).text()) == stab:
                temp_stab = self.tableWidget_stab.item(ligne, 0).text().replace("°C", "")
                
        #hom max

        hom = [float(x) for pt in self.sauvegarde_hom.values() for x in pt["EPSILONE_U"]]

        if hom:
            hom_max = np.amax(hom)
        else: hom_max = 0
        #temperatur hom max
        temp_hom = None

        list_position = ["AG", "BH", "EC", "FD"]        
        position_hom = None
        
        for pt in self.sauvegarde_hom.values():
            if str(hom_max) in pt["EPSILONE_U"] and hom_max !=0:
                temp_hom = pt["TEMPERATURE"].replace("°C", "")
                index = pt["EPSILONE_U"].index(str(hom_max))
                position_hom = list_position[index]
                
            else : pass

        u_generateur  = np.sqrt(np.power((stab/(2*np.sqrt(3))), 2)+np.power((hom_max/np.sqrt(3)), 2))
        
        caracterisation_resultat = {"ID_CARACT": self.id_caract, "STABILITE": self.dateEdit.date(), 
                                               "STABILITE": stab,  "TEMP_STAB": temp_stab, 
                                               "HOMOGENEITE": hom_max, "POSIT_HOMOGENEITE": str(position_hom), 
                                               "TEMP_HOMOGENEITE": temp_hom, "u_generateur": u_generateur, 
                                               "ECART_TYPE": 0}

        self.db_carac. update_table_caracterisation_gen_resultats(self.id_caract, caracterisation_resultat)

        
        #table carcaterisation_moyens_utilises
        id_materiel_utilises= []
        list_nom = []
        for ligne in range(self.tableWidget_moyens_select.rowCount()):
            nom =self.tableWidget_moyens_select.item(ligne, 0).text()
            list_nom.append(nom)
            if  nom in (x[1]for x in self.etalons):
                id_sonde = next(x[0] for x in  self.etalons if x[1] == nom)
            else:            
                id_sonde = next(x[0] for x in self.sondes_centrales if x[1] == nom)
            id_materiel_utilises.append(id_sonde)
        
        caracterisation_moyens_utilises = {"ID_CARACTERISATION": self.id_caract, 
                                                           "ID_SONDES_CENTRALE": id_materiel_utilises}

        self.db_carac.caracterisation_generateurs_moyens_mesure_update(self.id_caract, caracterisation_moyens_utilises)
        
        ####table stab/hom

        list_sauvegarde_hom = []
        dic_hom_bdd = {}
        for ele in self.sauvegarde_hom.values():
            dic_hom_bdd = {}
#            print(ele)
            dic_hom_bdd["ID_CARAC"] = self.id_caract
            dic_hom_bdd["MIN_1"] = [float(x) for x in ele["MIN_1"]] 
            dic_hom_bdd["MIN_2"] = [float(x) for x in ele["MIN_2"]] 
            dic_hom_bdd["MIN_4"] = [float(x) for x in ele["MIN_4"]] 
            dic_hom_bdd["MIN_5"] = [float(x) for x in ele["MIN_5"]] 
            dic_hom_bdd["MAX_1"] = [float(x) for x in ele["MAX_1"]] 
            dic_hom_bdd["MAX_2"] = [float(x) for x in ele["MAX_2"]] 
            dic_hom_bdd["MAX_4"] = [float(x) for x in ele["MAX_4"]] 
            dic_hom_bdd["MAX_5"] = [float(x) for x in ele["MAX_5"]] 
            dic_hom_bdd["MOY_1"] = [float(x) for x in ele["MOY_1"]] 
            dic_hom_bdd["MOY_2"] = [float(x) for x in ele["MOY_2"]] 
            dic_hom_bdd["MOY_4"] = [float(x) for x in ele["MOY_4"]] 
            dic_hom_bdd["MOY_5"] = [float(x) for x in ele["MOY_5"]] 
            dic_hom_bdd["S_1"] = [float(x) for x in ele["S_1"]] 
            dic_hom_bdd["S_2"] = [float(x) for x in ele["S_2"]] 
            dic_hom_bdd["S_4"] = [float(x) for x in ele["S_4"]] 
            dic_hom_bdd["S_5"] = [float(x) for x in ele["S_5"]] 
            dic_hom_bdd["DELTA_1"] = [float(x) for x in ele["DELTA_1"]]  
            dic_hom_bdd["DELTA_2"] = [float(x) for x in ele["DELTA_2"]] 
            dic_hom_bdd["EPSILONE"] = [float(x) for x in ele["EPSILONE"]] 
            dic_hom_bdd["EPSILONE_U"] = [float(x) for x in ele["EPSILONE_U"]] 
            dic_hom_bdd["TEMPERATURE"] = ele["TEMPERATURE"].replace("°C", "")
            
            list_sauvegarde_hom.append(dic_hom_bdd)
            

        self.db_carac.caracterisation_bains_homogeneite_update(self.id_caract, list_sauvegarde_hom)
        
        stab_sauvegarde={"ID_CARAC" : self.id_caract, 
                                    "TEMPERATURE": [int(x.replace("°C", "")) for x in self.sauvegarde_stab["TEMP"]], 
                                    "MIN":[float(x) for x in self.sauvegarde_stab["MIN"]], 
                                    "MAX":[float(x) for x in self.sauvegarde_stab["MAX"]], 
                                    "DELTA" : delta_stab, 
                                    "MOYEN_MESURE":self.sauvegarde_stab["MOYEN_MESURE"]}

        self.db_carac.caracterisation_bains_stabilite_update(self.id_caract, stab_sauvegarde)
        
        self.spinBox_n_temp_hom.setValue(1)
        self.tabWidget.setCurrentIndex (0)
        
        reponse = QMessageBox.question(self, 
                                    self.trUtf8("Information"), 
                                    self.trUtf8("Voulez-vous creer un rapport de caracterisation"), 
                                    QMessageBox.Yes, QMessageBox.No)
                                    
        if reponse == QMessageBox.Yes:
            dossier = QFileDialog.getExistingDirectory(None ,  "Selectionner le dossier de sauvegarde des Rapports", 'y:/1.METROLOGIE/MATERIEL/1-GENERATEURS/AIR/')
            if dossier:
                
                nom_fichier = "caracterisation n"+ " " + str(self.id_caract) + " " + str(self.sauvegarde_admin["DATE"])
                
                Admin = {"NOM": self.comboBox_ident_generateur.currentText(), 
                               "N_SERIE": self.lineEdit_n_serie.text(), 
                               "MODEL": self.lineEdit_model.text(), 
                               "MARQUE": self.lineEdit_marque.text(), 
                               "OPERATEUR": self.comboBox_operateur.currentText(), 
                               "HUILE": self.comboBox_fluide.currentText(), 
                               "PB": self.textEdit_reglage_spe.toPlainText(), 
                               "SONDES" : list_nom, 
                               "DATE": self.sauvegarde_admin["DATE"], 
                               "COMMENTAIRE": self.textEdit_commentaire.toPlainText()}
                
                sauvegarde = {"RESULTATS":caracterisation_resultat, 
                                       "ADMIN": Admin, 
                                       "STAB": stab_sauvegarde, 
                                       "HOM": list_sauvegarde_hom}
                
                
                rapport = RapportCaracterisationBain(dossier, nom_fichier)
                rapport.mise_en_forme(sauvegarde )  
        
        #fermeture
        self.emit(SIGNAL("nouvellecaracterisation_bain(PyQt_PyObject)"),self )
        self.close()
