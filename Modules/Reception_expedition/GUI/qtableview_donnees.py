from PyQt4.QtCore import  Qt, QAbstractTableModel, pyqtSignal
from PyQt4.QtGui import  QTableView , QMessageBox
#import sys
#import pandas as pd
class Tableview_donnees(QTableView):
    
    supprimerLigne = pyqtSignal(int)
    
    def __init__(self, parent=None):
        super(Tableview_donnees, self).__init__(parent)
#        print("je demarre")
#        self.installEventFilter(self)
#        self.installEventFilter(self)
#
#
#    def eventFilter(self, tableView, event):
#        print(f" coucou suis dans le menu princiapal {event}")
#    
    
    def keyPressEvent(self, event):
        """gestion du copier coller dans le tableau homogeneite"""
        print("coucou")
        items_tableView = self.selectedIndexes()
        ligne = sorted(set(index.row() for index in items_tableView))[0]

        print(ligne)
#        clavier = event.text()

        
        if event.key()== 67 and items_tableView !=None:
            self.copySelection()
#                
        elif event.key()== Qt.Key_Delete or event.key()== Qt.Key_Backspace:
            reponse = QMessageBox.question(self, 
                    self.trUtf8("Attention"), 
                    self.trUtf8("Voulez vous supprimer ces lignes"), 
                    QMessageBox.Yes, QMessageBox.No)
            
            if reponse == QMessageBox.Yes :
                id = self.donnees["ID_INTERVENTION"][ligne]
                self.supprimerLigne.emit(int(id))

        
            
            
            
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
    
#    def eventFilter(self, event):
#        print(event)

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
