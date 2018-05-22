from PyQt4.QtCore import  Qt, QAbstractTableModel
from PyQt4.QtGui import  QTableView 
#import sys
#import pandas as pd
class Tableview_resultats(QTableView):
    
    def __init__(self, parent=None):
        super(Tableview_resultats, self).__init__(parent)
        self.nbr_ligne =0
        
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
        model = PandasModel(self.donnees) 
        self.setModel(model)
        self.resizeColumnsToContents()
    
        self.nbr_ligne = model.rowCount() 
    
    def copySelection(self):
        """Fonction qui copie les donnees presente dans tablewidget """
        selection = self.selectedIndexes()

        if selection:              
            rows = list(set(index.row() for index in selection))
            columns = list(set(index.column() for index in selection))            
            data_export = self.donnees.iloc[rows, columns]            
            data_export.to_clipboard(excel =True)

    def rowCount(self):
        """fct qui renvoie le nbr de ligne apres la fct remplir"""        
        return self.nbr_ligne
    
    def return_row(self, row):
        """return l'index de la pandasdatafram correspondant à la row"""
#        print(self.donnees.iloc[row])
        return self.donnees.iloc[row]
        
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
