#-*- coding: utf-8 -*-
from sqlalchemy import *
from sqlalchemy.orm import *
#from sqlalchemy.engine import create_engine
#from Package.AccesBdd import AccesBdd
from sqlalchemy.ext.automap import automap_base
from PyQt4.QtCore import Qt
#import json
import  decimal
from sqlalchemy import func

class AccesBdd():
    '''class gerant la bdd'''
    
    def __init__(self, engine):
        
        Base = automap_base()   
        self.engine = engine 
        self.meta = MetaData()       
        self.meta.reflect(bind=self.engine)
        
        self.connection = self.engine.connect()

#        self.meta = MetaData()

        Base.prepare(engine, reflect=True)        
        
        self.INSTRUMENTS = Base.classes.INSTRUMENTS
        self.CMR = Base.classes.CORRESPONDANTS
        self.CLIENT = Base.classes.CLIENTS
        
    def __del__(self):
        self.connection.close()
    
    def parc_enceintes(self):
        Session = sessionmaker(bind= self.engine)
        session = Session()
#        try:
        try:
                enceintes = session.query(self.INSTRUMENTS).filter(self.INSTRUMENTS.DESIGNATION == "ENCEINTE CLIMATIQUE").all()
                return enceintes
        except Exception as e:
            print(e)
            session.rollback()
#                yield None
        finally:
            session.close()
    
    def recherche_enceintes_par_saisie(self, saisie):
        try:
            Session = sessionmaker(bind= self.engine)
            session = Session()
            enceinte = session.query(self.INSTRUMENTS) \
                        .filter(and_(self.INSTRUMENTS.DESIGNATION == "ENCEINTE CLIMATIQUE", self.INSTRUMENTS.IDENTIFICATION.contains(saisie)))\
                        .all()
    #        print(enceinte_desi_lit)
            yield enceinte
#            session.close()
        except Exception as e:
            print(e)
            session.rollback()
#                yield None
        finally:
            session.close()
        
        
    
    def recherche_enceintes_par_saisie_designat_litt(self, saisie):
        Session = sessionmaker(bind= self.engine)
        session = Session()
        enceintes_des_litt = session.query(self.INSTRUMENTS) \
                    .filter(and_(self.INSTRUMENTS.DESIGNATION == "ENCEINTE CLIMATIQUE", func.lower(self.INSTRUMENTS.DESIGNATION_LITTERALE).contains(func.lower(f"%{saisie}%"))))\
                    .all()
        yield enceintes_des_litt
        session.close()
        
    
    def centrales(self):
        table = Table("INSTRUMENTS", self.meta, autoload=True,  autoload_with= self.engine)
        ins = select([table.c.ID_INSTRUM, table.c.IDENTIFICATION,table.c.CONSTRUCTEUR, table.c.REFERENCE_CONSTRUCTEUR, \
                            table.c.N_SERIE, table.c.ETAT_UTILISATION])\
                        .where(and_(func.lower(table.c.ETAT_UTILISATION) == func.lower("En service"), func.lower(table.c.DESIGNATION) == func.lower("Centrale de température")))
        centrales = self.connection.execute(ins).fetchall()

#        self.connection.close()
        return centrales
        
    def centrales_all(self):
        """retourne toutes les centrales meme archivées"""
        table = Table("INSTRUMENTS", self.meta, autoload=True,  autoload_with= self.engine)
        ins = select([table.c.ID_INSTRUM, table.c.IDENTIFICATION,table.c.CONSTRUCTEUR, table.c.REFERENCE_CONSTRUCTEUR, \
                            table.c.N_SERIE, table.c.ETAT_UTILISATION])\
                        .where(func.lower(table.c.DESIGNATION) == func.lower("Centrale de température"))
        centrales = self.connection.execute(ins).fetchall()
#        self.connection.close()
        return centrales
        
        
    def sondes_centrales(self):
        
        table = Table("INSTRUMENTS", self.meta, autoload=True,  autoload_with= self.engine)
        ins = select([table.c.ID_INSTRUM, table.c.IDENTIFICATION,table.c.CONSTRUCTEUR, table.c.REFERENCE_CONSTRUCTEUR, \
                            table.c.N_SERIE, table.c.ETAT_UTILISATION, table.c.REF_INSTRUMENT])\
                        .where(and_(func.lower(table.c.ETAT_UTILISATION) == func.lower("En service"), table.c.INSTRUMENT_LIE == True))
        sondes = self.connection.execute(ins).fetchall()

        return sondes

    def polynome(self, ident):
        
        
        table = Table("POLYNOME_CORRECTION", self.meta, autoload=True,  autoload_with= self.engine)
        ins = select([table.c.COEFF_A, table.c.COEFF_B, table.c.COEFF_C, table.c.NUM_CERTIFICAT, table.c.DATE_ETAL]).where(and_(table.c.IDENTIFICATION == ident, table.c.ARCHIVAGE == False ))
        poly = self.connection.execute(ins).fetchone()
