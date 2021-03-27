# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file '.\KursAnlegen.ui'
#
# Created by: PyQt5 UI code generator 5.15.1
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_KursAnlegen(object):
    def setupUi(self, KursAnlegen):
        KursAnlegen.setObjectName("KursAnlegen")
        KursAnlegen.setWindowModality(QtCore.Qt.ApplicationModal)
        KursAnlegen.resize(270, 176)
        KursAnlegen.setMinimumSize(QtCore.QSize(270, 176))
        KursAnlegen.setMaximumSize(QtCore.QSize(270, 176))
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(".\\kursbuch.ico"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        KursAnlegen.setWindowIcon(icon)
        self.gridLayout_2 = QtWidgets.QGridLayout(KursAnlegen)
        self.gridLayout_2.setObjectName("gridLayout_2")
        self.label = QtWidgets.QLabel(KursAnlegen)
        self.label.setMaximumSize(QtCore.QSize(16777215, 31))
        font = QtGui.QFont()
        font.setPointSize(10)
        font.setBold(True)
        font.setWeight(75)
        self.label.setFont(font)
        self.label.setStyleSheet("background-color: rgb(255, 255, 255);")
        self.label.setAlignment(QtCore.Qt.AlignCenter)
        self.label.setObjectName("label")
        self.gridLayout_2.addWidget(self.label, 0, 0, 1, 1)
        self.gridLayout = QtWidgets.QGridLayout()
        self.gridLayout.setContentsMargins(-1, 6, -1, -1)
        self.gridLayout.setObjectName("gridLayout")
        self.label_2 = QtWidgets.QLabel(KursAnlegen)
        self.label_2.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.label_2.setObjectName("label_2")
        self.gridLayout.addWidget(self.label_2, 0, 0, 1, 1)
        self.lineEditKlasse = QtWidgets.QLineEdit(KursAnlegen)
        self.lineEditKlasse.setObjectName("lineEditKlasse")
        self.gridLayout.addWidget(self.lineEditKlasse, 2, 1, 1, 1)
        self.label_3 = QtWidgets.QLabel(KursAnlegen)
        self.label_3.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.label_3.setObjectName("label_3")
        self.gridLayout.addWidget(self.label_3, 1, 0, 1, 1)
        self.label_4 = QtWidgets.QLabel(KursAnlegen)
        self.label_4.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.label_4.setObjectName("label_4")
        self.gridLayout.addWidget(self.label_4, 2, 0, 1, 1)
        self.lineEditFachkrzl = QtWidgets.QLineEdit(KursAnlegen)
        self.lineEditFachkrzl.setObjectName("lineEditFachkrzl")
        self.gridLayout.addWidget(self.lineEditFachkrzl, 1, 1, 1, 1)
        self.comboBoxSchuljahr = QtWidgets.QComboBox(KursAnlegen)
        self.comboBoxSchuljahr.setObjectName("comboBoxSchuljahr")
        self.gridLayout.addWidget(self.comboBoxSchuljahr, 0, 1, 1, 1)
        self.gridLayout_2.addLayout(self.gridLayout, 1, 0, 1, 1)
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setContentsMargins(-1, 10, -1, -1)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.pushButtonAnlegen = QtWidgets.QPushButton(KursAnlegen)
        self.pushButtonAnlegen.setDefault(True)
        self.pushButtonAnlegen.setObjectName("pushButtonAnlegen")
        self.horizontalLayout.addWidget(self.pushButtonAnlegen)
        self.pushButtonAbbrechen = QtWidgets.QPushButton(KursAnlegen)
        self.pushButtonAbbrechen.setObjectName("pushButtonAbbrechen")
        self.horizontalLayout.addWidget(self.pushButtonAbbrechen)
        self.gridLayout_2.addLayout(self.horizontalLayout, 2, 0, 1, 1)

        self.retranslateUi(KursAnlegen)
        QtCore.QMetaObject.connectSlotsByName(KursAnlegen)
        KursAnlegen.setTabOrder(self.comboBoxSchuljahr, self.lineEditFachkrzl)
        KursAnlegen.setTabOrder(self.lineEditFachkrzl, self.lineEditKlasse)
        KursAnlegen.setTabOrder(self.lineEditKlasse, self.pushButtonAnlegen)
        KursAnlegen.setTabOrder(self.pushButtonAnlegen, self.pushButtonAbbrechen)

    def retranslateUi(self, KursAnlegen):
        _translate = QtCore.QCoreApplication.translate
        KursAnlegen.setWindowTitle(_translate("KursAnlegen", "Kurs anlegen"))
        self.label.setText(_translate("KursAnlegen", "Neuen Kurs anlegen"))
        self.label_2.setText(_translate("KursAnlegen", "Schuljahr:"))
        self.label_3.setText(_translate("KursAnlegen", "Fachkürzel:"))
        self.label_4.setText(_translate("KursAnlegen", "Klasse/Kurs:"))
        self.pushButtonAnlegen.setText(_translate("KursAnlegen", "Anlegen"))
        self.pushButtonAbbrechen.setText(_translate("KursAnlegen", "Abbrechen"))


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    KursAnlegen = QtWidgets.QWidget()
    ui = Ui_KursAnlegen()
    ui.setupUi(KursAnlegen)
    KursAnlegen.show()
    sys.exit(app.exec_())