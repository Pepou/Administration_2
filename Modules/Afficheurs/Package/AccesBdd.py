#-*- coding: utf-8 -*-
from sqlalchemy import *
from sqlalchemy.orm import *
from sqlalchemy.engine import create_engine
from sqlalchemy.ext.automap import automap_base
from sqlalchemy import func
import numpy as np
import pandas as pd
import itertools
from PyQt4.QtGui import QMessageBox
from PyQt4 import QtGui
class AccesBdd():
    '''class gerant la bdd'''
    
    def __init__(self, engine, meta):
        

#        self.namebdd = "Labo_Metro_Prod"#"Labo_metro_Test_5" #
#        self.adressebdd = "10.42.1.74"#"localhost"#"10.42.1.74"       # #localhost"     
#        self.portbdd = "5434" 
#        self.login = login
#        self.password = password
           
            #création de l'"engine"
            
        Base = automap_base()
        
        self.engine =  engine
        self.meta = meta        
        self.meta.reflect(bind=self.engine)
        self.polynome_correction = Table('POLYNOME_CORRECTION', self.meta)
        self.connection = self.engine.connect()
        Session = sessionmaker(bind=self.engine)
        self.session = Session.configure(bind=self.engine)
        
        
        Base.prepare(engine, reflect=True)        
        
        self.POLYNOME = Base.classes.POLYNOME_CORRECTION
        self.TABLE_ETAL_POLY = Base.classes.POLYNOME_TABLE_ETALONNAGE
        self.RESULTATS_ETAL_TEMP = Base.classes.ETALONNAGE_RESULTAT
        
        self.RESULT_AFFICHEUR = Base.classes.AFFICHEUR_CONTROLE_RESULTAT
        self.ADMIN_AFFICHEUR = Base.classes.AFFICHEUR_CONTROLE_ADMINISTRATIF
        self.ENTITE_CLIENT = Base.classes.ENTITE_CLIENT
        self.CLIENT = Base.classes.CLIENTS
        
    def __del__(self):
        self.connection.close()
        
    
    def recensement_sites(self, combobox):        
               
        Session = sessionmaker(bind= self.engine)
        session = Session()
#        
        
        try:
            table = session.query(self.CLIENT.CODE_CLIENT).\
                    join(self.ENTITE_CLIENT).\
                    filter(self.ENTITE_CLIENT.ABREVIATION == "EFS_CPDL").all()
            
                       
            code = set([x.CODE_CLIENT for x in table])
    #        print(sites)
            combobox.addItems(list(code))

    #        session.close()
#            return table
#        
        except Exception as e:
            print(e)
            session.rollback()
#            yield None
        finally:
            session.close()
        
    
    def recensement_afficheurs(self, type_afficheur, service, code_client):
        '''fct pour avoir l'ensemble des afficheurs du type : afficheur_type'''
        
        table = Table("INSTRUMENTS", self.meta)
        ins = table.select().where(and_(or_(table.c.DESIGNATION == type_afficheur, table.c.DESIGNATION == type_afficheur.upper(), table.c.DESIGNATION == type_afficheur.capitalize()), table.c.CODE == code_client))#, table.c.AFFECTATION == service))

        result = self.connection.execute(ins)
        
        identification_afficheurs = []
        for ele in result:
          identification_afficheurs.append(ele[1])
          
        return  identification_afficheurs
        
    def recensement_afficheurs_complet(self):
        '''recensement de tous les afficheurs'''
        table = Table("INSTRUMENTS", self.meta)
        ins = table.select().where(or_(table.c.DESIGNATION == "Sonde alarme température",table.c.DESIGNATION == "SONDE ALARME TEMPÉRATURE", 
                                    table.c.DESIGNATION == "Afficheur de vitesse", table.c.DESIGNATION == "AFFICHEUR DE VITESSE",
                                    table.c.DESIGNATION == "Afficheur de temps", table.c.DESIGNATION == "AFFICHEUR DE TEMPS",
                                    table.c.DESIGNATION == "Afficheur de température", table.c.DESIGNATION == "AFFICHEUR DE TEMPÉRATURE", 
                                    table.c.DESIGNATION == "TÉMOIN D'ENVIRONNEMENT"))

        result = self.connection.execute(ins)
        
        identification_afficheurs = []
        for ele in result:
          identification_afficheurs.append(ele[1])
          
        return  identification_afficheurs
        
        
    def recensement_etalons(self, type_afficheur, service, code, designation_etalon):
        '''fct pour avoir l'ensemble des afficheurs du type : afficheur_type'''
        
        table = Table("INSTRUMENTS", self.meta)
#        ins = table.select().where(and_(table.c.DOMAINE_MESURE == type_afficheur, table.c.SITE == site, table.c.DESIGNATION == designation_etalon))#, table.c.AFFECTATION == service))
        ins = table.select().where(and_(func.lower(table.c.DOMAINE_MESURE) == func.lower(type_afficheur),
                                        func.lower(table.c.DESIGNATION) == func.lower(designation_etalon)))\
                                        .order_by(table.c.ID_INSTRUM)#, table.c.SITE == site, table.c.DESIGNATION == designation_etalon))#, table.c.AFFECTATION == service))
        
        result = self.connection.execute(ins)
        
        identification_etalon = []
        for ele in result:
          identification_etalon.append(ele[1])
          
        return  identification_etalon
        
    def recensement_etalons_vitesse(self, designation_etalon):
        '''fct pour avoir l'ensemble des afficheurs du type : afficheur_type'''
        
        table = Table("INSTRUMENTS", self.meta)
        ins = table.select().where(table.c.DESIGNATION == designation_etalon)

        result = self.connection.execute(ins)
        
        identification_etalon = []
        for ele in result:
          identification_etalon.append(ele[1])
          
        return  identification_etalon
 
    def recensement_referentiel_emt(self, designation_afficheur):
        '''fct pour avoir l'ensemble des afficheurs du type : afficheur_type'''
        
        table = Table("REFERENTIEL_CONFORMITE", self.meta)
        ins = select([table.c.REFERENTIEL, table.c.COMMENTAIRE_REFERENTIEL, table.c.ERREUR_TERME_CST, 
                        table.c.ERREUR_TERME_VAR, table.c.ERREUR_UNITE]).where(func.lower(table.c.DESIGNATION) == func.lower(designation_afficheur)).order_by(table.c.ID_REFERENTIEL)

        result = self.connection.execute(ins)
        
        referentiel = []
        for ele in result:
          referentiel.append(ele)

        return  referentiel


    def valeur_emt(self, referentiel):
        '''fct pour avoir l'ensemble des afficheurs du type : afficheur_type'''
        
        table = Table("REFERENTIEL_CONFORMITE", self.meta)
        ins = select([table.c.ERREUR_TERME_CST, 
                        table.c.ERREUR_TERME_VAR, table.c.ERREUR_UNITE]).where(table.c.REFERENTIEL == referentiel)

        result = self.connection.execute(ins)
        
        valeur_emt = []
        for ele in result:
          valeur_emt.append(ele)
