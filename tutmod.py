
from calendar import Calendar
from datetime import date, timedelta, datetime
# from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5 import QtCore, QtWidgets
from Tutmodgui import Ui_Tutmodgui
import locale
import reportFehlz
from BlockGui import Ui_BlockKomp

locale.setlocale(locale.LC_ALL, 'deu_deu')


class Tutmod(Ui_Tutmodgui, QtWidgets.QDialog):
    def __init__(self, db, gui):
        super(Tutmod, self).__init__(gui.MainWindow)
        self.setupUi(self)
        self.show()

        self.db = db
        self.gui = gui

        klassen = ["5a", "5b", "5c", "5d", "5e",
                   "6a", "6b", "6c", "6d", "6e",
                   "7a", "7b", "7c", "7d", "7e",
                   "8a", "8b", "8c", "8d", "8e",
                   "9a", "9b", "9c", "9d", "9e",
                   "10a", "10b", "10c", "10d", "10e",
                   "EF", "Q1", "Q2"]
        self.comboBoxKlasse.addItems(klassen)
        # let non editable combobox in fusion style still respect maxitems
        self.comboBoxKlasse.setStyleSheet("combobox-popup: 0;")

        self.set_cur_year_month()
        self.setMonth(True)
        self.tableWidget.setColumnWidth(0, 180)

        self.comboBoxKlasse.activated.connect(self.zeigeKlasse)
        self.comboBoxMonat.activated.connect(self.setMonth)
        self.dateEditJahr.dateChanged.connect(self.setMonth)
        self.pushButtonWeekafter.clicked.connect(self.weekafter)
        self.pushButtonWeekbefore.clicked.connect(self.weekbefore)
        self.tableWidget.clicked.connect(self.set_fehlzeiten)
        self.dateEdit.dateChanged.connect(self.countfz)
        self.dateEdit_2.dateChanged.connect(self.countfz)
        self.dateEdit_3.dateChanged.connect(self.countfz)
        self.dateEdit_4.dateChanged.connect(self.countfz)
        self.pushButtonListeKlasse_1.clicked.connect(self.getKlassenFehlz_1)
        self.pushButtonListeKlasse_2.clicked.connect(self.getKlassenFehlz_2)
        self.pushButtonBlock.clicked.connect(self.block)

        self.button1_1.clicked.connect(self.set1_1)
        self.button1_2.clicked.connect(self.set1_2)
        self.button1_3.clicked.connect(self.set1_3)
        self.button1_4.clicked.connect(self.set1_4)
        self.button1_5.clicked.connect(self.set1_5)

        self.button2_1.clicked.connect(self.set2_1)
        self.button2_2.clicked.connect(self.set2_2)
        self.button2_3.clicked.connect(self.set2_3)
        self.button2_4.clicked.connect(self.set2_4)
        self.button2_5.clicked.connect(self.set2_5)

        self.button3_1.clicked.connect(self.set3_1)
        self.button3_2.clicked.connect(self.set3_2)
        self.button3_3.clicked.connect(self.set3_3)
        self.button3_4.clicked.connect(self.set3_4)
        self.button3_5.clicked.connect(self.set3_5)

        self.button4_1.clicked.connect(self.set4_1)
        self.button4_2.clicked.connect(self.set4_2)
        self.button4_3.clicked.connect(self.set4_3)
        self.button4_4.clicked.connect(self.set4_4)
        self.button4_5.clicked.connect(self.set4_5)

        self.button5_1.clicked.connect(self.set5_1)
        self.button5_2.clicked.connect(self.set5_2)
        self.button5_3.clicked.connect(self.set5_3)
        self.button5_4.clicked.connect(self.set5_4)
        self.button5_5.clicked.connect(self.set5_5)

        self.button6_1.clicked.connect(self.set6_1)
        self.button6_2.clicked.connect(self.set6_2)
        self.button6_3.clicked.connect(self.set6_3)
        self.button6_4.clicked.connect(self.set6_4)
        self.button6_5.clicked.connect(self.set6_5)

        self.button7_1.clicked.connect(self.set7_1)
        self.button7_2.clicked.connect(self.set7_2)
        self.button7_3.clicked.connect(self.set7_3)
        self.button7_4.clicked.connect(self.set7_4)
        self.button7_5.clicked.connect(self.set7_5)

        self.disableButtons()

    def disableButtons(self):
        self.comboBoxMonat.setEnabled(False)
        self.dateEditJahr.setEnabled(False)
        self.pushButtonWeekafter.setEnabled(False)
        self.pushButtonWeekbefore.setEnabled(False)
        self.pushButtonListeKlasse_1.setEnabled(False)
        self.pushButtonListeKlasse_2.setEnabled(False)
        self.pushButtonBlock.setEnabled(False)
        self.dateEdit.setEnabled(False)
        self.dateEdit_2.setEnabled(False)
        self.dateEdit_3.setEnabled(False)
        self.dateEdit_4.setEnabled(False)

    def enableButtons(self):
        self.comboBoxMonat.setEnabled(True)
        self.dateEditJahr.setEnabled(True)
        self.pushButtonWeekafter.setEnabled(True)
        self.pushButtonWeekbefore.setEnabled(True)
        self.pushButtonListeKlasse_1.setEnabled(True)
        self.pushButtonListeKlasse_2.setEnabled(True)
        self.pushButtonBlock.setEnabled(True)
        self.dateEdit.setEnabled(True)
        self.dateEdit_2.setEnabled(True)
        self.dateEdit_3.setEnabled(True)
        self.dateEdit_4.setEnabled(True)

        self.button1_1.setEnabled(True)
        self.button1_2.setEnabled(True)
        self.button1_3.setEnabled(True)
        self.button1_4.setEnabled(True)
        self.button1_5.setEnabled(True)

        self.button2_1.setEnabled(True)
        self.button2_2.setEnabled(True)
        self.button2_3.setEnabled(True)
        self.button2_4.setEnabled(True)
        self.button2_5.setEnabled(True)

        self.button3_1.setEnabled(True)
        self.button3_2.setEnabled(True)
        self.button3_3.setEnabled(True)
        self.button3_4.setEnabled(True)
        self.button3_5.setEnabled(True)

        self.button4_1.setEnabled(True)
        self.button4_2.setEnabled(True)
        self.button4_3.setEnabled(True)
        self.button4_4.setEnabled(True)
        self.button4_5.setEnabled(True)

        self.button5_1.setEnabled(True)
        self.button5_2.setEnabled(True)
        self.button5_3.setEnabled(True)
        self.button5_4.setEnabled(True)
        self.button5_5.setEnabled(True)

        self.button6_1.setEnabled(True)
        self.button6_2.setEnabled(True)
        self.button6_3.setEnabled(True)
        self.button6_4.setEnabled(True)
        self.button6_5.setEnabled(True)

        self.button7_1.setEnabled(True)
        self.button7_2.setEnabled(True)
        self.button7_3.setEnabled(True)
        self.button7_4.setEnabled(True)
        self.button7_5.setEnabled(True)

    def zeigeKlasse(self):
        """ Zeigt die Liste der Schüler der ausgewählten Klasse """

        # Buttons zunächst deaktivieren
        self.disableButtons()

        # gefilterte Liste bei jedem Aufruf leer bereitstellen
        self.filtered = []

        # ausgewählte Klasse
        self.klasse = self.comboBoxKlasse.currentText()

        # Filtern nach Klasse
        alle = self.db.getGesamtliste()
        z = 0
        for i in alle:
            if i[3] == self.klasse:
                self.filtered.append([i[1], i[2], i[0], i[3]])
                z += 1
        # Sortiertung nach Nachname
        self.filtered = sorted(
            self.filtered, key=lambda i: locale.strxfrm(i[0]))

        # Ausgabe in TableWidget
        z = 0
        for i in self.filtered:
            self.tableWidget.setRowCount(z+1)
            self.tableWidget.setItem(
                z, 0, QtWidgets.QTableWidgetItem(i[0]+", "+i[1]))
            self.tableWidget.setItem(z, 1, QtWidgets.QTableWidgetItem(i[3]))
            z += 1

    def set_cur_year_month(self):
        self.dateEditJahr.setDate(QtCore.QDate(date.today().year, 1, 1))
        self.comboBoxMonat.setCurrentText(datetime.now().strftime("%B"))

    def fillTableWidget(self):
        """ füllt die Schülernamen der gewählten Klasse ein"""
        pass

    def setMonth(self, set=True):
        y = str(self.dateEditJahr.date().toPyDate())
        y = y.split("-")
        y = int(y[0])
        self.m = int(self.comboBoxMonat.currentIndex())+1

        cal = Calendar()

        self.weeks = []
        w = 0
        currentweek = 0
        for week in cal.monthdatescalendar(y, self.m):
            z = 1
            oneweek = []
            date_fr = ""
            for date in week:
                if str(date) == datetime.now().strftime("%Y-%m-%d"):
                    currentweek = w
                if z <= 5:
                    oneweek.append(str(date))
                if z == 5:
                    date_fr = str(date)
                z += 1
            # Nur wenn der Freitag der ersten Woche auch noch im ausgewählten
            # Monat liegt, anhängen an weeks
            # leading zero, führende Null hinzufügen: "%02d" % (self.m,)
            if ("%02d" % (self.m,)) != date_fr.split("-")[1] and w == 0:
                # Wenn ausgefiltert, currentweek um eine Woche erniedrigen
                w -= 1
            else:
                self.weeks.append(oneweek)
            w += 1

        if set is True:
            # Wenn zu Beginn aus datensatz_anzeigen aufgerufen,
            # aktuelle Woche setzen
            self.weekno = currentweek
            self.weekafter(True)
        elif set == "withlast":
            # bei Button mit der letzten Woche beginnen
            self.weekno = len(self.weeks)
        else:
            # mit anderem Monat aus Auswahl starten
            self.weekno = -1
            self.weekafter()

    def weekbefore(self):
        if self.weekno <= 0:
            # Wenn am Anfang der Wochenliste angekommen, in vorherigen
            # Monat wechseln
            previousmonth = self.comboBoxMonat.currentIndex()
            if previousmonth >= 1:
                monat = date(9999, previousmonth, 1).strftime("%B")
                self.comboBoxMonat.setCurrentText(monat)
            else:
                previousmonth = 12
                monat = date(9999, previousmonth, 1).strftime("%B")
                self.comboBoxMonat.setCurrentText(monat)
                # vorheriges Jahr setzen
                previousyear = int(self.combo_jahr.get())-1
                self.dateEditJahr.setDate(QtCore.QDate(previousyear, 1, 1))
            # Datum des aktuellen Montags speichern
            aktmo = self.label_Mo.text()
            # neuen Monat setzen, dafür withlast übergeben, um am Ende zu
            # beginnen
            self.setMonth("withlast")
            self.weekbefore()
            # wenn der neue Montag in der gleichen Woche liegt, noch eine
            # Woche vor
            if aktmo == self.label_Mo.text():
                self.weekbefore()
        else:
            self.resetButtons()
            self.weekno -= 1

            self.set_weeks()

            self.set_fehlzeiten()

    def weekafter(self, set=None):
        if self.weekno+1 <= len(self.weeks)-1 or set is True:
            self.resetButtons()
            # Wenn zu Beginn aus setmonth aufgerufen, aktuelle Woche benutzen.
            # Nur wenn Button wurde gedrückt, eine Woche weiter
            if set is not True:
                self.weekno += 1

            self.set_weeks()

            # self.set_buchungen()
        # Wenn am Ende der Wochenliste angekommen, in nächsten Monat wechseln,
        # außer wenn aus setmonth aufgerufen
        else:
            if set is not True:
                nextmonth = self.comboBoxMonat.currentIndex()+2
                if nextmonth <= 12:
                    monat = date(9999, nextmonth, 1).strftime("%B")
                    self.comboBoxMonat.setCurrentText(monat)
                else:
                    nextmonth = 1
                    monat = date(9999, nextmonth, 1).strftime("%B")
                    self.comboBoxMonat.setCurrentText(monat)
                    # neues Jahr setzen
                    nextyear = self.dateEditJahr.date().toPyDate()
                    nextyear = str(nextyear).split("-")
                    nextyear = int(nextyear[0])+1
                    self.dateEditJahr.setDate(QtCore.QDate(nextyear, 1, 1))
                # Datum des aktuellen Montags speichern
                aktmo = self.label_Mo.text()
                # neuen Monat setzen
                self.setMonth()
                # wenn der neue Montag in der gleichen Woche liegt, noch eine
                # Woche vor
                if aktmo == self.label_Mo.text():
                    self.weekafter()
        if set is True:
            pass
        else:
            self.set_fehlzeiten()

    def set_weeks(self):
        self.label_Woche.setText(
            self.weeks[self.weekno][0].split("-")[2]+"." +
            self.weeks[self.weekno][0].split("-")[1]+"."+" bis " +
            self.weeks[self.weekno][4].split("-")[2]+"." +
            self.weeks[self.weekno][4].split("-")[1]+".")
        self.label_Mo.setText(
            self.weeks[self.weekno][0].split("-")[2]+"." +
            self.weeks[self.weekno][0].split("-")[1]+".")
        self.label_Di.setText(
            self.weeks[self.weekno][1].split("-")[2]+"." +
            self.weeks[self.weekno][1].split("-")[1]+".")
        self.label_Mi.setText(
            self.weeks[self.weekno][2].split("-")[2]+"." +
            self.weeks[self.weekno][2].split("-")[1]+".")
        self.label_Do.setText(
            self.weeks[self.weekno][3].split("-")[2]+"." +
            self.weeks[self.weekno][3].split("-")[1]+".")
        self.label_Fr.setText(
            self.weeks[self.weekno][4].split("-")[2]+"." +
            self.weeks[self.weekno][4].split("-")[1]+".")

    def set_fehlzeiten(self):
        """Führt alle set-Methoden aus, indem vorher die Liste aus der db
        geholt wird und den Methoden u oder e oder ""? übergeben wird """

        # Button reset and enable navigation
        self.resetButtons()
        self.enableButtons()

        # Schüler-pk setzen
        auswahl = int(self.tableWidget.currentRow())
        self.student_pk = self.filtered[auswahl][2]

        self.countfz()
        # DB-Verbindung
        # verbindung = sqlite3.connect("kurs.db")
        # c = verbindung.cursor()

        # Liste generieren (wenn es das Datum+Std nicht gibt, gibt sqlite das
        # Datum selbst zurück)
        setlist = []
        self.datelistweek = []

        for i in self.weeks[self.weekno]:
            fehlzlist = []
            datelist = []
            datelist.append(i+"_1")
            datelist.append(i+"_2")
            datelist.append(i+"_3")
            datelist.append(i+"_4")
            datelist.append(i+"_5")
            datelist.append(i+"_6")
            datelist.append(i+"_7")
            self.datelistweek.append(datelist)

            for d in datelist:
                d = '"'+d+'"'
                item = list(self.db.susc.execute("""SELECT """+d+"""
                                                FROM "sus"
                                                WHERE pk = ?;
                                            """,
                                                 (self.student_pk,)))
                fehlzlist.append(item)

            setlist.append(fehlzlist)

        # set-Methoden aufrufen

        self.set1_1(setlist[0][0][0][0])
        self.set1_2(setlist[1][0][0][0])
        self.set1_3(setlist[2][0][0][0])
        self.set1_4(setlist[3][0][0][0])
        self.set1_5(setlist[4][0][0][0])

        self.set2_1(setlist[0][1][0][0])
        self.set2_2(setlist[1][1][0][0])
        self.set2_3(setlist[2][1][0][0])
        self.set2_4(setlist[3][1][0][0])
        self.set2_5(setlist[4][1][0][0])

        self.set3_1(setlist[0][2][0][0])
        self.set3_2(setlist[1][2][0][0])
        self.set3_3(setlist[2][2][0][0])
        self.set3_4(setlist[3][2][0][0])
        self.set3_5(setlist[4][2][0][0])

        self.set4_1(setlist[0][3][0][0])
        self.set4_2(setlist[1][3][0][0])
        self.set4_3(setlist[2][3][0][0])
        self.set4_4(setlist[3][3][0][0])
        self.set4_5(setlist[4][3][0][0])

        self.set5_1(setlist[0][4][0][0])
        self.set5_2(setlist[1][4][0][0])
        self.set5_3(setlist[2][4][0][0])
        self.set5_4(setlist[3][4][0][0])
        self.set5_5(setlist[4][4][0][0])

        self.set6_1(setlist[0][5][0][0])
        self.set6_2(setlist[1][5][0][0])
        self.set6_3(setlist[2][5][0][0])
        self.set6_4(setlist[3][5][0][0])
        self.set6_5(setlist[4][5][0][0])

        self.set7_1(setlist[0][6][0][0])
        self.set7_2(setlist[1][6][0][0])
        self.set7_3(setlist[2][6][0][0])
        self.set7_4(setlist[3][6][0][0])
        self.set7_5(setlist[4][6][0][0])

    def set1_1(self, val=None):
        if val is False:
            if self.button1_1.text() == '':
                self.button1_1.setStyleSheet(
                    "background-color: rgb(216, 109, 109);")
                self.button1_1.setText("u")
                self.db.writeFehlzeiten(
                    self.student_pk, 1, self.datelistweek[0][0], True)
            elif self.button1_1.text() == 'u':
                self.button1_1.setStyleSheet(
                    "background-color: rgb(89, 209, 117);")
                self.button1_1.setText("e")
                self.db.writeFehlzeiten(
                    self.student_pk, 2, self.datelistweek[0][0], True)
            elif self.button1_1.text() == 'e':
                self.button1_1.setStyleSheet(
                    "background-color: rgb(255, 255, 127);")
                self.button1_1.setText("S")
                self.db.writeFehlzeiten(
                    self.student_pk, 3, self.datelistweek[0][0], True)
            elif self.button1_1.text() == 'S':
                self.button1_1.setStyleSheet(
                    "background-color: rgb(160, 209, 255);")
                self.button1_1.setText("Q")
                self.db.writeFehlzeiten(
                    self.student_pk, 4, self.datelistweek[0][0], True)
            elif self.button1_1.text() == 'Q':
                self.button1_1.setStyleSheet("")
                self.button1_1.setText("")
                self.db.writeFehlzeiten(
                    self.student_pk, 0, self.datelistweek[0][0], True)
            self.countfz()
        else:
            if val == "1":
                self.button1_1.setStyleSheet(
                    "background-color: rgb(216, 109, 109);")
                self.button1_1.setText("u")
            if val == "2":
                self.button1_1.setStyleSheet(
                    "background-color: rgb(89, 209, 117);")
                self.button1_1.setText("e")
            if val == "3":
                self.button1_1.setStyleSheet(
                    "background-color: rgb(255, 255, 127);")
                self.button1_1.setText("S")
            if val == "4":
                self.button1_1.setStyleSheet(
                    "background-color: rgb(160, 209, 255);")
                self.button1_1.setText("Q")

    def set1_2(self, val=None):
        if val is False:
            if self.button1_2.text() == '':
                self.button1_2.setStyleSheet(
                    "background-color: rgb(216, 109, 109);")
                self.button1_2.setText("u")
                self.db.writeFehlzeiten(
                    self.student_pk, 1, self.datelistweek[1][0], True)
            elif self.button1_2.text() == 'u':
                self.button1_2.setStyleSheet(
                    "background-color: rgb(89, 209, 117);")
                self.button1_2.setText("e")
                self.db.writeFehlzeiten(
                    self.student_pk, 2, self.datelistweek[1][0], True)
            elif self.button1_2.text() == 'e':
                self.button1_2.setStyleSheet(
                    "background-color: rgb(255, 255, 127);")
                self.button1_2.setText("S")
                self.db.writeFehlzeiten(
                    self.student_pk, 3, self.datelistweek[1][0], True)
            elif self.button1_2.text() == 'S':
                self.button1_2.setStyleSheet(
                    "background-color: rgb(160, 209, 255);")
                self.button1_2.setText("Q")
                self.db.writeFehlzeiten(
                    self.student_pk, 4, self.datelistweek[1][0], True)
            elif self.button1_2.text() == 'Q':
                self.button1_2.setStyleSheet("")
                self.button1_2.setText("")
                self.db.writeFehlzeiten(
                    self.student_pk, 0, self.datelistweek[1][0], True)
            self.countfz()
        else:
            if val == "1":
                self.button1_2.setStyleSheet(
                    "background-color: rgb(216, 109, 109);")
                self.button1_2.setText("u")
            if val == "2":
                self.button1_2.setStyleSheet(
                    "background-color: rgb(89, 209, 117);")
                self.button1_2.setText("e")
            if val == "3":
                self.button1_2.setStyleSheet(
                    "background-color: rgb(255, 255, 127);")
                self.button1_2.setText("S")
            if val == "4":
                self.button1_2.setStyleSheet(
                    "background-color: rgb(160, 209, 255);")
                self.button1_2.setText("Q")

    def set1_3(self, val=None):
        if val is False:
            if self.button1_3.text() == '':
                self.button1_3.setStyleSheet(
                    "background-color: rgb(216, 109, 109);")
                self.button1_3.setText("u")
                self.db.writeFehlzeiten(
                    self.student_pk, 1, self.datelistweek[2][0], True)
            elif self.button1_3.text() == 'u':
                self.button1_3.setStyleSheet(
                    "background-color: rgb(89, 209, 117);")
                self.button1_3.setText("e")
                self.db.writeFehlzeiten(
                    self.student_pk, 2, self.datelistweek[2][0], True)
            elif self.button1_3.text() == 'e':
                self.button1_3.setStyleSheet(
                    "background-color: rgb(255, 255, 127);")
                self.button1_3.setText("S")
                self.db.writeFehlzeiten(
                    self.student_pk, 3, self.datelistweek[2][0], True)
            elif self.button1_3.text() == 'S':
                self.button1_3.setStyleSheet(
                    "background-color: rgb(160, 209, 255);")
                self.button1_3.setText("Q")
                self.db.writeFehlzeiten(
                    self.student_pk, 4, self.datelistweek[2][0], True)
            elif self.button1_3.text() == 'Q':
                self.button1_3.setStyleSheet("")
                self.button1_3.setText("")
                self.db.writeFehlzeiten(
                    self.student_pk, 0, self.datelistweek[2][0], True)
            self.countfz()
        else:
            if val == "1":
                self.button1_3.setStyleSheet(
                    "background-color: rgb(216, 109, 109);")
                self.button1_3.setText("u")
            if val == "2":
                self.button1_3.setStyleSheet(
                    "background-color: rgb(89, 209, 117);")
                self.button1_3.setText("e")
            if val == "3":
                self.button1_3.setStyleSheet(
                    "background-color: rgb(255, 255, 127);")
                self.button1_3.setText("S")
            if val == "4":
                self.button1_3.setStyleSheet(
                    "background-color: rgb(160, 209, 255);")
                self.button1_3.setText("Q")

    def set1_4(self, val=None):
        if val is False:
            if self.button1_4.text() == '':
                self.button1_4.setStyleSheet(
                    "background-color: rgb(216, 109, 109);")
                self.button1_4.setText("u")
                self.db.writeFehlzeiten(
                    self.student_pk, 1, self.datelistweek[3][0], True)
            elif self.button1_4.text() == 'u':
                self.button1_4.setStyleSheet(
                    "background-color: rgb(89, 209, 117);")
                self.button1_4.setText("e")
                self.db.writeFehlzeiten(
                    self.student_pk, 2, self.datelistweek[3][0], True)
            elif self.button1_4.text() == 'e':
                self.button1_4.setStyleSheet(
                    "background-color: rgb(255, 255, 127);")
                self.button1_4.setText("S")
                self.db.writeFehlzeiten(
                    self.student_pk, 3, self.datelistweek[3][0], True)
            elif self.button1_4.text() == 'S':
                self.button1_4.setStyleSheet(
                    "background-color: rgb(160, 209, 255);")
                self.button1_4.setText("Q")
                self.db.writeFehlzeiten(
                    self.student_pk, 4, self.datelistweek[3][0], True)
            elif self.button1_4.text() == 'Q':
                self.button1_4.setStyleSheet("")
                self.button1_4.setText("")
                self.db.writeFehlzeiten(
                    self.student_pk, 0, self.datelistweek[3][0], True)
            self.countfz()
        else:
            if val == "1":
                self.button1_4.setStyleSheet(
                    "background-color: rgb(216, 109, 109);")
                self.button1_4.setText("u")
            if val == "2":
                self.button1_4.setStyleSheet(
                    "background-color: rgb(89, 209, 117);")
                self.button1_4.setText("e")
            if val == "3":
                self.button1_4.setStyleSheet(
                    "background-color: rgb(255, 255, 127);")
                self.button1_4.setText("S")
            if val == "4":
                self.button1_4.setStyleSheet(
                    "background-color: rgb(160, 209, 255);")
                self.button1_4.setText("Q")

    def set1_5(self, val=None):
        if val is False:
            if self.button1_5.text() == '':
                self.button1_5.setStyleSheet(
                    "background-color: rgb(216, 109, 109);")
                self.button1_5.setText("u")
                self.db.writeFehlzeiten(
                    self.student_pk, 1, self.datelistweek[4][0], True)
            elif self.button1_5.text() == 'u':
                self.button1_5.setStyleSheet(
                    "background-color: rgb(89, 209, 117);")
                self.button1_5.setText("e")
                self.db.writeFehlzeiten(
                    self.student_pk, 2, self.datelistweek[4][0], True)
            elif self.button1_5.text() == 'e':
                self.button1_5.setStyleSheet(
                    "background-color: rgb(255, 255, 127);")
                self.button1_5.setText("S")
                self.db.writeFehlzeiten(
                    self.student_pk, 3, self.datelistweek[4][0], True)
            elif self.button1_5.text() == 'S':
                self.button1_5.setStyleSheet(
                    "background-color: rgb(160, 209, 255);")
                self.button1_5.setText("Q")
                self.db.writeFehlzeiten(
                    self.student_pk, 4, self.datelistweek[4][0], True)
            elif self.button1_5.text() == 'Q':
                self.button1_5.setStyleSheet("")
                self.button1_5.setText("")
                self.db.writeFehlzeiten(
                    self.student_pk, 0, self.datelistweek[4][0], True)
            self.countfz()
        else:
            if val == "1":
                self.button1_5.setStyleSheet(
                    "background-color: rgb(216, 109, 109);")
                self.button1_5.setText("u")
            if val == "2":
                self.button1_5.setStyleSheet(
                    "background-color: rgb(89, 209, 117);")
                self.button1_5.setText("e")
            if val == "3":
                self.button1_5.setStyleSheet(
                    "background-color: rgb(255, 255, 127);")
                self.button1_5.setText("S")
            if val == "4":
                self.button1_5.setStyleSheet(
                    "background-color: rgb(160, 209, 255);")
                self.button1_5.setText("Q")

    def set2_1(self, val=None):
        if val is False:
            if self.button2_1.text() == '':
                self.button2_1.setStyleSheet(
                    "background-color: rgb(216, 109, 109);")
                self.button2_1.setText("u")
                self.db.writeFehlzeiten(
                    self.student_pk, 1, self.datelistweek[0][1], True)
            elif self.button2_1.text() == 'u':
                self.button2_1.setStyleSheet(
                    "background-color: rgb(89, 209, 117);")
                self.button2_1.setText("e")
                self.db.writeFehlzeiten(
                    self.student_pk, 2, self.datelistweek[0][1], True)
            elif self.button2_1.text() == 'e':
                self.button2_1.setStyleSheet(
                    "background-color: rgb(255, 255, 127);")
                self.button2_1.setText("S")
                self.db.writeFehlzeiten(
                    self.student_pk, 3, self.datelistweek[0][1], True)
            elif self.button2_1.text() == 'S':
                self.button2_1.setStyleSheet(
                    "background-color: rgb(160, 209, 255);")
                self.button2_1.setText("Q")
                self.db.writeFehlzeiten(
                    self.student_pk, 4, self.datelistweek[0][1], True)
            elif self.button2_1.text() == 'Q':
                self.button2_1.setStyleSheet("")
                self.button2_1.setText("")
                self.db.writeFehlzeiten(
                    self.student_pk, 0, self.datelistweek[0][1], True)
            self.countfz()
        else:
            if val == "1":
                self.button2_1.setStyleSheet(
                    "background-color: rgb(216, 109, 109);")
                self.button2_1.setText("u")
            if val == "2":
                self.button2_1.setStyleSheet(
                    "background-color: rgb(89, 209, 117);")
                self.button2_1.setText("e")
            if val == "3":
                self.button2_1.setStyleSheet(
                    "background-color: rgb(255, 255, 127);")
                self.button2_1.setText("S")
            if val == "4":
                self.button2_1.setStyleSheet(
                    "background-color: rgb(160, 209, 255);")
                self.button2_1.setText("Q")

    def set2_2(self, val=None):
        if val is False:
            if self.button2_2.text() == '':
                self.button2_2.setStyleSheet(
                    "background-color: rgb(216, 109, 109);")
                self.button2_2.setText("u")
                self.db.writeFehlzeiten(
                    self.student_pk, 1, self.datelistweek[1][1], True)
            elif self.button2_2.text() == 'u':
                self.button2_2.setStyleSheet(
                    "background-color: rgb(89, 209, 117);")
                self.button2_2.setText("e")
                self.db.writeFehlzeiten(
                    self.student_pk, 2, self.datelistweek[1][1], True)
            elif self.button2_2.text() == 'e':
                self.button2_2.setStyleSheet(
                    "background-color: rgb(255, 255, 127);")
                self.button2_2.setText("S")
                self.db.writeFehlzeiten(
                    self.student_pk, 3, self.datelistweek[1][1], True)
            elif self.button2_2.text() == 'S':
                self.button2_2.setStyleSheet(
                    "background-color: rgb(160, 209, 255);")
                self.button2_2.setText("Q")
                self.db.writeFehlzeiten(
                    self.student_pk, 4, self.datelistweek[1][1], True)
            elif self.button2_2.text() == 'Q':
                self.button2_2.setStyleSheet("")
                self.button2_2.setText("")
                self.db.writeFehlzeiten(
                    self.student_pk, 0, self.datelistweek[1][1], True)
            self.countfz()
        else:
            if val == "1":
                self.button2_2.setStyleSheet(
                    "background-color: rgb(216, 109, 109);")
                self.button2_2.setText("u")
            if val == "2":
                self.button2_2.setStyleSheet(
                    "background-color: rgb(89, 209, 117);")
                self.button2_2.setText("e")
            if val == "3":
                self.button2_2.setStyleSheet(
                    "background-color: rgb(255, 255, 127);")
                self.button2_2.setText("S")
            if val == "4":
                self.button2_2.setStyleSheet(
                    "background-color: rgb(160, 209, 255);")
                self.button2_2.setText("Q")

    def set2_3(self, val=None):
        if val is False:
            if self.button2_3.text() == '':
                self.button2_3.setStyleSheet(
                    "background-color: rgb(216, 109, 109);")
                self.button2_3.setText("u")
                self.db.writeFehlzeiten(
                    self.student_pk, 1, self.datelistweek[2][1], True)
            elif self.button2_3.text() == 'u':
                self.button2_3.setStyleSheet(
                    "background-color: rgb(89, 209, 117);")
                self.button2_3.setText("e")
                self.db.writeFehlzeiten(
                    self.student_pk, 2, self.datelistweek[2][1], True)
            elif self.button2_3.text() == 'e':
                self.button2_3.setStyleSheet(
                    "background-color: rgb(255, 255, 127);")
                self.button2_3.setText("S")
                self.db.writeFehlzeiten(
                    self.student_pk, 3, self.datelistweek[2][1], True)
            elif self.button2_3.text() == 'S':
                self.button2_3.setStyleSheet(
                    "background-color: rgb(160, 209, 255);")
                self.button2_3.setText("Q")
                self.db.writeFehlzeiten(
                    self.student_pk, 4, self.datelistweek[2][1], True)
            elif self.button2_3.text() == 'Q':
                self.button2_3.setStyleSheet("")
                self.button2_3.setText("")
                self.db.writeFehlzeiten(
                    self.student_pk, 0, self.datelistweek[2][1], True)
            self.countfz()
        else:
            if val == "1":
                self.button2_3.setStyleSheet(
                    "background-color: rgb(216, 109, 109);")
                self.button2_3.setText("u")
            if val == "2":
                self.button2_3.setStyleSheet(
                    "background-color: rgb(89, 209, 117);")
                self.button2_3.setText("e")
            if val == "3":
                self.button2_3.setStyleSheet(
                    "background-color: rgb(255, 255, 127);")
                self.button2_3.setText("S")
            if val == "4":
                self.button2_3.setStyleSheet(
                    "background-color: rgb(160, 209, 255);")
                self.button2_3.setText("Q")

    def set2_4(self, val=None):
        if val is False:
            if self.button2_4.text() == '':
                self.button2_4.setStyleSheet(
                    "background-color: rgb(216, 109, 109);")
                self.button2_4.setText("u")
                self.db.writeFehlzeiten(
                    self.student_pk, 1, self.datelistweek[3][1], True)
            elif self.button2_4.text() == 'u':
                self.button2_4.setStyleSheet(
                    "background-color: rgb(89, 209, 117);")
                self.button2_4.setText("e")
                self.db.writeFehlzeiten(
                    self.student_pk, 2, self.datelistweek[3][1], True)
            elif self.button2_4.text() == 'e':
                self.button2_4.setStyleSheet(
                    "background-color: rgb(255, 255, 127);")
                self.button2_4.setText("S")
                self.db.writeFehlzeiten(
                    self.student_pk, 3, self.datelistweek[3][1], True)
            elif self.button2_4.text() == 'S':
                self.button2_4.setStyleSheet(
                    "background-color: rgb(160, 209, 255);")
                self.button2_4.setText("Q")
                self.db.writeFehlzeiten(
                    self.student_pk, 4, self.datelistweek[3][1], True)
            elif self.button2_4.text() == 'Q':
                self.button2_4.setStyleSheet("")
                self.button2_4.setText("")
                self.db.writeFehlzeiten(
                    self.student_pk, 0, self.datelistweek[3][1], True)
            self.countfz()
        else:
            if val == "1":
                self.button2_4.setStyleSheet(
                    "background-color: rgb(216, 109, 109);")
                self.button2_4.setText("u")
            if val == "2":
                self.button2_4.setStyleSheet(
                    "background-color: rgb(89, 209, 117);")
                self.button2_4.setText("e")
            if val == "3":
                self.button2_4.setStyleSheet(
                    "background-color: rgb(255, 255, 127);")
                self.button2_4.setText("S")
            if val == "4":
                self.button2_4.setStyleSheet(
                    "background-color: rgb(160, 209, 255);")
                self.button2_4.setText("Q")

    def set2_5(self, val=None):
        if val is False:
            if self.button2_5.text() == '':
                self.button2_5.setStyleSheet(
                    "background-color: rgb(216, 109, 109);")
                self.button2_5.setText("u")
                self.db.writeFehlzeiten(
                    self.student_pk, 1, self.datelistweek[4][1], True)
            elif self.button2_5.text() == 'u':
                self.button2_5.setStyleSheet(
                    "background-color: rgb(89, 209, 117);")
                self.button2_5.setText("e")
                self.db.writeFehlzeiten(
                    self.student_pk, 2, self.datelistweek[4][1], True)
            elif self.button2_5.text() == 'e':
                self.button2_5.setStyleSheet(
                    "background-color: rgb(255, 255, 127);")
                self.button2_5.setText("S")
                self.db.writeFehlzeiten(
                    self.student_pk, 3, self.datelistweek[4][1], True)
            elif self.button2_5.text() == 'S':
                self.button2_5.setStyleSheet(
                    "background-color: rgb(160, 209, 255);")
                self.button2_5.setText("Q")
                self.db.writeFehlzeiten(
                    self.student_pk, 4, self.datelistweek[4][1], True)
            elif self.button2_5.text() == 'Q':
                self.button2_5.setStyleSheet("")
                self.button2_5.setText("")
                self.db.writeFehlzeiten(
                    self.student_pk, 0, self.datelistweek[4][1], True)
            self.countfz()
        else:
            if val == "1":
                self.button2_5.setStyleSheet(
                    "background-color: rgb(216, 109, 109);")
                self.button2_5.setText("u")
            if val == "2":
                self.button2_5.setStyleSheet(
                    "background-color: rgb(89, 209, 117);")
                self.button2_5.setText("e")
            if val == "3":
                self.button2_5.setStyleSheet(
                    "background-color: rgb(255, 255, 127);")
                self.button2_5.setText("S")
            if val == "4":
                self.button2_5.setStyleSheet(
                    "background-color: rgb(160, 209, 255);")
                self.button2_5.setText("Q")

    def set3_1(self, val=None):
        if val is False:
            if self.button3_1.text() == '':
                self.button3_1.setStyleSheet(
                    "background-color: rgb(216, 109, 109);")
                self.button3_1.setText("u")
                self.db.writeFehlzeiten(
                    self.student_pk, 1, self.datelistweek[0][2], True)
            elif self.button3_1.text() == 'u':
                self.button3_1.setStyleSheet(
                    "background-color: rgb(89, 209, 117);")
                self.button3_1.setText("e")
                self.db.writeFehlzeiten(
                    self.student_pk, 2, self.datelistweek[0][2], True)
            elif self.button3_1.text() == 'e':
                self.button3_1.setStyleSheet(
                    "background-color: rgb(255, 255, 127);")
                self.button3_1.setText("S")
                self.db.writeFehlzeiten(
                    self.student_pk, 3, self.datelistweek[0][2], True)
            elif self.button3_1.text() == 'S':
                self.button3_1.setStyleSheet(
                    "background-color: rgb(160, 209, 255);")
                self.button3_1.setText("Q")
                self.db.writeFehlzeiten(
                    self.student_pk, 4, self.datelistweek[0][2], True)
            elif self.button3_1.text() == 'Q':
                self.button3_1.setStyleSheet("")
                self.button3_1.setText("")
                self.db.writeFehlzeiten(
                    self.student_pk, 0, self.datelistweek[0][2], True)
            self.countfz()
        else:
            if val == "1":
                self.button3_1.setStyleSheet(
                    "background-color: rgb(216, 109, 109);")
                self.button3_1.setText("u")
            if val == "2":
                self.button3_1.setStyleSheet(
                    "background-color: rgb(89, 209, 117);")
                self.button3_1.setText("e")
            if val == "3":
                self.button3_1.setStyleSheet(
                    "background-color: rgb(255, 255, 127);")
                self.button3_1.setText("S")
            if val == "4":
                self.button3_1.setStyleSheet(
                    "background-color: rgb(160, 209, 255);")
                self.button3_1.setText("Q")

    def set3_2(self, val=None):
        if val is False:
            if self.button3_2.text() == '':
                self.button3_2.setStyleSheet(
                    "background-color: rgb(216, 109, 109);")
                self.button3_2.setText("u")
                self.db.writeFehlzeiten(
                    self.student_pk, 1, self.datelistweek[1][2], True)
            elif self.button3_2.text() == 'u':
                self.button3_2.setStyleSheet(
                    "background-color: rgb(89, 209, 117);")
                self.button3_2.setText("e")
                self.db.writeFehlzeiten(
                    self.student_pk, 2, self.datelistweek[1][2], True)
            elif self.button3_2.text() == 'e':
                self.button3_2.setStyleSheet(
                    "background-color: rgb(255, 255, 127);")
                self.button3_2.setText("S")
                self.db.writeFehlzeiten(
                    self.student_pk, 3, self.datelistweek[1][2], True)
            elif self.button3_2.text() == 'S':
                self.button3_2.setStyleSheet(
                    "background-color: rgb(160, 209, 255);")
                self.button3_2.setText("Q")
                self.db.writeFehlzeiten(
                    self.student_pk, 4, self.datelistweek[1][2], True)
            elif self.button3_2.text() == 'Q':
                self.button3_2.setStyleSheet("")
                self.button3_2.setText("")
                self.db.writeFehlzeiten(
                    self.student_pk, 0, self.datelistweek[1][2], True)
            self.countfz()
        else:
            if val == "1":
                self.button3_2.setStyleSheet(
                    "background-color: rgb(216, 109, 109);")
                self.button3_2.setText("u")
            if val == "2":
                self.button3_2.setStyleSheet(
                    "background-color: rgb(89, 209, 117);")
                self.button3_2.setText("e")
            if val == "3":
                self.button3_2.setStyleSheet(
                    "background-color: rgb(255, 255, 127);")
                self.button3_2.setText("S")
            if val == "4":
                self.button3_2.setStyleSheet(
                    "background-color: rgb(160, 209, 255);")
                self.button3_2.setText("Q")

    def set3_3(self, val=None):
        if val is False:
            if self.button3_3.text() == '':
                self.button3_3.setStyleSheet(
                    "background-color: rgb(216, 109, 109);")
                self.button3_3.setText("u")
                self.db.writeFehlzeiten(
                    self.student_pk, 1, self.datelistweek[2][2], True)
            elif self.button3_3.text() == 'u':
                self.button3_3.setStyleSheet(
                    "background-color: rgb(89, 209, 117);")
                self.button3_3.setText("e")
                self.db.writeFehlzeiten(
                    self.student_pk, 2, self.datelistweek[2][2], True)
            elif self.button3_3.text() == 'e':
                self.button3_3.setStyleSheet(
                    "background-color: rgb(255, 255, 127);")
                self.button3_3.setText("S")
                self.db.writeFehlzeiten(
                    self.student_pk, 3, self.datelistweek[2][2], True)
            elif self.button3_3.text() == 'S':
                self.button3_3.setStyleSheet(
                    "background-color: rgb(160, 209, 255);")
                self.button3_3.setText("Q")
                self.db.writeFehlzeiten(
                    self.student_pk, 4, self.datelistweek[2][2], True)
            elif self.button3_3.text() == 'Q':
                self.button3_3.setStyleSheet("")
                self.button3_3.setText("")
                self.db.writeFehlzeiten(
                    self.student_pk, 0, self.datelistweek[2][2], True)
            self.countfz()
        else:
            if val == "1":
                self.button3_3.setStyleSheet(
                    "background-color: rgb(216, 109, 109);")
                self.button3_3.setText("u")
            if val == "2":
                self.button3_3.setStyleSheet(
                    "background-color: rgb(89, 209, 117);")
                self.button3_3.setText("e")
            if val == "3":
                self.button3_3.setStyleSheet(
                    "background-color: rgb(255, 255, 127);")
                self.button3_3.setText("S")
            if val == "4":
                self.button3_3.setStyleSheet(
                    "background-color: rgb(160, 209, 255);")
                self.button3_3.setText("Q")

    def set3_4(self, val=None):
        if val is False:
            if self.button3_4.text() == '':
                self.button3_4.setStyleSheet(
                    "background-color: rgb(216, 109, 109);")
                self.button3_4.setText("u")
                self.db.writeFehlzeiten(
                    self.student_pk, 1, self.datelistweek[3][2], True)
            elif self.button3_4.text() == 'u':
                self.button3_4.setStyleSheet(
                    "background-color: rgb(89, 209, 117);")
                self.button3_4.setText("e")
                self.db.writeFehlzeiten(
                    self.student_pk, 2, self.datelistweek[3][2], True)
            elif self.button3_4.text() == 'e':
                self.button3_4.setStyleSheet(
                    "background-color: rgb(255, 255, 127);")
                self.button3_4.setText("S")
                self.db.writeFehlzeiten(
                    self.student_pk, 3, self.datelistweek[3][2], True)
            elif self.button3_4.text() == 'S':
                self.button3_4.setStyleSheet(
                    "background-color: rgb(160, 209, 255);")
                self.button3_4.setText("Q")
                self.db.writeFehlzeiten(
                    self.student_pk, 4, self.datelistweek[3][2], True)
            elif self.button3_4.text() == 'Q':
                self.button3_4.setStyleSheet("")
                self.button3_4.setText("")
                self.db.writeFehlzeiten(
                    self.student_pk, 0, self.datelistweek[3][2], True)
            self.countfz()
        else:
            if val == "1":
                self.button3_4.setStyleSheet(
                    "background-color: rgb(216, 109, 109);")
                self.button3_4.setText("u")
            if val == "2":
                self.button3_4.setStyleSheet(
                    "background-color: rgb(89, 209, 117);")
                self.button3_4.setText("e")
            if val == "3":
                self.button3_4.setStyleSheet(
                    "background-color: rgb(255, 255, 127);")
                self.button3_4.setText("S")
            if val == "4":
                self.button3_4.setStyleSheet(
                    "background-color: rgb(160, 209, 255);")
                self.button3_4.setText("Q")

    def set3_5(self, val=None):
        if val is False:
            if self.button3_5.text() == '':
                self.button3_5.setStyleSheet(
                    "background-color: rgb(216, 109, 109);")
                self.button3_5.setText("u")
                self.db.writeFehlzeiten(
                    self.student_pk, 1, self.datelistweek[4][2], True)
            elif self.button3_5.text() == 'u':
                self.button3_5.setStyleSheet(
                    "background-color: rgb(89, 209, 117);")
                self.button3_5.setText("e")
                self.db.writeFehlzeiten(
                    self.student_pk, 2, self.datelistweek[4][2], True)
            elif self.button3_5.text() == 'e':
                self.button3_5.setStyleSheet(
                    "background-color: rgb(255, 255, 127);")
                self.button3_5.setText("S")
                self.db.writeFehlzeiten(
                    self.student_pk, 3, self.datelistweek[4][2], True)
            elif self.button3_5.text() == 'S':
                self.button3_5.setStyleSheet(
                    "background-color: rgb(160, 209, 255);")
                self.button3_5.setText("Q")
                self.db.writeFehlzeiten(
                    self.student_pk, 4, self.datelistweek[4][2], True)
            elif self.button3_5.text() == 'Q':
                self.button3_5.setStyleSheet("")
                self.button3_5.setText("")
                self.db.writeFehlzeiten(
                    self.student_pk, 0, self.datelistweek[4][2], True)
            self.countfz()
        else:
            if val == "1":
                self.button3_5.setStyleSheet(
                    "background-color: rgb(216, 109, 109);")
                self.button3_5.setText("u")
            if val == "2":
                self.button3_5.setStyleSheet(
                    "background-color: rgb(89, 209, 117);")
                self.button3_5.setText("e")
            if val == "3":
                self.button3_5.setStyleSheet(
                    "background-color: rgb(255, 255, 127);")
                self.button3_5.setText("S")
            if val == "4":
                self.button3_5.setStyleSheet(
                    "background-color: rgb(160, 209, 255);")
                self.button3_5.setText("Q")

    def set4_1(self, val=None):
        if val is False:
            if self.button4_1.text() == '':
                self.button4_1.setStyleSheet(
                    "background-color: rgb(216, 109, 109);")
                self.button4_1.setText("u")
                self.db.writeFehlzeiten(
                    self.student_pk, 1, self.datelistweek[0][3], True)
            elif self.button4_1.text() == 'u':
                self.button4_1.setStyleSheet(
                    "background-color: rgb(89, 209, 117);")
                self.button4_1.setText("e")
                self.db.writeFehlzeiten(
                    self.student_pk, 2, self.datelistweek[0][3], True)
            elif self.button4_1.text() == 'e':
                self.button4_1.setStyleSheet(
                    "background-color: rgb(255, 255, 127);")
                self.button4_1.setText("S")
                self.db.writeFehlzeiten(
                    self.student_pk, 3, self.datelistweek[0][3], True)
            elif self.button4_1.text() == 'S':
                self.button4_1.setStyleSheet(
                    "background-color: rgb(160, 209, 255);")
                self.button4_1.setText("Q")
                self.db.writeFehlzeiten(
                    self.student_pk, 4, self.datelistweek[0][3], True)
            elif self.button4_1.text() == 'Q':
                self.button4_1.setStyleSheet("")
                self.button4_1.setText("")
                self.db.writeFehlzeiten(
                    self.student_pk, 0, self.datelistweek[0][3], True)
            self.countfz()
        else:
            if val == "1":
                self.button4_1.setStyleSheet(
                    "background-color: rgb(216, 109, 109);")
                self.button4_1.setText("u")
            if val == "2":
                self.button4_1.setStyleSheet(
                    "background-color: rgb(89, 209, 117);")
                self.button4_1.setText("e")
            if val == "3":
                self.button4_1.setStyleSheet(
                    "background-color: rgb(255, 255, 127);")
                self.button4_1.setText("S")
            if val == "4":
                self.button4_1.setStyleSheet(
                    "background-color: rgb(160, 209, 255);")
                self.button4_1.setText("Q")

    def set4_2(self, val=None):
        if val is False:
            if self.button4_2.text() == '':
                self.button4_2.setStyleSheet(
                    "background-color: rgb(216, 109, 109);")
                self.button4_2.setText("u")
                self.db.writeFehlzeiten(
                    self.student_pk, 1, self.datelistweek[1][3], True)
            elif self.button4_2.text() == 'u':
                self.button4_2.setStyleSheet(
                    "background-color: rgb(89, 209, 117);")
                self.button4_2.setText("e")
                self.db.writeFehlzeiten(
                    self.student_pk, 2, self.datelistweek[1][3], True)
            elif self.button4_2.text() == 'e':
                self.button4_2.setStyleSheet(
                    "background-color: rgb(255, 255, 127);")
                self.button4_2.setText("S")
                self.db.writeFehlzeiten(
                    self.student_pk, 3, self.datelistweek[1][3], True)
            elif self.button4_2.text() == 'S':
                self.button4_2.setStyleSheet(
                    "background-color: rgb(160, 209, 255);")
                self.button4_2.setText("Q")
                self.db.writeFehlzeiten(
                    self.student_pk, 4, self.datelistweek[1][3], True)
            elif self.button4_2.text() == 'Q':
                self.button4_2.setStyleSheet("")
                self.button4_2.setText("")
                self.db.writeFehlzeiten(
                    self.student_pk, 0, self.datelistweek[1][3], True)
            self.countfz()
        else:
            if val == "1":
                self.button4_2.setStyleSheet(
                    "background-color: rgb(216, 109, 109);")
                self.button4_2.setText("u")
            if val == "2":
                self.button4_2.setStyleSheet(
                    "background-color: rgb(89, 209, 117);")
                self.button4_2.setText("e")
            if val == "3":
                self.button4_2.setStyleSheet(
                    "background-color: rgb(255, 255, 127);")
                self.button4_2.setText("S")
            if val == "4":
                self.button4_2.setStyleSheet(
                    "background-color: rgb(160, 209, 255);")
                self.button4_2.setText("Q")

    def set4_3(self, val=None):
        if val is False:
            if self.button4_3.text() == '':
                self.button4_3.setStyleSheet(
                    "background-color: rgb(216, 109, 109);")
                self.button4_3.setText("u")
                self.db.writeFehlzeiten(
                    self.student_pk, 1, self.datelistweek[2][3], True)
            elif self.button4_3.text() == 'u':
                self.button4_3.setStyleSheet(
                    "background-color: rgb(89, 209, 117);")
                self.button4_3.setText("e")
                self.db.writeFehlzeiten(
                    self.student_pk, 2, self.datelistweek[2][3], True)
            elif self.button4_3.text() == 'e':
                self.button4_3.setStyleSheet(
                    "background-color: rgb(255, 255, 127);")
                self.button4_3.setText("S")
                self.db.writeFehlzeiten(
                    self.student_pk, 3, self.datelistweek[2][3], True)
            elif self.button4_3.text() == 'S':
                self.button4_3.setStyleSheet(
                    "background-color: rgb(160, 209, 255);")
                self.button4_3.setText("Q")
                self.db.writeFehlzeiten(
                    self.student_pk, 4, self.datelistweek[2][3], True)
            elif self.button4_3.text() == 'Q':
                self.button4_3.setStyleSheet("")
                self.button4_3.setText("")
                self.db.writeFehlzeiten(
                    self.student_pk, 0, self.datelistweek[2][3], True)
            self.countfz()
        else:
            if val == "1":
                self.button4_3.setStyleSheet(
                    "background-color: rgb(216, 109, 109);")
                self.button4_3.setText("u")
            if val == "2":
                self.button4_3.setStyleSheet(
                    "background-color: rgb(89, 209, 117);")
                self.button4_3.setText("e")
            if val == "3":
                self.button4_3.setStyleSheet(
                    "background-color: rgb(255, 255, 127);")
                self.button4_3.setText("S")
            if val == "4":
                self.button4_3.setStyleSheet(
                    "background-color: rgb(160, 209, 255);")
                self.button4_3.setText("Q")

    def set4_4(self, val=None):
        if val is False:
            if self.button4_4.text() == '':
                self.button4_4.setStyleSheet(
                    "background-color: rgb(216, 109, 109);")
                self.button4_4.setText("u")
                self.db.writeFehlzeiten(
                    self.student_pk, 1, self.datelistweek[3][3], True)
            elif self.button4_4.text() == 'u':
                self.button4_4.setStyleSheet(
                    "background-color: rgb(89, 209, 117);")
                self.button4_4.setText("e")
                self.db.writeFehlzeiten(
                    self.student_pk, 2, self.datelistweek[3][3], True)
            elif self.button4_4.text() == 'e':
                self.button4_4.setStyleSheet(
                    "background-color: rgb(255, 255, 127);")
                self.button4_4.setText("S")
                self.db.writeFehlzeiten(
                    self.student_pk, 3, self.datelistweek[3][3], True)
            elif self.button4_4.text() == 'S':
                self.button4_4.setStyleSheet(
                    "background-color: rgb(160, 209, 255);")
                self.button4_4.setText("Q")
                self.db.writeFehlzeiten(
                    self.student_pk, 4, self.datelistweek[3][3], True)
            elif self.button4_4.text() == 'Q':
                self.button4_4.setStyleSheet("")
                self.button4_4.setText("")
                self.db.writeFehlzeiten(
                    self.student_pk, 0, self.datelistweek[3][3], True)
            self.countfz()
        else:
            if val == "1":
                self.button4_4.setStyleSheet(
                    "background-color: rgb(216, 109, 109);")
                self.button4_4.setText("u")
            if val == "2":
                self.button4_4.setStyleSheet(
                    "background-color: rgb(89, 209, 117);")
                self.button4_4.setText("e")
            if val == "3":
                self.button4_4.setStyleSheet(
                    "background-color: rgb(255, 255, 127);")
                self.button4_4.setText("S")
            if val == "4":
                self.button4_4.setStyleSheet(
                    "background-color: rgb(160, 209, 255);")
                self.button4_4.setText("Q")

    def set4_5(self, val=None):
        if val is False:
            if self.button4_5.text() == '':
                self.button4_5.setStyleSheet(
                    "background-color: rgb(216, 109, 109);")
                self.button4_5.setText("u")
                self.db.writeFehlzeiten(
                    self.student_pk, 1, self.datelistweek[4][3], True)
            elif self.button4_5.text() == 'u':
                self.button4_5.setStyleSheet(
                    "background-color: rgb(89, 209, 117);")
                self.button4_5.setText("e")
                self.db.writeFehlzeiten(
                    self.student_pk, 2, self.datelistweek[4][3], True)
            elif self.button4_5.text() == 'e':
                self.button4_5.setStyleSheet(
                    "background-color: rgb(255, 255, 127);")
                self.button4_5.setText("S")
                self.db.writeFehlzeiten(
                    self.student_pk, 3, self.datelistweek[4][3], True)
            elif self.button4_5.text() == 'S':
                self.button4_5.setStyleSheet(
                    "background-color: rgb(160, 209, 255);")
                self.button4_5.setText("Q")
                self.db.writeFehlzeiten(
                    self.student_pk, 4, self.datelistweek[4][3], True)
            elif self.button4_5.text() == 'Q':
                self.button4_5.setStyleSheet("")
                self.button4_5.setText("")
                self.db.writeFehlzeiten(
                    self.student_pk, 0, self.datelistweek[4][3], True)
            self.countfz()
        else:
            if val == "1":
                self.button4_5.setStyleSheet(
                    "background-color: rgb(216, 109, 109);")
                self.button4_5.setText("u")
            if val == "2":
                self.button4_5.setStyleSheet(
                    "background-color: rgb(89, 209, 117);")
                self.button4_5.setText("e")
            if val == "3":
                self.button4_5.setStyleSheet(
                    "background-color: rgb(255, 255, 127);")
                self.button4_5.setText("S")
            if val == "4":
                self.button4_5.setStyleSheet(
                    "background-color: rgb(160, 209, 255);")
                self.button4_5.setText("Q")

    def set5_1(self, val=None):
        if val is False:
            if self.button5_1.text() == '':
                self.button5_1.setStyleSheet(
                    "background-color: rgb(216, 109, 109);")
                self.button5_1.setText("u")
                self.db.writeFehlzeiten(
                    self.student_pk, 1, self.datelistweek[0][4], True)
            elif self.button5_1.text() == 'u':
                self.button5_1.setStyleSheet(
                    "background-color: rgb(89, 209, 117);")
                self.button5_1.setText("e")
                self.db.writeFehlzeiten(
                    self.student_pk, 2, self.datelistweek[0][4], True)
            elif self.button5_1.text() == 'e':
                self.button5_1.setStyleSheet(
                    "background-color: rgb(255, 255, 127);")
                self.button5_1.setText("S")
                self.db.writeFehlzeiten(
                    self.student_pk, 3, self.datelistweek[0][4], True)
            elif self.button5_1.text() == 'S':
                self.button5_1.setStyleSheet(
                    "background-color: rgb(160, 209, 255);")
                self.button5_1.setText("Q")
                self.db.writeFehlzeiten(
                    self.student_pk, 4, self.datelistweek[0][4], True)
            elif self.button5_1.text() == 'Q':
                self.button5_1.setStyleSheet("")
                self.button5_1.setText("")
                self.db.writeFehlzeiten(
                    self.student_pk, 0, self.datelistweek[0][4], True)
            self.countfz()
        else:
            if val == "1":
                self.button5_1.setStyleSheet(
                    "background-color: rgb(216, 109, 109);")
                self.button5_1.setText("u")
            if val == "2":
                self.button5_1.setStyleSheet(
                    "background-color: rgb(89, 209, 117);")
                self.button5_1.setText("e")
            if val == "3":
                self.button5_1.setStyleSheet(
                    "background-color: rgb(255, 255, 127);")
                self.button5_1.setText("S")
            if val == "4":
                self.button5_1.setStyleSheet(
                    "background-color: rgb(160, 209, 255);")
                self.button5_1.setText("Q")

    def set5_2(self, val=None):
        if val is False:
            if self.button5_2.text() == '':
                self.button5_2.setStyleSheet(
                    "background-color: rgb(216, 109, 109);")
                self.button5_2.setText("u")
                self.db.writeFehlzeiten(
                    self.student_pk, 1, self.datelistweek[1][4], True)
            elif self.button5_2.text() == 'u':
                self.button5_2.setStyleSheet(
                    "background-color: rgb(89, 209, 117);")
                self.button5_2.setText("e")
                self.db.writeFehlzeiten(
                    self.student_pk, 2, self.datelistweek[1][4], True)
            elif self.button5_2.text() == 'e':
                self.button5_2.setStyleSheet(
                    "background-color: rgb(255, 255, 127);")
                self.button5_2.setText("S")
                self.db.writeFehlzeiten(
                    self.student_pk, 3, self.datelistweek[1][4], True)
            elif self.button5_2.text() == 'S':
                self.button5_2.setStyleSheet(
                    "background-color: rgb(160, 209, 255);")
                self.button5_2.setText("Q")
                self.db.writeFehlzeiten(
                    self.student_pk, 4, self.datelistweek[1][4], True)
            elif self.button5_2.text() == 'Q':
                self.button5_2.setStyleSheet("")
                self.button5_2.setText("")
                self.db.writeFehlzeiten(
                    self.student_pk, 0, self.datelistweek[1][4], True)
            self.countfz()
        else:
            if val == "1":
                self.button5_2.setStyleSheet(
                    "background-color: rgb(216, 109, 109);")
                self.button5_2.setText("u")
            if val == "2":
                self.button5_2.setStyleSheet(
                    "background-color: rgb(89, 209, 117);")
                self.button5_2.setText("e")
            if val == "3":
                self.button5_2.setStyleSheet(
                    "background-color: rgb(255, 255, 127);")
                self.button5_2.setText("S")
            if val == "4":
                self.button5_2.setStyleSheet(
                    "background-color: rgb(160, 209, 255);")
                self.button5_2.setText("Q")

    def set5_3(self, val=None):
        if val is False:
            if self.button5_3.text() == '':
                self.button5_3.setStyleSheet(
                    "background-color: rgb(216, 109, 109);")
                self.button5_3.setText("u")
                self.db.writeFehlzeiten(
                    self.student_pk, 1, self.datelistweek[2][4], True)
            elif self.button5_3.text() == 'u':
                self.button5_3.setStyleSheet(
                    "background-color: rgb(89, 209, 117);")
                self.button5_3.setText("e")
                self.db.writeFehlzeiten(
                    self.student_pk, 2, self.datelistweek[2][4], True)
            elif self.button5_3.text() == 'e':
                self.button5_3.setStyleSheet(
                    "background-color: rgb(255, 255, 127);")
                self.button5_3.setText("S")
                self.db.writeFehlzeiten(
                    self.student_pk, 3, self.datelistweek[2][4], True)
            elif self.button5_3.text() == 'S':
                self.button5_3.setStyleSheet(
                    "background-color: rgb(160, 209, 255);")
                self.button5_3.setText("Q")
                self.db.writeFehlzeiten(
                    self.student_pk, 4, self.datelistweek[2][4], True)
            elif self.button5_3.text() == 'Q':
                self.button5_3.setStyleSheet("")
                self.button5_3.setText("")
                self.db.writeFehlzeiten(
                    self.student_pk, 0, self.datelistweek[2][4], True)
            self.countfz()
        else:
            if val == "1":
                self.button5_3.setStyleSheet(
                    "background-color: rgb(216, 109, 109);")
                self.button5_3.setText("u")
            if val == "2":
                self.button5_3.setStyleSheet(
                    "background-color: rgb(89, 209, 117);")
                self.button5_3.setText("e")
            if val == "3":
                self.button5_3.setStyleSheet(
                    "background-color: rgb(255, 255, 127);")
                self.button5_3.setText("S")
            if val == "4":
                self.button5_3.setStyleSheet(
                    "background-color: rgb(160, 209, 255);")
                self.button5_3.setText("Q")

    def set5_4(self, val=None):
        if val is False:
            if self.button5_4.text() == '':
                self.button5_4.setStyleSheet(
                    "background-color: rgb(216, 109, 109);")
                self.button5_4.setText("u")
                self.db.writeFehlzeiten(
                    self.student_pk, 1, self.datelistweek[3][4], True)
            elif self.button5_4.text() == 'u':
                self.button5_4.setStyleSheet(
                    "background-color: rgb(89, 209, 117);")
                self.button5_4.setText("e")
                self.db.writeFehlzeiten(
                    self.student_pk, 2, self.datelistweek[3][4], True)
            elif self.button5_4.text() == 'e':
                self.button5_4.setStyleSheet(
                    "background-color: rgb(255, 255, 127);")
                self.button5_4.setText("S")
                self.db.writeFehlzeiten(
                    self.student_pk, 3, self.datelistweek[3][4], True)
            elif self.button5_4.text() == 'S':
                self.button5_4.setStyleSheet(
                    "background-color: rgb(160, 209, 255);")
                self.button5_4.setText("Q")
                self.db.writeFehlzeiten(
                    self.student_pk, 4, self.datelistweek[3][4], True)
            elif self.button5_4.text() == 'Q':
                self.button5_4.setStyleSheet("")
                self.button5_4.setText("")
                self.db.writeFehlzeiten(
                    self.student_pk, 0, self.datelistweek[3][4], True)
            self.countfz()
        else:
            if val == "1":
                self.button5_4.setStyleSheet(
                    "background-color: rgb(216, 109, 109);")
                self.button5_4.setText("u")
            if val == "2":
                self.button5_4.setStyleSheet(
                    "background-color: rgb(89, 209, 117);")
                self.button5_4.setText("e")
            if val == "3":
                self.button5_4.setStyleSheet(
                    "background-color: rgb(255, 255, 127);")
                self.button5_4.setText("S")
            if val == "4":
                self.button5_4.setStyleSheet(
                    "background-color: rgb(160, 209, 255);")
                self.button5_4.setText("Q")

    def set5_5(self, val=None):
        if val is False:
            if self.button5_5.text() == '':
                self.button5_5.setStyleSheet(
                    "background-color: rgb(216, 109, 109);")
                self.button5_5.setText("u")
                self.db.writeFehlzeiten(
                    self.student_pk, 1, self.datelistweek[4][4], True)
            elif self.button5_5.text() == 'u':
                self.button5_5.setStyleSheet(
                    "background-color: rgb(89, 209, 117);")
                self.button5_5.setText("e")
                self.db.writeFehlzeiten(
                    self.student_pk, 2, self.datelistweek[4][4], True)
            elif self.button5_5.text() == 'e':
                self.button5_5.setStyleSheet(
                    "background-color: rgb(255, 255, 127);")
                self.button5_5.setText("S")
                self.db.writeFehlzeiten(
                    self.student_pk, 3, self.datelistweek[4][4], True)
            elif self.button5_5.text() == 'S':
                self.button5_5.setStyleSheet(
                    "background-color: rgb(160, 209, 255);")
                self.button5_5.setText("Q")
                self.db.writeFehlzeiten(
                    self.student_pk, 4, self.datelistweek[4][4], True)
            elif self.button5_5.text() == 'Q':
                self.button5_5.setStyleSheet("")
                self.button5_5.setText("")
                self.db.writeFehlzeiten(
                    self.student_pk, 0, self.datelistweek[4][4], True)
            self.countfz()
        else:
            if val == "1":
                self.button5_5.setStyleSheet(
                    "background-color: rgb(216, 109, 109);")
                self.button5_5.setText("u")
            if val == "2":
                self.button5_5.setStyleSheet(
                    "background-color: rgb(89, 209, 117);")
                self.button5_5.setText("e")
            if val == "3":
                self.button5_5.setStyleSheet(
                    "background-color: rgb(255, 255, 127);")
                self.button5_5.setText("S")
            if val == "4":
                self.button5_5.setStyleSheet(
                    "background-color: rgb(160, 209, 255);")
                self.button5_5.setText("Q")

    def set6_1(self, val=None):
        if val is False:
            if self.button6_1.text() == '':
                self.button6_1.setStyleSheet(
                    "background-color: rgb(216, 109, 109);")
                self.button6_1.setText("u")
                self.db.writeFehlzeiten(
                    self.student_pk, 1, self.datelistweek[0][5], True)
            elif self.button6_1.text() == 'u':
                self.button6_1.setStyleSheet(
                    "background-color: rgb(89, 209, 117);")
                self.button6_1.setText("e")
                self.db.writeFehlzeiten(
                    self.student_pk, 2, self.datelistweek[0][5], True)
            elif self.button6_1.text() == 'e':
                self.button6_1.setStyleSheet(
                    "background-color: rgb(255, 255, 127);")
                self.button6_1.setText("S")
                self.db.writeFehlzeiten(
                    self.student_pk, 3, self.datelistweek[0][5], True)
            elif self.button6_1.text() == 'S':
                self.button6_1.setStyleSheet(
                    "background-color: rgb(160, 209, 255);")
                self.button6_1.setText("Q")
                self.db.writeFehlzeiten(
                    self.student_pk, 4, self.datelistweek[0][5], True)
            elif self.button6_1.text() == 'Q':
                self.button6_1.setStyleSheet("")
                self.button6_1.setText("")
                self.db.writeFehlzeiten(
                    self.student_pk, 0, self.datelistweek[0][5], True)
            self.countfz()
        else:
            if val == "1":
                self.button6_1.setStyleSheet(
                    "background-color: rgb(216, 109, 109);")
                self.button6_1.setText("u")
            if val == "2":
                self.button6_1.setStyleSheet(
                    "background-color: rgb(89, 209, 117);")
                self.button6_1.setText("e")
            if val == "3":
                self.button6_1.setStyleSheet(
                    "background-color: rgb(255, 255, 127);")
                self.button6_1.setText("S")
            if val == "4":
                self.button6_1.setStyleSheet(
                    "background-color: rgb(160, 209, 255);")
                self.button6_1.setText("Q")

    def set6_2(self, val=None):
        if val is False:
            if self.button6_2.text() == '':
                self.button6_2.setStyleSheet(
                    "background-color: rgb(216, 109, 109);")
                self.button6_2.setText("u")
                self.db.writeFehlzeiten(
                    self.student_pk, 1, self.datelistweek[1][5], True)
            elif self.button6_2.text() == 'u':
                self.button6_2.setStyleSheet(
                    "background-color: rgb(89, 209, 117);")
                self.button6_2.setText("e")
                self.db.writeFehlzeiten(
                    self.student_pk, 2, self.datelistweek[1][5], True)
            elif self.button6_2.text() == 'e':
                self.button6_2.setStyleSheet(
                    "background-color: rgb(255, 255, 127);")
                self.button6_2.setText("S")
                self.db.writeFehlzeiten(
                    self.student_pk, 3, self.datelistweek[1][5], True)
            elif self.button6_2.text() == 'S':
                self.button6_2.setStyleSheet(
                    "background-color: rgb(160, 209, 255);")
                self.button6_2.setText("Q")
                self.db.writeFehlzeiten(
                    self.student_pk, 4, self.datelistweek[1][5], True)
            elif self.button6_2.text() == 'Q':
                self.button6_2.setStyleSheet("")
                self.button6_2.setText("")
                self.db.writeFehlzeiten(
                    self.student_pk, 0, self.datelistweek[1][5], True)
            self.countfz()
        else:
            if val == "1":
                self.button6_2.setStyleSheet(
                    "background-color: rgb(216, 109, 109);")
                self.button6_2.setText("u")
            if val == "2":
                self.button6_2.setStyleSheet(
                    "background-color: rgb(89, 209, 117);")
                self.button6_2.setText("e")
            if val == "3":
                self.button6_2.setStyleSheet(
                    "background-color: rgb(255, 255, 127);")
                self.button6_2.setText("S")
            if val == "4":
                self.button6_2.setStyleSheet(
                    "background-color: rgb(160, 209, 255);")
                self.button6_2.setText("Q")

    def set6_3(self, val=None):
        if val is False:
            if self.button6_3.text() == '':
                self.button6_3.setStyleSheet(
                    "background-color: rgb(216, 109, 109);")
                self.button6_3.setText("u")
                self.db.writeFehlzeiten(
                    self.student_pk, 1, self.datelistweek[2][5], True)
            elif self.button6_3.text() == 'u':
                self.button6_3.setStyleSheet(
                    "background-color: rgb(89, 209, 117);")
                self.button6_3.setText("e")
                self.db.writeFehlzeiten(
                    self.student_pk, 2, self.datelistweek[2][5], True)
            elif self.button6_3.text() == 'e':
                self.button6_3.setStyleSheet(
                    "background-color: rgb(255, 255, 127);")
                self.button6_3.setText("S")
                self.db.writeFehlzeiten(
                    self.student_pk, 3, self.datelistweek[2][5], True)
            elif self.button6_3.text() == 'S':
                self.button6_3.setStyleSheet(
                    "background-color: rgb(160, 209, 255);")
                self.button6_3.setText("Q")
                self.db.writeFehlzeiten(
                    self.student_pk, 4, self.datelistweek[2][5], True)
            elif self.button6_3.text() == 'Q':
                self.button6_3.setStyleSheet("")
                self.button6_3.setText("")
                self.db.writeFehlzeiten(
                    self.student_pk, 0, self.datelistweek[2][5], True)
            self.countfz()
        else:
            if val == "1":
                self.button6_3.setStyleSheet(
                    "background-color: rgb(216, 109, 109);")
                self.button6_3.setText("u")
            if val == "2":
                self.button6_3.setStyleSheet(
                    "background-color: rgb(89, 209, 117);")
                self.button6_3.setText("e")
            if val == "3":
                self.button6_3.setStyleSheet(
                    "background-color: rgb(255, 255, 127);")
                self.button6_3.setText("S")
            if val == "4":
                self.button6_3.setStyleSheet(
                    "background-color: rgb(160, 209, 255);")
                self.button6_3.setText("Q")

    def set6_4(self, val=None):
        if val is False:
            if self.button6_4.text() == '':
                self.button6_4.setStyleSheet(
                    "background-color: rgb(216, 109, 109);")
                self.button6_4.setText("u")
                self.db.writeFehlzeiten(
                    self.student_pk, 1, self.datelistweek[3][5], True)
            elif self.button6_4.text() == 'u':
                self.button6_4.setStyleSheet(
                    "background-color: rgb(89, 209, 117);")
                self.button6_4.setText("e")
                self.db.writeFehlzeiten(
                    self.student_pk, 2, self.datelistweek[3][5], True)
            elif self.button6_4.text() == 'e':
                self.button6_4.setStyleSheet(
                    "background-color: rgb(255, 255, 127);")
                self.button6_4.setText("S")
                self.db.writeFehlzeiten(
                    self.student_pk, 3, self.datelistweek[3][5], True)
            elif self.button6_4.text() == 'S':
                self.button6_4.setStyleSheet(
                    "background-color: rgb(160, 209, 255);")
                self.button6_4.setText("Q")
                self.db.writeFehlzeiten(
                    self.student_pk, 4, self.datelistweek[3][5], True)
            elif self.button6_4.text() == 'Q':
                self.button6_4.setStyleSheet("")
                self.button6_4.setText("")
                self.db.writeFehlzeiten(
                    self.student_pk, 0, self.datelistweek[3][5], True)
            self.countfz()
        else:
            if val == "1":
                self.button6_4.setStyleSheet(
                    "background-color: rgb(216, 109, 109);")
                self.button6_4.setText("u")
            if val == "2":
                self.button6_4.setStyleSheet(
                    "background-color: rgb(89, 209, 117);")
                self.button6_4.setText("e")
            if val == "3":
                self.button6_4.setStyleSheet(
                    "background-color: rgb(255, 255, 127);")
                self.button6_4.setText("S")
            if val == "4":
                self.button6_4.setStyleSheet(
                    "background-color: rgb(160, 209, 255);")
                self.button6_4.setText("Q")

    def set6_5(self, val=None):
        if val is False:
            if self.button6_5.text() == '':
                self.button6_5.setStyleSheet(
                    "background-color: rgb(216, 109, 109);")
                self.button6_5.setText("u")
                self.db.writeFehlzeiten(
                    self.student_pk, 1, self.datelistweek[4][5], True)
            elif self.button6_5.text() == 'u':
                self.button6_5.setStyleSheet(
                    "background-color: rgb(89, 209, 117);")
                self.button6_5.setText("e")
                self.db.writeFehlzeiten(
                    self.student_pk, 2, self.datelistweek[4][5], True)
            elif self.button6_5.text() == 'e':
                self.button6_5.setStyleSheet(
                    "background-color: rgb(255, 255, 127);")
                self.button6_5.setText("S")
                self.db.writeFehlzeiten(
                    self.student_pk, 3, self.datelistweek[4][5], True)
            elif self.button6_5.text() == 'S':
                self.button6_5.setStyleSheet(
                    "background-color: rgb(160, 209, 255);")
                self.button6_5.setText("Q")
                self.db.writeFehlzeiten(
                    self.student_pk, 4, self.datelistweek[4][5], True)
            elif self.button6_5.text() == 'Q':
                self.button6_5.setStyleSheet("")
                self.button6_5.setText("")
                self.db.writeFehlzeiten(
                    self.student_pk, 0, self.datelistweek[4][5], True)
            self.countfz()
        else:
            if val == "1":
                self.button6_5.setStyleSheet(
                    "background-color: rgb(216, 109, 109);")
                self.button6_5.setText("u")
            if val == "2":
                self.button6_5.setStyleSheet(
                    "background-color: rgb(89, 209, 117);")
                self.button6_5.setText("e")
            if val == "3":
                self.button6_5.setStyleSheet(
                    "background-color: rgb(255, 255, 127);")
                self.button6_5.setText("S")
            if val == "4":
                self.button6_5.setStyleSheet(
                    "background-color: rgb(160, 209, 255);")
                self.button6_5.setText("Q")

    def set7_1(self, val=None):
        if val is False:
            if self.button7_1.text() == '':
                self.button7_1.setStyleSheet(
                    "background-color: rgb(216, 109, 109);")
                self.button7_1.setText("u")
                self.db.writeFehlzeiten(
                    self.student_pk, 1, self.datelistweek[0][6], True)
            elif self.button7_1.text() == 'u':
                self.button7_1.setStyleSheet(
                    "background-color: rgb(89, 209, 117);")
                self.button7_1.setText("e")
                self.db.writeFehlzeiten(
                    self.student_pk, 2, self.datelistweek[0][6], True)
            elif self.button7_1.text() == 'e':
                self.button7_1.setStyleSheet(
                    "background-color: rgb(255, 255, 127);")
                self.button7_1.setText("S")
                self.db.writeFehlzeiten(
                    self.student_pk, 3, self.datelistweek[0][6], True)
            elif self.button7_1.text() == 'S':
                self.button7_1.setStyleSheet(
                    "background-color: rgb(160, 209, 255);")
                self.button7_1.setText("Q")
                self.db.writeFehlzeiten(
                    self.student_pk, 4, self.datelistweek[0][6], True)
            elif self.button7_1.text() == 'Q':
                self.button7_1.setStyleSheet("")
                self.button7_1.setText("")
                self.db.writeFehlzeiten(
                    self.student_pk, 0, self.datelistweek[0][6], True)
            self.countfz()
        else:
            if val == "1":
                self.button7_1.setStyleSheet(
                    "background-color: rgb(216, 109, 109);")
                self.button7_1.setText("u")
            if val == "2":
                self.button7_1.setStyleSheet(
                    "background-color: rgb(89, 209, 117);")
                self.button7_1.setText("e")
            if val == "3":
                self.button7_1.setStyleSheet(
                    "background-color: rgb(255, 255, 127);")
                self.button7_1.setText("S")
            if val == "4":
                self.button7_1.setStyleSheet(
                    "background-color: rgb(160, 209, 255);")
                self.button7_1.setText("Q")

    def set7_2(self, val=None):
        if val is False:
            if self.button7_2.text() == '':
                self.button7_2.setStyleSheet(
                    "background-color: rgb(216, 109, 109);")
                self.button7_2.setText("u")
                self.db.writeFehlzeiten(
                    self.student_pk, 1, self.datelistweek[1][6], True)
            elif self.button7_2.text() == 'u':
                self.button7_2.setStyleSheet(
                    "background-color: rgb(89, 209, 117);")
                self.button7_2.setText("e")
                self.db.writeFehlzeiten(
                    self.student_pk, 2, self.datelistweek[1][6], True)
            elif self.button7_2.text() == 'e':
                self.button7_2.setStyleSheet(
                    "background-color: rgb(255, 255, 127);")
                self.button7_2.setText("S")
                self.db.writeFehlzeiten(
                    self.student_pk, 3, self.datelistweek[1][6], True)
            elif self.button7_2.text() == 'S':
                self.button7_2.setStyleSheet(
                    "background-color: rgb(160, 209, 255);")
                self.button7_2.setText("Q")
                self.db.writeFehlzeiten(
                    self.student_pk, 4, self.datelistweek[1][6], True)
            elif self.button7_2.text() == 'Q':
                self.button7_2.setStyleSheet("")
                self.button7_2.setText("")
                self.db.writeFehlzeiten(
                    self.student_pk, 0, self.datelistweek[1][6], True)
            self.countfz()
        else:
            if val == "1":
                self.button7_2.setStyleSheet(
                    "background-color: rgb(216, 109, 109);")
                self.button7_2.setText("u")
            if val == "2":
                self.button7_2.setStyleSheet(
                    "background-color: rgb(89, 209, 117);")
                self.button7_2.setText("e")
            if val == "3":
                self.button7_2.setStyleSheet(
                    "background-color: rgb(255, 255, 127);")
                self.button7_2.setText("S")
            if val == "4":
                self.button7_2.setStyleSheet(
                    "background-color: rgb(160, 209, 255);")
                self.button7_2.setText("Q")

    def set7_3(self, val=None):
        if val is False:
            if self.button7_3.text() == '':
                self.button7_3.setStyleSheet(
                    "background-color: rgb(216, 109, 109);")
                self.button7_3.setText("u")
                self.db.writeFehlzeiten(
                    self.student_pk, 1, self.datelistweek[2][6], True)
            elif self.button7_3.text() == 'u':
                self.button7_3.setStyleSheet(
                    "background-color: rgb(89, 209, 117);")
                self.button7_3.setText("e")
                self.db.writeFehlzeiten(
                    self.student_pk, 2, self.datelistweek[2][6], True)
            elif self.button7_3.text() == 'e':
                self.button7_3.setStyleSheet(
                    "background-color: rgb(255, 255, 127);")
                self.button7_3.setText("S")
                self.db.writeFehlzeiten(
                    self.student_pk, 3, self.datelistweek[2][6], True)
            elif self.button7_3.text() == 'S':
                self.button7_3.setStyleSheet(
                    "background-color: rgb(160, 209, 255);")
                self.button7_3.setText("Q")
                self.db.writeFehlzeiten(
                    self.student_pk, 4, self.datelistweek[2][6], True)
            elif self.button7_3.text() == 'Q':
                self.button7_3.setStyleSheet("")
                self.button7_3.setText("")
                self.db.writeFehlzeiten(
                    self.student_pk, 0, self.datelistweek[2][6], True)
            self.countfz()
        else:
            if val == "1":
                self.button7_3.setStyleSheet(
                    "background-color: rgb(216, 109, 109);")
                self.button7_3.setText("u")
            if val == "2":
                self.button7_3.setStyleSheet(
                    "background-color: rgb(89, 209, 117);")
                self.button7_3.setText("e")
            if val == "3":
                self.button7_3.setStyleSheet(
                    "background-color: rgb(255, 255, 127);")
                self.button7_3.setText("S")
            if val == "4":
                self.button7_3.setStyleSheet(
                    "background-color: rgb(160, 209, 255);")
                self.button7_3.setText("Q")

    def set7_4(self, val=None):
        if val is False:
            if self.button7_4.text() == '':
                self.button7_4.setStyleSheet(
                    "background-color: rgb(216, 109, 109);")
                self.button7_4.setText("u")
                self.db.writeFehlzeiten(
                    self.student_pk, 1, self.datelistweek[3][6], True)
            elif self.button7_4.text() == 'u':
                self.button7_4.setStyleSheet(
                    "background-color: rgb(89, 209, 117);")
                self.button7_4.setText("e")
                self.db.writeFehlzeiten(
                    self.student_pk, 2, self.datelistweek[3][6], True)
            elif self.button7_4.text() == 'e':
                self.button7_4.setStyleSheet(
                    "background-color: rgb(255, 255, 127);")
                self.button7_4.setText("S")
                self.db.writeFehlzeiten(
                    self.student_pk, 3, self.datelistweek[3][6], True)
            elif self.button7_4.text() == 'S':
                self.button7_4.setStyleSheet(
                    "background-color: rgb(160, 209, 255);")
                self.button7_4.setText("Q")
                self.db.writeFehlzeiten(
                    self.student_pk, 4, self.datelistweek[3][6], True)
            elif self.button7_4.text() == 'Q':
                self.button7_4.setStyleSheet("")
                self.button7_4.setText("")
                self.db.writeFehlzeiten(
                    self.student_pk, 0, self.datelistweek[3][6], True)
            self.countfz()
        else:
            if val == "1":
                self.button7_4.setStyleSheet(
                    "background-color: rgb(216, 109, 109);")
                self.button7_4.setText("u")
            if val == "2":
                self.button7_4.setStyleSheet(
                    "background-color: rgb(89, 209, 117);")
                self.button7_4.setText("e")
            if val == "3":
                self.button7_4.setStyleSheet(
                    "background-color: rgb(255, 255, 127);")
                self.button7_4.setText("S")
            if val == "4":
                self.button7_4.setStyleSheet(
                    "background-color: rgb(160, 209, 255);")
                self.button7_4.setText("Q")

    def set7_5(self, val=None):
        if val is False:
            if self.button7_5.text() == '':
                self.button7_5.setStyleSheet(
                    "background-color: rgb(216, 109, 109);")
                self.button7_5.setText("u")
                self.db.writeFehlzeiten(
                    self.student_pk, 1, self.datelistweek[4][6], True)
            elif self.button7_5.text() == 'u':
                self.button7_5.setStyleSheet(
                    "background-color: rgb(89, 209, 117);")
                self.button7_5.setText("e")
                self.db.writeFehlzeiten(
                    self.student_pk, 2, self.datelistweek[4][6], True)
            elif self.button7_5.text() == 'e':
                self.button7_5.setStyleSheet(
                    "background-color: rgb(255, 255, 127);")
                self.button7_5.setText("S")
                self.db.writeFehlzeiten(
                    self.student_pk, 3, self.datelistweek[4][6], True)
            elif self.button7_5.text() == 'S':
                self.button7_5.setStyleSheet(
                    "background-color: rgb(160, 209, 255);")
                self.button7_5.setText("Q")
                self.db.writeFehlzeiten(
                    self.student_pk, 4, self.datelistweek[4][6], True)
            elif self.button7_5.text() == 'Q':
                self.button7_5.setStyleSheet("")
                self.button7_5.setText("")
                self.db.writeFehlzeiten(
                    self.student_pk, 0, self.datelistweek[4][6], True)
            self.countfz()
        else:
            if val == "1":
                self.button7_5.setStyleSheet(
                    "background-color: rgb(216, 109, 109);")
                self.button7_5.setText("u")
            if val == "2":
                self.button7_5.setStyleSheet(
                    "background-color: rgb(89, 209, 117);")
                self.button7_5.setText("e")
            if val == "3":
                self.button7_5.setStyleSheet(
                    "background-color: rgb(255, 255, 127);")
                self.button7_5.setText("S")
            if val == "4":
                self.button7_5.setStyleSheet(
                    "background-color: rgb(160, 209, 255);")
                self.button7_5.setText("Q")

    def resetButtons(self):
        """ setzt alle Fehlzeiten-Buttons zurück"""
        self.button1_1.setStyleSheet("")
        self.button1_1.setText("")
        self.button1_2.setStyleSheet("")
        self.button1_2.setText("")
        self.button1_3.setStyleSheet("")
        self.button1_3.setText("")
        self.button1_4.setStyleSheet("")
        self.button1_4.setText("")
        self.button1_5.setStyleSheet("")
        self.button1_5.setText("")

        self.button2_1.setStyleSheet("")
        self.button2_1.setText("")
        self.button2_2.setStyleSheet("")
        self.button2_2.setText("")
        self.button2_3.setStyleSheet("")
        self.button2_3.setText("")
        self.button2_4.setStyleSheet("")
        self.button2_4.setText("")
        self.button2_5.setStyleSheet("")
        self.button2_5.setText("")

        self.button3_1.setStyleSheet("")
        self.button3_1.setText("")
        self.button3_2.setStyleSheet("")
        self.button3_2.setText("")
        self.button3_3.setStyleSheet("")
        self.button3_3.setText("")
        self.button3_4.setStyleSheet("")
        self.button3_4.setText("")
        self.button3_5.setStyleSheet("")
        self.button3_5.setText("")

        self.button4_1.setStyleSheet("")
        self.button4_1.setText("")
        self.button4_2.setStyleSheet("")
        self.button4_2.setText("")
        self.button4_3.setStyleSheet("")
        self.button4_3.setText("")
        self.button4_4.setStyleSheet("")
        self.button4_4.setText("")
        self.button4_5.setStyleSheet("")
        self.button4_5.setText("")

        self.button5_1.setStyleSheet("")
        self.button5_1.setText("")
        self.button5_2.setStyleSheet("")
        self.button5_2.setText("")
        self.button5_3.setStyleSheet("")
        self.button5_3.setText("")
        self.button5_4.setStyleSheet("")
        self.button5_4.setText("")
        self.button5_5.setStyleSheet("")
        self.button5_5.setText("")

        self.button6_1.setStyleSheet("")
        self.button6_1.setText("")
        self.button6_2.setStyleSheet("")
        self.button6_2.setText("")
        self.button6_3.setStyleSheet("")
        self.button6_3.setText("")
        self.button6_4.setStyleSheet("")
        self.button6_4.setText("")
        self.button6_5.setStyleSheet("")
        self.button6_5.setText("")

        self.button7_1.setStyleSheet("")
        self.button7_1.setText("")
        self.button7_2.setStyleSheet("")
        self.button7_2.setText("")
        self.button7_3.setStyleSheet("")
        self.button7_3.setText("")
        self.button7_4.setStyleSheet("")
        self.button7_4.setText("")
        self.button7_5.setStyleSheet("")
        self.button7_5.setText("")

    def countfz(self, event=None, student=None):
        if student is None:
            columns = self.db.getSFehlzeiten(self.student_pk)
        else:
            columns = self.db.getSFehlzeiten(student)

        u = 0
        e = 0
        u_2 = 0
        e_2 = 0
        if event is None:
            try:
                datelist = self.db.getTutmodDatePreset(self.klasse).split(",")
                self.dateEdit.setDate(
                    QtCore.QDate.fromString(datelist[0], "yyyy-MM-dd"))
                self.dateEdit_2.setDate(
                    QtCore.QDate.fromString(datelist[1], "yyyy-MM-dd"))
                self.dateEdit_3.setDate(
                    QtCore.QDate.fromString(datelist[2], "yyyy-MM-dd"))
                self.dateEdit_4.setDate(
                    QtCore.QDate.fromString(datelist[3], "yyyy-MM-dd"))
            except Exception:
                pass
        for i in range(len(columns[1])):
            if i >= 6:
                start = datetime.strptime(
                    str(self.dateEdit.date().toPyDate()), "%Y-%m-%d")
                end = datetime.strptime(
                    str(self.dateEdit_2.date().toPyDate()), "%Y-%m-%d")
                date = datetime.strptime(
                    columns[1][i][1].split("_")[0], "%Y-%m-%d")
                if start <= date <= end:
                    if columns[0][0][i] == "1":
                        u += 1
                    if columns[0][0][i] == "2":
                        e += 1
                start_2 = datetime.strptime(
                    str(self.dateEdit_3.date().toPyDate()), "%Y-%m-%d")
                end_2 = datetime.strptime(
                    str(self.dateEdit_4.date().toPyDate()), "%Y-%m-%d")
                date = datetime.strptime(
                    columns[1][i][1].split("_")[0], "%Y-%m-%d")
                if start_2 <= date <= end_2:
                    if columns[0][0][i] == "1":
                        u_2 += 1
                    if columns[0][0][i] == "2":
                        e_2 += 1
        if student is None:
            self.label_16.setText(str(e))
            self.label_17.setText(str(u))
            self.label_19.setText(str(u+e))
            self.label_22.setText(str(e_2))
            self.label_23.setText(str(u_2))
            self.label_25.setText(str(u_2+e_2))
        else:
            g = u+e
            g_2 = u_2+e_2
            return g, u, g_2, u_2
        datelist = str(self.dateEdit.date().toPyDate())+","+str(self.dateEdit_2.date().toPyDate()) + \
            ","+str(self.dateEdit_3.date().toPyDate())+"," + \
            str(self.dateEdit_4.date().toPyDate())
        self.db.writeTutmodDatePreset(self.klasse, datelist)

    def block(self):
        self.blockdial = Block(self.db, self.student_pk, self)

    def getKlassenFehlz_1(self):
        fzlist = [("Nr.", "Nachname", "Vorname", "Fehlstunden gesamt",
                   "davon unentschuldigt")]
        z = 0
        for i in self.filtered:
            z += 1
            liste = self.countfz(None, i[2])
            fzlist.append((z, i[0], i[1], liste[0], liste[1]))

        reportFehlz.makeFzUebersicht(fzlist, self.db.dbpath, self.klasse,
                                     "1. Halbjahr")

    def getKlassenFehlz_2(self):
        fzlist = [("Nr.", "Nachname", "Vorname", "Fehlstunden gesamt",
                   "davon unentschuldigt")]
        z = 0
        for i in self.filtered:
            z += 1
            liste = self.countfz(None, i[2])
            fzlist.append((z, i[0], i[1], liste[2], liste[3]))
        reportFehlz.makeFzUebersicht(fzlist, self.db.dbpath, self.klasse,
                                     "2. Halbjahr")


