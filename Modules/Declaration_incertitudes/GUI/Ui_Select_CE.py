# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'Y:\Logiciels\Logiciels_techniques_labo\0_ A valider tester\Declaration incertitudes\0.1\GUI\Select_CE.ui'
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

class Ui_Select_CE(object):
    def setupUi(self, Select_CE):
        Select_CE.setObjectName(_fromUtf8("Select_CE"))
        Select_CE.resize(528, 300)
        Select_CE.setSizeGripEnabled(True)
        self.verticalLayout = QtGui.QVBoxLayout(Select_CE)
        self.verticalLayout.setObjectName(_fromUtf8("verticalLayout"))
        self.tableWidget = QtGui.QTableWidget(Select_CE)
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
        self.verticalLayout.addWidget(self.tableWidget)
        self.hboxlayout = QtGui.QHBoxLayout()
        self.hboxlayout.setMargin(0)
        self.hboxlayout.setSpacing(6)
        self.hboxlayout.setObjectName(_fromUtf8("hboxlayout"))
        spacerItem = QtGui.QSpacerItem(131, 31, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.hboxlayout.addItem(spacerItem)
        self.okButton = QtGui.QPushButton(Select_CE)
        self.okButton.setObjectName(_fromUtf8("okButton"))
        self.hboxlayout.addWidget(self.okButton)
        self.cancelButton = QtGui.QPushButton(Select_CE)
        self.cancelButton.setObjectName(_fromUtf8("cancelButton"))
        self.hboxlayout.addWidget(self.cancelButton)
        self.verticalLayout.addLayout(self.hboxlayout)

        self.retranslateUi(Select_CE)
        QtCore.QObject.connect(self.okButton, QtCore.SIGNAL(_fromUtf8("clicked()")), Select_CE.accept)
        QtCore.QObject.connect(self.cancelButton, QtCore.SIGNAL(_fromUtf8("clicked()")), Select_CE.reject)
        QtCore.QMetaObject.connectSlotsByName(Select_CE)

    def retranslateUi(self, Select_CE):
        Select_CE.setWindowTitle(_translate("Select_CE", "Selection des CE", None))
        self.tableWidget.setSortingEnabled(True)
        item = self.tableWidget.horizontalHeaderItem(0)
        item.setText(_translate("Select_CE", "Etalon", None))
        item = self.tableWidget.horizontalHeaderItem(1)
        item.setText(_translate("Select_CE", "Date", None))
        item = self.tableWidget.horizontalHeaderItem(2)
        item.setText(_translate("Select_CE", "N°CE", None))
        item = self.tableWidget.horizontalHeaderItem(3)
        item.setText(_translate("Select_CE", "Residu max", None))
        item = self.tableWidget.horizontalHeaderItem(4)
        item.setText(_translate("Select_CE", "Selection", None))
        self.okButton.setText(_translate("Select_CE", "&OK", None))
        self.cancelButton.setText(_translate("Select_CE", "&Cancel", None))


if __name__ == "__main__":
    import sys
    app = QtGui.QApplication(sys.argv)
    Select_CE = QtGui.QDialog()
    ui = Ui_Select_CE()
    ui.setupUi(Select_CE)
    Select_CE.show()
    sys.exit(app.exec_())

