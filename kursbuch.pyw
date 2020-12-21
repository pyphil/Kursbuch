import sqlite3
import tkinter as tk
from tkinter import ttk
#import susverw
from time import strftime, strptime
import datetime
from datetime import datetime
import locale
import report
import tutmod
from PyQt5 import QtCore, QtGui, QtWidgets
from MainWindow import Ui_MainWindow
from KursAnlegen import Ui_KursAnlegen
from NeueStunde import Ui_Form
from PDFdialog import Ui_PdfExportieren
from Susverwgui import Ui_Susverwgui


 
# mit pyQt nicht mehr notwendig
# locale.setlocale(locale.LC_ALL, 'deu_deu')


class Database:
    def __init__(self):
        
        self.krzl = ""
        
        # Verbindung zur lokalen Datenbank herstellen
        self.verbindung = sqlite3.connect("U:\\kurs.db")
        self.c = self.verbindung.cursor()

        # Verbindung zur zentralen SuS-Datenbank herstellen
        self.susverbindung = sqlite3.connect("sus.db")
        self.susc = self.susverbindung.cursor()

        # Austesten, ob die Ersteinrichtung angezeigt werden muss
        try:
            self.krzl = list(self.c.execute("""SELECT Inhalt FROM settings
                                      WHERE Kategorie = "Krzl";"""))
            self.krzl = self.krzl[0][0]
        except:
            # Database übergibt sich selbst dem Objekt Ersteinrichtung 
            # und instanziiert es
            Ersteinrichtung(self)
        else:
            # Database übergibt sich selbst dem Gui Objekt und instanziiert es
            import sys
            self.app = QtWidgets.QApplication(sys.argv)
            self.app.setStyle("Fusion")
            self.ui = Gui(self)
            sys.exit(self.app.exec_())

    def createSettings(self, krz):
        """neue Tabelle settings anlegen aus Dialog Ersteinrichtung"""
        self.c.execute(""" CREATE TABLE settings (
                            "pk"	INTEGER,
                            "Kategorie"	VARCHAR(20),
                            "Inhalt" VARCHAR(20),
                            "Schuljahr" VARCHAR(10),
                            "tname" VARCHAR(20),
                            PRIMARY KEY("pk")
                        )""")
        self.c.execute("""INSERT INTO "settings"
                             ("pk","Kategorie","Inhalt") 
                             VALUES (NULL,"Krzl",?);""", 
                             (krz,))
        self.verbindung.commit()
        self.krzl = krz

    def createKurs(self, an, tn, s):
        """neue Tabelle aus Kursangaben der Funktion KursAnlegen.neu anlegen
        und den Namen in settings mit dem Schuljahr hinterlegen
        """

        self.c.execute(""" CREATE TABLE """ + tn + """ (
                            "pk"	INTEGER,
                            "Datum"	DATE,
                            "Inhalt"	VARCHAR(500),
                            "Ausfall" INTEGER,
                            "Kompensation" INTEGER,
                            "Hausaufgabe" VARCHAR(200),
                            "Planung"  VARCHAR(800),
                            PRIMARY KEY("pk")
                        );""")

        # in settings schreiben
        self.c.execute(""" INSERT INTO settings
                           ("Kategorie", "Inhalt", "Schuljahr", "tname")
                           VALUES ("Kurs",?,?,?); """, 
                            (an,s,tn))

        # kurs_sus Tabelle für die Schüler Primary keys erstellen
        kurssus = tn+"_sus"
        self.c.execute("""CREATE TABLE """ + kurssus + """ (
                       "pk"    INTEGER       
                       );""")

        self.verbindung.commit()

    def getKurse(self):
        """ ALTE VERSION: Gibt eine Liste der Tabellen zurück, die 
        mit dem Kürzel beginnen.
        
        NEUE VERSION: Filtert aus settings die Kursnamen in
        absteigender Reihenfolge der Schuljahre
        """
        # kurse = list(self.c.execute(""" SELECT name FROM sqlite_master WHERE 
        #                                 name like '"""+self.krzl+"""_%'
        #                             """))
        
        # Die Liste muss den Anzeigenamen, aber auch den Tabellennamen 
        # ausgeben, oder der Tabellenname wird erst im OptionMenu 
        # zusammengesetzt
        kurse = list(self.c.execute(""" SELECT Inhalt, Schuljahr FROM settings
                                        WHERE Kategorie = "Kurs"
                                        ORDER BY Schuljahr DESC;
                                    """))
        
        kursliste = []

        for i in kurse:
            #kursliste.append(i[0] + " " + i[1])
            kursliste.append(i[0])
        return kursliste

    def get_tn(self,k):
        """Tabellennamen zum Anzeigenamen zurückgeben"""
        tabellenname = list(self.c.execute("""SELECT tname FROM settings
                                         WHERE Inhalt = ?;
                                      """,
                                      (k,)))
        return tabellenname[0][0]

    # def getListeRaw(self, k):
    #     """Liste aus Datenbank holen und unformatiert zurückgeben"""
    #     tn = self.get_tn(k)
    #     liste = list(self.c.execute(""" SELECT pk, Datum FROM """+tn+""" 
    #                                     ORDER BY Datum DESC;
    #                                 """))
    #     return liste

    def getDateOfPk(self, k, pk):
        """Datum zum Primary Key ausgeben"""
        tn = self.get_tn(k)
        liste = list(self.c.execute(""" SELECT Datum FROM """+tn+""" 
                                        WHERE pk = ?;
                                    """,
                                    (pk,)))
        datum = liste[0][0]
        return datum
    
    def getListe(self, k):
        """Liste aus Datenbank holen und formatiert zurückgeben"""
        tn = self.get_tn(k)
        listedb = list(self.c.execute(""" SELECT pk, Datum, Ausfall, Kompensation 
                                          FROM """+tn+"""
                                          ORDER BY Datum DESC;
                                      """))
        liste = []
        for i in listedb:
            string = str(i[1]).split("_")
            datum = datetime.strptime(string[0], '%Y-%m-%d')
            datum = datum.strftime('%a, %d. %b %Y')
            # liste.append([str(i[0]),(datum+", "+string[1]+". Std."),i[2],i[3]])
            liste.append([str(i[0]), datum, string[1]+". Std.",i[2],i[3]])
        return liste
    
    def writeDatensatz(self, k, inh, ausf, komp, ha, plan, pk):
        tn = self.get_tn(k)
        self.c.execute(""" UPDATE """+tn+"""
                    SET Inhalt = ?, 
                    Ausfall = ?, 
                    Kompensation = ?, 
                    Hausaufgabe = ?, 
                    Planung = ?
                    WHERE pk = ?;
                    """,
                    (inh, ausf, komp, ha, plan, pk))
        self.verbindung.commit()

    def getDatensatz(self, pk, k):
        tn = self.get_tn(k)
        text = list(self.c.execute("""SELECT * FROM """+tn+""" 
                                    WHERE pk = ?;""",(pk,)))
        return text

    def deleteDatensatz(self, k, pk):
        tn = self.get_tn(k)
        self.c.execute(""" DELETE FROM """+tn+""" 
                           WHERE pk = ?;
                           """,
                           (pk,))

    def writeSuSListe(self,k,s):
        """ Löscht die alte Tabelle und erstellt eine neue mit den aktuellen
        SuS-PKs aus der Gesamtliste ohne Namen
        """
        tn = self.get_tn(k)
        kurssus = tn+"_sus"
    
        # Versuchen die Tabelle zu löschen
        try:
            self.c.execute("""drop table """ + kurssus + """
                            """)
        except:
            pass
      
        # Tabelle neu erstellen. Ohne primary key Angabe, da nur 
        # Speicherung der SuS-pks aus Gesamtliste
        self.c.execute("""CREATE TABLE """ + kurssus + """ (
                            "pk"    INTEGER       
                        );""")
        
        for i in s:
            self.c.execute("""INSERT INTO """ + kurssus + """
                                ("pk")
                                VALUES (?);""", 
                                (i[2],))
        self.verbindung.commit()

    def getSuSListe(self,k):
        tn = self.get_tn(k)
        kurssus = tn+"_sus"

        pkliste = list(self.c.execute("""SELECT pk 
                                   FROM """+kurssus+""" 
                                   """))
        susliste = []
        for i in pkliste:
            item = list(self.susc.execute("""SELECT pk,Name,Vorname,Klasse 
                                          FROM "sus"
                                          WHERE pk = ?;
                                       """,
                                        (i[0],)))
            susliste.append([item[0][1],item[0][2],item[0][0],item[0][3]])
        return susliste

    def getSuS(self, date, k):
        tn = self.get_tn(k)
        # Anführungsstriche um das Datum setzen
        date='"'+date+'"'
        kurssus = tn+"_sus"
        pkliste = list(self.c.execute("""SELECT pk 
                                   FROM """+kurssus+""" 
                                   """))
        
        # Prüfen, ob es schon eine Spalte für das Datum gibt
        try:
            # versuchen, die Spalte hinzuzufügen
            self.susc.execute("""ALTER TABLE sus ADD """+date+""" VARCHAR(12)
                           """)
            self.susverbindung.commit()
        except:
            pass
        else:
            # Wenn die Spalte neu erstellt wird, alles mit Nullen füllen
            self.susc.execute("""UPDATE sus
                              SET """+date+""" = ?;
                           """,
                           (0,))
            self.susverbindung.commit()               
        
        liste = []
        for i in pkliste:
            item = list(self.susc.execute("""SELECT pk,Name,Vorname,"""+date+""" 
                                          FROM "sus"
                                          WHERE pk = ?;
                                       """,
                                        (i[0],)))
            liste.append(item[0])
        return liste

    def writeFehlzeiten(self, pk, f, k, date):
        # Anführungsstriche um das Datum setzen
        date='"'+date+'"'
        self.susc.execute("""UPDATE "sus" 
                          SET """+date+""" = ?
                          WHERE pk = ?;
                       """,
                          (f,pk))
        self.susverbindung.commit()

    def writeNeueStunde(self, date, std, k):
        tn = self.get_tn(k)
        datum = date+"_"+str(std)
        self.c.execute("""INSERT INTO """+tn+"""
                            ("pk","Datum","Inhalt","Ausfall","Kompensation",
                            "Hausaufgabe","Planung") 
                            VALUES (NULL,?,"",0,0,"","");""", 
                            (datum,))
        self.verbindung.commit()

    def getGesamtliste(self):
        """Holt die Gesamtliste aller SuS für Zuordnung zum Kurs"""
        s = list(self.susc.execute("SELECT pk, Name, Vorname, Klasse FROM sus"))
        return s

    def close(self):
        self.c.close()
        self.verbindung.close()
        self.susc.close()
        self.susverbindung.close()