#        print(valeur_emt)
        return  valeur_emt
 
    def caract_afficheur(self, identification):
        '''fct qui recupere un n° serie , constructeur , type, en fct identification affcheur'''
#        print("identification {}".format(identification))
        table = Table("INSTRUMENTS", self.meta)
        ins = select([table.c.N_SERIE, table.c.CONSTRUCTEUR, table.c.TYPE, table.c.COMMENTAIRE, table.c.RESOLUTION,
                        table.c.AFFECTATION, table.c.SITE, table.c.CODE, table.c.ID_INSTRUM]).where(table .c.IDENTIFICATION == identification)
        result = self.connection.execute(ins)    
#        print(f"result {result}")
        for ele in result:
#            print("ele {}".format(ele))
            n_serie = ele[0]
            constructeur = ele[1]
            type = ele[2]
            commentaire = ele[3]
            resolution = ele[4]
            affectation = ele[5]
            site = ele[6]
            code = ele[7]
            id=ele[8]
        return n_serie, constructeur, type, commentaire, resolution, affectation, site, code, id
    
    def caract_afficheur_modif(self, identification):
        '''fct qui recupere un n° serie , constructeur , type, en fct identification affcheur'''
        
        table = Table("INSTRUMENTS", self.meta)
        ins = table.select().where(table .c.IDENTIFICATION == identification)
        result = self.connection.execute(ins)    
        
        for ele in result:
            caract_afficheur = ele
        
        return caract_afficheur
        
    def recensement_cmr(self):
        '''fct pour rapatrier le nom+prenom cmr dela table CORRESPONDANTS'''
        table = Table("CORRESPONDANTS", self.meta)
        ins = table.select().order_by(table.c.ID_CMR)
        result = self.connection.execute(ins)
        
        cmr = []
        for ele in result:
            cmr.append(ele[1] + " "+ele[2])#.capitalize())
            
        return cmr
        
    def recuperation_site_service_cmr(self, nom, prenom):
        '''fct pour recupere le site et le service du cmr'''
#        print(nom)
#        print(prenom)
        table = Table("CORRESPONDANTS", self.meta)
        ins = select([table.c.SITE, table.c.SERVICE]).where(and_(table.c.NOM == nom, table.c.PRENOM == prenom))

        result = self.connection.execute(ins)
         
        for ele in result:
            service_site = ele
        return service_site
    
    def recuperation_code_client_affectation(self, identification):
        '''fct qui recupere le code du client et affectation de l'instrument en fct de l'identification afficheur'''
        
        table = Table("INSTRUMENTS", self.meta)
        ins = select([table.c.CODE, table.c.AFFECTATION]).where(table .c.IDENTIFICATION == identification)
        result = self.connection.execute(ins)    
        
        for ele in result:
            code_client = ele[0]
            affectation = ele[1]
            
        table = Table("CLIENTS", self.meta)
        ins = select([table.c.SOCIETE, table.c.ADRESSE, table.c.CODE_POSTAL, table.c.VILLE]).where(table .c.CODE_CLIENT == code_client)
        result = self.connection.execute(ins)      
        
        for ele in result:
            societe = ele[0]
            adresse = ele[1]
            code_postal = ele[2]
            ville = ele[3]
            
        return societe, affectation, adresse, code_postal, ville
    
    
    def sauvegarde_table_afficheur_ctrl_admin(self, afficheur):
        '''fct qui sauvegarde dans la table afficheur controle admin'''
        donnees = {}
        #recuperation id instrument*
        table = Table("INSTRUMENTS", self.meta)
        ins = select([table.c.ID_INSTRUM]).where(table .c.IDENTIFICATION == afficheur["identification_instrument"])
        result = self.connection.execute(ins)    
        
        for ele in result:
            id_instrum = ele[0]
                
        #recuperation id cmr
        cmr = afficheur["operateur"].split()
        table = Table("CORRESPONDANTS", self.meta)
        ins = select([table.c.ID_CMR]).where(and_(table .c.NOM == cmr[0], table.c.PRENOM == cmr[1]))
        result = self.connection.execute(ins)    
        
        for ele in result:
            id_cmr = ele[0]
        
        #insertion dans table afficheur_controle admin
        donnees["DATE_CONTROLE"] = afficheur["date_etalonnage"]
        donnees["IDENTIFICATION"] = id_instrum
        donnees["NOM_PROCEDURE"] = "CPL/PIL/SUR/MET/MO" + afficheur["n_mode_operatoire"]
        donnees["NBR_PT"] = afficheur["nbr_pt_etalonnage"]
        donnees["TECHNICIEN"] = id_cmr
        donnees["ARCHIVAGE"] = False
        donnees["COMMENTAIRE_RESULTATS"] = afficheur["commentaire_resultats"]
        donnees["TYPE_RAPPORT"] = afficheur["type_rapport"]
        
        if afficheur["annule_remplace"] != "" :
            donnees["ANNULE_REMPLACE"] = afficheur["annule_remplace"]
        
        
        table = Table("AFFICHEUR_CONTROLE_ADMINISTRATIF", self.meta)
#        ins = table.select().where(extract('year', table.c.DATE_CONTROLE) == afficheur["annee_ctrl"])
        ins = table.select()
        saisies_annee = self.connection.execute(ins).fetchall()
#        print("saisies {}".format(saisies_annee))
        
        #tri sur n° CE  : le but recuperer le n° max
        if len(saisies_annee)!= 0:
            numeros_certificats = [x[2] for x in saisies_annee if str(x[2][3:7]) == str(afficheur["annee_ctrl"])]
#            for x in saisies_annee:
#                print("{}".format(x[2][3:7]))
#                print("afficheur[annee_ctrl] {}".format(afficheur["annee_ctrl"]))
#            print("numeros certificats {}".format(numeros_certificats))
            
            if len(numeros_certificats) !=0:             
#                numeros_fin_certificats = [int(x.split("_")[1]) for x in numeros_certificats]
                num_max = len(numeros_certificats) #np.amax(numeros_fin_certificats)
            else:
                num_max = 0
