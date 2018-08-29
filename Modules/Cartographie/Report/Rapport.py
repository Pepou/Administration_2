from reportlab.pdfgen import canvas
from reportlab.platypus import Table,  TableStyle
#from reportlab.lib.pagesizes import letter, inch
from reportlab.lib import colors
from reportlab.lib.pagesizes import A4 
from reportlab.lib.units import cm
from reportlab.graphics.charts.lineplots import LinePlot
from reportlab.graphics.charts.legends import LineLegend
from reportlab.graphics.charts.textlabels import Label
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
#from reportlab.lib.validators import Auto
from reportlab.lib.utils import ImageReader
#from PIL import Image

#from reportlab.graphics.widgets.markers import makeMarker
from reportlab.graphics.shapes import Drawing
#import numpy as np
from reportlab.graphics import renderPDF
#import pandas as pd
from itertools import zip_longest
import datetime, time
from path import Path
import pendulum
import json

from PyQt4.QtGui import QMessageBox

class Rapport():
    
    
    _cube_resultat_9s = Path('Modules/Cartographie/Ressources/cube_resultat_9s.jpg')
    _cube_resultat_15s =  Path('Modules/Cartographie/Ressources/cube_resultat_15s.jpg')
    
    dict_couleurs = {"ReportLabBlue": colors.Color(0,.2,.498039,1), "ReportLabBlueOLD": colors.Color(.305882,.337255,.533333,1), "ReportLabFidBlue": colors.Color(.2,.4,.8,1), 
           "ReportLabFidRed": colors.Color(.8,0,.2,1), "ReportLabGreen": colors.Color(.2,.4,0,1), "ReportLabLightBlue": colors.Color(.717647,.72549,.827451,1), 
            "ReportLabLightGreen": colors.Color(.2,.6,.2,1), "aliceblue": colors.Color(.941176,.972549,1,1), "antiquewhite": colors.Color(.980392,.921569,.843137,1), 
            "aqua": colors.Color(0,1,1,1), "aquamarine": colors.Color(.498039,1,.831373,1), "azure": colors.Color(.941176,1,1,1), "beige": colors.Color(.960784,.960784,.862745,1), 
            "bisque": colors.Color(1,.894118,.768627,1), "black": colors.Color(0,0,0,1), "blanchedalmond": colors.Color(1,.921569,.803922,1), "blue": colors.Color(0,0,1,1), 
            "blueviolet": colors.Color(.541176,.168627,.886275,1), "brown": colors.Color(.647059,.164706,.164706,1), "burlywood": colors.Color(.870588,.721569,.529412,1), 
            "cadetblue": colors.Color(.372549,.619608,.627451,1), "chartreuse": colors.Color(.498039,1,0,1),"chocolate": colors.Color(.823529,.411765,.117647,1), 
            "coral": colors.Color(1,.498039,.313725,1), "cornflower": colors.Color(.392157,.584314,.929412,1), "cornflowerblue": colors.Color(.392157,.584314,.929412,1), 
            "cornsilk": colors.Color(1,.972549,.862745,1), "crimson": colors.Color(.862745,.078431,.235294,1), "cyan": colors.Color(0,1,1,1), "darkblue": colors.Color(0,0,.545098,1), 
            "darkcyan": colors.Color(0,.545098,.545098,1), "darkgoldenrod": colors.Color(.721569,.52549,.043137,1), "darkgray": colors.Color(.662745,.662745,.662745,1), 
            "darkgreen": colors.Color(0,.392157,0,1), "darkgrey": colors.Color(.662745,.662745,.662745,1),  "darkkhaki": colors.Color(.741176,.717647,.419608,1), 
            "darkmagenta": colors.Color(.545098,0,.545098,1), "darkolivegreen": colors.Color(.333333,.419608,.184314,1),"darkorange": colors.Color(1,.54902,0,1), 
            "darkorchid": colors.Color(.6,.196078,.8,1), "darkred": colors.Color(.545098,0,0,1), "darksalmon": colors.Color(.913725,.588235,.478431,1), 
            "darkseagreen": colors.Color(.560784,.737255,.545098,1), "darkslateblue": colors.Color(.282353,.239216,.545098,1), "darkslategray": colors.Color(.184314,.309804,.309804,1), 
            "darkslategrey": colors.Color(.184314,.309804,.309804,1), "darkturquoise": colors.Color(0,.807843,.819608,1), "darkviolet": colors.Color(.580392,0,.827451,1), 
            "deeppink": colors.Color(1,.078431,.576471,1), "deepskyblue": colors.Color(0,.74902,1,1), "dimgray": colors.Color(.411765,.411765,.411765,1), 
            "dimgrey": colors.Color(.411765,.411765,.411765,1), "dodgerblue": colors.Color(.117647,.564706,1,1), "fidblue": colors.Color(.2,.4,.8,1), 
            "fidlightblue": colors.Color(.839216,.878431,.960784,1), "fidred" : colors.Color(.8,0,.2,1), "firebrick": colors.Color(.698039,.133333,.133333,1), 
            "floralwhite": colors.Color(1,.980392,.941176,1), "forestgreen": colors.Color(.133333,.545098,.133333,1), "fuchsia": colors.Color(1,0,1,1), 
            "gainsboro": colors.Color(.862745,.862745,.862745,1), "ghostwhite": colors.Color(.972549,.972549,1,1), "gold": colors.Color(1,.843137,0,1), 
            "goldenrod": colors.Color(.854902,.647059,.12549,1), "gray": colors.Color(.501961,.501961,.501961,1),  "green": colors.Color(0,.501961,0,1), 
            "greenyellow": colors.Color(.678431,1,.184314,1), "grey": colors.Color(.501961,.501961,.501961,1), "honeydew": colors.Color(.941176,1,.941176,1), 
            "hotpink": colors.Color(1,.411765,.705882,1), "indianred": colors.Color(.803922,.360784,.360784,1), "indigo": colors.Color(.294118,0,.509804,1), 
            "ivory": colors.Color(1,1,.941176,1), "khaki": colors.Color(.941176,.901961,.54902,1), "lavender": colors.Color(.901961,.901961,.980392,1), "lavenderblush": colors.Color(1,.941176,.960784,1), 
            "lawngreen": colors.Color(.486275,.988235,0,1), "lemonchiffon": colors.Color(1,.980392,.803922,1), "lightblue": colors.Color(.678431,.847059,.901961,1), 
            "lightcoral": colors.Color(.941176,.501961,.501961,1), "lightcyan": colors.Color(.878431,1,1,1), "lightgoldenrodyellow": colors.Color(.980392,.980392,.823529,1), 
            "lightgreen": colors.Color(.564706,.933333,.564706,1), "lightgrey": colors.Color(.827451,.827451,.827451,1), "lightpink": colors.Color(1,.713725,.756863,1), 
            "lightsalmon": colors.Color(1,.627451,.478431,1), "lightseagreen": colors.Color(.12549,.698039,.666667,1), "lightskyblue": colors.Color(.529412,.807843,.980392,1), 
            "lightslategray": colors.Color(.466667,.533333,.6,1), "lightslategrey": colors.Color(.466667,.533333,.6,1), "lightsteelblue": colors.Color(.690196,.768627,.870588,1), 
            "lightyellow": colors.Color(1,1,.878431,1), "lime": colors.Color(0,1,0,1), "limegreen": colors.Color(.196078,.803922,.196078,1), "linen": colors.Color(.980392,.941176,.901961,1), 
            "magenta": colors.Color(1,0,1,1), "maroon": colors.Color(.501961,0,0,1), "mediumaquamarine": colors.Color(.4,.803922,.666667,1), "mediumblue": colors.Color(0,0,.803922,1), 
            "mediumorchid": colors.Color(.729412,.333333,.827451,1),  "mediumpurple": colors.Color(.576471,.439216,.858824,1),  "mediumseagreen": colors.Color(.235294,.701961,.443137,1), 
            "mediumslateblue": colors.Color(.482353,.407843,.933333,1),  "mediumspringgreen": colors.Color(0,.980392,.603922,1),  "mediumturquoise": colors.Color(.282353,.819608,.8,1), 
            "mediumvioletred": colors.Color(.780392,.082353,.521569,1),  "midnightblue": colors.Color(.098039,.098039,.439216,1),  "mintcream": colors.Color(.960784,1,.980392,1), 
            "mistyrose": colors.Color(1,.894118,.882353,1), "moccasin": colors.Color(1,.894118,.709804,1), "navajowhite": colors.Color(1,.870588,.678431,1),  
            "navy": colors.Color(0,0,.501961,1), "oldlace": colors.Color(.992157,.960784,.901961,1), "olive": colors.Color(.501961,.501961,0,1),  "olivedrab": colors.Color(.419608,.556863,.137255,1), 
            "orange": colors.Color(1,.647059,0,1), "orangered": colors.Color(1,.270588,0,1), "orchid": colors.Color(.854902,.439216,.839216,1), "palegoldenrod": colors.Color(.933333,.909804,.666667,1), 
            "palegreen": colors.Color(.596078,.984314,.596078,1), "paleturquoise": colors.Color(.686275,.933333,.933333,1), "palevioletred": colors.Color(.858824,.439216,.576471,1), 
            "papayawhip": colors.Color(1,.937255,.835294,1), "peachpuff": colors.Color(1,.854902,.72549,1), "peru": colors.Color(.803922,.521569,.247059,1), "pink": colors.Color(1,.752941,.796078,1), 
            "plum": colors.Color(.866667,.627451,.866667,1), "powderblue": colors.Color(.690196,.878431,.901961,1), "purple": colors.Color(.501961,0,.501961,1), 
            "red": colors.Color(1,0,0,1), "rosybrown": colors.Color(.737255,.560784,.560784,1), "royalblue": colors.Color(.254902,.411765,.882353,1), 
            "saddlebrown": colors.Color(.545098,.270588,.07451,1), "salmon": colors.Color(.980392,.501961,.447059,1), "sandybrown": colors.Color(.956863,.643137,.376471,1), 
            "seagreen": colors.Color(.180392,.545098,.341176,1), "seashell": colors.Color(1,.960784,.933333,1), "sienna": colors.Color(.627451,.321569,.176471,1), 
            "silver": colors.Color(.752941,.752941,.752941,1), "skyblue": colors.Color(.529412,.807843,.921569,1), "slateblue": colors.Color(.415686,.352941,.803922,1), 
            "slategray": colors.Color(.439216,.501961,.564706,1), "slategrey": colors.Color(.439216,.501961,.564706,1), "snow": colors.Color(1,.980392,.980392,1), 
            "springgreen": colors.Color(0,1,.498039,1), "steelblue": colors.Color(.27451,.509804,.705882,1), "tan": colors.Color(.823529,.705882,.54902,1), 
            "teal": colors.Color(0,.501961,.501961,1), "thistle": colors.Color(.847059,.74902,.847059,1), "tomato": colors.Color(1,.388235,.278431,1), 
            "transparent": colors.Color(0,0,0,0), "turquoise": colors.Color(.25098,.878431,.815686,1), "violet": colors.Color(.933333,.509804,.933333,1), 
            "wheat": colors.Color(.960784,.870588,.701961,1), "white": colors.Color(1,1,1,1), "whitesmoke": colors.Color(.960784,.960784,.960784,1), 
            "yellow": colors.Color(1,1,0,1), "yellowgreen": colors.Color(.603922,.803922,.196078,1) 
            }
    couleur_dark = {"darkblue": colors.Color(0,0,.545098,1), 
                                    "darkcyan": colors.Color(0,.545098,.545098,1), "darkgoldenrod": colors.Color(.721569,.52549,.043137,1), 
                                    "darkgray": colors.Color(.662745,.662745,.662745,1), "darkgreen": colors.Color(0,.392157,0,1), 
                                    "darkgrey": colors.Color(.662745,.662745,.662745,1),  "darkkhaki": colors.Color(.741176,.717647,.419608,1), 
                                    "darkmagenta": colors.Color(.545098,0,.545098,1), "darkolivegreen": colors.Color(.333333,.419608,.184314,1),
                                    "darkorange": colors.Color(1,.54902,0,1), "darkorchid": colors.Color(.6,.196078,.8,1), 
                                    "darkred": colors.Color(.545098,0,0,1), "darksalmon": colors.Color(.913725,.588235,.478431,1), 
                                    "darkseagreen": colors.Color(.560784,.737255,.545098,1), "darkslateblue": colors.Color(.282353,.239216,.545098,1), 
                                    "darkslategray": colors.Color(.184314,.309804,.309804,1), "darkslategrey": colors.Color(.184314,.309804,.309804,1), 
                                    "darkturquoise": colors.Color(0,.807843,.819608,1), "darkviolet": colors.Color(.580392,0,.827451,1)}

    
    
    def __init__(self, chemin):
        