class Ersteinrichtung:
    def __init__(self, db):

        self.db = db

        # build ui
        ersteinrichtung = tk.Tk()
        frame1 = ttk.Frame(ersteinrichtung)
        heading = ttk.Label(frame1)
        heading.config(font='{Segoe UI} 12 {bold}', text='Ersteinrichtung')
        heading.pack(pady='10', side='top')
        subheading = ttk.Label(frame1)
        subheading.config(justify='center', text='Zur Ersteinrichtung von pyKursbuch brauchen wir dein Lehrerkürzel.', wraplength='200')
        subheading.pack(side='top')
        frame2 = ttk.Frame(frame1)
        Label_krz = ttk.Label(frame2)
        Label_krz.config(font='{Segoe UI} 9 {bold}', text='Kürzel: ')
        Label_krz.pack(side='left')
        self.krzEntry = ttk.Entry(frame2)
        self.krzEntry.config(font='TkDefaultFont', validate='none')
        self.krzEntry.pack(side='left')
        frame2.config(height='200', width='200')
        frame2.pack(pady='10', side='top')
        frame3 = ttk.Frame(frame1)
        self.buttonOK = ttk.Button(frame3)
        self.buttonOK.config(text='OK')
        self.buttonOK.pack(padx='10', side='left')
        self.buttonOK.configure(command=self.ok)
        self.buttonAbbrechen = ttk.Button(frame3)
        self.buttonAbbrechen.config(text='Abbrechen')
        self.buttonAbbrechen.pack(padx='10', side='left')
        self.buttonAbbrechen.configure(command=self.abbrechen)
        frame3.config(height='200', width='200')
        frame3.pack(pady='10', side='top')
        frame1.config(height='200', width='200')
        frame1.pack(expand='true', side='top')
        ersteinrichtung.config(height='180', width='280')
        ersteinrichtung.geometry('280x180')
        ersteinrichtung.title('pyKursbuch')

        # Main widget
        self.mainwindow = ersteinrichtung

        # Fenster positionieren
        # Gets the requested values of the height and widht.
        windowWidth = self.mainwindow.winfo_reqwidth()
        windowHeight = self.mainwindow.winfo_reqheight()
        # Gets both half the screen width/height and window width/height
        positionRight = int(self.mainwindow.winfo_screenwidth()/2 - windowWidth/2)
        positionDown = int(self.mainwindow.winfo_screenheight()/2 - windowHeight/2-15)
        # Positions the window in the center of the page.
        self.mainwindow.geometry("+{}+{}".format(positionRight, positionDown))

        # Grab window + focus
        self.mainwindow.grab_set()
        self.mainwindow.focus_set()      

        # mainloop
        self.mainwindow.mainloop()

    def ok(self):
        self.db.createSettings(self.krzEntry.get())
        self.mainwindow.destroy()

        import sys
        self.app = QtWidgets.QApplication(sys.argv)
        self.ui = Gui(self.db)

    def abbrechen(self):
        self.mainwindow.destroy()

