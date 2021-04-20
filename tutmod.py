
from calendar import Calendar
from datetime import date, timedelta, datetime
from PyQt5 import QtCore, QtGui, QtWidgets
from Tutmodgui import Ui_Tutmodgui
import locale

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

        self.set_cur_year_month()
        self.setMonth(True)
        self.tableWidget.setColumnWidth(0,180)

        self.comboBoxKlasse.activated.connect(self.zeigeKlasse)
        self.comboBoxMonat.activated.connect(self.setMonth)
        self.dateEditJahr.dateChanged.connect(self.setMonth)
        self.pushButtonWeekafter.clicked.connect(self.weekafter)
        self.pushButtonWeekbefore.clicked.connect(self.weekbefore)
        self.tableWidget.clicked.connect(self.set_fehlzeiten)


    def zeigeKlasse(self):
        """ Zeigt die Liste der Schüler der ausgewählten Klasse """

        # gefilterte Liste bei jedem Aufruf leer bereitstellen
        self.filtered = []

        # ausgewählte Klasse
        klasse = self.comboBoxKlasse.currentText()
        print(klasse)

        # Filtern nach Klasse
        alle = self.db.getGesamtliste()
        z = 0
        for i in alle:
            if i[3] == klasse:
                self.tableWidget.setRowCount(z+1)
                self.tableWidget.setItem(
                    z,0,QtWidgets.QTableWidgetItem(i[1]+", "+i[2]))
                self.tableWidget.setItem(z,1,QtWidgets.QTableWidgetItem(i[3]))
                self.filtered.append([i[1], i[2], i[0], i[3]])
                z += 1
        #print(self.filtered)



    def set_cur_year_month(self):
        self.dateEditJahr.setDate(QtCore.QDate(date.today().year,1,1))
        self.comboBoxMonat.setCurrentText(datetime.now().strftime("%B"))

    def fillTableWidget(self):
        """ füllt die Schülernamen der gewählten Klasse ein"""
        pass

    def setMonth(self, set=True):
        y = str(self.dateEditJahr.date().toPyDate())
        y = y.split("-")
        y = int(y[0])
        print("Jahr",y)
        self.m = int(self.comboBoxMonat.currentIndex())+1
        print("Monat: ",self.m)

        cal = Calendar()

        self.weeks = []
        w = 0
        currentweek = 0
        for week in cal.monthdatescalendar(y,self.m):
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
                pass
            else:
                self.weeks.append(oneweek)
            w += 1
        if set==True:
            # Wenn zu Beginn aus datensatz_anzeigen aufgerufen, 
            # aktuelle Woche setzen
            self.weekno = currentweek
            print("aktuelle Wochennummer", self.weekno)
            print(self.weeks)
            self.weekafter(True)
        elif set=="withlast":
            # bei Button mit der letzten Woche beginnen
            self.weekno = len(self.weeks)
        else:
            # mit anderem Monat aus Auswahl starten
            self.weekno = -1
            self.weekafter()


    def weekbefore(self):
        self.resetButtons()
        self.weekno -= 1
        self.set_weeks()
        #self.label_Woche.config(text=self.weeks[self.weekno][0].split("-")[2]+"."+self.weeks[self.weekno][0].split("-")[1]+"."+" bis "+self.weeks[self.weekno][4].split("-")[2]+"."+self.weeks[self.weekno][4].split("-")[1]+".")
        #self.label_Mo_date.config(text=self.weeks[self.weekno][0].split("-")[2]+"."+self.weeks[self.weekno][0].split("-")[1]+".")
        #self.label_Di_date.config(text=self.weeks[self.weekno][1].split("-")[2]+"."+self.weeks[self.weekno][1].split("-")[1]+".")
        #self.label_Mi_date.config(text=self.weeks[self.weekno][2].split("-")[2]+"."+self.weeks[self.weekno][2].split("-")[1]+".")
        #self.label_Do_date.config(text=self.weeks[self.weekno][3].split("-")[2]+"."+self.weeks[self.weekno][3].split("-")[1]+".")
        #self.label_Fr_date.config(text=self.weeks[self.weekno][4].split("-")[2]+"."+self.weeks[self.weekno][4].split("-")[1]+".")

        self.set_fehlzeiten()

    def weekafter(self, set=None):
        if self.weekno+1 <= len(self.weeks)-1:
            self.resetButtons()
            # wenn zu Beginn aus setmonth aufgerufen, aktuelle Woche benutzen
            if set==True:
                # nichts tun und self.weekno benutzen
                pass
            else:    
                # Button wurde gedrückt, eine Woche weiter
                self.weekno += 1

            self.set_weeks()
            """
            self.label_Woche.setText(
                     self.weeks[self.weekno][0].split("-")[2]+"."+
                     self.weeks[self.weekno][0].split("-")[1]+"."+" bis "+
                     self.weeks[self.weekno][4].split("-")[2]+"."+
                     self.weeks[self.weekno][4].split("-")[1]+".")
            self.label_Mo.setText(
                     self.weeks[self.weekno][0].split("-")[2]+"."+
                     self.weeks[self.weekno][0].split("-")[1]+".")
            self.label_Di.setText(
                     self.weeks[self.weekno][1].split("-")[2]+"."+
                     self.weeks[self.weekno][1].split("-")[1]+".")
            self.label_Mi.setText(
                     self.weeks[self.weekno][2].split("-")[2]+"."+
                     self.weeks[self.weekno][2].split("-")[1]+".")
            self.label_Do.setText(
                     self.weeks[self.weekno][3].split("-")[2]+"."+
                     self.weeks[self.weekno][3].split("-")[1]+".")
            self.label_Fr.setText(
                     self.weeks[self.weekno][4].split("-")[2]+"."+
                     self.weeks[self.weekno][4].split("-")[1]+".")
            """
            #self.set_buchungen()
        # Wenn am Ende der Wochenliste angekommen, in nächsten Monat wechseln
        else:
            nextmonth = self.comboBoxMonat.currentIndex()+2
            print(nextmonth)
            if nextmonth <= 12:
                monat = date(9999,nextmonth,1).strftime("%B")
                print(monat)
                self.comboBoxMonat.setCurrentText(monat)
            else:
                nextmonth = 1
                monat = date(9999,nextmonth,1).strftime("%B")
                self.comboBoxMonat.setCurrentText(monat)
                # neues Jahr setzen
                nextyear = self.dateEditJahr.date().toPyDate()
                nextyear = str(nextyear).split("-")
                nextyear = int(nextyear[0])+1
                self.dateEditJahr.setDate(QtCore.QDate(nextyear,1,1))
            # Datum des aktuellen Montags speichern
            aktmo = self.label_Mo.text()
            print(aktmo)
            # neuen Monat setzen
            self.setMonth()
            # wenn der neue Montag in der gleichen Woche liegt, noch eine 
            # Woche vor
            if aktmo == self.label_Mo.text():
                self.weekafter()
        if set == True:
            pass
        else:
            self.set_fehlzeiten()

    def set_weeks(self):
        self.label_Woche.setText(
                    self.weeks[self.weekno][0].split("-")[2]+"."+
                    self.weeks[self.weekno][0].split("-")[1]+"."+" bis "+
                    self.weeks[self.weekno][4].split("-")[2]+"."+
                    self.weeks[self.weekno][4].split("-")[1]+".")
        self.label_Mo.setText(
                    self.weeks[self.weekno][0].split("-")[2]+"."+
                    self.weeks[self.weekno][0].split("-")[1]+".")
        self.label_Di.setText(
                    self.weeks[self.weekno][1].split("-")[2]+"."+
                    self.weeks[self.weekno][1].split("-")[1]+".")
        self.label_Mi.setText(
                    self.weeks[self.weekno][2].split("-")[2]+"."+
                    self.weeks[self.weekno][2].split("-")[1]+".")
        self.label_Do.setText(
                    self.weeks[self.weekno][3].split("-")[2]+"."+
                    self.weeks[self.weekno][3].split("-")[1]+".")
        self.label_Fr.setText(
                    self.weeks[self.weekno][4].split("-")[2]+"."+
                    self.weeks[self.weekno][4].split("-")[1]+".")

    def set_fehlzeiten(self):
        """Führt alle set-Methoden aus, indem vorher die Liste aus der db
        geholt wird und den Methoden u oder e oder ""? übergeben wird """
        
        # Button reset
        self.resetButtons()

        # Schüler-pk setzen
        auswahl = int(self.tableWidget.currentRow())
        self.student_pk = self.filtered[auswahl][2]
        print(self.student_pk)

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
            datelist.append('"'+i+"_1"'"')
            datelist.append('"'+i+"_2"'"')
            datelist.append('"'+i+"_3"'"')
            datelist.append('"'+i+"_4"'"')
            datelist.append('"'+i+"_5"'"')
            datelist.append('"'+i+"_6"'"')
            datelist.append('"'+i+"_7"'"')
            self.datelistweek.append(datelist)
            for d in datelist:
                item = list(self.db.susc.execute("""SELECT """+d+""" 
                                                FROM "sus"
                                                WHERE pk = ?;
                                            """,
                                            (self.student_pk,)))
                fehlzlist.append(item)
            
            setlist.append(fehlzlist)
        
        # DB-Verindung schließen
        # c.close()
        # verbindung.close()
        
        #print(setlist[0][0][0][0])
        #print(self.datelistweek)
        print(setlist[0][0][0][0])
        
        # set-Methoden aufrufen

        self.set1_1(setlist[0][0][0][0])
        # self.set1_2(setlist[1][0][0][0])
        # self.set1_3(setlist[2][0][0][0])
        # self.set1_4(setlist[3][0][0][0])
        # self.set1_5(setlist[4][0][0][0])
       
        # self.set2_1(setlist[0][1][0][0])
        # self.set2_2(setlist[1][1][0][0])
        # self.set2_3(setlist[2][1][0][0])
        # self.set2_4(setlist[3][1][0][0])
        # self.set2_5(setlist[4][1][0][0])

        # self.set3_1(setlist[0][2][0][0])
        # self.set3_2(setlist[1][2][0][0])
        # self.set3_3(setlist[2][2][0][0])
        # self.set3_4(setlist[3][2][0][0])
        # self.set3_5(setlist[4][2][0][0])

        # self.set4_1(setlist[0][3][0][0])
        # self.set4_2(setlist[1][3][0][0])
        # self.set4_3(setlist[2][3][0][0])
        # self.set4_4(setlist[3][3][0][0])
        # self.set4_5(setlist[4][3][0][0])

        # self.set5_1(setlist[0][4][0][0])
        # self.set5_2(setlist[1][4][0][0])
        # self.set5_3(setlist[2][4][0][0])
        # self.set5_4(setlist[3][4][0][0])
        # self.set5_5(setlist[4][4][0][0])

        # self.set6_1(setlist[0][5][0][0])
        # self.set6_2(setlist[1][5][0][0])
        # self.set6_3(setlist[2][5][0][0])
        # self.set6_4(setlist[3][5][0][0])
        # self.set6_5(setlist[4][5][0][0])

        # self.set7_1(setlist[0][6][0][0])
        # self.set7_2(setlist[1][6][0][0])
        # self.set7_3(setlist[2][6][0][0])
        # self.set7_4(setlist[3][6][0][0])
        # self.set7_5(setlist[4][6][0][0])


    def set1_1(self, val=None):
        if val == None:
            if self.button1_1.config('text')[4] == '':
                self.button1_1.config(background='#f5010a', text='u')
                self.writeFehlzeit(self.datelistweek[0][0],1)
            elif self.button1_1.config('text')[4] == 'u':
                self.button1_1.config(background='#00e100', text='e')
                self.writeFehlzeit(self.datelistweek[0][0],2)
            elif self.button1_1.config('text')[4] == 'e':
                self.button1_1.config(background='#ffff80', text='S')
                self.writeFehlzeit(self.datelistweek[0][0],3)
            elif self.button1_1.config('text')[4] == 'S':
                self.button1_1.config(background='#c0c0c0', text='')
                self.writeFehlzeit(self.datelistweek[0][0],0)
        else:
            if val == "1":
                #self.button1_1.config(background='#f5010a', text='u')
                self.button1_1.setStyleSheet("background-color: rgb(216, 109, 109);")
                self.button1_1.setText("U")
            if val == 2:
                self.button1_1.config(background='#00e100', text='e')
            if val == 3:
                self.button1_1.config(background='#ffff80', text='S')
            else:
                pass
    def set1_2(self, val=None):
        if val == None:
            if self.button1_2.config('text')[4] == '':
                self.button1_2.config(background='#f5010a', text='u')
                self.writeFehlzeit(self.datelistweek[1][0],1)
            elif self.button1_2.config('text')[4] == 'u':
                self.button1_2.config(background='#00e100', text='e')
                self.writeFehlzeit(self.datelistweek[1][0],2)
            elif self.button1_2.config('text')[4] == 'e':
                self.button1_2.config(background='#ffff80', text='S')
                self.writeFehlzeit(self.datelistweek[1][0],3)
            elif self.button1_2.config('text')[4] == 'S':
                self.button1_2.config(background='#c0c0c0', text='')
                self.writeFehlzeit(self.datelistweek[1][0],0)
        else:
            if val == 1:
                self.button1_2.config(background='#f5010a', text='u')
            if val == 2:
                self.button1_2.config(background='#00e100', text='e')
            if val == 3:
                self.button1_2.config(background='#ffff80', text='S')
            else:
                pass                   
    def set1_3(self, val=None):
        if val == None:
            if self.button1_3.config('text')[4] == '':
                self.button1_3.config(background='#f5010a', text='u')
                self.writeFehlzeit(self.datelistweek[2][0],1)
            elif self.button1_3.config('text')[4] == 'u':
                self.button1_3.config(background='#00e100', text='e')
                self.writeFehlzeit(self.datelistweek[2][0],2)
            elif self.button1_3.config('text')[4] == 'e':
                self.button1_3.config(background='#ffff80', text='S')
                self.writeFehlzeit(self.datelistweek[2][0],3)
            elif self.button1_3.config('text')[4] == 'S':
                self.button1_3.config(background='#c0c0c0', text='')
                self.writeFehlzeit(self.datelistweek[2][0],0)
        else:
            if val == 1:
                self.button1_3.config(background='#f5010a', text='u')
            if val == 2:
                self.button1_3.config(background='#00e100', text='e')
            if val == 3:
                self.button1_3.config(background='#ffff80', text='S')
            else:
                pass                   
    def set1_4(self, val=None):
        if val == None:
            if self.button1_4.config('text')[4] == '':
                self.button1_4.config(background='#f5010a', text='u')
                self.writeFehlzeit(self.datelistweek[3][0],1)
            elif self.button1_4.config('text')[4] == 'u':
                self.button1_4.config(background='#00e100', text='e')
                self.writeFehlzeit(self.datelistweek[3][0],2)
            elif self.button1_4.config('text')[4] == 'e':
                self.button1_4.config(background='#ffff80', text='S')
                self.writeFehlzeit(self.datelistweek[3][0],3)
            elif self.button1_4.config('text')[4] == 'S':
                self.button1_4.config(background='#c0c0c0', text='')
                self.writeFehlzeit(self.datelistweek[3][0],0)
        else:
            if val == 1:
                self.button1_4.config(background='#f5010a', text='u')
            if val == 2:
                self.button1_4.config(background='#00e100', text='e')
            if val == 3:
                self.button1_4.config(background='#ffff80', text='S')
            else:
                pass                   
    def set1_5(self, val=None):
        if val == None:
            if self.button1_5.config('text')[4] == '':
                self.button1_5.config(background='#f5010a', text='u')
                self.writeFehlzeit(self.datelistweek[4][0],1)
            elif self.button1_5.config('text')[4] == 'u':
                self.button1_5.config(background='#00e100', text='e')
                self.writeFehlzeit(self.datelistweek[4][0],2)
            elif self.button1_5.config('text')[4] == 'e':
                self.button1_5.config(background='#ffff80', text='S')
                self.writeFehlzeit(self.datelistweek[4][0],3)
            elif self.button1_5.config('text')[4] == 'S':
                self.button1_5.config(background='#c0c0c0', text='')
                self.writeFehlzeit(self.datelistweek[4][0],0)
        else:
            if val == 1:
                self.button1_5.config(background='#f5010a', text='u')
            if val == 2:
                self.button1_5.config(background='#00e100', text='e')
            if val == 3:
                self.button1_5.config(background='#ffff80', text='S')
            else:
                pass                     
    def set2_1(self, val=None):
        if val == None:
            if self.button2_1.config('text')[4] == '':
                self.button2_1.config(background='#f5010a', text='u')
                self.writeFehlzeit(self.datelistweek[0][1],1)
            elif self.button2_1.config('text')[4] == 'u':
                self.button2_1.config(background='#00e100', text='e')
                self.writeFehlzeit(self.datelistweek[0][1],2)
            elif self.button2_1.config('text')[4] == 'e':
                self.button2_1.config(background='#ffff80', text='S')
                self.writeFehlzeit(self.datelistweek[0][1],3)
            elif self.button2_1.config('text')[4] == 'S':
                self.button2_1.config(background='#c0c0c0', text='')
                self.writeFehlzeit(self.datelistweek[0][1],0)
        else:
            if val == 1:
                self.button2_1.config(background='#f5010a', text='u')
            if val == 2:
                self.button2_1.config(background='#00e100', text='e')
            if val == 3:
                self.button2_1.config(background='#ffff80', text='S')
            else:
                pass                     
    def set2_2(self, val=None):
        if val == None:
            if self.button2_2.config('text')[4] == '':
                self.button2_2.config(background='#f5010a', text='u')
                self.writeFehlzeit(self.datelistweek[1][1],1)
            elif self.button2_2.config('text')[4] == 'u':
                self.button2_2.config(background='#00e100', text='e')
                self.writeFehlzeit(self.datelistweek[1][1],2)
            elif self.button2_2.config('text')[4] == 'e':
                self.button2_2.config(background='#ffff80', text='S')
                self.writeFehlzeit(self.datelistweek[1][1],3)
            elif self.button2_2.config('text')[4] == 'S':
                self.button2_2.config(background='#c0c0c0', text='')
                self.writeFehlzeit(self.datelistweek[1][1],0)
        else:
            if val == 1:
                self.button2_2.config(background='#f5010a', text='u')
            if val == 2:
                self.button2_2.config(background='#00e100', text='e')
            if val == 3:
                self.button2_2.config(background='#ffff80', text='S')
            else:
                pass                     
    def set2_3(self, val=None):
        if val == None:
            if self.button2_3.config('text')[4] == '':
                self.button2_3.config(background='#f5010a', text='u')
                self.writeFehlzeit(self.datelistweek[2][1],1)
            elif self.button2_3.config('text')[4] == 'u':
                self.button2_3.config(background='#00e100', text='e')
                self.writeFehlzeit(self.datelistweek[2][1],2)
            elif self.button2_3.config('text')[4] == 'e':
                self.button2_3.config(background='#ffff80', text='S')
                self.writeFehlzeit(self.datelistweek[2][1],3)
            elif self.button2_3.config('text')[4] == 'S':
                self.button2_3.config(background='#c0c0c0', text='')
                self.writeFehlzeit(self.datelistweek[2][1],0)
        else:
            if val == 1:
                self.button2_3.config(background='#f5010a', text='u')
            if val == 2:
                self.button2_3.config(background='#00e100', text='e')
            if val == 3:
                self.button2_3.config(background='#ffff80', text='S')
            else:
                pass                     
    def set2_4(self, val=None):
        if val == None:
            if self.button2_4.config('text')[4] == '':
                self.button2_4.config(background='#f5010a', text='u')
                self.writeFehlzeit(self.datelistweek[3][1],1)
            elif self.button2_4.config('text')[4] == 'u':
                self.button2_4.config(background='#00e100', text='e')
                self.writeFehlzeit(self.datelistweek[3][1],2)
            elif self.button2_4.config('text')[4] == 'e':
                self.button2_4.config(background='#ffff80', text='S')
                self.writeFehlzeit(self.datelistweek[3][1],3)
            elif self.button2_4.config('text')[4] == 'S':
                self.button2_4.config(background='#c0c0c0', text='')
                self.writeFehlzeit(self.datelistweek[3][1],0)
        else:
            if val == 1:
                self.button2_4.config(background='#f5010a', text='u')
            if val == 2:
                self.button2_4.config(background='#00e100', text='e')
            if val == 3:
                self.button2_4.config(background='#ffff80', text='S')
            else:
                pass                     
    def set2_5(self, val=None):
        if val == None:
            if self.button2_5.config('text')[4] == '':
                self.button2_5.config(background='#f5010a', text='u')
                self.writeFehlzeit(self.datelistweek[4][1],1)
            elif self.button2_5.config('text')[4] == 'u':
                self.button2_5.config(background='#00e100', text='e')
                self.writeFehlzeit(self.datelistweek[4][1],2)
            elif self.button2_5.config('text')[4] == 'e':
                self.button2_5.config(background='#ffff80', text='S')
                self.writeFehlzeit(self.datelistweek[4][1],3)
            elif self.button2_5.config('text')[4] == 'S':
                self.button2_5.config(background='#c0c0c0', text='')
                self.writeFehlzeit(self.datelistweek[4][1],0)
        else:
            if val == 1:
                self.button2_5.config(background='#f5010a', text='u')
            if val == 2:
                self.button2_5.config(background='#00e100', text='e')
            if val == 3:
                self.button2_5.config(background='#ffff80', text='S')
            else:
                pass                
    def set3_1(self, val=None):
        if val == None:
            if self.button3_1.config('text')[4] == '':
                self.button3_1.config(background='#f5010a', text='u')
                self.writeFehlzeit(self.datelistweek[0][2],1)
            elif self.button3_1.config('text')[4] == 'u':
                self.button3_1.config(background='#00e100', text='e')
                self.writeFehlzeit(self.datelistweek[0][2],2)
            elif self.button3_1.config('text')[4] == 'e':
                self.button3_1.config(background='#ffff80', text='S')
                self.writeFehlzeit(self.datelistweek[0][2],3)
            elif self.button3_1.config('text')[4] == 'S':
                self.button3_1.config(background='#c0c0c0', text='')
                self.writeFehlzeit(self.datelistweek[0][2],0)
        else:
            if val == 1:
                self.button3_1.config(background='#f5010a', text='u')
            if val == 2:
                self.button3_1.config(background='#00e100', text='e')
            if val == 3:
                self.button3_1.config(background='#ffff80', text='S')
            else:
                pass            
    def set3_2(self, val=None):
        if val == None:
            if self.button3_2.config('text')[4] == '':
                self.button3_2.config(background='#f5010a', text='u')
                self.writeFehlzeit(self.datelistweek[1][2],1)
            elif self.button3_2.config('text')[4] == 'u':
                self.button3_2.config(background='#00e100', text='e')
                self.writeFehlzeit(self.datelistweek[1][2],2)
            elif self.button3_2.config('text')[4] == 'e':
                self.button3_2.config(background='#ffff80', text='S')
                self.writeFehlzeit(self.datelistweek[1][2],3)
            elif self.button3_2.config('text')[4] == 'S':
                self.button3_2.config(background='#c0c0c0', text='')
                self.writeFehlzeit(self.datelistweek[1][2],0)
        else:
            if val == 1:
                self.button3_2.config(background='#f5010a', text='u')
            if val == 2:
                self.button3_2.config(background='#00e100', text='e')
            if val == 3:
                self.button3_2.config(background='#ffff80', text='S')
            else:
                pass                
    def set3_3(self, val=None):
        if val == None:
            if self.button3_3.config('text')[4] == '':
                self.button3_3.config(background='#f5010a', text='u')
                self.writeFehlzeit(self.datelistweek[2][2],1)
            elif self.button3_3.config('text')[4] == 'u':
                self.button3_3.config(background='#00e100', text='e')
                self.writeFehlzeit(self.datelistweek[2][2],2)
            elif self.button3_3.config('text')[4] == 'e':
                self.button3_3.config(background='#ffff80', text='S')
                self.writeFehlzeit(self.datelistweek[2][2],3)
            elif self.button3_3.config('text')[4] == 'S':
                self.button3_3.config(background='#c0c0c0', text='')
                self.writeFehlzeit(self.datelistweek[2][2],0)
        else:
            if val == 1:
                self.button3_3.config(background='#f5010a', text='u')
            if val == 2:
                self.button3_3.config(background='#00e100', text='e')
            if val == 3:
                self.button3_3.config(background='#ffff80', text='S')
            else:
                pass
    def set3_4(self, val=None):
        if val == None:
            if self.button3_4.config('text')[4] == '':
                self.button3_4.config(background='#f5010a', text='u')
                self.writeFehlzeit(self.datelistweek[3][2],1)
            elif self.button3_4.config('text')[4] == 'u':
                self.button3_4.config(background='#00e100', text='e')
                self.writeFehlzeit(self.datelistweek[3][2],2)
            elif self.button3_4.config('text')[4] == 'e':
                self.button3_4.config(background='#ffff80', text='S')
                self.writeFehlzeit(self.datelistweek[3][2],3)
            elif self.button3_4.config('text')[4] == 'S':
                self.button3_4.config(background='#c0c0c0', text='')
                self.writeFehlzeit(self.datelistweek[3][2],0)
        else:
            if val == 1:
                self.button3_4.config(background='#f5010a', text='u')
            if val == 2:
                self.button3_4.config(background='#00e100', text='e')
            if val == 3:
                self.button3_4.config(background='#ffff80', text='S')
            else:
                pass
    def set3_5(self, val=None):
        if val == None:
            if self.button3_5.config('text')[4] == '':
                self.button3_5.config(background='#f5010a', text='u')
                self.writeFehlzeit(self.datelistweek[4][2],1)
            elif self.button3_5.config('text')[4] == 'u':
                self.button3_5.config(background='#00e100', text='e')
                self.writeFehlzeit(self.datelistweek[4][2],2)
            elif self.button3_5.config('text')[4] == 'e':
                self.button3_5.config(background='#ffff80', text='S')
                self.writeFehlzeit(self.datelistweek[4][2],3)
            elif self.button3_5.config('text')[4] == 'S':
                self.button3_5.config(background='#c0c0c0', text='')
                self.writeFehlzeit(self.datelistweek[4][2],0)
        else:
            if val == 1:
                self.button3_5.config(background='#f5010a', text='u')
            if val == 2:
                self.button3_5.config(background='#00e100', text='e')
            if val == 3:
                self.button3_5.config(background='#ffff80', text='S')
            else:
                pass                
    def set4_1(self, val=None):
        if val == None:
            if self.button4_1.config('text')[4] == '':
                self.button4_1.config(background='#f5010a', text='u')
                self.writeFehlzeit(self.datelistweek[0][3],1)
            elif self.button4_1.config('text')[4] == 'u':
                self.button4_1.config(background='#00e100', text='e')
                self.writeFehlzeit(self.datelistweek[0][3],2)
            elif self.button4_1.config('text')[4] == 'e':
                self.button4_1.config(background='#ffff80', text='S')
                self.writeFehlzeit(self.datelistweek[0][3],3)
            elif self.button4_1.config('text')[4] == 'S':
                self.button4_1.config(background='#c0c0c0', text='')
                self.writeFehlzeit(self.datelistweek[0][3],0)
        else:
            if val == 1:
                self.button4_1.config(background='#f5010a', text='u')
            if val == 2:
                self.button4_1.config(background='#00e100', text='e')
            if val == 3:
                self.button4_1.config(background='#ffff80', text='S')
            else:
                pass                
    def set4_2(self, val=None):
        if val == None:
            if self.button4_2.config('text')[4] == '':
                self.button4_2.config(background='#f5010a', text='u')
                self.writeFehlzeit(self.datelistweek[1][3],1)
            elif self.button4_2.config('text')[4] == 'u':
                self.button4_2.config(background='#00e100', text='e')
                self.writeFehlzeit(self.datelistweek[1][3],2)
            elif self.button4_2.config('text')[4] == 'e':
                self.button4_2.config(background='#ffff80', text='S')
                self.writeFehlzeit(self.datelistweek[1][3],3)
            elif self.button4_2.config('text')[4] == 'S':
                self.button4_2.config(background='#c0c0c0', text='')
                self.writeFehlzeit(self.datelistweek[1][3],0)
        else:
            if val == 1:
                self.button4_2.config(background='#f5010a', text='u')
            if val == 2:
                self.button4_2.config(background='#00e100', text='e')
            if val == 3:
                self.button4_2.config(background='#ffff80', text='S')
            else:
                pass                     
    def set4_3(self, val=None):
        if val == None:
            if self.button4_3.config('text')[4] == '':
                self.button4_3.config(background='#f5010a', text='u')
                self.writeFehlzeit(self.datelistweek[2][3],1)
            elif self.button4_3.config('text')[4] == 'u':
                self.button4_3.config(background='#00e100', text='e')
                self.writeFehlzeit(self.datelistweek[2][3],2)
            elif self.button4_3.config('text')[4] == 'e':
                self.button4_3.config(background='#ffff80', text='S')
                self.writeFehlzeit(self.datelistweek[2][3],3)
            elif self.button4_3.config('text')[4] == 'S':
                self.button4_3.config(background='#c0c0c0', text='')
                self.writeFehlzeit(self.datelistweek[2][3],0)
        else:
            if val == 1:
                self.button4_3.config(background='#f5010a', text='u')
            if val == 2:
                self.button4_3.config(background='#00e100', text='e')
            if val == 3:
                self.button4_3.config(background='#ffff80', text='S')
            else:
                pass
    def set4_4(self, val=None):
        if val == None:
            if self.button4_4.config('text')[4] == '':
                self.button4_4.config(background='#f5010a', text='u')
                self.writeFehlzeit(self.datelistweek[3][3],1)
            elif self.button4_4.config('text')[4] == 'u':
                self.button4_4.config(background='#00e100', text='e')
                self.writeFehlzeit(self.datelistweek[3][3],2)
            elif self.button4_4.config('text')[4] == 'e':
                self.button4_4.config(background='#ffff80', text='S')
                self.writeFehlzeit(self.datelistweek[3][3],3)
            elif self.button4_4.config('text')[4] == 'S':
                self.button4_4.config(background='#c0c0c0', text='')
                self.writeFehlzeit(self.datelistweek[3][3],0)
        else:
            if val == 1:
                self.button4_4.config(background='#f5010a', text='u')
            if val == 2:
                self.button4_4.config(background='#00e100', text='e')
            if val == 3:
                self.button4_4.config(background='#ffff80', text='S')
            else:
                pass
    def set4_5(self, val=None):
        if val == None:
            if self.button4_5.config('text')[4] == '':
                self.button4_5.config(background='#f5010a', text='u')
                self.writeFehlzeit(self.datelistweek[4][3],1)
            elif self.button4_5.config('text')[4] == 'u':
                self.button4_5.config(background='#00e100', text='e')
                self.writeFehlzeit(self.datelistweek[4][3],2)
            elif self.button4_5.config('text')[4] == 'e':
                self.button4_5.config(background='#ffff80', text='S')
                self.writeFehlzeit(self.datelistweek[4][3],3)
            elif self.button4_5.config('text')[4] == 'S':
                self.button4_5.config(background='#c0c0c0', text='')
                self.writeFehlzeit(self.datelistweek[4][3],0)
        else:
            if val == 1:
                self.button4_5.config(background='#f5010a', text='u')
            if val == 2:
                self.button4_5.config(background='#00e100', text='e')
            if val == 3:
                self.button4_5.config(background='#ffff80', text='S')
            else:
                pass                     
    def set5_1(self, val=None):
        if val == None:
            if self.button5_1.config('text')[4] == '':
                self.button5_1.config(background='#f5010a', text='u')
                self.writeFehlzeit(self.datelistweek[0][4],1)
            elif self.button5_1.config('text')[4] == 'u':
                self.button5_1.config(background='#00e100', text='e')
                self.writeFehlzeit(self.datelistweek[0][4],2)
            elif self.button5_1.config('text')[4] == 'e':
                self.button5_1.config(background='#ffff80', text='S')
                self.writeFehlzeit(self.datelistweek[0][4],3)
            elif self.button5_1.config('text')[4] == 'S':
                self.button5_1.config(background='#c0c0c0', text='')
                self.writeFehlzeit(self.datelistweek[0][4],0)
        else:
            if val == 1:
                self.button5_1.config(background='#f5010a', text='u')
            if val == 2:
                self.button5_1.config(background='#00e100', text='e')
            if val == 3:
                self.button5_1.config(background='#ffff80', text='S')
            else:
                pass                     
    def set5_2(self, val=None):
        if val == None:
            if self.button5_2.config('text')[4] == '':
                self.button5_2.config(background='#f5010a', text='u')
                self.writeFehlzeit(self.datelistweek[1][4],1)
            elif self.button5_2.config('text')[4] == 'u':
                self.button5_2.config(background='#00e100', text='e')
                self.writeFehlzeit(self.datelistweek[1][4],2)
            elif self.button5_2.config('text')[4] == 'e':
                self.button5_2.config(background='#ffff80', text='S')
                self.writeFehlzeit(self.datelistweek[1][4],3)
            elif self.button5_2.config('text')[4] == 'S':
                self.button5_2.config(background='#c0c0c0', text='')
                self.writeFehlzeit(self.datelistweek[1][4],0)
        else:
            if val == 1:
                self.button5_2.config(background='#f5010a', text='u')
            if val == 2:
                self.button5_2.config(background='#00e100', text='e')
            if val == 3:
                self.button5_2.config(background='#ffff80', text='S')
            else:
                pass                         
    def set5_3(self, val=None):
        if val == None:
            if self.button5_3.config('text')[4] == '':
                self.button5_3.config(background='#f5010a', text='u')
                self.writeFehlzeit(self.datelistweek[2][4],1)
            elif self.button5_3.config('text')[4] == 'u':
                self.button5_3.config(background='#00e100', text='e')
                self.writeFehlzeit(self.datelistweek[2][4],2)
            elif self.button5_3.config('text')[4] == 'e':
                self.button5_3.config(background='#ffff80', text='S')
                self.writeFehlzeit(self.datelistweek[2][4],3)
            elif self.button5_3.config('text')[4] == 'S':
                self.button5_3.config(background='#c0c0c0', text='')
                self.writeFehlzeit(self.datelistweek[2][4],0)
        else:
            if val == 1:
                self.button5_3.config(background='#f5010a', text='u')
            if val == 2:
                self.button5_3.config(background='#00e100', text='e')
            if val == 3:
                self.button5_3.config(background='#ffff80', text='S')
            else:
                pass                         
    def set5_4(self, val=None):
        if val == None:
            if self.button5_4.config('text')[4] == '':
                self.button5_4.config(background='#f5010a', text='u')
                self.writeFehlzeit(self.datelistweek[3][4],1)
            elif self.button5_4.config('text')[4] == 'u':
                self.button5_4.config(background='#00e100', text='e')
                self.writeFehlzeit(self.datelistweek[3][4],2)
            elif self.button5_4.config('text')[4] == 'e':
                self.button5_4.config(background='#ffff80', text='S')
                self.writeFehlzeit(self.datelistweek[3][4],3)
            elif self.button5_4.config('text')[4] == 'S':
                self.button5_4.config(background='#c0c0c0', text='')
                self.writeFehlzeit(self.datelistweek[3][4],0)
        else:
            if val == 1:
                self.button5_4.config(background='#f5010a', text='u')
            if val == 2:
                self.button5_4.config(background='#00e100', text='e')
            if val == 3:
                self.button5_4.config(background='#ffff80', text='S')
            else:
                pass                         
    def set5_5(self, val=None):
        if val == None:
            if self.button5_5.config('text')[4] == '':
                self.button5_5.config(background='#f5010a', text='u')
                self.writeFehlzeit(self.datelistweek[4][4],1)
            elif self.button5_5.config('text')[4] == 'u':
                self.button5_5.config(background='#00e100', text='e')
                self.writeFehlzeit(self.datelistweek[4][4],2)
            elif self.button5_5.config('text')[4] == 'e':
                self.button5_5.config(background='#ffff80', text='S')
                self.writeFehlzeit(self.datelistweek[4][4],3)
            elif self.button5_5.config('text')[4] == 'S':
                self.button5_5.config(background='#c0c0c0', text='')
                self.writeFehlzeit(self.datelistweek[4][4],0)
        else:
            if val == 1:
                self.button5_5.config(background='#f5010a', text='u')
            if val == 2:
                self.button5_5.config(background='#00e100', text='e')
            if val == 3:
                self.button5_5.config(background='#ffff80', text='S')
            else:
                pass                         
    def set6_1(self, val=None):
        if val == None:
            if self.button6_1.config('text')[4] == '':
                self.button6_1.config(background='#f5010a', text='u')
                self.writeFehlzeit(self.datelistweek[0][5],1)
            elif self.button6_1.config('text')[4] == 'u':
                self.button6_1.config(background='#00e100', text='e')
                self.writeFehlzeit(self.datelistweek[0][5],2)
            elif self.button6_1.config('text')[4] == 'e':
                self.button6_1.config(background='#ffff80', text='S')
                self.writeFehlzeit(self.datelistweek[0][5],3)
            elif self.button6_1.config('text')[4] == 'S':
                self.button6_1.config(background='#c0c0c0', text='')
                self.writeFehlzeit(self.datelistweek[0][5],0)
        else:
            if val == 1:
                self.button6_1.config(background='#f5010a', text='u')
            if val == 2:
                self.button6_1.config(background='#00e100', text='e')
            if val == 3:
                self.button6_1.config(background='#ffff80', text='S')
            else:
                pass                         
    def set6_2(self, val=None):
        if val == None:
            if self.button6_2.config('text')[4] == '':
                self.button6_2.config(background='#f5010a', text='u')
                self.writeFehlzeit(self.datelistweek[1][5],1)
            elif self.button6_2.config('text')[4] == 'u':
                self.button6_2.config(background='#00e100', text='e')
                self.writeFehlzeit(self.datelistweek[1][5],2)
            elif self.button6_2.config('text')[4] == 'e':
                self.button6_2.config(background='#ffff80', text='S')
                self.writeFehlzeit(self.datelistweek[1][5],3)
            elif self.button6_2.config('text')[4] == 'S':
                self.button6_2.config(background='#c0c0c0', text='')
                self.writeFehlzeit(self.datelistweek[1][5],0)
        else:
            if val == 1:
                self.button6_2.config(background='#f5010a', text='u')
            if val == 2:
                self.button6_2.config(background='#00e100', text='e')
            if val == 3:
                self.button6_2.config(background='#ffff80', text='S')
            else:
                pass                          
    def set6_3(self, val=None):
        if val == None:
            if self.button6_3.config('text')[4] == '':
                self.button6_3.config(background='#f5010a', text='u')
                self.writeFehlzeit(self.datelistweek[2][5],1)
            elif self.button6_3.config('text')[4] == 'u':
                self.button6_3.config(background='#00e100', text='e')
                self.writeFehlzeit(self.datelistweek[2][5],2)
            elif self.button6_3.config('text')[4] == 'e':
                self.button6_3.config(background='#ffff80', text='S')
                self.writeFehlzeit(self.datelistweek[2][5],3)
            elif self.button6_3.config('text')[4] == 'S':
                self.button6_3.config(background='#c0c0c0', text='')
                self.writeFehlzeit(self.datelistweek[2][5],0)
        else:
            if val == 1:
                self.button6_3.config(background='#f5010a', text='u')
            if val == 2:
                self.button6_3.config(background='#00e100', text='e')
            if val == 3:
                self.button6_3.config(background='#ffff80', text='S')
            else:
                pass                          
    def set6_4(self, val=None):
        if val == None:
            if self.button6_4.config('text')[4] == '':
                self.button6_4.config(background='#f5010a', text='u')
                self.writeFehlzeit(self.datelistweek[3][5],1)
            elif self.button6_4.config('text')[4] == 'u':
                self.button6_4.config(background='#00e100', text='e')
                self.writeFehlzeit(self.datelistweek[3][5],2)
            elif self.button6_4.config('text')[4] == 'e':
                self.button6_4.config(background='#ffff80', text='S')
                self.writeFehlzeit(self.datelistweek[3][5],3)
            elif self.button6_4.config('text')[4] == 'S':
                self.button6_4.config(background='#c0c0c0', text='')
                self.writeFehlzeit(self.datelistweek[3][5],0)
        else:
            if val == 1:
                self.button6_4.config(background='#f5010a', text='u')
            if val == 2:
                self.button6_4.config(background='#00e100', text='e')
            if val == 3:
                self.button6_4.config(background='#ffff80', text='S')
            else:
                pass                          
    def set6_5(self, val=None):
        if val == None:
            if self.button6_5.config('text')[4] == '':
                self.button6_5.config(background='#f5010a', text='u')
                self.writeFehlzeit(self.datelistweek[4][5],1)
            elif self.button6_5.config('text')[4] == 'u':
                self.button6_5.config(background='#00e100', text='e')
                self.writeFehlzeit(self.datelistweek[4][5],2)
            elif self.button6_5.config('text')[4] == 'e':
                self.button6_5.config(background='#ffff80', text='S')
                self.writeFehlzeit(self.datelistweek[4][5],3)
            elif self.button6_5.config('text')[4] == 'S':
                self.button6_5.config(background='#c0c0c0', text='')
                self.writeFehlzeit(self.datelistweek[4][5],0)
        else:
            if val == 1:
                self.button6_5.config(background='#f5010a', text='u')
            if val == 2:
                self.button6_5.config(background='#00e100', text='e')
            if val == 3:
                self.button6_5.config(background='#ffff80', text='S')
            else:
                pass                          
    def set7_1(self, val=None):
        if val == None:
            if self.button7_1.config('text')[4] == '':
                self.button7_1.config(background='#f5010a', text='u')
                self.writeFehlzeit(self.datelistweek[0][6],1)
            elif self.button7_1.config('text')[4] == 'u':
                self.button7_1.config(background='#00e100', text='e')
                self.writeFehlzeit(self.datelistweek[0][6],2)
            elif self.button7_1.config('text')[4] == 'e':
                self.button7_1.config(background='#ffff80', text='S')
                self.writeFehlzeit(self.datelistweek[0][6],3)
            elif self.button7_1.config('text')[4] == 'S':
                self.button7_1.config(background='#c0c0c0', text='')
                self.writeFehlzeit(self.datelistweek[0][6],0)
        else:
            if val == 1:
                self.button7_1.config(background='#f5010a', text='u')
            if val == 2:
                self.button7_1.config(background='#00e100', text='e')
            if val == 3:
                self.button7_1.config(background='#ffff80', text='S')
            else:
                pass                          
    def set7_2(self, val=None):
        if val == None:
            if self.button7_2.config('text')[4] == '':
                self.button7_2.config(background='#f5010a', text='u')
                self.writeFehlzeit(self.datelistweek[1][6],1)
            elif self.button7_2.config('text')[4] == 'u':
                self.button7_2.config(background='#00e100', text='e')
                self.writeFehlzeit(self.datelistweek[1][6],2)
            elif self.button7_2.config('text')[4] == 'e':
                self.button7_2.config(background='#ffff80', text='S')
                self.writeFehlzeit(self.datelistweek[1][6],3)
            elif self.button7_2.config('text')[4] == 'S':
                self.button7_2.config(background='#c0c0c0', text='')
                self.writeFehlzeit(self.datelistweek[1][6],0)
        else:
            if val == 1:
                self.button7_2.config(background='#f5010a', text='u')
            if val == 2:
                self.button7_2.config(background='#00e100', text='e')
            if val == 3:
                self.button7_2.config(background='#ffff80', text='S')
            else:
                pass                          
    def set7_3(self, val=None):
        if val == None:
            if self.button7_3.config('text')[4] == '':
                self.button7_3.config(background='#f5010a', text='u')
                self.writeFehlzeit(self.datelistweek[2][6],1)
            elif self.button7_3.config('text')[4] == 'u':
                self.button7_3.config(background='#00e100', text='e')
                self.writeFehlzeit(self.datelistweek[2][6],2)
            elif self.button7_3.config('text')[4] == 'e':
                self.button7_3.config(background='#ffff80', text='S')
                self.writeFehlzeit(self.datelistweek[2][6],3)
            elif self.button7_3.config('text')[4] == 'S':
                self.button7_3.config(background='#c0c0c0', text='')
                self.writeFehlzeit(self.datelistweek[2][6],0)
        else:
            if val == 1:
                self.button7_3.config(background='#f5010a', text='u')
            if val == 2:
                self.button7_3.config(background='#00e100', text='e')
            if val == 3:
                self.button7_3.config(background='#ffff80', text='S')
            else:
                pass                      
    def set7_4(self, val=None):
        if val == None:
            if self.button7_4.config('text')[4] == '':
                self.button7_4.config(background='#f5010a', text='u')
                self.writeFehlzeit(self.datelistweek[3][6],1)
            elif self.button7_4.config('text')[4] == 'u':
                self.button7_4.config(background='#00e100', text='e')
                self.writeFehlzeit(self.datelistweek[3][6],2)
            elif self.button7_4.config('text')[4] == 'e':
                self.button7_4.config(background='#ffff80', text='S')
                self.writeFehlzeit(self.datelistweek[3][6],3)
            elif self.button7_4.config('text')[4] == 'S':
                self.button7_4.config(background='#c0c0c0', text='')
                self.writeFehlzeit(self.datelistweek[3][6],0)
        else:
            if val == 1:
                self.button7_4.config(background='#f5010a', text='u')
            if val == 2:
                self.button7_4.config(background='#00e100', text='e')
            if val == 3:
                self.button7_4.config(background='#ffff80', text='S')
            else:
                pass                  
    def set7_5(self, val=None):
        if val == None:
            if self.button7_5.config('text')[4] == '':
                self.button7_5.config(background='#f5010a', text='u')
                self.writeFehlzeit(self.datelistweek[4][6],1)
            elif self.button7_5.config('text')[4] == 'u':
                self.button7_5.config(background='#00e100', text='e')
                self.writeFehlzeit(self.datelistweek[4][6],2)
            elif self.button7_5.config('text')[4] == 'e':
                self.button7_5.config(background='#ffff80', text='S')
                self.writeFehlzeit(self.datelistweek[4][6],3)
            elif self.button7_5.config('text')[4] == 'S':
                self.button7_5.config(background='#c0c0c0', text='')
                self.writeFehlzeit(self.datelistweek[4][6],0)
        else:
            if val == 1:
                self.button7_5.config(background='#f5010a', text='u')
            if val == 2:
                self.button7_5.config(background='#00e100', text='e')
            if val == 3:
                self.button7_5.config(background='#ffff80', text='S')
            else:
                pass                  

    def writeFehlzeit(self, d, f):
        #print(d,f)

        # DB-Verbindung
        # verbindung = sqlite3.connect("kurs.db")
        # c = verbindung.cursor()
        # TODO mit try exception abfangen und bei nicht existierender Spalte diese anlegen
        c.execute(""" UPDATE sus
                    SET """+d+""" = ?
                    WHERE pk = ?;
                    """,
                    (f,self.student_pk))
        verbindung.commit()

        # DB-Verbindung schließen
        c.close()
        verbindung.close()

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
