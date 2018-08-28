# -*- coding: utf-8 -*-

"""
Module implementing Bon_Livraison.
"""

from PyQt4.QtCore import pyqtSlot
from PyQt4.QtGui import QMainWindow

from .Ui_BonLivraison import Ui_Bon_Livraison
from PyQt4 import QtGui
from Modules.Reception_expedition.BondeLivraison.Package.AccesBdd import AccesBdd
from PyQt4.QtGui import QStandardItemModel, QStandardItem 
from Modules.Reception_expedition.BondeLivraison.Package.Export_excel import Export_excel

class Bon_Livraison(QMainWindow, Ui_Bon_Livraison):
    """
    Class documentation goes here.
    """
    def __init__(self, engine, parent=None):
        """
        Constructor
        
        @param parent reference to the parent widget (QWidget)
        """
        super(Bon_Livraison, self).__init__(parent)
        self.setupUi(self)
        self.comboBox_dates.hide()
        
        self.engine =engine
        
        #cte
        self.instruments_tries = {}
        self.adresse_client = {}
        
        #bdd
        self.db = AccesBdd(self.engine)
        liste_dates = self.db.recensement_dates_interventions()
#        liste_dates.sort()
#        print(liste_dates)
        
        self.date_dernieres_expedition = liste_dates[len(liste_dates)-1]
#        print(self.date_dernieres_expedition)
        
        self.affichage_instruments_expedies(self.date_dernieres_expedition)
        
        #insertion combobox
        
        self.comboBox_dates.installEventFilter(self)
        model = QStandardItemModel()

        for i,word in enumerate(liste_dates):
            item = QStandardItem(word)
            model.setItem(i, 0, item)

        self.comboBox_dates.setModel(model)
        self.comboBox_dates.setModelColumn(0)
        
        
        
        
    @pyqtSlot(str)
    def on_comboBox_dates_activated(self, p0):
        """
        Slot documentation goes here.
        """
        date = self.comboBox_dates.currentText()
        self.affichage_instruments_expedies(date)
    
    @pyqtSlot()
    def on_pushButton_export_clicked(self):
        """
        Slot documentation goes here.
        """
        # TODO: not implemented yet
        BL = Export_excel()
        BL.export_bl(self.instruments_tries, self.adresse_client)#list_nom_onglet, instruments
        
        
    def affichage_instruments_expedies(self, date):
        
        self.instruments_tries = {}
        self.adresse_client = {}
        nbr_ligne = self.tableWidget.rowCount()
        for i in range(nbr_ligne):
            self.tableWidget.removeRow(0)
        
        list_instruments_expedies = self.db.instruments_expedies(date)
        
        print(f"date {date} instrum exped {list_instruments_expedies}")
        for i in range(len(list_instruments_expedies)):
            self.tableWidget.insertRow(0)
        
            self.tableWidget.setItem(0, 0, QtGui.QTableWidgetItem(str(date)))
            self.tableWidget.setItem(0, 1, QtGui.QTableWidgetItem(str(list_instruments_expedies[i][1])))
            self.tableWidget.setItem(0, 2, QtGui.QTableWidgetItem(str(list_instruments_expedies[i][5])))
            self.tableWidget.setItem(0, 3, QtGui.QTableWidgetItem(str(list_instruments_expedies[i][6])))
            self.tableWidget.setItem(0, 4, QtGui.QTableWidgetItem(str(list_instruments_expedies[i][2])))
            self.tableWidget.setItem(0, 5,  QtGui.QTableWidgetItem(str(list_instruments_expedies[i][3])))
            self.tableWidget.setItem(0, 6, QtGui.QTableWidgetItem(str(list_instruments_expedies[i][4])))
            
        #trie des instruments 

        tupple_site_service = set([(x[5], x[6]) for x in list_instruments_expedies])
        
        
        for site_service in tupple_site_service:
            instruments_expedies_tries = [x for x in list_instruments_expedies if x[5] == site_service[0] and x[6]== site_service[1]]
            
            if str(site_service[1]) == "None":
                nom = site_service[0]
            else:
                nom = site_service[0] +"_" + site_service[1]
            self.instruments_tries[str(nom)] = instruments_expedies_tries
            self.adresse_client[str(nom)] = self.db.adresse_client(instruments_expedies_tries[0][1])
   
    
    @pyqtSlot()
    def on_radioButton_clicked(self):
        """
        Slot documentation goes here.
        """
        self.affichage_instruments_expedies(self.date_dernieres_expedition)
