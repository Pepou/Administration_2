#import sys
from PyQt4.QtGui import QLineEdit,  QCompleter
from PyQt4.QtCore import Qt , pyqtSignal

from PyQt4.QtCore import * 
from PyQt4.QtGui import * 


class ExtendedLine( QLineEdit ):
    
    tabPressed = pyqtSignal()


    def __init__(self, parent =None):
        super(ExtendedLine, self).__init__(parent)
        
#        self.setFocusPolicy(Qt.StrongFocus)
        self.setFocus()
        
#        
        
    def mise_a_jour_completerList(self, list):
        self.completerList = list
        self.completer = QCompleter(self.completerList, self)
        self.completer.setCompletionMode(QCompleter.PopupCompletion)
        self.completer.setCaseSensitivity(Qt.CaseInsensitive)
        self.setCompleter(self.completer)
        
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
