#import sys
from PyQt4.QtGui import QLineEdit,  QCompleter, QStandardItemModel, QStandardItem, QSortFilterProxyModel, QStringListModel
from PyQt4.QtCore import Qt , pyqtSignal

from PyQt4.QtCore import * 
from PyQt4.QtGui import * 


class ExtendedLine( QLineEdit ):
    
    tabPressed = pyqtSignal()


    def __init__(self, parent =None):
        super(ExtendedLine, self).__init__(parent)
        
#        self.setFocusPolicy(Qt.StrongFocus)
        self.setFocus()
        
        self.completer = QCompleter()
        self.setCompleter(self.completer)
        self.completer.setCompletionMode(QCompleter.UnfilteredPopupCompletion)
        self.completer.setCaseSensitivity(Qt.CaseInsensitive)
        
    def mise_a_jour_completerList(self, list):
        self.completerList = list
        self.completer = QCompleter(self.completerList, self)
        self.completer.setCompletionMode(QCompleter.PopupCompletion)
        self.completer.setCaseSensitivity(Qt.CaseInsensitive)
        self.setCompleter(self.completer)
        
    
    def completer_list(self, list_enceinte):        
        """permet de remplir le comlpeter du qline avec une liste"""
#        print("tu y es")
        model = QStringListModel()
        self.completer.setModel(model)
        self.get_data(model, list_enceinte)
        
    def get_data(self, model, list_enceinte):
        """met a disposition du model la liste"""
        model.setStringList(list_enceinte)
    
    def nettoyage_completer(self):
        self.completer.clear()
#        # installe le model à partir de la liste fournie datas
#        model = QStandardItemModel()
#        for i, word in enumerate(list):
#            item = QStandardItem(word)
#            model.setItem(i, 0, item)
# 
#        # installe le QSortFilterProxyModel qui s'insère entre le QCompleter et le model
#        self.proxymodel = QSortFilterProxyModel(self)
#        self.proxymodel.setFilterCaseSensitivity(Qt.CaseInsensitive)
#        self.proxymodel.setSourceModel(model)
#        self.completer.setModel(self.proxymodel)
# 
#        # chaque changement de texte déclenchera la filtration du model
#        self.textEdited.connect(self.proxymodel.setFilterFixedString)
#        
#        
        
        
        
#        self.completer.activated.connect(self.test)
#        self.completer.highlighted[QModelIndex].connect(self.test)
        
    def event(self, event):
#        print(event.obj())
        if (event.type()==QEvent.KeyPress) and (event.key()==Qt.Key_Tab):
            self.tabPressed.emit()

        return QLineEdit.event(self, event)
    
    def focusOutEvent(self, event):
#        print (event.reason())
        if event.reason() == Qt.TabFocusReason:
            self.setFocus()
    
    
#    def test(self, index):
#        print("coucou enter")
#        self.clear()
#        self.setText("")