#        print("poly {}".format(poly))
        return poly
    
    
    def polynome_par_n_ce(self, n_ce):
        
        
        table = Table("POLYNOME_CORRECTION", self.meta, autoload=True,  autoload_with= self.engine)
        ins = select([table.c.COEFF_A, table.c.COEFF_B, table.c.COEFF_C, table.c.NUM_CERTIFICAT, table.c.DATE_ETAL]).where(table.c.NUM_CERTIFICAT == n_ce)
        poly = self.connection.execute(ins).fetchone()
#        print("poly {}".format(poly))
        return poly
    
    def u_etal(self, ident):
       
#        print(f"ident {ident}")
       #verification des polynomes savoir si l'etalonnage est encore actif
        table = Table("POLYNOME_CORRECTION", self.meta, autoload=True,  autoload_with= self.engine)
        ins = select([table.c.NUM_CERTIFICAT, table.c.ID_POLYNOME]).where(and_(table.c.IDENTIFICATION == ident, table.c.ARCHIVAGE == False))
        result = self.connection.execute(ins).fetchall()
        poly_actif = (x[0] for x in result)
#        print(f" type poly {type(poly_actif)}")
        id_poly_actif = (x[1] for x in result)
#        print([x[1] for x in result])
       
        table = Table("ETALONNAGE_RESULTAT", self.meta, autoload=True,  autoload_with= self.engine)
        ins = select([table.c.U, table.c.ID_ETAL_RESULT]).where(and_(table.c.CODE_INSTRUM == ident, table.c.NUM_ETAL.in_(poly_actif))).order_by(table.c.ID_ETAL_RESULT.desc())
        result = self.connection.execute(ins).fetchall()
#        print(f"result count {result}")

        etal_u = (x[0] for x in result)
#        print(f"etal_u {[x[0] for x in result]}")
        if result:
            max_etal_u = max(etal_u)
        else:
            max_etal_u =0
        
#        print(max_etal_u)
        
        table = Table("POLYNOME_TABLE_ETALONNAGE", self.meta, autoload=True,  autoload_with= self.engine)
        ins = select([table.c.INCERTITUDE]).where(table.c.ID_POLYNOME.in_(id_poly_actif)).order_by(table.c.ID_POLY_TABLE_ETAL.desc())
        result = self.connection.execute(ins).fetchall()
        etal_u_par_poly = (x[0] for x in result)
#        print(etal_u_par_poly)
        if result:
            max_etal_par_poly = max(etal_u_par_poly)
        else:
            max_etal_par_poly =0
        
        max_etal = max(max_etal_u, max_etal_par_poly)
        
        u_etal = decimal.Decimal(str(max_etal))\
                                    .quantize(decimal.Decimal(str(0.01)),rounding = decimal.ROUND_UP)

        return u_etal
    
    def u_etal_n_ce(self, n_ce):
        

       
        table = Table("ETALONNAGE_RESULTAT", self.meta, autoload=True,  autoload_with= self.engine)
        ins = select([table.c.U, table.c.ID_ETAL_RESULT]).where(table.c.NUM_ETAL == n_ce).order_by(table.c.ID_ETAL_RESULT.desc())
        result = self.connection.execute(ins).fetchall()
#        print(result)
        etal_u = [x[0] for x in result]
#        print(etal_u)
        if etal_u:
            max_etal = max(etal_u)
        else:
            max_etal =0
        

        return max_etal
        
    def cmr(self, combobox):
        
        Session = sessionmaker(bind= self.engine)
        session = Session()
#        try:
        try:
#        print("couuco")
            cmr = session.query(self.CMR).filter((self.CMR.ARCHIVAGE == None)|(self.CMR.ARCHIVAGE != True)).all()
    
            list_nom_prenom_cmr = [str(x.NOM+" "+x.PRENOM) for x in cmr ]
            list_nom_prenom_cmr.sort()
            list_nom_prenom_cmr.insert(0, "*")
    #        print(list_nom_prenom_cmr)
            combobox.addItems(list_nom_prenom_cmr)
                
        except Exception as e:
            session.rollback()
            print(e)