#            print("num max {}".format(num_max))
            
            n_saisie = num_max + 1
            
        else:
            n_saisie = 1
#        print(nbr_saisies)
        
        
        
        
#        b = [x.split("_")[1] for x in a] 
        
        
        #construction numero doc
        if afficheur["designation"] == "Sonde alarme température":
            prefix = "SAT"
        elif afficheur["designation"] == "Afficheur de température":
            prefix = "AFT"
        elif afficheur["designation"] == "Afficheur de temps":
            prefix = "AFM"
        elif afficheur["designation"] == "Afficheur de vitesse":
            prefix = "AFV"            
        elif afficheur["designation"] == "Temoin d'environnement":
            prefix = "TEV"  
        
        donnees["NUM_DOC"] = prefix + afficheur["num_doc_provisoire"]+"_"+ str(n_saisie)
#        print("n ce {}".format(donnees["NUM_DOC"]))
        
        #verification si le numero n'est pas ds la bdd
        table = Table("AFFICHEUR_CONTROLE_ADMINISTRATIF", self.meta)
        ins = select([table.c.NUM_DOC])
        result = self.connection.execute(ins).fetchall()
        list_n_ce=[x[0] for x in result]

        while donnees["NUM_DOC"] in list_n_ce:
#            print(donnees["NUM_DOC"])
            n_saisie +=1
            donnees["NUM_DOC"] = prefix + afficheur["num_doc_provisoire"]+"_"+ str(n_saisie)
            
      
        
        #insertion
        table = Table("AFFICHEUR_CONTROLE_ADMINISTRATIF", self.meta)
        ins = table.insert(returning=[table.c.ID_AFFICHEUR_ADMINISTRATIF])
        result = self.connection.execute(ins, donnees)
        id = []
        for ele in result:            
            id = ele 
            
        
#        table = Table("AFFICHEUR_CONTROLE_ADMINISTRATIF", self.meta)
#        ins = table.update().where(table.c.ID_AFFICHEUR_ADMINISTRATIF == id[0]).values(NUM_DOC = num_doc)
#        result = self.connection.execute(ins, donnees)
        
        #on reecrit le num du doc pour le ce si jamais annule et remplace
        if afficheur["annule_remplace"] == "" :
            num_doc = prefix + afficheur["num_doc_provisoire"]+"_"+ str(n_saisie)
        else:
            num_doc = prefix + afficheur["num_doc_provisoire"]+"_"+ str(n_saisie) + "\n" + "Annule et remplace" +\
                        " "+afficheur["annule_remplace"]
        
        n_ce = afficheur["ce_etalon"][:len(afficheur["ce_etalon"])-12]  #permet de recuperer juste le n°ce etalon sinon n°CE etalon +la date
        
        #gestion insertion bdd table AFFICHEUR_CONTROLE_RESULTAT
            # recuperation id etalon
            #recuperation id instrument*
        table = Table("INSTRUMENTS", self.meta)
        ins = select([table.c.ID_INSTRUM]).where(table .c.IDENTIFICATION == afficheur["etalon"])
        result = self.connection.execute(ins)    
        
        for ele in result:
            id_etalon = ele[0]

        afficheur["list_referentiel"] = []
        for ele in afficheur["emt"]:
            table = Table("REFERENTIEL_CONFORMITE", self.meta)
            ins = select([table.c.ID_REFERENTIEL]).where(table .c.REFERENTIEL == ele)
            result = self.connection.execute(ins)           
            for ele in result:
                afficheur["list_referentiel"].append(ele[0]) 
        
        list_table_aff_result = []       
        for i in range(0, donnees["NBR_PT"]):

            dict_table_aff_result = {}
            dict_table_aff_result["ID_AFF_CTRL_ADMIN"] = id[0]
            dict_table_aff_result["NBR_PT_CTRL"] = donnees["NBR_PT"]
            dict_table_aff_result["N_PT_CTRL"] = i + 1
            dict_table_aff_result["ID_ETALON"] = id_etalon
            dict_table_aff_result["CE_ETALON"] = n_ce
            dict_table_aff_result["RESOLUTION"] =  afficheur["resolution"][i]
            dict_table_aff_result["MOYENNE_ETALON_NC"] =  np.mean(afficheur["valeurs_etalon_nc"][i])
            dict_table_aff_result["MOYENNE_ETALON_C"] = afficheur["moyenne_etalon_corri"][i]
            dict_table_aff_result["MOYENNE_AFFICHEUR"] = afficheur["moyenne_instrum"][i]
            dict_table_aff_result["MOYENNE_CORRECTION"] = afficheur["moyenne_correction"][i]
            dict_table_aff_result["U"] =  afficheur["U"][i]
            dict_table_aff_result["CONFORMITE"] =  afficheur["conformite"] [i]
            dict_table_aff_result["ARCHIVAGE"] = False
            dict_table_aff_result["ID_REF_CONFORMITE"] =  afficheur["list_referentiel"][i]
            
            list_table_aff_result.append(dict_table_aff_result)

        #insertion table resultat
        table = Table("AFFICHEUR_CONTROLE_RESULTAT", self.meta)
        ins = table.insert()
        result = self.connection.execute(ins, list_table_aff_result)

        #Ërecherche id polynome
            
        table = Table("POLYNOME_CORRECTION", self.meta)
        ins = select([table.c.ID_POLYNOME]).where(table .c.NUM_CERTIFICAT == n_ce)
        result = self.connection.execute(ins)    
        
        for ele in result:
            id_poly = ele[0]
        
        
        
        list_mesures = []
        for i in range(0, donnees["NBR_PT"]):           
            for j in range(0, len(afficheur["valeurs_etalon_nc"][i])):
                dict_table_mesures = {}
                
                dict_table_mesures["ID_AFF_CTRL_ADMIN"] = id[0]
                dict_table_mesures["ID_ETALON"] = id_etalon
                dict_table_mesures["ID_POLYNOME"] = id_poly
                dict_table_mesures["ETALON_NC"] = afficheur["valeurs_etalon_nc"][i][j]
                dict_table_mesures["ETALON_C"] = afficheur["valeurs_etalon_c"][i][j]
                dict_table_mesures["AFFICHEUR"] = afficheur["valeurs_afficheur"][i][j]
                dict_table_mesures["NBR_PTS"] = donnees["NBR_PT"]
                dict_table_mesures["N_PT"] = i + 1
                dict_table_mesures["NBR_MESURE"] = len(afficheur["valeurs_etalon_nc"][i])
                dict_table_mesures["N_MESURE"] = j+1
                list_mesures.append(dict_table_mesures)

        #insertion table mesure
        table = Table("AFFICHEUR_CONTROLE_MESURES", self.meta)
        ins = table.insert()
        result = self.connection.execute(ins, list_mesures)
        
        
        return num_doc
        
    def recuperation_polynomes_etal(self, identification):
        '''fct qui va recuperer dans la table polynome corrections
        les differents poly ainsi que leurs caracteristiques'''
        table = Table("POLYNOME_CORRECTION", self.meta)
        ins = select([table.c.NUM_CERTIFICAT, table.c.DATE_ETAL, table.c.ORDRE_POLY,\
                        table.c.COEFF_A, table.c.COEFF_B, table.c.COEFF_C, table.c.ARCHIVAGE])\
                        .where(and_(table.c.IDENTIFICATION == identification, table.c.ARCHIVAGE == 'False')).order_by(table.c.NUM_CERTIFICAT)
        result = self.connection.execute(ins)
        
        donnees_poly_table_etal = []        
        for ele in result:   
            donnees_poly_table_etal.append(ele) 
        
        return donnees_poly_table_etal
        
    def recuperation_polynome_etal_num_ce(self, num_ce):
        '''fct qui va recuperer dans la table polynome corrections
        les differents poly ainsi que leurs caracteristiques'''
        
        table = Table("POLYNOME_CORRECTION", self.meta)
        ins = select([table.c.NUM_CERTIFICAT, table.c.DATE_ETAL, table.c.ORDRE_POLY,\
                        table.c.COEFF_A, table.c.COEFF_B, table.c.COEFF_C, table.c.ARCHIVAGE])\
                        .where(table.c.NUM_CERTIFICAT == num_ce).order_by(table.c.NUM_CERTIFICAT)
        result = self.connection.execute(ins)
        
        donnees_poly_table_etal = []        
        for ele in result:   
            donnees_poly_table_etal.append(ele) 
        
        return donnees_poly_table_etal
        
    
    
    def etendue_mesure_etalon(self, num_ce):
        """fcontion qui va calculer l'etendue de msuere de l'etalon dans les table polynome_correction
        tableetalpoly,temperature resultat"""
