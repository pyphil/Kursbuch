# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file '.\Abgangsdatum.ui'
#
# Created by: PyQt5 UI code generator 5.15.1
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_Abgangsdatum(object):
    def setupUi(self, Abgangsdatum):
        Abgangsdatum.setObjectName("Abgangsdatum")
        Abgangsdatum.setWindowModality(QtCore.Qt.ApplicationModal)
        Abgangsdatum.resize(364, 108)
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(".\\kursbuch.ico"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        Abgangsdatum.setWindowIcon(icon)
        self.gridLayout_2 = QtWidgets.QGridLayout(Abgangsdatum)
        self.gridLayout_2.setObjectName("gridLayout_2")
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.gridLayout = QtWidgets.QGridLayout()
        self.gridLayout.setObjectName("gridLayout")
        self.label = QtWidgets.QLabel(Abgangsdatum)
        self.label.setObjectName("label")
        self.gridLayout.addWidget(self.label, 0, 0, 1, 1)
        self.labelSname = QtWidgets.QLabel(Abgangsdatum)
        font = QtGui.QFont()
        font.setBold(True)
        font.setWeight(75)
        self.labelSname.setFont(font)
        self.labelSname.setObjectName("labelSname")
        self.gridLayout.addWidget(self.labelSname, 1, 0, 1, 1)
        self.horizontalLayout.addLayout(self.gridLayout)
        spacerItem = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout.addItem(spacerItem)
        self.dateEdit = QtWidgets.QDateEdit(Abgangsdatum)
        self.dateEdit.setCalendarPopup(True)
        self.dateEdit.setObjectName("dateEdit")
        self.horizontalLayout.addWidget(self.dateEdit)
        self.gridLayout_2.addLayout(self.horizontalLayout, 0, 0, 1, 2)
        spacerItem1 = QtWidgets.QSpacerItem(239, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.gridLayout_2.addItem(spacerItem1, 1, 0, 1, 1)
        self.pushButtonOK = QtWidgets.QPushButton(Abgangsdatum)
        self.pushButtonOK.setObjectName("pushButtonOK")
        self.gridLayout_2.addWidget(self.pushButtonOK, 1, 1, 1, 1)

        self.retranslateUi(Abgangsdatum)
        QtCore.QMetaObject.connectSlotsByName(Abgangsdatum)

    def retranslateUi(self, Abgangsdatum):
        _translate = QtCore.QCoreApplication.translate
        Abgangsdatum.setWindowTitle(_translate("Abgangsdatum", "Abgangs-/Wechseldatum"))
        self.label.setText(_translate("Abgangsdatum", "Abgangs-/Wechseldatum setzten für:"))
        self.labelSname.setText(_translate("Abgangsdatum", "Vorname, Nachname"))
        self.pushButtonOK.setText(_translate("Abgangsdatum", "OK"))


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    Abgangsdatum = QtWidgets.QDialog()
    ui = Ui_Abgangsdatum()
    ui.setupUi(Abgangsdatum)
    Abgangsdatum.show()
    sys.exit(app.exec_())