#                yield None
        finally:
            session.close()
            
    def client(self, code_client):
        """permete de retourner le nom ,l'adresse et la vile du client"""
        Session = sessionmaker(bind= self.engine)
        session = Session()
        try:
            client = session.query(self.CLIENT.SOCIETE, self.CLIENT.ADRESSE, self.CLIENT.VILLE, self.CLIENT.CODE_POSTAL)\
                                    .filter(self.CLIENT.CODE_CLIENT == code_client).first() 
    #        print(client)
            return client
        except Exception as e:
            print(e)
            session.rollback()
#                yield None
        finally:
            session.close()
            
    def recup_designation_litt_par_ident(self, ident):
        Session = sessionmaker(bind= self.engine)
        session = Session()
        try:
            designation_litt = session.query(self.INSTRUMENTS.DESIGNATION_LITTERALE) \
                        .filter(self.INSTRUMENTS.IDENTIFICATION == ident)\
                        .first()[0]
    #        print(designation_litt)
            yield designation_litt
#            session.close()
        except Exception as e:
            print(e)
            session.rollback()
#                yield None
        finally:
            session.close()
    def recup_constructeur_par_ident(self, ident):
        Session = sessionmaker(bind= self.engine)
        session = Session()
        constructeur = session.query(self.INSTRUMENTS.CONSTRUCTEUR) \
                    .filter(self.INSTRUMENTS.IDENTIFICATION == ident)\
                    .first()[0]
        yield constructeur
        session.close()
        
    def recup_ref_constructeur_par_ident(self, ident):
        Session = sessionmaker(bind= self.engine)
        session = Session()
        ref_constructeur = session.query(self.INSTRUMENTS.REFERENCE_CONSTRUCTEUR) \
                    .filter(self.INSTRUMENTS.IDENTIFICATION == ident)\
                    .first()[0]
        yield ref_constructeur
        session.close()
    
    def recup_n_serie_par_ident(self, ident):
        Session = sessionmaker(bind= self.engine)
        session = Session()
        n_serie = session.query(self.INSTRUMENTS.N_SERIE) \
                    .filter(self.INSTRUMENTS.IDENTIFICATION == ident)\
                    .first()[0]
        yield n_serie
        session.close()
    
    def recup_code_par_ident(self, ident):
        Session = sessionmaker(bind= self.engine)
        session = Session()
        code = session.query(self.INSTRUMENTS.CODE) \
                    .filter(self.INSTRUMENTS.IDENTIFICATION == ident)\
                    .first()[0]
        yield code
        session.close()
        
    def recup_site_par_ident(self, ident):
        Session = sessionmaker(bind= self.engine)
        session = Session()
        site = session.query(self.INSTRUMENTS.SITE) \
                    .filter(self.INSTRUMENTS.IDENTIFICATION == ident)\
                    .first()[0]
        yield site
        session.close()
    
    def recup_localisation_par_ident(self, ident):
        Session = sessionmaker(bind= self.engine)
        session = Session()
        localisation = session.query(self.INSTRUMENTS.LOCALISATION) \
                    .filter(self.INSTRUMENTS.IDENTIFICATION == ident)\
                    .first()[0]
        yield localisation
        session.close()    
    
    def recup_affect_par_ident(self, ident):
        Session = sessionmaker(bind= self.engine)
        session = Session()
        affect = session.query(self.INSTRUMENTS.AFFECTATION) \
                    .filter(self.INSTRUMENTS.IDENTIFICATION == ident)\
                    .first()[0]
        yield affect
        session.close()
    
    def recup_sous_affect_par_ident(self, ident):
        Session = sessionmaker(bind= self.engine)
        session = Session()
        sous_affect = session.query(self.INSTRUMENTS.SOUS_AFFECTATION) \
                    .filter(self.INSTRUMENTS.IDENTIFICATION == ident)\
                    .first()[0]
        yield sous_affect
        session.close()
    

    def recherche_ident_enceinte_par_saisie_designat_litt(self, design_litt):
        Session = sessionmaker(bind= self.engine)
        session = Session()
        ident = session.query(self.INSTRUMENTS.IDENTIFICATION) \
                    .filter(self.INSTRUMENTS.DESIGNATION_LITTERALE == design_litt)\
                    .first()[0]
        yield ident
        session.close()
        
            
