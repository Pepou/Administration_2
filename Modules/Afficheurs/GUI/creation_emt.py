# -*- coding: utf-8 -*-

"""
Module implementing creation_emt.
"""

from PyQt4.QtCore import pyqtSlot
from PyQt4.QtGui import QDialog
from PyQt4.QtCore import SIGNAL

from Modules.Afficheurs.GUI.Ui_creation_emt import Ui_Creation_emt


class Creation_emt(QDialog, Ui_Creation_emt):
    """
    Class documentation goes here.
    """
    def __init__(self, parent=None):
        """
        Constructor
        
        @param parent reference to the parent widget (QWidget)
        """
        super(Creation_emt, self).__init__(parent)
        self.setupUi(self)
    
    @pyqtSlot()
    def on_buttonBox_rejected(self):
        """
        Slot documentation goes here.
        """
        # TODO: not implemented yet
        self.close()
    
    @pyqtSlot()
    def on_buttonBox_accepted(self):
        """
        Slot documentation goes here.
        """
        nouveau_ref_emt = {}
        nouveau_ref_emt["REFERENTIEL"] = self.lineEdit_nom_referentiel.text()        
        nouveau_ref_emt["DESIGNATION"] = self.comboBox_designation.currentText()
        nouveau_ref_emt["TYPE_ERREUR"] = self.comboBox_type_erreur.currentText()
        nouveau_ref_emt["COMMENTAIRE_REFERENTIEL"] = self.comboBox_commentaire_ref.currentText()
        nouveau_ref_emt["CLASSE"] = self.comboBox_classe.currentText()
        
        if self.lineEdit_valeur_min.text()!= "":
            nouveau_ref_emt["TEMP_MIN"] = self.lineEdit_valeur_min.text()
        else:
            nouveau_ref_emt["TEMP_MIN"] = 0
        
        if  self.lineEdit_valeur_max.text()!="":   
            nouveau_ref_emt["TEMP_MAX"] = self.lineEdit_valeur_max.text()
        else:
            nouveau_ref_emt["TEMP_MAX"] = 0
        nouveau_ref_emt["TEMP_UNITE"] = self.comboBox_unite.currentText()
        
        if self.lineEdit_erreur_cte.text() != "":
            nouveau_ref_emt["ERREUR_TERME_CST"] = self.lineEdit_erreur_cte.text()
        else: 
            nouveau_ref_emt["ERREUR_TERME_CST"] = 0
        
        if self.lineEdit_erreur_variable.text() != "":
            nouveau_ref_emt["ERREUR_TERME_VAR"] = self.lineEdit_erreur_variable.text()
        else:
            nouveau_ref_emt["ERREUR_TERME_VAR"] = 0
            
        nouveau_ref_emt["ERREUR_UNITE"] = self.comboBox_unite.currentText()
        nouveau_ref_emt["NORMATIF"] = 0
        
        self.emit(SIGNAL("fermeturequelclient(PyQt_PyObject)"), nouveau_ref_emt)
        
        