#        self.POLYNOME = Base.classes.POLYNOME_CORRECTION
#        self.TABLE_ETAL_POLY = Base.classes.POLYNOME_TABLE_ETALONNAGE
#        self.RESULTATS_ETAL_TEMP = Base.classes.ETALONNAGE_RESULTAT
        
#        print(num_ce)
        try:
            Session = sessionmaker(bind= self.engine)
            session = Session()
    #        try:
            id_poly = session.query(self.POLYNOME).filter(self.POLYNOME.NUM_CERTIFICAT == num_ce).first().ID_POLYNOME
            #on regarde si presence d'une table etalon dans Polynome_table_etalonnage
            table_etalonnage = session.query(self.TABLE_ETAL_POLY).filter(self.TABLE_ETAL_POLY.ID_POLYNOME == id_poly).all()
            
            if table_etalonnage:
    #                print(f"table etal {table_etalonnage}")
                resultat_etal = session.query(self.TABLE_ETAL_POLY.MOYENNE_ETALON_CORRI).filter(self.TABLE_ETAL_POLY.ID_POLYNOME == id_poly)
                resultat_etal_pandas = pd.read_sql(resultat_etal.statement, session.bind) 
#                print(resultat_etal_pandas)
                min = resultat_etal_pandas.min()
                max = resultat_etal_pandas.max()
#                print(f" min  {min} max {max}")
            else:
                
                resultat_etal = session.query(self.RESULTATS_ETAL_TEMP.MOYENNE_ETAL_C).filter(self.RESULTATS_ETAL_TEMP.NUM_ETAL == num_ce)
                resultat_etal_pandas = pd.read_sql(resultat_etal.statement, session.bind) 
#                print(resultat_etal_pandas)
                min = resultat_etal_pandas.min()
                max = resultat_etal_pandas.max()
#                print(f" min  {min} max {max}")
                
            return min, max
        except Exception as e:
            print(e)
            session.rollback()
            
        finally:
            session.close()
#    
    def incertitude_etalonnage_temperature(self, identification_etalon, numero_ce):
        '''fct permettant de recupere l'incertitude max d'etalonnage'''
        
        table = Table("ETALONNAGE_RESULTAT", self.meta)
        ins = select([table.c.U]).where(and_(table.c.CODE_INSTRUM == identification_etalon, table.c.NUM_ETAL == numero_ce))
        result = self.connection.execute(ins)
        
        U_etalonnage_etalon =[]
        for ele in result:
            U_etalonnage_etalon.append(ele)
                       
        return U_etalonnage_etalon
        
    def incertitude_etalonnage_temperatre_bis(self, identification_etalon, numero_ce):
        ''''fct qui recupere dans une list les incertitudes d'etalonnage'''
        
        #recuperation id polynome
        table = Table("POLYNOME_CORRECTION", self.meta)
        ins = select([table.c.ID_POLYNOME]).where(and_(table.c.IDENTIFICATION == identification_etalon, table.c.NUM_CERTIFICAT == numero_ce))
        result = self.connection.execute(ins)
        
#        id_poly =[]
        for ele in result:
            id_poly = ele[0]

        #recuperation id polynome
        table = Table("POLYNOME_TABLE_ETALONNAGE", self.meta)
        ins = select([table.c.INCERTITUDE]).where(table.c.ID_POLYNOME == id_poly)
        result = self.connection.execute(ins)
        U =[]
        for ele in result:
            U.append(ele)
            
        return U
        
    def incertitude_etalonnage_vitesse(self, identification_etalon, numero_ce):
        ''''fct qui recupere dans une list les incertitudes d'etalonnage'''
        
        #recuperation id polynome
        table = Table("POLYNOME_CORRECTION", self.meta)
        ins = select([table.c.ID_POLYNOME]).where(and_(table.c.IDENTIFICATION == identification_etalon, table.c.NUM_CERTIFICAT == numero_ce))
        result = self.connection.execute(ins)
        
