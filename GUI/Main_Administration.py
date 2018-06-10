# -*- coding: utf-8 -*-

"""
Module implementing MainWindow.
"""

from PyQt4.QtCore import pyqtSlot, pyqtSignal, QModelIndex
from PyQt4.QtGui import QMainWindow

from .Ui_Main_Administration import Ui_MainWindow
from Package.AccesBdd import Instrument, Intervention, Client, Secteur_exploitation, Poste_tech_sap
from Modules.Indicateurs.GUI.Indicateurs import Indicateur
from Modules.Afficheurs.GUI.afficheurs import Afficheurs

from Modules.Labo_Temp.IHM.Menu import Menu
from Modules.Labo_Temp.Package.GestionBdd import GestionBdd

from Modules.Synchronisation.GUI.Exploitation_enregistreurs import Exploitation_enregistreurs

from Modules.Caracterisation_generateurs_temperature.GUI.Main_Caracterisation import MainCaracterisation

from Modules.Consultation.GUI.Consultation_bdd import Consultation_Bdd

from Modules.Declaration_incertitudes.GUI.Main_Declaration_Incertitudes import MainDeclaration_Incertitudes

from Modules.Polynome.GUI.polynome import Polynome

from Modules.Cartographie.GUI.Main_Carto import Cartographie

from GUI.Instrument.Creation_Instruments import Creation_Instrument
from GUI.Instrument.Modification_Instrument import Modification_Instrument

from GUI.Clients.Creation_Client import Creation_Client
from GUI.Clients.Modification_Entite_Client import Modification_Entite_Client
from GUI.Clients.Modification_Site_Client import Modification_Site_Client

from Modules.Reception_expedition.GUI.Reception_Expedition import ReceptionExpedition

import pendulum
import warnings
import numpy as np


class MainWindow(QMainWindow, Ui_MainWindow):
    """
    Class documentation goes here.
    """
    
    signalMAJ_Site_Client = pyqtSignal(object)
    signalMAJ_Service_Client = pyqtSignal(object)
    signal_mise_a_dispo_client_efs = pyqtSignal(list)
    signal_mise_a_dispo_post_tech_sap_efs = pyqtSignal(list)
    signal_mise_a_dispo_poste_tech_efs = pyqtSignal(list)
    
    def __init__(self, engine, meta, login, password, parent=None):
        """
        Constructor
        
        @param parent reference to the parent widget (QWidget)
        """
        super().__init__(parent)
        self.setupUi(self)
        
#        print(f" mot de passe {self.password} login {self.login}")
        
        self.dateEdit.setDate(pendulum.now('Europe/Paris'))
        
        self.engine = engine
        self.meta = meta
        
        self.class_instrum = Instrument(self.engine)        
        self.parc = self.class_instrum.parc_complet()
#        self.parc["PERIODICITE_QUANTITE"].fillna('nan').astype(int)
        self.tableView_instruments.remplir(self.parc)
        
        class_intervention = Intervention(self.engine, self.meta)
        interventions = class_intervention.future_reception()
        self.tableView_reception.remplir(interventions.sort_values("DATE_PROCHAINE_INTERVENTION"))
        
        
        #ne sert que pour labo_temp
        self.login = login
        self.password = password
        
        #mise en place pour le tri
        self.comboBox_nom_colonne.addItems(list(self.parc))

    
    @pyqtSlot()
    def on_actionLaboTemp_triggered(self):
        """
        Slot documentation goes here.
        """
        db = GestionBdd('db')

        db.premiere_connexion(self.login, self.password)
        
        self.labotemp = Menu()
        self.labotemp.showMaximized()
    
    @pyqtSlot()
    def on_actionSynchronisation_enregisteurs_triggered(self):
        """
        Slot documentation goes here.
        """
        self.exploitation = Exploitation_enregistreurs(self.engine, self.meta)
        self.exploitation.show()
    
    @pyqtSlot()
    def on_actionCaracterisation_Generateurs_triggered(self):
        """
        Slot documentation goes here.
        """
        self.caracterisation = MainCaracterisation(self.engine,self.meta )
        self.caracterisation.showMaximized()
    
    @pyqtSlot()
    def on_actionAfficheurs_triggered(self):
        """
        Slot documentation goes here.
        """
        self.module_afficheur = Afficheurs(self.engine, self.meta)
