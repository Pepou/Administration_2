#-*- coding: utf-8 -*-
from sqlalchemy import *
from sqlalchemy.orm import *
from sqlalchemy.engine import create_engine
import numpy as np

class AccesBdd():
    '''class gerant la bdd'''
    
    def __init__(self, engine, meta):
        
#        self.namebdd = "Labo_Metro_Prod"#"Labo_Metro_Test_2"##"Labo_Metro_Test"#
#        self.adressebdd = "10.42.1.74"#"localhost"#"10.42.1.74" # "localhost"   #"localhost"            
#        self.portbdd = "5432"
#        self.login = login
#        self.password = password
           
            #création de l'"engine"
        self.engine = engine #create_engine("postgresql+psycopg2://{}:{}@{}:{}/{}".format(self.login, self.password, self.adressebdd, self.portbdd, self.namebdd)) 
        self.meta = meta                
        self.meta.reflect(bind=self.engine)
        self.connection = self.engine.connect()
        Session = sessionmaker(bind=self.engine)
        self.session = Session.configure(bind=self.engine)
        
    def nom_tables(self):
        '''fct qui recuperes l'ensemble des noms des tables'''
        nom_tables = list(self.meta.tables.keys())
        nom_tables.sort()
        return nom_tables 
        
    def nom_colonnes(self, nom_table):
        table = Table(nom_table, self.meta)
        ins = table.select()
        result = self.connection.execute(ins)
        
        list_nom_colonnes =[]
        for nom_colonnes in result.keys():
            list_nom_colonnes.append(nom_colonnes)
            
        return list_nom_colonnes
    
    def recuperation_donnees_table(self, nom_table):
        '''fct qui recupere toutes les donnees d'une tables'''
        table = Table(nom_table, self.meta)
        ins = table.select()
        result = self.connection.execute(ins)
        
        donnees_table = []
        for row in result:
          donnees_table.append(row)
          
        return  donnees_table
