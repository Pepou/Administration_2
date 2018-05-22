#-*- coding: utf-8 -*-
from sqlalchemy import *
from sqlalchemy.orm import *
from sqlalchemy.engine import create_engine
import numpy as np
from datetime import datetime

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
#        self.meta.reflect(bind=self.engine)
        self.table_instruments = Table('INSTRUMENTS', self.meta)
        self.connection = self.engine.connect()
        Session = sessionmaker(bind=self.engine)
        self.session = Session.configure(bind=self.engine)
        
        
    def __del__(self):
        self.connection.close()
    

    def resencement_instrument(self):
        '''retourne tous les identifications des instruments dans une list'''

        result = self.connection.execute('SELECT "IDENTIFICATION", "DOMAINE_MESURE", "DESIGNATION" FROM "INSTRUMENTS"')
        
        instruments = []        
        for ele in result:            
            
            instruments.append(ele) #mise en forme

        return instruments
    def resencement_instrument_utilises(self):
        '''retourne tous les identifications des instruments utilisés dans une list'''

        result = self.connection.execute('''SELECT "IDENTIFICATION", "DOMAINE_MESURE", "DESIGNATION","CODE","AFFECTATION" , "SITE" \
                                            FROM "INSTRUMENTS" \
                                            WHERE "ETAT_UTILISATION" != 'Sommeil' AND "ETAT_UTILISATION" != 'Réformé'\
                                            ORDER BY "ID_INSTRUM" ''')
        
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
    
    def recensement_intervention(self, date_debut, date_fin):
        '''retourne sous forme de list l'ensemble de la table intervention'''
        result = self.connection.execute("""SELECT * FROM "INTERVENTIONS" WHERE "DATE_INTERVENTION" >= '{}' AND "DATE_INTERVENTION" <= '{}' ORDER BY "ID_INTERVENTION" """.format(date_debut, date_fin))
        
        intervention = []        
        for ele in result:            
            
            intervention.append(ele) #mise en forme

        return intervention
        
        
    def recensement_conformite(self, date_debut, date_fin):
        '''fct permettant de connaitre le nbr de non conforme'''
        
        result = self.connection.execute("""SELECT * FROM "CONFORMITE_TEMP_RESULTAT" WHERE "DATE_ETAL" >= '{}' AND "DATE_ETAL" <= '{}' ORDER BY "ID_CONFORMITE" """.format(date_debut, date_fin))
        
        conformite = []        
        for ele in result:            
            
            conformite.append(ele) #mise en forme

        return conformite
        
        
        
        
    def return_code_intrument(self, identification_instrument):
        '''retourne le code instrument'''
        result = self.connection.execute("""SELECT "CODE" FROM "INSTRUMENTS" WHERE "IDENTIFICATION" ='{}'""".format(identification_instrument))
        
        for ele in result:
            code = ele[0]
        return code
        
        
    def indicateur_temperature(self,date_debut, date_fin, parc_temperature):
        indicateurs_temperature = {}
        
        #Campagnes
        table = Table("CAMPAGNE_ETALONNAGE_TEMP", self.meta)
        ins = select([table.c.ID_CAMPAGNE_ETALONNAGE_TEMP]).where(and_(table.c.DATE >= date_debut, table.c.DATE <= date_fin)).order_by(table.c.ID_CAMPAGNE_ETALONNAGE_TEMP)
        result = self.connection.execute(ins)
        id_campagne = []
        for ele in result:
            id_campagne.append(ele[0])
            
            #nbr campagne
        indicateurs_temperature["nbr_campagne"] = len(id_campagne)        
            
            #nbr d'instruments par campagne
        nbr_instrument_par_campagne = []
        for ele in id_campagne:
            table = Table("ETALONNAGE_TEMP_ADMINISTRATION", self.meta)
            ins = select([table.c.IDENTIFICATION_INSTRUM]).where(table.c.ID_CAMPAGNE_ETAL == ele)
            result = self.connection.execute(ins)
            
            instruments_par_campagne = []
            for element in result:
                instruments_par_campagne.append(element[0])
            
            nbr_instrument_par_campagne.append(len(instruments_par_campagne))
        
        indicateurs_temperature["nbr_moyen_intrument_par_campagne"] = np.mean(np.array(nbr_instrument_par_campagne))
        
        indicateurs_temperature["ecart_type_nbr_instrument_campagne"]=np.std(np.array(nbr_instrument_par_campagne), ddof = 1)
         
        indicateurs_temperature["nbr_instruments_max_par_campagne"] = np.amax(np.array(nbr_instrument_par_campagne))
        indicateurs_temperature["nbr_instruments_min_par_campagne"]= np.amin(np.array(nbr_instrument_par_campagne))
         
            #nbr de points d'etalonnage:
        nbr_pt_etal_par_campagne = []
        for ele in id_campagne:
