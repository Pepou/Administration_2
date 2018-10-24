#-*-coding:Latin-1 -*
from PyQt4 import  QtSql
#from PyQt4 import QtCore, QtGui
#from PyQt4.QtGui import QMessageBox
#import datetime
import os
import json

class GestionBdd:
    
    def __init__(self, nom):
        '''Constructeur de la classe'''
        
        # fichier config bdd :
        with open("config_bdd.json") as json_file:
            config_bdd = json.load(json_file)
#            print(config_bdd)

        
        self.nombdd = config_bdd["name_bdd"] #Labo_Metro_Prod"#"Test_carac_generateurs"#"Labo_Metro_Prod"# #
        self.adressebdd = config_bdd["adresse_bdd"]#"10.42.1.74" #"localhost"  #"10.42.1.74"          
        self.portbdd = int(config_bdd["port_bdd"])
        
        self.path_bdd = os.path.abspath("BDD/saisie_etal_temp_test.db")
#         = "Labo_Metro_Prod"#"Test_Labo_Temp"# #Labo_Metro_Test_4"#
        self.nom = nom
#        self.model = QtSql.QSqlTableModel()
    
    def premiere_connexion(self, login, password):
        '''Fonction a utiliser lors de la premiere connexion du logiciel'''
        
        type_bdd = QtSql.QSqlDatabase.addDatabase('QPSQL')
        type_bdd.setHostName(self.adressebdd)#('localhost') #('10.42.1.74')            # 
        type_bdd.setPort(self.portbdd)
        type_bdd.setDatabaseName(self.nombdd)
        type_bdd.setUserName(login) 
        type_bdd.setPassword(password)
        a = type_bdd.open()
#        print("ouverture base postgresql {}".format(a))
#        self.gestion_combobox_onglet_config_2()
        return a
        
    def reconnexion(self):
        '''Permet de se reconnecter à la bdd'''
        db = QtSql.QSqlDatabase()
        
    
    def fermeture(self):
        db = QtSql.QSqlDatabase()
        db.close()
    
    def remove_connexion_database(self):
        db = QtSql.QSqlDatabase()
        db.close()
        db.removeDatabase(self.path_bdd)
        
    def gestion_combobox_onglet_config(self):
        '''Fonction qui va chercher l'ensemble des instruments dans la base et renvoi une list
        La fonction utilise un qttablemodel'''
        
        model = QtSql.QSqlTableModel()
        model.setTable("INSTRUMENTS")
        model.select()
                
        #recupere le nombre de lignes
        while model.canFetchMore():
            model.fetchMore()
           
        nb_row = model.rowCount()
       
        #Gestion des differentes listes possibles sur la bdd permet d'alimenter les combobox configration etalonnage
        instrum = []
        list_instrum = []
        list_identification_instrum = []
                  
        a = 1
        while a < nb_row:
            record = model.record(a)
            instrum = [record.value("IDENTIFICATION"), record.value("N_SERIE"), \
                                record.value("CONSTRUCTEUR"), record.value("TYPE"), record.value("RESOLUTION")]
            list_instrum.append(instrum)
            list_identification_instrum.append(record.value("IDENTIFICATION"))
    
            a +=1
#        print("list instrum {}".format(list_identification_instrum))
        return list_identification_instrum
        
    
    
    def gestion_combobox_onglet_config_2(self):
        query = QtSql.QSqlQuery()

        requete =str("""SELECT "IDENTIFICATION" FROM "INSTRUMENTS" """\
                            +"""WHERE "DOMAINE_MESURE" = 'Température' OR "DOMAINE_MESURE" = 'TEMPÉRATURE' """\
                            +"""AND "TYPE" != 'Generateur de Temperature' """\
                            +"""AND "DESIGNATION" != 'Afficheur de température' """\
                            +"""AND "DESIGNATION" != 'Sonde alarme température' ORDER BY "IDENTIFICATION";""")
        
        query.exec_(requete)  
        list_identification_instrum = []
            
        while query.next() :
            list_identification_instrum.append(query.value(0))
                        
        query.finish()
        
                
        return list_identification_instrum
    
    
    
    def gestion_combobox_onglet_operateur(self):
        model = QtSql.QSqlTableModel()        
        model.setTable("TECHNICIEN")
        model.select()
        list_technicien = []
          
        a=0
        nb_row = model.rowCount()
        
        while a < nb_row:
            record = model.record(a)
            list_technicien.append(record.value("PRENOM"))
        
            a +=1
            
        return list_technicien
        
        
    def gestion_combobox_onglet_operateur_2(self):
        query = QtSql.QSqlQuery()

        requete =str("""SELECT "PRENOM" FROM "TECHNICIEN" ORDER BY "ID_TECHNICIEN";""")
        query.exec_(requete)  
        technicien = []
            
        while query.next() :
            technicien.append(query.value(0))
                        
        query.finish()
        
        return technicien
        
    
    def gestion_remplissage_onglet_config(self, ident_instrum):
        '''fonction qui va chercher le 
        -n° serie
        -constructeur
        -type'
        et les renvoies'''
        
        #creer et configure le model
        model = QtSql.QSqlTableModel()
        model.setTable("INSTRUMENTS")
        model.select()
                
        #creer et configure le model
        model.setFilter("IDENTIFICATION =\""+ ident_instrum +"\"") #attention on est obligé de declarer les retour à la ligne
        model.select
        
        #Recuperation des donnees
        record= model.record(0)
        n_serie = record.value("N_SERIE")
        constructeur = record.value("CONSTRUCTEUR")
        type = record.value("TYPE")
        commentaire = record.value("COMMENTAIRE")
        resolution = record.value("RESOLUTION")
                
        return n_serie , constructeur, type, resolution , commentaire
        
    def gestion_remplissage_onglet_config_2(self, ident_instrum):
        
        try:
            query = QtSql.QSqlQuery()
    
            requete =str("""SELECT "N_SERIE","CONSTRUCTEUR","TYPE","COMMENTAIRE","RESOLUTION" """\
                                +""" FROM "INSTRUMENTS" WHERE "IDENTIFICATION" = '{}' ;""".format(ident_instrum))
            
            query.exec_(requete)  
                    
            while query.next() :
                n_serie = query.value(0)
                constructeur = query.value(1)
                type = query.value(2)
                commentaire = query.value(3)
                resolution = query.value(4)
                            
            query.finish()
            
            return n_serie , constructeur, type, resolution , commentaire
        except UnboundLocalError:
            n_serie = "L'instrument n'existe pas dans la BDD"
            constructeur = "L'instrument n'existe pas dans la BDD"
            type = "L'instrument n'existe pas dans la BDD"
            commentaire = "L'instrument n'existe pas dans la BDD"
            resolution = "L'instrument n'existe pas dans la BDD"
            return n_serie , constructeur, type, resolution , commentaire
            pass
            
    def recherche_id_instrument(self, ident_instrum):
        '''fonction qui renvoie id_instrum en fct de son ident'''        
        query = QtSql.QSqlQuery()
        requete = """SELECT "ID_INSTRUM" FROM "INSTRUMENTS" WHERE "IDENTIFICATION" = '{}';""".format(ident_instrum)
        query.exec_(requete)
        
        while query.next() :
            id_instrum = query.value(0)
                    
        query.finish()
        return id_instrum
        
    def recherche_identification_instrument(self,id_instrum ):
        '''fonction qui renvoie ident instrum en fct de son id '''        
        query = QtSql.QSqlQuery()
        requete = """SELECT "IDENTIFICATION" FROM "INSTRUMENTS" WHERE "ID_INSTRUM" = '{}';""".format(id_instrum)
        
        query.exec_(requete)
        
        while query.next() :
            ident_instrum = query.value(0)
                    
        query.finish()
        return ident_instrum
        
    def recherche_identification_instrument_num_ce(self,num_certificat ):
        '''fonction qui renvoie ident instrum en fct de son num_ce sur la table etalonnage temp administration '''        
        query = QtSql.QSqlQuery()
        requete = """SELECT "IDENTIFICATION_INSTRUM" FROM "ETALONNAGE_TEMP_ADMINISTRATION" WHERE "NUM_DOCUMENT" = '{}';""".format(num_certificat)
#        print(requete)
        query.exec_(requete)
        
        while query.next() :
            ident_instrum = query.value(0)
                    
        query.finish()
        return ident_instrum
        
        
        
    def gestion_combobox_etalon(self):
        query = QtSql.QSqlQuery()

        requete =str("""SELECT "IDENTIFICATION" FROM "INSTRUMENTS" WHERE ("DESIGNATION" = 'Etalon' OR "DESIGNATION" = 'Etalon de Référence')
                                                                        AND "ETAT_UTILISATION" = 'En service' ORDER BY "ID_INSTRUM";""")
        query.exec_(requete)  
        etalons = []
            
        while query.next() :
            etalons.append(query.value(0))
                        
        query.finish()
        
        return etalons
    
    def gestion_combobox_generateur(self):
        
        query = QtSql.QSqlQuery()

        requete =str("""SELECT "IDENTIFICATION" FROM "INSTRUMENTS" WHERE "DESIGNATION" = 'Bain de Glace Fondante' AND "ETAT_UTILISATION" = 'En service' ORDER BY "ID_INSTRUM";""")
        query.exec_(requete)  
        
        generateurs = []
        while query.next() :
            generateurs.append(query.value(0))

        requete =str("""SELECT "IDENTIFICATION" FROM "INSTRUMENTS" WHERE "DESIGNATION" = 'Bain d''etalonnage' AND "ETAT_UTILISATION" = 'En service' ORDER BY "ID_INSTRUM";""")
        query.exec_(requete)  
        while query.next() :
            generateurs.append(query.value(0))
         
        requete =str("""SELECT "IDENTIFICATION" FROM "INSTRUMENTS" WHERE "DESIGNATION" = 'Enceinte climatique' AND "ETAT_UTILISATION" = 'En service' ORDER BY "ID_INSTRUM";""")
        query.exec_(requete)  
        while query.next() :
            generateurs.append(query.value(0))
            
        
        query.finish()
        
        return generateurs
        
    def insertion_table_campagne_etal(self, nom_campagne, date_etal, id_instrum):
        '''fonction qui gere l'insertion de donnees dans la table campagne etal
        Attention id_instrum est une list
        '''
        query = QtSql.QSqlQuery()
        requete = """INSERT INTO "CAMPAGNE_ETALONNAGE_TEMP" ("ARCHIVAGE", "NOM_CAMPAGNE_ETAL", "DATE", "ID_INST_1", "ID_INST_2", "ID_INST_3", "ID_INST_4", "ID_INST_5", "ID_INST_6","""\
                    +""" "ID_INST_7", "ID_INST_8", "ID_INST_9", "ID_INST_10", "ID_INST_11", "ID_INST_12","""\
                    +""" "ID_INST_13", "ID_INST_14", "ID_INST_15", "ID_INST_16", "ID_INST_17", "ID_INST_18","""\
                    +""" "ID_INST_19", "ID_INST_20") VALUES('{}', '{}', {}, {}, {}, {}, {}, {}, {}, {}, {}, {}, {}, {}, {}, {}, {}, {}, {}, {}, {}, {}, {});"""\
                    .format("FALSE", nom_campagne, date_etal, id_instrum[0], id_instrum[1], id_instrum[2], id_instrum[3], id_instrum[4], 
                                    id_instrum[5], id_instrum[6], id_instrum[7], id_instrum[8], id_instrum[9], id_instrum[10], 
                                    id_instrum[11], id_instrum[12], id_instrum[13], id_instrum[14], id_instrum[15],
                                    id_instrum[16], id_instrum[17], id_instrum[18], id_instrum[19])
        
        query.exec_(requete) 
        query.finish()
        
        
    def insertion_table_campagne_etal_2(self, nom_campagne, date_etal, id_instrum):
        '''fonction qui gere l'insertion de donnees dans la table campagne etal
        et utilise le returning de postgresql
        '''
        query = QtSql.QSqlQuery()
        requete = """INSERT INTO "CAMPAGNE_ETALONNAGE_TEMP" ("ARCHIVAGE", "NOM_CAMPAGNE_ETAL", "DATE", "ID_INST_1", "ID_INST_2", "ID_INST_3", "ID_INST_4", "ID_INST_5", "ID_INST_6","""\
                    +""" "ID_INST_7", "ID_INST_8", "ID_INST_9", "ID_INST_10", "ID_INST_11", "ID_INST_12","""\
                    +""" "ID_INST_13", "ID_INST_14", "ID_INST_15", "ID_INST_16", "ID_INST_17", "ID_INST_18","""\
                    +""" "ID_INST_19", "ID_INST_20") VALUES('{}', '{}', '{}', {}, {}, {}, {}, {}, {}, {}, {}, {}, {}, {}, {}, {}, {}, {}, {}, {}, {}, {}, {}) RETURNING "ID_CAMPAGNE_ETALONNAGE_TEMP";"""\
                    .format("FALSE", nom_campagne, date_etal, id_instrum[0], id_instrum[1], id_instrum[2], id_instrum[3], id_instrum[4], 
                                    id_instrum[5], id_instrum[6], id_instrum[7], id_instrum[8], id_instrum[9], id_instrum[10], 
                                    id_instrum[11], id_instrum[12], id_instrum[13], id_instrum[14], id_instrum[15],
                                    id_instrum[16], id_instrum[17], id_instrum[18], id_instrum[19])
