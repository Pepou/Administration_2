# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'Y:\Logiciels\Logiciels_techniques_labo\Polynome\A VALIDER  V1.11\GUI\polynome.ui'
#
# Created: Mon Jan 25 15:09:20 2016
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

class Ui_Polynome(object):
    def setupUi(self, Polynome):
        Polynome.setObjectName(_fromUtf8("Polynome"))
        Polynome.resize(875, 785)
        self.centralWidget = QtGui.QWidget(Polynome)
        self.centralWidget.setObjectName(_fromUtf8("centralWidget"))
        self.verticalLayout_3 = QtGui.QVBoxLayout(self.centralWidget)
        self.verticalLayout_3.setObjectName(_fromUtf8("verticalLayout_3"))
        self.tabWidget = QtGui.QTabWidget(self.centralWidget)
        self.tabWidget.setTabShape(QtGui.QTabWidget.Triangular)
        self.tabWidget.setElideMode(QtCore.Qt.ElideNone)
        self.tabWidget.setObjectName(_fromUtf8("tabWidget"))
        self.tab_1 = QtGui.QWidget()
        self.tab_1.setObjectName(_fromUtf8("tab_1"))
        self.verticalLayout = QtGui.QVBoxLayout(self.tab_1)
        self.verticalLayout.setObjectName(_fromUtf8("verticalLayout"))
        self.groupBox = QtGui.QGroupBox(self.tab_1)
        self.groupBox.setMinimumSize(QtCore.QSize(0, 73))
        self.groupBox.setMaximumSize(QtCore.QSize(16777215, 100))
        font = QtGui.QFont()
        font.setFamily(_fromUtf8("Calibri"))
        font.setPointSize(12)
        self.groupBox.setFont(font)
        self.groupBox.setObjectName(_fromUtf8("groupBox"))
        self.splitter = QtGui.QSplitter(self.groupBox)
        self.splitter.setGeometry(QtCore.QRect(10, 30, 1061, 23))
        self.splitter.setOrientation(QtCore.Qt.Horizontal)
        self.splitter.setObjectName(_fromUtf8("splitter"))
        self.radioButton_new_saisie = QtGui.QRadioButton(self.splitter)
        font = QtGui.QFont()
        font.setFamily(_fromUtf8("Calibri"))
        font.setPointSize(12)
        self.radioButton_new_saisie.setFont(font)
        self.radioButton_new_saisie.setObjectName(_fromUtf8("radioButton_new_saisie"))
        self.radioButton_modification = QtGui.QRadioButton(self.splitter)
        font = QtGui.QFont()
        font.setFamily(_fromUtf8("Calibri"))
        font.setPointSize(12)
        self.radioButton_modification.setFont(font)
        self.radioButton_modification.setObjectName(_fromUtf8("radioButton_modification"))
        self.verticalLayout.addWidget(self.groupBox)
        self.splitter_2 = QtGui.QSplitter(self.tab_1)
        self.splitter_2.setMaximumSize(QtCore.QSize(16777215, 16777215))
        self.splitter_2.setFrameShape(QtGui.QFrame.Panel)
        self.splitter_2.setLineWidth(1)
        self.splitter_2.setOrientation(QtCore.Qt.Vertical)
        self.splitter_2.setObjectName(_fromUtf8("splitter_2"))
        self.label_10 = QtGui.QLabel(self.splitter_2)
        self.label_10.setAlignment(QtCore.Qt.AlignLeading|QtCore.Qt.AlignLeft|QtCore.Qt.AlignVCenter)
        self.label_10.setMargin(4)
        self.label_10.setObjectName(_fromUtf8("label_10"))
        self.layoutWidget = QtGui.QWidget(self.splitter_2)
        self.layoutWidget.setObjectName(_fromUtf8("layoutWidget"))
        self.formLayout = QtGui.QFormLayout(self.layoutWidget)
        self.formLayout.setFieldGrowthPolicy(QtGui.QFormLayout.AllNonFixedFieldsGrow)
        self.formLayout.setContentsMargins(9, -1, 9, 0)
        self.formLayout.setHorizontalSpacing(6)
        self.formLayout.setVerticalSpacing(10)
        self.formLayout.setObjectName(_fromUtf8("formLayout"))
        self.label_11 = QtGui.QLabel(self.layoutWidget)
        self.label_11.setMaximumSize(QtCore.QSize(16777215, 30))
        self.label_11.setAlignment(QtCore.Qt.AlignCenter)
        self.label_11.setObjectName(_fromUtf8("label_11"))
        self.formLayout.setWidget(0, QtGui.QFormLayout.LabelRole, self.label_11)
        self.comboBox_identification = ExtendedCombo(self.layoutWidget)
        self.comboBox_identification.setEnabled(True)
        self.comboBox_identification.setMinimumSize(QtCore.QSize(0, 25))
        self.comboBox_identification.setMaximumSize(QtCore.QSize(16777215, 30))
        self.comboBox_identification.setMouseTracking(True)
        self.comboBox_identification.setAcceptDrops(True)
        self.comboBox_identification.setEditable(True)
        self.comboBox_identification.setObjectName(_fromUtf8("comboBox_identification"))
        self.formLayout.setWidget(0, QtGui.QFormLayout.FieldRole, self.comboBox_identification)
        self.label_15 = QtGui.QLabel(self.layoutWidget)
        self.label_15.setMaximumSize(QtCore.QSize(16777215, 30))
        self.label_15.setAlignment(QtCore.Qt.AlignCenter)
        self.label_15.setObjectName(_fromUtf8("label_15"))
        self.formLayout.setWidget(1, QtGui.QFormLayout.LabelRole, self.label_15)
        self.comboBox_n_ce = QtGui.QComboBox(self.layoutWidget)
        self.comboBox_n_ce.setMinimumSize(QtCore.QSize(0, 25))
        self.comboBox_n_ce.setMaximumSize(QtCore.QSize(16777215, 30))
        self.comboBox_n_ce.setEditable(True)
        self.comboBox_n_ce.setModelColumn(0)
        self.comboBox_n_ce.setObjectName(_fromUtf8("comboBox_n_ce"))
        self.formLayout.setWidget(1, QtGui.QFormLayout.FieldRole, self.comboBox_n_ce)
        self.label_7 = QtGui.QLabel(self.layoutWidget)
        self.label_7.setMaximumSize(QtCore.QSize(16777215, 30))
        self.label_7.setAlignment(QtCore.Qt.AlignCenter)
        self.label_7.setObjectName(_fromUtf8("label_7"))
        self.formLayout.setWidget(2, QtGui.QFormLayout.LabelRole, self.label_7)
        self.dateEdit = QtGui.QDateEdit(self.layoutWidget)
        self.dateEdit.setMinimumSize(QtCore.QSize(206, 0))
        self.dateEdit.setMaximumSize(QtCore.QSize(16777215, 30))
        self.dateEdit.setDate(QtCore.QDate(2014, 1, 1))
        self.dateEdit.setCalendarPopup(True)
        self.dateEdit.setObjectName(_fromUtf8("dateEdit"))
        self.formLayout.setWidget(2, QtGui.QFormLayout.FieldRole, self.dateEdit)
        self.label_12 = QtGui.QLabel(self.layoutWidget)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label_12.sizePolicy().hasHeightForWidth())
        self.label_12.setSizePolicy(sizePolicy)
        self.label_12.setMaximumSize(QtCore.QSize(16777215, 30))
        self.label_12.setObjectName(_fromUtf8("label_12"))
        self.formLayout.setWidget(3, QtGui.QFormLayout.LabelRole, self.label_12)
        self.textEdit_constructeur = QtGui.QTextEdit(self.layoutWidget)
        self.textEdit_constructeur.setMaximumSize(QtCore.QSize(16777215, 30))
        self.textEdit_constructeur.setObjectName(_fromUtf8("textEdit_constructeur"))
        self.formLayout.setWidget(3, QtGui.QFormLayout.FieldRole, self.textEdit_constructeur)
        self.label_13 = QtGui.QLabel(self.layoutWidget)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label_13.sizePolicy().hasHeightForWidth())
        self.label_13.setSizePolicy(sizePolicy)
        self.label_13.setMinimumSize(QtCore.QSize(200, 0))
        self.label_13.setMaximumSize(QtCore.QSize(16777215, 30))
        self.label_13.setObjectName(_fromUtf8("label_13"))
        self.formLayout.setWidget(4, QtGui.QFormLayout.LabelRole, self.label_13)
        self.textEdit_n_serie = QtGui.QTextEdit(self.layoutWidget)
        self.textEdit_n_serie.setMaximumSize(QtCore.QSize(16777215, 30))
        self.textEdit_n_serie.setObjectName(_fromUtf8("textEdit_n_serie"))
        self.formLayout.setWidget(4, QtGui.QFormLayout.FieldRole, self.textEdit_n_serie)
        self.label_14 = QtGui.QLabel(self.layoutWidget)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label_14.sizePolicy().hasHeightForWidth())
        self.label_14.setSizePolicy(sizePolicy)
        self.label_14.setMaximumSize(QtCore.QSize(16777215, 30))
        self.label_14.setObjectName(_fromUtf8("label_14"))
        self.formLayout.setWidget(5, QtGui.QFormLayout.LabelRole, self.label_14)
        self.textEdit_model = QtGui.QTextEdit(self.layoutWidget)
        self.textEdit_model.setMaximumSize(QtCore.QSize(16777215, 30))
        self.textEdit_model.setObjectName(_fromUtf8("textEdit_model"))
        self.formLayout.setWidget(5, QtGui.QFormLayout.FieldRole, self.textEdit_model)
        self.label_16 = QtGui.QLabel(self.layoutWidget)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label_16.sizePolicy().hasHeightForWidth())
        self.label_16.setSizePolicy(sizePolicy)
        self.label_16.setMaximumSize(QtCore.QSize(16777215, 30))
        self.label_16.setObjectName(_fromUtf8("label_16"))
        self.formLayout.setWidget(7, QtGui.QFormLayout.LabelRole, self.label_16)
        self.comboBox_etat_polynome = QtGui.QComboBox(self.layoutWidget)
        self.comboBox_etat_polynome.setObjectName(_fromUtf8("comboBox_etat_polynome"))
        self.comboBox_etat_polynome.addItem(_fromUtf8(""))
        self.comboBox_etat_polynome.addItem(_fromUtf8(""))
        self.formLayout.setWidget(7, QtGui.QFormLayout.FieldRole, self.comboBox_etat_polynome)
        self.lineEdit_resolution = QtGui.QLineEdit(self.layoutWidget)
        self.lineEdit_resolution.setObjectName(_fromUtf8("lineEdit_resolution"))
        self.formLayout.setWidget(6, QtGui.QFormLayout.FieldRole, self.lineEdit_resolution)
        self.label_6 = QtGui.QLabel(self.layoutWidget)
        font = QtGui.QFont()
        font.setFamily(_fromUtf8("Calibri"))
        font.setPointSize(12)
        self.label_6.setFont(font)
        self.label_6.setObjectName(_fromUtf8("label_6"))
        self.formLayout.setWidget(6, QtGui.QFormLayout.LabelRole, self.label_6)
        self.verticalLayout.addWidget(self.splitter_2)
        self.splitter_3 = QtGui.QSplitter(self.tab_1)
        self.splitter_3.setFrameShape(QtGui.QFrame.Panel)
        self.splitter_3.setOrientation(QtCore.Qt.Vertical)
        self.splitter_3.setObjectName(_fromUtf8("splitter_3"))
        self.label_5 = QtGui.QLabel(self.splitter_3)
        self.label_5.setMargin(4)
        self.label_5.setObjectName(_fromUtf8("label_5"))
        self.tableWidget_table_etalonnage = QtGui.QTableWidget(self.splitter_3)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(200)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.tableWidget_table_etalonnage.sizePolicy().hasHeightForWidth())
        self.tableWidget_table_etalonnage.setSizePolicy(sizePolicy)
        self.tableWidget_table_etalonnage.setMinimumSize(QtCore.QSize(0, 0))
        self.tableWidget_table_etalonnage.setBaseSize(QtCore.QSize(0, 0))
        self.tableWidget_table_etalonnage.setFrameShadow(QtGui.QFrame.Sunken)
        self.tableWidget_table_etalonnage.setLineWidth(1)
        self.tableWidget_table_etalonnage.setMidLineWidth(0)
        self.tableWidget_table_etalonnage.setAutoScroll(False)
        self.tableWidget_table_etalonnage.setAutoScrollMargin(10)
        self.tableWidget_table_etalonnage.setProperty("showDropIndicator", True)
        self.tableWidget_table_etalonnage.setAlternatingRowColors(True)
        self.tableWidget_table_etalonnage.setShowGrid(True)
        self.tableWidget_table_etalonnage.setGridStyle(QtCore.Qt.DashDotLine)
        self.tableWidget_table_etalonnage.setObjectName(_fromUtf8("tableWidget_table_etalonnage"))
        self.tableWidget_table_etalonnage.setColumnCount(4)
        self.tableWidget_table_etalonnage.setRowCount(0)
        item = QtGui.QTableWidgetItem()
        self.tableWidget_table_etalonnage.setHorizontalHeaderItem(0, item)
        item = QtGui.QTableWidgetItem()
        self.tableWidget_table_etalonnage.setHorizontalHeaderItem(1, item)
        item = QtGui.QTableWidgetItem()
        self.tableWidget_table_etalonnage.setHorizontalHeaderItem(2, item)
        item = QtGui.QTableWidgetItem()
        self.tableWidget_table_etalonnage.setHorizontalHeaderItem(3, item)
        self.tableWidget_table_etalonnage.verticalHeader().setMinimumSectionSize(19)
        self.layoutWidget_2 = QtGui.QWidget(self.splitter_3)
        self.layoutWidget_2.setObjectName(_fromUtf8("layoutWidget_2"))
        self.gridLayout = QtGui.QGridLayout(self.layoutWidget_2)
        self.gridLayout.setMargin(0)
        self.gridLayout.setObjectName(_fromUtf8("gridLayout"))
        self.Button_plus = QtGui.QPushButton(self.layoutWidget_2)
        self.Button_plus.setText(_fromUtf8(""))
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(_fromUtf8(":/Icones/ajouter-en-plus-icone-7956-48.png")), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.Button_plus.setIcon(icon)
        self.Button_plus.setObjectName(_fromUtf8("Button_plus"))
        self.gridLayout.addWidget(self.Button_plus, 0, 0, 1, 1)
        self.buttton_supp = QtGui.QPushButton(self.layoutWidget_2)
        self.buttton_supp.setText(_fromUtf8(""))
        icon1 = QtGui.QIcon()
        icon1.addPixmap(QtGui.QPixmap(_fromUtf8(":/Icones/moins-arriere-zoom-icone-6351-128.PNG")), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.buttton_supp.setIcon(icon1)
        self.buttton_supp.setObjectName(_fromUtf8("buttton_supp"))
        self.gridLayout.addWidget(self.buttton_supp, 0, 1, 1, 1)
        spacerItem = QtGui.QSpacerItem(2000, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.gridLayout.addItem(spacerItem, 0, 3, 1, 1)
        self.tableWidget_polynome = QtGui.QTableWidget(self.layoutWidget_2)
        self.tableWidget_polynome.setObjectName(_fromUtf8("tableWidget_polynome"))
        self.tableWidget_polynome.setColumnCount(4)
        self.tableWidget_polynome.setRowCount(1)
        item = QtGui.QTableWidgetItem()
        self.tableWidget_polynome.setVerticalHeaderItem(0, item)
        item = QtGui.QTableWidgetItem()
        self.tableWidget_polynome.setHorizontalHeaderItem(0, item)
        item = QtGui.QTableWidgetItem()
        self.tableWidget_polynome.setHorizontalHeaderItem(1, item)
        item = QtGui.QTableWidgetItem()
        self.tableWidget_polynome.setHorizontalHeaderItem(2, item)
        item = QtGui.QTableWidgetItem()
        self.tableWidget_polynome.setHorizontalHeaderItem(3, item)
        self.gridLayout.addWidget(self.tableWidget_polynome, 1, 0, 1, 4)
        self.button_actualise = QtGui.QPushButton(self.layoutWidget_2)
        self.button_actualise.setMaximumSize(QtCore.QSize(28, 16777215))
        self.button_actualise.setText(_fromUtf8(""))
        icon2 = QtGui.QIcon()
        icon2.addPixmap(QtGui.QPixmap(_fromUtf8(":/Icones/icone_actualiser.png")), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.button_actualise.setIcon(icon2)
        self.button_actualise.setObjectName(_fromUtf8("button_actualise"))
        self.gridLayout.addWidget(self.button_actualise, 0, 2, 1, 1)
        self.verticalLayout.addWidget(self.splitter_3)
        self.tabWidget.addTab(self.tab_1, _fromUtf8(""))
        self.tab = QtGui.QWidget()
        self.tab.setObjectName(_fromUtf8("tab"))
        self.gridLayout_2 = QtGui.QGridLayout(self.tab)
        self.gridLayout_2.setObjectName(_fromUtf8("gridLayout_2"))
        self.scrollArea = QtGui.QScrollArea(self.tab)
        self.scrollArea.setWidgetResizable(True)
        self.scrollArea.setObjectName(_fromUtf8("scrollArea"))
        self.scrollAreaWidgetContents = QtGui.QWidget()
        self.scrollAreaWidgetContents.setGeometry(QtCore.QRect(0, 0, 775, 539))
        self.scrollAreaWidgetContents.setObjectName(_fromUtf8("scrollAreaWidgetContents"))
        self.verticalLayout_2 = QtGui.QVBoxLayout(self.scrollAreaWidgetContents)
        self.verticalLayout_2.setObjectName(_fromUtf8("verticalLayout_2"))
        self.splitter_4 = QtGui.QSplitter(self.scrollAreaWidgetContents)
        self.splitter_4.setOrientation(QtCore.Qt.Vertical)
        self.splitter_4.setObjectName(_fromUtf8("splitter_4"))
        self.graphicsView = PlotWidget(self.splitter_4)
        self.graphicsView.setMinimumSize(QtCore.QSize(0, 214))
        self.graphicsView.setObjectName(_fromUtf8("graphicsView"))
        self.tableWidget_modelisation = QtGui.QTableWidget(self.splitter_4)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(200)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.tableWidget_modelisation.sizePolicy().hasHeightForWidth())
        self.tableWidget_modelisation.setSizePolicy(sizePolicy)
        self.tableWidget_modelisation.setMinimumSize(QtCore.QSize(0, 0))
        self.tableWidget_modelisation.setBaseSize(QtCore.QSize(0, 0))
        self.tableWidget_modelisation.setFrameShape(QtGui.QFrame.Panel)
        self.tableWidget_modelisation.setFrameShadow(QtGui.QFrame.Plain)
        self.tableWidget_modelisation.setAutoScroll(False)
        self.tableWidget_modelisation.setAutoScrollMargin(10)
        self.tableWidget_modelisation.setProperty("showDropIndicator", True)
        self.tableWidget_modelisation.setAlternatingRowColors(True)
        self.tableWidget_modelisation.setShowGrid(True)
        self.tableWidget_modelisation.setGridStyle(QtCore.Qt.DashDotLine)
        self.tableWidget_modelisation.setObjectName(_fromUtf8("tableWidget_modelisation"))
        self.tableWidget_modelisation.setColumnCount(7)
        self.tableWidget_modelisation.setRowCount(0)
        item = QtGui.QTableWidgetItem()
        self.tableWidget_modelisation.setHorizontalHeaderItem(0, item)
        item = QtGui.QTableWidgetItem()
        self.tableWidget_modelisation.setHorizontalHeaderItem(1, item)
        item = QtGui.QTableWidgetItem()
        self.tableWidget_modelisation.setHorizontalHeaderItem(2, item)
        item = QtGui.QTableWidgetItem()
        self.tableWidget_modelisation.setHorizontalHeaderItem(3, item)
        item = QtGui.QTableWidgetItem()
        self.tableWidget_modelisation.setHorizontalHeaderItem(4, item)
        item = QtGui.QTableWidgetItem()
        self.tableWidget_modelisation.setHorizontalHeaderItem(5, item)
        item = QtGui.QTableWidgetItem()
        self.tableWidget_modelisation.setHorizontalHeaderItem(6, item)
        self.tableWidget_modelisation.verticalHeader().setMinimumSectionSize(19)
        self.layoutWidget1 = QtGui.QWidget(self.splitter_4)
        self.layoutWidget1.setObjectName(_fromUtf8("layoutWidget1"))
        self.formLayout_2 = QtGui.QFormLayout(self.layoutWidget1)
        self.formLayout_2.setFieldGrowthPolicy(QtGui.QFormLayout.AllNonFixedFieldsGrow)
        self.formLayout_2.setContentsMargins(0, 10, 500, -1)
        self.formLayout_2.setVerticalSpacing(19)
        self.formLayout_2.setObjectName(_fromUtf8("formLayout_2"))
        self.label = QtGui.QLabel(self.layoutWidget1)
        self.label.setMinimumSize(QtCore.QSize(200, 0))
        font = QtGui.QFont()
        font.setFamily(_fromUtf8("Calibri"))
        font.setPointSize(12)
        self.label.setFont(font)
        self.label.setObjectName(_fromUtf8("label"))
        self.formLayout_2.setWidget(0, QtGui.QFormLayout.LabelRole, self.label)
        self.lineEdit_incertitude_max_etal = QtGui.QLineEdit(self.layoutWidget1)
        self.lineEdit_incertitude_max_etal.setObjectName(_fromUtf8("lineEdit_incertitude_max_etal"))
        self.formLayout_2.setWidget(0, QtGui.QFormLayout.FieldRole, self.lineEdit_incertitude_max_etal)
        self.label_2 = QtGui.QLabel(self.layoutWidget1)
        font = QtGui.QFont()
        font.setFamily(_fromUtf8("Calibri"))
        font.setPointSize(12)
        self.label_2.setFont(font)
        self.label_2.setObjectName(_fromUtf8("label_2"))
        self.formLayout_2.setWidget(1, QtGui.QFormLayout.LabelRole, self.label_2)
        self.lineEdit_residu_max = QtGui.QLineEdit(self.layoutWidget1)
        self.lineEdit_residu_max.setObjectName(_fromUtf8("lineEdit_residu_max"))
        self.formLayout_2.setWidget(1, QtGui.QFormLayout.FieldRole, self.lineEdit_residu_max)
        self.label_3 = QtGui.QLabel(self.layoutWidget1)
        font = QtGui.QFont()
        font.setFamily(_fromUtf8("Calibri"))
        font.setPointSize(12)
        self.label_3.setFont(font)
        self.label_3.setObjectName(_fromUtf8("label_3"))
        self.formLayout_2.setWidget(2, QtGui.QFormLayout.LabelRole, self.label_3)
        self.lineEdit_incertitude_residu_max = QtGui.QLineEdit(self.layoutWidget1)
        self.lineEdit_incertitude_residu_max.setObjectName(_fromUtf8("lineEdit_incertitude_residu_max"))
        self.formLayout_2.setWidget(2, QtGui.QFormLayout.FieldRole, self.lineEdit_incertitude_residu_max)
        self.label_4 = QtGui.QLabel(self.layoutWidget1)
        font = QtGui.QFont()
        font.setFamily(_fromUtf8("Calibri"))
        font.setPointSize(12)
        self.label_4.setFont(font)
        self.label_4.setObjectName(_fromUtf8("label_4"))
        self.formLayout_2.setWidget(3, QtGui.QFormLayout.LabelRole, self.label_4)
        self.lineEdit_ecartype_residus = QtGui.QLineEdit(self.layoutWidget1)
        self.lineEdit_ecartype_residus.setObjectName(_fromUtf8("lineEdit_ecartype_residus"))
        self.formLayout_2.setWidget(3, QtGui.QFormLayout.FieldRole, self.lineEdit_ecartype_residus)
        self.label_8 = QtGui.QLabel(self.layoutWidget1)
        font = QtGui.QFont()
        font.setFamily(_fromUtf8("Calibri"))
        font.setPointSize(12)
        self.label_8.setFont(font)
        self.label_8.setObjectName(_fromUtf8("label_8"))
        self.formLayout_2.setWidget(4, QtGui.QFormLayout.LabelRole, self.label_8)
        self.lineEdit_normalite_residus = QtGui.QLineEdit(self.layoutWidget1)
        self.lineEdit_normalite_residus.setObjectName(_fromUtf8("lineEdit_normalite_residus"))
        self.formLayout_2.setWidget(4, QtGui.QFormLayout.FieldRole, self.lineEdit_normalite_residus)
        self.label_17 = QtGui.QLabel(self.layoutWidget1)
        font = QtGui.QFont()
        font.setFamily(_fromUtf8("Calibri"))
        font.setPointSize(12)
        self.label_17.setFont(font)
        self.label_17.setObjectName(_fromUtf8("label_17"))
        self.formLayout_2.setWidget(5, QtGui.QFormLayout.LabelRole, self.label_17)
        self.lineEdit_incertitude_modelisation = QtGui.QLineEdit(self.layoutWidget1)
        self.lineEdit_incertitude_modelisation.setObjectName(_fromUtf8("lineEdit_incertitude_modelisation"))
        self.formLayout_2.setWidget(5, QtGui.QFormLayout.FieldRole, self.lineEdit_incertitude_modelisation)
        self.verticalLayout_2.addWidget(self.splitter_4)
        self.scrollArea.setWidget(self.scrollAreaWidgetContents)
        self.gridLayout_2.addWidget(self.scrollArea, 0, 0, 1, 1)
        self.tabWidget.addTab(self.tab, _fromUtf8(""))
        self.tab_2 = QtGui.QWidget()
        self.tab_2.setObjectName(_fromUtf8("tab_2"))
        self.gridLayout_5 = QtGui.QGridLayout(self.tab_2)
        self.gridLayout_5.setObjectName(_fromUtf8("gridLayout_5"))
        self.graphicsView_2 = PlotWidget(self.tab_2)
        self.graphicsView_2.setObjectName(_fromUtf8("graphicsView_2"))
        self.gridLayout_5.addWidget(self.graphicsView_2, 0, 0, 1, 1)
        self.tabWidget.addTab(self.tab_2, _fromUtf8(""))
        self.verticalLayout_3.addWidget(self.tabWidget)
        Polynome.setCentralWidget(self.centralWidget)
        self.menuBar = QtGui.QMenuBar(Polynome)
        self.menuBar.setGeometry(QtCore.QRect(0, 0, 875, 21))
        self.menuBar.setObjectName(_fromUtf8("menuBar"))
        self.menuEnregistrer = QtGui.QMenu(self.menuBar)
        self.menuEnregistrer.setObjectName(_fromUtf8("menuEnregistrer"))
        self.menuEdition = QtGui.QMenu(self.menuBar)
        self.menuEdition.setObjectName(_fromUtf8("menuEdition"))
        Polynome.setMenuBar(self.menuBar)
        self.actionEnregistrer = QtGui.QAction(Polynome)
        self.actionEnregistrer.setObjectName(_fromUtf8("actionEnregistrer"))
        self.actionMise_jour = QtGui.QAction(Polynome)
        self.actionMise_jour.setObjectName(_fromUtf8("actionMise_jour"))
        self.actionSupprimer = QtGui.QAction(Polynome)
        self.actionSupprimer.setObjectName(_fromUtf8("actionSupprimer"))
        self.actionExport_Rapport = QtGui.QAction(Polynome)
        self.actionExport_Rapport.setObjectName(_fromUtf8("actionExport_Rapport"))
        self.menuEnregistrer.addAction(self.actionEnregistrer)
        self.menuEnregistrer.addAction(self.actionMise_jour)
        self.menuEnregistrer.addAction(self.actionSupprimer)
        self.menuEdition.addAction(self.actionExport_Rapport)
        self.menuBar.addAction(self.menuEnregistrer.menuAction())
        self.menuBar.addAction(self.menuEdition.menuAction())

        self.retranslateUi(Polynome)
        self.tabWidget.setCurrentIndex(0)
        QtCore.QMetaObject.connectSlotsByName(Polynome)

    def retranslateUi(self, Polynome):
        Polynome.setWindowTitle(_translate("Polynome", "Polynome de modelisation v1.11", None))
        self.groupBox.setTitle(_translate("Polynome", "Selection operation ", None))
        self.radioButton_new_saisie.setText(_translate("Polynome", "Nouvelle Saisie", None))
        self.radioButton_modification.setText(_translate("Polynome", "Modification/Consultation", None))
        self.label_10.setText(_translate("Polynome", "<html><head/><body><p><span style=\" font-size:12pt; text-decoration: underline;\">Instrument à modeliser</span></p></body></html>", None))
        self.label_11.setText(_translate("Polynome", "<html><head/><body><p align=\"center\"><span style=\" font-size:11pt;\">Identification Instrument</span></p></body></html>", None))
        self.label_15.setText(_translate("Polynome", "<html><head/><body><p><span style=\" font-size:11pt;\">N°Certificat</span></p></body></html>", None))
        self.label_7.setText(_translate("Polynome", "<html><head/><body><p><span style=\" font-size:11pt;\">Date Etalonnage</span></p></body></html>", None))
        self.label_12.setText(_translate("Polynome", "<html><head/><body><p align=\"center\"><span style=\" font-size:11pt;\">Constructeur</span></p></body></html>", None))
        self.label_13.setText(_translate("Polynome", "<html><head/><body><p><span style=\" font-size:11pt;\">N° Serie</span></p></body></html>", None))
        self.label_14.setText(_translate("Polynome", "<html><head/><body><p align=\"center\"><span style=\" font-size:11pt;\">Model</span></p></body></html>", None))
        self.label_16.setText(_translate("Polynome", "<html><head/><body><p align=\"center\"><span style=\" font-size:11pt;\">Etat Polynome</span></p></body></html>", None))
        self.comboBox_etat_polynome.setItemText(0, _translate("Polynome", "Archivé", None))
        self.comboBox_etat_polynome.setItemText(1, _translate("Polynome", "Actif", None))
        self.label_6.setText(_translate("Polynome", "<html><head/><body><p align=\"center\">Resolution</p></body></html>", None))
        self.label_5.setText(_translate("Polynome", "<html><head/><body><p><span style=\" font-size:12pt; text-decoration: underline;\">Information Etalonnage</span></p></body></html>", None))
        item = self.tableWidget_table_etalonnage.horizontalHeaderItem(0)
        item.setText(_translate("Polynome", "Valeurs de l\'etalon corrigées", None))
        item = self.tableWidget_table_etalonnage.horizontalHeaderItem(1)
        item.setText(_translate("Polynome", "Valeurs chaine de mesure à étalonner", None))
        item = self.tableWidget_table_etalonnage.horizontalHeaderItem(2)
        item.setText(_translate("Polynome", "Corrections", None))
        item = self.tableWidget_table_etalonnage.horizontalHeaderItem(3)
        item.setText(_translate("Polynome", "Incertitude (k=2)", None))
        item = self.tableWidget_polynome.verticalHeaderItem(0)
        item.setText(_translate("Polynome", "Polynome Correction = f(Tlue)", None))
        item = self.tableWidget_polynome.horizontalHeaderItem(0)
        item.setText(_translate("Polynome", "Ordre Polynome", None))
        item = self.tableWidget_polynome.horizontalHeaderItem(1)
        item.setText(_translate("Polynome", "A", None))
        item = self.tableWidget_polynome.horizontalHeaderItem(2)
        item.setText(_translate("Polynome", "B", None))
        item = self.tableWidget_polynome.horizontalHeaderItem(3)
        item.setText(_translate("Polynome", "C", None))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab_1), _translate("Polynome", "Saisie", None))
        item = self.tableWidget_modelisation.horizontalHeaderItem(0)
        item.setText(_translate("Polynome", "Valeurs de l\'etalon corrigées", None))
        item = self.tableWidget_modelisation.horizontalHeaderItem(1)
        item.setText(_translate("Polynome", "Valeurs chaine de mesure à étalonner", None))
        item = self.tableWidget_modelisation.horizontalHeaderItem(2)
        item.setText(_translate("Polynome", "Corrections", None))
        item = self.tableWidget_modelisation.horizontalHeaderItem(3)
        item.setText(_translate("Polynome", "Incertitudes", None))
        item = self.tableWidget_modelisation.horizontalHeaderItem(4)
        item.setText(_translate("Polynome", "Corrections modelisees", None))
        item = self.tableWidget_modelisation.horizontalHeaderItem(5)
        item.setText(_translate("Polynome", "Residus", None))
        item = self.tableWidget_modelisation.horizontalHeaderItem(6)
        item.setText(_translate("Polynome", "Recouvrement incertitudes", None))
        self.label.setText(_translate("Polynome", "Incertitude d\'etalonnage max", None))
        self.label_2.setText(_translate("Polynome", "Residu max", None))
        self.label_3.setText(_translate("Polynome", "Incertitude Residu max", None))
        self.label_4.setText(_translate("Polynome", "Ecart type des residus", None))
        self.label_8.setText(_translate("Polynome", "Normalite des residus", None))
        self.label_17.setText(_translate("Polynome", "Incertitude modelisation", None))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab), _translate("Polynome", "Analyse", None))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab_2), _translate("Polynome", "Analyse_residus", None))
        self.menuEnregistrer.setTitle(_translate("Polynome", "Sauvegarder", None))
        self.menuEdition.setTitle(_translate("Polynome", "Edition", None))
        self.actionEnregistrer.setText(_translate("Polynome", "Enregistrer", None))
        self.actionMise_jour.setText(_translate("Polynome", "Mise à jour", None))
        self.actionSupprimer.setText(_translate("Polynome", "Supprimer", None))
        self.actionExport_Rapport.setText(_translate("Polynome", "Export Rapport", None))

from pyqtgraph import PlotWidget
from Modules.Polynome.GUI.extendedcombo import ExtendedCombo
import Modules.Polynome.Icones_rc

if __name__ == "__main__":
    import sys
    app = QtGui.QApplication(sys.argv)
    Polynome = QtGui.QMainWindow()
    ui = Ui_Polynome()
    ui.setupUi(Polynome)
    Polynome.show()
    sys.exit(app.exec_())

