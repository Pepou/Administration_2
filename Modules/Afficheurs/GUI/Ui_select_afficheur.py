# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'C:\Developpement Informatique\Python\Administration\Modules\Afficheurs\GUI\select_afficheur.ui'
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

class Ui_Modification_afficheur(object):
    def setupUi(self, Modification_afficheur):
        Modification_afficheur.setObjectName(_fromUtf8("Modification_afficheur"))
        Modification_afficheur.resize(315, 98)
        Modification_afficheur.setMinimumSize(QtCore.QSize(315, 98))
        Modification_afficheur.setMaximumSize(QtCore.QSize(315, 98))
        Modification_afficheur.setSizeGripEnabled(True)
        self.gridLayout_2 = QtGui.QGridLayout(Modification_afficheur)
        self.gridLayout_2.setObjectName(_fromUtf8("gridLayout_2"))
        self.gridLayout = QtGui.QGridLayout()
        self.gridLayout.setObjectName(_fromUtf8("gridLayout"))
        self.hboxlayout = QtGui.QHBoxLayout()
        self.hboxlayout.setSizeConstraint(QtGui.QLayout.SetMinimumSize)
        self.hboxlayout.setMargin(0)
        self.hboxlayout.setSpacing(6)
        self.hboxlayout.setObjectName(_fromUtf8("hboxlayout"))
        spacerItem = QtGui.QSpacerItem(131, 31, QtGui.QSizePolicy.Fixed, QtGui.QSizePolicy.Minimum)
        self.hboxlayout.addItem(spacerItem)
        self.okButton = QtGui.QPushButton(Modification_afficheur)
        self.okButton.setObjectName(_fromUtf8("okButton"))
        self.hboxlayout.addWidget(self.okButton)
        self.cancelButton = QtGui.QPushButton(Modification_afficheur)
        self.cancelButton.setObjectName(_fromUtf8("cancelButton"))
        self.hboxlayout.addWidget(self.cancelButton)
        self.gridLayout.addLayout(self.hboxlayout, 2, 0, 1, 1)
        self.comboBox = ExtendedCombo(Modification_afficheur)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Preferred, QtGui.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.comboBox.sizePolicy().hasHeightForWidth())
        self.comboBox.setSizePolicy(sizePolicy)
        self.comboBox.setObjectName(_fromUtf8("comboBox"))
        self.gridLayout.addWidget(self.comboBox, 1, 0, 1, 1)
        self.label = QtGui.QLabel(Modification_afficheur)
        self.label.setObjectName(_fromUtf8("label"))
        self.gridLayout.addWidget(self.label, 0, 0, 1, 1)
        self.gridLayout_2.addLayout(self.gridLayout, 0, 0, 1, 1)

        self.retranslateUi(Modification_afficheur)
        QtCore.QObject.connect(self.okButton, QtCore.SIGNAL(_fromUtf8("clicked()")), Modification_afficheur.accept)
        QtCore.QObject.connect(self.cancelButton, QtCore.SIGNAL(_fromUtf8("clicked()")), Modification_afficheur.reject)
        QtCore.QMetaObject.connectSlotsByName(Modification_afficheur)

    def retranslateUi(self, Modification_afficheur):
        Modification_afficheur.setWindowTitle(_translate("Modification_afficheur", "Modification afficheur", None))
        self.okButton.setText(_translate("Modification_afficheur", "&OK", None))
        self.cancelButton.setText(_translate("Modification_afficheur", "&Cancel", None))
        self.label.setText(_translate("Modification_afficheur", "Selectionner l\'afficheurà modifier", None))

from Modules.Afficheurs.GUI.extendedcombo import ExtendedCombo

if __name__ == "__main__":
    import sys
    app = QtGui.QApplication(sys.argv)
    Modification_afficheur = QtGui.QDialog()
    ui = Ui_Modification_afficheur()
    ui.setupUi(Modification_afficheur)
    Modification_afficheur.show()
    sys.exit(app.exec_())