#        print("requete insertion_table_campagne_etal {}".format(requete))
        query.exec_(requete)
        while query.next() :
            id_campagne = query.value(0)
        
        query.finish()
        return id_campagne
        
    def recherche_id_campagne_etal(self):
        ''' fct recupere l'id de la derniere camapgne cree'''
        
        query = QtSql.QSqlQuery()
        requete = """SELECT "ID_CAMPAGNE_ETALONNAGE_TEMP" FROM "CAMPAGNE_ETALONNAGE_TEMP" """\
                        +"""ORDER BY "ID_CAMPAGNE_ETALONNAGE_TEMP" DESC"""\
                        +""" LIMIT 1;"""
#        print("requete recherche_id_campagne_etal {}".format(requete))
        query.exec_(requete)
        while query.next():
            id_campagne_etal = query.value(0)
            
        query.finish()
        
        return id_campagne_etal
        
    def recherche_n_ce_id_campagne_identification_instrum(self, id_campagne_etal_particuliere, identification_instrum):
        '''fct qui va chercher le numero d'etalonnage en fct de l'id campagne etal et l'identification de l'instrument'''
        
        query = QtSql.QSqlQuery()
        requete = """SELECT "NUM_DOCUMENT","ANNULE_NUM_DOC" FROM "ETALONNAGE_TEMP_ADMINISTRATION" """\
                        +"""WHERE "ID_CAMPAGNE_ETAL" = {} AND "IDENTIFICATION_INSTRUM" = '{}';"""\
                        .format(id_campagne_etal_particuliere, identification_instrum)
#        print("recherche_n_ce_id_campagne_identification_instrum : {}".format(requete))
        query.exec_(requete)
        while query.next():
            num_doc = query.value(0)
            annule = query.value(1)
#        print(annule)
#        print(type(annule))
        if not isinstance(annule, str):
           annule = "Neant"
        query.finish()
        return num_doc, annule
        
        
    def recherche_caract_instrument(self, nom_instrum):
        '''fcontion qui va chercher dans la base les caracteristiques de l'instruments
         en fonction de son nom '''
         
        query = QtSql.QSqlQuery()
        requete =str("""SELECT "N_SERIE", "CONSTRUCTEUR", "DESIGNATION", "TYPE", "CODE", "AFFECTATION", "DESIGNATION_LITTERALE" FROM "INSTRUMENTS" WHERE "IDENTIFICATION" = {};""".format(nom_instrum))
        query.exec_(requete)
        
        while query.next() :
                n_serie =  str("'"+str(query.value(0))+"'")
                n_serie_bis = str(query.value(0))
                constructeur =  str(query.value(1))
                designation = str(query.value(2))
                designation_litterale = str(query.value(6))                
                type = str(query.value(3))
                affectation = query.value(5)                
                code_client = str("'"+str(query.value(4))+"'")
##        print(type(designation_litterale))
#        print(designation_litterale)
        if isinstance(affectation, str):
            pass
        else:
            if affectation.isNull() == True:
                affectation = "Neant"
        
        if isinstance(designation_litterale, str) and designation_litterale != "None" and  "PyQt4.QtCore.QPyNullVariant" not in designation_litterale :
            designation_finale = designation +" "+ "/" + " "+ designation_litterale
        else:
            designation_finale = designation
        query.finish()
        return n_serie, n_serie_bis, constructeur, designation_finale, type, affectation, code_client
        
    
    def recuperation_id_operateur(self, prenom, nom):
        '''recupere l id à partir du prenom et du non '''
        query = QtSql.QSqlQuery()
        requete =str("""SELECT "ID_TECHNICIEN", "PRENOM", "NOM" FROM "TECHNICIEN" """\
                            +"""WHERE "PRENOM" = '{}' AND "NOM" = '{}';""".format(prenom, nom))
#        print(requete)
        query.exec_(requete)        
            
        while query.next() :
            id_technicien = query.value(0)
            
        query.finish()
        return id_technicien
    
    
    
    def recherche_technicien_depuis_id(self, id_operateur):
        ''' va chercher les info sur le technicien en fction de son id dans la base et renvoi le prenom_nom'''
        
        query = QtSql.QSqlQuery()
        requete =str("""SELECT "PRENOM", "NOM" FROM "TECHNICIEN" WHERE "ID_TECHNICIEN" = {};""".format(id_operateur))
        
#        print("requete recherche_technicien_depuis_id {}".format(requete))
        query.exec_(requete)        
            
        while query.next() :
            technicien =  str("'"+str(query.value(0)) +" "+str(query.value(1))+"'")
            technicien_bis = str(query.value(0)) +" "+str(query.value(1))
            
        query.finish()
        return technicien, technicien_bis
            
    def recherche_client(self, code_client):
        '''fonction qui va chercher les données du client'''
        query = QtSql.QSqlQuery()
        requete =str("""SELECT "SOCIETE", "ADRESSE", "CODE_POSTAL", "VILLE" FROM "CLIENTS" WHERE "CODE_CLIENT" = {};""".format(str(code_client)))
#        print(requete)
        query.exec_(requete)
        
#        print("requete recherche_client {}".format(requete))
        while query.next() :
            societe = str(query.value(0))
            adresse= str(query.value(1))
            code_postal = str(query.value(2))
            ville = str(query.value(3))
            
        query.finish()
        return societe, adresse, code_postal, ville
    
    def recherche_n_inventaire(self, identification_instrum, n_serie): # il s'agit n SAP
        ''' fonction qui va chercher le n SAP dans la base'''
            
        query = QtSql.QSqlQuery()
        requete =str("""SELECT "N_SAP_PM" FROM "INSTRUMENTS" WHERE "IDENTIFICATION" = {};""".format(identification_instrum))
        query.exec_(requete) 
        while query.next() :
            n_sap =  query.value(0)
        
        if n_sap is None  :
            requete =str("""SELECT "N_INVENTAIRE" FROM "PARC_SAP" WHERE "N_SERIE_FABRICANT" = {};""".format(n_serie))
            query.exec_(requete) 
            while query.next() :
                n_sap =  query.value(0)
        
#        print("conversion booleen n _sap {}".format(bool(n_sap)))
        query.finish()
        return n_sap
    
    def insertion_table_etalonnage_temp_administration(self,id_campagne_etal, nbr_pt_etalonnage, 
                                                                                    n_sap, identification_instrum, date_etal, 
                                                                                    nom_procedure, num_doc, edit_ce, edit_cv, 
                                                                                    technicien, ville_etal, domaine_accreditation, 
                                                                                    numero_accreditation, nbr_pages_annexe, 
                                                                                    laboratoire):
        '''Fonction qui réalise l'insertion dans la table etal temp administration'''
            
        query = QtSql.QSqlQuery()
        requete = """INSERT INTO "ETALONNAGE_TEMP_ADMINISTRATION" """\
                            +"""("ID_CAMPAGNE_ETAL", "NBR_PT_ETALONNAGE","""\
                            +""" "N_SAP", "IDENTIFICATION_INSTRUM", "DATE_ETAL", "NOM_PROC","""\
                            +""" "NUM_DOCUMENT", "EDIT_CE", "EDIT_CV", "TECHNICIEN", "VILLE_ETAL","""\
                            +""" "DOMAINE_ACCRED", "NUM_ACCRED",  "NB_PAGES_ANNEXE", "LABORATOIRE", "ARCHIVAGE")"""\
                            +""" VALUES({}, {}, {}, {}, {}, {}, {}, {}, {}, {}, {}, {}, {}, {}, {}, 'FALSE');"""\
                                .format(id_campagne_etal,nbr_pt_etalonnage, n_sap, identification_instrum,\
                                            date_etal, nom_procedure, num_doc, edit_ce, edit_cv, technicien, \
                                            ville_etal, domaine_accreditation, numero_accreditation, nbr_pages_annexe, \
                                            laboratoire)

        query.exec_(requete) 
        query.finish()
        
    def insertion_table_etalonnage_temp_administration_2(self,id_campagne_etal, nbr_pt_etalonnage, 
                                                                                    n_sap, identification_instrum, date_etal, 
                                                                                    nom_procedure, num_doc, edit_ce, edit_cv, 
                                                                                    technicien, ville_etal, domaine_accreditation, 
                                                                                    numero_accreditation, nbr_pages_annexe, 
                                                                                    laboratoire, etat_reception):
        '''Fonction qui réalise l'insertion dans la table etal temp administration et utilise RETURNING de postgresql'''
            
        query = QtSql.QSqlQuery()
        requete = """INSERT INTO "ETALONNAGE_TEMP_ADMINISTRATION" """\
                            +"""("ID_CAMPAGNE_ETAL", "NBR_PT_ETALONNAGE","""\
                            +""" "N_SAP", "IDENTIFICATION_INSTRUM", "DATE_ETAL", "NOM_PROC","""\
                            +""" "NUM_DOCUMENT", "EDIT_CE", "EDIT_CV", "TECHNICIEN", "VILLE_ETAL","""\
                            +""" "DOMAINE_ACCRED", "NUM_ACCRED", "NBR_PAGES_ANNEXE", "LABORATOIRE", "ARCHIVAGE", "ETAT_RECEPTION")"""\
                            +""" VALUES({}, {}, '{}', {}, '{}', {}, {}, {}, {}, {}, {}, {}, {}, {}, {}, 'FALSE', '{}') RETURNING "ID_ETAL";"""\
                                .format(id_campagne_etal, nbr_pt_etalonnage, n_sap, identification_instrum, \
                                            date_etal, nom_procedure, num_doc, edit_ce, edit_cv, technicien, \
                                            ville_etal, domaine_accreditation, numero_accreditation, nbr_pages_annexe, \
                                            laboratoire, etat_reception)