#        print(chemin)
        if ".pdf" not in chemin:
            self.fichier =chemin + ".pdf"
        else:
            self.fichier = chemin
            
        with open("config_bdd.json") as json_file:
            config_bdd = json.load(json_file)        
        site = config_bdd["site"]
        
        if site == "LMS":
            self._logo_efs = Path('Modules/Cartographie/Ressources/Logo EFS LMS.JPG')
        elif site == "ORLS":
            self._logo_efs = Path('Modules/Cartographie/Ressources/Logo EFS ORLS.JPG')
    
    def rapport_carto(self, donnees):
        """fct qui cree la page de garde """
        administratif = donnees["administratif"]
        resultat = donnees["resultats"]
#        nb_page_total = 1
        c = canvas.Canvas(self.fichier)
        width, height = A4
        
        pdfmetrics.registerFont(TTFont('Arial', 'Arial.ttf'))
        pdfmetrics.registerFont(TTFont('Arial-Bold', 'Arialbd.ttf'))
        
        #Logo
        c.drawImage(self._logo_efs, 1.5*cm, 22*cm, width=5.5*cm, preserveAspectRatio=True) 
        
        #Titre
        c.setFont("Arial", 16)
        c.drawString(8.0*cm,20.3*cm,"RAPPORT D'ESSAI")
        
        #n° Cartographie
        c.setFont("Arial", 12.5)
        if len(administratif["num_rapport"])<=14:
            c.drawString(8.5*cm,19.6*cm,"N° {}".format(administratif["num_rapport"]))
        else:
            c.drawString(5.5*cm,19.6*cm,"N° {}".format(administratif["num_rapport"]))
    
        #Adresse client
        c.setFont("Arial", 8)
        c.drawString(1.7*cm,17.1*cm,"DÉLIVRÉ À :")
        
        if administratif["affectation"] == "None" or administratif["affectation"] == ".":
            text_ob = c.beginText(4.5*cm,17.1*cm)
            text_ob.textLines(f'{administratif["nom_client"]} \n{administratif["adresse_client"]}\n{administratif["code_postal_client"]} {administratif["ville_client"]}')
            c.drawText(text_ob)
        else:
            text_ob = c.beginText(4.5*cm,17.1*cm)
            text_ob.textLines(f'{administratif["nom_client"]} ({administratif["affectation"]}) \n{administratif["adresse_client"]}\n{administratif["code_postal_client"]} {administratif["ville_client"]}')
            c.drawText(text_ob)

        #Enceintes:        
        c.setFont("Arial", 10.5)
        c.drawString(1.7*cm,15.2*cm,"DISPOSITIF CARTOGRAPHIÉ")

        c.setFont("Arial", 8)
        c.drawString(1.7*cm,13.8*cm,"Désignation :")
        c.drawString(4.5*cm,13.8*cm,"Enceinte Réfrigérée")
        
        c.drawString(9.6*cm,13.8*cm,"Désignation Littérale :")
        c.drawString(13*cm,13.8*cm,administratif["design_litt"])
        
        c.drawString(1.7*cm,12.8*cm,"Constructeur")
        c.drawString(4.5*cm,12.8*cm,administratif["constructeur_enceinte"])
        
        c.drawString(1.7*cm,11.7*cm,"Model :")
        c.drawString(4.5*cm,11.7*cm,administratif["model_enceinte"])
        
        c.drawString(9.6*cm,11.7*cm,"N° de série :")
        c.drawString(13*cm,11.7*cm,administratif["nserie_enceinte"])
        
        c.drawString(9.6*cm,10.7*cm,"N° d'identification :")
        c.drawString(13*cm,10.7*cm,administratif["ident_enceinte"])
        
        #administration du rapport
        if donnees["simulation"]["simulation"]:
            c.drawString(1.7*cm,9*cm,"Ce document comporte 3 pages et 2 annexes")
        else:
            c.drawString(1.7*cm,9*cm,"Ce document comporte 3 pages et 1 annexe")
        
        date_emission= pendulum.now('Europe/Paris').format('%d/%m/%Y')
        c.drawString(12.8*cm,9*cm,"Date d'émission : {}".format(date_emission))

        c.setFont("Arial", 7)
        c.drawString(14*cm,7.8*cm,"Approuvé par")    
        
        #pied de page
        c.setFont("Arial", 4.5)
        c.drawString(1.7*cm,0.8*cm,"LA REPRODUCTION DE CE RAPPORT N'EST AUTORISÉE QUE SOUS LA FORME DE FAC-SIMILÉ PHOTOGRAPHIQUE INTÉGRAL.")
    
        c.setFont("Arial", 9)
        c.drawString(17.8*cm,0.8*cm,"Page 1 / 3")
    
        c.showPage()
        
        
        ############Page n°2################
        
        #n° Cartographie
        c.setFont("Arial", 9)
        c.drawString(1.7*cm,28.4*cm,"RAPPORT D'ESSAI N° {}".format(administratif["num_rapport"]))
        c.setFont("Arial", 8)
