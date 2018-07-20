#-*- coding: utf-8 -*-
from sqlalchemy import *
from sqlalchemy.orm import *
from sqlalchemy.engine import create_engine


class AccesBdd():
    '''class gerant la bdd'''
    
    def __init__(self, engine):

           
            #création de l'"engine"
        self.engine = engine
        self.meta = MetaData()        
        self.meta.reflect(bind=self.engine)
#        self.table_instruments = Table('INSTRUMENTS', self.meta)
        self.connection = self.engine.connect()
        Session = sessionmaker(bind=self.engine)
        self.session = Session.configure(bind=self.engine)
        
        
    def recensement_dates_interventions(self):
        '''fct pour avoir l'ensemble des afficheurs du type : afficheur_type'''
        
        table = Table("INTERVENTIONS", self.meta)
#        ins = table.select().where(and_(table.c.DOMAINE_MESURE == type_afficheur, table.c.SITE == site, table.c.DESIGNATION == designation_etalon))#, table.c.AFFECTATION == service))
        ins = select([table.c.DATE_INTERVENTION]).where(or_(table.c.INTERVENTION == "Expedition", table.c.INTERVENTION == "Expédition")).order_by(table.c.ID_INTERVENTION)
        
        
        #.where(and_(table.c.DOMAINE_MESURE == type_afficheur)).order_by(table.c.ID_INSTRUM)#, table.c.SITE == site, table.c.DESIGNATION == designation_etalon))#, table.c.AFFECTATION == service))
        
        result = self.connection.execute(ins)
#        print(result)
        
        list_dates = []
        for ele in result:
#            print(ele)
            if ele[0] not in list_dates:            
                list_dates.append(ele[0])
            else:
                pass
        list_dates.sort()
        list_dates_strint =[x.strftime("%d-%m-%Y" ) for x in list_dates]
#        print(list_dates_strint)
        return list_dates_strint


    def instruments_expedies(self, date_expedition):
        
        table = Table("INTERVENTIONS", self.meta)
        ins = select([table.c.CODE_CLIENT, table.c.IDENTIFICATION]).where(and_(table.c.DATE_INTERVENTION == date_expedition, or_(table.c.INTERVENTION == "Expedition", table.c.INTERVENTION == "Expédition"))).order_by(table.c.ID_INTERVENTION.desc())
        result = self.connection.execute(ins)        
#        print(result)
        list_instruments = []
        list_expedition = []
        for ele in result:
            list_instruments.append(ele)
#        print(list_instruments)
        #recuperation type d'instruments_
        
        for instrument in list_instruments:
#            print("instruments {}".format(instrument))
            
            table = Table("INSTRUMENTS", self.meta)
            ins = select([table.c.DESIGNATION, table.c.ID_INSTRUM, table.c.SITE, table.c.AFFECTATION]).where(table.c.IDENTIFICATION == str(instrument[1]))
            result = self.connection.execute(ins).fetchone()
            site = str(result[2])
            affectation = str(result[3])
            
            #recuperation du numero des rapport et de la date de celuici:
            
            
            if result != None:
#                print(result[0])
                if result[0] in ["Enregistreur de température", "Chaîne de mesure de température", "ENREGISTREUR DE TEMPÉRATURE", "CHAÎNE DE MESURE DE TEMPÉRATURE"] :
                    table  = Table("ETALONNAGE_TEMP_ADMINISTRATION", self.meta)
                    ins = select([table.c.NUM_DOCUMENT, table.c.DATE_ETAL]).where(table.c.IDENTIFICATION_INSTRUM == instrument[1]).order_by(table.c.ID_ETAL)
                    result = self.connection.execute(ins).fetchall()

                    
                    if len (result) != 0:                
                        list_expedition.append((date_expedition, instrument[0], instrument[1], result[len(result)-1][0], result[len(result)-1][1].strftime("%d-%m-%Y" ), site, affectation))
    
    #                
                elif  result[0] in ["Sonde alarme température", "Afficheur de temps","Afficheur de température","Afficheur de vitesse", "SONDE ALARME TEMPÉRATURE", 
                                    "AFFICHEUR DE TEMPS", "AFFICHEUR DE TEMPÉRATURE","AFFICHEUR DE VITESSE","Témoin d'environnement","TÉMOIN D'ENVIRONNEMENT"]  :
                    table  = Table("AFFICHEUR_CONTROLE_ADMINISTRATIF", self.meta)
                    ins = select([table.c.NUM_DOC, table.c.DATE_CONTROLE]).where(table.c.IDENTIFICATION == result[1]).order_by(table.c.ID_AFFICHEUR_ADMINISTRATIF)
                    result = self.connection.execute(ins).fetchall()
                    
                    if len (result) != 0:                  
                        list_expedition.append((date_expedition, instrument[0], instrument[1], result[len(result)-1][0], result[len(result)-1][1].strftime("%d-%m-%Y" ), site, affectation))

                elif result[0] in ["ENCEINTE CLIMATIQUE"]:
                    table  = Table("CARTO_ADMINISTRATION", self.meta)
                    ins = select([table.c.NUM_RAPPORT, table.c.DATE_REALISATION]).where(table.c.IDENT_ENCEINTE == instrument[1]).order_by(table.c.ID_CARTO)
                    result = self.connection.execute(ins).fetchall()
                    
                    if len (result) != 0:                  
                        list_expedition.append((date_expedition, instrument[0], instrument[1], result[len(result)-1][0], result[len(result)-1][1].strftime("%d-%m-%Y" ), site, affectation))
                
        return list_expedition
            
            
            
    def adresse_client(self, code_client):
        
            
        table = Table("CLIENTS", self.meta)
        ins = select([table.c.SOCIETE, table.c.ADRESSE, table.c.CODE_POSTAL, table.c.VILLE]).where(table.c.CODE_CLIENT == code_client)
        adresse = self.connection.execute(ins).fetchone()   
            
            
            
        
        return adresse
            
            
            
            
            
            
            
            
            