#        print(requete)
        query.exec_(requete) 
        
        while query.next() :
            id_etalonnage_temp_administration = query.value(0)
        
        query.finish()
        return id_etalonnage_temp_administration
       
    def mise_a_jour_table_etalonnage_temp_administration(self,id_campagne_etal, identification_ancien_instrum, nbr_pt_etalonnage, 
                                                                                    n_sap, identification_instrum, date_etal, 
                                                                                    nom_procedure, num_doc, edit_ce, edit_cv, 
                                                                                    technicien, ville_etal, domaine_accreditation, 
                                                                                    numero_accreditation, nbr_pages_annexe, 
                                                                                    laboratoire, etat_reception):
        '''Fonction qui réalise la mise a jour dans la table etal temp administration'''
            
        query = QtSql.QSqlQuery()
        requete = """UPDATE "ETALONNAGE_TEMP_ADMINISTRATION" SET"""\
                        +""" "ID_CAMPAGNE_ETAL" = {}, "NBR_PT_ETALONNAGE" = {},""".format(id_campagne_etal, nbr_pt_etalonnage) \
                        +""" "N_SAP" = '{}', "IDENTIFICATION_INSTRUM" = {}, "DATE_ETAL" = '{}', "NOM_PROC" = {},""".format(n_sap, identification_instrum, date_etal, nom_procedure) \
                        +""" "NUM_DOCUMENT" = '{}', "EDIT_CE" = {}, "EDIT_CV" = {}, "TECHNICIEN" = {}, "VILLE_ETAL" = {},""".format(num_doc[0], edit_ce, edit_cv, technicien, ville_etal) \
                        +""" "DOMAINE_ACCRED" = {}, "NUM_ACCRED" = {},  "NBR_PAGES_ANNEXE" = {}, "LABORATOIRE" = {},""".format(domaine_accreditation, numero_accreditation, nbr_pages_annexe, laboratoire) \
                        +""" "ARCHIVAGE" = '{}',""" .format("FALSE") \
                        +""" "ETAT_RECEPTION" = '{}' """.format(etat_reception) \
                        +""" WHERE "IDENTIFICATION_INSTRUM" = '{}' AND "ID_CAMPAGNE_ETAL" = {} ;""".format(identification_ancien_instrum, id_campagne_etal)
#        print("mise_a_jour_table_etalonnage_temp_administration : {}".format(requete))
        query.exec_(requete) 
        query.finish()  
    
    def mise_a_jour_table_etalonnage_temp_administration_2(self,id_campagne_etal, nbr_pt_etalonnage, 
                                                                                    n_sap, identification_instrum, date_etal, 
                                                                                    nom_procedure, num_doc, edit_ce, edit_cv, 
                                                                                    technicien, ville_etal, domaine_accreditation, 
                                                                                    numero_accreditation, nbr_pages_annexe, 
                                                                                    laboratoire, etat_reception, id_etalonnage_temp_administration):
        '''Fonction qui réalise la mise a jour dans la table etal temp administration specialement pour le bouton enregistrement'''
            
        query = QtSql.QSqlQuery()
        requete = """UPDATE "ETALONNAGE_TEMP_ADMINISTRATION" SET"""\
                        +""" "ID_CAMPAGNE_ETAL" = {}, "NBR_PT_ETALONNAGE" = {},""".format(id_campagne_etal, nbr_pt_etalonnage) \
                        +""" "N_SAP" = '{}', "IDENTIFICATION_INSTRUM" = {}, "DATE_ETAL" = '{}', "NOM_PROC" = {},""".format(n_sap, identification_instrum, date_etal, nom_procedure) \
                        +""" "NUM_DOCUMENT" = '{}', "EDIT_CE" = {}, "EDIT_CV" = {}, "TECHNICIEN" = {}, "VILLE_ETAL" = {},""".format(num_doc, edit_ce, edit_cv, technicien, ville_etal) \
                        +""" "DOMAINE_ACCRED" = {}, "NUM_ACCRED" = {},  "NBR_PAGES_ANNEXE" = {}, "LABORATOIRE" = {},""".format(domaine_accreditation, numero_accreditation, nbr_pages_annexe, laboratoire) \
                        +""" "ARCHIVAGE" = '{}',""" .format("FALSE") \
                        +""" "ETAT_RECEPTION" = '{}' """.format(etat_reception) \
                        +""" WHERE "ID_ETAL" = {} ;""".format(id_etalonnage_temp_administration)
#        print(requete)
        query.exec_(requete) 
        query.finish() 
        
        
    def mise_a_jour_table_etalonnage_temp_administration_annule_remplace_2(self,id_campagne_etal, nbr_pt_etalonnage, 
                                                                                n_sap, identification_instrum, date_etal, 
                                                                                nom_procedure, num_doc, edit_ce, edit_cv, 
                                                                                technicien, ville_etal, domaine_accreditation, 
                                                                                numero_accreditation, nbr_pages_annexe, 
                                                                                laboratoire, annule_remplace, etat_reception, id_etalonnage_temp_administration):
        '''Fonction qui réalise l'insertion dans la table etal temp administration et utilise la fct returning de postgresql'''
        
        query = QtSql.QSqlQuery()
        requete = """UPDATE "ETALONNAGE_TEMP_ADMINISTRATION" SET"""\
                        +""" "ID_CAMPAGNE_ETAL" = {},""".format(id_campagne_etal)\
                        + """ "NBR_PT_ETALONNAGE" = {},""".format(nbr_pt_etalonnage)\
                        +""" "N_SAP" = '{}',""".format(n_sap)\
                        +""" "IDENTIFICATION_INSTRUM" = {},""".format(identification_instrum)\
                        +""" "DATE_ETAL" = '{}',""".format(date_etal)\
                        +""" "NOM_PROC" = {},""".format(nom_procedure)\
                        +""" "NUM_DOCUMENT" = '{}',""".format(num_doc)\
                        +""" "EDIT_CE" = {},""".format(edit_ce)\
                        +""" "EDIT_CV" = {},""".format(edit_cv)\
                        +""" "TECHNICIEN" = {},""".format(technicien)\
                        +""" "VILLE_ETAL" = {},""".format(ville_etal)\
                        +""" "DOMAINE_ACCRED" = {},""".format(domaine_accreditation)\
                        +""" "NUM_ACCRED" = {},""".format(numero_accreditation)\
                        +""" "NBR_PAGES_ANNEXE" = {},""".format(nbr_pages_annexe)\
                        +""" "LABORATOIRE" = {},""".format(laboratoire)\
                        +""" "ARCHIVAGE" = {},""".format('FALSE')\
                        +""" "ANNULE_NUM_DOC" = '{}',""".format(annule_remplace)\
                        +""" "ETAT_RECEPTION" = '{}' """.format(etat_reception)\
                        +""" WHERE "ID_ETAL" = {} ;""".format(id_etalonnage_temp_administration)
                            
#        print(requete)
        query.exec_(requete) 
     
        query.finish()
        
 
     
     
     
    def insertion_table_etalonnage_temp_administration_annule_remplace(self,id_campagne_etal, nbr_pt_etalonnage, 
                                                                                    n_sap, identification_instrum, date_etal, 
                                                                                    nom_procedure, num_doc, edit_ce, edit_cv, 
                                                                                    technicien, ville_etal, domaine_accreditation, 
                                                                                    numero_accreditation, nbr_pages_annexe, 
                                                                                    laboratoire, annule_remplace):
        '''Fonction qui réalise l'insertion dans la table etal temp administration'''
            
        query = QtSql.QSqlQuery()
        requete = """INSERT INTO "ETALONNAGE_TEMP_ADMINISTRATION" """\
                            +"""("ID_CAMPAGNE_ETAL", "NBR_PT_ETALONNAGE","""\
                            +""" "N_SAP", "IDENTIFICATION_INSTRUM", "DATE_ETAL", "NOM_PROC","""\
                            +""" "NUM_DOCUMENT", "EDIT_CE", "EDIT_CV", "TECHNICIEN", "VILLE_ETAL","""\
                            +""" "DOMAINE_ACCRED", "NUM_ACCRED", "NBR_PAGES_ANNEXE", "LABORATOIRE", "ARCHIVAGE", "ANNULE_NUM_DOC")"""\
                            +""" VALUES({}, {}, '{}', {}, {}, {}, {}, {}, {}, {}, {}, {}, {}, {}, {}, 'FALSE', '{}');"""\
                                .format(id_campagne_etal, nbr_pt_etalonnage, n_sap, identification_instrum,\
                                            date_etal, nom_procedure, num_doc, edit_ce, edit_cv, technicien, \
                                            ville_etal, domaine_accreditation, numero_accreditation, nbr_pages_annexe, \
                                            laboratoire, annule_remplace)

#        print(requete)
        query.exec_(requete) 
        query.finish()
        
    def insertion_table_etalonnage_temp_administration_annule_remplace_2(self,id_campagne_etal, nbr_pt_etalonnage, 
                                                                                    n_sap, identification_instrum, date_etal, 
                                                                                    nom_procedure, num_doc, edit_ce, edit_cv, 
                                                                                    technicien, ville_etal, domaine_accreditation, 
                                                                                    numero_accreditation, nbr_pages_annexe, 
                                                                                    laboratoire, annule_remplace, etat_reception):
        '''Fonction qui réalise l'insertion dans la table etal temp administration et utilise la fct returning de postgresql'''
            
        query = QtSql.QSqlQuery()
        requete = """INSERT INTO "ETALONNAGE_TEMP_ADMINISTRATION" """\
                            +"""("ID_CAMPAGNE_ETAL", "NBR_PT_ETALONNAGE","""\
                            +""" "N_SAP", "IDENTIFICATION_INSTRUM", "DATE_ETAL", "NOM_PROC","""\
                            +""" "NUM_DOCUMENT", "EDIT_CE", "EDIT_CV", "TECHNICIEN", "VILLE_ETAL","""\
                            +""" "DOMAINE_ACCRED", "NUM_ACCRED", "NBR_PAGES_ANNEXE", "LABORATOIRE", "ARCHIVAGE", "ANNULE_NUM_DOC", "ETAT_RECEPTION")"""\
                            +""" VALUES({}, {}, '{}', {}, '{}', {}, '{}', {}, {}, {}, {}, {}, {}, {}, {}, 'FALSE', '{}', '{}') RETURNING "ID_ETAL";"""\
                                .format(id_campagne_etal, nbr_pt_etalonnage, n_sap, identification_instrum,\
                                            date_etal, nom_procedure, num_doc, edit_ce, edit_cv, technicien, \
                                            ville_etal, domaine_accreditation, numero_accreditation, nbr_pages_annexe, \
                                            laboratoire, annule_remplace, etat_reception)

#        print(requete)
        query.exec_(requete) 
        while query.next() :
            id_etalonnage_temp_administration = query.value(0)
        query.finish()
        return id_etalonnage_temp_administration
        
    def recherche_id_etalonnage_admin(self):
        '''fonction qui recupere le dernier id cree dans la table etalonnage_temp_administration'''
        
        query = QtSql.QSqlQuery()
        requete = """SELECT "ID_ETAL" FROM "ETALONNAGE_TEMP_ADMINISTRATION" """\
                        +""" ORDER BY "ID_ETAL" DESC"""\
                        +""" LIMIT 1;"""
    
        query.exec_(requete)
        while query.next():
            id_etalonnage_temp_administration = query.value(0)
            
        query.finish()
        return id_etalonnage_temp_administration
    
    def recherche_id_etalonnage_admin_id_campagne_identification_instrum(self, id_campagne_etal, identification_instrum):
        '''fonction qui va chercher l'id de la table etalonnage" admin en fct e l'id campagne etal et identification materiel'''
        
        query = QtSql.QSqlQuery()
        requete = """SELECT "ID_ETAL" FROM "ETALONNAGE_TEMP_ADMINISTRATION" """\
                        +"""WHERE "ID_CAMPAGNE_ETAL" = {} AND "IDENTIFICATION_INSTRUM" = '{}';"""\
                        .format(id_campagne_etal, identification_instrum )
#        print(requete)
        query.exec_(requete)
        
#        print("requete :recherche_id_etalonnage_admin_id_campagne_identification_instrum {} ".format(requete))
        while query.next():
            id_etalonnage_temp_administration = query.value(0)
            
        query.finish()
        return id_etalonnage_temp_administration
                        
                        
    def recherche_id_etalonnage_num_doc(self, num_certificat):
        '''fonction qui va chercher l'id de la table etalonnage" en fct num certificat '''
        
        query = QtSql.QSqlQuery()
        requete = """SELECT "ID_ETAL" FROM "ETALONNAGE_TEMP_ADMINISTRATION" """\
                        +"""WHERE "NUM_DOCUMENT" = '{}' ;"""\
                        .format(num_certificat )
