#-*- coding: utf-8 -*-
from sqlalchemy import *
from sqlalchemy.orm import *
from sqlalchemy.engine import create_engine


class AccesBdd_consultation():
    '''class gerant la bdd'''
    
    def __init__(self, engine, meta):

           
            #création de l'"engine"
        self.engine = engine 
        self.meta = meta        
        self.meta.reflect(bind=self.engine)
        
        self.connection = self.engine.connect()

        
        
    def __del__(self):
        self.connection.close()
        
        
    def generateurs(self):
        table = Table("INSTRUMENTS", self.meta)
        ins = select([table.c.ID_INSTRUM, table.c.IDENTIFICATION,table.c.CONSTRUCTEUR, table.c.REFERENCE_CONSTRUCTEUR, \
                            table.c.N_SERIE, table.c.ETAT_UTILISATION, table.c.DESIGNATION])\
                            .where(table.c.TYPE == "Generateur de Temperature")
        generateurs = self.connection.execute(ins).fetchall()
        return generateurs
    
    def techniciens(self):
        table = Table("TECHNICIEN", self.meta)
        ins = select([table.c.ID_TECHNICIEN, table.c.VISA])\
                            .where(table.c.ARCHIVAGE == False)
        techniciens = self.connection.execute(ins).fetchall()
        return techniciens
        
        
    def table_caracterisation_gen_admin(self):
        
        table = Table("CARACTERISATION_GENERATEURS_ADMIN", self.meta)
        ins = select([table.c.ID_CARAC, table.c.DATE, table.c.ID_GENERATEUR, table.c.OPERATEUR, table.c.COMMENTAIRE, \
                        table.c.NBR_TEMP_STABILITE, table.c.NBR_TEMP_HOMOGENEITE, table.c.ARCHIVAGE]).order_by(table.c.ID_CARAC)
                        
        caract_admin = self.connection.execute(ins).fetchall()
        return caract_admin
        
        
    def table_caracterisation_gen_resultats(self):
        table = Table("CARACTERISATION_RESULTATS", self.meta)
        ins = table.select().order_by(table.c.ID_RESULTS)
                        
        caract_resultats = self.connection.execute(ins).fetchall()
        return caract_resultats
        
        
      #########################################################################################  
        
    def recup_caracterisation_id (self, id_caract_admin, type_generateur):
        
        if type_generateur == "Enceinte":
        #table_caracterisation_gen_admin
            caracterisation_dictionnaire = {}
            table = Table("CARACTERISATION_GENERATEURS_ADMIN", self.meta)
            ins = table.select().where(table.c.ID_CARAC == id_caract_admin)
                            
            caract_admin = self.connection.execute(ins).fetchall()[0]
            
            dict_caract_admin = {"ID_CARACTERISATION": caract_admin[0], 
                                            "ID_GENERATEUR": caract_admin[1], 
                                            "DATE": caract_admin[2], "ID_OPERATEUR":caract_admin[3], 
                                            "COMMENTAIRE": caract_admin[5], 
                                            "ARCHIVAGE" : caract_admin[6], "NBR_TEMP_STABILITE": caract_admin[7], 
                                            "NBR_TEMP_HOMOGENEITE": caract_admin[8]}
                                            
            caracterisation_dictionnaire["ADMIN"] =   dict_caract_admin
#            print("admin {}".format(caracterisation_dictionnaire["ADMIN"]))
            
#            print("admin {}".format(caract_admin))
            
#            table = Table("CARACTERISATION_RESULTATS", self.meta)
#            ins = table.select().where(table.c.ID_CARACT == id_caract_admin)                            
#            caract_resultats = self.connection.execute(ins).fetchall()        
#            print("resultats {}".format(caract_resultats))
        
            table = Table("CARACTERISATION_ENCEINTES_MESURES", self.meta)
            ins = table.select().where(table.c.ID_CARACTERISATION == id_caract_admin).order_by(table.c.ID_MESURES)                            
            caract_mesures = self.connection.execute(ins).fetchall()#            
            caracterisation_dictionnaire["MESURES"] = caract_mesures