#        c.drawString(1.7*cm,28*cm,"N°Identification {}".format(administratif["ident_enceinte"]))
        
        
        #Administration
        c.setFont("Arial-Bold", 10)
        c.drawString(9.8*cm,27*cm,"Application")
        c.rect(1.3*cm, 26.9*cm, 18.1*cm, 0.4*cm , stroke=1, fill=0)
        
        
        c.setFont("Arial", 10)        
        c.drawString(1.7*cm,26.2*cm,"N°Identification : {}".format(administratif["ident_enceinte"]))
        
        Application = administratif["application"]
             
        c.drawString(1.7*cm,25.2*cm,"Application : {}".format(Application))
        
        if administratif["type_consign"] != "*":
            c.drawString(13*cm,25.2*cm,"Température consigne : {}°C".format(administratif["temp_consign"]))
        else:
            c.drawString(13*cm,25.2*cm,"Repère consigne : {}".format(administratif["temp_consign"]))
#            
            
        c.drawString(1.7*cm,24.2*cm,"Condition désirée : {}°C".format(administratif["condition_desiree"]))
        
        emt_processus = administratif["emt_processus"]
        
        signe = administratif["signe_EMT"]
        if float(emt_processus) != 0:
            c.drawString(13*cm,24.2*cm,"EMT processus : {} {} °C".format(signe, emt_processus))
        else:
            c.drawString(13*cm,24.2*cm,"EMT processus : na")
        
        
        nom_resp_mesure = administratif["responsable_mesure"]
        c.drawString(1.7*cm,23.2*cm,"Responsable des mesures : {}".format(nom_resp_mesure))

        
        index_debut = donnees["annexe"]["INDEX_DEBUT"]        