#            print("id campagne {}".format(ele))
            table = Table("ETALONNAGE_TEMP_ADMINISTRATION", self.meta)
            ins = select([table.c.NBR_PT_ETALONNAGE]).where(table.c.ID_CAMPAGNE_ETAL == ele)
            result = self.connection.execute(ins).fetchall()
            
            if len(result) :
                nbr_pt_etal_par_etal = result[0][0]
                nbr_pt_etal_par_campagne.append(nbr_pt_etal_par_etal)
            else :
                pass

        if len(nbr_pt_etal_par_campagne):
        
            indicateurs_temperature["nbr_moyen_pt_etal_par_campagne"] = np.mean(np.array(nbr_pt_etal_par_campagne))
            
            indicateurs_temperature["ecart_type_nbr_pt_etal_campagne"]= np.std(np.array(nbr_pt_etal_par_campagne), ddof = 1)
            indicateurs_temperature["nbr_pt_max_par_campagne"] = np.amax(np.array(nbr_pt_etal_par_campagne))
            indicateurs_temperature["nbr_pt_min_par_campagne"]= np.amin(np.array(nbr_pt_etal_par_campagne))
        else:
            indicateurs_temperature["nbr_moyen_pt_etal_par_campagne"] = 0
            
            indicateurs_temperature["ecart_type_nbr_pt_etal_campagne"]= 0
            indicateurs_temperature["nbr_pt_max_par_campagne"] = 0
            indicateurs_temperature["nbr_pt_min_par_campagne"]= 0
 
 
            #nrb Etalonnage
        table = Table("ETALONNAGE_TEMP_ADMINISTRATION", self.meta)
        ins = select([table.c.ID_ETAL]).where(and_(table.c.DATE_ETAL >= date_debut, table.c.DATE_ETAL <= date_fin))
        result = self.connection.execute(ins)
        id_etal = []
        for element in result:
            id_etal.append(element[0])
        
        indicateurs_temperature["nbr_etalonnage"] = len(id_etal)
        
            #nbr etalonnage air
        table = Table("ETALONNAGE_TEMP_ADMINISTRATION", self.meta)
        ins = select([table.c.ID_ETAL]).where(and_(table.c.DATE_ETAL >= date_debut, table.c.DATE_ETAL <= date_fin, 
                        table.c.NOM_PROC == "PDL/PIL/SUR/MET/MO/030"))
        indicateurs_temperature["nbr_etalonnage_air"] = len(self.connection.execute(ins).fetchall())
        
            #nbr etalonnage liquide
        table = Table("ETALONNAGE_TEMP_ADMINISTRATION", self.meta)
        ins = select([table.c.ID_ETAL]).where(and_(table.c.DATE_ETAL >= date_debut, table.c.DATE_ETAL <= date_fin, 
                        or_(table.c.NOM_PROC == "PDL/PIL/SUR/MET/MO/025", table.c.NOM_PROC == "PDL/PIL/SUR/MET/MO/052")))
        indicateurs_temperature["nbr_etalonnage_liquide"] = len(self.connection.execute(ins).fetchall())
        
        
        #Interventions
        table = Table("ETALONNAGE_TEMP_ADMINISTRATION", self.meta)
        ins = select([table.c.IDENTIFICATION_INSTRUM, table.c.DATE_ETAL]).where(and_(table.c.DATE_ETAL >= date_debut, table.c.DATE_ETAL <= date_fin))
        result = self.connection.execute(ins)
        list_instruments = []
        for element in result:
            list_instruments.append(element)
        indicateurs_temperature["list_instruments_etalonnes"] = list_instruments
        
        #nr de reception:
        table = Table("INTERVENTIONS", self.meta)
        ins = select([table.c.IDENTIFICATION, table.c.CODE_CLIENT, table.c.DATE_INTERVENTION])\
                        .where(and_(table.c.DATE_INTERVENTION >= date_debut, 
                        table.c.DATE_INTERVENTION <= date_fin,\
                        table.c.INTERVENTION == "Réception" ))\
                        .order_by(table.c.ID_INTERVENTION)
        list_instruments_receptionnes = self.connection.execute(ins).fetchall()
        identification_instrum_temp = [x[0] for x in parc_temperature]
        list_instruments_receptionnes_temperature  = set([x[0] for x in list_instruments_receptionnes if x[0] in identification_instrum_temp])
        

        indicateurs_temperature["nbr_instruments_receptionnes"] = len(list_instruments_receptionnes_temperature)
        indicateurs_temperature["list_instruments_receptionnes"] = list_instruments_receptionnes_temperature
        #nbr expedition
        table = Table("INTERVENTIONS", self.meta)
        ins = select([table.c.IDENTIFICATION, table.c.CODE_CLIENT, table.c.DATE_INTERVENTION])\
                        .where(and_(table.c.DATE_INTERVENTION >= date_debut, 
                        table.c.DATE_INTERVENTION <= date_fin,\
                        or_(table.c.INTERVENTION == "Expedition" , table.c.INTERVENTION == "Expédition")))\
                        .order_by(table.c.ID_INTERVENTION)
        list_instruments_expedies = self.connection.execute(ins).fetchall()
        list_instruments_expedies_temperature  = set([x[0] for x in list_instruments_expedies if x[0] in identification_instrum_temp])

        indicateurs_temperature["nbr_instruments_expedies"] = len(list_instruments_expedies_temperature)
        indicateurs_temperature["list_instruments_expedies"] = list_instruments_expedies_temperature
        
        list_error_temperature = [x for x in list_instruments_receptionnes_temperature if x not in list_instruments_expedies_temperature]
        list_error_temperature_bis = [x for x in list_instruments_expedies_temperature if x not in list_instruments_receptionnes_temperature]
        
        indicateurs_temperature["list_instruments_receptionnes_non_expedies"] = list_error_temperature
        indicateurs_temperature["list_instruments_expedies_non_receptionnes"] = list_error_temperature_bis
        #Conformite
        table = Table("CONFORMITE_TEMP_RESULTAT", self.meta)
        ins = table.select().where(and_(table.c.DATE_ETAL >= date_debut, 
                        table.c.DATE_ETAL <= date_fin))
        indicateurs_temperature["nbr_declaration_conformite"] = len(self.connection.execute(ins).fetchall())
