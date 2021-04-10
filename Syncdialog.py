# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file '.\Syncdialog.ui'
#
# Created by: PyQt5 UI code generator 5.15.1
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_Syncdialog(object):
    def setupUi(self, Syncdialog):
        Syncdialog.setObjectName("Syncdialog")
        Syncdialog.setWindowModality(QtCore.Qt.ApplicationModal)
        Syncdialog.resize(449, 249)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(Syncdialog.sizePolicy().hasHeightForWidth())
        Syncdialog.setSizePolicy(sizePolicy)
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(".\\kursbuch.ico"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        Syncdialog.setWindowIcon(icon)
        self.gridLayout_5 = QtWidgets.QGridLayout(Syncdialog)
        self.gridLayout_5.setObjectName("gridLayout_5")
        self.label = QtWidgets.QLabel(Syncdialog)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label.sizePolicy().hasHeightForWidth())
        self.label.setSizePolicy(sizePolicy)
        font = QtGui.QFont()
        font.setPointSize(10)
        font.setBold(True)
        font.setWeight(75)
        self.label.setFont(font)
        self.label.setStyleSheet("background-color: rgb(255, 255, 255);")
        self.label.setAlignment(QtCore.Qt.AlignCenter)
        self.label.setWordWrap(True)
        self.label.setObjectName("label")
        self.gridLayout_5.addWidget(self.label, 0, 0, 1, 2)
        self.frame = QtWidgets.QFrame(Syncdialog)
        self.frame.setStyleSheet("background-color: rgb(211, 211, 211);")
        self.frame.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame.setObjectName("frame")
        self.gridLayout_4 = QtWidgets.QGridLayout(self.frame)
        self.gridLayout_4.setObjectName("gridLayout_4")
        self.gridLayout_2 = QtWidgets.QGridLayout()
        self.gridLayout_2.setObjectName("gridLayout_2")
        self.label_4 = QtWidgets.QLabel(self.frame)
        self.label_4.setAlignment(QtCore.Qt.AlignLeading|QtCore.Qt.AlignLeft|QtCore.Qt.AlignVCenter)
        self.label_4.setWordWrap(True)
        self.label_4.setObjectName("label_4")
        self.gridLayout_2.addWidget(self.label_4, 0, 0, 1, 1)
        self.label_5 = QtWidgets.QLabel(self.frame)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label_5.sizePolicy().hasHeightForWidth())
        self.label_5.setSizePolicy(sizePolicy)
        self.label_5.setMinimumSize(QtCore.QSize(0, 30))
        font = QtGui.QFont()
        font.setBold(True)
        font.setWeight(75)
        self.label_5.setFont(font)
        self.label_5.setAlignment(QtCore.Qt.AlignLeading|QtCore.Qt.AlignLeft|QtCore.Qt.AlignTop)
        self.label_5.setWordWrap(True)
        self.label_5.setObjectName("label_5")
        self.gridLayout_2.addWidget(self.label_5, 1, 0, 1, 1)
        self.gridLayout_4.addLayout(self.gridLayout_2, 0, 0, 1, 1)
        self.gridLayout_5.addWidget(self.frame, 1, 0, 1, 2)
        self.gridLayout = QtWidgets.QGridLayout()
        self.gridLayout.setObjectName("gridLayout")
        self.pushButtonUebernehmen = QtWidgets.QPushButton(Syncdialog)
        self.pushButtonUebernehmen.setObjectName("pushButtonUebernehmen")
        self.gridLayout.addWidget(self.pushButtonUebernehmen, 0, 0, 1, 1)
        self.pushButtonAbbrechen = QtWidgets.QPushButton(Syncdialog)
        self.pushButtonAbbrechen.setObjectName("pushButtonAbbrechen")
        self.gridLayout.addWidget(self.pushButtonAbbrechen, 0, 1, 1, 1)
        self.gridLayout_5.addLayout(self.gridLayout, 3, 1, 1, 1)
        self.gridLayout_3 = QtWidgets.QGridLayout()
        self.gridLayout_3.setObjectName("gridLayout_3")
        self.label_2 = QtWidgets.QLabel(Syncdialog)
        self.label_2.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.label_2.setObjectName("label_2")
        self.gridLayout_3.addWidget(self.label_2, 0, 0, 1, 1)
        self.lineEditFTPS = QtWidgets.QLineEdit(Syncdialog)
        self.lineEditFTPS.setObjectName("lineEditFTPS")
        self.gridLayout_3.addWidget(self.lineEditFTPS, 0, 1, 1, 1)
        self.label_3 = QtWidgets.QLabel(Syncdialog)
        self.label_3.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.label_3.setObjectName("label_3")
        self.gridLayout_3.addWidget(self.label_3, 1, 0, 1, 1)
        self.lineEditPW = QtWidgets.QLineEdit(Syncdialog)
        self.lineEditPW.setEchoMode(QtWidgets.QLineEdit.Password)
        self.lineEditPW.setObjectName("lineEditPW")
        self.gridLayout_3.addWidget(self.lineEditPW, 1, 1, 1, 1)
        self.checkBoxSync = QtWidgets.QCheckBox(Syncdialog)
        self.checkBoxSync.setObjectName("checkBoxSync")
        self.gridLayout_3.addWidget(self.checkBoxSync, 2, 1, 1, 1)
        self.gridLayout_5.addLayout(self.gridLayout_3, 2, 0, 1, 2)

        self.retranslateUi(Syncdialog)
        QtCore.QMetaObject.connectSlotsByName(Syncdialog)
        Syncdialog.setTabOrder(self.lineEditFTPS, self.lineEditPW)
        Syncdialog.setTabOrder(self.lineEditPW, self.checkBoxSync)

    def retranslateUi(self, Syncdialog):
        _translate = QtCore.QCoreApplication.translate
        Syncdialog.setWindowTitle(_translate("Syncdialog", "Synchronisation"))
        self.label.setText(_translate("Syncdialog", "Synchronisation einrichten"))
        self.label_4.setText(_translate("Syncdialog", "Bei der ersten Einrichtung wird die lokale Datenbank auf den Server geladen."))
        self.label_5.setText(_translate("Syncdialog", "Wenn bereits eine Datenbank auf den Server hochgeladen wurde, wird die lokale Version durch die Serverversion ersetzt."))
        self.pushButtonUebernehmen.setText(_translate("Syncdialog", "Übernehmen"))
        self.pushButtonAbbrechen.setText(_translate("Syncdialog", "Abbrechen"))
        self.label_2.setText(_translate("Syncdialog", "FTPS-Server-Domain:"))
        self.label_3.setText(_translate("Syncdialog", "Passwort:"))
        self.checkBoxSync.setText(_translate("Syncdialog", "Synchronisation aktivieren"))


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    Syncdialog = QtWidgets.QDialog()
    ui = Ui_Syncdialog()
    ui.setupUi(Syncdialog)
    Syncdialog.show()
    sys.exit(app.exec_())
