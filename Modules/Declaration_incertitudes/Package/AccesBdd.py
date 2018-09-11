#-*- coding: utf-8 -*-
from sqlalchemy import *
from sqlalchemy.orm import *
#from sqlalchemy.engine import create_engine
from sqlalchemy import func

class AccesBdd():
    '''class gerant la bdd'''
    
    def __init__(self, engine, meta):
        
        self.engine = engine
        self.meta = meta 
        self.meta.reflect(bind=self.engine)        
        self.connection = self.engine.connect()
        
        
    def __del__(self):
        self.connection.close()
        
    def recup_table_incertitudes_moyens_mesure(self):
        
        table = Table("INCERTITUDES_MOYENS_MESURE", self.meta)
        ins = table.select().order_by(table.c.ID_INCERTITUDES_MOYENS_MESURE)
        u = self.connection.execute(ins).fetchall()
#        print(u)
        return u
        
    def u_moyens_mesure(self, id_caract):
        table = Table("CARACTERISATION_ENCEINTES_MESURES", self.meta)
        ins =select([table.c.U_MOYENS]).where(table.c.ID_CARACTERISATION == id_caract)
        result = self.connection.execute(ins).fetchall()
        u = max([float(x[0]) for x in result if x[0]])
        
        return u
    
    
     
    def generateurs(self):
        table = Table("INSTRUMENTS", self.meta)
        ins = select([table.c.ID_INSTRUM, table.c.IDENTIFICATION,table.c.CONSTRUCTEUR, table.c.REFERENCE_CONSTRUCTEUR, \
                            table.c.N_SERIE, table.c.ETAT_UTILISATION, table.c.DESIGNATION])\
                            .where(table.c.TYPE == "Generateur de Temperature")
        generateurs = self.connection.execute(ins).fetchall()
        return generateurs
        
    def etalons(self):
        table = Table("INSTRUMENTS", self.meta)
        ins = select([table.c.ID_INSTRUM, table.c.IDENTIFICATION,table.c.CONSTRUCTEUR, table.c.REFERENCE_CONSTRUCTEUR, \
                            table.c.N_SERIE, table.c.ETAT_UTILISATION])\
                        .where(and_(func.lower(table.c.ETAT_UTILISATION) == func.lower("En service"), table.c.DESIGNATION.contains("Etalon")))
        etalons = self.connection.execute(ins).fetchall()
        
#        print(f"etalon {etalons}")
        return etalons
        
    def return_polys_etalon(self, list_etalon):
        """renvoie les caracteristiques des polynomes qd noms etalons en listes"""
        table = Table("POLYNOME_CORRECTION", self.meta)
        ins = table.select()\
                            .where(table.c.IDENTIFICATION.in_(list_etalon)).order_by(table.c.DATE_CREATION_POLY.desc())
        poly = self.connection.execute(ins).fetchall()
#        print(poly)
        return poly
        
    def return_polys_by_id(self, id):
        """renvoie les caracteristiques des polynomes qd noms etalons en listes"""
        table = Table("POLYNOME_CORRECTION", self.meta)
        ins = select([table.c.DATE_ETAL, table.c.NUM_CERTIFICAT, table.c.IDENTIFICATION])\
                            .where(table.c.ID_POLYNOME == id)
        poly = self.connection.execute(ins).fetchone()
#        print(poly)
        return poly
        
    def incertitude_etal_list_id_poly(self , list_id_poly):
        table = Table("POLYNOME_TABLE_ETALONNAGE", self.meta)
        ins = select([table.c.INCERTITUDE])\
                            .where(table.c.ID_POLYNOME.in_(list_id_poly))
        result = self.connection.execute(ins).fetchall()
        list_uetal = [float(x[0]) for x in result]
#        print("uetal {}".format(list_uetal))
        return list_uetal
        
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
        
        
    def return_caracterisations_list_generateurs(self, list_generateurs):
        """renvoie les caracteristiques des polynomes qd noms etalons en listes"""
        table = Table("CARACTERISATION_GENERATEURS_ADMIN", self.meta)
        ins = table.select()\
                            .where(table.c.ID_GENERATEUR.in_(list_generateurs)).order_by(table.c.DATE.desc())
        list_carac = self.connection.execute(ins).fetchall()

        return list_carac
        
    def return_carac_by_id(self, id):
        table = Table("CARACTERISATION_GENERATEURS_ADMIN", self.meta)
        ins = select([table.c.DATE, table.c.ID_GENERATEUR])\
                            .where(table.c.ID_CARAC == id)
        carac = list(self.connection.execute(ins).fetchone())
#        print(carac)
        table = Table("INSTRUMENTS", self.meta)
        ins = select([table.c.IDENTIFICATION])\
                            .where(table.c.ID_INSTRUM == carac[1])
        nom_generateur = self.connection.execute(ins).fetchone()[0]

#        del carac[1] 
        carac.insert(1,nom_generateur)
        carac.insert(1, id)
#        print("carac ")
        return carac
        
    def return_designation_by_id(self, id_instrum):
        table = Table("INSTRUMENTS", self.meta)
        ins = select([table.c.DESIGNATION])\
                            .where(table.c.ID_INSTRUM == id_instrum)
        designation = self.connection.execute(ins).fetchone()[0]
        return designation
        
        
    def incertitude_caracterisation(self, list_id_caract):
        table = Table("CARACTERISATION_RESULTATS", self.meta)
        ins = select([table.c.STABILITE, table.c.HOMOGENEITE, table.c.ECART_TYPE, table.c.u_generateur, table.c.ID_CARACT])\
                .where(table.c.ID_CARACT.in_(list_id_caract))
                
        result = self.connection.execute(ins).fetchall()
#        print("selection des caracterisation {}".format(result))
        return result
        
    def insertion_declaration_incertitudes(self, dict_donnees):
        
        table = Table("INCERTITUDES_MOYENS_MESURE", self.meta)
        
        self.connection.execute(table.insert(), dict_donnees)
        
    def archivage_declaration(self, id):
        table = Table("INCERTITUDES_MOYENS_MESURE", self.meta)
        ins = table.update().values(ARCHIVAGE = True).where(table.c.ID_INCERTITUDES_MOYENS_MESURE == id)
        self.connection.execute(ins)
        
        
    def update_declaration_incertitudes(self, declaration_incertitudes, id):
        
        table = Table("INCERTITUDES_MOYENS_MESURE", self.meta)
        ins = table.update().values(declaration_incertitudes).where(table.c.ID_INCERTITUDES_MOYENS_MESURE == id)
        self.connection.execute(ins)   