#        index_fin = donnees["annexe"]["INDEX_FIN"] + 1
        date_debut = donnees["annexe"]["DONNEES"]["Date"].iloc[index_debut].strftime("%d/%m/%Y") 
#        date_fin = donnees["annexe"]["DONNEES"]["Date"].iloc[index_fin-1].strftime("%d-%m-%Y %H:%M:%S")
        date_execution = "{}".format(date_debut)
        c.drawString(13*cm,23.2*cm,"Date d'exécution : {}".format(date_execution))
        
        
        c.rect(1.3*cm, 22.8*cm, 18.1*cm, 3.8*cm , stroke=1, fill=0)

        c.setFont("Arial-Bold", 10)
        c.drawString(9.8*cm,22.2*cm,"Méthode")
        c.rect(1.3*cm, 22.1*cm, 18.1*cm, 0.4*cm , stroke=1, fill=0)
        
        
        c.setFont("Arial", 10)
        doc_ref = "FD X 15-140"
        c.drawString(1.7*cm,21.4*cm,"Document de référence : {}".format(doc_ref))
        
        procedure ="CPL/PIL/SUR/MET/MO/010"
        c.drawString(13*cm,21.4*cm,"Procedure : {}".format(procedure))
        
        c.rect(1.3*cm, 21.1*cm, 18.1*cm, 0.7*cm , stroke=1, fill=0)
        
        #Moyen de mesure :
#        print(administratif)
        c.setFont("Arial-Bold", 10)
        c.drawString(9.8*cm,20.4*cm,"Moyen de mesure")
        c.rect(1.3*cm, 20.3*cm, 18.1*cm, 0.4*cm , stroke=1, fill=0)
        
        c.setFont("Arial", 10)
        modele_centrale = administratif["model_centrale"]
        c.drawString(1.7*cm,19.7*cm,"Model : {}".format(modele_centrale))
        
        identification_centrale = administratif["nom_centrale"]
        c.drawString(1.7*cm,19.2*cm,"Identification : {}".format(identification_centrale))
        
        Marque_centrale = administratif["marque"]
        c.drawString(13.3*cm,19.7*cm,"Marque : {}".format(Marque_centrale))
        
        n_serie_centrale = administratif["n_serie"]
        c.drawString(13.3*cm,19.2*cm,"N°de serie : {}".format(n_serie_centrale))
        
#        print(administratif["tableau_centrale"])
        tableau_central = [[x[0], x[1], x[3], x[5], x[4].replace("\n", "")] for x in administratif["tableau_centrale"]]
        tableau_central.insert(0, ["Voie", "Emplacement", "U etalonnage", "Date Etalonnage", "Certificat n°"])
