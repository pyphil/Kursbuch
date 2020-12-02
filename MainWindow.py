# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file '.\MainWindow.ui'
#
# Created by: PyQt5 UI code generator 5.15.1
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(1032, 681)
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(".\\kursbuch.ico"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        MainWindow.setWindowIcon(icon)
        MainWindow.setTabShape(QtWidgets.QTabWidget.Rounded)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.gridLayout_2 = QtWidgets.QGridLayout(self.centralwidget)
        self.gridLayout_2.setObjectName("gridLayout_2")
        self.comboBoxKurs = QtWidgets.QComboBox(self.centralwidget)
        self.comboBoxKurs.setStyleSheet("selection-background-color: rgb(85, 170, 255);")
        self.comboBoxKurs.setObjectName("comboBoxKurs")
        self.gridLayout_2.addWidget(self.comboBoxKurs, 0, 0, 1, 1)
        self.tabWidget = QtWidgets.QTabWidget(self.centralwidget)
        self.tabWidget.setObjectName("tabWidget")
        self.tab_Unterricht = QtWidgets.QWidget()
        self.tab_Unterricht.setObjectName("tab_Unterricht")
        self.gridLayout = QtWidgets.QGridLayout(self.tab_Unterricht)
        self.gridLayout.setObjectName("gridLayout")
        self.labelKurshefteintrag = QtWidgets.QLabel(self.tab_Unterricht)
        self.labelKurshefteintrag.setObjectName("labelKurshefteintrag")
        self.gridLayout.addWidget(self.labelKurshefteintrag, 0, 0, 1, 1)
        self.labelHausaufgaben = QtWidgets.QLabel(self.tab_Unterricht)
        self.labelHausaufgaben.setObjectName("labelHausaufgaben")
        self.gridLayout.addWidget(self.labelHausaufgaben, 0, 2, 1, 1)
        self.textEditKurshefteintrag = QtWidgets.QTextEdit(self.tab_Unterricht)
        self.textEditKurshefteintrag.setEnabled(False)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.textEditKurshefteintrag.sizePolicy().hasHeightForWidth())
        self.textEditKurshefteintrag.setSizePolicy(sizePolicy)
        self.textEditKurshefteintrag.setMaximumSize(QtCore.QSize(16777215, 144))
        self.textEditKurshefteintrag.setObjectName("textEditKurshefteintrag")
        self.gridLayout.addWidget(self.textEditKurshefteintrag, 1, 0, 1, 2)
        self.textEditHausaufgaben = QtWidgets.QTextEdit(self.tab_Unterricht)
        self.textEditHausaufgaben.setEnabled(False)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.textEditHausaufgaben.sizePolicy().hasHeightForWidth())
        self.textEditHausaufgaben.setSizePolicy(sizePolicy)
        self.textEditHausaufgaben.setMaximumSize(QtCore.QSize(16777215, 144))
        self.textEditHausaufgaben.setSizeIncrement(QtCore.QSize(0, 0))
        self.textEditHausaufgaben.setBaseSize(QtCore.QSize(0, 0))
        self.textEditHausaufgaben.setObjectName("textEditHausaufgaben")
        self.gridLayout.addWidget(self.textEditHausaufgaben, 1, 2, 1, 1)
        self.horizontalLayout_3 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_3.setObjectName("horizontalLayout_3")
        self.checkBox = QtWidgets.QCheckBox(self.tab_Unterricht)
        self.checkBox.setEnabled(False)
        self.checkBox.setObjectName("checkBox")
        self.horizontalLayout_3.addWidget(self.checkBox)
        self.checkBox_2 = QtWidgets.QCheckBox(self.tab_Unterricht)
        self.checkBox_2.setEnabled(False)
        self.checkBox_2.setObjectName("checkBox_2")
        self.horizontalLayout_3.addWidget(self.checkBox_2)
        self.gridLayout.addLayout(self.horizontalLayout_3, 2, 0, 1, 1)
        spacerItem = QtWidgets.QSpacerItem(506, 22, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.gridLayout.addItem(spacerItem, 2, 1, 1, 2)
        self.label = QtWidgets.QLabel(self.tab_Unterricht)
        self.label.setObjectName("label")
        self.gridLayout.addWidget(self.label, 4, 0, 1, 1)
        self.textEdit = QtWidgets.QTextEdit(self.tab_Unterricht)
        self.textEdit.setEnabled(False)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.textEdit.sizePolicy().hasHeightForWidth())
        self.textEdit.setSizePolicy(sizePolicy)
        self.textEdit.setObjectName("textEdit")
        self.gridLayout.addWidget(self.textEdit, 5, 0, 1, 3)
        spacerItem1 = QtWidgets.QSpacerItem(511, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.gridLayout.addItem(spacerItem1, 3, 0, 1, 3)
        self.tabWidget.addTab(self.tab_Unterricht, "")
        self.tab_Fehlzeiten = QtWidgets.QWidget()
        self.tab_Fehlzeiten.setObjectName("tab_Fehlzeiten")
        self.frameFehlzTitel = QtWidgets.QFrame(self.tab_Fehlzeiten)
        self.frameFehlzTitel.setGeometry(QtCore.QRect(160, 0, 511, 31))
        self.frameFehlzTitel.setFrameShape(QtWidgets.QFrame.NoFrame)
        self.frameFehlzTitel.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frameFehlzTitel.setObjectName("frameFehlzTitel")
        self.labelName = QtWidgets.QLabel(self.frameFehlzTitel)
        self.labelName.setGeometry(QtCore.QRect(20, 10, 89, 13))
        font = QtGui.QFont()
        font.setBold(True)
        font.setWeight(75)
        self.labelName.setFont(font)
        self.labelName.setObjectName("labelName")
        self.label_eFs = QtWidgets.QLabel(self.frameFehlzTitel)
        self.label_eFs.setGeometry(QtCore.QRect(300, 10, 19, 13))
        font = QtGui.QFont()
        font.setBold(True)
        font.setWeight(75)
        self.label_eFs.setFont(font)
        self.label_eFs.setObjectName("label_eFs")
        self.label_uFs = QtWidgets.QLabel(self.frameFehlzTitel)
        self.label_uFs.setGeometry(QtCore.QRect(250, 10, 19, 13))
        font = QtGui.QFont()
        font.setBold(True)
        font.setWeight(75)
        self.label_uFs.setFont(font)
        self.label_uFs.setObjectName("label_uFs")
        self.label_anw = QtWidgets.QLabel(self.frameFehlzTitel)
        self.label_anw.setGeometry(QtCore.QRect(200, 10, 26, 13))
        font = QtGui.QFont()
        font.setBold(True)
        font.setWeight(75)
        self.label_anw.setFont(font)
        self.label_anw.setObjectName("label_anw")
        self.label_Schulv = QtWidgets.QLabel(self.frameFehlzTitel)
        self.label_Schulv.setGeometry(QtCore.QRect(350, 10, 40, 13))
        font = QtGui.QFont()
        font.setBold(True)
        font.setWeight(75)
        self.label_Schulv.setFont(font)
        self.label_Schulv.setObjectName("label_Schulv")
        self.label_Schulv_2 = QtWidgets.QLabel(self.frameFehlzTitel)
        self.label_Schulv_2.setGeometry(QtCore.QRect(400, 10, 67, 13))
        font = QtGui.QFont()
        font.setBold(True)
        font.setWeight(75)
        self.label_Schulv_2.setFont(font)
        self.label_Schulv_2.setObjectName("label_Schulv_2")
        self.verticalLayoutWidget = QtWidgets.QWidget(self.tab_Fehlzeiten)
        self.verticalLayoutWidget.setGeometry(QtCore.QRect(160, 30, 511, 531))
        self.verticalLayoutWidget.setObjectName("verticalLayoutWidget")
        self.verticalLayoutFehlzeiten = QtWidgets.QVBoxLayout(self.verticalLayoutWidget)
        self.verticalLayoutFehlzeiten.setContentsMargins(0, 0, 0, 0)
        self.verticalLayoutFehlzeiten.setSpacing(0)
        self.verticalLayoutFehlzeiten.setObjectName("verticalLayoutFehlzeiten")
        self.tabWidget.addTab(self.tab_Fehlzeiten, "")
        self.gridLayout_2.addWidget(self.tabWidget, 1, 1, 2, 1)
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.pushButtonNeuerKurs = QtWidgets.QPushButton(self.centralwidget)
        self.pushButtonNeuerKurs.setObjectName("pushButtonNeuerKurs")
        self.horizontalLayout.addWidget(self.pushButtonNeuerKurs)
        self.pushButtonDelKurs = QtWidgets.QPushButton(self.centralwidget)
        self.pushButtonDelKurs.setEnabled(False)
        self.pushButtonDelKurs.setObjectName("pushButtonDelKurs")
        self.horizontalLayout.addWidget(self.pushButtonDelKurs)
        self.pushButtonKursmitglieder = QtWidgets.QPushButton(self.centralwidget)
        self.pushButtonKursmitglieder.setEnabled(False)
        self.pushButtonKursmitglieder.setObjectName("pushButtonKursmitglieder")
        self.horizontalLayout.addWidget(self.pushButtonKursmitglieder)
        self.pushButtonNeueStd = QtWidgets.QPushButton(self.centralwidget)
        self.pushButtonNeueStd.setEnabled(False)
        self.pushButtonNeueStd.setObjectName("pushButtonNeueStd")
        self.horizontalLayout.addWidget(self.pushButtonNeueStd)
        self.pushButtonDelStd = QtWidgets.QPushButton(self.centralwidget)
        self.pushButtonDelStd.setEnabled(False)
        self.pushButtonDelStd.setObjectName("pushButtonDelStd")
        self.horizontalLayout.addWidget(self.pushButtonDelStd)
        self.pushButtonKursheftAnzeigen = QtWidgets.QPushButton(self.centralwidget)
        self.pushButtonKursheftAnzeigen.setEnabled(False)
        self.pushButtonKursheftAnzeigen.setObjectName("pushButtonKursheftAnzeigen")
        self.horizontalLayout.addWidget(self.pushButtonKursheftAnzeigen)
        self.gridLayout_2.addLayout(self.horizontalLayout, 0, 1, 1, 1)
        self.tableWidget = QtWidgets.QTableWidget(self.centralwidget)
        self.tableWidget.setMinimumSize(QtCore.QSize(245, 0))
        self.tableWidget.setMaximumSize(QtCore.QSize(245, 16777215))
        self.tableWidget.setStyleSheet("selection-background-color: rgb(85, 170, 255);\n"
"selection-color: rgb(255, 255, 255);")
        self.tableWidget.setEditTriggers(QtWidgets.QAbstractItemView.NoEditTriggers)
        self.tableWidget.setSelectionMode(QtWidgets.QAbstractItemView.SingleSelection)
        self.tableWidget.setSelectionBehavior(QtWidgets.QAbstractItemView.SelectRows)
        self.tableWidget.setObjectName("tableWidget")
        self.tableWidget.setColumnCount(2)
        self.tableWidget.setRowCount(0)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget.setHorizontalHeaderItem(0, item)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget.setHorizontalHeaderItem(1, item)
        self.tableWidget.horizontalHeader().setDefaultSectionSize(50)
        self.tableWidget.horizontalHeader().setMinimumSectionSize(50)
        self.tableWidget.horizontalHeader().setStretchLastSection(True)
        self.tableWidget.verticalHeader().setVisible(False)
        self.tableWidget.verticalHeader().setDefaultSectionSize(20)
        self.tableWidget.verticalHeader().setMinimumSectionSize(20)
        self.gridLayout_2.addWidget(self.tableWidget, 1, 0, 1, 1)
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 1032, 21))
        self.menubar.setObjectName("menubar")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)
        self.tabWidget.setCurrentIndex(0)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "Kursbuch von"))
        self.comboBoxKurs.setPlaceholderText(_translate("MainWindow", "Kursauswahl"))
        self.labelKurshefteintrag.setText(_translate("MainWindow", "Kurshefteintrag"))
        self.labelHausaufgaben.setText(_translate("MainWindow", "Hausaufgaben/Lernzeitaufgaben"))
        self.checkBox.setText(_translate("MainWindow", "Ferien/Feiertag"))
        self.checkBox_2.setText(_translate("MainWindow", "Kompensationsstunde"))
        self.label.setText(_translate("MainWindow", "Planungsnotizen"))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab_Unterricht), _translate("MainWindow", "Unterricht"))
        self.labelName.setText(_translate("MainWindow", "Name, Vorname"))
        self.label_eFs.setText(_translate("MainWindow", "eFs"))
        self.label_uFs.setText(_translate("MainWindow", "uFs"))
        self.label_anw.setText(_translate("MainWindow", "anw."))
        self.label_Schulv.setText(_translate("MainWindow", "Schulv."))
        self.label_Schulv_2.setText(_translate("MainWindow", "Quarantäne"))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab_Fehlzeiten), _translate("MainWindow", "Fehlzeiten"))
        self.pushButtonNeuerKurs.setText(_translate("MainWindow", "Neuen Kurs anlegen"))
        self.pushButtonDelKurs.setText(_translate("MainWindow", "Kurs löschen"))
        self.pushButtonKursmitglieder.setText(_translate("MainWindow", "Kursmitglieder"))
        self.pushButtonNeueStd.setText(_translate("MainWindow", "Neue Stunde"))
        self.pushButtonDelStd.setText(_translate("MainWindow", "Stunde löschen"))
        self.pushButtonKursheftAnzeigen.setText(_translate("MainWindow", "Kursheft anzeigen"))
        self.tableWidget.setSortingEnabled(False)
        item = self.tableWidget.horizontalHeaderItem(0)
        item.setText(_translate("MainWindow", "Datum"))
        item = self.tableWidget.horizontalHeaderItem(1)
        item.setText(_translate("MainWindow", "Stunde"))


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())
