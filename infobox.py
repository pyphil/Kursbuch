# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file '.\infobox.ui'
#
# Created by: PyQt5 UI code generator 5.15.1
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_Infobox(object):
    def setupUi(self, Infobox):
        Infobox.setObjectName("Infobox")
        Infobox.setWindowModality(QtCore.Qt.ApplicationModal)
        Infobox.resize(462, 38)
        Infobox.setStyleSheet("background-color: rgb(255, 255, 191);")
        self.labelInfo = QtWidgets.QLabel(Infobox)
        self.labelInfo.setGeometry(QtCore.QRect(10, 10, 441, 20))
        self.labelInfo.setStyleSheet("color: rgb(0, 0, 0);")
        self.labelInfo.setAlignment(QtCore.Qt.AlignCenter)
        self.labelInfo.setObjectName("labelInfo")

        self.retranslateUi(Infobox)
        QtCore.QMetaObject.connectSlotsByName(Infobox)

    def retranslateUi(self, Infobox):
        _translate = QtCore.QCoreApplication.translate
        Infobox.setWindowTitle(_translate("Infobox", "Infobox"))
        self.labelInfo.setText(_translate("Infobox", "TextLabel"))


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    Infobox = QtWidgets.QDialog()
    ui = Ui_Infobox()
    ui.setupUi(Infobox)
    Infobox.show()
    sys.exit(app.exec_())