#        self.caracterisation_bain = Caracterisation_Bain(self.engine,self.meta )
        
#        self.connect(self.caracterisation_bain, SIGNAL("nouvellecaracterisation_bain(PyQt_PyObject)"), self.initialisation)
        self.module_afficheur.showMaximized()
    
    @pyqtSlot()
    def on_actionIndicateurs_triggered(self):
        """
        Slot documentation goes here.
        """
        self.module_indicateur = Indicateur(self.engine, self.meta)
#        self.caracterisation_bain = Caracterisation_Bain(self.engine,self.meta )
        
#        self.connect(self.caracterisation_bain, SIGNAL("nouvellecaracterisation_bain(PyQt_PyObject)"), self.initialisation)
        self.module_indicateur.showMaximized()
#        self.module_indicateur.resize(100,100)
    
    @pyqtSlot()
    def on_actionCreation_triggered(self):
        """
        CREATION D INSTRUMENTS
        """
        
        self.instrument = Creation_Instrument(self.engine)
        self.instrument.signal_Creation_ok.connect(self.mise_a_jour_parc)
        self.instrument.showMaximized()
    
    
    
    @pyqtSlot()
    def on_actionModification_triggered(self):
        """
        Modification instrument
        """
        model = self.tableView_instruments.model()
        id = []
        for row in range(model.rowCount()):
#            for column in range(model.columnCount()):
            index = model.index(row, 0)
            id.append(int(model.data(index)))
#        print(id)
#        print(model.rowCount())
        instrument = self.parc.loc[self.parc["ID_INSTRUM"].isin(id)]
