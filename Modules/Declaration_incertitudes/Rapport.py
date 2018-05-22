from reportlab.pdfgen import canvas
from reportlab.platypus import Table,  TableStyle
#from reportlab.lib.pagesizes import letter, inch
from reportlab.lib import colors
from reportlab.lib.pagesizes import A4 
from reportlab.lib.units import cm
from reportlab.graphics.charts.piecharts import Pie
from reportlab.graphics.shapes import Drawing
import numpy as np
from reportlab.graphics import renderPDF


class Rapport():
    
    def __init__(self, administration,  donnees, resultat_u , chemin):
        
#        print(chemin)
        if ".pdf" not in chemin:
            fichier =chemin + ".pdf"
        else:
            fichier = chemin
        c = canvas.Canvas(fichier)
        width, height = A4
        
        c.setFont("Helvetica-Bold", 11)
        c.drawString(7.5*cm,27.5*cm,"Rapport Declaration Incertitudes")
        c.rect(7*cm, 27*cm, 7*cm, 1.5*cm , stroke=1, fill=0)
        
        c.setFont("Helvetica", 8)
        c.drawString(2*cm,26*cm,"Date: " + administration ["DATE"])
        c.drawString(15*cm,26*cm,"Type: " + administration ["TYPE"])
         
        if len(administration["LIST_GENERATEUR"])>=1:
            t = Table(administration["LIST_GENERATEUR"])
            t.setStyle(TableStyle([('ALIGN',(0,0),(-1,-1),'CENTER'),
                            ('BACKGROUND',(0, 0), (-1, 0), colors.lightgrey), 
                           ('TEXTCOLOR',(0,0),(-1,-1),colors.black),
                           ('FONT', (0, 0), (-1, -1), 'Helvetica', 8 ), 
                           ('VALIGN',(0,0),(-1,-1),'MIDDLE'),
                           ('INNERGRID', (0,0), (-1,-1), 0.25, colors.black),
                           ('BOX', (0,0), (-1,-1), 0.25, colors.black),
                           ]))
            
            t.wrapOn(c, width, height)
            t.drawOn(c, 2*cm, 23.8*cm)
            
        if len(administration["LIST_ETALON"])>=1:
            t = Table(administration["LIST_ETALON"])
            t.setStyle(TableStyle([('ALIGN',(0,0),(-1,-1),'CENTER'),
                            ('BACKGROUND',(0, 0), (-1, 0), colors.lightgrey), 
                           ('TEXTCOLOR',(0,0),(-1,-1),colors.black),
                           ('FONT', (0, 0), (-1, -1), 'Helvetica', 8 ), 
                           ('VALIGN',(0,0),(-1,-1),'MIDDLE'),
                           ('INNERGRID', (0,0), (-1,-1), 0.25, colors.black),
                           ('BOX', (0,0), (-1,-1), 0.25, colors.black),
                           ]))
            
            t.wrapOn(c, width, height)
            t.drawOn(c, 12*cm, 23.8*cm)

        donnees.insert(0, ["Sources", "Valeur", "Loi distribution","u", "u²"])
        t= Table(donnees)#,5*[0.5*inch], len(donnees)*[0.2*inch])
        
        t.setStyle(TableStyle([('ALIGN',(0,0),(-1,-1),'CENTER'),
                        ('BACKGROUND',(0, 0), (-1, 0), colors.lightgrey),
                       ('BACKGROUND',(0, 1), (0, -1), colors.lightgrey), 
                       ('TEXTCOLOR',(0,0),(-1,-1),colors.black),
                       ('FONT', (0, 0), (-1, 0), 'Helvetica-Bold', 8 ), 
                       ('FONT', (0, 1), (0, -1), 'Helvetica-Bold', 8 ),
                       ('FONT', (1, 1), (-1, -1), 'Helvetica', 8 ), 
                       ('VALIGN',(0,0),(-1,-1),'MIDDLE'),
                       ('INNERGRID', (0,0), (-1,-1), 0.25, colors.black),
                       ('BOX', (0,0), (-1,-1), 0.25, colors.black),
                       ]))

        
        t.wrapOn(c, width, height)
        t.drawOn(c, 2*cm, 15.3*cm)
        
        donnees_tableau_resultat = []
        donnees_tableau_resultat .append(["Type", "Somme u²", "u", "U (k=2"])
        donnees_tableau_resultat.append(["Incertitude Finale", resultat_u["Somme u²"], resultat_u["u final"],  resultat_u["U final"]])
        donnees_tableau_resultat.append(["Incertitude Déclarée", resultat_u["Somme u² declaree"], resultat_u["u declaree"],  resultat_u["U declaree"]])
        
        t= Table(donnees_tableau_resultat)#,5*[0.5*inch], len(donnees)*[0.2*inch])
        
        t.setStyle(TableStyle([('ALIGN',(0,0),(-1,-1),'CENTER'),
                        ('BACKGROUND',(0, 0), (-1, 0), colors.lightgrey),
                        ('BACKGROUND',(0, 1), (0, -1), colors.lightgrey),
                       ('FONT', (0, 0), (-1, 0), 'Helvetica-Bold', 8 ), 
                       ('FONT', (0, 0), (0, -1), 'Helvetica-Bold', 8 ),
                       ('TEXTCOLOR',(0,0),(-1,-1),colors.black),                       
                       ('TEXTCOLOR',(-1,-1),(-1,-1),colors.red),
                        ('FONT', (-1, -1), (-1, -1), 'Helvetica-Bold', 9 ),
                        ('FONT', (1, 1), (3, 1), 'Helvetica', 8 ),
                        ('FONT', (1, 2), (2, 2), 'Helvetica', 8 ),
                       ('VALIGN',(0,0),(-1,-1),'MIDDLE'),
                       ('INNERGRID', (0,0), (-1,-1), 0.25, colors.black),
                       ('BOX', (0,0), (-1,-1), 0.25, colors.black),
                       ]))
                       
        t.wrapOn(c, width, height)
        t.drawOn(c, 2*cm, 12.8*cm)
                       
                       
                       
        
        text_ob = c.beginText(2*cm,11.8*cm)
        text_ob.textLines("Commentaire: " + administration ["COMMENTAIRE"])
        c.drawText(text_ob)
        
        c.drawString(19*cm,1*cm,"Page 1/1")

#        c.showPage()
        
        
        
        
        data_u = [float(x[3]) for x in donnees[1:]]
        sumdata_u = np.sum(data_u)
        list_data = [int(x/sumdata_u * 100) for x in data_u]
        
        list_label = [x[0] for x in donnees[1:]]
        
        d = Drawing()
        pc = Pie()
        pc.x = 65
        pc.y = 15
        pc.width = 200
        pc.height = 200
        pc.data = list_data
        pc.labels = list_label
        pc.slices.strokeWidth=0

        d.add(pc)
        renderPDF.draw(d, c, 5*cm, 2.2*cm)
        
        
        c.drawString(1*cm,2*cm,"Validation :")
        
#        c.drawString(19*cm,1*cm,"Page 2/2")
        
        c.save()

        
        
        
        
        
        