class Carto_BDD():
        """class gestion de la bdd pour carto"""
        def __init__(self, engine):
        
            Base = automap_base()   
            self.engine = engine 
            self.meta = MetaData()       
            self.meta.reflect(bind=self.engine)
        
        
            Base.prepare(engine, reflect=True)        
        
            self.ADMIN_CARTO = Base.classes.CARTO_ADMINISTRATION
            self.CMR = Base.classes.CORRESPONDANTS
            self.CARTO_CENTRALE = Base.classes.CARTO_CENTRALE
            self.CARTO_DONNEES = Base.classes.CARTO_DONNEES
            self.CARTO_RESULTAT = Base.classes.CARTO_RESULTAT
            self.CARTO_SIMULATION = Base.classes.CARTO_SIMULATION
        
        def table_admin_entier(self):
            """recupere toute la table carto admin"""
            Session = sessionmaker(bind= self.engine)
            session = Session()
            
            try:              
                result = session.query(self.ADMIN_CARTO.IDENT_ENCEINTE, 
                                       self.ADMIN_CARTO.DATE_REALISATION,
                                       self.CMR.NOM,
                                       self.CMR.PRENOM, 
                                       self.ADMIN_CARTO.NUM_RAPPORT,
                                       self.ADMIN_CARTO.IDENT_CENTRALE,
                                       self.ADMIN_CARTO.APPLICATION, 
                                       self.ADMIN_CARTO.CONDITION_DESIREE, 
                                       self.ADMIN_CARTO.TEMP_CONSIGNE, 
                                       self.ADMIN_CARTO.SIGNE_EMT, 
                                       self.ADMIN_CARTO.EMT, 
                                       self.ADMIN_CARTO.SIMULATION, 
                                       self.ADMIN_CARTO.CONFORMITE_GLOBALE).\
                                       join(self.CMR, self.ADMIN_CARTO.ID_OPERATEUR == self.CMR.ID_CMR )\
                                       .order_by(self.ADMIN_CARTO.ID_CARTO.desc())\
                                       .limit(100)
                                       
    #            print(result.all())
                return result.all()                      

            except Exception as e:
                print(e)
                session.rollback()
                
            finally:
                session.close()
                
                
        def insertion_nvlle_carto(self, donnees):
            Session = sessionmaker(bind= self.engine)
            session = Session()
#            print(donnees)
            #########################################################################################
            def num_rapport():
                """fct pour generer le num carto"""
                annee = donnees["annexe"]["DATE"].year()                
                annee_n_1 = annee-1
                nbr_carto = len(session.query(self.ADMIN_CARTO).filter(self.ADMIN_CARTO.DATE_REALISATION <= str(str(annee)+"-12-31"), self.ADMIN_CARTO.DATE_REALISATION > str(str(annee_n_1)+"-12-31")).all())
                if nbr_carto:
                    num_rapport = "TC_"+donnees["annexe"]["DATE"].toString('yyyyMM')+"_"+str(nbr_carto+1)
                else:
                    num_rapport = "TC_"+donnees["annexe"]["DATE"].toString('yyyyMM')+"_"+str(1)                  
                          
                return num_rapport
            ##########################################################################################    
            try:
                id_operateur = session.query(self.CMR.ID_CMR).filter(self.CMR.NOM == donnees["administratif"]["responsable_mesure"].split()[0], self.CMR.PRENOM == donnees["administratif"]["responsable_mesure"].split()[1]).first()[0]
                
                if donnees["resultats"]["conclusion_generale"] == "Enceinte non Conforme"\
                    or donnees["resultats"]["conclusion_generale"] == "Enceinte non Conforme.\
                            La simulation de la température à cœur du CGR est non conforme":
                    enceinte_conforme = False
                else:
                    enceinte_conforme = True
                #Table admin
    #                print(donnees["administratif"])
                new_carto = self.ADMIN_CARTO(IDENT_ENCEINTE = donnees["administratif"]["ident_enceinte"], 
                                            DATE_REALISATION = donnees["annexe"]["DATE"].toString(Qt.ISODate) , 
                                            ID_OPERATEUR = id_operateur, 
                                            NUM_RAPPORT= num_rapport(), 
                                            IDENT_CENTRALE= donnees["administratif"]["nom_centrale"], 
                                            APPLICATION= donnees["administratif"]["application"], 
                                            CONDITION_DESIREE= donnees["administratif"]["condition_desiree"], 
                                            TEMP_CONSIGNE= donnees["administratif"]["temp_consign"], 
                                            SIGNE_EMT= donnees["administratif"]["signe_EMT"], 
                                            EMT = donnees["administratif"]["emt_processus"], 
                                            SIMULATION = donnees["simulation"]["simulation"], 
                                            CONFORMITE_GLOBALE = enceinte_conforme, 
                                            MODEL_CENTRALE = donnees["administratif"]["model_centrale"], 
                                            TYPE_CONSIGNE = donnees["administratif"]["type_consign"])
                
        
                session.add(new_carto)
                session.flush()
    #                session.commit()
    
                #table carto_sonde
    #            print(donnees["administratif"]["tableau_centrale"])
                conf_sonde = []
                for sonde in donnees["administratif"]["tableau_centrale"]:
    #                    print(f"sonde {sonde}")
                    new_sonde = self.CARTO_CENTRALE(
                                        ID_CARTO_ADMIN = new_carto.ID_CARTO , 
                                        IDENT_SONDE = sonde[0], 
                                        POSITION_SONDE = sonde[1], 
                                        NOM_SONDE_FICHIER = sonde[2], 
                                        U_ETAL = sonde[3], 
                                        DATE_ETAL = sonde[5], 
                                        N_CE = sonde[4], 
                                        RESOLUTION = (sonde[6]), 
                                        DERIVE = sonde[7])
                    conf_sonde.append(new_sonde)
    #                print(f"envoi bdd {conf_sonde}")
                session.add_all(conf_sonde)
    #            session.flush()
                
                #table donnees
    
                
                new_donnees = self.CARTO_DONNEES(ID_CARTO_ADMIN = new_carto.ID_CARTO, 
                                                CORRECTION_DONNEES = donnees["annexe"]["CORRECTION_DONNEES"], 
                                                DONNEES = donnees["annexe"]["DONNEES"].to_json(orient='index',date_format ='iso')) 
                                                
                
                session.add(new_donnees)
                session.flush()
