#-*- coding: utf-8 -*-
import win32com.client
from datetime import time
from datetime import datetime
#import time as tp
#from Package.AccesBdd import AccesBdd
#from pywintypes import Time

from PyQt4.QtGui import QMessageBox, QInputDialog 
#from PyQt4 import QtGui
from PyQt4 import QtCore, QtGui
import pandas as pd


class FichierEnregistreur():
    '''Classe gerant l'ensemble des enregistreurs'''
    
    def __init__(self,path_fichier,AccesBdd):
        
        self.path_fichier = path_fichier
        self.db = AccesBdd
        
    def fichier_datalog(self):
        '''fonction qui permet la lecture d'un fichier datalog : format txt'''
        
        with open(self.path_fichier, 'r') as fichier_datalog:
            donnees_fichier = fichier_datalog.readlines() #list avec une ligne fichier egal un el

#        print(donnees_fichier)
        nbr_lignes_fichier = len(donnees_fichier)
        
        list_ligne = []
        dict_fichier = {}
        
        for i in range(nbr_lignes_fichier):
            #transforme chaque ligne en list d'elements la composant
            if "\t" in donnees_fichier[i]:
                list_ligne.append(donnees_fichier[i].split("\t"))
            else:
                list_ligne.append(donnees_fichier[i].split())
                
            
#        print(list_ligne)
        nbr_colonnes = len(list_ligne[1])
                
        if len(list_ligne[0]) == 1: #test le fichier en effet il peut apparaitre ou non une date sur la ligne 0
            i = 0
            while i < nbr_colonnes:
                nom_colonne = list_ligne[1][i]
#                print(nom_colonne)
                
                list_donnees_colonne = []
                
                j =2
                while j < nbr_lignes_fichier:
    
                    try:
                        list_donnees_colonne.append(float(list_ligne[j][i].replace(",", ".")))
                        
                    except ValueError:
                        list_donnees_colonne.append(list_ligne[j][i])               
                    
                    j+=1
                dict_fichier[nom_colonne] = list_donnees_colonne #dictionnaire de list chaque list est une colonne du fichier
                
                i+=1
        else:
            i = 0
            while i < nbr_colonnes:
                nom_colonne = list_ligne[0][i]
                
                list_donnees_colonne = []
                
                j =2
                while j < nbr_lignes_fichier:
    
                    try:
                        list_donnees_colonne.append(float(list_ligne[j][i].replace(",", ".")))
                        
                    except ValueError:
                        list_donnees_colonne.append(list_ligne[j][i])               
                    
                    j+=1
                dict_fichier[nom_colonne] = list_donnees_colonne #dictionnaire de list chaque list est une colonne du fichier
                
                i+=1
#        print(list_donnees_colonne)
        return dict_fichier
        
    def fichier_ebro(self):
        '''fct permettant de lire et de renvoyer un dictinnaire de list des differentes colonnes du fichier ebr format xls.
        pour une sonde clef dicp n°serie et les donnees sont dans deux list (dateheure et donnees)'''
        
        #test avec pandas
#        print("coucou")
        
        df=pd.read_excel(self.path_fichier, 0, 0)

                
#        print(df)
##        print(type(df))
#        for ele in df.keys():
#            print(ele)
            
        return df
#        print(df["Numéro de série"])
        