#        print(instrument)

        self.modif_instrument = Modification_Instrument(self.engine, instrument)
        self.modif_instrument.signal_modification_ok.connect(self.mise_a_jour_parc)
        self.modif_instrument.showMaximized()
        
        
    @pyqtSlot()
    def on_actionRecherche_triggered(self):
        """
        Slot documentation goes here.
        """
        # TODO: not implemented yet
        raise NotImplementedError
    
    @pyqtSlot()
    def on_actionCreation_2_triggered(self):
        """
        Slot Gere la creation et l'enregistrement d'un nouveau client
        """

        def table_sect_exploit_sap_bdd():
            """fct recoit le signal de demande secteur exploit de la gui client et
            renvoie la liste en emettant un signal a la gui"""            
            class_table = Secteur_exploitation(self.engine)
            colonne_complete = class_table.return_colonne_responsable()            
            self.signal_mise_a_dispo_client_efs.emit(colonne_complete)        
        
        def sauvegarde_new_client(client):
            """fct qui sauvegarde le nouveau client"""      
            new_client = Client(self.engine)
            new_client.ajouter_client(client)
            
        def mise_dispo_prefix_post_tech():
            """fct recoit le signal de demande poste tech de la gui client et
            renvoie la liste en emettant un signal a la gui""" 
        
        
        def table_postes_tech_sap():
            class_table = Poste_tech_sap(self.engine)
            colonne_complete = class_table.return_prefixe_colonne_poste_tech()            
            self.signal_mise_a_dispo_poste_tech_efs.emit(colonne_complete) 
        
        
        
        self.new_client = Creation_Client(self)
        
        self.new_client.signalNewclient.connect(sauvegarde_new_client)
        self.new_client.signalBesoinservices_efs.connect(table_sect_exploit_sap_bdd)
        
        self.new_client.signalBesoinpostetech_efs.connect(table_postes_tech_sap)

        self.new_client.show()
        
        
        
    
    
    @pyqtSlot()    
    def on_actionReception_Expedition_triggered(self):
        self.reception_expedition = ReceptionExpedition(self.engine)
        self.reception_expedition.showMaximized()
        
    
    @pyqtSlot()
    def on_actionModification_2_triggered(self):
        """
        Slot documentation goes here.
        """
        # TODO: not implemented yet
        raise NotImplementedError
    
    @pyqtSlot()
    def on_actionRecherche_2_triggered(self):
        """
        Slot documentation goes here.
        """
        # TODO: not implemented yet
        raise NotImplementedError
    
    @pyqtSlot()
    def on_actionCreer_triggered(self):
        """
        Slot documentation goes here.
        """
        # TODO: not implemented yet
        raise NotImplementedError
    
    @pyqtSlot()
    def on_actionModifier_triggered(self):
        """
        Slot documentation goes here.
        """
        # TODO: not implemented yet
        raise NotImplementedError
    
    @pyqtSlot()
    def on_actionAffecter_triggered(self):
        """
        Slot documentation goes here.
        """
        # TODO: not implemented yet
        raise NotImplementedError
    
    @pyqtSlot()
    def on_actionModifier_2_triggered(self):
        """
        Slot documentation goes here.
        """
        # TODO: not implemented yet
        raise NotImplementedError
    
    @pyqtSlot()
    def on_actionRechercher_triggered(self):
        """
        Slot documentation goes here.
        """
        # TODO: not implemented yet
        raise NotImplementedError
    
    @pyqtSlot()
    def on_actionPolynome_triggered(self):
        """
        Slot documentation goes here.
        """
        self.polynome = Polynome(self.engine, self.meta)
        self.polynome.showMaximized()
    
    @pyqtSlot()
    def on_actionConsultation_triggered(self):
        """
        Slot documentation goes here.
        """
        self.consultation_bdd = Consultation_Bdd(self.engine, self.meta)
        self.consultation_bdd.showMaximized()
    
    @pyqtSlot()
    def on_actionDeclaration_incertitudes_triggered(self):
        """
        Slot documentation goes here.
        """
        self.declaration_u = MainDeclaration_Incertitudes(self.engine,self.meta )
        self.declaration_u.showMaximized()
    
    @pyqtSlot()
    def on_actionEntite_Client_triggered(self):
        """
        Slot documentation goes here.
        """
        ensemble_client_modif = Client(self.engine)
        table_entite_client = ensemble_client_modif.ensemble_entites_clients()
        
        self.modif_entite_client = Modification_Entite_Client(table_entite_client)
        
        self.modif_entite_client.signalModif_Entite_Client.connect(self.modification_entite_client)

        self.modif_entite_client.show()
    
    def modification_entite_client(self, client):
        
        client_modif = Client(self.engine)
        client_modif.mise_a_jour_ent_client(client)
    
    @pyqtSlot()
    def on_actionSite_Client_triggered(self):
        """
        Gestion de la gui modification client
        """
        def table_postes_tech_sap():
            class_table = Poste_tech_sap(self.engine)
            colonne_complete = class_table.return_prefixe_colonne_poste_tech()            
            self.signal_mise_a_dispo_poste_tech_efs.emit(colonne_complete)
           
        def table_sect_exploit_sap_bdd():
            """fct recoit le signal de demande secteur exploit de la gui client et
            renvoie la liste en emettant un signal a la gui"""            
            class_table = Secteur_exploitation(self.engine)
            colonne_complete = class_table.return_colonne_responsable()            
            self.signal_mise_a_dispo_client_efs.emit(colonne_complete)
        
        def modification_service_client(service_dic):        
            service_modif = Client(self.engine)
            service_modif.mise_a_jour_service_client(service_dic)
            
            table_services_client = service_modif.ensemble_service_client()
            self.signalMAJ_Service_Client.emit(table_services_client)
        
        def ajout_service_client(service_dic ):
            service_new = Client(self.engine)
            service_new.ajout_service(service_dic)            
            table_services_client = service_new.ensemble_service_client()
            
            self.signalMAJ_Service_Client.emit(table_services_client)
           
        def modification_site_client(site):
        
            site_modif = Client(self.engine)
            site_modif.mise_a_jour_site_client(site)
    
            table_site_client = site_modif.ensemble_sites_clients()
    
            self.signalMAJ_Site_Client.emit(table_site_client)
            self.mise_a_jour_parc()
    
        def ajout_site_client(site):
        
            site_new = Client(self.engine)
            site_new.ajout_site(site)
    
            table_site_client = site_new.ensemble_sites_clients()
    
            self.signalMAJ_Site_Client.emit(table_site_client)
            
            self.mise_a_jour_parc()
        
        
        
        ensemble_sites_modif = Client(self.engine)
        table_entite_client = ensemble_sites_modif.ensemble_entites_clients()
        table_site_client = ensemble_sites_modif.ensemble_sites_clients()
        table_services_client = ensemble_sites_modif.ensemble_service_client()
        
        
        self.modif_site_client = Modification_Site_Client(self, table_entite_client, table_site_client, table_services_client )
        
        #connection des signaux
    
        self.modif_site_client.signalModif_Site_Client.connect(modification_site_client)        
        self.modif_site_client.signalAjout_Site_Client.connect(ajout_site_client)
        
        self.modif_site_client.signalModif_Service_Client.connect(modification_service_client)
        self.modif_site_client.signalAjout_Service_Client.connect(ajout_service_client)
        
        
        self.modif_site_client.signalBesoinservices_efs.connect(table_sect_exploit_sap_bdd)
        
        self.modif_site_client.signalBesoinpostetech_efs.connect(table_postes_tech_sap)
        

        self.modif_site_client.show()
    
    