#        print(indicateurs_temperature["nbr_declaration_conformite"])
        
        table = Table("CONFORMITE_TEMP_RESULTAT", self.meta)
        ins = table.select().where(and_(table.c.DATE_ETAL >= date_debut, 
                        table.c.DATE_ETAL <= date_fin, table.c.CONCLUSION == "Conforme"))
        indicateurs_temperature["nbr_instruments_conforme"] = len(self.connection.execute(ins).fetchall())
#        print(indicateurs_temperature["nbr_instruments_conforme"])
        
        table = Table("CONFORMITE_TEMP_RESULTAT", self.meta)
        ins = table.select().where(and_(table.c.DATE_ETAL >= date_debut, 
                        table.c.DATE_ETAL <= date_fin, table.c.CONCLUSION == "Non Conforme"))
        indicateurs_temperature["nbr_instruments_non_conforme"] = len(self.connection.execute(ins).fetchall())
#        print(indicateurs_temperature["nbr_instruments_non_conforme"])
        
        return indicateurs_temperature


    def indicateurs_afficheur(self, date_debut, date_fin, parc_afficheur):
        table = Table("AFFICHEUR_CONTROLE_ADMINISTRATIF", self.meta)
        ins = select([table.c.ID_AFFICHEUR_ADMINISTRATIF, table.c.IDENTIFICATION, table.c.DATE_CONTROLE, table.c.NBR_PT]).where(and_(table.c.DATE_CONTROLE >= date_debut, table.c.DATE_CONTROLE <= date_fin)).order_by(table.c.DATE_CONTROLE)
        list_id_afficheur = self.connection.execute(ins).fetchall()

        #print(list_id_afficheur)

        conformite =[]
        for ele in list_id_afficheur:
            #print(ele[0])

            table = Table("AFFICHEUR_CONTROLE_RESULTAT", self.meta)
            ins = select([table.c.CONFORMITE]).where(table.c.ID_AFF_CTRL_ADMIN == ele[0])
            resultat = self.connection.execute(ins).fetchone()
        
            conformite.append((ele[1], ele[2],resultat[0], ele[3]))

        ctrl_afficheur = []

        for ele in conformite:

            table = Table("INSTRUMENTS", self.meta)
            ins = select([table.c.IDENTIFICATION]).where(table.c.ID_INSTRUM == str(ele[0]))
            afficheur = self.connection.execute(ins).fetchone()
            
            ctrl_afficheur.append((afficheur[0], ele[1], ele[2], ele[3]))
            
