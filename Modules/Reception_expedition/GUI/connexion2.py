# -*- coding: utf-8 -*-

"""
Module implementing MainWindow.
"""

from PyQt4.QtCore import pyqtSlot
from PyQt4.QtGui import QMainWindow
from PyQt4.QtGui import QMessageBox
from GUI.Reception_Expedition import ReceptionExpedition
from GUI.Ui_connexion2 import Ui_MainWindow
from sqlalchemy import *
from sqlalchemy.orm import *
from sqlalchemy.engine import create_engine
import json



class Connexion(QMainWindow, Ui_MainWindow):
    """
    Class documentation goes here.
    """
    def __init__(self, parent=None):
        """
        Constructor
        
        @param parent reference to the parent widget (QWidget)
        """
        super().__init__(parent)
        self.setupUi(self)
        
        #connection
        self.password.returnPressed.connect(self.buttonBox_2.accepted)
        
        
        # fichier config bdd :
        with open("config_bdd.json") as json_file:
            config_bdd = json.load(json_file)
#            print(config_bdd)

        
        self.namebdd = config_bdd["name_bdd"] #Labo_Metro_Prod"#"Test_carac_generateurs"#"Labo_Metro_Prod"# #
        self.adressebdd = config_bdd["adresse_bdd"]#"10.42.1.74" #"localhost"  #"10.42.1.74"          
        self.portbdd = config_bdd["port_bdd"]

    
    @pyqtSlot()
    def on_buttonBox_2_accepted(self):
        """
        Connexion à la base
        """
        # acces à la BDD
#        try:

        # acces à la BDD
#        try:
        
        login = self.login.text()
        password = self.password.text()
        
#        db = GestionBdd('db', self.namebdd, self.adressebdd, self.portbdd, login, password)
#        connexion_laboTemp = db.premiere_connexion()
        
        
        self.engine = create_engine("postgresql+psycopg2://{}:{}@{}:{}/{}".format(login, password, self.adressebdd, self.portbdd, self.namebdd)) 
        self.meta = MetaData()        


        self.reception_expedition = ReceptionExpedition(self.engine)
        self.reception_expedition.showMaximized()
        self.close()    
        
#        return login, password
#        except exc.SQLAlchemyError:
#            QMessageBox.information(self, 
#                ("Erreur connexion "), 
#                ("Erreur sur le login et/ou mot de passe")) 
#            self.show()
#        



#        except:
#            QMessageBox.information(self, 
#                ("Erreur connexion "), 
#                ("Erreur sur le login et/ou mot de passe")) 
#            self.show()
#        

    
    @pyqtSlot()
    def on_buttonBox_2_rejected(self):
        """
        Slot documentation goes here.
        """
        # TODO: not implemented yet
        self.close()
