#-*- coding: utf-8 -*-
from sqlalchemy import *
from sqlalchemy.orm import *
from sqlalchemy.engine import create_engine
#from PyQt4.QtGui import QMessageBox
#from PyQt4 import QtCore

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
        self.polynome_correction = Table('POLYNOME_CORRECTION', self.meta)
        self.connection = self.engine.connect()
        Session = sessionmaker(bind=self.engine)
        self.session = Session.configure(bind=self.engine)
        
        
    def __del__(self):
        self.connection.close()
    

    def resencement_instrument(self):
        '''retourne tous les identifications des instruments dans une list'''

        result = self.connection.execute('SELECT "IDENTIFICATION" FROM "INSTRUMENTS"')
        
        instruments = []        
        for ele in result:            
            instruments.append(ele[0]) #mise en forme
        return instruments
    
    
    
    def resencement_instrument_table_polynome_correction(self):
        '''retourne tous les identifications des instruments dans une list'''

        result = self.connection.execute('SELECT "IDENTIFICATION" FROM "POLYNOME_CORRECTION"')
        
        instruments = []        
        for ele in result:            
            instruments.append(ele[0]) #mise en forme
        return instruments
    
    
    def resencement_ce_ident_instrument_table_polynome_correction(self, ident_instrum):
        '''retourne tous les n °ce d'un instrument dans une list'''
            
        result = self.connection.execute('''SELECT "NUM_CERTIFICAT" FROM "POLYNOME_CORRECTION" WHERE "IDENTIFICATION" = '{}' ORDER BY "ID_POLYNOME"'''.format(ident_instrum))
        
        ce = []        
        for ele in result:            
            ce.append(ele[0]) #mise en forme
        return ce
    
    def renvoie_caracteristique_poly_n_ce(self, identification_instrument, n_ce):
        '''retourne les caracteristique polynome en fct n°CE'''
            
        result = self.connection.execute('''SELECT "DATE_ETAL","ORDRE_POLY","COEFF_A","COEFF_B","COEFF_C","ARCHIVAGE","ID_POLYNOME" FROM "POLYNOME_CORRECTION" WHERE "NUM_CERTIFICAT" = '{}' AND "IDENTIFICATION" = '{}' '''''.format(n_ce, identification_instrument))
    
               
        for ele in result: 
            carcat_poly = ele
#            ce.append(ele[0]) #mise en forme
        return carcat_poly
        
    def resencement_instrument_utilises(self):
        '''retourne tous les identifications des instruments utilisés dans une list'''

        result = self.connection.execute('''SELECT "IDENTIFICATION", "DOMAINE_MESURE", "DESIGNATION" FROM "INSTRUMENTS" WHERE "ETAT_UTILISATION" != 'Sommeil' AND "ETAT_UTILISATION" != 'Réformé' ''')
        
        instruments = []        
        for ele in result:            
            
            instruments.append(ele) #mise en forme

        return instruments
    
    def resencement_etalonnage_temp(self, date_debut, date_fin):
        '''retourne les etalonnages effectues entre deux dates dans une list'''

        result = self.connection.execute("""SELECT * FROM "ETALONNAGE_TEMP_ADMINISTRATION" WHERE "DATE_ETAL" >= '{}' AND "DATE_ETAL" <= '{}' ORDER BY "ID_ETAL" """.format(date_debut, date_fin))
        
        etalonnage_temp = []        
        for ele in result:            
            
            etalonnage_temp.append(ele) #mise en forme

        return etalonnage_temp
    

        
    def recuperation_donnees_etalonnage_n_ce(self, n_ce):
        '''fct qui va chercher dans la table etalonnage resultat les donnees de l'etalonnage'''
        
        
        result = self.connection.execute('''SELECT "MOYENNE_ETAL_C","MOYENNE_INSTRUM","MOYENNE_CORRECTION","U" FROM "ETALONNAGE_RESULTAT" WHERE "NUM_ETAL" = '{}' ORDER BY "ID_ETAL_RESULT" '''.format(n_ce))

        donnees_etal = []
        for ele in result:           
            donnees_etal.append(ele) 

        return donnees_etal
        

        
    def return_caracteristiques_intrument(self, identification_instrument):
        '''retourne certaines caracteristiques instrument
            constructeur
            reference_constructeur
            n_serie'''
