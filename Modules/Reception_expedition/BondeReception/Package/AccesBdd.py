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
        ins = select([table.c.DATE_INTERVENTION]).where(table.c.INTERVENTION == "Réception").order_by(table.c.ID_INTERVENTION)
        
        
        #.where(and_(table.c.DOMAINE_MESURE == type_afficheur)).order_by(table.c.ID_INSTRUM)#, table.c.SITE == site, table.c.DESIGNATION == designation_etalon))#, table.c.AFFECTATION == service))
        
        result = self.connection.execute(ins)
        
        list_dates = []
        for ele in result:
            if ele[0].strftime("%d-%m-%Y" )not in list_dates:            
                list_dates.append(ele[0].strftime("%d-%m-%Y" ))
            else:
                pass
        
        return list_dates


    def instruments_receptionnes(self, date_reception):
        
        table = Table("INTERVENTIONS", self.meta)
        ins = select([table.c.CODE_CLIENT, table.c.IDENTIFICATION]).where(and_(table.c.DATE_INTERVENTION == date_reception, table.c.INTERVENTION == "Réception")).order_by(table.c.ID_INTERVENTION)
        result = self.connection.execute(ins)        
        
        list_instruments = []
        list_reception = []
        for ele in result:
            list_instruments.append(ele)
        
        #recuperation type d'instruments_
        
        for instrument in list_instruments:
#            print("instruments {}".format(instrument))
            
            table = Table("INSTRUMENTS", self.meta)
            ins = select([table.c.DESIGNATION, table.c.ID_INSTRUM, table.c.SITE, table.c.AFFECTATION]).where(table.c.IDENTIFICATION == str(instrument[1]))
            result = self.connection.execute(ins).fetchone()
              
            site = str(result[2])
            
                
#            if len (result[3]) != 0:    
            affectation = str(result[3])
#            else:
#                affectation = "None"
            
            
            if len (result) != 0:
              list_reception.append((date_reception, instrument[0], instrument[1], site, affectation))  
                
#            
#            #recuperation du numero des rapport et de la date de celuici:
#            if result != None:
#                if result[0] == "Enregistreur de température" or result[0] == "Chaîne de mesure de température":
#                    table  = Table("ETALONNAGE_TEMP_ADMINISTRATION", self.meta)
#                    ins = select([table.c.NUM_DOCUMENT, table.c.DATE_ETAL]).where(table.c.IDENTIFICATION_INSTRUM == instrument[1]).order_by(table.c.ID_ETAL)
#                    result = self.connection.execute(ins).fetchall()
#
#                    
#                    if len (result) != 0:                
#                        list_expedition.append((date_expedition, instrument[0], instrument[1], result[len(result)-1][0], result[len(result)-1][1].strftime("%d-%m-%Y" ), site, affectation))
#    
#    #                
#                elif result[0] == "Afficheur de temps" or result[0] == "Afficheur de température" or result[0] == "Afficheur de vitesse":
#                    table  = Table("AFFICHEUR_CONTROLE_ADMINISTRATIF", self.meta)
#                    ins = select([table.c.NUM_DOC, table.c.DATE_CONTROLE]).where(table.c.IDENTIFICATION == result[1]).order_by(table.c.ID_AFFICHEUR_ADMINISTRATIF)
#                    result = self.connection.execute(ins).fetchall()
#                    
#                    if len (result) != 0:                  
#                        list_expedition.append((date_expedition, instrument[0], instrument[1], result[len(result)-1][0], result[len(result)-1][1].strftime("%d-%m-%Y" ), site, affectation))
#
#                
                
        return list_reception
            
            
            
    def adresse_client(self, code_client):
        
            
        table = Table("CLIENTS", self.meta)
        ins = select([table.c.SOCIETE, table.c.ADRESSE, table.c.CODE_POSTAL, table.c.VILLE]).where(table.c.CODE_CLIENT == code_client)
        adresse = self.connection.execute(ins).fetchone()   
            
            
            
        
        return adresse
            
            
            
            
            
            
            
            
            