#                print(f"""deb {donnees["annexe"]["INDEX_DEBUT"]} type : {type(donnees["annexe"]["INDEX_DEBUT"])}  
#                                    fin {donnees["annexe"]["INDEX_FIN"]} type {type(donnees["annexe"]["INDEX_FIN"])}""")
                
                new_resultat = self.CARTO_RESULTAT(ID_CARTO_ADMIN = new_carto.ID_CARTO,
                                                    RESULTAT = donnees["annexe"]["RESULTATS"].to_json(orient='index'), 
                                                    INDEX_DEB = donnees["annexe"]["INDEX_DEBUT"], 
                                                    INDEX_FIN = donnees["annexe"]["INDEX_FIN"], 
                                                    TEMP_AIR = donnees["resultats"]["temp_air"], 
                                                    U_TEMP_AIR = donnees["resultats"]["U_temp_air"],
                                                    ECART_CONSIGNE = donnees["resultats"]["ecart_consigne"],
                                                    MOY_MAX = donnees["resultats"]["moy_max"],
                                                    MOY_MIN = donnees["resultats"]["moy_min"],
                                                    HOMOGENEITE = donnees["resultats"]["homogeneite"],
                                                    STABILITE = donnees["resultats"]["stab"],
                                                    POSITION_STAB = donnees["resultats"]["position_stab"], 
                                                    CONFORMITE_CAPTEUR = donnees["resultats"]["tableau_conformite_par_capteur"], 
                                                    CONFORMITE_GLOBAL = enceinte_conforme, 
                                                    CONSEIL = donnees["resultats"]["conseils"], 
                                                    OBJET_REMARQUE = donnees["resultats"]["objet_remarques"])
                session.add(new_resultat)
                session.flush()
    #                if donnees["simulation"]["simulation"]:
    #                    new_simu = self.CARTO_SIMULATION(ID_CARTO_ADMIN = new_carto.ID_CARTO,
    #                                                      DONNEES_SIMU = donnees["simulation"]["donnees_simu"].to_json(orient='index',date_format ='iso')  )
    #                
    #                    session.add(new_simu)
    #                    session.flush()
                
                session.commit()
    #                print(f"num rapport bddd {new_carto.NUM_RAPPORT}")
                return new_carto.NUM_RAPPORT
            except Exception as e:
#                print(e)
                return e
                session.rollback()
