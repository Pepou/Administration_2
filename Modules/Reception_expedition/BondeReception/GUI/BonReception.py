# -*- coding: utf-8 -*-

"""
Module implementing Bon_Reception.
"""

from PyQt4.QtCore import pyqtSlot
from PyQt4.QtGui import QMainWindow
from PyQt4 import QtGui

from .Ui_BonReception import Ui_Bon_Reception
from Modules.Reception_expedition.BondeReception.Package.AccesBdd import AccesBdd
from PyQt4.QtGui import QStandardItemModel, QStandardItem 
from Modules.Reception_expedition.BondeReception.Package.Export_excel import Export_excel


class Bon_Reception(QMainWindow, Ui_Bon_Reception):
    """
    Class documentation goes here.
    """
    def __init__(self, engine,parent=None):
        """
        Constructor
        
        @param parent reference to the parent widget (QWidget)
        """
        super(Bon_Reception, self).__init__(parent)
        self.setupUi(self)
        self.comboBox_dates.hide()
        self.engine =engine
        
                #cte
        self.instruments_tries = {}
        self.adresse_client = {}
        
        #bdd
        self.db = AccesBdd(self.engine)
        liste_dates = self.db.recensement_dates_interventions()
        
        self.date_dernieres_reception = liste_dates[len(liste_dates)-1]
        print(self.date_dernieres_reception)
        
        self.affichage_instruments_expedies(self.date_dernieres_reception)
        
        #insertion combobox
        
        self.comboBox_dates.installEventFilter(self)
        model = QStandardItemModel()

        for i,word in enumerate(liste_dates):
            item = QStandardItem(word)
            model.setItem(i, 0, item)

        self.comboBox_dates.setModel(model)
        self.comboBox_dates.setModelColumn(0)
    
    @pyqtSlot()
    def on_radioButton_clicked(self):
        """
        Slot documentation goes here.
        """
        self.affichage_instruments_expedies(self.self.date_dernieres_reception)
    

    
    @pyqtSlot()
    def on_pushButton_export_clicked(self):
        """
        Slot documentation goes here.
        """
        BL = Export_excel()
        BL.export_bl(self.instruments_tries, self.adresse_client)
        
    @pyqtSlot(str)
    def on_comboBox_dates_activated(self, p0):
        """
        Slot documentation goes here.
        """
        date = self.comboBox_dates.currentText()
        self.affichage_instruments_expedies(date)
        
    
    def affichage_instruments_expedies(self, date):
        
        self.instruments_tries = {}
        self.adresse_client = {}
        nbr_ligne = self.tableWidget.rowCount()
        for i in range(nbr_ligne):
            self.tableWidget.removeRow(0)
        
        list_instruments_receptionnes= self.db.instruments_receptionnes(date)
#        print(list_instruments_receptionnes)
        
        for i in range(len(list_instruments_receptionnes)):
            self.tableWidget.insertRow(0)
            
            self.tableWidget.setItem(0, 0, QtGui.QTableWidgetItem(str(date)))
            self.tableWidget.setItem(0, 1, QtGui.QTableWidgetItem(str(list_instruments_receptionnes[i][1])))
            self.tableWidget.setItem(0, 2, QtGui.QTableWidgetItem(str(list_instruments_receptionnes[i][3])))
            self.tableWidget.setItem(0, 3, QtGui.QTableWidgetItem(str(list_instruments_receptionnes[i][4])))
            self.tableWidget.setItem(0, 4, QtGui.QTableWidgetItem(str(list_instruments_receptionnes[i][2])))




        tupple_site_service = set([(x[3], x[4]) for x in list_instruments_receptionnes])
        
        
        for site_service in tupple_site_service:
            instruments_receptionnes_tries = [x for x in list_instruments_receptionnes if x[3] == site_service[0] and x[4]== site_service[1]]
            
            if str(site_service[1]) == "None":
                nom = site_service[0]
            else:
                nom = site_service[0] +"_" + site_service[1]
            self.instruments_tries[str(nom)] = instruments_receptionnes_tries
            self.adresse_client[str(nom)] = self.db.adresse_client(instruments_receptionnes_tries[0][1])
#        print(self.adresse_client)
#        print(self.instruments_tries)






