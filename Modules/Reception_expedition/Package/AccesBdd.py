#-*- coding: utf-8 -*-
from sqlalchemy import *
from sqlalchemy.orm import *
from sqlalchemy.engine import create_engine
from sqlalchemy.ext.automap import automap_base
import pandas as pd

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
        
        
    def __del__(self):
        self.connection.close()

        
    def identification_instrument(self):
        '''retourne tous les identifications des instruments dans une list'''

        result = self.connection.execute('SELECT "IDENTIFICATION" FROM "INSTRUMENTS"')
        
        instruments = []        
        for ele in result:            
            instruments.append(ele[0]) #mise en forme

        return instruments
        
    def return_code_intrument(self, identification_instrument):
        '''retourne le code instrument'''
        result = self.connection.execute("""SELECT "CODE" FROM "INSTRUMENTS" WHERE "IDENTIFICATION" ='{}'""".format(identification_instrument))
        
        for ele in result:
            code = ele[0]
        return code
        
        
        

    def recuperation_periodicite_instrum(self, nom_instrum, nom_intervention):
        
        table = Table("INSTRUMENTS", self.meta)
        ins = select([table.c.ID_INSTRUM, table.c.DESIGNATION]).where(table.c.IDENTIFICATION == nom_instrum)

        caract_instrum = self.connection.execute(ins).fetchone()
        
        
        table = Table("INSTRUMENT_DESIGNATION", self.meta)
        ins = select([table.c.ID_DESIGNATION]).where(table.c.NOM_DESIGNATION == caract_instrum[1])
        id_designation = self.connection.execute(ins).fetchone()
        
        
        
        table = Table("INTERVENTION_TYPE", self.meta)
        ins = select([table.c.PERIODICITE, table.c.UNITE_PERIODICITE]).where(and_(table.c.DESIGNATION == id_designation[0], table.c.NOM_INTERVENTION == nom_intervention))
        periodicite = self.connection.execute(ins).fetchone()
        
        
        
        return periodicite
        
        
#        print(periodicite)
        
    def insertion_table(self, table_nom, donnees):
        '''fct qui insere dans la table_nom'''
        
        table = Table(table_nom, self.meta)
        ins = table.insert()
        result = self.connection.execute(ins, donnees)
        
        


class Intervention():
    """classe pour gerer la table intervention"""
    def __init__(self,engine):
        
        Base = automap_base()
        self.engine = engine     
#        self.meta = MetaData()
        self.connection = self.engine.connect()
        
        Base.prepare(engine, reflect=True)
        
        
        self.INTERVENTION = Base.classes.INTERVENTIONS
        
    def recuperation_interventions(self):
        """recupere la table entite_client et la met dans une dataframe pandas"""
        meta = MetaData()
        Session = sessionmaker(bind= self.engine)
        session = Session()
        
        try:
            #chargement de la table complete:
            table = session.query(Table("INTERVENTIONS", meta, autoload=True,  autoload_with= self.engine))
            
            #mise sous pandas:
            table_intervention = pd.read_sql(table.statement, session.bind)      
            
    
    #        session.close()
            return table_intervention
        
        except:
            session.rollback()
#            yield None
        finally:
            session.close()
    def suppresion_intervention_by_id(self, id):
        
        try:
            Session = sessionmaker(bind= self.engine)
            session = Session()
    
#            id = int(donnees_en_dic.pop("ID"))
    
            session.query(self.INTERVENTION).filter(self.INTERVENTION.ID_INTERVENTION == id).delete()
            session.commit()
#            session.close()
        
        except :
            session.rollback()
#            session.close()
        
        finally:
            session.close()
        