#        print(requete)
        query.exec_(requete)
        
#        print("requete :recherche_id_etalonnage_admin_id_campagne_identification_instrum {} ".format(requete))
        while query.next():
            id_etalonnage_temp_administration = query.value(0)
            
        query.finish()
        return id_etalonnage_temp_administration
                                            
                        
    def insertion_table_etalonnage_mesure(self, id_etalonnage_temp_administration, id_campagne_etal, 
                                                                correction, num_doc, identification_instrum, nbr_pt_etalonnage,
                                                                num_pt_etalonnage, nbr_mesure, numero_mesure, mesure_etal_non_corri,
                                                                mesure_etal_corri, mesure_instrum, id_poly):
        '''fonction qui insert les valeurs saisies dans la table etalonnage mesure'''
        
        query = QtSql.QSqlQuery()
        requete = """INSERT INTO "ETALONNAGE_MESURE" ("ID_CAMPAGNE_ETAL",""" \
                                    +""" "ID_ETALONNAGE", "CORRECTION", "NUM_DOCUMENT", "IDENTIFICATION", "NBR_PT_ETALONNAGE","""\
                                    +""" "NUM_PT_ETAL", "NBR_MESURE_PAR_PT", "NUM_MESURE", "MESURE_ETAL_NC", """\
                                    +""" "MESURE_ETAL_C", "MESURE_INSTRUM","ID_POLY_ETALON")""" \
                                    +""" VALUES({}, {}, {}, '{}', {}, {}, {}, {}, {}, {}, {}, {}, {});""".\
                                    format(id_campagne_etal, id_etalonnage_temp_administration, correction, num_doc, \
                                            identification_instrum, nbr_pt_etalonnage, num_pt_etalonnage, nbr_mesure, \
                                            numero_mesure, mesure_etal_non_corri, mesure_etal_corri, mesure_instrum, id_poly)
                    
#        print(requete)
        query.exec_(requete)
        query.finish()
        
        
    def mise_a_jour_table_etalonnage_mesure(self, id_etalonnage_temp_administration, id_campagne_etal, 
                                                                correction, num_doc, identification_instrum, nbr_pt_etalonnage,
                                                                num_pt_etalonnage, nbr_mesure, numero_mesure, mesure_etal_non_corri,
                                                                mesure_etal_corri, mesure_instrum, id_etal_mesures, id_polynome_etalon):
        ''' fct qui gere la mise à jour de la table etalonnage mesure en fct de l'id_etal_mesures'''
        
        query = QtSql.QSqlQuery()
        requete = """UPDATE "ETALONNAGE_MESURE" SET"""\
                        +""" "ID_CAMPAGNE_ETAL" = {},""".format(id_campagne_etal) \
                        +""" "ID_ETALONNAGE" = {}, """.format(id_etalonnage_temp_administration)\
                        +""" "CORRECTION" = {}, """.format(correction)\
                        +""" "NUM_DOCUMENT" = '{}',""".format(num_doc[0])\
                        +""" "IDENTIFICATION" = {},""".format(identification_instrum)\
                        +""" "NBR_PT_ETALONNAGE" = {},""".format(nbr_pt_etalonnage)\
                        +""" "NUM_PT_ETAL" = {},""".format(num_pt_etalonnage)\
                        +""" "NBR_MESURE_PAR_PT" = {},""".format(nbr_mesure)\
                        +""" "NUM_MESURE" = {},""".format(numero_mesure)\
                        +""" "MESURE_ETAL_NC" = {},""".format(mesure_etal_non_corri)\
                        +""" "MESURE_ETAL_C" = {},""".format(mesure_etal_corri)\
                        +""" "MESURE_INSTRUM" = {}, """.format(mesure_instrum) \
                        +""" "ID_POLY_ETALON" = {} """.format(id_polynome_etalon)\
                        +"""WHERE "ID_ETAL_MESURES" = {};""".format(id_etal_mesures, numero_mesure)
                                    
#        print("requete mise_a_jour_table_etalonnage_mesure {}".format(requete))
        query.exec_(requete)
        query.finish()
        
    def recherche_id_etalonnage_mesure_id_campagne_id_etal(self, id_campagne_etal, id_etalonnage_temp_administration, numero_mesure , num_pt_etal):
        '''fcontion qui l''id de la table etalonnage mesure en fct de la campagne d'etal
        et de l'id etal temp administratif ainsi que du numero de la mesure'''
        query = QtSql.QSqlQuery()
        requete = """SELECT "ID_ETAL_MESURES" """\
                        +"""FROM "ETALONNAGE_MESURE" """\
                        +"""WHERE "ID_CAMPAGNE_ETAL" = {} AND "ID_ETALONNAGE" = {} AND "NUM_MESURE" = {} AND "NUM_PT_ETAL" = {};"""\
                        .format(id_campagne_etal, id_etalonnage_temp_administration, numero_mesure, num_pt_etal)
#        print(requete)
        query.exec_(requete)
        
#        print("requete id_etalonnage_mesure_id_campagne_id_etal {}".format(requete))
#        id_etal_mesures = []
        while query.next():
            id_etal_mesures = query.value(0)
            
        query.finish()
        return id_etal_mesures
        
    def insertion_table_etalonnage_resultat(self, temp_consigne, id_campagne_etal, id_etalonnage_temp_administration,
                                                                    nom_etalon, nom_generateur, autoechauffement , fuite_thermique, 
                                                                    resolution, stabilite, eiv, num_doc, identification_instrum, date_etal, 
                                                                    nbr_pt_etalonnage, num_pt_etalonnage, moyenne_etalon_non_corri, 
                                                                    moyenne_etalon_corri, moyenne_instrum, moyenne_correction, U, 
                                                                    ecart_type, immersion, valeur_resolution_instrument):
        '''fonction qui insert les donnees dans la table etalonnage resultat'''
        query = QtSql.QSqlQuery()
        requete = """INSERT INTO "ETALONNAGE_RESULTAT" ("TEMP_CONSIGNE", "ID_CAMPAGNE_ETAL","""\
                                +""" "ID_ETALONNAGE", "NOM_ETALON", "NOM_GENERATEUR", "AUTOECHAUFFEMENT","""\
                                +""" "FUITE_THERMIQUE", "RESOLUTION", "STABILITE", "EIV_MEILLEURE_COURANTE_U","""\
                                +""" "NUM_ETAL", "CODE_INSTRUM", "DATE_ETAL", "NBR_PTS_ETAL", "NUM_PT_ETAL","""\
                                +""" "MOYENNE_ETALON_NC", "MOYENNE_ETAL_C", "MOYENNE_INSTRUM","""\
                                +""" "MOYENNE_CORRECTION", "U", "ECART_TYPE", "IMMERSION", "RESOLUTION_INSTRUMENT") """\
                                +"""VALUES({}, {}, {}, {}, {}, {}, {}, {}, {}, {}, '{}', {}, '{}', {}, {}, {}, {}, {}, {}, {}, {}, '{}', {});""".\
                                format(temp_consigne, id_campagne_etal, id_etalonnage_temp_administration,
                                            nom_etalon, nom_generateur, autoechauffement , fuite_thermique, 
                                            resolution, stabilite, eiv, num_doc, identification_instrum, date_etal, 
                                            nbr_pt_etalonnage, num_pt_etalonnage, moyenne_etalon_non_corri, 
                                            moyenne_etalon_corri, moyenne_instrum, moyenne_correction, U, 
                                            ecart_type, immersion, valeur_resolution_instrument)
#        print("insertion table resultat {}".format(requete))
        query.exec_(requete)
        query.finish()
        
        
    def mis_a_jour_table_etalonnage_resultat(self, temp_consigne, id_campagne_etal, id_etalonnage_temp_administration,
                                                                    nom_etalon, nom_generateur, autoechauffement , fuite_thermique, 
                                                                    resolution, stabilite, eiv, num_doc, identification_instrum, date_etal, 
                                                                    nbr_pt_etalonnage, num_pt_etalonnage, moyenne_etalon_non_corri, 
                                                                    moyenne_etalon_corri, moyenne_instrum, moyenne_correction, U, 
                                                                    ecart_type, immersion, valeur_resolution_instrument, id_etal_result):
                                        
        '''Mise à jour table etalonnage resultat en fct de l'id_etal_resultat'''
        query = QtSql.QSqlQuery()
        requete = """UPDATE "ETALONNAGE_RESULTAT" SET"""\
                                +""" "TEMP_CONSIGNE" = {},""".format(temp_consigne)\
                                +""" "ID_CAMPAGNE_ETAL" = {},""".format(id_campagne_etal)\
                                +""" "ID_ETALONNAGE" = {},""".format(id_etalonnage_temp_administration)\
                                +""" "NOM_ETALON" = {},""".format(nom_etalon)\
                                +""" "NOM_GENERATEUR" = {},""".format(nom_generateur)\
                                +""" "AUTOECHAUFFEMENT" = {},""".format(autoechauffement)\
                                +""" "FUITE_THERMIQUE" = {},""".format(fuite_thermique)\
                                +""" "RESOLUTION" = {},""".format(resolution)\
                                +""" "STABILITE" = {},""".format(stabilite)\
                                +""" "EIV_MEILLEURE_COURANTE_U" = {},""".format(eiv)\
                                +""" "NUM_ETAL" = '{}',""".format(num_doc[0])\
                                +""" "CODE_INSTRUM" = {},""".format(identification_instrum)\
                                +""" "DATE_ETAL" = '{}',""".format(date_etal)\
                                +""" "NBR_PTS_ETAL" = {},""".format(nbr_pt_etalonnage)\
                                +""" "NUM_PT_ETAL" = {},""".format(num_pt_etalonnage)\
                                +""" "MOYENNE_ETALON_NC" = {},""".format(moyenne_etalon_non_corri)\
                                +""" "MOYENNE_ETAL_C" = {},""".format(moyenne_etalon_corri)\
                                +""" "MOYENNE_INSTRUM" = {},""".format(moyenne_instrum)\
                                +""" "MOYENNE_CORRECTION" = {},""".format(moyenne_correction)\
                                +""" "U" = {},""".format(U)\
                                +""" "ECART_TYPE" = {},""".format(ecart_type)\
                                +""" "IMMERSION" = '{}',""".format(immersion)\
                                +""" "RESOLUTION_INSTRUMENT" = {}""".format(valeur_resolution_instrument)\
                                +""" WHERE "ID_ETAL_RESULT" = {} ;""".format(id_etal_result)\
                                
#        print("requete mis_a_jour_table_etalonnage_resultat {}".format(requete))
        query.exec_(requete)
        query.finish()
        
        
        
        
        
    def recherche_id_etal_result_table_etalonnage_resultat(self, id_campagne_etal, id_etalonnage_temp_administration):
        '''fct qui recupere tout les id_etal_resultat pour un etalonnage particulier'''
        query = QtSql.QSqlQuery()
        requete = """SELECT "ID_ETAL_RESULT" """\
                        +"""FROM "ETALONNAGE_RESULTAT" """\
                        +"""WHERE "ID_CAMPAGNE_ETAL" = {} AND "ID_ETALONNAGE" = {} ORDER BY "ID_ETAL_RESULT";"""\
                        .format(id_campagne_etal, id_etalonnage_temp_administration)
#        print(requete)
        query.exec_(requete)
        id_etal_result = []
        while query.next():
            id_etal_result.append(query.value(0))
            
        query.finish()
        return id_etal_result        
        
    def archivage_polynome(self, identification_instrum, num_doc, date_etal):
        '''fct qui' archive tous les polynome precedent l'etalonnage'''
        query = QtSql.QSqlQuery()
        requete = """UPDATE "POLYNOME_CORRECTION" SET "ARCHIVAGE" = 'TRUE' """\
                        +"""WHERE "IDENTIFICATION" = {} AND  "DATE_ETAL" <= '{}';"""\
                        .format(identification_instrum, date_etal)