#        print(data)
        tableau_sondes_centrale = Table(tableau_central, colWidths=[3.68*cm, 3.68*cm, 3.68*cm, 3.68*cm, 3.68*cm] )
#
#        gen_couleur =(couleur for couleur in self.couleur_dark.values())
        list_style_table = [('ALIGN',(0,0),(-1,-1),'CENTER'),
                            ('BACKGROUND',(0, 0), (-1, 0), colors.lightgrey),
                            ('BACKGROUND',(0, 0), (0, -1), colors.lightgrey),
                            ('TEXTCOLOR',(1,1),(-1,-1),colors.black),
                           ('FONT', (0, 0), (-1, -1), 'Arial', 7 ), 
                           ('VALIGN',(0,0),(-1,-1),'MIDDLE'),
                           ('INNERGRID', (0,0), (-1,-1), 0.25, colors.black),
                           ('BOX', (0,0), (-1,-1), 0.25, colors.black)]
                           
        tableau_sondes_centrale.setStyle(TableStyle(list_style_table))                           
        tableau_sondes_centrale.wrapOn(c, width, height)
        
        
        c.setFont("Arial", 7)
        
        ##Rapport qui decale en fct nbr de sonde sondes si moins il faut decaler:
        
        decalage_cm = (15-len(administratif["tableau_centrale"] )) *0.5
        

        tableau_sondes_centrale.drawOn(c, 1.3*cm, (10.8+decalage_cm)*cm) 
        c.drawInlineImage(self._cube_resultat_15s, 3.1*cm, (-10.6+decalage_cm)*cm, width=15*cm,  preserveAspectRatio=True)    
        
        #placement des valeurs dans le cube_resultat_15s
        gene_voie = (x[0] for x in resultat["tableau_resultats"])
        coordonnees_moyennes_cube= {"CH":(6.5, (9.3+decalage_cm)), "CP":(12.2, (9.3+decalage_cm)), 
                                                      "HPG":(4.9, (7.95+decalage_cm)), "HPD":(14.5, (7.95+decalage_cm)), 
                                                      "HAG":(4.9, (6.9+decalage_cm)), "HAD":(14.5, (6.9+decalage_cm)), 
                                                      "CG":(3.5, 5.5+decalage_cm), "CD":(14.5, 5.9+decalage_cm), 
                                                      "BPG":(4.9, 4.5+decalage_cm), "BPD":(14.5, 4.5+decalage_cm), 
                                                      "BAG":(4.9, 3.15+decalage_cm), "BAD":(14.5, 3.15+decalage_cm),
                                                      "CA":(3.5, 2.1+decalage_cm), "CENTRE":(10, 2.1+decalage_cm),"CB":(14.5, 2.1+decalage_cm)}
        coordonnees_u_cube= {"CH":(8.2, 9.3+decalage_cm), "CP":(14.2, 9.3+decalage_cm), 
                                                      "HPG":(3.4, 7.95+decalage_cm), "HPD":(16.2, 7.95+decalage_cm), 
                                                      "HAG":(3.4, 6.9+decalage_cm), "HAD":(16.2, 6.9+decalage_cm), 
                                                      "CG":(4.8, 5.5+decalage_cm), "CD":(16.1, 5.9+decalage_cm), 
                                                      "BPG":(3.4, 4.5+decalage_cm), "BPD":(16.1, 4.5+decalage_cm), 
                                                      "BAG":(3.4, 3.15+decalage_cm), "BAD":(16.1, 3.15+decalage_cm),
                                                      "CA":(4.8, 2.1+decalage_cm), "CENTRE":(8.3, 2.1+decalage_cm),"CB":(16.1, 2.1+decalage_cm)}                                              
                                                      
        for nom_emplacement in gene_voie:
            if nom_emplacement in coordonnees_moyennes_cube:
                
                moyenne = [x[1] for x in resultat["tableau_resultats"] if x[0] == nom_emplacement][0]
                x_m = coordonnees_moyennes_cube[nom_emplacement][0]
                y_m = coordonnees_moyennes_cube[nom_emplacement][1]
                c.drawString(x_m*cm, y_m*cm,"{}".format(moyenne))
                
                U = [x[11] for x in resultat["tableau_resultats"] if x[0] == nom_emplacement][0]
                x_U = coordonnees_u_cube[nom_emplacement][0]
                y_U = coordonnees_u_cube[nom_emplacement][1]
                c.drawString(x_U*cm, y_U*cm,"+/- {}".format(U))
        
        c.setFont("Arial", 9)
        c.drawString(17.8*cm,0.8*cm,"Page 2 / 3")
        
        #######Page 3 ##############
        c.showPage()
        #n° Cartographie
        c.setFont("Arial", 9)
        c.drawString(1.7*cm,28.4*cm,"RAPPORT D'ESSAI N° {}".format(administratif["num_rapport"]))
        c.setFont("Arial", 8)
        c.drawString(1.7*cm,28*cm,"N°Identification {}".format(administratif["ident_enceinte"]))
        
        #Administration
        c.setFont("Arial-Bold", 10)
        c.drawString(9.8*cm,27*cm,"Résultats")
        c.rect(1.3*cm, 26.9*cm, 18.1*cm, 0.4*cm , stroke=1, fill=0)
        
        c.drawString(1.7*cm,26.2*cm,"Température de l'air de l'enceinte : θ air")
        moyen_air = resultat["temp_air"]
        c.drawString(16.5*cm,26.2*cm,"{}°C".format(moyen_air))
        
        c.drawString(1.7*cm,25.7*cm,"Incertitude sur la température de l'air (k=2) : Uθ air")
        U_air = resultat["U_temp_air"]
        c.drawString(16.5*cm,25.7*cm,"+/- {}°C".format(U_air))
        
        c.drawString(1.7*cm,25.2*cm,"Ecart  consigne /mesure  ∆ co = θ co - θair ")
        ecart_consigne = resultat["ecart_consigne"]                
        if administratif["type_consign"] != "*":
            c.drawString(16.5*cm,25.2*cm,"{}°C".format(ecart_consigne))
        else:
            c.drawString(16.5*cm,25.2*cm,"Na")
            
        c.drawString(1.7*cm,24.7*cm,"Moyenne maximum de la température en régime établi")
        moy_max = resultat["moy_max"]
        c.drawString(16.5*cm,24.7*cm,"{}°C".format(moy_max))
        
        c.drawString(1.7*cm,24.2*cm,"Moyenne minimum de la température en régime établi.")
        moy_min = resultat["moy_min"]
        c.drawString(16.5*cm,24.2*cm,"{}°C".format(moy_min))        
        
        c.drawString(1.7*cm,23.7*cm,"Homogénéité : Hθ ")
        c.setFont("Arial", 7)
        text_ob = c.beginText(1.7*cm,23.4*cm)
        text_ob.textLines("Ecart entre les moyennes maxi et mini augmentées de leur incertitude élargie,\nen régime établi dans l'espace de travail")
        c.drawText(text_ob)
        
        c.setFont("Arial-Bold", 10)
        homogeneite = resultat["homogeneite"]
        c.drawString(16.5*cm,23.7*cm,"{}°C".format(homogeneite))
        
        
       
        c.drawString(1.7*cm,22.6*cm,"Stabilité maximale : SθM")
        c.setFont("Arial", 7)
        text_ob = c.beginText(1.7*cm,22.3*cm)
        text_ob.textLines("Valeur maximale des valeurs de stabilité (val.max-val.min) des capteurs")
        c.drawText(text_ob)
        
        c.setFont("Arial-Bold", 10)
        c.drawString(13.9*cm,22.6*cm,"SθM")
        stab = resultat["stab"]
        c.drawString(16.5*cm,22.6*cm,"{}°C".format(stab))
        
        c.drawString(13.9*cm,22.1*cm,"Capteur:")
        position_stab = resultat["position_stab"]
        c.drawString(16.5*cm,22.1*cm,"{}".format(position_stab))
        
        
        #Conclusion et graphique
        c.setFont("Arial-Bold", 10)
        c.drawString(9.8*cm,21.5*cm,"Conclusions")
        c.rect(1.3*cm, 21.4*cm, 18.1*cm, 0.4*cm , stroke=1, fill=0)        
        
        c.drawImage(ImageReader(resultat["graph_result"]),2.2*cm, 17.3*cm, width=16*cm, height= 4*cm)
        
        #Objet et remarque
        c.setFont("Arial-Bold", 10)
        c.drawString(9.8*cm,16.3*cm,"Objet et Remarques")
        c.rect(1.3*cm, 16.2*cm, 18.1*cm, 0.4*cm , stroke=1, fill=0)
        
        c.setFont("Arial", 10)
        text_ob = c.beginText(1.7*cm,15.7*cm)
        objet_remarques = resultat["objet_remarques"]
        text_ob.textLines(objet_remarques)
        c.drawText(text_ob)
        
        #Conformite capteurs 
        c.setFont("Arial-Bold", 10)
        c.drawString(9.8*cm,13.5*cm,"Conformite par Capteur")
        c.rect(1.3*cm, 13.4*cm, 18.1*cm, 0.4*cm , stroke=1, fill=0)   
            
