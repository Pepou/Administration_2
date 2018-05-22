#-*- coding: utf-8 -*-
from sqlalchemy import *
from sqlalchemy.orm import *
#from sqlalchemy.engine import create_engine
#from Package.AccesBdd import AccesBdd
from sqlalchemy.ext.automap import automap_base
from PyQt4.QtCore import Qt
#import json



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
        except:
            session.rollback()
#                yield None
        finally:
            session.close()
    
    
    def centrales(self):
        table = Table("INSTRUMENTS", self.meta, autoload=True,  autoload_with= self.engine)
        ins = select([table.c.ID_INSTRUM, table.c.IDENTIFICATION,table.c.CONSTRUCTEUR, table.c.REFERENCE_CONSTRUCTEUR, \
                            table.c.N_SERIE, table.c.ETAT_UTILISATION])\
                        .where(and_(table.c.ETAT_UTILISATION == "En service", table.c.DESIGNATION == "Centrale de température"))
        centrales = self.connection.execute(ins).fetchall()
#        self.connection.close()
        return centrales
        
        
    def sondes_centrales(self):
        
        table = Table("INSTRUMENTS", self.meta, autoload=True,  autoload_with= self.engine)
        ins = select([table.c.ID_INSTRUM, table.c.IDENTIFICATION,table.c.CONSTRUCTEUR, table.c.REFERENCE_CONSTRUCTEUR, \
                            table.c.N_SERIE, table.c.ETAT_UTILISATION, table.c.REF_INSTRUMENT])\
                        .where(and_(table.c.ETAT_UTILISATION == "En service", table.c.INSTRUMENT_LIE == True))
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
        
#        u_etal = float(0)
       
       #verification des polynomes savoir si l'etalonnage est encore actif
        table = Table("POLYNOME_CORRECTION", self.meta, autoload=True,  autoload_with= self.engine)
        ins = select([table.c.NUM_CERTIFICAT]).where(and_(table.c.IDENTIFICATION == ident, table.c.ARCHIVAGE == False))
        result = self.connection.execute(ins).fetchall()
        poly_actif = [x[0] for x in result]
#        print("certificats analysés : {}".format(poly_actif))
       
        table = Table("ETALONNAGE_RESULTAT", self.meta, autoload=True,  autoload_with= self.engine)
        ins = select([table.c.U, table.c.ID_ETAL_RESULT]).where(and_(table.c.CODE_INSTRUM == ident, table.c.NUM_ETAL.in_(poly_actif))).order_by(table.c.ID_ETAL_RESULT.desc())
        result = self.connection.execute(ins).fetchall()
#        print(result)
        etal_u = [x[0] for x in result]
#        print(etal_u)
        if etal_u:
            max_etal = max(etal_u)
        else:
            max_etal =0
        

        return max_etal
    
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
    #        print(cmr)
    #        test = [x.ARCHIVAGE for x in cmr if x.ARCHIVAGE != True]
    #        print(f"tes {test}")
            list_nom_prenom_cmr = [str(x.NOM+" "+x.PRENOM) for x in cmr ]
    #        print(list_nom_prenom_cmr)
            combobox.addItems(list_nom_prenom_cmr)
                
        except:
            session.rollback()
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
        except:
            session.rollback()
#                yield None
        finally:
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
                                       join(self.CMR, self.ADMIN_CARTO.ID_OPERATEUR == self.CMR.ID_CMR ).\
                                       order_by(self.ADMIN_CARTO.ID_CARTO.desc())
                                       
    #            print(result.all())
                return result.all()                      

            except:
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
                    num_rapport = "TC_"+donnees["annexe"]["DATE"].toString('yyyyMM')+"_"+str(nbr_carto)
                else:
                    num_rapport = "TC_"+donnees["annexe"]["DATE"].toString('yyyyMM')+"_"+str(1)                  
                          
                return num_rapport
            ##########################################################################################    
            try:
                id_operateur = session.query(self.CMR.ID_CMR).filter(self.CMR.NOM == donnees["administratif"]["responsable_mesure"].split()[0], self.CMR.PRENOM == donnees["administratif"]["responsable_mesure"].split()[1]).first()[0]
                
                if donnees["resultats"]["conclusion_generale"] == "Enceinte non Conforme":
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
                                            TEMP_CONSIGNE= float(donnees["administratif"]["temp_consign"]), 
                                            SIGNE_EMT= donnees["administratif"]["signe_EMT"], 
                                            EMT = float(donnees["administratif"]["emt_processus"]), 
                                            SIMULATION = donnees["simulation"]["simulation"], 
                                            CONFORMITE_GLOBALE = enceinte_conforme)
                
        
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
                                        U_ETAL = float(sonde[3]), 
                                        DATE_ETAL = sonde[5], 
                                        N_CE = sonde[4], 
                                        RESOLUTION = float(sonde[6]), 
                                        DERIVE = float(sonde[7]))
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
                                                    TEMP_AIR = float(donnees["resultats"]["temp_air"]), 
                                                    U_TEMP_AIR = float(donnees["resultats"]["U_temp_air"]),
                                                    ECART_CONSIGNE = float(donnees["resultats"]["ecart_consigne"]),
                                                    MOY_MAX = float(donnees["resultats"]["moy_max"]),
                                                    MOY_MIN = float(donnees["resultats"]["moy_min"]),
                                                    HOMOGENEITE = float(donnees["resultats"]["homogeneite"]),
                                                    STABILITE = float(donnees["resultats"]["stab"]),
                                                    POSITION_STAB = donnees["resultats"]["position_stab"], 
                                                    CONFORMITE_CAPTEUR = donnees["resultats"]["tableau_conformite_par_capteur"], 
                                                    CONFORMITE_GLOBAL = enceinte_conforme, 
                                                    CONSEIL = donnees["resultats"]["conseils"])
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
            except:
                session.rollback()
#                yield None
            finally:
                session.close()
#            
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
                               
    #            print(result_bis)
                return result, result_bis
            except:
                session.rollback()

            finally:
                session.close()
            
