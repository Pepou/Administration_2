#-*- coding: utf-8 -*-
from sqlalchemy import *
from sqlalchemy.orm import *
from sqlalchemy.engine import create_engine
from sqlalchemy import func

class AccesBdd():
    '''class gerant la bdd'''
    
    def __init__(self, engine, meta):
#        self.namebdd = "Labo_Metro_Prod"#"Labo_Metro_Test_3"#"Labo_Metro_Prod"# #
#        self.adressebdd = "10.42.1.74" #"localhost"  #"10.42.1.74"          
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
    
     
    def instruments(self):
        
        table = Table("INSTRUMENTS", self.meta)
        ins = select([table.c.IDENTIFICATION]).where(table.c.DOMAINE_MESURE == "Température")

        list_instruments = [inst[0] for inst in self.connection.execute(ins).fetchall()]  

#        print(list_instruments)
        
        return list_instruments
  
        
    def return_ident_instrum(self, n_serie):
        '''retourne certaines caracteristiques instrument
            constructeur
            reference_constructeur
            n_serie'''
        
        result = self.connection.execute("""SELECT "IDENTIFICATION" 
                    FROM "INSTRUMENTS" WHERE "N_SERIE" ='{}'""".format(n_serie)).fetchone()
        if result != None:
            ident = result[0]
        else:
            ident = None
        return ident
        
    def return_ident_instrum_logtag(self, n_serie):
        '''retourne certaines caracteristiques instrument
            constructeur
            reference_constructeur
            n_serie'''

        table = Table("INSTRUMENTS", self.meta)
        ins = select([table.c.IDENTIFICATION]).where(table.c.N_SERIE.like("%{}%".format(n_serie)))

        result = self.connection.execute(ins).fetchall()  
#        print(result)
#        for ele in result:
#            print(ele)
        
        return result
  
    def return_instrum_waranet(self):
        
        table = Table("INSTRUMENTS", self.meta)
        ins = select([table.c.IDENTIFICATION, table.c.N_SERIE]).where(func.lower(table.c.CONSTRUCTEUR) == func.lower("Waranet"))
        waranet = self.connection.execute(ins).fetchall()          
   
        
        return waranet
        
        
    def return_instrum_progesplus(self):
        
        table = Table("INSTRUMENTS", self.meta)
        ins = select([table.c.IDENTIFICATION, table.c.N_SERIE]).where(func.lower(table.c.CONSTRUCTEUR) == func.lower("Proges plus"))
        progesplus = self.connection.execute(ins).fetchall()          
   
        
        return progesplus
        
    def return_caract_instrum(self, ident):
        table = Table("INSTRUMENTS", self.meta)
        ins = select([table.c.CONSTRUCTEUR, table.c.N_SERIE, table.c.TYPE, table.c.RESOLUTION, table.c.COMMENTAIRE]).where(table.c.IDENTIFICATION == ident)
        carac =self.connection.execute(ins).fetchone()
#        print("caract {}".format(carac))
        
#        print(carac)
        return carac
        
    def gestion_combobox_onglet_operateur(self):
        
        table = Table("TECHNICIEN", self.meta)
        ins = select([table.c.PRENOM]).order_by(table.c.ID_TECHNICIEN)
        operateur = self.connection.execute(ins).fetchall()
        
        return operateur
        
    def list_generateur(self):
        list_generateur = []
        table = Table("INSTRUMENTS", self.meta)
        ins = select([table.c.IDENTIFICATION]).where(and_(table.c.DESIGNATION == 'Bain de Glace Fondante', table.c.ETAT_UTILISATION == 'En service'))#.order_by(table.c.IDENTIFICATION)
        
        bgf = [x[0] for x in self.connection.execute(ins).fetchall()]
        
        ins = select([table.c.IDENTIFICATION]).where(and_(table.c.DESIGNATION == "Bain d'etalonnage", table.c.ETAT_UTILISATION == 'En service'))
        hart = [x[0]for x in self.connection.execute(ins).fetchall()]
        
        
        
        ins = select([table.c.IDENTIFICATION]).where(and_(table.c.DESIGNATION == "Enceinte climatique", table.c.ETAT_UTILISATION == 'En service'))
        enceinte = [x[0] for x in self.connection.execute(ins).fetchall()]
        
#        list_generateur.append(bgf)+hart+enceinte
        
        list_generateur = bgf + hart +enceinte
#        list_generateur.sort()
        
#        print(list_generateur)
        
        return list_generateur
        
        
    def list_etalon(self):
        
        table = Table("INSTRUMENTS", self.meta)
        
        ins = select([table.c.IDENTIFICATION]).where(and_(table.c.DESIGNATION == 'Etalon',table.c.ETAT_UTILISATION == 'En service' )).order_by(table.c.ID_INSTRUM)
        list_etalon = [x[0] for x in self.connection.execute(ins).fetchall()]
        
        
        return list_etalon
        
        
        
        
        
    def id_poly(self, ref):
        
        table = Table("POLYNOME_CORRECTION", self.meta)
        ins = select([table.c.ID_POLYNOME]).where(and_(table.c.IDENTIFICATION == ref,table.c.ARCHIVAGE == False ))
        id = self.connection.execute(ins).fetchone()[0]
        
        return id
        