#        print(resultat["tableau_conformite_par_capteur"])
        tableau_conf_capteur = Table(resultat["tableau_conformite_par_capteur"], colWidths=[4.5*cm, 4.5*cm, 4.5*cm, 4.5*cm])

#        gen_couleur =(couleur for couleur in self.couleur_dark.values())
        list_style_table = [('ALIGN',(0,0),(-1,-1),'CENTER'),
#                            ('BACKGROUND',(0, 0), (-1, 0), colors.lightgrey),
#                            ('BACKGROUND',(0, 0), (0, -1), colors.lightgrey),
                            ('TEXTCOLOR',(1,1),(-1,-1),colors.black),
                           ('FONT', (0, 0), (-1, -1), 'Arial', 7 ), 
                           ('VALIGN',(0,0),(-1,-1),'MIDDLE'),
                           ('INNERGRID', (0,0), (-1,-1), 0.25, colors.black),
                           ('BOX', (0,0), (-1,-1), 0.25, colors.black)]
                           
        tableau_conf_capteur.setStyle(TableStyle(list_style_table))                           
        tableau_conf_capteur.wrapOn(c, width, height)
        
        tableau_conf_capteur.drawOn(c, 1.3*cm, 11*cm)
        
        #Conclusion Génerale
        c.setFont("Arial-Bold", 10)
        c.drawString(9.8*cm,10*cm,"Conclusion Générale")
        c.rect(1.3*cm, 9.9*cm, 18.1*cm, 0.4*cm , stroke=1, fill=0)
        
        c.setFont("Arial", 10)
        text_ob = c.beginText(1.7*cm,9.4*cm)
        objet_remarques = resultat["conclusion_generale"]
        text_ob.textLines(objet_remarques)
        c.drawText(text_ob)
        
         #Conseil
        c.setFont("Arial-Bold", 10)
        c.drawString(9.8*cm,8.4*cm,"Conseil")
        c.rect(1.3*cm, 8.3*cm, 18.1*cm, 0.4*cm , stroke=1, fill=0)
        
        c.setFont("Arial", 10)
        text_ob = c.beginText(1.7*cm,7.8*cm)
        objet_remarques = resultat["conseils"]
        text_ob.textLines(objet_remarques)
        c.drawText(text_ob)
        
        c.setFont("Arial-Bold", 10)
        c.drawString(9*cm,1.5*cm,"FIN DU RAPPORT")
        
        c.setFont("Arial", 9)
        c.drawString(17.8*cm,0.8*cm,"Page 3 / 3")