#        xl = win32com.client.DispatchEx('Excel.Application')
#        classeur = xl.Workbooks.Open(self.path_fichier)
#
#        XlDirectionDown = 4
#        XlDirectionRight = 2
#        xl.Visible = True 
#        
#        # recherche nbr_colonnes et nbr de ligne :
#        
# 
#        #nbr_colonnes
#               
#        nbr_colonnes = xl.Range("A1").End(XlDirectionRight).Column
#        nbr_sondes = nbr_colonnes/2
#        
#
#        
#        list_dict = []
#        j=1
#        while j<= nbr_sondes :
#            dict_fichier = {}
#            list_date_heure = []
#            list_mesures_sonde = []
#
#            n_serie = str(int(classeur.ActiveSheet.Cells(1,2*j).Value))
#            
#            #recherche nbr_lignes_sonde:
#
#            nbr_lignes_sonde = xl.Range(classeur.ActiveSheet.Cells(8,2*j), classeur.ActiveSheet.Cells(8,2*j)).End(XlDirectionDown).Row
#
#            
#
#            #gestion des dates rapides :
#            valeur_date = [v[0] for v in classeur.ActiveSheet.Range(classeur.ActiveSheet.Cells(8,(2*j-1)), classeur.ActiveSheet.Cells(nbr_lignes_sonde,(2*j-1))).value]
#            
#            for date in valeur_date:
#                if len(date)>=19:
#                    date_string = date                    
#                else:
#                    date_string = date + " "+"00:00:00"
#                
#                date_conversion = datetime.strptime(date_string, "%d/%m/%Y %H:%M:%S")
#                list_date_heure.append(date_conversion.strftime("%Y-%m-%d %H:%M:%S"))
#            
#            #gestion donnees rapide
#            list_mesures_sonde = [float(v[0]) for v in classeur.ActiveSheet.Range(classeur.ActiveSheet.Cells(8,(2*j)), classeur.ActiveSheet.Cells(nbr_lignes_sonde,(2*j))).value]
#            
#        
#            
#            
#            dict_fichier["n_serie"] = n_serie
#            dict_fichier["identification_instrum"] = self.db.return_ident_instrum(n_serie)
#            dict_fichier["date_heure"] = list_date_heure
#            dict_fichier ["mesures"] = list_mesures_sonde
#            
#            list_dict.append(dict_fichier)
#            
#            j+=1
#            
##        print(list_dict)
#        xl.Application.Quit()
#
#        return list_dict
            
    def fichier_fd5(self):
        '''fct permettant d'ouvir et renvoyer les donnees fichier fd5 format txt'''
        
        with open(self.path_fichier, 'r') as fichier_fd5:
            donnees_fichier = fichier_fd5.readlines() #list avec une ligne fichier egal un el


        nbr_lignes_fichier = len(donnees_fichier)

        list_ligne = []
        dict_fichier = {}
        
        for i in range(nbr_lignes_fichier):
            list_ligne.append(donnees_fichier[i].split())#transforme chaque ligne en list d'elements la composant
        

        for ele in list_ligne[0]:    #trie pour elever tous les elemet (°C)        
            if ele == '(°C)':                
                list_ligne[0].remove('(°C)')
            elif ele == '()':
                list_ligne[0].remove('()')
        list_ligne[0].remove('M')
        
        if "Heure" not in list_ligne[0]:
            list_ligne[0].insert(2, "Heure")

        nbr_colonnes = len(list_ligne[0])

        i = 0
        while i < nbr_colonnes: #on a enlever la colonne 'M'

            nom_colonne = list_ligne[0][i]                    
 
            list_donnees_colonne = []            
            j =1
            while j < nbr_lignes_fichier:

                if len(list_ligne[j][i])!= 0:
                    try:
                        list_donnees_colonne.append(float(list_ligne[j][i].replace(",", ".")))
                        
                    except ValueError:
                        list_donnees_colonne.append(list_ligne[j][i])               
                else:
                    list_donnees_colonne.append(None)
                j+=1
            dict_fichier[nom_colonne] = list_donnees_colonne #dictionnaire de list chaque list est une colonne du fichier
            
            i+=1
        #on va modifier le format des heures  
        list_heure =[]
        for ele in dict_fichier["Heure"]:
            list_heure.append(ele[:len(ele)-4])
        dict_fichier["Heure"] = list_heure
        

        return dict_fichier
   
    
    def fichier_labovigil(self):
        '''fct permettant depuis un fichier extration labovigil (xls de renvoyer un dictionnaire de list:
        une lit dateheure et une list mesure'''
        
        xl = win32com.client.DispatchEx('Excel.Application')
        classeur = xl.Workbooks.Open(self.path_fichier)
        xl.Visible = True 
        
        dict_fichier = {}
        list_date = []
        list_donnees_sonde = []
        
        reference = classeur.ActiveSheet.Cells(1,2).Value
        n_serie = classeur.ActiveSheet.Cells(2,2).Value
        
        i=9
        while classeur.ActiveSheet.Cells(i,1).Value != None:
            date = str(classeur.ActiveSheet.Cells(i,1).Value)
            print(date[:len(date)-6])
            list_date.append(datetime.strptime(date[:len(date)-6], "%Y-%m-%d %H:%M:%S"))