#        print(ctrl_afficheur)
        indicateur_afficheur = {}
        indicateur_afficheur["list_afficheurs"] = ctrl_afficheur
        indicateur_afficheur ["Nbr_controle"] = len (ctrl_afficheur)
        
        conforme = [x[2] for x in ctrl_afficheur if x[2] == "Conforme"]
#        print(conforme)
        non_conforme = [x[2] for x in ctrl_afficheur if x[2] == "Non Conforme"]
        
        nbr_pt = [x[3] for x in ctrl_afficheur ]
        indicateur_afficheur["nbr_pt_moyen_afficheur"] = np.mean(np.array(nbr_pt))
        indicateur_afficheur["ecart_type_nbr_pt_afficheur"]=np.std(np.array(nbr_pt), ddof = 1)
        indicateur_afficheur["nbr_pt_max_afficheur"] = np.amax(np.array(nbr_pt))
        indicateur_afficheur["nbr_pt_min_afficheur"]= np.amin(np.array(nbr_pt))
        
        indicateur_afficheur["nbr_afficheurs_conformes"] = len(conforme)
        indicateur_afficheur["nbr_afficheurs_non_conformes"] = len(non_conforme)
        
        
        
        
        
        
         #nr de reception:
        table = Table("INTERVENTIONS", self.meta)
        ins = select([table.c.IDENTIFICATION, table.c.CODE_CLIENT, table.c.DATE_INTERVENTION])\
                        .where(and_(table.c.DATE_INTERVENTION >= date_debut, 
                        table.c.DATE_INTERVENTION <= date_fin,\
                        table.c.INTERVENTION == "Réception" ))\
                        .order_by(table.c.ID_INTERVENTION)
        list_instruments_receptionnes = self.connection.execute(ins).fetchall()
        identification_afficheurs = [x[0] for x in parc_afficheur]
        list_afficheurs_receptionnes  = [x[0] for x in list_instruments_receptionnes if x[0] in identification_afficheurs]


        indicateur_afficheur["nbr_afficheurs_receptionnes"] = len(list_afficheurs_receptionnes)
        indicateur_afficheur["list_afficheurs_receptionnes"] = list_afficheurs_receptionnes
        #nbr expedition
        table = Table("INTERVENTIONS", self.meta)
        ins = select([table.c.IDENTIFICATION, table.c.CODE_CLIENT, table.c.DATE_INTERVENTION])\
                        .where(and_(table.c.DATE_INTERVENTION >= date_debut, 
                        table.c.DATE_INTERVENTION <= date_fin,\
                        or_(table.c.INTERVENTION == "Expedition", table.c.INTERVENTION == "Expédition" )))\
                        .order_by(table.c.ID_INTERVENTION)
        list_instruments_expedies = self.connection.execute(ins).fetchall()
        list_afficheurs_expedies  = [x[0] for x in list_instruments_expedies if x[0] in identification_afficheurs]
        indicateur_afficheur["nbr_afficheurs_expedies"] = len(list_afficheurs_expedies)
        indicateur_afficheur["list_instruments_expedies"] = list_afficheurs_expedies
        
        list_error_afficheur = [x for x in list_afficheurs_receptionnes if x not in list_afficheurs_expedies]
        list_error_afficheur_bis = [x for x in list_afficheurs_expedies if x not in  list_afficheurs_receptionnes]
        
        indicateur_afficheur["list_afficheur_receptionnes_non_expedies"] = list_error_afficheur
        indicateur_afficheur["list_afficheur_expedies_non_receptionnes"] = list_error_afficheur_bis
        
        
        

        return indicateur_afficheur
        

    def indicateur_delais(self,date_debut, date_fin, parc_instruments ):
#        print("parc instrum {}".format(parc_instruments))
#        print("date debut {} date fin {}".format(date_debut, date_fin))
        set_designation = set([x[2] for x in parc_instruments])
#        print(set_designation)

              #delais d'etalonnage : 
        
        table = Table("INTERVENTIONS", self.meta)
        ins = select([table.c.IDENTIFICATION, table.c.CODE_CLIENT, table.c.DATE_INTERVENTION])\
                        .where(and_(table.c.DATE_INTERVENTION >= date_debut, 
                        table.c.DATE_INTERVENTION <= date_fin,\
                        or_(table.c.INTERVENTION == "Expedition" ,table.c.INTERVENTION == "Expédition" )))\
                        .order_by(table.c.ID_INTERVENTION)
        list_instruments_expedies = self.connection.execute(ins).fetchall()
