#-*- coding: utf-8 -*-
from sqlalchemy import *
from sqlalchemy.orm import *
from sqlalchemy.engine import create_engine

import numpy as np

class AccesBdd():
    '''class gerant la bdd'''
    
    def __init__(self, engine, meta):
        

#        self.namebdd = "Labo_Metro_Prod"#"Labo_metro_Test_5" #
#        self.adressebdd = "10.42.1.74"#"localhost"#"10.42.1.74"       # #localhost"     
#        self.portbdd = "5434" 
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
        
    def recensement_afficheurs(self, type_afficheur, service, site):
        '''fct pour avoir l'ensemble des afficheurs du type : afficheur_type'''
        
        table = Table("INSTRUMENTS", self.meta)
        ins = table.select().where(and_(table.c.DESIGNATION == type_afficheur, table.c.SITE == site))#, table.c.AFFECTATION == service))

        result = self.connection.execute(ins)
        
        identification_afficheurs = []
        for ele in result:
          identification_afficheurs.append(ele[1])
          
        return  identification_afficheurs
        
    def recensement_afficheurs_complet(self):
        '''recensement de tous les afficheurs'''
        table = Table("INSTRUMENTS", self.meta)
        ins = table.select().where(or_(table.c.DESIGNATION == "Sonde alarme température",
                                    table.c.DESIGNATION == "Afficheur de vitesse", 
                                    table.c.DESIGNATION == "Afficheur de temps", 
                                    table.c.DESIGNATION == "Afficheur de température"))

        result = self.connection.execute(ins)
        
        identification_afficheurs = []
        for ele in result:
          identification_afficheurs.append(ele[1])
          
        return  identification_afficheurs
        
        
    def recensement_etalons(self, type_afficheur, service, site, designation_etalon):
        '''fct pour avoir l'ensemble des afficheurs du type : afficheur_type'''
        
        table = Table("INSTRUMENTS", self.meta)
#        ins = table.select().where(and_(table.c.DOMAINE_MESURE == type_afficheur, table.c.SITE == site, table.c.DESIGNATION == designation_etalon))#, table.c.AFFECTATION == service))
        ins = table.select().where(and_(table.c.DOMAINE_MESURE == type_afficheur)).order_by(table.c.ID_INSTRUM)#, table.c.SITE == site, table.c.DESIGNATION == designation_etalon))#, table.c.AFFECTATION == service))
        
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
                        table.c.ERREUR_TERME_VAR, table.c.ERREUR_UNITE]).where(table.c.DESIGNATION == designation_afficheur).order_by(table.c.ID_REFERENTIEL)

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
                        table.c.AFFECTATION, table.c.SITE]).where(table .c.IDENTIFICATION == identification)
        result = self.connection.execute(ins)    
        
        for ele in result:
#            print("ele {}".format(ele))
            n_serie = ele[0]
            constructeur = ele[1]
            type = ele[2]
            commentaire = ele[3]
            resolution = ele[4]
            affectation = ele[5]
            site = ele[6]
        return n_serie, constructeur, type, commentaire, resolution, affectation, site
    
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
        donnees["NOM_PROCEDURE"] = "PDL/PIL/SUR/MET/MO" + afficheur["n_mode_operatoire"]
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
        table = Table("CLIENTS", self.meta)
        ins = select([table.c.CODE_CLIENT]).where(or_(table.c.SOCIETE.contains("EFS PAYS DE LA LOIRE"), table.c.SOCIETE.contains("ATLANTIC BIO GMP"))).order_by(table.c.ID_CLIENTS)
        result = self.connection.execute(ins)    
        code_client = []
        for ele in result:
            code_client.append(ele[0])
                
        return code_client
        
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
        
        #recuperation du site : 
        if afficheur ["CODE"] == "ABG__-44":
            afficheur["SITE"] = "ST Herblain"
            abreviation = "ABG"            
        elif afficheur ["CODE"] == "EFS  -53":
            afficheur["SITE"] = "LAV"
            abreviation = "LAV"
        elif afficheur ["CODE"] == "EFS  -72":
            afficheur["SITE"] = "LMS"   
            abreviation = "LMS"             
        elif afficheur ["CODE"] == "EFS  -85":
            afficheur["SITE"] = "LRY"
            abreviation = "LRY"         
        elif afficheur ["CODE"] == "EFSNA-44":
            afficheur["SITE"] = "SNA"
            abreviation = "SNA" 
        elif afficheur ["CODE"] == "EFS  -49":
            afficheur["SITE"] = "ANG"
            abreviation = "ANG"
        elif afficheur ["CODE"] == "EFS  -44":
            afficheur["SITE"] = "Nantes" 
            abreviation = "NTS"                    
        elif afficheur ["CODE"] == "EFSNO-44":
            afficheur["SITE"] = "NTSNO"
            abreviation = "NTSNO"
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
        
        #recuperation du site : 
        if afficheur ["CODE"] == "ABG__-44":
            afficheur["SITE"] = "ST Herblain"                      
        elif afficheur ["CODE"] == "EFS  -53":
            afficheur["SITE"] = "LAV"            
        elif afficheur ["CODE"] == "EFS  -72":
            afficheur["SITE"] = "LMS"                       
        elif afficheur ["CODE"] == "EFS  -85":
            afficheur["SITE"] = "LRY"                   
        elif afficheur ["CODE"] == "EFSNA-44":
            afficheur["SITE"] = "SNA"            
        elif afficheur ["CODE"] == "EFS  -49":
            afficheur["SITE"] = "ANG"            
        elif afficheur ["CODE"] == "EFS  -44":
            afficheur["SITE"] = "Nantes"                                
        elif afficheur ["CODE"] == "EFSNO-44":
            afficheur["SITE"] = "NTSNO"
            
        table = Table("INSTRUMENTS", self.meta)
        ins = table.update(table.c.IDENTIFICATION == afficheur["IDENTIFICATION"])
        result = self.connection.execute(ins, afficheur)
