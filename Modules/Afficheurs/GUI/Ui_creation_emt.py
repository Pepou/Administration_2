# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'C:\Developpement Informatique\Python\Afficheurs\Afficheur-V1.4\GUI\creation_emt.ui'
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

class Ui_Creation_emt(object):
    def setupUi(self, Creation_emt):
        Creation_emt.setObjectName(_fromUtf8("Creation_emt"))
        Creation_emt.resize(624, 328)
        Creation_emt.setMinimumSize(QtCore.QSize(0, 328))
        Creation_emt.setMaximumSize(QtCore.QSize(16777215, 328))
        Creation_emt.setSizeGripEnabled(True)
        self.verticalLayout = QtGui.QVBoxLayout(Creation_emt)
        self.verticalLayout.setObjectName(_fromUtf8("verticalLayout"))
        self.formLayout = QtGui.QFormLayout()
        self.formLayout.setSizeConstraint(QtGui.QLayout.SetMaximumSize)
        self.formLayout.setFieldGrowthPolicy(QtGui.QFormLayout.AllNonFixedFieldsGrow)
        self.formLayout.setObjectName(_fromUtf8("formLayout"))
        self.label = QtGui.QLabel(Creation_emt)
        font = QtGui.QFont()
        font.setFamily(_fromUtf8("Calibri"))
        font.setPointSize(11)
        font.setBold(True)
        font.setWeight(75)
        self.label.setFont(font)
        self.label.setObjectName(_fromUtf8("label"))
        self.formLayout.setWidget(0, QtGui.QFormLayout.LabelRole, self.label)
        self.lineEdit_nom_referentiel = QtGui.QLineEdit(Creation_emt)
        self.lineEdit_nom_referentiel.setObjectName(_fromUtf8("lineEdit_nom_referentiel"))
        self.formLayout.setWidget(0, QtGui.QFormLayout.FieldRole, self.lineEdit_nom_referentiel)
        self.label_2 = QtGui.QLabel(Creation_emt)
        font = QtGui.QFont()
        font.setFamily(_fromUtf8("Calibri"))
        font.setPointSize(11)
        font.setBold(True)
        font.setWeight(75)
        self.label_2.setFont(font)
        self.label_2.setObjectName(_fromUtf8("label_2"))
        self.formLayout.setWidget(1, QtGui.QFormLayout.LabelRole, self.label_2)
        self.comboBox_designation = QtGui.QComboBox(Creation_emt)
        self.comboBox_designation.setEditable(False)
        self.comboBox_designation.setObjectName(_fromUtf8("comboBox_designation"))
        self.comboBox_designation.addItem(_fromUtf8(""))
        self.comboBox_designation.addItem(_fromUtf8(""))
        self.comboBox_designation.addItem(_fromUtf8(""))
        self.comboBox_designation.addItem(_fromUtf8(""))
        self.comboBox_designation.addItem(_fromUtf8(""))
        self.formLayout.setWidget(1, QtGui.QFormLayout.FieldRole, self.comboBox_designation)
        self.label_3 = QtGui.QLabel(Creation_emt)
        font = QtGui.QFont()
        font.setFamily(_fromUtf8("Calibri"))
        font.setPointSize(11)
        font.setBold(True)
        font.setWeight(75)
        self.label_3.setFont(font)
        self.label_3.setObjectName(_fromUtf8("label_3"))
        self.formLayout.setWidget(2, QtGui.QFormLayout.LabelRole, self.label_3)
        self.comboBox_type_erreur = QtGui.QComboBox(Creation_emt)
        self.comboBox_type_erreur.setEditable(True)
        self.comboBox_type_erreur.setObjectName(_fromUtf8("comboBox_type_erreur"))
        self.comboBox_type_erreur.addItem(_fromUtf8(""))
        self.formLayout.setWidget(2, QtGui.QFormLayout.FieldRole, self.comboBox_type_erreur)
        self.label_4 = QtGui.QLabel(Creation_emt)
        font = QtGui.QFont()
        font.setFamily(_fromUtf8("Calibri"))
        font.setPointSize(11)
        font.setBold(True)
        font.setWeight(75)
        self.label_4.setFont(font)
        self.label_4.setObjectName(_fromUtf8("label_4"))
        self.formLayout.setWidget(3, QtGui.QFormLayout.LabelRole, self.label_4)
        self.comboBox_commentaire_ref = QtGui.QComboBox(Creation_emt)
        self.comboBox_commentaire_ref.setObjectName(_fromUtf8("comboBox_commentaire_ref"))
        self.comboBox_commentaire_ref.addItem(_fromUtf8(""))
        self.comboBox_commentaire_ref.addItem(_fromUtf8(""))
        self.formLayout.setWidget(3, QtGui.QFormLayout.FieldRole, self.comboBox_commentaire_ref)
        self.label_5 = QtGui.QLabel(Creation_emt)
        font = QtGui.QFont()
        font.setFamily(_fromUtf8("Calibri"))
        font.setPointSize(11)
        font.setBold(True)
        font.setWeight(75)
        self.label_5.setFont(font)
        self.label_5.setObjectName(_fromUtf8("label_5"))
        self.formLayout.setWidget(4, QtGui.QFormLayout.LabelRole, self.label_5)
        self.comboBox_classe = QtGui.QComboBox(Creation_emt)
        self.comboBox_classe.setEnabled(True)
        self.comboBox_classe.setEditable(True)
        self.comboBox_classe.setObjectName(_fromUtf8("comboBox_classe"))
        self.comboBox_classe.addItem(_fromUtf8(""))
        self.formLayout.setWidget(4, QtGui.QFormLayout.FieldRole, self.comboBox_classe)
        self.label_6 = QtGui.QLabel(Creation_emt)
        font = QtGui.QFont()
        font.setFamily(_fromUtf8("Calibri"))
        font.setPointSize(11)
        font.setBold(True)
        font.setWeight(75)
        self.label_6.setFont(font)
        self.label_6.setObjectName(_fromUtf8("label_6"))
        self.formLayout.setWidget(5, QtGui.QFormLayout.LabelRole, self.label_6)
        self.lineEdit_valeur_min = QtGui.QLineEdit(Creation_emt)
        self.lineEdit_valeur_min.setObjectName(_fromUtf8("lineEdit_valeur_min"))
        self.formLayout.setWidget(5, QtGui.QFormLayout.FieldRole, self.lineEdit_valeur_min)
        self.label_7 = QtGui.QLabel(Creation_emt)
        font = QtGui.QFont()
        font.setFamily(_fromUtf8("Calibri"))
        font.setPointSize(11)
        font.setBold(True)
        font.setWeight(75)
        self.label_7.setFont(font)
        self.label_7.setObjectName(_fromUtf8("label_7"))
        self.formLayout.setWidget(6, QtGui.QFormLayout.LabelRole, self.label_7)
        self.lineEdit_valeur_max = QtGui.QLineEdit(Creation_emt)
        self.lineEdit_valeur_max.setObjectName(_fromUtf8("lineEdit_valeur_max"))
        self.formLayout.setWidget(6, QtGui.QFormLayout.FieldRole, self.lineEdit_valeur_max)
        self.label_8 = QtGui.QLabel(Creation_emt)
        font = QtGui.QFont()
        font.setFamily(_fromUtf8("Calibri"))
        font.setPointSize(11)
        font.setBold(True)
        font.setWeight(75)
        self.label_8.setFont(font)
        self.label_8.setObjectName(_fromUtf8("label_8"))
        self.formLayout.setWidget(7, QtGui.QFormLayout.LabelRole, self.label_8)
        self.comboBox_unite = QtGui.QComboBox(Creation_emt)
        self.comboBox_unite.setObjectName(_fromUtf8("comboBox_unite"))
        self.comboBox_unite.addItem(_fromUtf8(""))
        self.comboBox_unite.addItem(_fromUtf8(""))
        self.comboBox_unite.addItem(_fromUtf8(""))
        self.formLayout.setWidget(7, QtGui.QFormLayout.FieldRole, self.comboBox_unite)
        self.label_9 = QtGui.QLabel(Creation_emt)
        font = QtGui.QFont()
        font.setFamily(_fromUtf8("Calibri"))
        font.setPointSize(11)
        font.setBold(True)
        font.setWeight(75)
        self.label_9.setFont(font)
        self.label_9.setObjectName(_fromUtf8("label_9"))
        self.formLayout.setWidget(8, QtGui.QFormLayout.LabelRole, self.label_9)
        self.lineEdit_erreur_cte = QtGui.QLineEdit(Creation_emt)
        self.lineEdit_erreur_cte.setObjectName(_fromUtf8("lineEdit_erreur_cte"))
        self.formLayout.setWidget(8, QtGui.QFormLayout.FieldRole, self.lineEdit_erreur_cte)
        self.label_10 = QtGui.QLabel(Creation_emt)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Preferred, QtGui.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label_10.sizePolicy().hasHeightForWidth())
        self.label_10.setSizePolicy(sizePolicy)
        font = QtGui.QFont()
        font.setFamily(_fromUtf8("Calibri"))
        font.setPointSize(11)
        font.setBold(True)
        font.setWeight(75)
        self.label_10.setFont(font)
        self.label_10.setObjectName(_fromUtf8("label_10"))
        self.formLayout.setWidget(9, QtGui.QFormLayout.LabelRole, self.label_10)
        self.lineEdit_erreur_variable = QtGui.QLineEdit(Creation_emt)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.lineEdit_erreur_variable.sizePolicy().hasHeightForWidth())
        self.lineEdit_erreur_variable.setSizePolicy(sizePolicy)
        self.lineEdit_erreur_variable.setObjectName(_fromUtf8("lineEdit_erreur_variable"))
        self.formLayout.setWidget(9, QtGui.QFormLayout.FieldRole, self.lineEdit_erreur_variable)
        self.buttonBox = QtGui.QDialogButtonBox(Creation_emt)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.buttonBox.sizePolicy().hasHeightForWidth())
        self.buttonBox.setSizePolicy(sizePolicy)
        self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
        self.buttonBox.setStandardButtons(QtGui.QDialogButtonBox.Cancel|QtGui.QDialogButtonBox.Ok)
        self.buttonBox.setObjectName(_fromUtf8("buttonBox"))
        self.formLayout.setWidget(10, QtGui.QFormLayout.FieldRole, self.buttonBox)
        self.verticalLayout.addLayout(self.formLayout)

        self.retranslateUi(Creation_emt)
        QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL(_fromUtf8("accepted()")), Creation_emt.accept)
        QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL(_fromUtf8("rejected()")), Creation_emt.reject)
        QtCore.QMetaObject.connectSlotsByName(Creation_emt)

    def retranslateUi(self, Creation_emt):
        Creation_emt.setWindowTitle(_translate("Creation_emt", "Creation EMT", None))
        self.label.setText(_translate("Creation_emt", "Nom Referentiel", None))
        self.label_2.setText(_translate("Creation_emt", "Instruments concernes", None))
        self.comboBox_designation.setItemText(0, _translate("Creation_emt", "TÉMOIN D\'ENVIRONNEMENT", None))
        self.comboBox_designation.setItemText(1, _translate("Creation_emt", "SONDE ALARME TEMPÉRATURE", None))
        self.comboBox_designation.setItemText(2, _translate("Creation_emt", "AFFICHEUR DE TEMPÉRATURE", None))
        self.comboBox_designation.setItemText(3, _translate("Creation_emt", "AFFICHEUR DE TEMPS", None))
        self.comboBox_designation.setItemText(4, _translate("Creation_emt", "AFFICHEUR DE VITESSE", None))
        self.label_3.setText(_translate("Creation_emt", "Type d\'erreur", None))
        self.comboBox_type_erreur.setItemText(0, _translate("Creation_emt", "Erreur d\'indication", None))
        self.label_4.setText(_translate("Creation_emt", "Commentaire referentiel", None))
        self.comboBox_commentaire_ref.setItemText(0, _translate("Creation_emt", "Déclaration de conformité selon ISO 14 253-1 (prise en compte de U)", None))
        self.comboBox_commentaire_ref.setItemText(1, _translate("Creation_emt", "Déclaration de conformité sans prise en compte de U", None))
        self.label_5.setText(_translate("Creation_emt", "Classe", None))
        self.comboBox_classe.setItemText(0, _translate("Creation_emt", "Conforme", None))
        self.label_6.setText(_translate("Creation_emt", "Valeur min", None))
        self.lineEdit_valeur_min.setText(_translate("Creation_emt", "0", None))
        self.label_7.setText(_translate("Creation_emt", "Valeur max", None))
        self.lineEdit_valeur_max.setText(_translate("Creation_emt", "0", None))
        self.label_8.setText(_translate("Creation_emt", "Unite", None))
        self.comboBox_unite.setItemText(0, _translate("Creation_emt", "°C", None))
        self.comboBox_unite.setItemText(1, _translate("Creation_emt", "t/min", None))
        self.comboBox_unite.setItemText(2, _translate("Creation_emt", "s", None))
        self.label_9.setText(_translate("Creation_emt", "Erreur terme constant", None))
        self.label_10.setText(_translate("Creation_emt", "Erreur terme variable", None))


if __name__ == "__main__":
    import sys
    app = QtGui.QApplication(sys.argv)
    Creation_emt = QtGui.QDialog()
    ui = Ui_Creation_emt()
    ui.setupUi(Creation_emt)
    Creation_emt.show()
    sys.exit(app.exec_())

