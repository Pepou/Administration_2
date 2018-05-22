# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'C:\Travail\EFS\Travail accreditation\SQ\Developpement Informatique\Gestion_Fichiers_Enregistreurs\Builds\0.5\GUI\Affichage_graphique.ui'
#
# Created: Mon May  2 12:59:37 2016
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

class Ui_Graphique(object):
    def setupUi(self, Graphique):
        Graphique.setObjectName(_fromUtf8("Graphique"))
        Graphique.resize(800, 600)
        self.centralWidget = QtGui.QWidget(Graphique)
        self.centralWidget.setObjectName(_fromUtf8("centralWidget"))
        self.gridLayout = QtGui.QGridLayout(self.centralWidget)
        self.gridLayout.setObjectName(_fromUtf8("gridLayout"))
        self.verticalLayout = QtGui.QVBoxLayout()
        self.verticalLayout.setObjectName(_fromUtf8("verticalLayout"))
        self.graphique = matplotlibWidget(self.centralWidget)
        self.graphique.setObjectName(_fromUtf8("graphique"))
        self.verticalLayout.addWidget(self.graphique)
        self.buttonBox = QtGui.QDialogButtonBox(self.centralWidget)
        self.buttonBox.setStandardButtons(QtGui.QDialogButtonBox.Cancel|QtGui.QDialogButtonBox.Ok)
        self.buttonBox.setObjectName(_fromUtf8("buttonBox"))
        self.verticalLayout.addWidget(self.buttonBox)
        self.gridLayout.addLayout(self.verticalLayout, 0, 0, 1, 1)
        Graphique.setCentralWidget(self.centralWidget)

        self.retranslateUi(Graphique)
        QtCore.QMetaObject.connectSlotsByName(Graphique)

    def retranslateUi(self, Graphique):
        Graphique.setWindowTitle(_translate("Graphique", "Graphique donnees", None))

from GUI.matplotlibwidgetFile import matplotlibWidget

if __name__ == "__main__":
    import sys
    app = QtGui.QApplication(sys.argv)
    Graphique = QtGui.QMainWindow()
    ui = Ui_Graphique()
    ui.setupUi(Graphique)
    Graphique.show()
    sys.exit(app.exec_())