class KursAnlegen(Ui_KursAnlegen):
    def __init__(self, gui, db):
        self.kursneudialog = QtWidgets.QWidget()
        self.setupUi(self.kursneudialog)
        self.kursneudialog.show()

        self.gui = gui
        self.db = db
               
        # Schuljahr
        jahre = ["2020/21", "2021/22", "2022/23"]

        self.comboBoxSchuljahr.addItems(jahre)
        
        # signals and slots
        self.pushButtonAnlegen.clicked.connect(self.neu)
        self.pushButtonAbbrechen.clicked.connect(self.abbrechen)



    def neu(self):
        # # Umwandlung in Großbuchstaben mit upper und whitespace enternen
        fach = self.lineEditFachkrzl.text().upper().lstrip().rstrip()
        klasse = self.lineEditKlasse.text().upper().lstrip().rstrip()
        print(fach)
        print(klasse)
        print(self.comboBoxSchuljahr.currentText())

        schuljahr = self.comboBoxSchuljahr.currentText()
        anzeigename = fach + " " + klasse + " " + schuljahr
        schuljahr_ = schuljahr.replace("/","_")
        tabellenname = (self.db.krzl + "_" + fach + "_" + klasse + "_" + schuljahr_)

        # Sonderzeichen und Leerzeichen entfernen
        tabellenname = tabellenname.replace("-","_")
        tabellenname = tabellenname.replace("/","_")
        tabellenname = tabellenname.replace(" ","_")

        # Namen und Schuljahr an Datenbankobjekt übergeben
        self.db.createKurs(anzeigename, tabellenname, schuljahr)
        self.gui.kursauswahlMenue()
        self.kursneudialog.close()

    def abbrechen(self):
        self.kursneudialog.close()

        

