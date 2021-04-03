# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file '.\pdfdialog.ui'
#
# Created by: PyQt5 UI code generator 5.15.1
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_PdfExportieren(object):
    def setupUi(self, PdfExportieren):
        PdfExportieren.setObjectName("PdfExportieren")
        PdfExportieren.setWindowModality(QtCore.Qt.ApplicationModal)
        PdfExportieren.resize(358, 203)
        PdfExportieren.setMinimumSize(QtCore.QSize(304, 184))
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(".\\kursbuch.ico"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        PdfExportieren.setWindowIcon(icon)
        self.gridLayout_2 = QtWidgets.QGridLayout(PdfExportieren)
        self.gridLayout_2.setObjectName("gridLayout_2")
        self.gridLayout = QtWidgets.QGridLayout()
        self.gridLayout.setContentsMargins(20, 6, 20, -1)
        self.gridLayout.setObjectName("gridLayout")
        self.radioButtonMitFs = QtWidgets.QRadioButton(PdfExportieren)
        self.radioButtonMitFs.setChecked(True)
        self.radioButtonMitFs.setObjectName("radioButtonMitFs")
        self.gridLayout.addWidget(self.radioButtonMitFs, 2, 0, 1, 1)
        self.radioButtonOhneFS = QtWidgets.QRadioButton(PdfExportieren)
        self.radioButtonOhneFS.setObjectName("radioButtonOhneFS")
        self.gridLayout.addWidget(self.radioButtonOhneFS, 3, 0, 1, 1)
        self.label_2 = QtWidgets.QLabel(PdfExportieren)
        font = QtGui.QFont()
        font.setBold(True)
        font.setItalic(False)
        font.setWeight(75)
        self.label_2.setFont(font)
        self.label_2.setWordWrap(True)
        self.label_2.setObjectName("label_2")
        self.gridLayout.addWidget(self.label_2, 0, 0, 1, 1)
        self.gridLayout_2.addLayout(self.gridLayout, 1, 0, 1, 1)
        self.label = QtWidgets.QLabel(PdfExportieren)
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
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setContentsMargins(-1, 10, -1, -1)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.pushButtonExport = QtWidgets.QPushButton(PdfExportieren)
        self.pushButtonExport.setDefault(True)
        self.pushButtonExport.setObjectName("pushButtonExport")
        self.horizontalLayout.addWidget(self.pushButtonExport)
        self.pushButtonAbbrechen = QtWidgets.QPushButton(PdfExportieren)
        self.pushButtonAbbrechen.setObjectName("pushButtonAbbrechen")
        self.horizontalLayout.addWidget(self.pushButtonAbbrechen)
        self.gridLayout_2.addLayout(self.horizontalLayout, 3, 0, 1, 1)

        self.retranslateUi(PdfExportieren)
        QtCore.QMetaObject.connectSlotsByName(PdfExportieren)
        PdfExportieren.setTabOrder(self.pushButtonExport, self.pushButtonAbbrechen)

    def retranslateUi(self, PdfExportieren):
        _translate = QtCore.QCoreApplication.translate
        PdfExportieren.setWindowTitle(_translate("PdfExportieren", "PDF Export"))
        self.radioButtonMitFs.setText(_translate("PdfExportieren", "mit Fehlzeiten (wenn verfügbar)"))
        self.radioButtonOhneFS.setText(_translate("PdfExportieren", "ohne Fehlzeiten (Übersicht für Schüler*innen)"))
        self.label_2.setText(_translate("PdfExportieren", "Das aktuelle Kursbuch zum Druck oder zur Übersicht exportieren:"))
        self.label.setText(_translate("PdfExportieren", "PDF exportieren"))
        self.pushButtonExport.setText(_translate("PdfExportieren", "Exportieren und öffnen"))
        self.pushButtonAbbrechen.setText(_translate("PdfExportieren", "Abbrechen"))


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    PdfExportieren = QtWidgets.QWidget()
    ui = Ui_PdfExportieren()
    ui.setupUi(PdfExportieren)
    PdfExportieren.show()
    sys.exit(app.exec_())