#            print("caract_mesures {}".format(caracterisation_dictionnaire["MESURES"]))
            
            table = Table("CARACTERISATION_MOYENS_UTILISES", self.meta)
            ins = table.select().where(table.c.ID_CARACTERISATION == id_caract_admin)                            
            caract_moyens_utilises = self.connection.execute(ins).fetchall()[0]
            dict_moyens_utilises ={"ID_ETALON": caract_moyens_utilises[2], "ID_CENTRALE" : caract_moyens_utilises[3], 
                                            "ID_SONDES_CENTRALES": caract_moyens_utilises[4], "ID_POLYNOME": caract_moyens_utilises[5], 
                                            "LISTE_U_ETALON": caract_moyens_utilises[6], "LISTE_U_CENTRALE" : caract_moyens_utilises[7]}
            
            caracterisation_dictionnaire["MOYENS_MESURE"] = dict_moyens_utilises
#            print("caract_moyens_utilises {}".format(caracterisation_dictionnaire["MOYENS_MESURE"]))
            
            
#            print("ensemble {}".format(caracterisation_dictionnaire))
        
            return caracterisation_dictionnaire
            
            
            
            
    def instruments(self):
        
        table = Table("INSTRUMENTS", self.meta)
        ins = select([table.c.IDENTIFICATION]).where(table.c.DOMAINE_MESURE == "Température")

        list_instruments = [inst[0] for inst in self.connection.execute(ins).fetchall()]  

#        print(list_instruments)
        
        return list_instruments
  

        
    def return_caract_instrum(self, ident):
        table = Table("INSTRUMENTS", self.meta)
        ins = select([table.c.CONSTRUCTEUR, table.c.N_SERIE, table.c.TYPE, table.c.RESOLUTION, table.c.COMMENTAIRE]).where(table.c.IDENTIFICATION == ident)
        carac =self.connection.execute(ins).fetchone()
        
#        print(carac)
        return carac
        
    def gestion_combobox_onglet_operateur(self):
        
        table = Table("TECHNICIEN", self.meta)
        ins = select([table.c.PRENOM]).order_by(table.c.ID_TECHNICIEN)
        operateur = self.connection.execute(ins).fetchall()
        
        return operateur
        
    def list_generateur(self):
        
        table = Table("INSTRUMENTS", self.meta)
        ins = select([table.c.IDENTIFICATION]).where(and_(or_(table.c.DESIGNATION == 'Bain de Glace Fondante', table.c.DESIGNATION == "Bain d'etalonnage",
                table.c.DESIGNATION == 'Enceinte climatique' ), table.c.ETAT_UTILISATION == 'En service'))
        
        list_generateur = [x[0] for x in self.connection.execute(ins).fetchall()]
        
#        print(list_generateur)
        
        return list_generateur
        
        
    def list_etalon(self):
        
        table = Table("INSTRUMENTS", self.meta)
        
        ins = select([table.c.IDENTIFICATION]).where(and_(table.c.DESIGNATION == 'Etalon',table.c.ETAT_UTILISATION == 'En service' )).order_by(table.c.ID_INSTRUM)
        list_etalon = [x[0] for x in self.connection.execute(ins).fetchall()]
        
        
        return list_etalon
        
        
        
        
        
    def id_poly(self, ref):
        
        table = Table("POLYNOME_CORRECTION", self.meta)
        ins = select([table.c.ID_POLYNOME]).where(and_(table.c.IDENTIFICATION == ref,table.c.ARCHIVAGE == False ))
        id = self.connection.execute(ins).fetchone()[0]
        
        return id
    
    def table_caracterisation_enceintes_mesures_stab_hom(self):
        
        table = Table("CARACTERISATION_ENCEINTES_MESURES", self.meta)
        ins = select([table.c.ID_CARACTERISATION, table.c.STABILITE, table.c.DELTA, table.c.TEMPERATURE])
                        
        caract_enceintes_mesures = self.connection.execute(ins).fetchall()
        return caract_enceintes_mesures
        