#        print(requete)                
        query.exec_(requete)
        query.finish()
                        
    def insertion_table_polynome(self, identification_instrum,date_du_jour_mise_en_forme, num_doc,
                                                    date_etal, ordre_poly,a, b, c, archivage):
        ''' fct qui insere le poly dans la table polynome'''
        
        query = QtSql.QSqlQuery()
        requete = """INSERT INTO "POLYNOME_CORRECTION" ("IDENTIFICATION", "DATE_CREATION_POLY","""\
                                +""" "NUM_CERTIFICAT", "DATE_ETAL", "ORDRE_POLY", "COEFF_A","""\
                                +""" "COEFF_B", "COEFF_C", "ARCHIVAGE") """\
                                +"""VALUES({}, {}, '{}', '{}', {}, {}, {}, {}, {});""".\
                                    format(identification_instrum, date_du_jour_mise_en_forme, num_doc, \
                                                date_etal, ordre_poly, a, b, c, archivage )
#        print("requete insertion poly {}".format(requete) )      
        query.exec_(requete)
        
        query.finish()
        
    def mise_a_jour_table_polynome(self, identification_instrum,date_du_jour_mise_en_forme, num_doc,
                                                    date_etal, ordre_poly,a, b, c, archivage):
        '''fct qui met à jour la table polynome en fct du numero de certificat'''
        query = QtSql.QSqlQuery()
        requete = """UPDATE "POLYNOME_CORRECTION" SET"""\
                        +""" "IDENTIFICATION" = {},""".format(identification_instrum)\
                        +""" "DATE_CREATION_POLY" = {},""".format(date_du_jour_mise_en_forme)\
                        +""" "DATE_ETAL" = '{}',""".format(date_etal)\
                        +""" "ORDRE_POLY" = {},""".format(ordre_poly)\
                        +""" "COEFF_A" ={},""".format(a)\
                        +""" "COEFF_B" = {},""".format(b)\
                        +""" "COEFF_C" = {},""".format(c)\
                        +""" "ARCHIVAGE" = {}""".format(archivage)\
                        +""" WHERE "NUM_CERTIFICAT" = '{}';""".format(num_doc[0])
               
#        print("requete mise_a_jour_table_polynome {}".format(requete))
        query.exec_(requete)
        
        query.finish()
        
        
    def recherche_nom_ref_emt(self, id_referentiel_conformite):
        query = QtSql.QSqlQuery()
        requete = """SELECT "REFERENTIEL" FROM "REFERENTIEL_CONFORMITE" WHERE "ID_REFERENTIEL" = {} ;""".format(id_referentiel_conformite)
        query.exec_(requete) 
                
        while query.next() : 
            referentiel_emt = query.value(0)
                
        query.finish()
        return referentiel_emt
        
    def recherche_type_erreur_ref_emt(self, id_referentiel_conformite):
        query = QtSql.QSqlQuery()
        requete = """SELECT "TYPE_ERREUR" FROM "REFERENTIEL_CONFORMITE" WHERE "ID_REFERENTIEL" = {} ;""".format(id_referentiel_conformite)
        query.exec_(requete) 
                
        while query.next() : 
            type_erreur = query.value(0)
                
        query.finish()
        return type_erreur
    
    
    def recherche_id_ref_emt(self, nom_referentiel_conformite):
        query = QtSql.QSqlQuery()
        requete = """SELECT "ID_REFERENTIEL" FROM "REFERENTIEL_CONFORMITE" WHERE "REFERENTIEL" = '{}' ;""".format(nom_referentiel_conformite)
#        print(requete)
        query.exec_(requete) 
                
        while query.next() : 
                id_referentiel_emt = query.value(0)
                
        query.finish()
        return id_referentiel_emt
        
    def recuperation_poly_etalon(self, ident_etalon ):
        '''fonction qui recupere les coefficients du polynome de correction
        attention ne tient pas compte de l'archivage'''
                #recuperation poly
                #creer et configure le model
        model = QtSql.QSqlTableModel()
        model.setTable("POLYNOME_CORRECTION")
        model.select()
        
        #creer et configure le model
        
        model.setFilter("IDENTIFICATION=\""+ident_etalon+"\"")
 
        #Recuperation des donnees
        record= model.record(0)
        
        a = record.value("COEFF_A")
        b = record.value("COEFF_B")
        c = record.value("COEFF_C")
        
        return a, b, c
        
    def recuperation_poly_etalon_bis(self, ident_etalon ):
        '''fonction qui recupere les coefficients du poly etalon
        et trie en fcontion si polynome archivé ou non'''
        query = QtSql.QSqlQuery()
        requete = """SELECT "COEFF_A", "COEFF_B", "COEFF_C","ID_POLYNOME", "NUM_CERTIFICAT","DATE_ETAL" FROM "POLYNOME_CORRECTION" WHERE "IDENTIFICATION" = '{}' AND "ARCHIVAGE" = 'FALSE' ORDER BY "ID_POLYNOME" DESC;""".format(ident_etalon)
        query.exec_(requete)
       
        list_polynome = []
        while query.next() :            
            polynome = {"a": query.value(0), "b": query.value(1), "c": query.value(2), 
                        "id_poly": query.value(3),  "num_ce": query.value(4), "date_etal": query.value(5)} 
            list_polynome.append(polynome)
        query.finish()
        
        return list_polynome
        
        
    def recuperation_poly_etalon_inactifs(self, ident_etalon ):
        '''fonction qui recupere les coefficients du poly etalon
        et trie en fcontion si polynome archivé ou non'''
        query = QtSql.QSqlQuery()
        requete = """SELECT "COEFF_A", "COEFF_B", "COEFF_C","ID_POLYNOME", "NUM_CERTIFICAT","DATE_ETAL" FROM "POLYNOME_CORRECTION" WHERE "IDENTIFICATION" = '{}' AND "ARCHIVAGE" = 'TRUE' ORDER BY "ID_POLYNOME" DESC;""".format(ident_etalon)
        query.exec_(requete)
       
        list_polynome = []
        while query.next() :            
            polynome = {"a": query.value(0), "b": query.value(1), "c": query.value(2), 
                        "id_poly": query.value(3),  "num_ce": query.value(4), "date_etal": query.value(5)} 
            list_polynome.append(polynome)
        query.finish()
        
        return list_polynome
        
    def recuperation_poly_etalon_id(self, ident_etalon, id_poly ):
        '''fonction qui recupere les coefficients du poly etalon
        et trie en fcontion si polynome archivé ou non'''
        try:
            query = QtSql.QSqlQuery()
            requete = """SELECT "COEFF_A", "COEFF_B", "COEFF_C","ID_POLYNOME", "NUM_CERTIFICAT","DATE_ETAL" FROM "POLYNOME_CORRECTION" WHERE "IDENTIFICATION" = '{}' AND "ID_POLYNOME" = '{}';""".format(ident_etalon, id_poly)
            query.exec_(requete)
        
            while query.next() : 
                a = query.value(0)
                b = query.value(1)
                c = query.value(2)
                id_poly = query.value(3)
                num_ce = query.value(4)
                date_etal = query.value(5)
            query.finish()
        
            return a, b, c, id_poly, num_ce, date_etal
            
        except:
            poly = self.recuperation_poly_etalon_bis(ident_etalon)
            a = poly[0]
            b = poly[1]
            c = poly[2]
            id_poly = poly[3]
            num_ce = poly[4]
            date_etal = poly[5]            
        
            return a, b, c, id_poly, num_ce, date_etal
            
    def recherche_designation_instrument(self, nom):
        """renvoi la designation de l'instrument en fct du nom sert pour les eiv"""        
        query = QtSql.QSqlQuery()
        requete = """SELECT "DESIGNATION" FROM "INSTRUMENTS" WHERE "IDENTIFICATION" = '{}';""".format(nom)
        query.exec_(requete)
        
        while query.next() :
            designation = query.value(0)
                    
        query.finish()
        return designation
    
    def recuperation_eiv(self, nom_generateur, nom_etalon):
        '''recupere les eiv en fct des moyens mis en oeuvre lors de l'etalonnage'''
        
        designation_generateur = self.recherche_designation_instrument(nom_generateur)
#        print(str(designation_generateur))
        
        query = QtSql.QSqlQuery()
            #Definition de la requete à executer :
        if designation_generateur == "Bain de Glace Fondante" :
            if nom_etalon == "REF_101A" or nom_etalon == "REF_102B":
                requete = str ("""SELECT "ARCHIVAGE", "TYPE", "u_FINALE","U_DECLARATION" FROM "INCERTITUDES_MOYENS_MESURE" WHERE ("TYPE" = 'MEILLEURES_BGF' AND "ARCHIVAGE" = 'FALSE');""")
            else :
                requete = str ("""SELECT "ARCHIVAGE", "TYPE", "u_FINALE", "U_DECLARATION" FROM "INCERTITUDES_MOYENS_MESURE" WHERE ("TYPE" = 'COURANTES_BGF' AND "ARCHIVAGE" = 'FALSE');""")
        
        elif designation_generateur == "Bain d'etalonnage" :
            if nom_etalon == "REF_101A" or nom_etalon == "REF_102B":
                requete = str ("""SELECT "ARCHIVAGE", "TYPE", "u_FINALE", "U_DECLARATION" FROM "INCERTITUDES_MOYENS_MESURE" WHERE ("TYPE" = 'MEILLEURES_LIQUIDE' AND "ARCHIVAGE" = 'FALSE');""")
            else :
                requete = str ("""SELECT "ARCHIVAGE", "TYPE", "u_FINALE", "U_DECLARATION" FROM "INCERTITUDES_MOYENS_MESURE" WHERE ("TYPE" = 'COURANTES_LIQUIDE' AND "ARCHIVAGE" = 'FALSE');""")
        
            
        else :
            requete = str ("""SELECT "ARCHIVAGE", "TYPE", "u_FINALE", "U_DECLARATION" FROM "INCERTITUDES_MOYENS_MESURE" WHERE ("TYPE" ='COURANTE_AIR' OR "TYPE" ='COURANTES_AIR' AND "ARCHIVAGE" = 'FALSE');""")

#        print("requete recuperation_eiv {}".format(requete))
        query.exec_(requete)
        
        while query.next() :