#        print(service_dic)
    
    
    
#        print(service_dic)
    
    @pyqtSlot(str)
    def on_lineEdit_valeur_textChanged(self, p0):
        """
        Gestion du tri
        """
        warnings.filterwarnings("error")
        
        text = p0
#        print(p0)
        signe = self.comboBox_signe.currentText()
        nom_colonne = self.comboBox_nom_colonne.currentText()
        
        if text:
            if signe == "=":
                try:
#                    
                    tri = self.parc.loc[(self.parc[nom_colonne] == text)| 
                                        (self.parc[nom_colonne] == text.upper()) |
                                        (self.parc[nom_colonne] == text.capitalize())]
                    self.tableView_instruments.remplir(tri)

                except :
                    try:
                        tri = self.parc[self.parc[nom_colonne].astype(str) == text] #☺gestion des colonnes numeriques
                        self.tableView_instruments.remplir(tri)
                    except:
                        pass

            elif signe == "Contient":
#                try:
                    tri = self.parc[(self.parc[nom_colonne].astype(str).str.contains(text))|
                    (self.parc[nom_colonne].astype(str).str.contains(text.upper()))|
                    (self.parc[nom_colonne].astype(str).str.contains(text.capitalize()))]
                    
                    self.tableView_instruments.remplir(tri)
                    
#                except:                    
#                    pass
            
            elif signe == "<":
                try:
                    tri = self.parc[self.parc[nom_colonne] < float(text)]
                    self.tableView_instruments.remplir(tri)
                    
                except:
                    pass
                    
            elif signe == ">":
                try:
                    tri = self.parc[self.parc[nom_colonne] > float(text)]
                    self.tableView_instruments.remplir(tri)
#                    print(tri)
                except:
                   pass
        else:
            self.tableView_instruments.remplir(self.parc)
#            if tri:
#                self.tableView_instruments.remplir(tri)
    
    @pyqtSlot(int)
    def on_comboBox_signe_currentIndexChanged(self, index):
        """
        Slot documentation goes here.
        """
        text = self.lineEdit_valeur.text()
        self.on_lineEdit_valeur_textChanged(text)
    
    @pyqtSlot(int)
    def on_comboBox_nom_colonne_currentIndexChanged(self, index):
        """
        Slot documentation goes here.
        """
        text = self.lineEdit_valeur.text()
        self.on_lineEdit_valeur_textChanged(text)

    
    def mise_a_jour_parc(self):
#        print("coucou")
        self.parc = self.class_instrum.parc_complet()
        self.tableView_instruments.remplir(self.parc)
        
        self.on_groupBox_clicked()
    
    @pyqtSlot()
    def on_groupBox_clicked(self):
        """
        Slot documentation goes here.
        """
        if self.groupBox.isChecked():
            text = self.lineEdit_valeur.text()
            self.on_lineEdit_valeur_textChanged(text)
            
        else:
            self.on_lineEdit_valeur_textChanged("")
#        raise NotImplementedError
    
    @pyqtSlot()
    def on_actionCartographie_triggered(self):
        """
        Slot documentation goes here.
        """
        self.carto = Cartographie(self.engine)#Exploitation_Centrales(self.engine)
        self.carto.showMaximized()