#        print("intrum expedie {}".format(list_instruments_expedies))
#        list_recep_expe_delais = []
        indicateur_delais = {}
        
        for designation in set_designation:
            list_recep_expe_delais = []
#            print(designation)
            
            instrument_par_designation = [x[0] for x in parc_instruments if x[2] == designation]
            list_instruments_expedies_par_designation = [x for x in list_instruments_expedies if x[0] in instrument_par_designation]
#            print(" designation {} parc {}".format(designation, list_instruments_expedies_par_designation))

            for ele in list_instruments_expedies_par_designation:
                
                #reception
                table = Table("INTERVENTIONS", self.meta)
                ins = select([table.c.IDENTIFICATION, table.c.DATE_INTERVENTION])\
                            .where(and_(table.c.DATE_INTERVENTION <= ele[2], 
                            table.c.IDENTIFICATION == ele[0], 
                            table.c.INTERVENTION == "Réception"))\
                            .order_by(desc(table.c.ID_INTERVENTION))
                reception = self.connection.execute(ins).fetchone()
                
                if reception != None:
                    delais = (ele[2] - reception[1]).days
    #                print(ele[2].strftime("%d-%m-%Y"))
                    list_recep_expe_delais.append((ele[0], reception[1], ele[2], delais))
            indicateur_delais["list_instruments_recep_expe_delais" +  " " + str(designation)] = list_recep_expe_delais
        
            list_delais = [ele[3] for ele in list_recep_expe_delais]

            if len(list_delais) != 0 : 
                indicateur_delais["delais_moyen_immobilisation" + " " + str(designation)] = np.mean(np.array(list_delais))
                indicateur_delais["ecart_type_immobilisation" +  " " + str(designation)] = np.std(np.array(list_delais), ddof = 1)
                indicateur_delais["delais_max_immobilisation" +  " " + str(designation)] = np.amax(np.array(list_delais))
                indicateur_delais["delais_min_immobilisation" +  " " + str(designation)]= np.amin(np.array(list_delais))
                
            
#        for designation in set_designation:
#            
#            for ele in indicateur_delais.keys():
#            
#                if designation in ele :
#                    print("{} valeurs : {}".format(ele, indicateur_delais[ele]))
        
        
        return indicateur_delais
        
        
        
    def instrument_temperature_etal(self, date_debut, date_fin):
        '''fct pour recuperer chaine de temperature etalonnées'''
        
        table = Table("ETALONNAGE_TEMP_ADMINISTRATION", self.meta)
        ins = select([table.c.IDENTIFICATION_INSTRUM, table.c.IDENTIFICATION_INSTRUM, table.c.DATE_ETAL]).where(and_(table.c.DATE_ETAL >= date_debut, table.c.DATE_ETAL <= date_fin))
        list_instruments = self.connection.execute(ins).fetchall()

        list_id = []
        for ele in list_instruments:

            table = Table("INSTRUMENTS", self.meta)
            ins = select([table.c.ID_INSTRUM, table.c.CODE, table.c.AFFECTATION, table.c.SITE]).where(table.c.IDENTIFICATION == str(ele[0]))
            id = self.connection.execute(ins).fetchone()
            
            list_id.append((id[0], ele[0], ele[1], id[1], id[2], id[3]))
            

        
        indicateurs_temperature = []
        for ele in list_id:
            table = Table("CONFORMITE_TEMP_RESULTAT", self.meta)
            ins = select([table.c.CONCLUSION]).where(and_(table.c.DATE_ETAL >= date_debut, 
                        table.c.DATE_ETAL <= date_fin,  table.c.ID_INSTRUM == ele[0]))
            
            conformite = self.connection.execute(ins).fetchone()

            if conformite != None:                
            
                indicateurs_temperature.append((ele[0],ele[1], ele[2], conformite[0], ele[3], ele[4], ele[5]))
            else: 
                indicateurs_temperature.append((ele[0],ele[1], ele[2],  "NONE",  ele[3], ele[4], ele[5]))
                
        return indicateurs_temperature
        