#        id_poly =[]
        for ele in result:
            id_poly = ele[0]

        #recuperation id polynome
        table = Table("POLYNOME_TABLE_ETALONNAGE", self.meta)
        ins = select([table.c.INCERTITUDE]).where(table.c.ID_POLYNOME == id_poly)
        result = self.connection.execute(ins)
        U =[]
        for ele in result:
            U.append(ele)
            
        return U
        
        
    def recuperation_corrections_etalonnage_vitesse(self, identification_etalon, numero_ce):
        ''''fct qui recupere dans une list les corrections d'etalonnage'''
        
        #recuperation id polynome
        table = Table("POLYNOME_CORRECTION", self.meta)
        ins = select([table.c.ID_POLYNOME]).where(and_(table.c.IDENTIFICATION == identification_etalon, table.c.NUM_CERTIFICAT == numero_ce))
        result = self.connection.execute(ins)
        
        
        for ele in result:
            id_poly = ele[0]
        
        #recuperation id polynome
        table = Table("POLYNOME_TABLE_ETALONNAGE", self.meta)
        ins = select([table.c.MOYENNE_INSTRUM, table.c.CORRECTION]).where(table.c.ID_POLYNOME == id_poly)
        result = self.connection.execute(ins)
        table_etal_tlue_correction =[]
        for ele in result:
            table_etal_tlue_correction.append(ele)
            
        return table_etal_tlue_correction
        
    def recuperation_corrections_etalonnage_temp(self, identification_etalon, numero_ce):
        '''fct permettant de recuêrer les donnees d'etalonnage (correction...) 
        afin de calculer une incertitude de modelisation'''
        
        table = Table("ETALONNAGE_RESULTAT", self.meta)
        ins = select([table.c.MOYENNE_INSTRUM, table.c.MOYENNE_CORRECTION]).where(and_(table.c.CODE_INSTRUM == identification_etalon, table.c.NUM_ETAL == numero_ce))
        result = self.connection.execute(ins)
        
        table_etal_tlue_correction = []
        for ele in result:
            table_etal_tlue_correction.append(ele)
        
        return table_etal_tlue_correction
        
    def recuperation_corrections_etalonnage_temp_bis(self, identification_etalon, numero_ce):
        ''''fct qui recupere dans une list les corrections d'etalonnage'''
        
        #recuperation id polynome
        table = Table("POLYNOME_CORRECTION", self.meta)
        ins = select([table.c.ID_POLYNOME]).where(and_(table.c.IDENTIFICATION == identification_etalon, table.c.NUM_CERTIFICAT == numero_ce))
        result = self.connection.execute(ins)
        
        
        for ele in result:
            id_poly = ele[0]
        
        #recuperation id polynome
        table = Table("POLYNOME_TABLE_ETALONNAGE", self.meta)
        ins = select([table.c.MOYENNE_INSTRUM, table.c.CORRECTION]).where(table.c.ID_POLYNOME == id_poly)
        result = self.connection.execute(ins)
        table_etal_tlue_correction =[]
        for ele in result:
            table_etal_tlue_correction.append(ele)
            
        return table_etal_tlue_correction
        
        
    def recuperation_resolution_etalon(self, identification_etalon):
        '''fct pour aller cherche la resolution table instrument'''
        
        table = Table("INSTRUMENTS", self.meta)
        ins = select([table.c.RESOLUTION]).where(table.c.IDENTIFICATION == identification_etalon)
        result = self.connection.execute(ins)
        
        
        for ele in result:
            resolution = ele[0]
        
        return resolution
    
    def insertion_ref_emt(self, referentiel):
        '''fct pour inserer dans la table referentiel_conformite '''
        
        table = Table("REFERENTIEL_CONFORMITE", self.meta)
        ins = table.insert()
        result = self.connection.execute(ins, referentiel)
        
    def recuperation_code_client(self):
        '''recupere l'ensemble des codes (appartenant à efs_pl clients dans la table client '''
        Session = sessionmaker(bind= self.engine)
        session = Session()
#        
        
        try:
            table = session.query(self.CLIENT.CODE_CLIENT).\
                    join(self.ENTITE_CLIENT).\
                    filter(self.ENTITE_CLIENT.ABREVIATION == "EFS_CPDL").all()
            
                       
            code = set([x.CODE_CLIENT for x in table])
    #        print(sites)
#            combobox.addItems(list(code))

    #        session.close()
#            return table
            return list(code)
            
        except Exception as e:
            print(e)
            session.rollback()
#            yield None
        finally:
            session.close()
                
        
        
    def recuperation_constructeurs(self):
        '''recupere les constructeurs de la table instrument'''
        
        table = Table("INSTRUMENTS", self.meta)
        ins = select([table.c.CONSTRUCTEUR])
        result = self.connection.execute(ins)    
        constructeur = []
        for ele in result:
            if ele[0] != None:
                constructeur.append(ele[0])

        constructeurs = list(set(constructeur))
        constructeurs.sort()
        return constructeurs
        
    def recuperation_service(self):
        '''recupere le site et le service dans la table correspondant'''
        
        table = Table("CORRESPONDANTS", self.meta)
        ins = select([table.c.SERVICE])
        result = self.connection.execute(ins)    
        
        service = []
        for ele in result:
            service.append(ele[0])       
        services = list(set(service))
        
        return services
        
    def insertion_afficheur(self, afficheur):
        '''fct pour inserer dans la table instruments '''
        
        
        
        
        
        Session = sessionmaker(bind= self.engine)
        session = Session()
#        
        
        try:
            abreviation = session.query(self.CLIENT.PREFIXE_POSTE_TECH_SAP).\
                                      filter(self.CLIENT.CODE_CLIENT == afficheur ["CODE"]).first()[0][-3:]
                
    #        print(abreviation)
    
    #        
    #        except:
    #            session.rollback()
    ##            yield None
    #        finally:
    #            session.close()
            
            
    
            #creation racine de l'afficheur        
            if afficheur["DESIGNATION"] == "Sonde alarme température":
                suffixe = "SAT" + "-" + abreviation
            elif afficheur["DESIGNATION"] == "Afficheur de température":
                suffixe = "AFT" + "-" + abreviation
            elif afficheur["DESIGNATION"] == "Afficheur de temps":
                suffixe = "AFM" + "-" + abreviation
            elif afficheur["DESIGNATION"] == "Afficheur de vitesse":
                suffixe = "AFV" + "-" + abreviation
    
            #creation identification afficheur si afficheur["IDENTIFICATION] == "":
            
            if afficheur["IDENTIFICATION"] == "":
                table = Table("INSTRUMENTS", self.meta)
                ins = select([table.c.IDENTIFICATION]).where(table.c.IDENTIFICATION.contains(suffixe)).order_by(table.c.ID_INSTRUM)
                result = self.connection.execute(ins)
                
                resultat_afficheur =[]
                for ele in result:
    #                print(ele)
                    resultat_afficheur.append(ele[0])
    #            print(resultat_afficheur)
                if len(resultat_afficheur)>= 1:
                    num_afficheur = str(np.amax([int(x[len(x)-4:len(x)]) for x in resultat_afficheur]) + 1).rjust(4, '0')
                else:
                    num_afficheur = str(1).rjust(4, '0')
    #            print("nbr instrument {}".format(num_afficheur.rjust(4, '0')))
                
                afficheur["IDENTIFICATION"] = suffixe + "-" + num_afficheur
    
    
            table = Table("INSTRUMENTS", self.meta)
            ins = table.insert()
            result = self.connection.execute(ins, afficheur)
            
            
            return afficheur["IDENTIFICATION"]
        except Exception as e:
            res = QMessageBox.critical(
                None,
                "Attention",
                f"""Creation impossible erreur : {e}""")
            
