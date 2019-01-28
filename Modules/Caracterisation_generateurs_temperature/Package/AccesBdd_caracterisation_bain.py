#-*- coding: utf-8 -*-
from sqlalchemy import *
from sqlalchemy.orm import *
from sqlalchemy.engine import create_engine


class AccesBdd_caracterisation_Bain():
    '''class gerant la bdd'''
    
    def __init__(self, engine, meta):

           
            #création de l'"engine"
        self.engine = engine
        self.meta = meta 
        self.meta.reflect(bind=self.engine)
        
        self.connection = self.engine.connect()

        
        
    def __del__(self):
        self.connection.close()
        
        
    def generateurs_liquide(self):
        table = Table("INSTRUMENTS", self.meta)
        ins = select([table.c.ID_INSTRUM, table.c.IDENTIFICATION,table.c.CONSTRUCTEUR, table.c.REFERENCE_CONSTRUCTEUR, \
                            table.c.N_SERIE, table.c.ETAT_UTILISATION])\
                            .where(and_(table.c.TYPE == "Generateur de Temperature", or_(table.c.DESIGNATION == "Bain d'etalonnage", table.c.DESIGNATION == "Bain de Glace Fondante")))
        generateurs = self.connection.execute(ins).fetchall()
        
        return generateurs
        
        
    def etalons(self):
        table = Table("INSTRUMENTS", self.meta)
        ins = select([table.c.ID_INSTRUM, table.c.IDENTIFICATION,table.c.CONSTRUCTEUR, table.c.REFERENCE_CONSTRUCTEUR, \
                            table.c.N_SERIE, table.c.ETAT_UTILISATION])\
                        .where(and_(table.c.ETAT_UTILISATION == "En service", table.c.DESIGNATION == "Etalon"))
        etalons = self.connection.execute(ins).fetchall()
        return etalons
        
    def centrales(self):
        table = Table("INSTRUMENTS", self.meta)
        ins = select([table.c.ID_INSTRUM, table.c.IDENTIFICATION,table.c.CONSTRUCTEUR, table.c.REFERENCE_CONSTRUCTEUR, \
                            table.c.N_SERIE, table.c.ETAT_UTILISATION])\
                        .where(and_(table.c.ETAT_UTILISATION == "En service", table.c.DESIGNATION == "Centrale de température"))
        centrales = self.connection.execute(ins).fetchall()
        return centrales
        
    def sondes_centrales(self):
        
        table = Table("INSTRUMENTS", self.meta)
        ins = select([table.c.ID_INSTRUM, table.c.IDENTIFICATION,table.c.CONSTRUCTEUR, table.c.REFERENCE_CONSTRUCTEUR, \
                            table.c.N_SERIE, table.c.ETAT_UTILISATION, table.c.REF_INSTRUMENT])#
#                        .where(and_(table.c.ETAT_UTILISATION == "En service", table.c.INSTRUMENT_LIE == True))
        sondes = self.connection.execute(ins).fetchall()
        return sondes
        
    
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
        
    def table_caracterisation_gen_resultats_insert(self, resultat):
        table = Table("CARACTERISATION_RESULTATS", self.meta)
        self.connection.execute(table.insert(), resultat)
            
    def update_table_caracterisation_gen_resultats(self, id, resultat):
        table = Table("CARACTERISATION_RESULTATS", self.meta)
        ins = table.update().values(resultat).where(table.c.ID_CARACT == id)
        self.connection.execute(ins)
        
    def recup_caracterisation_generateurs_admin(self, id):
        table = Table("CARACTERISATION_GENERATEURS_ADMIN", self.meta)
        ins = table.select().where(table.c.ID_CARAC == id)
        admin = self.connection.execute(ins).fetchone()
#        print(id_carac)
        yield admin    
    
    
    
    def caracterisation_generateurs_admin(self, admin):
        table = Table("CARACTERISATION_GENERATEURS_ADMIN", self.meta)
        ins = table.insert(returning=[table.c.ID_CARAC]).values()
        id_carac = self.connection.execute(ins, admin).fetchone()