class StundeAnlegen(Ui_Form):
    def __init__(self, gui, db, kurs):
                
        self.gui = gui
        self.db = db
        self.kurs = kurs

        self.Form = QtWidgets.QWidget()
        self.setupUi(self.Form)
        self.Form.show()
        
        self.pushButton.clicked.connect(self.neueStundeAnlegen)
        self.pushButton_2.clicked.connect(self.abbrechen)

    def neueStundeAnlegen(self):
        datum = str(self.calendarWidget.selectedDate().toPyDate())
        stunde = 0
        if self.radioButton.isChecked() == True:
            stunde = "1"
        if self.radioButton_2.isChecked() == True:
            stunde = "2"
        if self.radioButton_3.isChecked() == True:
            stunde = "3"    
        if self.radioButton_4.isChecked() == True:
            stunde = "4"
        if self.radioButton_5.isChecked() == True:
            stunde = "5"
        if self.radioButton_6.isChecked() == True:
            stunde = "6"
        if self.radioButton_7.isChecked() == True:
            stunde = "7"
        # Hinweis, wenn keine Stunde ausgewählt wurde
        if stunde == 0:
            self.message = QtWidgets.QMessageBox()
            self.message.setIcon(QtWidgets.QMessageBox.Critical)
            self.message.setWindowTitle("Fehler")
            self.message.setText("Bitte eine Stunde angeben.")
            self.message.exec_()
        else:
            # Datum an Datenbankobjekt übergeben
            self.db.writeNeueStunde(datum, stunde, self.kurs)
            self.gui.kursAnzeigen()
            self.Form.close()

    def abbrechen(self):
        self.Form.close()    