#            msg = QMessageBox()
#            msg.setIcon(QMessageBox.warning)
#        
#            msg.setText("This is a message box")
#            msg.setInformativeText("La création n'a pu etre effectuée")
#            msg.setWindowTitle("Attention")
#            res.show()
#            QMessageBox.warning(self, 
#                            "Attention", 
#                            "La création n'a pu etre effectuée") 
                            
            session.rollback()

        finally:
            session.close()
    
    def recuperation_n_ce_actif(self):  
        '''fct qui recupere dans la table afficheur_controle_administratif les n°ce non archivé'''
        table = Table("AFFICHEUR_CONTROLE_ADMINISTRATIF", self.meta)
        ins = select([table.c.NUM_DOC]).where(table.c.ARCHIVAGE == False).order_by(table.c.ID_AFFICHEUR_ADMINISTRATIF)
        result = self.connection.execute(ins)
        num_ce = []
        for ele in result:
            num_ce.append(ele[0])
            
        return num_ce
        
    def recuperation_n_ce(self):  
        '''fct qui recupere dans la table afficheur_controle_administratif les n°ce tous'''
        table = Table("AFFICHEUR_CONTROLE_ADMINISTRATIF", self.meta)
        ins = select([table.c.NUM_DOC]).order_by(table.c.ID_AFFICHEUR_ADMINISTRATIF)
        result = self.connection.execute(ins)
        num_ce = []
        for ele in result:
            num_ce.append(ele[0])
            
        return num_ce
    
    def recuperation_etalonnage_saisie(self, n_ce):
        '''fct qui recupere l'ensemble des donnees'''
#        print("n_ce {}".format(n_ce))
        #table administrative:
        table = Table("AFFICHEUR_CONTROLE_ADMINISTRATIF", self.meta)
        ins = select([table.c.IDENTIFICATION, table.c.DATE_CONTROLE, table.c.NBR_PT, table.c.TECHNICIEN,
                        table.c.ID_AFFICHEUR_ADMINISTRATIF, table.c.COMMENTAIRE_RESULTATS, table.c.ANNULE_REMPLACE, 
                        table.c.TYPE_RAPPORT]).where(table.c.NUM_DOC == n_ce)
        result = self.connection.execute(ins)
        
        for ele in result:
            
#            print("etalonnage {}".format(ele))
            id_identification = ele[0]
            date_ctrl = ele[1]
            nbr_pt = ele[2]
            id_technicien = ele[3]
            id_administratif = ele[4]
            commentaire_resultats = ele[5]
            annule_remplace = ele[6]
            type_rapport = ele[7]
        
        #identification afficheur
        table = Table("INSTRUMENTS", self.meta)
        ins = select([table.c.IDENTIFICATION, table.c.DESIGNATION]).where(table.c.ID_INSTRUM == id_identification)
        result = self.connection.execute(ins)
        for ele in result:
            ident_afficheur = ele[0]
            famille_afficheur = ele[1]
        
        #table cmr
        table = Table("CORRESPONDANTS", self.meta)
        ins = select([table.c.NOM, table.c.PRENOM, table.c.SERVICE, table.c.SITE]).where(table.c.ID_CMR == id_technicien)
        result = self.connection.execute(ins)
        for ele in result:
            cmr = ele[0] + " "+ele[1]#.capitalize()
            service = ele[2]
            site = ele[3]
            
        #table resultat
        table = Table("AFFICHEUR_CONTROLE_RESULTAT", self.meta)
        ins = select([table.c.ID_ETALON, table.c.CE_ETALON, table.c.RESOLUTION]).where(and_(table.c.ID_AFF_CTRL_ADMIN == id_administratif, table.c.N_PT_CTRL == 1))
        result = self.connection.execute(ins)       
               
        for ele in result:
            id_etalon = ele[0]
            n_ce_etalon = ele[1]
            resolution_aff = ele[2]
            
            #recuperation des id referentiel
        table = Table("AFFICHEUR_CONTROLE_RESULTAT", self.meta)
        ins = select([table.c.ID_REF_CONFORMITE]).where(table.c.ID_AFF_CTRL_ADMIN == id_administratif)
        result = self.connection.execute(ins)
        
        list_id_ref_conformite = []
        for ele in result:
            list_id_ref_conformite.append(ele[0])
        
        list_nom_referentiel = []
        for ele in list_id_ref_conformite:
            table = Table("REFERENTIEL_CONFORMITE", self.meta)
            ins = select([table.c.REFERENTIEL]).where(table.c.ID_REFERENTIEL == ele)
            result = self.connection.execute(ins)            
            for element in result:
                list_nom_referentiel.append(element[0])
                
        #date etalonnage etalon et mise en forme du n°CE et date 
        table = Table("POLYNOME_CORRECTION", self.meta)
        ins = select([table.c.DATE_ETAL]).where(table.c.NUM_CERTIFICAT == n_ce_etalon)
        result = self.connection.execute(ins)
        
        for ele in result:
            date_etal_etalon = ele[0]
        mise_forme_n_ce = str(n_ce_etalon +" "+ "du" +" "+ date_etal_etalon.strftime("%d/%m/%y"))
        
        
        #table instrument identification etalon
        table = Table("INSTRUMENTS", self.meta)
        ins = select([table.c.IDENTIFICATION]).where(table.c.ID_INSTRUM == id_etalon)
        result = self.connection.execute(ins)
        for ele in result:
            ident_etalon = ele[0]
        
        #table mesure        
        ensemble_mesures ={}
        for i in range(1, (nbr_pt + 1)):
            
            mesures_etalon_nc = []
            mesures_afficheur = []
            table = Table("AFFICHEUR_CONTROLE_MESURES", self.meta)
            ins = select([table.c.ETALON_NC, table.c.AFFICHEUR]).where(and_(table.c.ID_AFF_CTRL_ADMIN == id_administratif, table.c.N_PT == i)).order_by(table.c.N_MESURE)
            result = self.connection.execute(ins) 
            
            for ele in result:
                mesures_etalon_nc.append(ele[0])
                mesures_afficheur.append(ele[1])
            
            ensemble_mesures[i] = [mesures_etalon_nc, mesures_afficheur]