#                yield None
            finally:
                session.close()
            
        def recup_carto(self, n_ce):
            """fct qui recupere l'ensemble des donnees d'une carto en fct de son numero de ce"""
            
            Session = sessionmaker(bind= self.engine)
            session = Session()
            
            try:  


                result = session.query(self.ADMIN_CARTO,
                                        self.CMR,
                                        self.CARTO_DONNEES, 
                                        self.CARTO_RESULTAT)\
                                        .join(self.CMR, self.ADMIN_CARTO.ID_OPERATEUR == self.CMR.ID_CMR )\
                                        .join(self.CARTO_DONNEES, self.ADMIN_CARTO.ID_CARTO == self.CARTO_DONNEES.ID_CARTO_ADMIN )\
                                        .join(self.CARTO_RESULTAT, self.ADMIN_CARTO.ID_CARTO == self.CARTO_RESULTAT.ID_CARTO_ADMIN )\
                                        .filter(self.ADMIN_CARTO.NUM_RAPPORT == n_ce).all() 
    

                
                result_bis =  session.query(self.CARTO_CENTRALE).filter(self.CARTO_CENTRALE.ID_CARTO_ADMIN == result[0][0].ID_CARTO).all()

                yield result, result_bis
            except Exception as e:
                print(e)
                session.rollback()

            finally:
                session.close()
            
        def maj_carto(self, donnees):
            """fct maj des donnees d'une carto"""
            Session = sessionmaker(bind= self.engine)
            session = Session()

            try:
                id_operateur = session.query(self.CMR.ID_CMR).filter(self.CMR.NOM == donnees["administratif"]["responsable_mesure"].split()[0], self.CMR.PRENOM == donnees["administratif"]["responsable_mesure"].split()[1]).first()[0]            
                
                id_carto = session.query(self.ADMIN_CARTO.ID_CARTO).filter(self.ADMIN_CARTO.NUM_RAPPORT == donnees["administratif"]["num_rapport"]).first()[0]
           
                if donnees["resultats"]["conclusion_generale"] == "Enceinte non Conforme"\
                    or donnees["resultats"]["conclusion_generale"] == "Enceinte non Conforme.\
                            La simulation de la température à cœur du CGR est non conforme":
                    enceinte_conforme = False
                else:
                    enceinte_conforme = True
                    
                carto_a_modif = session.query(self.ADMIN_CARTO).get(id_carto)
                
                carto_a_modif.IDENT_ENCEINTE = donnees["administratif"]["ident_enceinte"], 
                carto_a_modif.DATE_REALISATION = donnees["annexe"]["DATE"].toString(Qt.ISODate) 
                carto_a_modif.ID_OPERATEUR = id_operateur 
    #            carto_a_modif.NUM_RAPPORT= num_rapport() 
                carto_a_modif.IDENT_CENTRALE= donnees["administratif"]["nom_centrale"] 
                carto_a_modif.APPLICATION= donnees["administratif"]["application"] 
                carto_a_modif.CONDITION_DESIREE= donnees["administratif"]["condition_desiree"] 
                carto_a_modif.TEMP_CONSIGNE= donnees["administratif"]["temp_consign"] 
                carto_a_modif.SIGNE_EMT= donnees["administratif"]["signe_EMT"] 
                carto_a_modif.EMT = donnees["administratif"]["emt_processus"] 
                carto_a_modif.SIMULATION = donnees["simulation"]["simulation"]
                carto_a_modif.CONFORMITE_GLOBALE = enceinte_conforme 
                carto_a_modif.MODEL_CENTRALE = donnees["administratif"]["model_centrale"]
                carto_a_modif.TYPE_CONSIGNE = donnees["administratif"]["type_consign"]
                                                
                session.flush()
                
                
                #table carto_sonde
                session.query(self.CARTO_CENTRALE).filter(self.CARTO_CENTRALE.ID_CARTO_ADMIN == id_carto).delete()    
                conf_sonde = []
                for sonde in donnees["administratif"]["tableau_centrale"]:
                    new_sonde = self.CARTO_CENTRALE(
                                        ID_CARTO_ADMIN = id_carto , 
                                        IDENT_SONDE = sonde[0], 
                                        POSITION_SONDE = sonde[1], 
                                        NOM_SONDE_FICHIER = sonde[2], 
                                        U_ETAL = sonde[3], 
                                        DATE_ETAL = sonde[5], 
                                        N_CE = sonde[4], 
                                        RESOLUTION = sonde[6], 
                                        DERIVE = sonde[7])
                    conf_sonde.append(new_sonde)
                session.add_all(conf_sonde)
                
                session.flush()
                
                
                 #table donnees
                
#                print(id_carto)
                id_carto_donnees = session.query(self.CARTO_DONNEES.ID).filter(self.CARTO_DONNEES.ID_CARTO_ADMIN == id_carto).first()[0]