#            datetime.strptime((classeur.ActiveSheet.Cells(i,1).Value +" "+classeur.ActiveSheet.Cells(i,2).Value), "%d/%m/%Y %H:%M:%S")
            list_donnees_sonde.append(float(classeur.ActiveSheet.Cells(i,3).Value))
           
            i+=1 
        
        dict_fichier["Date_Heure"] = list_date
        dict_fichier[n_serie[1:]]=list_donnees_sonde
        xl.Application.Quit()
            
        return dict_fichier
            

    def fichier_pc10(self):
        '''fct permettant depuis un fichier extration ltc10 (txt de renvoyer un dictionnaire de list:
        une list dateheure et une list mesure'''  
        
        with open(self.path_fichier, 'r') as fichier_fd5:
            donnees_fichier = fichier_fd5.readlines() #list avec une ligne fichier egal un el

#        ident_centrale = donnees_fichier[0][1].replace("#","-")
        
        nbr_lignes_fichier = len(donnees_fichier)
        
        
        list_ligne = []
        dict_fichier = {}
        nom_colonne =  []

        for ele in donnees_fichier[2].split("\t"):            
            if ele[1:len(ele)-1] == '"':            
                nom_colonne.append(ele[1:len(ele)-1].replace('"',"" ))
            else: 
                nom_colonne.append(ele.replace('\n', ""))
                
#        print("nom_colonne {}".format(nom_colonne))
        list_ligne.append(nom_colonne)
        for i in range(nbr_lignes_fichier):
            list_ligne.append(donnees_fichier[i].split())#transforme chaque ligne en list d'elements la composant
        
        #on enleve les 4 premieres lignes qui ne servent à rien et on remplace par nom_colonne
        #index egal à 1 car on a inseré nom_colonne
        list_ligne.pop(1)
        list_ligne.pop(1)
        list_ligne.pop(1)
        list_ligne.pop(1)

        nbr_colonnes = len(nom_colonne)
        
        i = 0
        while i < nbr_colonnes: 
            nom_colonne = list_ligne[0][i]                       
            list_donnees_colonne = []
            
            j =1
            while j < nbr_lignes_fichier - 3:

                try:
                    list_donnees_colonne.append(float(list_ligne[j][i].replace(",", ".")))
                    
                except ValueError:
                    list_donnees_colonne.append(list_ligne[j][i])               
                
                j+=1
            dict_fichier[nom_colonne] = list_donnees_colonne #dictionnaire de list chaque list est une colonne du fichier

            i+=1
#        print(" dict fichier  {}".format(dict_fichier))
        if dict_fichier.get("Intervalle", True):
            dict_fichier.pop("Intervalle")
            
        
        #on va modifier le format des heures  
        list_heure =[]
        for ele in dict_fichier["Heure"]:
            if len(ele)>8:
                list_heure.append(ele[:len(ele)-4])   
            else:
                list_heure.append(ele)

        dict_fichier["Heure"] = list_heure
#        print("list_heure {}".format(list_heure))
        return dict_fichier  
    
    def fichier_progesplus(self):
        '''fct permettant depuis un fichier extration progesplus (xls de renvoyer un dictionnaire de list:
        une list dateheure et une list mesure'''
        
        xl = win32com.client.DispatchEx('Excel.Application')
        classeur = xl.Workbooks.Open(self.path_fichier)
        xl.Visible = True 
        XlDirectionDown = 4
        
        parc = self.db.return_instrum_progesplus()
        list_n_serie = [x[1] for x in parc]
        
        dict_fichier = {}

        
        reference = classeur.ActiveSheet.Cells(5,6).Value
        identification = self.db.return_ident_instrum(reference)
