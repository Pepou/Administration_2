import sys
from PyQt4.QtGui import QComboBox, QApplication, QCompleter, QSortFilterProxyModel, QStandardItemModel, QStandardItem
from PyQt4.QtCore import Qt

from PyQt4.QtCore import * 
from PyQt4.QtGui import * 


class ExtendedCombo( QComboBox ):
    def __init__( self,  parent = None):
        super( ExtendedCombo, self ).__init__( parent )

        self.setFocusPolicy( Qt.StrongFocus )
        self.setEditable( True )

        self.setEditable( True )
        self.completer = QCompleter( self )

        # always show all completions
        self.completer.setCompletionMode( QCompleter.UnfilteredPopupCompletion )
        self.pFilterModel = QSortFilterProxyModel( self )
        self.pFilterModel.setFilterCaseSensitivity( Qt.CaseInsensitive )



        self.completer.setPopup( self.view() )


        self.setCompleter( self.completer )


        self.lineEdit().textEdited.connect( self.pFilterModel.setFilterFixedString )
        self.completer.activated.connect(self.setTextIfCompleterIsClicked)

    def setModel( self, model ):
        super(ExtendedCombo, self).setModel( model )
        self.pFilterModel.setSourceModel( model )
        self.completer.setModel(self.pFilterModel)

    def setModelColumn( self, column ):
        self.completer.setCompletionColumn( column )
        self.pFilterModel.setFilterKeyColumn( column )
        super(ExtendedCombo, self).setModelColumn( column )


    def view( self ):
        return self.completer.popup()

    def index( self ):
        return self.currentIndex()

    def setTextIfCompleterIsClicked(self, text):

      if text:
        index = self.findText(text)
        self.setCurrentIndex(index)
#        print(str(index))

    def event(self, event):
        if (event.type()==QEvent.KeyPress) and (event.key()==Qt.Key_Tab):
            self.emit(SIGNAL("tabPressed"))

            return True
        return QComboBox.event(self, event)
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