#                print(id_carto_donnees)
#                print(session.query(self.CARTO_DONNEES.ID).filter(self.CARTO_DONNEES.ID_CARTO_ADMIN == id_carto).first())
                modif_table_donnees = session.query(self.CARTO_DONNEES).get(id_carto_donnees)
                modif_table_donnees.ID_CARTO_ADMIN = id_carto 
                modif_table_donnees.CORRECTION_DONNEES = donnees["annexe"]["CORRECTION_DONNEES"] 
                modif_table_donnees.DONNEES = donnees["annexe"]["DONNEES"].to_json(orient='index',date_format ='iso') 
                    
                session.flush()
    
    
                
                #Table Resultat
                id_carto_result = session.query(self.CARTO_RESULTAT.ID).filter(self.CARTO_RESULTAT.ID_CARTO_ADMIN == id_carto).first()[0]
                
                modif_table_resultat = session.query(self.CARTO_RESULTAT).get(id_carto_result)
                modif_table_resultat.ID_CARTO_ADMIN = id_carto
                modif_table_resultat.RESULTAT = donnees["annexe"]["RESULTATS"].to_json(orient='index') 
                modif_table_resultat.INDEX_DEB = donnees["annexe"]["INDEX_DEBUT"] 
                modif_table_resultat.INDEX_FIN = donnees["annexe"]["INDEX_FIN"] 
                modif_table_resultat.TEMP_AIR = donnees["resultats"]["temp_air"] 
                modif_table_resultat.U_TEMP_AIR = donnees["resultats"]["U_temp_air"]
                modif_table_resultat.ECART_CONSIGNE = donnees["resultats"]["ecart_consigne"]
                modif_table_resultat.MOY_MAX = donnees["resultats"]["moy_max"]
                modif_table_resultat.MOY_MIN = donnees["resultats"]["moy_min"]
                modif_table_resultat.HOMOGENEITE = donnees["resultats"]["homogeneite"] 
                modif_table_resultat.STABILITE = donnees["resultats"]["stab"]
                modif_table_resultat.POSITION_STAB = donnees["resultats"]["position_stab"] 
                modif_table_resultat.CONFORMITE_CAPTEUR = donnees["resultats"]["tableau_conformite_par_capteur"] 
                modif_table_resultat.CONFORMITE_GLOBAL = enceinte_conforme 
                modif_table_resultat.CONSEIL = donnees["resultats"]["conseils"]
                modif_table_resultat.OBJET_REMARQUE = donnees["resultats"]["objet_remarques"]
    #                session.add(new_resultat)
                
                session.flush()
                session.commit()
                session.close()
                
#
            except Exception as e:
                return e
                session.rollback()
#                yield None
            finally:
                session.close()    


        def insertion_carto_annule_remplace(self, donnees):
            Session = sessionmaker(bind= self.engine)
            session = Session()
#            print(donnees)
            #########################################################################################
            def num_rapport():
                """fct pour generer le num carto"""
                annee = donnees["annexe"]["DATE"].year()                
                annee_n_1 = annee-1
                nbr_carto = len(session.query(self.ADMIN_CARTO).filter(self.ADMIN_CARTO.DATE_REALISATION <= str(str(annee)+"-12-31"), self.ADMIN_CARTO.DATE_REALISATION > str(str(annee_n_1)+"-12-31")).all())