#        print(identification)
        
        if len(identification)== 0:
            QMessageBox.critical(None, 
                                                ("Attention"),
                                                ("""L'enregistreur {} presente un pb sur son n°de serie'""".format(reference)))
                                                
                                                
            tuple = QInputDialog.getItem(None, 
                       ("N ° de serie"), 
                       ("Choisissez dans la liste le n° correspondant à {}".format(reference)),
                       list_n_serie)
            if tuple[1] == True:
                identification = tuple[0]
            else:
                identification = None
                                                
            
        
        
        #recherche nbr_lignes_sonde:

        nbr_lignes_sonde = xl.Range(classeur.ActiveSheet.Cells(5,1), classeur.ActiveSheet.Cells(5,1)).End(XlDirectionDown).Row

        

        #gestion des dates rapides :
        valeur_date = [datetime.strptime((v[0]+ " "+ v[1]),"%d/%m/%Y %H:%M:%S")  for v in classeur.ActiveSheet.Range(classeur.ActiveSheet.Cells(5,1), classeur.ActiveSheet.Cells(nbr_lignes_sonde,2)).value]
        

        
        #gestion donnees rapide
        list_mesures_sonde = [float(v[0]) for v in classeur.ActiveSheet.Range(classeur.ActiveSheet.Cells(5,3), classeur.ActiveSheet.Cells(nbr_lignes_sonde,3)).value]

    
          

        dict_fichier["Date_Heure"] = valeur_date

        dict_fichier[identification]= list_mesures_sonde
        dict_fichier["identification_instrum"] = identification

        xl.Application.Quit()
        
        

        return dict_fichier
        
    
    def fichier_sa32(self):
        '''fct traitant fichier sa32 txt et renvoie un dictionnaire de listes'''
        
        with open(self.path_fichier, 'r') as fichier_sa32:
            donnees_fichier = fichier_sa32.readlines() #list avec une ligne fichier egal un el

        nbr_lignes_fichier = len(donnees_fichier)
#        print(donnees_fichier)
#        print(nbr_lignes_fichier)
        
        list_ligne = []
        dict_fichier = {}
        nom_colonne =  []
#        print(donnees_fichier[0].split())
        if len(donnees_fichier[0].split()) == 1:
            for ele in donnees_fichier[1].split():
    #            print(ele)  
                nom_colonne.append(ele)
        else:
            for ele in donnees_fichier[0].split():
    #            print(ele)  
                nom_colonne.append(ele)
        nom_colonne_majuscule =[a.upper() for a in nom_colonne]
        
        
        list_ligne.append(nom_colonne)
        
        bolleen_colonne_cycle = False
        bolleen_colonne_inter = False
        for ele in nom_colonne_majuscule:
            if "Inter".upper() in ele:
                 bolleen_colonne_inter = True
            if "Cycle".upper() in ele:
                bolleen_colonne_cycle = True
        #mise en forme nom colonne inter , cycle , date , heures
        if bolleen_colonne_inter == True and bolleen_colonne_cycle == True:
            
            list_ligne [0][0] = 'Inter'
            list_ligne [0][1] = 'Cycle'
            list_ligne [0][2] = 'Date'
            list_ligne [0][3] = 'Heure'
            
        elif bolleen_colonne_inter == True and bolleen_colonne_cycle == False:
            list_ligne [0][0] = 'Inter'
#            list_ligne [0][2] = 'Cycle'
            list_ligne [0][1] = 'Date'
            list_ligne [0][2] = 'Heure'
            
        elif bolleen_colonne_inter == False and bolleen_colonne_cycle == True:
#            list_ligne [0][0] = 'Inter'
            list_ligne [0][0] = 'Cycle'
            list_ligne [0][1] = 'Date'
            list_ligne [0][2] = 'Heure'

        elif bolleen_colonne_inter == False and bolleen_colonne_cycle == False:
            list_ligne [0][0] = 'Date'
            list_ligne [0][1] = 'Heure'
        