#        print(id_carac)
        return id_carac[0]
        
    def caracterisation_generateurs_admin_update(self, id, admin):
        
        table = Table("CARACTERISATION_GENERATEURS_ADMIN", self.meta)
        ins = table.update().values(admin).where(table.c.ID_CARAC == id)
        self.connection.execute(ins)
        
    def caracterisation_generateurs_admin_archiver(self, id):
        
        table = Table("CARACTERISATION_GENERATEURS_ADMIN", self.meta)
        ins = table.update().values(ARCHIVAGE = True).where(table.c.ID_CARAC == id)
        self.connection.execute(ins)
        
    def recup_caracterisation_moyens_utilises(self, id):
        table = Table("CARACTERISATION_MOYENS_UTILISES", self.meta)
        ins = select([table.c.ID_SONDES_CENTRALE]).where(table.c.ID_CARACTERISATION == id)
        sondes = self.connection.execute(ins).fetchone()
        yield sondes[0]
    
    def caracterisation_generateurs_moyens_mesure(self, moyens_mesure):
        table = Table("CARACTERISATION_MOYENS_UTILISES", self.meta)        
        self.connection.execute(table.insert(), moyens_mesure)
         
#    def update_caracterisation_generateurs_moyens_mesure(self, id, moyens_mesure):
#        table = Table("CARACTERISATION_MOYENS_UTILISES", self.meta)
#        ins = table.update().values(moyens_mesure).where(table.c.ID_CARACTERISATION == id)     
#        self.connection.execute(table.insert(), moyens_mesure)
        
        
    def caracterisation_generateurs_moyens_mesure_update(self, id, moyens_mesure):
        table = Table("CARACTERISATION_MOYENS_UTILISES", self.meta)
        ins = table.update().values(moyens_mesure).where(table.c.ID_CARACTERISATION == id)
        self.connection.execute(ins)       
        
    def caracterisation_bains_homogeneite(self, sauvegarde_homogeneite):
        table = Table("CARACTERISATION_BAINS_HOMOGENEITE", self.meta)        
        self.connection.execute(table.insert(), sauvegarde_homogeneite)
        
        
    def caracterisation_bains_homogeneite_update(self, id, sauvegarde_homogeneite):
        table = Table("CARACTERISATION_BAINS_HOMOGENEITE", self.meta)
        #suppression des anciennes ligne
        self.connection.execute(table.delete().where(table.c.ID_CARAC == id))
        
        self.caracterisation_bains_homogeneite(sauvegarde_homogeneite)
    
    def recup_caracterisation_bains_homogeneite(self, id):
        table = Table("CARACTERISATION_BAINS_HOMOGENEITE", self.meta)
        ins = table.select().where(table.c.ID_CARAC == id)
        homogeneite = self.connection.execute(ins).fetchall()
        n_pt = 1
        sauvegarde_hom = {}
        for resultat in homogeneite:
            sauvegarde_hom[n_pt]= {"MIN_1": resultat[3], "MIN_2": resultat[4], "MIN_4": resultat[5], "MIN_5": resultat[6],
                                                 "MAX_1": resultat[7], "MAX_2": resultat[8], "MAX_4": resultat[9], "MAX_5": resultat[10],
                                                 "MOY_1": resultat[15], "MOY_2": resultat[16], "MOY_4": resultat[17], "MOY_5": resultat[18],
                                                 "S_1": resultat[12], "S_2": resultat[13], "S_4": resultat[14], "S_5": resultat[11],
                                                 "DELTA_1": resultat[19], "DELTA_2": resultat[20], 
                                                 "EPSILONE": resultat[21], "EPSILONE_U": resultat[22], 
                                                 "TEMPERATURE": resultat[2]}
            n_pt += 1
            
#        print(sauvegarde_hom)
        
        return sauvegarde_hom
        
#        yield sondes[0]
    
    def recup_stab(self, id_caract):
        table = Table("CARACTERISATION_BAINS_STABILITE", self.meta)
        ins = table.select().where(table.c.ID_CARAC == id_caract)      
        stab = self.connection.execute(ins).fetchone()
#        print(stab)
        yield stab
    
    def caracterisation_bains_stabilite(self, sauvegarde_stab):
        table = Table("CARACTERISATION_BAINS_STABILITE", self.meta)        
        self.connection.execute(table.insert(), sauvegarde_stab)
        
        
    def caracterisation_bains_stabilite_update(self, id, sauvegarde_stab):
        table = Table("CARACTERISATION_BAINS_STABILITE", self.meta)
        ins = table.update().values(sauvegarde_stab).where(table.c.ID_CARAC == id)
        self.connection.execute(ins)
        
        
    
      #########################################################################################  
        
        
        
        
        
        
        
