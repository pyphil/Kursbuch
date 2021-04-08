
from calendar import Calendar
from datetime import date, timedelta, datetime
from PyQt5 import QtCore, QtGui, QtWidgets
from Tutmodgui import Ui_Tutmodgui


class Tutmod(Ui_Tutmodgui, QtWidgets.QWidget):
    def __init__(self):
        super(Tutmod, self).__init__()
        self.setupUi(self)
        self.show()
        self.comboBoxMonat.activated.connect(self.setMonth)

        self.set_cur_year_month()
        self.setMonth(True)

    def set_cur_year_month(self):
        # self.combo_jahr.set(date.today().year)
        self.comboBoxMonat.setCurrentText(datetime.now().strftime("%B"))

    def setMonth(self, set=True):
        y = int(self.comboBoxMonat.currentIndex())
        print(y)
        self.m = y+1
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
            print(self.weekno)
            # self.weekafter(True)
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
        self.label_Woche.config(text=self.weeks[self.weekno][0].split("-")[2]+"."+self.weeks[self.weekno][0].split("-")[1]+"."+" bis "+self.weeks[self.weekno][4].split("-")[2]+"."+self.weeks[self.weekno][4].split("-")[1]+".")
        self.label_Mo_date.config(text=self.weeks[self.weekno][0].split("-")[2]+"."+self.weeks[self.weekno][0].split("-")[1]+".")
        self.label_Di_date.config(text=self.weeks[self.weekno][1].split("-")[2]+"."+self.weeks[self.weekno][1].split("-")[1]+".")
        self.label_Mi_date.config(text=self.weeks[self.weekno][2].split("-")[2]+"."+self.weeks[self.weekno][2].split("-")[1]+".")
        self.label_Do_date.config(text=self.weeks[self.weekno][3].split("-")[2]+"."+self.weeks[self.weekno][3].split("-")[1]+".")
        self.label_Fr_date.config(text=self.weeks[self.weekno][4].split("-")[2]+"."+self.weeks[self.weekno][4].split("-")[1]+".")

        self.set_fehlzeiten()

    def weekafter(self):
        self.resetButtons()
        self.weekno += 1
    
        if self.m != int(self.weeks[self.weekno][4].split("-")[1]):
            self.weekno += 1
        self.label_Woche.config(text=self.weeks[self.weekno][0].split("-")[2]+"."+self.weeks[self.weekno][0].split("-")[1]+"."+" bis "+self.weeks[self.weekno][4].split("-")[2]+"."+self.weeks[self.weekno][4].split("-")[1]+".")
        self.label_Mo_date.config(text=self.weeks[self.weekno][0].split("-")[2]+"."+self.weeks[self.weekno][0].split("-")[1]+".")
        self.label_Di_date.config(text=self.weeks[self.weekno][1].split("-")[2]+"."+self.weeks[self.weekno][1].split("-")[1]+".")
        self.label_Mi_date.config(text=self.weeks[self.weekno][2].split("-")[2]+"."+self.weeks[self.weekno][2].split("-")[1]+".")
        self.label_Do_date.config(text=self.weeks[self.weekno][3].split("-")[2]+"."+self.weeks[self.weekno][3].split("-")[1]+".")
        self.label_Fr_date.config(text=self.weeks[self.weekno][4].split("-")[2]+"."+self.weeks[self.weekno][4].split("-")[1]+".")

        self.set_fehlzeiten()

    def set_fehlzeiten(self):
        """Führt alle set-Methoden aus, indem vorher die Liste aus der db
        geholt wird und den Methoden u oder e oder ""? übergeben wird """
        # TODO Schüler-pk übergeben
        self.student_pk = 1

        # DB-Verbindung
        verbindung = sqlite3.connect("kurs.db")
        c = verbindung.cursor()

        # Liste generieren (wenn es das Datum+Std nicht gibt gibt sqlite das
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
                item = list(c.execute("""SELECT """+d+""" 
                                                FROM "sus"
                                                WHERE pk = ?;
                                            """,
                                            (self.student_pk,)))
                fehlzlist.append(item)
            
            setlist.append(fehlzlist)
        
        # DB-Verindung schließen
        c.close()
        verbindung.close()
        
        #print(setlist[0][0][0][0])
        print(self.datelistweek)
        
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
            if val == 1:
                self.button1_1.config(background='#f5010a', text='u')
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
        print(d,f)

        # DB-Verbindung
        verbindung = sqlite3.connect("kurs.db")
        c = verbindung.cursor()
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
        self.button1_1.config(background='#c0c0c0', text='')
        self.button1_2.config(background='#c0c0c0', text='')
        self.button1_3.config(background='#c0c0c0', text='')
        self.button1_4.config(background='#c0c0c0', text='')
        self.button1_5.config(background='#c0c0c0', text='')
        
        self.button2_1.config(background='#c0c0c0', text='')
        self.button2_2.config(background='#c0c0c0', text='')
        self.button2_3.config(background='#c0c0c0', text='')
        self.button2_4.config(background='#c0c0c0', text='')
        self.button2_5.config(background='#c0c0c0', text='')
        
        self.button3_1.config(background='#c0c0c0', text='')
        self.button3_2.config(background='#c0c0c0', text='')
        self.button3_3.config(background='#c0c0c0', text='')
        self.button3_4.config(background='#c0c0c0', text='')
        self.button3_5.config(background='#c0c0c0', text='')
        
        self.button4_1.config(background='#c0c0c0', text='')
        self.button4_2.config(background='#c0c0c0', text='')
        self.button4_3.config(background='#c0c0c0', text='')
        self.button4_4.config(background='#c0c0c0', text='')
        self.button4_5.config(background='#c0c0c0', text='')
        
        self.button5_1.config(background='#c0c0c0', text='')
        self.button5_2.config(background='#c0c0c0', text='')
        self.button5_3.config(background='#c0c0c0', text='')
        self.button5_4.config(background='#c0c0c0', text='')
        self.button5_5.config(background='#c0c0c0', text='')
        
        self.button6_1.config(background='#c0c0c0', text='')
        self.button6_2.config(background='#c0c0c0', text='')
        self.button6_3.config(background='#c0c0c0', text='')
        self.button6_4.config(background='#c0c0c0', text='')
        self.button6_5.config(background='#c0c0c0', text='')
        
        self.button7_1.config(background='#c0c0c0', text='')
        self.button7_2.config(background='#c0c0c0', text='')
        self.button7_3.config(background='#c0c0c0', text='')
        self.button7_4.config(background='#c0c0c0', text='')
        self.button7_5.config(background='#c0c0c0', text='')



    def run(self):
        self.mainwindow.mainloop()

if __name__ == '__main__':
    import sys
    app = QtWidgets.QApplication(sys.argv)
    ui = Tutmod()
    sys.exit(app.exec_())