#                test_1 =session.query(self.ADMIN_CARTO).filter(self.ADMIN_CARTO.DATE_REALISATION <= str(str(annee)+"-12-31"), self.ADMIN_CARTO.DATE_REALISATION > str(str(annee_n_1)+"-12-31")).count()
#                test_2 = session.query(func.count(self.ADMIN_CARTO.ID_CARTO)).filter(self.ADMIN_CARTO.DATE_REALISATION <= str(str(annee)+"-12-31"), self.ADMIN_CARTO.DATE_REALISATION > str(str(annee_n_1)+"-12-31"))
#                print(f"test_1 {test_1}")
#                print(f"test_2 {test_2.scalar()}")
#                print()
                
                if nbr_carto:
                    num_rapport = "TC_"+donnees["annexe"]["DATE"].toString('yyyyMM')+"_"+str(nbr_carto+1)+" Annule et Remplace "+donnees["administratif"]["num_rapport"]
                else:
                    num_rapport = "TC_"+donnees["annexe"]["DATE"].toString('yyyyMM')+"_"+str(1)+" Annule et Remplace "+donnees["administratif"]["num_rapport"]                  
                          
                return num_rapport
            ##########################################################################################    
            try:
                id_operateur = session.query(self.CMR.ID_CMR).filter(self.CMR.NOM == donnees["administratif"]["responsable_mesure"].split()[0], self.CMR.PRENOM == donnees["administratif"]["responsable_mesure"].split()[1]).first()[0]
                
                if donnees["resultats"]["conclusion_generale"] == "Enceinte non Conforme"\
                    or donnees["resultats"]["conclusion_generale"] == "Enceinte non Conforme.\
                            La simulation de la température à cœur du CGR est non conforme":
                    enceinte_conforme = False
                else:
                    enceinte_conforme = True
                #Table admin
                new_carto = self.ADMIN_CARTO(IDENT_ENCEINTE = donnees["administratif"]["ident_enceinte"], 
                                            DATE_REALISATION = donnees["annexe"]["DATE"].toString(Qt.ISODate) , 
                                            ID_OPERATEUR = id_operateur, 
                                            NUM_RAPPORT= num_rapport(), 
                                            IDENT_CENTRALE= donnees["administratif"]["nom_centrale"], 
                                            APPLICATION= donnees["administratif"]["application"], 
                                            CONDITION_DESIREE= donnees["administratif"]["condition_desiree"], 
                                            TEMP_CONSIGNE= (donnees["administratif"]["temp_consign"]), 
                                            SIGNE_EMT= donnees["administratif"]["signe_EMT"], 
                                            EMT = (donnees["administratif"]["emt_processus"]), 
                                            SIMULATION = donnees["simulation"]["simulation"], 
                                            CONFORMITE_GLOBALE = enceinte_conforme, 
                                            MODEL_CENTRALE = donnees["administratif"]["model_centrale"])
                
        
                session.add(new_carto)
                session.flush()
    #                session.commit()
    
                #table carto_sonde
                conf_sonde = []
                for sonde in donnees["administratif"]["tableau_centrale"]:
                    new_sonde = self.CARTO_CENTRALE(
                                        ID_CARTO_ADMIN = new_carto.ID_CARTO , 
                                        IDENT_SONDE = sonde[0], 
                                        POSITION_SONDE = sonde[1], 
                                        NOM_SONDE_FICHIER = sonde[2], 
                                        U_ETAL = (sonde[3]), 
                                        DATE_ETAL = sonde[5], 
                                        N_CE = sonde[4], 
                                        RESOLUTION = (sonde[6]), 
                                        DERIVE = (sonde[7]))
                    conf_sonde.append(new_sonde)
                session.add_all(conf_sonde)
            
                
                #table donnees
    
                
                new_donnees = self.CARTO_DONNEES(ID_CARTO_ADMIN = new_carto.ID_CARTO, 
                                                CORRECTION_DONNEES = donnees["annexe"]["CORRECTION_DONNEES"], 
                                                DONNEES = donnees["annexe"]["DONNEES"].to_json(orient='index',date_format ='iso')) 
                                                
                
                session.add(new_donnees)
                session.flush()
                
                
                new_resultat = self.CARTO_RESULTAT(ID_CARTO_ADMIN = new_carto.ID_CARTO,
                                                    RESULTAT = donnees["annexe"]["RESULTATS"].to_json(orient='index'), 
                                                    INDEX_DEB = donnees["annexe"]["INDEX_DEBUT"], 
                                                    INDEX_FIN = donnees["annexe"]["INDEX_FIN"], 
                                                    TEMP_AIR = donnees["resultats"]["temp_air"], 
                                                    U_TEMP_AIR = donnees["resultats"]["U_temp_air"],
                                                    ECART_CONSIGNE = donnees["resultats"]["ecart_consigne"],
                                                    MOY_MAX = donnees["resultats"]["moy_max"],
                                                    MOY_MIN = donnees["resultats"]["moy_min"],
                                                    HOMOGENEITE = donnees["resultats"]["homogeneite"],
                                                    STABILITE = donnees["resultats"]["stab"],
                                                    POSITION_STAB = donnees["resultats"]["position_stab"], 
                                                    CONFORMITE_CAPTEUR = donnees["resultats"]["tableau_conformite_par_capteur"], 
                                                    CONFORMITE_GLOBAL = enceinte_conforme, 
                                                    CONSEIL = donnees["resultats"]["conseils"], 
                                                    OBJET_REMARQUE = donnees["resultats"]["objet_remarques"])
                session.add(new_resultat)
                session.flush()
    #                if donnees["simulation"]["simulation"]:
    #                    new_simu = self.CARTO_SIMULATION(ID_CARTO_ADMIN = new_carto.ID_CARTO,
    #                                                      DONNEES_SIMU = donnees["simulation"]["donnees_simu"].to_json(orient='index',date_format ='iso')  )
    #                
    #                    session.add(new_simu)
    #                    session.flush()
                
                session.commit()
    #            print(f"num rapport bddd {new_carto.NUM_RAPPORT}")
                return new_carto.NUM_RAPPORT
            except Exception as e:
                return e
                session.rollback()
#                yield None
            finally:
                session.close()            