class Block(Ui_BlockKomp, QtWidgets.QDialog):
    def __init__(self, db, spk, tut):
        super(Block, self).__init__(tut)
        self.db = db
        self.student_pk = spk
        self.tutmod = tut
        self.setupUi(self)
        self.show()
        self.getBlockKomp()

    def getBlockKomp(self):
        # Liste der Blockkompensationen holen
        # TODO: Datumsbereich der Halbjahre berücksichtigen
        liste = self.db.getBlockkomp(self.student_pk)

        z = 0
        for i in liste:
            self.label = QtWidgets.QLabel(self.scrollAreaWidgetContents)
            self.label.setAlignment(
                QtCore.Qt.AlignLeading |
                QtCore.Qt.AlignLeft |
                QtCore.Qt.AlignVCenter)
            self.label.setObjectName("label_" + str(z))
            self.gridLayout.addWidget(self.label, z, 0, 1, 1)
            self.button = QtWidgets.QPushButton(self.scrollAreaWidgetContents)
            sizePolicy = QtWidgets.QSizePolicy(
                QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
            sizePolicy.setHorizontalStretch(0)
            sizePolicy.setVerticalStretch(0)
            sizePolicy.setHeightForWidth(
                self.button.sizePolicy().hasHeightForWidth())
            self.button.setSizePolicy(sizePolicy)
            self.button.setMinimumSize(QtCore.QSize(40, 40))
            self.button.setMaximumSize(QtCore.QSize(40, 40))
            # self.button.setText(i[1])
            # self.button.setObjectName("button_" + str(z) + str(i))
            self.button.setObjectName(str(i[1]) + "," + str(i[2]))
            self.label.setText(i[0])
            self.gridLayout.addWidget(self.button, z, 1, 1, 1)
            z += 1

            if i[1] == "1":
                self.button.setStyleSheet(
                    "background-color: rgb(216, 109, 109);")
                self.button.setText("u")
            elif i[1] == "2":
                self.button.setStyleSheet(
                    "background-color: rgb(89, 209, 117);")
                self.button.setText("e")
            elif i[1] == "3":
                self.button.setStyleSheet(
                    "background-color: rgb(255, 255, 127);")
                self.button.setText("S")
            elif i[1] == "4":
                self.button.setStyleSheet(
                    "background-color: rgb(160, 209, 255);")
                self.button.setText("Q")

            self.button.clicked.connect(self.click)

    def click(self):
        sender = self.button.sender().objectName()
        sender = sender.split(",")
        f = int(sender[0])
        if f == 4:
            f = 0
        else:
            f += 1
        # Änderung in DB schreiben
        self.db.writeFehlzeiten(self.student_pk, f, sender[1])
        # Ansicht aktualisieren TODO: Inhalte liegen übereinander
        self.getBlockKomp()
        self.tutmod.countfz()