#            print(query.value)
            u = query.value(2)
            u_declaration = query.value(3)

        query.finish()
        return(u, u_declaration)
        
    def recuperation_ref_emt(self):
        '''Fonction qui recupere des differentes EMT (referentiel de conformite) dans la bdd
        '''
        
        #Acces bdd
        query = QtSql.QSqlQuery()
        
        requete = str("""SELECT "REFERENTIEL" FROM "REFERENTIEL_CONFORMITE" WHERE ("DESIGNATION" = 'Chaine de mesure Temperature' AND "ARCHIVAGE" = 'FALSE') ORDER BY "ID_REFERENTIEL";""")
        
        query.exec_(requete) 
        
        list_emt = []
        while query.next(): 
            list_emt.append(query.value(0))
        
        query.finish()
        
        return list_emt
        
    def recuperation_valeur_emt(self, id_referentiel_conformite):
        '''Fct qui recupere les valeurs des emt pour la classe OngletResultat'''
        
        #Acces bdd
        
        query = QtSql.QSqlQuery()
                        
        requete = """SELECT "ERREUR_TERME_CST" FROM "REFERENTIEL_CONFORMITE" WHERE "ID_REFERENTIEL" = {} ;""".format(id_referentiel_conformite)
        query.exec_(requete) 
                
        while query.next() : 
            valeur_emt = query.value(0)
        query.finish()
                   
        return valeur_emt
        
    def recuperation_n_ce(self):
        '''fct qui recupere l'ensemble des n° d'etalonnage'''
        
        #Acces bdd
        
        query = QtSql.QSqlQuery()                        
        requete = """SELECT "NUM_DOCUMENT", "ID_ETAL", "ID_CAMPAGNE_ETAL" FROM "ETALONNAGE_TEMP_ADMINISTRATION" ORDER BY "ID_ETAL";"""
        
        query.exec_(requete) 
        
        num_doc =[]
        id_etal = []
        id_campagne_etal = []
        resultat = {}
        
        while query.next() : 
            num_doc.append(query.value(0))
            id_etal.append(query.value(1))
            id_campagne_etal.append(query.value(2))
            
        resultat["num_doc"]  = num_doc
        resultat["id_etal"] = id_etal
        resultat["id_campagne_etal"] = id_campagne_etal
        
        query.finish()
        return resultat
        
    def recuperation_n_ce_non_valide(self):
        '''fct qui recupere l'ensemble des n° d'etalonnage qui n'ont pas ete validé'''
        
        #Acces bdd
        
        query = QtSql.QSqlQuery()                        
        requete = """SELECT "NUM_DOCUMENT", "ID_ETAL", "ID_CAMPAGNE_ETAL" FROM "ETALONNAGE_TEMP_ADMINISTRATION" """\
                        +"""WHERE "ARCHIVAGE" = 'FALSE' ORDER BY "ID_ETAL";"""
        
        query.exec_(requete) 
        
        num_doc =[]
        id_etal = []
        id_campagne_etal = []
        resultat = {}
        
        while query.next() : 
            num_doc.append(query.value(0))
            id_etal.append(query.value(1))
            id_campagne_etal.append(query.value(2))
            
        resultat["num_doc"]  = num_doc
        resultat["id_etal"] = id_etal
        resultat["id_campagne_etal"] = id_campagne_etal
        
        query.finish()
        return resultat
        
    def recuperation_n_ce_all(self):
        '''fct qui recupere l'ensemble des n° d'etalonnage '''
        
        #Acces bdd
        
        query = QtSql.QSqlQuery()                        
        requete = """SELECT "NUM_DOCUMENT", "ID_ETAL", "ID_CAMPAGNE_ETAL" FROM "ETALONNAGE_TEMP_ADMINISTRATION" """\
                        +"""ORDER BY "ID_ETAL";"""
        
        query.exec_(requete) 
        
        num_doc =[]
        id_etal = []
        id_campagne_etal = []
        resultat = {}
        
        while query.next() : 
            num_doc.append(query.value(0))
            id_etal.append(query.value(1))
            id_campagne_etal.append(query.value(2))
            
        resultat["num_doc"]  = num_doc
        resultat["id_etal"] = id_etal
        resultat["id_campagne_etal"] = id_campagne_etal
        
        query.finish()
        return resultat
       
    def modif_table_instruments(self, donnee):
        ''''fct qui modifie la table instruments si l utilisateur modifie un parametre dans config etal'''
        
           #Acces bdd
        query = QtSql.QSqlQuery()
        
        nbr_instrum = donnee[0]["nbr_instrum"]
        
        i=1
        while i <= nbr_instrum :
            
            renseignement_complementaire = (donnee[i]["renseignement_complementaire"].replace('"', '\"')).replace('\'','\'\'')
                 
            requete = """UPDATE "INSTRUMENTS" SET "CONSTRUCTEUR" = '{}', "N_SERIE" = '{}', "TYPE" = '{}', "RESOLUTION" = {}, "COMMENTAIRE" = '{}' WHERE "IDENTIFICATION" = '{}' ;"""\
                        .format(donnee[i]["constructeur"], donnee[i]["n_serie"], donnee[i]["Type"], \
                                    donnee[i]["resolution"][0], renseignement_complementaire, donnee[i]["nom_instrum"])
#            print(requete)
            query.exec(requete)
            i+=1
        query.finish()
        
    def mise_a_jour_table_campagne_etalonnage_temp(self, nom_campagne, date_etal, id_instrum, id_campagne_etal):
        '''mise à jour de la table campagne_etalonnage_temp'''
              
        query =QtSql.QSqlQuery()
        requete = """UPDATE "CAMPAGNE_ETALONNAGE_TEMP" SET "ARCHIVAGE" = '{}', "NOM_CAMPAGNE_ETAL" = '{}',""".format("FALSE", nom_campagne) \
                        +""" "DATE" = '{}', "ID_INST_1" = {}, "ID_INST_2" = {}, "ID_INST_3" = {}, "ID_INST_4" = {},""".format(date_etal, id_instrum[0], id_instrum[1], id_instrum[2], id_instrum[3]) \
                        +""" "ID_INST_5" = {}, "ID_INST_6" = {}, "ID_INST_7" = {}, "ID_INST_8" = {}, "ID_INST_9" = {},""".format(id_instrum[4], id_instrum[5], id_instrum[6], id_instrum[7], id_instrum[8])\
                        +""" "ID_INST_10" = {}, "ID_INST_11" = {}, "ID_INST_12" = {}, "ID_INST_13" = {}, "ID_INST_14" = {},""".format(id_instrum[9], id_instrum[10], id_instrum[11], id_instrum[12], id_instrum[13])\
                        +""" "ID_INST_15" = {}, "ID_INST_16" = {}, "ID_INST_17" ={}, "ID_INST_18" = {}, "ID_INST_19" = {},""".format(id_instrum[14], id_instrum[15], id_instrum[16], id_instrum[17], id_instrum[18])\
                        +""" "ID_INST_20" ={} WHERE "ID_CAMPAGNE_ETALONNAGE_TEMP" = {} ;""".format( id_instrum[19], id_campagne_etal)

#        print(requete)
        query.finish()
        query.exec_(requete)
    def recuperation_id_instrums_table_campagne_etalonnage_temp(self,id_campagne_etal):
        '''mise à jour de la table campagne_etalonnage_temp'''
              
        query =QtSql.QSqlQuery()
        requete = """SELECT * """\
                        +"""FROM "CAMPAGNE_ETALONNAGE_TEMP" """\
                        +"""WHERE "ID_CAMPAGNE_ETALONNAGE_TEMP" = {};""".format(id_campagne_etal)

#        print(requete)
        query.exec(requete)   
        list_instrument_campagne = []
        
        while query.next() :
            for i in range(4, 23):
                if query.value(i) != 0:
                    list_instrument_campagne.append(query.value(i))
    
            
        query.finish()
        return list_instrument_campagne
        
        
    def recuperation_donnees_etalonnage(self, n_doc):
        ''''fct qui recupere l'ensemble des donnees permettant de generer un rapport'''
                   
        query = QtSql.QSqlQuery()
        requete = """SELECT "NBR_PT_ETALONNAGE", "DATE_ETAL", "IDENTIFICATION_INSTRUM", "EDIT_CE", "EDIT_CV", "ID_ETAL", "TECHNICIEN", "ETAT_RECEPTION", "ANNULE_NUM_DOC" """\
                        +"""FROM "ETALONNAGE_TEMP_ADMINISTRATION" """\
                        +"""WHERE "NUM_DOCUMENT" = '{}';""".format(n_doc)
                        
        query.exec(requete)
        
        rapport_etalonnage = {}
        while query.next() : 
            rapport_etalonnage["nbr_pt_etalonnage"] = query.value(0)
            rapport_etalonnage["date_etalonnage"] = query.value(1)
            rapport_etalonnage["identification_instrument"] = query.value(2)
            rapport_etalonnage["CE"] = query.value(3)
            rapport_etalonnage["CV"] = query.value(4)
            id_etal =  query.value(5)
            rapport_etalonnage["operateur"] = query.value(6)
            rapport_etalonnage["Etat_reception"] = query.value(7)
            rapport_etalonnage["Annule_doc"] = query.value(8)
        
        requete = """SELECT "DESIGNATION", "TYPE", "CONSTRUCTEUR", "N_SERIE", "CODE", "COMMENTAIRE", "AFFECTATION", "RESOLUTION" """\
                        +"""FROM "INSTRUMENTS" """\
                        +"""WHERE "IDENTIFICATION" = '{}';""".format(rapport_etalonnage["identification_instrument"] )
                        
        
        query.exec(requete)
        
        while query.next() : 
            rapport_etalonnage["designation"] = query.value(0)
            rapport_etalonnage["type"] = query.value(1)
            rapport_etalonnage["constructeur"] = query.value(2)
            rapport_etalonnage["n_serie"] = query.value(3)
            ref_client = query.value(4)
            rapport_etalonnage["renseignement_complementaire"] = query.value(5)
            rapport_etalonnage["affectation"] = query.value(6)
            rapport_etalonnage["resolution"] = query.value(7)
            
        if not rapport_etalonnage["affectation"]:
            rapport_etalonnage["affectation"] = "Neant"
            
        requete = """SELECT "SOCIETE", "ADRESSE", "VILLE", "CODE_POSTAL" """\
                        +"""FROM "CLIENTS" """\
                        +"""WHERE "CODE_CLIENT" = '{}';""".format(ref_client )
                        
        query.exec(requete)
        while query.next() : 
            rapport_etalonnage["societe"] = query.value(0)
            rapport_etalonnage["adresse"] = query.value(1)
            rapport_etalonnage["ville"] = query.value(2)
            rapport_etalonnage["code_postal"] = query.value(3)
            
            
        requete = """SELECT "TEMP_CONSIGNE", "NOM_ETALON", "NOM_GENERATEUR", "MOYENNE_ETAL_C", "MOYENNE_INSTRUM","""\
                        +""" "MOYENNE_CORRECTION", "U" ,"IMMERSION" """\
                        +"""FROM "ETALONNAGE_RESULTAT" """\
                        +"""WHERE "ID_ETALONNAGE" = {} ORDER BY "ID_ETAL_RESULT";""".format(id_etal)
#        print(requete)

        temps_consignes = []
        nom_etalon = []
        nom_generateur = []
        moyenne_etalon_corri = []
        moyenne_instrum = []
        moyenne_correction = []
        U = []
        immersion = []
        
        query.exec(requete)
        while query.next() : 
            temps_consignes.append(query.value(0))
            nom_etalon.append(query.value(1))
            nom_generateur.append(query.value(2))
            moyenne_etalon_corri.append(query.value(3))
            moyenne_instrum.append(query.value(4))
            moyenne_correction.append(query.value(5))
            U.append(query.value(6))
            immersion.append(query.value(7))
            
        rapport_etalonnage["temps_consignes"] = temps_consignes
        rapport_etalonnage["etalon"] = nom_etalon
        rapport_etalonnage["generateur"] = nom_generateur
        rapport_etalonnage["moyenne_etalon_corri"] = moyenne_etalon_corri
        rapport_etalonnage["moyenne_instrum"] = moyenne_instrum
        rapport_etalonnage["moyenne_correction"] = moyenne_correction
        rapport_etalonnage["U"] = U
        rapport_etalonnage["immersion"] = immersion
        
        for ele in nom_generateur:
#            print("nom generateur {}".format(ele))
            if ele == "ESPEC_1" or ele == "ESPEC_2" or ele == "Etuve ESPEC  N° 2" or ele == "Etuve ESPEC  N° 1" :
                rapport_etalonnage["milieu"] = "AIR"              
            else:
                rapport_etalonnage["milieu"] = "LIQUIDE"
        
        rapport_etalonnage["n_certificat"] = n_doc
        query.finish()
        return rapport_etalonnage
    
    def insertion_table_conformite_temp_resultat(self, donnees, date_etal):
        '''fct qui vient ecrire dans la table conformité_temp_resultat  les conclusions de conf'''
        
        query = QtSql.QSqlQuery()       

        #id_instrum
        requete = """SELECT "ID_INSTRUM" FROM "INSTRUMENTS" WHERE "IDENTIFICATION" = '{}';""".format(donnees["identification_instrument"])
        query.exec(requete)
        while query.next() : 
            id_instrum = query.value(0) 
        
        #id_referentiel
        requete = """SELECT "ID_REFERENTIEL" FROM "REFERENTIEL_CONFORMITE" WHERE "REFERENTIEL" = '{}';""".format(donnees["referentiel_emt"])
        query.exec(requete)
        while query.next() : 
            id_referentiel = query.value(0)        
        
        requete = """INSERT INTO "CONFORMITE_TEMP_RESULTAT" ("DATE_ETAL","""\
                                +""" "ID_ETALONNAGE", "ID_INSTRUM", "ID_REFERENTIEL", "CONCLUSION") """\
                                +"""VALUES('{}', {}, {}, {}, '{}');"""\
                                .format(date_etal, donnees["id_etal"], id_instrum,  id_referentiel, donnees["conformite"]  )
               
       
        query.exec_(requete)
        
        query.finish()
        
    def mise_a_jour_table_conformite_temp_resultat(self, id_conformite,  donnees, date_etal):
        '''fct qui vient ecrire dans la table conformité_temp_resultat  les conclusions de conf'''
        
        query = QtSql.QSqlQuery()       

        #id_instrum
        requete = """SELECT "ID_INSTRUM" FROM "INSTRUMENTS" WHERE "IDENTIFICATION" = '{}';""".format(donnees["identification_instrument"])
#        print(requete)
        query.exec(requete)
        while query.next() : 
            id_instrum = query.value(0) 
        
        #id_referentiel
        requete = """SELECT "ID_REFERENTIEL" FROM "REFERENTIEL_CONFORMITE" WHERE "REFERENTIEL" = '{}';""".format(donnees["referentiel_emt"])
        query.exec(requete)
        while query.next() : 
            id_referentiel = query.value(0)        
        
        requete = """UPDATE "CONFORMITE_TEMP_RESULTAT" SET """\
                        +""" "DATE_ETAL" = '{}',""".format(date_etal)\
                        +""" "ID_ETALONNAGE" = {},""".format(donnees["id_etal"])\
                        +""" "ID_INSTRUM" = {},""".format(id_instrum)\
                        +""" "ID_REFERENTIEL" = {},""".format(id_referentiel)\
                        +""" "CONCLUSION" = '{}' """.format(donnees["conformite"])\
                        +"""WHERE "ID_CONFORMITE" = {};""".format(id_conformite)
               
#        print("requete mise_a_jour_table_conformite_temp_resultat {}".format(requete))
        query.exec_(requete)
        
        query.finish()
        
    def recuperation_donnees_conformite(self, donnees):
        ''' permet de recuperer les donnees dans la table conformite_temp_resultat '''
        try:
            cv ={}
            query = QtSql.QSqlQuery()
            
            #id_certificat
            requete = """SELECT "ID_ETAL" FROM "ETALONNAGE_TEMP_ADMINISTRATION" WHERE "NUM_DOCUMENT" = '{}';"""\
                            .format(donnees["n_certificat"])
            query.exec(requete)
            while query.next() : 
                id_etal = query.value(0)
                
            #recuperation donnnees
            requete = """SELECT "ID_REFERENTIEL", "CONCLUSION" FROM "CONFORMITE_TEMP_RESULTAT" WHERE "ID_ETALONNAGE" = {};"""\
                            .format(id_etal)
            query.exec(requete)
            while query.next() : 
                id_ref = query.value(0)
                conclusion = query.value(1)
                
            #recuperation nom referentiel
            requete = """SELECT "REFERENTIEL" FROM "REFERENTIEL_CONFORMITE" WHERE "ID_REFERENTIEL" = {};""".format(id_ref)
            query.exec(requete)
            while query.next() : 
                nom_ref = query.value(0)
            
            cv["conformite"] = conclusion
            cv["referentiel_emt"] = nom_ref
            
            
            requete = """SELECT "TYPE_ERREUR" FROM "REFERENTIEL_CONFORMITE" WHERE "ID_REFERENTIEL" = {} ;""".format(id_ref)
            query.exec_(requete) 
                    
            while query.next() : 
                type_erreur = query.value(0)
                    
            query.finish()
            
            cv["type_erreur"] = type_erreur
            
            
            query.finish()
            return cv
        except UnboundLocalError:
            cv["conformite"] = ""
            cv["referentiel_emt"] = ""
            return cv
        
    def n_certificat(self, annee):
        '''fonction qui va créer un n° certificat en regardant dans la base le nombre de prestation sur l'annee en cours'''
        
        query = QtSql.QSqlQuery()
        requete =str("""SELECT "DATE_ETAL" FROM "ETALONNAGE_TEMP_ADMINISTRATION" WHERE "DATE_ETAL" LIKE"+" "+"'"+str(annee)+"%"+"'"+" "+";""")
        query.exec_(requete)
        results = []
        while query.next() :
            date_etal = query.value(0)
            results.append(date_etal)
                    
        query.finish()
        
        return results
        
    def n_certificat_2(self, annee):
        '''fonction qui va créer un n° certificat en regardant dans la base le nombre de prestation sur l'annee en cours
        Pour postgresql obligation de convertir date_etal en text sinon like ne marche pas'''
        
        query = QtSql.QSqlQuery()
        requete =str("""SELECT "DATE_ETAL" FROM "ETALONNAGE_TEMP_ADMINISTRATION" WHERE to_char("DATE_ETAL",'YYYY') LIKE '{}{}';""".format(annee, "%"))
        
        
        query.exec_(requete)
        results = []
        while query.next() :
            date_etal = query.value(0)
            results.append(date_etal)
                    
        query.finish()
        
        return results
        
        
    def n_certificat_3(self, annee):
        '''fonction qui va créer un n° certificat en regardant dans la base le nombre de prestation sur l'annee en cours
        Pour postgresql obligation de convertir date_etal en text sinon like ne marche pas'''
        
        query = QtSql.QSqlQuery()
        
        
        requete = """INSERT INTO "ETALONNAGE_TEMP_ADMINISTRATION" DEFAULT VALUES RETURNING "ID_ETAL";"""
#        print(requete)
        query.exec_(requete)
        while query.next() :
            id_etal = query.value(0)       
        
        
        requete =str("""SELECT "DATE_ETAL" FROM "ETALONNAGE_TEMP_ADMINISTRATION" WHERE to_char("DATE_ETAL",'YYYY') LIKE '{}{}' AND "ID_ETAL" < {};""".format(annee, "%", id_etal))
        
#        print (requete)
        query.exec_(requete)
        results = []
        while query.next() :
            date_etal = query.value(0)
            results.append(date_etal)
                    
        query.finish()
        
        return results, id_etal
        
    def test_n_certificat(self, n_ce):
        
        boleen = True
        query = QtSql.QSqlQuery()       
        
        requete = """SELECT * FROM "ETALONNAGE_TEMP_ADMINISTRATION" WHERE "NUM_DOCUMENT" = '{}';""".format(n_ce)
        
        query.exec_(requete)
        results = []
        while query.next() :
            results.append(query.value(0))
            
        if len(results)!= 0:
            boleen = False        
            
        return boleen

    def n_campagne_etal(self, annee):
        '''fonction qui va créer un n° certificat en regardant dans la base le nombre de prestation sur l'annee en cours'''
        
        query = QtSql.QSqlQuery()
        requete =str("""SELECT "DATE" FROM "CAMPAGNE_ETALONNAGE_TEMP" WHERE "DATE" LIKE {} {};""".format(annee, "%"))
        
        query.exec_(requete)
        
        results = []
        while query.next() :
            date_campagne = query.value(0)
            results.append(date_campagne)
                    
        query.finish()
        
        return results 


    def n_campagne_etal_2(self, annee):
        '''fonction qui va créer un n° certificat en regardant dans la base le nombre de prestation sur l'annee en cours'
        version postgresql : obligation de convertir la date en caractere LIKE ne marche qu'avec du text'''
        
        query = QtSql.QSqlQuery()
        requete =str("""SELECT "DATE" FROM "CAMPAGNE_ETALONNAGE_TEMP" WHERE to_char("DATE",'YYYY') LIKE '{}{}';""".format(annee, "%"))
        
        query.exec_(requete)
        
        results = []
        while query.next() :
            date_campagne = query.value(0)
            results.append(date_campagne)
                    
        query.finish()
        
        return results 
        
    def n_campagne_etal_3(self, annee):
        '''fonction qui va créer un n° certificat en regardant dans la base le nombre de prestation sur l'annee en cours'
        version postgresql : obligation de convertir la date en caractere LIKE ne marche qu'avec du text'''
    
        query = QtSql.QSqlQuery()
        
        requete = """INSERT INTO "CAMPAGNE_ETALONNAGE_TEMP" DEFAULT VALUES RETURNING "ID_CAMPAGNE_ETALONNAGE_TEMP";"""
        
#        print(requete)
        query.exec_(requete)
        while query.next() :
            id_campagne = query.value(0)        
        
        requete ="""SELECT "DATE" FROM "CAMPAGNE_ETALONNAGE_TEMP" WHERE to_char("DATE",'YYYY') LIKE '{}{}' AND "ID_CAMPAGNE_ETALONNAGE_TEMP" < {};""".format(annee, "%", id_campagne)
        
#        print(requete)
        query.exec_(requete)
        
        results = []
        while query.next() :
            date_campagne = query.value(0)
            results.append(date_campagne)
                    
        query.finish()
        
        return results, id_campagne
        
    def test_n_campagne(self, n_campagne):
        
        boleen = True
        query = QtSql.QSqlQuery()       
        
        requete = """SELECT * FROM "CAMPAGNE_ETALONNAGE_TEMP" WHERE "NOM_CAMPAGNE_ETAL" = '{}';""".format(n_campagne)
#        print(requete)
        query.exec_(requete)
        results = []
        while query.next() :
            results.append(query.value(0))
        
        if len(results)!= 0:
            boleen = False        
        
        return boleen
        
    def recuperation_nom_campagne_etal_non_valide(self):
        '''fct qui va chercher l'ensemble des nom des campagne et renvoie une list'''
        query = QtSql.QSqlQuery()       
        requete = """SELECT "NOM_CAMPAGNE_ETAL" FROM "CAMPAGNE_ETALONNAGE_TEMP" WHERE "ARCHIVAGE" = 'FALSE' ORDER BY "ID_CAMPAGNE_ETALONNAGE_TEMP";"""
#        print(requete)
        query.exec_(requete)
        
        nom_campagne = []
        while query.next() :
            nom_campagne.append(query.value(0))
            
        query.finish()
        
        return nom_campagne
        
    def recuperation_nom_campagne_etal_all(self):
        '''fct qui va chercher l'ensemble des nom des campagne et renvoie une list'''
        query = QtSql.QSqlQuery()       
        requete = """SELECT "NOM_CAMPAGNE_ETAL" FROM "CAMPAGNE_ETALONNAGE_TEMP" ORDER BY "ID_CAMPAGNE_ETALONNAGE_TEMP";"""
#        print(requete)
        query.exec_(requete)
        
        nom_campagne = []
        while query.next() :
            nom_campagne.append(query.value(0))
            
        query.finish()
        
        return nom_campagne   
        
    def recherche_id_campagne_etal_particuliere(self,  nom):
        ''' fct recupere l'id de la campagne en fction du nom de la campagne'''
        
        query = QtSql.QSqlQuery()
        requete = """SELECT "ID_CAMPAGNE_ETALONNAGE_TEMP" FROM "CAMPAGNE_ETALONNAGE_TEMP" """\
                        """WHERE "NOM_CAMPAGNE_ETAL" = '{}';""".format(nom)
       
        
