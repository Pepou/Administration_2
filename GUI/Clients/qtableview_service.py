from PyQt4.QtCore import  Qt, QAbstractTableModel, pyqtSignal# QVariant
from PyQt4.QtGui import  QTableView 
#import sys
#import pandas as pd
class Tableview_donnees_fichier(QTableView):
    
    signalSelect_service = pyqtSignal(int)
    
    def __init__(self, parent=None):
        super(Tableview_donnees_fichier, self).__init__(parent)
        
        
    def mouseDoubleClickEvent(self, event):
        """gestion du copier coller dans le tableau homogeneite"""
        
#        print(event)       
        if event.button() == Qt.LeftButton:
            selection = self.selectedIndexes()
            row = selection[0].row() 
#            print(row)
            self.signalSelect_service.emit(row)

    def keyPressEvent(self, event):
        """gestion du copier coller dans le tableau homogeneite"""
       
        items_tableView = self.selectedIndexes()

        clavier = event.key()

        if clavier == Qt.Key_Delete or clavier == Qt.Key_Backspace:
            ligne_select = self.currentRow()            
            if ligne_select != -1 :
                self.removeRow(ligne_select)        
        
        elif clavier == 67 and items_tableView !=None:            
            self.copySelection()
                

    def remplir(self, donnees):
        """fct pour remplir le tableview attention les donnees sont des dataframes pandas"""

        self.donnees = donnees
        model = PandasModel(self.donnees) 
        self.setModel(model)
#        self.resizeColumnsToContents()    
    
    def copySelection(self):
        """Fonction qui copie les donnees presente dans tablewidget """
        selection = self.selectedIndexes()

        if selection:              
            rows = list(set(index.row() for index in selection))
            columns = list(set(index.column() for index in selection))            
            data_export = self.donnees.iloc[rows, columns]            
            data_export.to_clipboard(excel =True)


class PandasModel(QAbstractTableModel):
    """
    Class to populate a table view with a pandas dataframe
    """
    def __init__(self, data, parent=None):
        QAbstractTableModel.__init__(self, parent)
        self._data = data
#        self.headerDate = [x for x in data.columns]
    def rowCount(self, parent=None):
        return self._data.shape[0]

    def columnCount(self, parent=None):
        return self._data.shape[1]

    def data(self, index, role=Qt.DisplayRole):
#        print("coucou {}".format((self._data.iloc[index.row(), index.column()])))
        
        if index.isValid():
            if role == Qt.DisplayRole:
                
                return str(self._data.iloc[index.row(), index.column()])
        return None

    def headerData(self, col, orientation, role):
#        print(col)
        if orientation == Qt.Horizontal and role == Qt.DisplayRole:
#            print(self.headerDate[col])
#            return self.headerDate[col]
            return str(self._data.columns[col])
        return None
        
        
#    def setHeaderDate(self):
