from PyQt4.QtCore import  Qt, QAbstractTableModel, QModelIndex
from PyQt4.QtGui import  QTableView 
#import sys
#import pandas as pd
class Tableview_donnees_fichier(QTableView):
    
    def __init__(self, parent=None):
        super(Tableview_donnees_fichier, self).__init__(parent)
        
        
    def keyPressEvent(self, event):
        """gestion du copier coller dans le tableau homogeneite"""
       
        items_tableView = self.selectedIndexes()

        clavier = event.key()

        if items_tableView !=None:
            if clavier == 67 :
                self.copySelection()
                

    def remplir(self, donnees):
        """fct pour remplir le tableview attention les donnees sont des dataframes pandas"""

        
        self.donnees = donnees
        self.model = PandasModel(self.donnees) 
        self.setModel(self.model)
        self.resizeColumnsToContents()    
        
    def copySelection(self):
        """Fonction qui copie les donnees presente dans tablewidget """
        selection = self.selectedIndexes()

        if selection:              
            rows = list(set(index.row() for index in selection))
            columns = list(set(index.column() for index in selection))            
            data_export = self.donnees.iloc[rows, columns]            
            data_export.to_clipboard(excel =True)
    
#    def clear(self):
#        """efface"""
#        try: 
#            print(self.model.rowCount())
#            print("tu essaies de m'evacer")
#            
#            
#    #            print(a)
#            a = self.model.removeRows(0,self.model.rowCount())
#            print("tu as reussi hahaahah")
#            print(a)
#        except AttributeError:
#           pass
##        self.model.efface()
##    def horizon_header(self, list_nom):
##        "permet de rajouter des header au model à faire aavant de remplir"
##        self.model.setHorizontalHeaderLabels(list_nom)

class PandasModel(QAbstractTableModel):
    """
    Class to populate a table view with a pandas dataframe
    """
    def __init__(self, data, parent=None):
        QAbstractTableModel.__init__(self, parent)
        self._data = data

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
        if orientation == Qt.Horizontal and role == Qt.DisplayRole:
            return self._data.columns[col]
        return None
        
#    def removeRows(self, position, rows=1, index=QModelIndex()):
##        print "\n\t\t ...removeRows() Starting position: '%s'"%position, 'with the total rows to be deleted: ', rows
#        self.beginRemoveRows(QModelIndex(), position, position + rows - 1)       
#        self.items = self.items[:position] + self.items[position + rows:]
#        self.endRemoveRows()
#
#        return True
