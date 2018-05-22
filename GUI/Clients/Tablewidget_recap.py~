#from PyQt4 import QtGui, QtCore
from PyQt4.QtCore import  Qt
from PyQt4.QtGui import QMainWindow, QTableWidgetItem, QBrush, QFont, QTableWidget
import sys

class Tablewidget_Homogeneite(QTableWidget):

    def __init__(self, parent=None):
        super(Tablewidget_Homogeneite, self).__init__(parent)
#        print("nb ligne {}".format(self.rowCount()))
        
        for i in range(7):
            self.insertColumn(0)
        for i in range(44):
            self.insertRow(0)
        self.mise_en_forme()
        
    
    def mise_en_forme(self):
        """permet de customiser le tablewidget"""
#        print("copucouc")
#        print(str(self.rowCount()))
        
        list_sommet = [("A", "G"), ("B", "H"), ("E","C"), ("F","D")]
        for i in range(4):            
            coef_multi = i*11
            n_emplacement = i*2
            
            self.setSpan(0+coef_multi, 0, 1, 3)
            item = QTableWidgetItem("Emplacement n°"+str(1+n_emplacement))
#            print(item)
            self.setItem(0 +coef_multi, 0, item)
            self.item(0 +coef_multi, 0).setTextAlignment(Qt.AlignVCenter | Qt.AlignHCenter)
            self.item(0 +coef_multi, 0).setBackground(Qt.yellow)
            self.item(0 +coef_multi, 0).setFlags(Qt.ItemIsSelectable |Qt.ItemIsEnabled )
            
            font = QFont()
            font.setBold(True)
            self.item(0 +coef_multi, 0).setFont(font)
            
            
            item = QTableWidgetItem("Sommet")
            self.setItem(1 +coef_multi, 0, item)
            self.item(1 +coef_multi, 0).setBackground(Qt.gray)
            self.item(1 +coef_multi, 0).setFlags(Qt.ItemIsSelectable |Qt.ItemIsEnabled )

            item = QTableWidgetItem(list_sommet[i][0])
            self.setItem(1 +coef_multi, 1, item)
            self.item(1 +coef_multi, 1).setFlags(Qt.ItemIsSelectable |Qt.ItemIsEnabled )
            self.item(1 +coef_multi, 1).setTextAlignment(Qt.AlignVCenter | Qt.AlignHCenter)
            font = QFont()
            font.setBold(True)
            self.item(1 +coef_multi, 1).setFont(font)
            
            item = QTableWidgetItem(list_sommet[i][1])
            self.setItem(1 +coef_multi, 2, item)
            self.item(1 +coef_multi, 2).setTextAlignment(Qt.AlignVCenter | Qt.AlignHCenter)
            self.item(1 +coef_multi, 2).setFlags(Qt.ItemIsSelectable |Qt.ItemIsEnabled )
            font = QFont()
            font.setBold(True)
            self.item(1 +coef_multi, 2).setFont(font)
            
            
            item = QTableWidgetItem("Sondes")
            self.setItem(2 +coef_multi, 0, item)
            self.item(2 +coef_multi, 0).setBackground(Qt.gray)
            self.item(2 +coef_multi, 0).setFlags(Qt.ItemIsSelectable |Qt.ItemIsEnabled )
            
            item = QTableWidgetItem("Config")
            self.setItem(3 +coef_multi, 0, item)
            self.item(3 +coef_multi, 0).setBackground(Qt.gray)
            self.item(3 +coef_multi, 0).setFlags(Qt.ItemIsSelectable |Qt.ItemIsEnabled )
            
            item = QTableWidgetItem("e1")
            self.setItem(3 +coef_multi, 1, item)
            self.item(3 +coef_multi, 1).setTextAlignment(Qt.AlignVCenter | Qt.AlignHCenter)
            self.item(3 +coef_multi, 1).setFlags(Qt.ItemIsSelectable |Qt.ItemIsEnabled )
            item = QTableWidgetItem("e2")
            self.setItem(3 +coef_multi, 2, item)
            self.item(3 +coef_multi, 2).setTextAlignment(Qt.AlignVCenter | Qt.AlignHCenter)
            self.item(3 +coef_multi, 2).setFlags(Qt.ItemIsSelectable |Qt.ItemIsEnabled )
            
            
            
            item = QTableWidgetItem("Min")
            self.setItem(4 +coef_multi, 0, item)
            self.item(4 +coef_multi, 0).setBackground(Qt.gray)
            self.item(4 +coef_multi, 0).setFlags(Qt.ItemIsSelectable |Qt.ItemIsEnabled )
            
            item = QTableWidgetItem("Max")
            self.setItem(5 +coef_multi, 0, item)
            self.item(5 +coef_multi, 0).setBackground(Qt.gray)
            self.item(5 +coef_multi, 0).setFlags(Qt.ItemIsSelectable |Qt.ItemIsEnabled )
            
            item = QTableWidgetItem("Moyenne")
            self.setItem(6 +coef_multi, 0, item)
            self.item(6 +coef_multi, 0).setBackground(Qt.gray)
            self.item(6 +coef_multi, 0).setFlags(Qt.ItemIsSelectable |Qt.ItemIsEnabled )
            
            item = QTableWidgetItem("Ecart type")
            self.setItem(7 +coef_multi, 0, item)
            self.item(7 +coef_multi, 0).setBackground(Qt.gray)
            self.item(7 +coef_multi, 0).setFlags(Qt.ItemIsSelectable |Qt.ItemIsEnabled )
            
            self.setSpan(8 +coef_multi, 1, 1, 2)
            item = QTableWidgetItem("Delta 1")
            self.setItem(8 +coef_multi, 0, item)
            self.item(8 +coef_multi, 0).setBackground(Qt.gray)
            self.item(8 +coef_multi, 0).setFlags(Qt.ItemIsSelectable |Qt.ItemIsEnabled )
            
            self.setSpan(0 +coef_multi, 3, 9, 1)
            item = QTableWidgetItem("Double pesée")
            brush = QBrush()
            brush.setStyle(Qt.Dense5Pattern)
            font = QFont()
            font.setBold(True)
            self.setItem(0 +coef_multi, 3, item)
            self.item(0 +coef_multi, 3).setTextAlignment(Qt.AlignVCenter | Qt.AlignHCenter)
            self.item(0 +coef_multi, 3).setBackground(brush)
            self.item(0 +coef_multi, 3).setFont(font)
            self.item(0 +coef_multi, 3).setFlags(Qt.ItemIsSelectable |Qt.ItemIsEnabled )
            
            
            self.setSpan(0 +coef_multi, 4, 1, 4)
            
            item = QTableWidgetItem("Emplacement n°"+str(2+n_emplacement))
            self.setItem(0+coef_multi, 4, item)
            self.item(0 +coef_multi, 4).setTextAlignment(Qt.AlignVCenter | Qt.AlignHCenter)
            self.item(0 +coef_multi, 4).setBackground(Qt.yellow)
            font = QFont()
            font.setBold(True)
            self.item(0 +coef_multi, 4).setFont(font)
            self.item(0 +coef_multi, 4).setFlags(Qt.ItemIsSelectable |Qt.ItemIsEnabled )
            
            item = QTableWidgetItem("Sommet")
            self.setItem(1 +coef_multi, 6, item)
            self.item(1 +coef_multi, 6).setTextAlignment(Qt.AlignVCenter | Qt.AlignRight)
            self.item(1 +coef_multi, 6).setBackground(Qt.gray)
            self.item(1 +coef_multi, 6).setFlags(Qt.ItemIsSelectable |Qt.ItemIsEnabled )
            
            
            item = QTableWidgetItem(list_sommet[i][1])
            self.setItem(1 +coef_multi, 4, item)
            self.item(1 +coef_multi, 4).setTextAlignment(Qt.AlignVCenter | Qt.AlignHCenter)
            self.item(1 +coef_multi, 4).setFlags(Qt.ItemIsSelectable |Qt.ItemIsEnabled )
            font = QFont()
            font.setBold(True)
            self.item(1 +coef_multi, 4).setFont(font)
            
            item = QTableWidgetItem(list_sommet[i][0])
            self.setItem(1 +coef_multi, 5, item)
            self.item(1 +coef_multi, 5).setTextAlignment(Qt.AlignVCenter | Qt.AlignHCenter)
            self.item(1 +coef_multi, 5).setFlags(Qt.ItemIsSelectable |Qt.ItemIsEnabled )
            font = QFont()
            font.setBold(True)
            self.item(1 +coef_multi, 5).setFont(font)
            
            item = QTableWidgetItem("Sondes")
            self.setItem(2 +coef_multi, 6, item)
            self.item(2 +coef_multi, 6).setTextAlignment(Qt.AlignVCenter | Qt.AlignRight)
            self.item(2 +coef_multi, 6).setBackground(Qt.gray)
            self.item(2 +coef_multi, 6).setFlags(Qt.ItemIsSelectable |Qt.ItemIsEnabled )
            
            item = QTableWidgetItem("Config")
            self.setItem(3 +coef_multi, 6, item)
            self.item(3 +coef_multi, 6).setTextAlignment(Qt.AlignVCenter | Qt.AlignRight)
            self.item(3 +coef_multi, 6).setBackground(Qt.gray)
            self.item(3 +coef_multi, 6).setFlags(Qt.ItemIsSelectable |Qt.ItemIsEnabled )
            
            item = QTableWidgetItem("e4")
            self.setItem(3 +coef_multi, 4, item)
            self.item(3 +coef_multi, 4).setTextAlignment(Qt.AlignVCenter | Qt.AlignHCenter)
            self.item(3 +coef_multi, 4).setFlags(Qt.ItemIsSelectable |Qt.ItemIsEnabled )
            item = QTableWidgetItem("e3")
            self.setItem(3 +coef_multi, 5, item)
            self.item(3 +coef_multi, 5).setTextAlignment(Qt.AlignVCenter | Qt.AlignHCenter)
            self.item(3 +coef_multi, 5).setFlags(Qt.ItemIsSelectable |Qt.ItemIsEnabled )
            
            item = QTableWidgetItem("Min")
            self.setItem(4 +coef_multi, 6, item)
            self.item(4 +coef_multi, 6).setTextAlignment(Qt.AlignVCenter | Qt.AlignRight)
            self.item(4 +coef_multi, 6).setBackground(Qt.gray)
            self.item(4 +coef_multi, 6).setFlags(Qt.ItemIsSelectable |Qt.ItemIsEnabled )
            
            item = QTableWidgetItem("Max")
            self.setItem(5 +coef_multi, 6, item)
            self.item(5 +coef_multi, 6).setTextAlignment(Qt.AlignVCenter | Qt.AlignRight)
            self.item(5 +coef_multi, 6).setBackground(Qt.gray)
            self.item(5 +coef_multi, 6).setFlags(Qt.ItemIsSelectable |Qt.ItemIsEnabled )
            
            item = QTableWidgetItem("Moyenne")
            self.setItem(6 +coef_multi, 6, item)
            self.item(6 +coef_multi, 6).setTextAlignment(Qt.AlignVCenter | Qt.AlignRight)
            self.item(6 +coef_multi, 6).setBackground(Qt.gray)
            self.item(6 +coef_multi, 6).setFlags(Qt.ItemIsSelectable |Qt.ItemIsEnabled )
            
            item = QTableWidgetItem("Ecart type")
            self.setItem(7 +coef_multi, 6, item)
            self.item(7 +coef_multi, 6).setTextAlignment(Qt.AlignVCenter | Qt.AlignRight)
            self.item(7 +coef_multi, 6).setBackground(Qt.gray)
            self.item(7 +coef_multi, 6).setFlags(Qt.ItemIsSelectable |Qt.ItemIsEnabled )
            
            self.setSpan(8 +coef_multi, 4, 1, 2)
            item = QTableWidgetItem("Delta 2")
            self.setItem(8 +coef_multi, 6, item)
            self.item(8 +coef_multi, 6).setTextAlignment(Qt.AlignVCenter | Qt.AlignRight)
            self.item(8 +coef_multi, 6).setBackground(Qt.gray)
            self.item(8 +coef_multi, 6).setFlags(Qt.ItemIsSelectable |Qt.ItemIsEnabled )
            
            #"ε =[(e2-e1)+(e4-e3) ]/ 2"
            self.setSpan(9 +coef_multi, 1, 1, 5)
            item = QTableWidgetItem("")
            self.setItem(9 +coef_multi, 1, item)            
            self.item(9 +coef_multi, 1).setBackground(Qt.gray)
