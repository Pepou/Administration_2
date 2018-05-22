# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'Y:\Logiciels\Logiciels_techniques_labo\0_ A valider tester\Declaration incertitudes\0.1\GUI\Select_Caracterisation.ui'
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

class Ui_Select_Caracterisation(object):
    def setupUi(self, Select_Caracterisation):
        Select_Caracterisation.setObjectName(_fromUtf8("Select_Caracterisation"))
        Select_Caracterisation.resize(474, 300)
        Select_Caracterisation.setSizeGripEnabled(True)
        self.verticalLayout = QtGui.QVBoxLayout(Select_Caracterisation)
        self.verticalLayout.setObjectName(_fromUtf8("verticalLayout"))
        self.tableWidget = QtGui.QTableWidget(Select_Caracterisation)
        self.tableWidget.setAlternatingRowColors(True)
        self.tableWidget.setObjectName(_fromUtf8("tableWidget"))
        self.tableWidget.setColumnCount(5)
        self.tableWidget.setRowCount(0)
        item = QtGui.QTableWidgetItem()
        self.tableWidget.setHorizontalHeaderItem(0, item)
        item = QtGui.QTableWidgetItem()
        self.tableWidget.setHorizontalHeaderItem(1, item)
        item = QtGui.QTableWidgetItem()
        self.tableWidget.setHorizontalHeaderItem(2, item)
        item = QtGui.QTableWidgetItem()
        self.tableWidget.setHorizontalHeaderItem(3, item)
        item = QtGui.QTableWidgetItem()
        self.tableWidget.setHorizontalHeaderItem(4, item)
        self.tableWidget.verticalHeader().setSortIndicatorShown(False)
        self.verticalLayout.addWidget(self.tableWidget)
        self.hboxlayout = QtGui.QHBoxLayout()
        self.hboxlayout.setMargin(0)
        self.hboxlayout.setSpacing(6)
        self.hboxlayout.setObjectName(_fromUtf8("hboxlayout"))
        spacerItem = QtGui.QSpacerItem(131, 31, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.hboxlayout.addItem(spacerItem)
        self.okButton = QtGui.QPushButton(Select_Caracterisation)
        self.okButton.setObjectName(_fromUtf8("okButton"))
        self.hboxlayout.addWidget(self.okButton)
        self.cancelButton = QtGui.QPushButton(Select_Caracterisation)
        self.cancelButton.setObjectName(_fromUtf8("cancelButton"))
        self.hboxlayout.addWidget(self.cancelButton)
        self.verticalLayout.addLayout(self.hboxlayout)

        self.retranslateUi(Select_Caracterisation)
        QtCore.QObject.connect(self.okButton, QtCore.SIGNAL(_fromUtf8("clicked()")), Select_Caracterisation.accept)
        QtCore.QObject.connect(self.cancelButton, QtCore.SIGNAL(_fromUtf8("clicked()")), Select_Caracterisation.reject)
        QtCore.QMetaObject.connectSlotsByName(Select_Caracterisation)

    def retranslateUi(self, Select_Caracterisation):
        Select_Caracterisation.setWindowTitle(_translate("Select_Caracterisation", "Selection des caracterisations", None))
        self.tableWidget.setSortingEnabled(True)
        item = self.tableWidget.horizontalHeaderItem(0)
        item.setText(_translate("Select_Caracterisation", "Date", None))
        item = self.tableWidget.horizontalHeaderItem(1)
        item.setText(_translate("Select_Caracterisation", "ID Caracterisation", None))
        item = self.tableWidget.horizontalHeaderItem(2)
        item.setText(_translate("Select_Caracterisation", "Nom generateur", None))
        item = self.tableWidget.horizontalHeaderItem(3)
        item.setText(_translate("Select_Caracterisation", "u generateur", None))
        item = self.tableWidget.horizontalHeaderItem(4)
        item.setText(_translate("Select_Caracterisation", "Selection", None))
        self.okButton.setText(_translate("Select_Caracterisation", "&OK", None))
        self.cancelButton.setText(_translate("Select_Caracterisation", "&Cancel", None))


if __name__ == "__main__":
    import sys
    app = QtGui.QApplication(sys.argv)
    Select_Caracterisation = QtGui.QDialog()
    ui = Ui_Select_Caracterisation()
    ui.setupUi(Select_Caracterisation)
    Select_Caracterisation.show()
    sys.exit(app.exec_())