#        print(resultat["tableau_conformite_par_capteur"])
        
        c.showPage()
        self.annexe(c, donnees)
        
        if donnees["simulation"]["simulation"]:
#            print("coucou")
            c.showPage()
            self.annexe_simulation(c, donnees)
#        try:
        c.save()
        
    
    def annexe(self, c, donnees): 
#        c = canvas.Canvas(self.fichier)
#        print(donnees)
        width, height = A4
        
        c.setFont("Helvetica-Bold", 14)
        if donnees["simulation"]["simulation"]:
            c.drawString(7.5*cm,27.5*cm,"Annexe 1/2")
        else:
            c.drawString(7.5*cm,27.5*cm,"Annexe 1/1")
#        c.rect(7*cm, 27*cm, 7*cm, 1.5*cm , stroke=1, fill=0)
        
        c.setFont("Helvetica", 8)
        c.drawString(7.5*cm,27*cm,"Cartographie N°: {}".format(donnees["administratif"]["num_rapport"]))#donnees["CARTO"]
        c.drawString(7.5*cm,26.5*cm,"Service: {} Enceinte: {}".format(donnees["annexe"]["LIEU"], donnees["annexe"]["ENCEINTE"]))

       
        list_data = [ tuple(zip_longest(donnees["annexe"]["DONNEES"]["Date"].apply(self.format_date_secondes), 
                        donnees["annexe"]["DONNEES"][clef].dropna().astype(float).tolist()))  
                        for clef in donnees["annexe"]["DONNEES"] if clef !="Date" ]
        index_debut = donnees["annexe"]["INDEX_DEBUT"]        
        index_fin = donnees["annexe"]["INDEX_FIN"] + 1 #permet de tenir compte de la derniere valeur c'est une liste
#        print(index_debut)
#        print(donnees["annexe"]["DONNEES"]["Date"])
        date_debut = donnees["annexe"]["DONNEES"]["Date"].iloc[index_debut].strftime("%d-%m-%Y %H:%M:%S") 
        date_fin = donnees["annexe"]["DONNEES"]["Date"].iloc[index_fin-1].strftime("%d-%m-%Y %H:%M:%S")  ###-1 pour afficher la valeur de fin reellement selectionnée
        nbr_mesure = len(donnees["annexe"]["DONNEES"][index_debut:index_fin]["Date"])


        list_data_selec = [ tuple(zip_longest(donnees["annexe"]["DONNEES"][index_debut:index_fin]["Date"].apply(self.format_date_secondes), 
                            donnees["annexe"]["DONNEES"][index_debut:index_fin][clef].dropna().astype(float).tolist()))  
                            for clef in donnees["annexe"]["DONNEES"] if clef !="Date" ]
        

        #Graph total:
        d = Drawing()
        lp = LinePlot()
#        lp.title.text = "Zone totale"
        
        lp.strokeColor = colors.black
        lp.width = 15*cm
        lp.height = 8*cm
        lp.data = list_data
        
        #Graph Selection
        d_select = Drawing()
        lp_select = LinePlot()
        lp_select.strokeColor = colors.black
        lp_select.width = 15*cm
        lp_select.height = 8*cm
        lp_select.data = list_data_selec
        
        
        colors_list = []
        list_sonde = [clef for clef in donnees["annexe"]["DONNEES"] if clef !="Date" ]
        gen_couleur = [couleur for couleur in self.couleur_dark.values()]
        for i in range(len(list_data)):
            couleur = gen_couleur[i]
           
            colors_list.append((couleur, list_sonde[i]))
            lp.lines[i].strokeColor = couleur
            lp_select.lines[i].strokeColor = couleur


        #labelTextFormat
        title = Label()
        title.fontName = "Helvetica-Bold"
        title.fontSize = 14
        title.setText("Periode totale d'observation")
        title.dx = 4*cm
        title.dy = 9*cm
        
        title_graph_select = Label()
        title_graph_select.fontName = "Helvetica-Bold"
        title_graph_select.fontSize = 14
        title_graph_select.setText("Periode Retenue pour la cartographie")
        title_graph_select.dx = 5*cm
        title_graph_select.dy = 9*cm
        
        exploit_graph_select = Label()
#        title_graph_select.fontName = "Helvetica-Bold"
#        title_graph_select.fontSize = 14
        exploit_graph_select.setText( "Nombre de valeurs retenues {} \nPeriode Retenue {} au  {}".format(nbr_mesure, date_debut, date_fin))
        exploit_graph_select.dx = 4*cm
        exploit_graph_select.dy = -3.5*cm
        
        
#         \n Nombre de valeurs retenues {} \n Periode Retenue {} au  {}".format(nbr_mesure, date_debut, date_fin))
        
        
        #Legend
        
        lp_select.xValueAxis.labelTextFormat = self.formatter_axis_x
        lp.xValueAxis.labelTextFormat = self.formatter_axis_x
        
        legend = LineLegend()
        legend.alignment = 'left'
        legend.x = 20
        legend.y = -15
        legend.dxTextSpace = 1
        
        legend.colorNamePairs = colors_list