class SuSVerw(Ui_Susverwgui):
    def __init__(self, gui, db, kurs):
                
        self.gui = gui
        self.db = db
        self.kurs = kurs

        self.susverwgui = QtWidgets.QWidget()
        self.setupUi(self.susverwgui)
        self.susverwgui.show()

        self.tableWidget.setColumnWidth(0,190)
        self.tableWidget_2.setColumnWidth(0,190)

        # Listen bereitstellen
        self.liste2 = []
        self.liste2sorted = []
        
        # Zeigt die Liste der Schüler im Kurs
        self.labelLerngruppe.setText("Mitglieder der Lerngruppe: "+self.kurs)
        self.liste2 = self.db.getSuSListe(self.kurs)
        self.liste2sorted = self.liste2
        z = 0
        for i in self.liste2sorted:
            self.tableWidget_2.setRowCount(z+1)
            self.tableWidget_2.setItem(
                    z,0,QtWidgets.QTableWidgetItem(i[0]+", "+i[1]))
            self.tableWidget_2.setItem(z,1,QtWidgets.QTableWidgetItem(i[3]))
            z += 1

        # Signals and slots
        self.comboBox.activated.connect(self.zeigeKlasse)
        self.pushButtonAddSelected.clicked.connect(self.susadd)

        klassen = ["5a", "5b", "5c", "5d", "5e",
                   "6a", "6b", "6c", "6d", "6e",
                   "7a", "7b", "7c", "7d", "7e",
                   "8a", "8b", "8c", "8d", "8e",
                   "9a", "9b", "9c", "9d", "9e",
                   "10a", "10b", "10c", "10d", "10e",
                    "EF", "Q1", "Q2"]
        self.comboBox.addItems(klassen)

    def zeigeKlasse(self):
        """ Zeigt die Liste der Schüler der ausgewählten Klasse, bzw. wenn
        noch keine Auswahl erfolgt ist, einen Hinweis
        """

        # gefilterte Liste bei jedem Aufruf leer bereitstellen
        self.filtered = []

        # ausgewählte Klasse
        klasse = self.comboBox.currentText()

        # Filtern nach Klasse
        alle = self.db.getGesamtliste()
        z = 0
        for i in alle:
            if i[3] == klasse:
                self.tableWidget.setRowCount(z+1)
                self.tableWidget.setItem(
                    z,0,QtWidgets.QTableWidgetItem(i[1]+", "+i[2]))
                self.tableWidget.setItem(z,1,QtWidgets.QTableWidgetItem(i[3]))
                self.filtered.append([i[1], i[2], i[0]])
                z += 1

    def susadd(self):
        selection = self.tableWidget.selectionModel().selectedRows()
        rows = []
        for i in selection:
            print(i)
            rows.append(i.row())
        print(rows)

class Kursbuch_Dialog(Ui_PdfExportieren):
    def __init__(self, tn, kurs, krzl):
        self.PdfExportieren = QtWidgets.QWidget()
        self.setupUi(self.PdfExportieren)
        self.PdfExportieren.show()

        self.tn = tn
        self.kurs = kurs
        self.krzl = krzl

        self.pushButtonExport.clicked.connect(self.ok)
        self.pushButtonAbbrechen.clicked.connect(self.abbrechen)

    def ok(self):
        if self.radioButtonMitFs.isChecked() == True:
            var = "1"
        if self.radioButtonOhneFS.isChecked() == True:
            var = "2"
        self.PdfExportieren.close()
        report.makeKursbuch(self.tn, self.kurs, self.krzl, var)

    def abbrechen(self):
        self.PdfExportieren.close()