#            self.tableWidget_hom.item(9 +coef_multi, 1).setFlags(Qt.ItemIsSelectable |Qt.ItemIsEnabled )
            
            item = QTableWidgetItem("ε =[(e2-e1)+(e4-e3) ]/ 2")
            self.setItem(9 +coef_multi, 0, item)
            self.item(9 +coef_multi, 0).setBackground(Qt.gray)
            self.item(9 +coef_multi, 0).setFlags(Qt.ItemIsSelectable |Qt.ItemIsEnabled )
            
            item = QTableWidgetItem("ε =[(e2-e1)+(e4-e3) ]/ 2")
            self.setItem(9 +coef_multi, 6, item)
            self.item(9 +coef_multi, 6).setTextAlignment(Qt.AlignVCenter | Qt.AlignRight)
            self.item(9 +coef_multi, 6).setBackground(Qt.gray)
            self.item(9 +coef_multi, 6).setFlags(Qt.ItemIsSelectable |Qt.ItemIsEnabled )
            
            #"ε+Uε"
            self.setSpan(10 +coef_multi, 1, 1, 5)
            item = QTableWidgetItem("")
            self.setItem(10 +coef_multi, 1, item)
            self.item(10 +coef_multi, 1).setBackground(Qt.gray)
#            self.tableWidget_hom.item(10 +coef_multi, 1).setFlags(Qt.ItemIsSelectable |Qt.ItemIsEnabled )
            
            item = QTableWidgetItem("ε+Uε")
            self.setItem(10 +coef_multi, 0, item)
            self.item(10 +coef_multi, 0).setBackground(Qt.gray)
            self.item(10 +coef_multi, 0).setFlags(Qt.ItemIsSelectable |Qt.ItemIsEnabled )
            
            item = QTableWidgetItem("ε+Uε")
            self.setItem(10 +coef_multi, 6, item)
            self.item(10 +coef_multi, 6).setTextAlignment(Qt.AlignVCenter | Qt.AlignRight)
            self.item(10 +coef_multi, 6).setBackground(Qt.gray)
            self.item(10 +coef_multi, 6).setFlags(Qt.ItemIsSelectable |Qt.ItemIsEnabled )
        
    def nettoyage(self):
#       self.clear()
       colonne = [1, 2, 4, 5]
       ligne =[4, 5, 6, 7, 15, 16, 17, 18, 26, 27, 28, 29, 37, 38, 39, 40] #[x for x in range(4, 7, 8)]
       for c in colonne:
           for l in ligne:
               item = QTableWidgetItem("0")
               self.setItem(l, c, item)
#       self.mise_en_forme()
       

#            self.cellWidget(i, 1).setChecked(False)
