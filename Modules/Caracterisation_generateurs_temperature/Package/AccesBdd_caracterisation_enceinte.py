#-*- coding: utf-8 -*-
from sqlalchemy import *
from sqlalchemy.orm import *
from sqlalchemy.engine import create_engine


class AccesBdd_caracterisation_enceinte():
    '''class gerant la bdd'''
    
    def __init__(self, engine, meta):

           
            #création de l'"engine"
        self.engine = engine
        self.meta = meta 
        self.meta.reflect(bind=self.engine)
        
        self.connection = self.engine.connect()

        
        
    def __del__(self):
        self.connection.close()
        
        
    def enceintes(self):
        table = Table("INSTRUMENTS", self.meta)
        ins = select([table.c.ID_INSTRUM, table.c.IDENTIFICATION,table.c.CONSTRUCTEUR, table.c.REFERENCE_CONSTRUCTEUR, \
                            table.c.N_SERIE, table.c.ETAT_UTILISATION])\
                            .where(and_(table.c.TYPE == "Generateur de Temperature", table.c.DESIGNATION == "Enceinte climatique"))
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
                            table.c.N_SERIE, table.c.ETAT_UTILISATION, table.c.REF_INSTRUMENT])\
                        .where(and_(table.c.ETAT_UTILISATION == "En service", table.c.INSTRUMENT_LIE == True))
        sondes = self.connection.execute(ins).fetchall()
        return sondes
        
    
    def techniciens(self):
        table = Table("TECHNICIEN", self.meta)
        ins = select([table.c.ID_TECHNICIEN, table.c.VISA])\
                            .where(table.c.ARCHIVAGE == False)
        techniciens = self.connection.execute(ins).fetchall()
        return techniciens
        
        
    def poly_etalon(self, nom):
        table = Table("POLYNOME_CORRECTION", self.meta)
        ins = table.select()\
                            .where(table.c.IDENTIFICATION == nom).order_by(table.c.DATE_CREATION_POLY.desc())
        poly = self.connection.execute(ins).fetchall()
#        print(poly)
        return poly
        
    def nom_poly_etalon_id(self, id):
        
        table = Table("POLYNOME_CORRECTION", self.meta)
        ins = table.select()\
                            .where(table.c.ID_POLYNOME == id)
        poly = self.connection.execute(ins).fetchone()
#        print(poly)
        return poly
        
    def incertitude_etal(self, nom_ce, id_poly):
        table = Table("POLYNOME_TABLE_ETALONNAGE", self.meta)
        ins = select([table.c.INCERTITUDE])\
                            .where(table.c.ID_POLYNOME == id_poly)
        u_etal = self.connection.execute(ins).fetchall()
        
        if len(u_etal) == 0:
            table = Table("ETALONNAGE_RESULTAT", self.meta)
            ins = select([table.c.U])\
                            .where(table.c.NUM_ETAL == nom_ce)
            u_etal = self.connection.execute(ins).fetchall()
        
        u_etal_mise_en_forme = [x[0] for x in u_etal]
        return u_etal_mise_en_forme
        
        
    def incertitude_max_sondes_centrale(self, list_sonde):
        print(list_sonde)
#        u_etal = float(0)
       
       #verification des polynomes savoir si l'etalonnage est encore actif
        table = Table("POLYNOME_CORRECTION", self.meta)
        ins = select([table.c.NUM_CERTIFICAT]).where(and_(table.c.IDENTIFICATION.in_(list_sonde), table.c.ARCHIVAGE == False))
        result = self.connection.execute(ins).fetchall()
        poly_actif = [x[0] for x in result]
#        print("certificats analysés : {}".format(poly_actif))
       
        table = Table("ETALONNAGE_RESULTAT", self.meta)
        ins = select([table.c.U, table.c.ID_ETAL_RESULT]).where(and_(table.c.CODE_INSTRUM.in_(list_sonde), table.c.NUM_ETAL.in_(poly_actif))).order_by(table.c.ID_ETAL_RESULT.desc())
        result = self.connection.execute(ins).fetchall()
#        print(result)
        etal_u = [x[0] for x in result]
#        print(etal_u)
        if etal_u:
            max_etal = max(etal_u)
        else:
            max_etal =0
        

        return max_etal, poly_actif
        
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
        
    def caracterisation_generateurs_moyens_mesure(self, moyens_mesure):
        table = Table("CARACTERISATION_MOYENS_UTILISES", self.meta)
        
        self.connection.execute(table.insert(), moyens_mesure)
         
    
    def caracterisation_generateurs_moyens_mesure_update(self, id, moyens_mesure):
        table = Table("CARACTERISATION_MOYENS_UTILISES", self.meta)
        ins = table.update().values(moyens_mesure).where(table.c.ID_CARACTERISATION == id)
        self.connection.execute(ins)       
        
        
    def caracterisation_enceinte_mesure(self, mesures):
        table = Table("CARACTERISATION_ENCEINTES_MESURES", self.meta)

        self.connection.execute(table.insert(), mesures)
        
        
    def caracterisation_enceinte_mesure_sup(self, id):
        table = Table("CARACTERISATION_ENCEINTES_MESURES", self.meta)
        
        self.connection.execute(table.delete().where(table.c.ID_CARACTERISATION == id))
        
        
    def caracterisation_enceinte_resultats(self, resultats):
        table = Table("CARACTERISATION_RESULTATS", self.meta)
        
        self.connection.execute(table.insert(), resultats) 
      
    
    def caracterisation_enceinte_resultats_update(self, id, resultats):
        table = Table("CARACTERISATION_RESULTATS", self.meta)
        ins = table.update().values(resultats).where(table.c.ID_CARACT == id)
        self.connection.execute(ins)   
      #########################################################################################  
        
        
        
        
        
        
        
        
        
        
     
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
        