class Gui(Ui_MainWindow):
    def __init__(self, db):
        self.MainWindow = QtWidgets.QMainWindow()
        self.setupUi(self.MainWindow)
        
        # Auf dem Desktop zentrieren
        # geometry of the main window
        qr = self.MainWindow.frameGeometry()
        # center point of screen
        cp = QtWidgets.QDesktopWidget().availableGeometry().center()
        # move rectangle's center point to screen's center point
        qr.moveCenter(cp)
        # Taskleiste abziehen
        qr.setTop(qr.top()-15)
        # top left of rectangle becomes top left of window centering it
        self.MainWindow.move(qr.topLeft())

        self.MainWindow.show()
        
        self.db = db
        
        # Variable für den aktuellen Kurs
        self.kurs = ""
        # Variable für den aktuellen Primary Key
        self.pk = ""
        
        self.fehlzeitenansicht = 0
        self.kurswechel = 0

        self.tableWidget.setColumnWidth(0,140)

        # Kürzel in Fenstertitel anzeigen
        self.MainWindow.setWindowTitle("Kursbuch von "+self.db.krzl)  

        # Window Deletion abfangen, speichern und Datenbank schließen
        # def on_closing():
        #     if self.kurs != "":
        #         self.datensatzSpeichern()
        #     self.db.close()
        #     self.master.destroy()



        # Methoden aurufen
        self.kursauswahlMenue()

        # Signals and slots
        self.comboBoxKurs.activated.connect(self.kursAnzeigen)
        self.tableWidget.clicked.connect(self.datensatzAnzeigen)
        self.pushButtonNeuerKurs.clicked.connect(self.kursNeu)
        self.pushButtonKursmitglieder.clicked.connect(self.schuelerVerw)
        self.pushButtonNeueStd.clicked.connect(self.neueStunde)
        self.pushButtonDelStd.clicked.connect(self.stundeDel)
        self.pushButtonKursheftAnzeigen.clicked.connect(self.kursheftAnzeigen)
        self.tabWidget.tabBarClicked.connect(self.fehlzeitenAnzeige)

        # alle focusChanged Events der App an self.leave leiten
        self.db.app.focusChanged.connect(self.leave)

    def leave(self, old, new):
        # prüfen welche Felder welchen Fokuswechsel haben
        if old == self.textEditKurshefteintrag or old == self.textEditHausaufgaben or old == self.textEdit or old == self.checkBox or old == self.checkBox_2:
            self.datensatzSpeichern()

    def kursauswahlMenue(self):
        '''Holt Liste der Kurse aus db und füllt Combobox '''
        self.comboBoxKurs.clear()
        self.comboBoxKurs.addItems(self.db.getKurse())
    
    def disableFieldsStd(self):
        self.textEditKurshefteintrag.setEnabled(False)
        self.textEditKurshefteintrag.clear()
        self.textEditHausaufgaben.setEnabled(False)
        self.textEditHausaufgaben.clear()
        self.textEdit.setEnabled(False)
        self.textEdit.clear()
        self.checkBox.setEnabled(False)
        self.checkBox.setChecked(0)
        self.checkBox_2.setEnabled(False)
        self.checkBox_2.setChecked(0)
        # self.pushButtonDelKurs.setEnabled(False)
        # self.pushButtonKursmitglieder.setEnabled(False)
        # self.pushButtonNeueStd.setEnabled(False)
        self.pushButtonDelStd.setEnabled(False)
        # self.pushButtonKursheftAnzeigen.setEnabled(False)

    def enableFieldsStd(self):
        self.textEditKurshefteintrag.setEnabled(True)
        self.textEditHausaufgaben.setEnabled(True)
        self.textEdit.setEnabled(True)
        self.checkBox.setEnabled(True)
        self.checkBox_2.setEnabled(True)
        self.pushButtonDelStd.setEnabled(True)

    def enableFieldsKurs(self):
        self.pushButtonDelKurs.setEnabled(True)
        self.pushButtonKursmitglieder.setEnabled(True)
        self.pushButtonNeueStd.setEnabled(True)
        self.pushButtonKursheftAnzeigen.setEnabled(True)

    def kursAnzeigen(self):
        """ setzt die aktuelle Combobox-Auswahl als Kursvariable
        und führt die Methode zum Füllen des tableWidgets/listbox aus
        """
        self.disableFieldsStd()
        self.kurs = self.comboBoxKurs.currentText()
        # Wenn bereits ein Kurs angezeigt wird, vorher speichern und Variable
        # kurwechsel auf 1 setzen
        # if self.kurs != "":
            #self.datensatzSpeichern()
            # self.kurswechel = 1
            # Felder leeren
            #self.disableFields()

        # # Wenn noch in Fehlzeitenasicht, erst zurückwechseln
        # if self.fehlzeitenansicht == 1:
        #     self.back()

        # if type(k) is tuple:
        #     self.kurs = k[0]
        # else:
        #     self.kurs = k

        self.fillListbox()

        self.enableFieldsKurs()

        # self.pk für den aktuellen Datensatz zunächst auf "" setzen
        self.pk = ""

        # Fehlzeiten Widget schließen -> bei Kurswechsel keine falschen Fehlzeiten
        self.verticalLayoutWidget.close()

    def markieren(self, *args):
        pass
        # self.datensatzSpeichern()
        # self.fillListbox()

    def fillListbox(self):
        self.tableWidget.setRowCount(len(self.db.getListe(self.kurs)))
    
        z = 0
        for i in self.db.getListe(self.kurs):
            self.tableWidget.setItem(z,0,QtWidgets.QTableWidgetItem(i[1]))
            self.tableWidget.setItem(z,1,QtWidgets.QTableWidgetItem(i[2]))
            if i[3] == 1:
                # Ausfalltage in grau markieren
                self.tableWidget.item(z,0).setBackground(QtGui.QColor(200, 200, 200))  
                self.tableWidget.item(z,1).setBackground(QtGui.QColor(200, 200, 200))  
            if i[4] == 1:
                # Kompensation in grün markieren      
                self.tableWidget.item(z,0).setBackground(QtGui.QColor(100, 210, 120))
                self.tableWidget.item(z,1).setBackground(QtGui.QColor(100, 210, 120))
            if i[3] == 1 and i[4] == 1:
                # Kompensation in Ausfalltagen in grau-grün markieren      
                self.tableWidget.item(z,0).setBackground(QtGui.QColor(200, 215, 200))  
                self.tableWidget.item(z,1).setBackground(QtGui.QColor(200, 215, 200))  
            z += 1

    def datensatzAnzeigen(self):
        self.enableFieldsStd()
        # Aktuelle Datumsauswahl in Variable speichern
        auswahl = self.tableWidget.currentRow()
        # auswahl = self.evt.widget.curselection()[0]
        # Zugehörigen Primary Key der Auswahl setzen
        self.pk = self.db.getListe(self.kurs)[auswahl][0]
        # Datensatz als liste holen
        liste = self.db.getDatensatz(self.pk, self.kurs)      
        # # Textvariable mit Text aus Datenbankfeld füllen
        self.textEditKurshefteintrag.setText(liste[0][2])
        # self.feldInhalt.delete('1.0', tk.END)
        # self.feldInhalt.insert('1.0', liste[0][2])
        
        # Ferien/Ausfall:
        if liste[0][3] == 1:
            self.checkBox.setChecked(True)
        else:
            self.checkBox.setChecked(False)
        
        # # Kompensation:
        if liste[0][4] == 1:
            self.checkBox_2.setChecked(True)
        else:
            self.checkBox_2.setChecked(False)

        # Kursbuch Feld Hausaufgaben
        self.textEditHausaufgaben.setText(liste[0][5])

        # # Feld Planungsnotizen
        self.textEdit.setText(liste[0][6])

        # Fehlzeiten auf aktuelles Datum aktualisieren, 
        # wenn in Fehlzeitenansicht
        if self.tabWidget.currentIndex() == 1:
            self.fehlzeitenAnzeige(1)

    def kursNeu(self):
        self.kurs_neu = KursAnlegen(self, self.db)

    def updateMenuKurse(self):
        pass
        # self.menuKurse.destroy()
        # self.kursauswahlMenue()

    def kursDel(self):
        pass

    def schuelerVerw(self):
        #susverw.SuSVerwaltung(self, self.db, self.kurs)
        self.susverw = SuSVerw(self, self.db, self.kurs)

    def neueStunde(self):
        """instanziiert das Objekt KursAnlegen und übergibt 
        sich selbst, db und kurs
        """
        self.neuestd = StundeAnlegen(self, self.db, self.kurs)
        
        

    def stundeDel(self):
        """Löscht die aktuelle Stunde ohne die eingetragenen Fehlzeiten"""
        self.db.deleteDatensatz(self.kurs, self.pk)
        self.kursAnzeigen()

    def datensatz_wechseln(self, evt):
        """ Zeigt den Inhalt des auswählten Datums und speichert
        vorher den aktuellen Eintrag (in der Fehlzeitenansicht wird direkt
        gespeichert)
        """
        pass
        # # Event Variable aus Listbox verfügbar machen
        # self.evt = evt
        # # nur beim Wechseln speichern, wenn im gleichen Datensatz
        # if self.kurswechel == 0:
        #     self.datensatzSpeichern()
        # else:
        #     # Felder aktivieren, wenn Wechsel in neuen Datensatz
        #     self.enableFields()
        #     self.kurswechel = 0
        # self.datensatzAnzeigen()

    def datensatzSpeichern(self):
        # Inhalt der aktuellen Felder speichern, rstrip löscht die automatische
        # neue Zeile der tkinter Textbox
        inhaltNeu = self.textEditKurshefteintrag.toPlainText()
        
        # Checkbox State abfragen. Durch die Migration von tkinter gibt es in
        # db nur 0 und 1
        if self.checkBox.checkState() == 2:
            ausfallNeu = 1
        else:
            ausfallNeu = 0
        if self.checkBox_2.checkState() == 2:
            kompNeu = 1
        else:
            kompNeu = 0

        haNeu = self.textEditHausaufgaben.toPlainText()
        planungNeu = self.textEdit.toPlainText()

        self.db.writeDatensatz(self.kurs,inhaltNeu, ausfallNeu, kompNeu, haNeu,
                              planungNeu, self.pk)

        # Listbox neu einfüllen, da sich Ausfall und Komp ggf. geändert haben
        self.fillListbox()

    def fehlzeitenAnzeige(self, tab):

        if tab == 1:
            try:
                self.verticalLayoutWidget.close()
            except:
                pass

            self.verticalLayoutWidget = QtWidgets.QWidget(self.tab_Fehlzeiten)
            self.verticalLayoutWidget.setGeometry(QtCore.QRect(160, 30, 511, 550))
            self.verticalLayoutWidget.setObjectName("verticalLayoutWidget")
            self.verticalLayoutFehlzeiten = QtWidgets.QVBoxLayout(self.verticalLayoutWidget)
            self.verticalLayoutFehlzeiten.setContentsMargins(0, 0, 0, 0)
            self.verticalLayoutFehlzeiten.setSpacing(0)
            self.verticalLayoutFehlzeiten.setObjectName("verticalLayoutFehlzeiten")

            self.verticalLayoutWidget.show()

            if self.pk != "":
                self.datum = self.db.getDateOfPk(self.kurs, self.pk)
                self.sus = self.db.getSuS(self.datum, self.kurs)

                for i in range(len(self.sus)):
                    self.frame = QtWidgets.QFrame(self.verticalLayoutWidget)
                    self.frame.setGeometry(QtCore.QRect(180, 90, 450, 30))
                    self.frame.setFrameShape(QtWidgets.QFrame.NoFrame)
                    self.frame.setFrameShadow(QtWidgets.QFrame.Raised)
                    self.frame.setObjectName("frame"+str(i))
                    self.label = QtWidgets.QLabel(self.frame)
                    self.label.setGeometry(QtCore.QRect(20, 0, 200, 15))
                    self.label.setText(str(i+1)+". "+self.sus[i][1]+", "+self.sus[i][2])
                    self.radioButton = QtWidgets.QRadioButton(self.frame)
                    self.radioButton.setGeometry(QtCore.QRect(200, 0, 182, 15))
                    self.radioButton.setObjectName("0,"+str(i))
                    self.radioButton2 = QtWidgets.QRadioButton(self.frame)
                    self.radioButton2.setGeometry(QtCore.QRect(250, 0, 82, 15))
                    self.radioButton2.setObjectName("1,"+str(i))
                    self.radioButton3 = QtWidgets.QRadioButton(self.frame)
                    self.radioButton3.setGeometry(QtCore.QRect(300, 0, 82, 15))
                    self.radioButton3.setObjectName("2,"+str(i))
                    self.radioButton4 = QtWidgets.QRadioButton(self.frame)
                    self.radioButton4.setGeometry(QtCore.QRect(350, 0, 82, 15))
                    self.radioButton4.setObjectName("3,"+str(i))
                    self.radioButton5 = QtWidgets.QRadioButton(self.frame)
                    self.radioButton5.setGeometry(QtCore.QRect(400, 0, 82, 15))
                    self.radioButton5.setObjectName("4,"+str(i))
                    
                    self.verticalLayoutFehlzeiten.addWidget(self.frame)
                    
                    self.radioButton.clicked.connect(self.fsSpeichern)
                    self.radioButton2.clicked.connect(self.fsSpeichern)
                    self.radioButton3.clicked.connect(self.fsSpeichern)
                    self.radioButton4.clicked.connect(self.fsSpeichern)
                    self.radioButton5.clicked.connect(self.fsSpeichern)

                    if self.sus[i][3] == "0":
                        self.radioButton.setChecked(True)
                    if self.sus[i][3] == "1":
                        self.radioButton2.setChecked(True)
                    if self.sus[i][3] == "2":
                        self.radioButton3.setChecked(True)
                    if self.sus[i][3] == "3":
                        self.radioButton4.setChecked(True)
                    if self.sus[i][3] == "4":
                        self.radioButton5.setChecked(True)
                
                # Für wenige Einträge Höhe des Spacers unten anpassen
                if len(self.sus) >= 15:
                    h = 0
                elif len(self.sus) >= 10:
                    h = 200
                elif len(self.sus) >= 0:
                    h = 300

                spacerItem = QtWidgets.QSpacerItem(20, h, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Fixed)
                self.verticalLayoutFehlzeiten.addItem(spacerItem)
    
    def fsSpeichern(self):
        sender = self.radioButton.sender().objectName()
        sender = sender.split(",")
        # print("Entschuldigungsstatus: "+sender[0]+"\n"+
        #       "Datensatz-Nr.:"+sender[1]+"\n"+
        #       "Datensatz:"+str(self.sus[int(sender[1])])+"\n"+
        #       "PK:"+str(self.sus[int(sender[1])][0]))
        fstatus = sender[0]
        pk = self.sus[int(sender[1])][0]
        self.db.writeFehlzeiten(pk,fstatus,self.kurs, self.datum)
    
    def back(self):
        pass
        # Fehlzeitenansicht aus
        # self.fehlzeitenansicht = 0
        # self.frameFehlzeiten.pack_forget()
        # self.frameRechts.pack(fill="both", expand=1)

    def tutmod(self):
        pass
        """ Objekt für Tutorenmodus instanziieren und starten"""
        app = tutmod.Tutmod01App()
        app.run()

    def kursheftAnzeigen(self):
        # self.datensatzSpeichern()
        # Kursbuch Dialog instantiieren
        self.kdialog = Kursbuch_Dialog(self.db.get_tn(self.kurs), self.kurs, self.db.krzl)
        #report.makeKursbuch(self.db.get_tn(self.kurs), self.kurs, self.db.krzl)


if __name__ == "__main__":
    Database()