#        try:
        result = self.connection.execute("""SELECT "CONSTRUCTEUR","REFERENCE_CONSTRUCTEUR","N_SERIE","RESOLUTION" FROM "INSTRUMENTS" WHERE "IDENTIFICATION" ='{}'""".format(identification_instrument))
        
        
        for ele in result:
            caract_instrument = ele
            
        return caract_instrument
#        except:
#            QMessageBox.critical(None, 
#                    QtCore.QObject.trUtf8(QtCore.QObject(None),"Instrument"), 
#                    QtCore.QObject.trUtf8(QtCore.QObject(None),"L'instrument est inconnu")) 
        
        
    def update_table_polynome(self, identification_instrument,  n_ce, donnees):
        '''fct qui mais à jour le poly dans la base '''
        
        #gestion archivage
        if donnees["ARCHIVAGE"] == False:            
            self.connection.execute("""UPDATE "POLYNOME_CORRECTION" SET "ARCHIVAGE" = TRUE """\
                                                    + """WHERE "IDENTIFICATION" ='{}' AND "NUM_CERTIFICAT"!= '{}' """.format(identification_instrument, n_ce))        
        else:
            pass
            
        #update poly
        self.connection.execute("""UPDATE "POLYNOME_CORRECTION" SET """\
                                                    + """"DATE_ETAL"= '{}', """.format(donnees["DATE_ETAL"])\
                                                    +""" "ARCHIVAGE"= '{}', """.format(donnees["ARCHIVAGE"])\
                                                    +""""ORDRE_POLY"= {},""".format(donnees["ORDRE_POLY"])\
                                                    +""" "COEFF_A" = {}, """.format(donnees["COEFF_A"]) \
                                                    +""" "COEFF_B" ={}, """.format(donnees["COEFF_B"])\
                                                    +""" "COEFF_C" = {},""".format(donnees["COEFF_C"]) \
                                                    +""" "RESIDU_MAX" = {},""".format(donnees["RESIDU_MAX"])\
                                                    +""" "MODELISATION" = {}""".format(donnees["MODELISATION"])\
                                                    + """WHERE "IDENTIFICATION" ='{}' AND "NUM_CERTIFICAT"= '{}' """.format(identification_instrument, n_ce))
        
    def insert_table_polynome(self,  donnees):
        '''fct qui insert le poly dans la base '''
        
        table = Table("POLYNOME_CORRECTION", self.meta)
        ins = table.insert(returning=[table.c.ID_POLYNOME])
        result = self.connection.execute(ins, donnees)

        id = []
        for ele in result:            
            id = ele          
        return id
        
    def insert_polynome_table_etalonnage(self,  donnees):
        '''fct qui insert les donnees de construction du poly dans la base '''

        table = Table("POLYNOME_TABLE_ETALONNAGE", self.meta)
        ins = table.insert()
        self.connection.execute(ins, donnees)


    def recuperation_donnees_table_polynome_table_etalonnage(self, id_poly):
        '''fct pour recuperer les donnnees dans la table polynome-table-etal'''
        
        table = Table("POLYNOME_TABLE_ETALONNAGE", self.meta)
        ins = select([table.c.MOYENNE_ETALON_CORRI, table.c.MOYENNE_INSTRUM, table.c.CORRECTION, table.c.INCERTITUDE]).where(table.c.ID_POLYNOME == id_poly).order_by(table.c.ID_POLY_TABLE_ETAL)
        result = self.connection.execute(ins)
        
        donnees_poly_table_etal = []        
        for ele in result:   
            donnees_poly_table_etal.append(ele) 
        
        return donnees_poly_table_etal
        
    def delete_table_polynome_table_etalonnage(self, id_poly):
        '''efface les lignes de la table polynome_donnees_etal'''
        table = Table("POLYNOME_TABLE_ETALONNAGE", self.meta)
        ins = table.delete(table.c.ID_POLYNOME == id_poly)
        self.connection.execute(ins)
        
