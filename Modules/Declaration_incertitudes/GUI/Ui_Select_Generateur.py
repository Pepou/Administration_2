# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'C:\Developpement Informatique\Python\Declaration incertitudes\0.1\GUI\Select_Generateur.ui'
#
# Created by: PyQt4 UI code generator 4.11.4
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui

try:
    _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
    def _fromUtf8(s):
        return s

try:
    _encoding = QtGui.QApplication.UnicodeUTF8
    def _translate(context, text, disambig):
        return QtGui.QApplication.translate(context, text, disambig, _encoding)
except AttributeError:
    def _translate(context, text, disambig):
        return QtGui.QApplication.translate(context, text, disambig)

class Ui_Select_Generateurs(object):
    def setupUi(self, Select_Generateurs):
        Select_Generateurs.setObjectName(_fromUtf8("Select_Generateurs"))
        Select_Generateurs.resize(400, 300)
        Select_Generateurs.setSizeGripEnabled(True)
        self.verticalLayout = QtGui.QVBoxLayout(Select_Generateurs)
        self.verticalLayout.setObjectName(_fromUtf8("verticalLayout"))
        self.tableWidget = QtGui.QTableWidget(Select_Generateurs)
        self.tableWidget.setObjectName(_fromUtf8("tableWidget"))
        self.tableWidget.setColumnCount(2)
        self.tableWidget.setRowCount(0)
        item = QtGui.QTableWidgetItem()
        self.tableWidget.setHorizontalHeaderItem(0, item)
        item = QtGui.QTableWidgetItem()
        self.tableWidget.setHorizontalHeaderItem(1, item)
        self.verticalLayout.addWidget(self.tableWidget)
        self.hboxlayout = QtGui.QHBoxLayout()
        self.hboxlayout.setMargin(0)
        self.hboxlayout.setSpacing(6)
        self.hboxlayout.setObjectName(_fromUtf8("hboxlayout"))
        spacerItem = QtGui.QSpacerItem(131, 31, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.hboxlayout.addItem(spacerItem)
        self.okButton = QtGui.QPushButton(Select_Generateurs)
        self.okButton.setObjectName(_fromUtf8("okButton"))
        self.hboxlayout.addWidget(self.okButton)
        self.cancelButton = QtGui.QPushButton(Select_Generateurs)
        self.cancelButton.setObjectName(_fromUtf8("cancelButton"))
        self.hboxlayout.addWidget(self.cancelButton)
        self.verticalLayout.addLayout(self.hboxlayout)

        self.retranslateUi(Select_Generateurs)
        QtCore.QObject.connect(self.okButton, QtCore.SIGNAL(_fromUtf8("clicked()")), Select_Generateurs.accept)
        QtCore.QObject.connect(self.cancelButton, QtCore.SIGNAL(_fromUtf8("clicked()")), Select_Generateurs.reject)
        QtCore.QMetaObject.connectSlotsByName(Select_Generateurs)

    def retranslateUi(self, Select_Generateurs):
        Select_Generateurs.setWindowTitle(_translate("Select_Generateurs", "Selection des Generateurs", None))
        item = self.tableWidget.horizontalHeaderItem(0)
        item.setText(_translate("Select_Generateurs", "Nom", None))
        item = self.tableWidget.horizontalHeaderItem(1)
        item.setText(_translate("Select_Generateurs", "Selection", None))
        self.okButton.setText(_translate("Select_Generateurs", "&OK", None))
        self.cancelButton.setText(_translate("Select_Generateurs", "&Cancel", None))


if __name__ == "__main__":
    import sys
    app = QtGui.QApplication(sys.argv)
    Select_Generateurs = QtGui.QDialog()
    ui = Ui_Select_Generateurs()
    ui.setupUi(Select_Generateurs)
    Select_Generateurs.show()
    sys.exit(app.exec_())