#        
    def afficheur_etal(self, date_debut, date_fin):
        '''fct pour recuperer chaine de temperature etalonnées'''
        
        table = Table("AFFICHEUR_CONTROLE_ADMINISTRATIF", self.meta)
        ins = select([table.c.ID_AFFICHEUR_ADMINISTRATIF, table.c.IDENTIFICATION, table.c.DATE_CONTROLE]).where(and_(table.c.DATE_CONTROLE >= date_debut, table.c.DATE_CONTROLE <= date_fin)).order_by(table.c.DATE_CONTROLE)
        list_id_afficheur = self.connection.execute(ins).fetchall()

        
        conformite =[]
        for ele in list_id_afficheur:

            table = Table("AFFICHEUR_CONTROLE_RESULTAT", self.meta)
            ins = select([table.c.CONFORMITE]).where(table.c.ID_AFF_CTRL_ADMIN == ele[0])
            resultat = self.connection.execute(ins).fetchone()
        
            conformite.append((ele[1], ele[2],resultat))

        indicateur_afficheur = []

        for ele in conformite:

            table = Table("INSTRUMENTS", self.meta)
            ins = select([table.c.IDENTIFICATION, table.c.CODE, table.c.AFFECTATION, table.c.SITE]).where(table.c.ID_INSTRUM == str(ele[0]))
            afficheur = self.connection.execute(ins).fetchone()
            
            indicateur_afficheur.append((afficheur[0], ele[1], ele[2], afficheur[1], afficheur[2], afficheur[3]))
            

        return indicateur_afficheur
        
        
    def delais_export_excel(self, date_debut, date_fin, parc_instruments ):
            
#        print("parc {}".format(parc_instruments))
        
        set_designation = set([x[2] for x in parc_instruments])

              #delais d'etalonnage : 
        
        table = Table("INTERVENTIONS", self.meta)
        ins = select([table.c.IDENTIFICATION, table.c.CODE_CLIENT, table.c.DATE_INTERVENTION])\
                        .where(and_(table.c.DATE_INTERVENTION >= date_debut, 
                        table.c.DATE_INTERVENTION <= date_fin,\
                        or_(table.c.INTERVENTION == "Expedition" , table.c.INTERVENTION == "Expédition")))\
                        .order_by(table.c.ID_INTERVENTION)
        list_instruments_expedies = self.connection.execute(ins).fetchall()
        
        
        indicateur_delais = {}
        
        for designation in set_designation:
            list_recep_expe_delais = []
            
            instrument_par_designation = [x[0] for x in parc_instruments if x[2] == designation]
            list_instruments_expedies_par_designation = [x for x in list_instruments_expedies if x[0] in instrument_par_designation]
            
#            print("list_instrumenst expedies {}".format(list_instruments_expedies_par_designation))
            
            for ele in list_instruments_expedies_par_designation:
                
                #reception
                table = Table("INTERVENTIONS", self.meta)
                ins = select([table.c.IDENTIFICATION, table.c.DATE_INTERVENTION])\
                            .where(and_(table.c.DATE_INTERVENTION <= ele[2], 
                            table.c.IDENTIFICATION == ele[0], 
                            table.c.INTERVENTION == "Réception"))\
                            .order_by(desc(table.c.ID_INTERVENTION))
                reception = self.connection.execute(ins).fetchone()
                
                if reception != None:
                    delais = (ele[2] - reception[1]).days
                    list_recep_expe_delais.append((ele[0], reception[1], ele[2], delais))
            
            mise_en_forme_list_recep_expe_delais = []
            for ele in list_recep_expe_delais:
                
                affectation = [(ele[0], ele[1], ele[2],ele[3], x[3], x[4], x[5])for x in parc_instruments if x[0] == ele[0]]
                
                mise_en_forme_list_recep_expe_delais.append(affectation[0]) 
                
#            print(mise_en_forme_list_recep_expe_delais)
            
            indicateur_delais[designation] = mise_en_forme_list_recep_expe_delais
            

        return indicateur_delais
        
        
        
        
    def recup_date_pb_expedition_reception(self, date_debut, date_fin, list_instrum):
        
        list_finale =[]
        for ele in list_instrum:                
            
            table = Table("INTERVENTIONS", self.meta)
            ins = select([table.c.DATE_INTERVENTION])\
                        .where(and_(table.c.DATE_INTERVENTION <= date_fin, 
                        table.c.DATE_INTERVENTION >= date_debut))
                        
            date = self.connection.execute(ins).fetchone()
            list_finale.append((ele, date[0]))
            
        return list_finale
            
                