#        print("ensemble mesure {}".format(ensemble_mesures))
        
        
        #compilation en dictionnaire
        
        saisie = {}
        saisie["type_rapport"] = type_rapport
        saisie["nom_cmr"] = cmr
        saisie["service"] = service
        saisie["site"] = site
        saisie["famille_afficheur"] = famille_afficheur
        saisie["identification_afficheur"] = ident_afficheur
#        print("ident afficheur {}".format(ident_afficheur))
        
        saisie["date_etalonnage"] = date_ctrl
        saisie["identification_etalon"] = ident_etalon
        saisie["n_ce_etalon"] = mise_forme_n_ce
        saisie["resolution_afficheur"] = resolution_aff
        saisie["nb_pt_ctrl"] = nbr_pt
        saisie["nbr_mesure"] = len(ensemble_mesures[1][0])
        saisie["mesures"] = ensemble_mesures
        saisie["referentiel_conformite"] = list_nom_referentiel
        saisie["commentaire_resultats"] = commentaire_resultats
        saisie["annule_remplace"] = annule_remplace
        
        return saisie        
        
        
        
    def mise_a_jour_donnees_saisie(self, afficheur, n_ce):
        '''fct pour la mise à joru des donnees'''
        
        donnees = {}
        #recuperation id instrument*
        table = Table("INSTRUMENTS", self.meta)
        ins = select([table.c.ID_INSTRUM]).where(table .c.IDENTIFICATION == afficheur["identification_instrument"])
        result = self.connection.execute(ins)    
        
        for ele in result:
            id_instrum = ele[0]
                
        #recuperation id cmr
        cmr = afficheur["operateur"].split()
        table = Table("CORRESPONDANTS", self.meta)
        ins = select([table.c.ID_CMR]).where(and_(table .c.NOM == cmr[0], table.c.PRENOM == cmr[1]))
        result = self.connection.execute(ins)    
        
        for ele in result:
            id_cmr = ele[0]
        
        #maj table afficheur_controle admin
        donnees["DATE_CONTROLE"] = afficheur["date_etalonnage"]
        donnees["IDENTIFICATION"] = id_instrum
        donnees["NOM_PROCEDURE"] = "PDL/PIL/SUR/MET/MO" + afficheur["n_mode_operatoire"]
        donnees["NBR_PT"] = afficheur["nbr_pt_etalonnage"]
        donnees["TECHNICIEN"] = id_cmr
        donnees["ARCHIVAGE"] = False
        donnees["COMMENTAIRE_RESULTATS"] = afficheur["commentaire_resultats"]
        donnees["TYPE_RAPPORT"] = afficheur["type_rapport"]
        
            #recuperation id de la ligne a modifier
        table = Table("AFFICHEUR_CONTROLE_ADMINISTRATIF", self.meta)
        ins = select([table.c.ID_AFFICHEUR_ADMINISTRATIF]).where(table.c.NUM_DOC == n_ce)
        result = self.connection.execute(ins) 
        for ele in result:
            id_administratif = ele[0]

        table = Table("AFFICHEUR_CONTROLE_ADMINISTRATIF", self.meta)
        ins = table.update(table.c.NUM_DOC == n_ce)
        result = self.connection.execute(ins, donnees)

        
        #gestion insertion bdd table AFFICHEUR_CONTROLE_RESULTAT
            # recuperation id etalon
            #recuperation id instrument*
        table = Table("INSTRUMENTS", self.meta)
        ins = select([table.c.ID_INSTRUM]).where(table .c.IDENTIFICATION == afficheur["etalon"])
        result = self.connection.execute(ins)    
        
        for ele in result:
            id_etalon = ele[0]

        afficheur["list_referentiel"] = []
        for ele in afficheur["emt"]:
            table = Table("REFERENTIEL_CONFORMITE", self.meta)
            ins = select([table.c.ID_REFERENTIEL]).where(table .c.REFERENTIEL == ele)
            result = self.connection.execute(ins)           
            for ele in result:
                afficheur["list_referentiel"].append(ele[0]) 
        
        n_ce_etalon = afficheur["ce_etalon"][:len(afficheur["ce_etalon"])-12]
        list_table_aff_result = []       
        for i in range(0, donnees["NBR_PT"]):

            dict_table_aff_result = {}
            dict_table_aff_result["ID_AFF_CTRL_ADMIN"] = id_administratif
            dict_table_aff_result["NBR_PT_CTRL"] = donnees["NBR_PT"]
            dict_table_aff_result["N_PT_CTRL"] = i + 1
            dict_table_aff_result["ID_ETALON"] = id_etalon
            dict_table_aff_result["CE_ETALON"] = n_ce_etalon
            dict_table_aff_result["RESOLUTION"] =  afficheur["resolution"][i]
            dict_table_aff_result["MOYENNE_ETALON_NC"] =  np.mean(afficheur["valeurs_etalon_nc"][i])
            dict_table_aff_result["MOYENNE_ETALON_C"] = afficheur["moyenne_etalon_corri"][i]
            dict_table_aff_result["MOYENNE_AFFICHEUR"] = afficheur["moyenne_instrum"][i]
            dict_table_aff_result["MOYENNE_CORRECTION"] = afficheur["moyenne_correction"][i]
            dict_table_aff_result["U"] =  afficheur["U"][i]
            dict_table_aff_result["CONFORMITE"] =  afficheur["conformite"] [i]
            dict_table_aff_result["ARCHIVAGE"] = False
            dict_table_aff_result["ID_REF_CONFORMITE"] =  afficheur["list_referentiel"][i]
            
            list_table_aff_result.append(dict_table_aff_result)