#        print("list_ligne {}".format(list_ligne))
        
        for i in range(nbr_lignes_fichier):
            list_ligne.append(donnees_fichier[i].split())#transforme chaque ligne en list d'elements la composant

        #on enleve les 4 premieres lignes qui ne servent à rien et on remplace par nom_colonne
        #index egal à 1 car on a inseré nom_colonne
        if len(donnees_fichier[0].split()) == 1:
            list_ligne.pop(1)
            list_ligne.pop(1)
        else:
            list_ligne.pop(1)      
        
        
        
        nbr_colonnes = len(nom_colonne)


        i = 0
        while i < nbr_colonnes: 
            nom_colonne = list_ligne[0][i]                       
            list_donnees_colonne = []
            
            j =1
            while j < nbr_lignes_fichier - 1:

                try:
                    list_donnees_colonne.append(float(list_ligne[j][i].replace(",", ".")))
                    
                except ValueError:
                    list_donnees_colonne.append(list_ligne[j][i])               
                
                j+=1
            dict_fichier[nom_colonne] = list_donnees_colonne #dictionnaire de list chaque list est une colonne du fichier

            i+=1
#        print(dict_fichier)
        return dict_fichier
    
    def fichier_spy(self):
        '''fct qui ouvre fichier spy xls et regarde le nbr d'unite .
        Renvoie à la fin un dictinnaire de list'''
        
            
        xl = win32com.client.DispatchEx('Excel.Application')
        classeur = xl.Workbooks.Open(self.path_fichier)
        xl.Visible = True 
        
        #on recherche le nbr d'unité
        i=4
        while classeur.ActiveSheet.Cells(3,i).Value !=None:
            i+=1
         
        nbr_spy = i -4
        
        #Recherche nbr de ligne        
        i=3
        while classeur.ActiveSheet.Cells(i,1).Value !=None:
            i+=1
        nbr_ligne = i
        
        dict_fichier = {}
        i=4
        while i < nbr_spy+4: 
            list_instrument = []
            list_donnees_sonde = []
            list_date_heure = []
            
            j=4
            while j < nbr_ligne:
                if classeur.ActiveSheet.Cells(j,i).Value !=None:
                    
                    #colonne date
                    date = str(classeur.ActiveSheet.Cells(j,1).Value)
                                        
                    #Colonne Heure 
                    x = classeur.ActiveSheet.Cells(j,2).Value # a float
                    x = int(x * 24 * 3600) # convert to number of seconds
                    my_time = time(x//3600, (x%3600)//60, x%60) # hours, minutes, secondseure =                     
                    mise_en_forme_time = str(time.strftime(my_time, '%H:%M:%S'))
                    
                    
                    list_date_heure.append(datetime.strptime((date[:len(date)-15] +" "+ mise_en_forme_time), "%Y-%m-%d %H:%M:%S"))
                    list_donnees_sonde.append(classeur.ActiveSheet.Cells(j,i).Value)
                else:
                    pass
                                                   
                j+=1
            
            list_instrument.append(list_date_heure)
            list_instrument.append(list_donnees_sonde) 
            
            dict_fichier[classeur.ActiveSheet.Cells(3,i).Value] = list_instrument
            i+=1

        xl.Application.Quit()
        return dict_fichier
    
    def fichier_tag_ela(self):
        '''fct qui permet le traitement des fichier tag ela renvoie un dictionnaire de list'''
        
        xl = win32com.client.DispatchEx('Excel.Application')
        classeur = xl.Workbooks.Open(self.path_fichier)
        xl.Visible = True 
        
        XlDirectionDown = 4
        XlDirectionRight = 2
        xl.Visible = True 
        
        # recherche nbr_colonnes et nbr de ligne :
        
 
        #nbr_colonnes
               
        nbr_colonnes = xl.Range("A1").End(XlDirectionRight).Column
#        nbr_sondes = nbr_colonnes/2
        nbr_lignes = xl.Range(classeur.ActiveSheet.Cells(1,1), classeur.ActiveSheet.Cells(1,1)).End(XlDirectionDown).Row

        dict_fichier = {}   

        #gestion des nom colonnes rapides :
#        list_nom_colonnes = [v[0] for v in classeur.ActiveSheet.Range(classeur.ActiveSheet.Cells(1,1), classeur.ActiveSheet.Cells(1,nbr_colonnes)).value]
            
        
        
        #on recherche le nbr d'unité/et le nom colonnes
        
        #mise en forme excel:

        classeur.ActiveSheet.Range(classeur.ActiveSheet.Cells(2,2), classeur.ActiveSheet.Cells(nbr_lignes,2)).NumberFormat = "aaaa/mm/jj"
        classeur.ActiveSheet.Range(classeur.ActiveSheet.Cells(2,3), classeur.ActiveSheet.Cells(nbr_lignes,3)).NumberFormat = "0.000"
        classeur.ActiveSheet.Range(classeur.ActiveSheet.Cells(2,3), classeur.ActiveSheet.Cells(nbr_lignes,3)).NumberFormat = "aaaa/mm/jj hh:mm:ss"

        list_date = [datetime.strftime(v[0].date(), '%Y/%m/%d') for v in classeur.ActiveSheet.Range(classeur.ActiveSheet.Cells(2,2), classeur.ActiveSheet.Cells(nbr_lignes,2)).value]
        list_heure = [time.strftime(v[0].time(), '%H:%M:%S') for v in classeur.ActiveSheet.Range(classeur.ActiveSheet.Cells(2,3), classeur.ActiveSheet.Cells(nbr_lignes,3)).value]    
        nbr_tag = nbr_colonnes - 3 #3 colonne pour date heure et nbr et i=1   

        dict_fichier["Heure"] = list_heure
        dict_fichier["Date"] = list_date
        
        for i in range(4, nbr_tag):
            list_donnees_colonne = [v[0] for v in classeur.ActiveSheet.Range(classeur.ActiveSheet.Cells(2,i), classeur.ActiveSheet.Cells(nbr_lignes,i)).value]
            dict_fichier[classeur.ActiveSheet.Cells(1,i).value] = list_donnees_colonne

        
        xl.Application.Quit()
        return dict_fichier
        
    def fichier_testo(self):
        '''fct qui ouvre fichier testo xls et regarde le nbr d'unite .
        Renvoie à la fin un dictinnaire de list'''
        
            
        xl = win32com.client.DispatchEx('Excel.Application')
        classeur = xl.Workbooks.Open(self.path_fichier)
        xl.Visible = True 
        
        list_donnees_colonne = []
        list_date_heure = []
        dict_fichier = {}
        i=13
        while classeur.ActiveSheet.Cells(i,1).Value !=None:
            date = str(classeur.ActiveSheet.Cells(i,2).Value)
            list_date_heure.append(datetime.strptime(date, "%d/%m/%Y %H:%M:%S"))
            list_donnees_colonne.append(classeur.ActiveSheet.Cells(i,3).Value)
            i+=1 
        nom_instrument = classeur.ActiveSheet.Cells(3,2).Value
        n_serie = classeur.ActiveSheet.Cells(6,1).Value.split()
        
        dict_fichier["Date_Heure"] = list_date_heure
        dict_fichier["identification_instrum"] = self.db.return_ident_instrum(n_serie[0])
        
        dict_fichier[nom_instrument[:len(nom_instrument)-4]] = list_donnees_colonne
        
        
        xl.Application.Quit()
        
        return dict_fichier
        
    def fichier_logtag(self):
        '''fct traitant fichier logtag csv et renvoie un dictionnaire de listes'''
        
        with open(self.path_fichier, 'r') as fichier_logtag:
            donnees_fichier = fichier_logtag.readlines() #list avec une ligne fichier egal un el
         
        nbr_lignes_fichier = len(donnees_fichier)
       
        list_ligne_brute = []
        dict_fichier = {}
        nom_colonne =  []

        for ele in donnees_fichier[12].split():  
            nom_colonne.append(ele)
        
        for i in range(nbr_lignes_fichier):
            list_ligne_brute.append(donnees_fichier[i].split('"'))#transforme chaque ligne en list d'elements la composant

        list_ligne = []
        i=0
        while i < nbr_lignes_fichier:
            list_ligne_propre = [ele for ele in list_ligne_brute[i] if ele != "," and ele != "\n" and ele != ""]
            list_ligne.append(list_ligne_propre)
            
            i+=1
        
        identification_enregistreur = list_ligne[1][3]

        #on enleve les 12 premieres lignes qui ne servent à rien et on remplace par nom_colonne
        for i in range(12):
            list_ligne.pop(0)
            
        while len(list_ligne[0]) == 0:
            list_ligne.pop(0)
            i+=1
        
        dict_fichier = {}
        list_date_heure = []
        list_donnees_colonne =[]
        
        
        j=1
        while j < len(list_ligne):
#            datetime.strptime((date[:len(date)-1] +" "+ ele), "%d/%m/%Y %H:%M:%S")
#            print(j)
#            print(list_ligne[j][0])
#            print(list_ligne[j][1].replace(",", "."))
            list_date_heure.append(list_ligne[j][0])
            list_donnees_colonne.append(float(list_ligne[j][1].replace(",", ".")))
            
            j+=1
        #mise en forme date_heure:
        list_date_heure_mise_en_forme =[]
        for ele in list_date_heure:         
            element_list_date_heure = ele.split()
            element_date =  element_list_date_heure[0].split('/')

            day = element_date[0]
            
            
            if element_date[1][:3].capitalize().replace("é", "e") != "Jui":
                month_1 = element_date[1][:3].capitalize().replace("é", "e")
                month = month_1.replace("û", "u")
                english_month = {"Jan":"Jan", "Fev":"Feb", "Mar":"Mar", 
                            "Avr":"Apr", "Mai":"May","Jui":"Jun", 
                            "Jui":"Jul", "Aou":"Aug", "Sep":"Sep", 
                            "Oct":"Oct", 'Nov':"Nov", "Dec":"Dec"}
            else : 
                month = element_date[1][:4].capitalize().replace("é", "e")
                
                english_month = {"Juin":"Jun", 
                            "Juil":"Jul"}
                
                           
                            
            year = element_date[2]            
            heure_mise_en_forme = element_list_date_heure[1].replace(",", "")# sur certains fichiers une virgule apparait apres l'heure
            
            list_date_heure_mise_en_forme.append(datetime.strptime((day +"/"+english_month[month]+"/"+year+ " "+heure_mise_en_forme), "%d/%b/%Y %H:%M:%S"))
#            
        dict_fichier["Date_Heure"] = list_date_heure_mise_en_forme
        dict_fichier[identification_enregistreur] = list_donnees_colonne
        
        #modification n° serie pour ne pas avoir de 0 devant

        i=0
        while identification_enregistreur[i] == "0":
            n_serie_modi = identification_enregistreur[i+1:]
            i+=1
        
        parc = self.db.return_instrum_waranet()
        list_n_serie = [x[1] for x in parc]
        
        list_n_serie_modifie = []
        for nserie in list_n_serie:
            if nserie[0] == "0":
                i=0
                while nserie[i] == "0":
                    n_serie_modi_2 = nserie[i+1:]
                    i+=1
            
                list_n_serie_modifie.append(n_serie_modi_2)
            else:
                list_n_serie_modifie.append(nserie)
#        print(list_n_serie_modifie)    
        
        if n_serie_modi in list_n_serie_modifie:
            dict_fichier["identification_instrum"] = parc[list_n_serie_modifie.index(n_serie_modi)][0]

        else :
#            a = QtGui.QApplication(sys.argv)
            QMessageBox.critical(None, 
                                    ("Attention"),
                                    ("""L'enregistreur {} presente un pb sur son n°de serie""".format(n_serie_modi)))
                                    
            tuple = QInputDialog.getItem(None, 
                       ("N ° de serie"), 
                       ("Choisissez dans la liste le n° correspondant à {}".format(n_serie_modi)),
                       list_n_serie_modifie)
            if tuple[1] == True:
                dict_fichier["identification_instrum"] = parc[list_n_serie_modifie.index(tuple[0])][0]
            else:
                dict_fichier = None
            
                
#            print(dict_fichier)
            
            
        return dict_fichier
        
        
    def fichier_waranet_puce(self):
        '''fct traitant fichier puces waranet et renvoie un dictionnaire de listes'''
        
        with open(self.path_fichier, 'r') as fichier_puce:
            donnees_fichier = fichier_puce.readlines() #list avec une ligne fichier egal un el
        
        nbr_lignes_fichier = len(donnees_fichier)
       
        list_ligne_brute = []
        dict_fichier = {}
        nom_colonne =  []

        for ele in donnees_fichier[12].split():  
            nom_colonne.append(ele)
        
        for i in range(nbr_lignes_fichier):
            list_ligne_brute.append(donnees_fichier[i].split('"'))#transforme chaque ligne en list d'elements la composant
        
        list_ligne = []
        i=0
        while i < nbr_lignes_fichier:
            list_ligne_propre = [ele for ele in list_ligne_brute[i] if ele != "," and ele != "\n" and ele != ""]
            list_ligne.append(list_ligne_propre)
            
            i+=1
        identification_enregistreur = list_ligne[1][3]

        #on enleve les 12 premieres lignes qui ne servent à rien et on remplace par nom_colonne
        for i in range(12):
            list_ligne.pop(0)
            
        dict_fichier = {}
        list_date_heure = []
        list_donnees_colonne =[]

        j=1
        while j < len(list_ligne):
            list_date_heure.append(list_ligne[j][0])
            list_donnees_colonne.append(float(list_ligne[j][1].replace(",", ".")))
            
            j+=1
            
        dict_fichier["Date_Heure"] = list_date_heure
        dict_fichier[identification_enregistreur] = list_donnees_colonne
    
        #modification n° serie pour ne pas avoir de 0 devant

        i=0
        while identification_enregistreur[i] == "0":
            n_serie_modi = identification_enregistreur[i+1:]
            i+=1
        
        parc = self.db.return_instrum_waranet()
        list_n_serie = [x[1] for x in parc]
        
        list_n_serie_modifie = []
        for nserie in list_n_serie:
            if nserie[0] == "0":
                i=0
                while nserie[i] == "0":
                    n_serie_modi_2 = nserie[i+1:]
                    i+=1
            
                list_n_serie_modifie.append(n_serie_modi_2)
            else:
                list_n_serie_modifie.append(nserie)
            

        dict_fichier["identification_instrum"] = parc[list_n_serie_modifie.index(n_serie_modi)][0]



    

        return dict_fichier
    
    
    def traitement_fichier_etalon(self):
        '''Gestion de l'importation des donnees TXT et de leur mise en forme'''
#        try:        
        with open(self.path_fichier, 'r') as fichier_etalon:
            donnees_etalon = fichier_etalon.readlines()

        ligne = []
        for texte in donnees_etalon :
            ligne.append(texte)
        
        #nbr de lignes du fichier
        nbr_lignes_fichier = len(donnees_etalon)

        #gestion test sur le nbr d'etalons (lignes: 5 à 10)
        i = 0
        nbr_etalon = 1
        while i <= 4 :            
            lettres=[lettre for lettre in ligne[i+5]]            
            if lettres[0]=="T":                
                nbr_etalon += 1                
            i+=1
        
        date = ligne[0]
        operateur = ligne[1]
#        ligne_generateur = []
        ligne_generateur = ligne[3].split()        
        generateur = ligne_generateur[1]
        pt_consigne = int(float((ligne[2].split()[3][2:-2].replace(",", "."))))
        
       
        ligne_etalon = ligne[4].split()
        etalon = ligne_etalon[0]
        premiere_donnees = 4+nbr_etalon + 3
        
        i = premiere_donnees
        valeurs={}
        nbr_colonne = 2* nbr_etalon + 2
        j=0
        donnees_fichier = []
           
        #mise en place des donnees du fichier en dictionnaire : indice = colonne de mesure et valeur list de toutes les donnees en colonnes
        #indice 0= n° mesure, indice 1=datage mesure , indice 2=etal1,indice3=etal 3..... 
                
        while i<= nbr_lignes_fichier-1:
            
            ligne_valeurs = ligne[i].split()
            donnees_fichier.append(ligne[i].split())
           
            while j< nbr_colonne :
                valeurs[j]=[]
                j+=1
                
            for indice , elements in enumerate(ligne_valeurs) :
                valeurs[indice].append(elements)
                
            i+=1
        
        horodatage = []
        for ele in valeurs[1]:

            horodatage.append( datetime.strptime((date[:len(date)-1] +" "+ ele), "%d/%m/%Y %H:%M:%S"))

        
        valeurs[1] = horodatage
        valeurs["operateur"] = operateur
        valeurs["generateur"] = generateur
        valeurs["etalon"] = etalon
        valeurs["pt_consigne"] = pt_consigne
        
        return valeurs
#        except :
#            pass

        