#        print(requete)
        query.exec_(requete)
        while query.next():
            id_campagne_etal_particuliere = query.value(0)
            
        query.finish()
        return id_campagne_etal_particuliere
        
        
    def recherche_id_campagne_etal_n_etalonnage(self,  num_etal):
        ''' fct recupere l'id de la campagne en fction du nom certificat '''
        
        query = QtSql.QSqlQuery()
        requete = """SELECT "ID_CAMPAGNE_ETAL" FROM "ETALONNAGE_TEMP_ADMINISTRATION" """\
                        """WHERE "NUM_DOCUMENT" = '{}';""".format(num_etal)
       
        query.exec_(requete)
        while query.next():
            id_campagne_etal_particuliere = query.value(0)
            
        query.finish()
        return id_campagne_etal_particuliere
        
    def recherche_nom_campagne_etal_id_campagne(self,  id_campagne_etal_particuliere):
        ''' fct recupere l'id de la campagne en fction du nom certificat '''
        
        query = QtSql.QSqlQuery()
        requete = """SELECT "NOM_CAMPAGNE_ETAL" FROM "CAMPAGNE_ETALONNAGE_TEMP" """\
                        """WHERE "ID_CAMPAGNE_ETALONNAGE_TEMP" = '{}';""".format(id_campagne_etal_particuliere)
       
        query.exec_(requete)
        while query.next():
            nom_campagne = query.value(0)
            
        query.finish()
        return nom_campagne
        
    def recuperation_donnees_etalonnage_validation(self, id_campagne_etal_particuliere):
        '''fct qui recupere l'ensemble des donnees d'un etalonnage pour permettre la validation des donnees renvoi une liste de dictionnaires 
        [0]= dict 1er instrument'''
        
        query = QtSql.QSqlQuery()
                
        
        #nbr d'instruments = nbr de ligne retourne lors de la selection sur la table etalonnage_temp_administration avec l'id de la campagne
        
        requete ="""SELECT "ID_ETAL" FROM "ETALONNAGE_TEMP_ADMINISTRATION" """\
                        +"""WHERE "ID_CAMPAGNE_ETAL" = {} ORDER BY "ID_ETAL";""".format(id_campagne_etal_particuliere)
        
#        print(requete)        
        query.exec_(requete)
        list_id_etal = []
        while query.next() : 
            list_id_etal.append(query.value(0))
        
        nbr_instrum = len(list_id_etal)
        campagne_etal = []
        
        i =0
        while i < nbr_instrum:
            etalonnage = {}

            immersion = []
            temp_consigne = []
            ecart_type = []
            nom_etalon = []
            
            nom_generateur = []
            autoechauffement = []
            fuite_thermique = []
            resolution = []
            stabilite = []
            eiv_meilleure_courante = []
            moyenne_etalon_nc = []
            moyenne_etalon_c = []
            moyenne_instrum = []
            moyenne_correction = []
            U = []
            resolution_instrument = []
            
            requete = """SELECT "NBR_PT_ETALONNAGE", "DATE_ETAL", "IDENTIFICATION_INSTRUM","""\
                            +""" "EDIT_CE", "EDIT_CV", "TECHNICIEN", "NUM_DOCUMENT", "ETAT_RECEPTION" """\
                            +"""FROM "ETALONNAGE_TEMP_ADMINISTRATION" """\
                            +"""WHERE "ID_ETAL" = {};""".format(list_id_etal[i])
                        
            
            query.exec(requete)        
            
            while query.next() :                 
                etalonnage["nbr_pt_etalonnage"] = query.value(0)
                etalonnage["date_etalonnage"] = query.value(1)
                etalonnage["identification_instrument"] = query.value(2)
                etalonnage["CE"] = query.value(3)
                etalonnage["CV"] = query.value(4)
                etalonnage["operateur"] = query.value(5)
                etalonnage["num_document"] = query.value(6)
                etalonnage["Etat_reception"] = query.value(7)
            
                 
            
            nbr_pt_temp = etalonnage["nbr_pt_etalonnage"]
#            print("nbr_t-etal {}".format(nbr_pt_temp))
            
            j=0
            while j < nbr_pt_temp:
                
                correction = []
                mesure_etal_non_corri = []
                mesure_etal_corri = []
                mesure_instrum = []
                id_polynome_etalon = []
                
                requete = """SELECT "CORRECTION", "MESURE_ETAL_NC", "MESURE_ETAL_C", "MESURE_INSTRUM", "NUM_MESURE","ID_POLY_ETALON" """\
                                +"""FROM "ETALONNAGE_MESURE" """\
                                +"""WHERE "ID_ETALONNAGE" = {} AND "NUM_PT_ETAL" = {} ORDER BY "NUM_MESURE";""".format(list_id_etal[i], (j+1))
                
#                print(requete)
                query.exec(requete)       
            
                while query.next() :
                    correction.append(query.value(0))
#                    print("correction {}".format(correction))
                    mesure_etal_non_corri.append(query.value(1))
                    mesure_etal_corri.append(query.value(2))
                    mesure_instrum.append(query.value(3))
                    id_polynome_etalon.append(query.value(5))
            
                
                etalonnage[str("correction_pt"+str(j+1))] = correction
                etalonnage[str("mesure_etal_non_corri_pt"+str(j+1))] = mesure_etal_non_corri
                etalonnage[str("mesure_etal_corri_pt"+str(j+1))] = mesure_etal_corri
                etalonnage[str("mesure_instrum_pt"+str(j+1))] = mesure_instrum
                etalonnage["id_poly"+str(j+1)] = id_polynome_etalon
                
                requete = """SELECT "IMMERSION", "TEMP_CONSIGNE", "ECART_TYPE", "NOM_ETALON","""\
                                +""" "NOM_GENERATEUR", "AUTOECHAUFFEMENT", "FUITE_THERMIQUE","""\
                                +""" "RESOLUTION", "STABILITE", "EIV_MEILLEURE_COURANTE_U", "MOYENNE_ETALON_NC","""\
                                +""" "MOYENNE_ETAL_C", "MOYENNE_INSTRUM", "MOYENNE_CORRECTION", "U", "RESOLUTION_INSTRUMENT" """\
                                +"""FROM "ETALONNAGE_RESULTAT" """\
                                +"""WHERE "ID_ETALONNAGE" = {} AND "NUM_PT_ETAL" = {};""".format(list_id_etal[i], (j+1)) 
#                print(requete)
                query.exec(requete)
                
                while query.next() :
                    immersion.append(query.value(0))
                    temp_consigne.append(query.value(1))
                    ecart_type.append(query.value(2))
                    nom_etalon.append(query.value(3))
                    nom_generateur.append(query.value(4))
                    autoechauffement.append(query.value(5))
                    fuite_thermique.append(query.value(6))
                    resolution.append(query.value(7))
                    stabilite.append(query.value(8))
                    eiv_meilleure_courante.append(query.value(9))
                    moyenne_etalon_nc.append(query.value(10))
                    moyenne_etalon_c.append(query.value(11))
                    moyenne_instrum.append(query.value(12))
                    moyenne_correction.append(query.value(13))
                    U.append(query.value(14))
                    resolution_instrument.append(query.value(15))
                    
                etalonnage["immersion"] = immersion
                etalonnage["temp_consigne"] = temp_consigne
                etalonnage["ecart_type"] = ecart_type
                etalonnage["nom_etalon"] = nom_etalon
                etalonnage["nom_generateur"] = nom_generateur
                etalonnage["autoechauffement"] = autoechauffement
                etalonnage["fuite_thermique"] = fuite_thermique
                etalonnage["resolution"] = resolution
                etalonnage["stabilite"] = stabilite
                etalonnage["eiv_meilleure_courante"] = eiv_meilleure_courante
                etalonnage["moyenne_etalon_nc"] = moyenne_etalon_nc
                etalonnage["moyenne_etalon_c"] = moyenne_etalon_c
                etalonnage["moyenne_instrum"] = moyenne_instrum
                etalonnage["moyenne_correction"] = moyenne_correction
                etalonnage["U"] = U
                etalonnage["resolution_instrument"] = resolution_instrument
                
                j += 1
                            
            requete = """SELECT "ID_CONFORMITE", "ID_REFERENTIEL", "CONCLUSION" """\
                                +"""FROM "CONFORMITE_TEMP_RESULTAT" """\
                                +"""WHERE "ID_ETALONNAGE" = {};""".format(list_id_etal[i]) 
            
            query.exec(requete)
            
                #attention la requete peut etre vide et si vide pas de creation de clef dans les dicos sauf a les creer avant et à modif apres
            while query.next() :
                etalonnage["id_conformite"] = query.value(0)
                etalonnage["id_referentiel"] = query.value(1)
                etalonnage["conformite"] = query.value(2)
                
            campagne_etal.append(etalonnage)
            i+=1

        query.finish()
#        print("campagne_etal {}".format(campagne_etal))
        return campagne_etal
    
    
    
    def recherche_doc_annule_remplace(self, n_document_selectionne): 
        '''fct qui va chercher le numero dans la colonne ANNULE_NUM_DOC table etalonnage_temp_administration ''' 
        
        query = QtSql.QSqlQuery()
        requete = """SELECT "ANNULE_NUM_DOC" """\
                                +"""FROM "ETALONNAGE_TEMP_ADMINISTRATION" """\
                                +"""WHERE "NUM_DOCUMENT" = '{}';""".format(n_document_selectionne) 
            
        query.exec(requete) 
        
        while query.next() :
            if not isinstance(query.value(0), str):
                annule_doc = "Neant"
            else:
                annule_doc = query.value(0)
        query.finish()
        
        return annule_doc


    def recherche_id_conformite_temp_resultat_id_etalonnage(self, id_etal):
        '''fct qui renvoie l'id de la declaration de conformite en fct de l'id d'etalonnage_temp_administration'''
        
        try :
            query = QtSql.QSqlQuery()
                      
            requete ="""SELECT "ID_CONFORMITE", "ID_REFERENTIEL", "CONCLUSION" """\
                        +"""FROM "CONFORMITE_TEMP_RESULTAT" """\
                        +"""WHERE "ID_ETALONNAGE" = {};""".format(id_etal)
#            print(requete)
            query.exec(requete)
        
            while query.next() :
                id_conformite = query.value(0)
                id_ref = query.value(1)
                conclusion = query.value(2)      
        
            query.finish()
            return id_conformite, id_ref, conclusion
        
        except UnboundLocalError:
            id_conformite = None
            id_ref = None
            conclusion = None
            return id_conformite, id_ref, conclusion
            
        
        
    def archivage_campage_etal(self, id_campagne_etal_particuliere):
        ''' requete qui archive (passe archivage de N à O) la campagne d etalonnage '''
        
        query = QtSql.QSqlQuery()
                      
        requete ="""UPDATE "CAMPAGNE_ETALONNAGE_TEMP" SET "ARCHIVAGE" = 'TRUE' """\
                        +"""WHERE "ID_CAMPAGNE_ETALONNAGE_TEMP" = {};""".format(id_campagne_etal_particuliere)
                        
        query.finish()
        query.exec(requete)
        
    def archivage_etalonnage_unique(self, id_etalonnage):        
        '''archive l''etalonnage (passe archivage de N à O) id_etal'''
        
        query = QtSql.QSqlQuery()
                      
        requete ="""UPDATE "ETALONNAGE_TEMP_ADMINISTRATION" SET "ARCHIVAGE" = 'TRUE' """\
                        +"""WHERE "ID_ETAL" = {};""".format(id_etalonnage)
                        
        query.finish()
        query.exec(requete)
        
    def archivage_etalonnage(self, id_campagne_etal_particuliere):        
        '''archive un ou des etalonnages (passe archivage de N à O) de la campagne correspondante à id campagne'''
        
        query = QtSql.QSqlQuery()
                      
        requete ="""UPDATE "ETALONNAGE_TEMP_ADMINISTRATION" SET "ARCHIVAGE" = 'TRUE' """\
                        +"""WHERE "ID_CAMPAGNE_ETAL" = {};""".format(id_campagne_etal_particuliere)
                        
        query.finish()
        query.exec(requete)