#        # adding legend
        d_select.add(legend, 'legend')
        d_select.add(title_graph_select)
        d_select.add(exploit_graph_select)
        d_select.add(lp_select)
        renderPDF.draw(d_select, c, 2*cm, 15*cm)
#        print(donnees["RESULTATS"])
        data = donnees["annexe"]["RESULTATS"].iloc[:,[0, 1, 2, 3, 4]].values.tolist()
        data.insert(0, ["Voie", "Moyenne", "Ecart Type", "Minimum", "Maximum"])
#        print(data)
        t = Table(data)
#
#        gen_couleur =(couleur for couleur in self.couleur_dark.values())
        list_style_table = [('ALIGN',(0,0),(-1,-1),'CENTER'),
                            ('BACKGROUND',(0, 0), (-1, 0), colors.lightgrey),
                            ('BACKGROUND',(0, 0), (0, -1), colors.lightgrey),
                            ('TEXTCOLOR',(1,1),(-1,-1),colors.black),
                           ('FONT', (0, 0), (-1, -1), 'Helvetica', 8 ), 
                           ('VALIGN',(0,0),(-1,-1),'MIDDLE'),
                           ('INNERGRID', (0,0), (-1,-1), 0.25, colors.black),
                           ('BOX', (0,0), (-1,-1), 0.25, colors.black)]
                           
        
        
                           
        for ligne in range(1, len(data)):
            couleur = [valeur[0] for valeur in colors_list if valeur[1]==data[ligne][0]][0]
            list_style_table.append(('TEXTCOLOR',(0, ligne),(0, ligne), couleur))

        
        t.setStyle(TableStyle(list_style_table))
                           
        t.wrapOn(c, width, height)
        t.drawOn(c, 1.5*cm, 2*cm)

        c.showPage()
        
        d.add(legend, 'legend')
        d.add(title)
        d.add(lp)
        
        
        
        renderPDF.draw(d, c, 2*cm, 15*cm)
        

#        c.drawString(1*cm,2*cm,"Validation :")
        
#        c.drawString(19*cm,1*cm,"Page 2/2")
        
#        c.save()


    def annexe_simulation(self, c, donnees):
        
#        print(donnees)
        c.setFont("Helvetica-Bold", 14)
        c.drawString(7.5*cm,27.5*cm,"Annexe 2/2")
#        c.rect(7*cm, 27*cm, 7*cm, 1.5*cm , stroke=1, fill=0)
        
        c.setFont("Helvetica", 8)
#        print(donnees["administratif"]["num_rapport"])
        c.drawString(7.5*cm,27*cm,"Cartographie N°: {}".format(donnees["administratif"]["num_rapport"]))#donnees["CARTO"]
        c.drawString(7.5*cm,26.5*cm,"Service: {} Enceinte: {}".format(donnees["annexe"]["LIEU"], donnees["annexe"]["ENCEINTE"]))
        
        c.setFont("Arial-Bold", 10)
        text_ob = c.beginText(2.2*cm,25*cm)
        objet_remarques = "Evolution de la température simulée d'un CGR en fonction de la température de l'air de chaque capteur \n dans l'enceinte (en régime établi):"
        text_ob.textLines(objet_remarques)
        c.drawText(text_ob)
        
        
#        c.setFont("Arial-Bold", 10)
#        c.drawString(2.2*cm,23*cm,"Evolution de la témperature simulée d'un CGR en fonction de la témperature de l'air de chaque capteur dans l'enceinte (en régime établi):")
#        c.rect(1.3*cm, 21.4*cm, 18.1*cm, 0.4*cm , stroke=1, fill=0)        
        
        c.drawImage(ImageReader(donnees["simulation"]["graph_simulation"]),1*cm, 17.5*cm, width=20*cm, height= 7*cm)
        
        c.setFont("Arial-Bold", 10)
        text_ob = c.beginText(2.2*cm,16*cm)
        objet_remarques = "Graphique de conformité par capteur(température simulée d'un CGR):"
        text_ob.textLines(objet_remarques)
        c.drawText(text_ob)
        
        c.drawImage(ImageReader(donnees["simulation"]["graph_simulation_resultat"]),1*cm, 10.5*cm, width=20*cm, height= 5*cm)
        
        c.setFont("Arial-Bold", 10)
        c.drawString(2.2*cm,7.5*cm,"Conclusion")
        
        c.setFont("Arial", 10)
        text_ob = c.beginText(2.2*cm,7*cm)
        objet_conclusion = donnees["simulation"]["conclusion_generale"]
        text_ob.textLines(objet_conclusion)
        c.drawText(text_ob)
        
        
    def format_date_secondes(self, value_timestramp):
        """transforme timestramp de pandas en datetime puis en seconde totale"""
#        print(value_timestramp)
        date = datetime.datetime(value_timestramp.year,value_timestramp.month,value_timestramp.day,
                                             value_timestramp.hour, value_timestramp.minute, value_timestramp.second)
        value_seconde = time.mktime(date.timetuple())
        
        return value_seconde
    
    def formatter_axis_x(self, val):
        """fct pour afficher une date sous axis du graphe 
        prend le total seconde pour enfaire une date en string"""
        text_date = time.strftime("%d-%m-%Y %H:%M:%S", time.localtime(val))
#        print("texte date {}".format(text_date))
        return text_date
