# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'C:\Travail\EFS\Travail accreditation\SQ\Developpement Informatique\Reception_Expedition\Build\V0.3\BondeReception\GUI\BonReception.ui'
#
# Created: Wed Nov  4 15:42:25 2015
#      by: PyQt4 UI code generator 4.11.3
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

class Ui_Bon_Reception(object):
    def setupUi(self, Bon_Reception):
        Bon_Reception.setObjectName(_fromUtf8("Bon_Reception"))
        Bon_Reception.resize(800, 667)
        self.centralWidget = QtGui.QWidget(Bon_Reception)
        self.centralWidget.setObjectName(_fromUtf8("centralWidget"))
        self.verticalLayout = QtGui.QVBoxLayout(self.centralWidget)
        self.verticalLayout.setObjectName(_fromUtf8("verticalLayout"))
        self.groupBox = QtGui.QGroupBox(self.centralWidget)
        self.groupBox.setObjectName(_fromUtf8("groupBox"))
        self.horizontalLayout_2 = QtGui.QHBoxLayout(self.groupBox)
        self.horizontalLayout_2.setObjectName(_fromUtf8("horizontalLayout_2"))
        self.horizontalLayout = QtGui.QHBoxLayout()
        self.horizontalLayout.setObjectName(_fromUtf8("horizontalLayout"))
        self.radioButton = QtGui.QRadioButton(self.groupBox)
        self.radioButton.setChecked(True)
        self.radioButton.setObjectName(_fromUtf8("radioButton"))
        self.horizontalLayout.addWidget(self.radioButton)
        self.radioButton_2 = QtGui.QRadioButton(self.groupBox)
        self.radioButton_2.setObjectName(_fromUtf8("radioButton_2"))
        self.horizontalLayout.addWidget(self.radioButton_2)
        self.horizontalLayout_2.addLayout(self.horizontalLayout)
        self.verticalLayout.addWidget(self.groupBox)
        self.comboBox_dates = ExtendedCombo(self.centralWidget)
        self.comboBox_dates.setEnabled(True)
        self.comboBox_dates.setEditable(True)
        self.comboBox_dates.setObjectName(_fromUtf8("comboBox_dates"))
        self.verticalLayout.addWidget(self.comboBox_dates)
        self.tableWidget = QtGui.QTableWidget(self.centralWidget)
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
        self.pushButton_export = QtGui.QPushButton(self.centralWidget)
        self.pushButton_export.setObjectName(_fromUtf8("pushButton_export"))
        self.verticalLayout.addWidget(self.pushButton_export)
        Bon_Reception.setCentralWidget(self.centralWidget)

        self.retranslateUi(Bon_Reception)
        QtCore.QObject.connect(self.radioButton, QtCore.SIGNAL(_fromUtf8("clicked()")), self.comboBox_dates.hide)
        QtCore.QObject.connect(self.radioButton_2, QtCore.SIGNAL(_fromUtf8("clicked()")), self.comboBox_dates.show)
        QtCore.QMetaObject.connectSlotsByName(Bon_Reception)
        Bon_Reception.setTabOrder(self.radioButton, self.radioButton_2)
        Bon_Reception.setTabOrder(self.radioButton_2, self.comboBox_dates)
        Bon_Reception.setTabOrder(self.comboBox_dates, self.tableWidget)
        Bon_Reception.setTabOrder(self.tableWidget, self.pushButton_export)

    def retranslateUi(self, Bon_Reception):
        Bon_Reception.setWindowTitle(_translate("Bon_Reception", "Bon de reception", None))
        self.groupBox.setTitle(_translate("Bon_Reception", "Type de tri", None))
        self.radioButton.setText(_translate("Bon_Reception", "Derniere date de reception", None))
        self.radioButton_2.setText(_translate("Bon_Reception", "Selectionner une date", None))
        item = self.tableWidget.horizontalHeaderItem(0)
        item.setText(_translate("Bon_Reception", "Date reception", None))
        item = self.tableWidget.horizontalHeaderItem(1)
        item.setText(_translate("Bon_Reception", "Code client", None))
        item = self.tableWidget.horizontalHeaderItem(2)
        item.setText(_translate("Bon_Reception", "Site", None))
        item = self.tableWidget.horizontalHeaderItem(3)
        item.setText(_translate("Bon_Reception", "Service", None))
        item = self.tableWidget.horizontalHeaderItem(4)
        item.setText(_translate("Bon_Reception", "Instrument", None))
        self.pushButton_export.setText(_translate("Bon_Reception", "Export ", None))

from Modules.Reception_expedition.BondeReception.GUI.extendedcombo import ExtendedCombo

if __name__ == "__main__":
    import sys
    app = QtGui.QApplication(sys.argv)
    Bon_Reception = QtGui.QMainWindow()
    ui = Ui_Bon_Reception()
    ui.setupUi(Bon_Reception)
    Bon_Reception.show()
    sys.exit(app.exec_())