#        print(list_table_aff_result)
        
        for i in range(len(list_table_aff_result)):
            table = Table("AFFICHEUR_CONTROLE_RESULTAT", self.meta)
            ins = table.update(and_(table.c.ID_AFF_CTRL_ADMIN == id_administratif, table.c.N_PT_CTRL == (i+1)))
            result = self.connection.execute(ins, list_table_aff_result[i])


        #Ërecherche id polynome
            
        table = Table("POLYNOME_CORRECTION", self.meta)
        ins = select([table.c.ID_POLYNOME]).where(table .c.NUM_CERTIFICAT == n_ce_etalon)
        result = self.connection.execute(ins)    
        for ele in result:
            id_poly = ele[0]       
        
        for i in range(0, donnees["NBR_PT"]):           
            for j in range(0, len(afficheur["valeurs_etalon_nc"][i])):
                dict_table_mesures = {}
                
                dict_table_mesures["ID_AFF_CTRL_ADMIN"] = id_administratif
                dict_table_mesures["ID_ETALON"] = id_etalon
                dict_table_mesures["ID_POLYNOME"] = id_poly
                dict_table_mesures["ETALON_NC"] = afficheur["valeurs_etalon_nc"][i][j]
                dict_table_mesures["ETALON_C"] = afficheur["valeurs_etalon_c"][i][j]
                dict_table_mesures["AFFICHEUR"] = afficheur["valeurs_afficheur"][i][j]
                dict_table_mesures["NBR_PTS"] = donnees["NBR_PT"]
                dict_table_mesures["N_PT"] = i + 1
                dict_table_mesures["NBR_MESURE"] = len(afficheur["valeurs_etalon_nc"][i])
                dict_table_mesures["N_MESURE"] = j+1

                table = Table("AFFICHEUR_CONTROLE_MESURES", self.meta)
                ins = table.update(and_(table.c.ID_AFF_CTRL_ADMIN == id_administratif, 
                                        table.c.N_PT == (i+1), table.c.N_MESURE == (j+1)))
                result = self.connection.execute(ins, dict_table_mesures)
    
    def validation_ce(self, n_ce):
        
        donnees = {"ARCHIVAGE":True}
        table = Table("AFFICHEUR_CONTROLE_ADMINISTRATIF", self.meta)
        ins = table.update(table.c.NUM_DOC == n_ce)
        result = self.connection.execute(ins, donnees)
        
        
        
        
    def commentaire_referentiel(self, nom_referentiel):
        '''fct pour recupere commentaire sur le referentiel de conformite'''            
        
#        print("nom ref {}".format(nom_referentiel))
        table = Table("REFERENTIEL_CONFORMITE", self.meta)
        ins = select([table.c.COMMENTAIRE_REFERENTIEL]).where(table.c.REFERENTIEL == nom_referentiel)
        result = self.connection.execute(ins) 
        for ele in result:
            commentaire = ele[0]
        return commentaire
        
        
    def mise_a_jour_afficheur(self, afficheur):
        
        
        Session = sessionmaker(bind= self.engine)
        session = Session()
#        
        
        try:
            afficheur["SITE"] = session.query(self.CLIENT.VILLE).\
                                      filter(self.CLIENT.CODE_CLIENT == afficheur ["CODE"]).first()[0]

            
            table = Table("INSTRUMENTS", self.meta)
            ins = table.update(table.c.ID_INSTRUM == afficheur["ID_INSTRUM"])
            self.connection.execute(ins, afficheur)

        except Exception as e:
            print(e)
            session.rollback()

        finally:
            session.close()



    def resultats_prestations_afficheur(self, id_afficheur):
        """recupere l'ensemble des valeurs de la table afficheur resultat en fct id afficheur"""
#        print(id_afficheur)
#       self.RESULT_AFFICHEUR = Base.classes.AFFICHEUR_CONTROLE_RESULTAT
#        self.ADMIN_AFFICHEUR = Base.classes.AFFICHEUR_CONTROLE_ADMINISTRATIF
        
#        df = pd.DataFrame(columns=['MOYENNE_ETALON_C', 'MOYENNE_AFFICHEUR', 'MOYENNE_CORRECTION','U', 'DATE_CONTROLE' ])
#        print(num_ce)
        Session = sessionmaker(bind= self.engine)
        session = Session()
        try:
            list_id = session.query(self.ADMIN_AFFICHEUR.ID_AFFICHEUR_ADMINISTRATIF).\
                    filter(self.ADMIN_AFFICHEUR.IDENTIFICATION == id_afficheur).\
                    order_by(self.ADMIN_AFFICHEUR.ID_AFFICHEUR_ADMINISTRATIF).all()
                    
#            print(list_id)
            
            if list_id:
                list_pandas = []
                for id in list_id:
                    id_admin = id[0]
                    date_ctrl = session.query(self.ADMIN_AFFICHEUR.DATE_CONTROLE).filter(self.ADMIN_AFFICHEUR.ID_AFFICHEUR_ADMINISTRATIF==id_admin).first()
                    num_certificat = session.query(self.ADMIN_AFFICHEUR.NUM_DOC).filter(self.ADMIN_AFFICHEUR.ID_AFFICHEUR_ADMINISTRATIF==id_admin).first()
                    commentaire = session.query(self.ADMIN_AFFICHEUR.COMMENTAIRE_RESULTATS).filter(self.ADMIN_AFFICHEUR.ID_AFFICHEUR_ADMINISTRATIF==id_admin).first()
    #                print(num_certificat)
                    resultat = session.query(self.RESULT_AFFICHEUR.MOYENNE_ETALON_C, 
                                            self.RESULT_AFFICHEUR.MOYENNE_AFFICHEUR, 
                                            self.RESULT_AFFICHEUR.MOYENNE_CORRECTION, 
                                            self.RESULT_AFFICHEUR.U).filter(self.RESULT_AFFICHEUR.ID_AFF_CTRL_ADMIN == id_admin)
                    
                    resultat_pandas = pd.read_sql(resultat.statement, session.bind)
    #                print(len(resultat_pandas.index)) 
                    resultat_pandas.insert(0, 'DATE_CONTROLE', list(itertools.repeat(date_ctrl[0], len(resultat_pandas.index))))
    #                print(resultat_pandas)
                    resultat_pandas.insert(1, 'N_CERTIFICAT', list(itertools.repeat(num_certificat[0], len(resultat_pandas.index))))
    #                print(resultat_pandas)
    #                print(commentaire)
                    resultat_pandas["COMMENTAIRE_RESULTATS"] = commentaire[0]
        #            resultat_pandas["DATE_CONTROLE"] = date_ctrl
    #                print(resultat_pandas)
                
                    list_pandas.append(resultat_pandas)
                
                result = pd.concat(list_pandas)
    #            print(result)
                new_index =[x for x in range(len(result))]
    #                print(new_index)
                result.index = new_index
    #                print(result)
                return result
            else:
                return None

        except Exception as e:
            print(e)
            session.rollback()
            return None
        finally:
            session.close()










