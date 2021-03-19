import sqlite3
from time import strftime, strptime, sleep, time
import datetime
from datetime import datetime, date, timedelta
import locale
import sys
import subprocess
import report
import keyring
import threading
from os import path, system, environ
from PyQt5 import QtCore, QtGui, QtWidgets
from MainWindow import Ui_MainWindow
from KursAnlegen import Ui_KursAnlegen
from NeueStunde import Ui_Form
from PDFdialog import Ui_PdfExportieren
from Susverwgui import Ui_Susverwgui
from Ersteinrichtung import Ui_Ersteinrichtung
from Syncdialog import Ui_Syncdialog

# QtWidgets.QApplication.setAttribute(QtCore.Qt.AA_EnableHighDpiScaling, True)
#QtWidgets.QApplication.setAttribute(QtCore.Qt.AA_UseHighDpiPixmaps, True)
#environ["QT_AUTO_SCREEN_SCALE_FACTOR"] = "1"

from keyring.backends import Windows
import win32timezone
keyring.set_keyring(Windows.WinVaultKeyring())

# nur für das alphabetisch richtige Sortieren der Kursmitglieder
locale.setlocale(locale.LC_ALL, 'deu_deu')

# Variable für subprocess.call ohne cmd fenster, -> 0 für debugging
CREATE_NO_WINDOW = 0x08000000
# CREATE_NO_WINDOW = 0

class Database:
    def __init__(self):
        
        self.krzl = ""
        self.feriendaten = ""
        self.nosus = 0

        # Verbindung zur lokalen Datenbank herstellen
        home = environ['HOMEDRIVE']+environ['HOMEPATH']
        if path.exists(home+"\\pyKursbuch") == False:
            system("mkdir "+home+"\\pyKursbuch")
        self.dbpath = home+"\\pyKursbuch"

        self.verbindung = sqlite3.connect(self.dbpath+"\\kurs.db")
        self.c = self.verbindung.cursor()
        # Sicherstellen, dass kurs.db als versteckte Datei angelegt ist
        #subprocess.check_call(["attrib","+H","U:\\kurs.db"])

        # Synchronisationsstatus an/aus erfassen
        self.sync = self.getSyncstate()

        # Verbindung zur zentralen SuS-Datenbank herstellen
        if path.isfile('sus.db'):
            print("sus.db found")
            self.susverbindung = sqlite3.connect("sus.db")
            self.susc = self.susverbindung.cursor()
        else:
            print("sus.db not found")
            # Schaltflächen sperren
            self.nosus = 1

        # Database übergibt sich selbst dem Gui Objekt und instanziiert es
        # import sys
        self.app = QtWidgets.QApplication(sys.argv)
        self.app.setStyle("Fusion")
        
        
        # Austesten, ob die Ersteinrichtung angezeigt werden muss
        try:
            self.krzl = list(self.c.execute("""SELECT Inhalt FROM settings
                                      WHERE Kategorie = "Krzl";"""))
            self.krzl = self.krzl[0][0]
            # Synchronisationsstatus erfassen
            # self.sync = list(self.c.execute("""SELECT Inhalt FROM settings
            #                           WHERE Kategorie = "sync";"""))
            # self.sync = int(self.sync[0][0])
        except:
            # Database übergibt sich selbst dem Objekt Ersteinrichtung 
            # und instanziiert es
            self.firstrun = Ersteinrichtung(self)
            sys.exit(self.app.exec_())
        else:
            # Datenbank vom Server laden, wenn Synchronisation an
            # Wenn self.pw = None -> Passwort erneute abfragen durch Übergabe
            # an Gui Objekt
            pw = keyring.get_password("pyKursbuch", self.krzl.lower())

            if self.sync == 2 and pw != None:
                access = self.get_FTPS_db()
            else:
                access = None

            # Gui Objekt instanziieren, Database übergeben und event loop
            # starten
            self.ui = Gui(self)
            if self.sync == 2:
                if pw == None or access == False:
                    msg_pw = QtWidgets.QMessageBox()
                    msg_pw.setIcon(QtWidgets.QMessageBox.Information)
                    msg_pw.setWindowTitle("Zugangsdaten")
                    msg_pw.setWindowIcon(QtGui.QIcon('kursbuch.ico'))
                    msg_pw.setText("Auf diesem Rechner ist das Passwort noch "+
                                    "nicht zwischengespeichert. Bitte erneut "+
                                    "eingeben")
                    msg_pw.exec_()
                    self.ui.sync()
                if access == "host":
                    msg_host = QtWidgets.QMessageBox()
                    msg_host.setIcon(QtWidgets.QMessageBox.Critical)
                    msg_host.setWindowTitle("Fehler")
                    msg_host.setWindowIcon(QtGui.QIcon('kursbuch.ico'))
                    msg_host.setText("Servername falsch oder Server nicht erreichbar.")
                    msg_host.exec_()
                    self.ui.sync()
            sys.exit(self.app.exec_())

    def createSettings(self, krz):
        """neue Tabelle settings anlegen aus Dialog Ersteinrichtung"""
        self.c.execute(""" CREATE TABLE settings (
                            "pk"	INTEGER,
                            "Kategorie"	VARCHAR(20),
                            "Inhalt" VARCHAR(20),
                            "Schuljahr" VARCHAR(10),
                            "tname" VARCHAR(20),
                            "Sortierung" INTEGER,
                            "lastedit" INTEGER,
                            PRIMARY KEY("pk")
                        )""")
        self.c.execute("""INSERT INTO "settings"
                             ("pk","Kategorie","Inhalt") 
                             VALUES (NULL,"Krzl",?);""", 
                             (krz,))
        self.c.execute("""INSERT INTO "settings"
                             ("Kategorie","Inhalt") 
                             VALUES ("sync",?);""", 
                             (0,))
        self.verbindung.commit()
        self.krzl = krz

    def get_FTPS_db(self):
        self.pw = keyring.get_password("pyKursbuch", self.krzl.lower())
    
        self.login = self.krzl.lower()+":"+self.pw
        self.url = self.get_FTPS_URL()

        # timestamp setzen
        self.timestamp = str(time())
        with open (self.dbpath+"\\timestamp","w") as f:
            f.write(self.timestamp)
        subprocess.call("curl\\curl.exe --retry-max-time 1 --tlsv1.2 --tls-max 1.2 --ftp-ssl -u "+self.login+" -T "+self.dbpath+"\\timestamp ftp://"+self.url+"//timestamp", creationflags=CREATE_NO_WINDOW)
        # kurs.db laden mit log
        subprocess.call("curl\\curl.exe --trace "+self.dbpath+"\\log.txt --retry-max-time 1 --ftp-ssl -u "+self.login+" -o "+self.dbpath+"\\kurs.db ftp://"+self.url+"//kurs.db", creationflags=CREATE_NO_WINDOW)
        with open (self.dbpath+"\\log.txt","r") as f:
            data = f.read()
        system("del "+self.dbpath+"\\log.txt")
        if "not resolve host" in data:
            return "host"
        if "Access denied" in data:
            return False
        else:
            # Intervall Upload in Thread starten, as daemon to exit when 
            # programme is exited
            self.thread = threading.Thread(target=self.interval_upload, daemon=True)
            self.thread.start()

    def save_FTPS_URL(self, url):
        self.c.execute("""DELETE FROM "settings"
                            WHERE "Kategorie" = "FTPS_URL";""")
        self.c.execute("""INSERT INTO "settings"
                            ("Kategorie","Inhalt") 
                            VALUES ("FTPS_URL",?);""", 
                            (url,))
        self.verbindung.commit()

    def get_FTPS_URL(self):
        url = list(self.c.execute("""SELECT Inhalt FROM "settings"
                            WHERE "Kategorie" = "FTPS_URL";
                            """))
        url = url[0][0]
        return url

    def saveSyncstate(self, s, gui):
        if s == 2:
            self.c.execute("""DELETE FROM "settings"
                            WHERE "Kategorie" = "sync";""")
            self.c.execute("""INSERT INTO "settings"
                            ("Kategorie","Inhalt") 
                            VALUES ("sync",?);""", 
                            (s,))
            self.verbindung.commit()
            self.sync = s
            access = self.get_FTPS_db()
            if access == False:
                msg_pw = QtWidgets.QMessageBox()
                msg_pw.setIcon(QtWidgets.QMessageBox.Critical)
                msg_pw.setWindowTitle("Fehler")
                msg_pw.setWindowIcon(QtGui.QIcon('kursbuch.ico'))
                msg_pw.setText("Wahrscheinlich ist das Passwort falsch.")
                msg_pw.exec_()
                gui.sync()
            if access == "host":
                msg_host = QtWidgets.QMessageBox()
                msg_host.setIcon(QtWidgets.QMessageBox.Critical)
                msg_host.setWindowTitle("Fehler")
                msg_host.setWindowIcon(QtGui.QIcon('kursbuch.ico'))
                msg_host.setText("Servername falsch oder Server nicht erreichbar.")
                msg_host.exec_()
                gui.sync()
            else:
                gui.kursauswahlMenue()
        if s == 0:
            # kurs.db auf dem Server löschen
            # Dialog mit Hinweis und Beenden -> Neustart
            msg_restart = QtWidgets.QMessageBox()
            msg_restart.setIcon(QtWidgets.QMessageBox.Question)
            msg_restart.setWindowTitle("Synchronisation entfernen")
            msg_restart.setWindowIcon(QtGui.QIcon('kursbuch.ico'))
            msg_restart.setText("Soll die Datenbank auf dem Server gelöscht, "+
                                "werden? Die lokale Datenbank bleibt erhalten. "+
                                "Das Programm wird geschlossen und muss "+
                                "neugestartet werden.")
            msg_restart.setStandardButtons(QtWidgets.QMessageBox.Ok | QtWidgets.QMessageBox.Cancel)
            abbrechen = msg_restart.button(QtWidgets.QMessageBox.Cancel)
            abbrechen.setText("Abbrechen")
            retval = msg_restart.exec_()
            if retval == 1024:
                self.c.execute("""DELETE FROM "settings"
                            WHERE "Kategorie" = "sync";""")
                self.c.execute("""INSERT INTO "settings"
                            ("Kategorie","Inhalt") 
                            VALUES ("sync",?);""", 
                            (s,))
                self.verbindung.commit()
                self.sync = s
                subprocess.call("curl\\curl.exe --retry-max-time 1 --tlsv1.2 --tls-max 1.2 --ftp-ssl -u "+self.login+" -Q "+'"'+"DELE kurs.db"+'"'+" ftp://"+self.url, creationflags=CREATE_NO_WINDOW)
                self.app.quit()

    def getSyncstate(self):
        """Synchronisationsstatus erfassen"""
        try:
            sync = list(self.c.execute("""SELECT Inhalt FROM settings
                                        WHERE Kategorie = "sync";"""))
            sync = int(sync[0][0])
        except:
            sync = 0
        return sync

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
                            "Pruefung" INTEGER,
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
                       "pk"    INTEGER,
                       "zuab" INTEGER,
                       "Datum" DATE
                       );""")

        self.verbindung.commit()

    def getKurse(self):
        ''' Filtert aus settings die Kursnamen in
        absteigender Reihenfolge der Schuljahre
        '''
        kurse = list(self.c.execute(""" SELECT Inhalt, Schuljahr FROM settings
                                        WHERE Kategorie = "Kurs"
                                        ORDER BY Schuljahr DESC;
                                    """))
        
        kursliste = []

        for i in kurse:
            kursliste.append(i[0])
        return kursliste

    def get_tn(self,k):
        """Tabellennamen zum Anzeigenamen zurückgeben"""
        tabellenname = list(self.c.execute("""SELECT tname FROM settings
                                         WHERE Inhalt = ?;
                                      """,
                                      (k,)))
        return tabellenname[0][0]

    def getDateOfPk(self, k, pk):
        """Datum zum Primary Key ausgeben"""
        tn = self.get_tn(k)
        liste = list(self.c.execute(""" SELECT Datum FROM """+tn+""" 
                                        WHERE pk = ?;
                                    """,
                                    (pk,)))
        datum = liste[0][0]
        return datum

    def getRowOfDate(self,k,d):
        tn = self.get_tn(k)
        listedb = list(self.c.execute(""" SELECT Datum 
                                          FROM """+tn+"""
                                          ORDER BY Datum DESC;
                                      """))
        i = 0
        for datum in listedb:
            if datum[0] == d:
                return i
            else:
                i += 1

    def getCurrentDate(self, k, pk):
        """gibt das aktulle Datum mit der Stunde formatiert zurück"""
        string = self.getDateOfPk(k,pk)
        string = string.split("_")
        datum = datetime.strptime(string[0], '%Y-%m-%d')
        datum = datum.strftime('%a, %d. %b %Y')
        datum = datum +", "+ string[1] +" . Std."
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

    def getDatelist(self, k):
        """ Datumsliste aus Datenbank holen """
        tn = self.get_tn(k)
        listedb = list(self.c.execute(""" SELECT Datum 
                                          FROM """+tn+"""
                                          ORDER BY Datum DESC;
                                      """))
        dbdatetxt = ""
        for i in range(len(listedb)):
            dbdatetxt += listedb[i][0]
        return dbdatetxt
    
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
        self.c.execute(""" UPDATE settings
                           SET lastedit = ?
                           WHERE tname = ?;
                        """,
                        (pk, tn))
        self.verbindung.commit()

    def getLastedit(self,k):
        tn = self.get_tn(k)
        lastedit = list(self.c.execute(""" SELECT lastedit FROM settings
                                           WHERE tname = ?
                                       """,
                                       (tn,)))
        lastedit = lastedit[0][0]
        return lastedit

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
        self.verbindung.commit()

    def deleteKurs(self, k):
        tn = self.get_tn(k)
        self.c.execute(""" DELETE FROM settings
                           WHERE tname = ?;
                           """,
                           (tn,))
        self.verbindung.commit()    

        self.c.execute(""" DROP TABLE """+tn+""";
                           """
                           )
        self.verbindung.commit()    

        tnsus = tn + "_sus"
        self.c.execute(""" DROP TABLE """+tnsus+""";
                           """
                           )
        self.verbindung.commit()    

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
                            "pk"    INTEGER,
                            "zuab"     INTEGER,
                            "Datum"  DATE   
                        );""")
        
        for i in s:
            self.c.execute("""INSERT INTO """ + kurssus + """
                                ("pk", "zuab")
                                VALUES (?,?);""", 
                                (i[2],0))
        self.verbindung.commit()

    def addAbgaenger(self,k,s):
        tn = self.get_tn(k)
        kurssus = tn+"_sus"

        for i in s:
            self.c.execute("""INSERT INTO """ + kurssus + """
                                ("pk", "zuab")
                                VALUES (?,?);""", 
                                (i[2],1))
        self.verbindung.commit()

    def getSuSListe(self,k,m):
        """ Über diese Methode erhält die Mitgliederverwaltung die
        Listen der aktiven (mode=normal) oder Abgänger (mode=abg)
        """
        tn = self.get_tn(k)
        kurssus = tn+"_sus"
        mode = m

        if mode == "normal":
            pkliste = list(self.c.execute("""SELECT pk
                                    FROM """+kurssus+""" 
                                    WHERE zuab = 0
                                    """))
        if mode == "abg":
            pkliste = list(self.c.execute("""SELECT pk 
                                    FROM """+kurssus+"""
                                    WHERE zuab = 1 
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
        """ Über diese Methode erhält die Fehlzeitenanzeige die Daten zu einem
        bestimmten Datum ohne Abgänger
        """
        
        tn = self.get_tn(k)
        # Anführungsstriche um das Datum setzen
        date='"'+date+'"'
        kurssus = tn+"_sus"

        pkliste = list(self.c.execute("""SELECT pk
                                FROM """+kurssus+""" 
                                WHERE zuab = 0
                                """))
 
        try:
            # Prüfen, ob es schon eine Spalte für das Datum gibt und ggf.
            # versuchen, die Spalte hinzuzufügen
            self.susc.execute("""ALTER TABLE sus ADD """+date+""" VARCHAR(12)
                           """)
            self.susverbindung.commit()
        except:
            pass
        
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

    def writeNeueStunde(self, date, std, k, komp):
        tn = self.get_tn(k)
        datum = date+"_"+str(std)
        if self.feriendaten == "":
            self.feriendaten = self.getFerienDaten()
        
        if date in self.feriendaten:
            ferientext = self.getFerientext(date)
            ferientext = "– "+ferientext[0][0]+" –"
            self.c.execute("""INSERT INTO """+tn+"""
                                ("pk","Datum","Inhalt","Ausfall","Kompensation",
                                "Hausaufgabe","Planung") 
                                VALUES (NULL,?,?,1,?,"","");""", 
                                (datum,ferientext,komp))
        else:
            self.c.execute("""INSERT INTO """+tn+"""
                                ("pk","Datum","Inhalt","Ausfall","Kompensation",
                                "Hausaufgabe","Planung") 
                                VALUES (NULL,?,"",0,?,"","");""", 
                                (datum,komp))
        
        self.verbindung.commit()
        newrow = self.getRowOfDate(k,datum)
        return newrow

    def getFerienDaten(self):
        ferienverbindung = sqlite3.connect("ferien.db")
        ferienc = ferienverbindung.cursor()
        liste = list(ferienc.execute("""SELECT Datum 
                                                FROM "ferien";
                                                """,
                                       ))
        feriendaten = ""
        ferienc.close()
        ferienverbindung.close()
        for i in liste:
            feriendaten += i[0]+" "
        return feriendaten

    def getFerientext(self, date):
        ferienverbindung = sqlite3.connect("ferien.db")
        ferienc = ferienverbindung.cursor()
        ferientext = list(ferienc.execute("""SELECT Ferientext 
                                          FROM "ferien"
                                          WHERE Datum = ?;
                                       """,
                                        (date,)))     
        ferienc.close()
        ferienverbindung.close()
        return ferientext

    def getGesamtliste(self):
        """Holt die Gesamtliste aller SuS für Zuordnung zum Kurs"""
        s = list(self.susc.execute("SELECT pk, Name, Vorname, Klasse FROM sus"))
        return s

    def close(self):
        self.c.close()
        self.verbindung.close()
        if self.nosus == 0:
            self.susc.close()
            self.susverbindung.close()
        if self.sync == 2:
            self.upload()
            system("copy "+self.dbpath+"\\kurs.db "+self.dbpath+"\\kurs.dbBACKUP")

    def upload(self):  
        subprocess.call("curl\\curl.exe --tlsv1.2 --tls-max 1.2 --ftp-ssl -u "+self.login+" -T "+self.dbpath+"\\kurs.db ftp://"+self.url+"//kurs.db", creationflags=CREATE_NO_WINDOW)

    def interval_upload(self):
        # started as daemon in thread
        while True:
            sleep(30)
            # Download timestamp and compare
            subprocess.call("curl\\curl.exe --ftp-ssl -u "+self.login+" -o "+self.dbpath+"\\timestamp ftp://"+self.url+"//timestamp", creationflags=CREATE_NO_WINDOW)
            with open (self.dbpath+"\\timestamp","r") as f:
                currentstamp = f.read()
            if self.timestamp == currentstamp:
                try:
                    self.ui.datensatzSpeichernIntervalThread()
                except:
                    pass
                self.upload()
            else:
                self.app.quit()


class Ersteinrichtung(Ui_Ersteinrichtung):
    def __init__(self, db):

        self.db = db

        self.Ersteinrichtung = QtWidgets.QWidget()
        self.setupUi(self.Ersteinrichtung)
        self.Ersteinrichtung.show()

        self.pushButtonAbbrechen.clicked.connect(self.abbrechen)
        self.pushButtonEinrichten.clicked.connect(self.ok)

        # Key Press Events
        self.Ersteinrichtung.keyPressEvent = self.keyPressEvent

    def keyPressEvent(self, e):
        if e.key()  == QtCore.Qt.Key_Return or e.key() == QtCore.Qt.Key_Enter:
            self.ok()
        elif e.key() == QtCore.Qt.Key_Escape :   
            self.abbrechen() 

    def ok(self):
        krzl = self.lineEditKrzl.text().upper().lstrip().rstrip()
        self.db.createSettings(krzl)
        self.Ersteinrichtung.close()
        # Gui Objekt instanziieren und Database übergeben
        self.ui = Gui(self.db)

    def abbrechen(self):
        self.Ersteinrichtung.close()

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

        # Key Press Events
        self.kursneudialog.keyPressEvent = self.keyPressEvent

    def keyPressEvent(self, e):
        if e.key()  == QtCore.Qt.Key_Return or e.key() == QtCore.Qt.Key_Enter:
            self.neu()
        elif e.key() == QtCore.Qt.Key_Escape :   
            self.abbrechen() 

    def neu(self):
        # # Umwandlung in Großbuchstaben mit upper und whitespace enternen
        fach = self.lineEditFachkrzl.text().upper().lstrip().rstrip()
        klasse = self.lineEditKlasse.text().upper().lstrip().rstrip()

        # Unerlaubte Zeichen entfernen
        fach = fach.replace("."," ")
        fach = fach.replace(":","")
        fach = fach.replace(","," ")
        fach = fach.replace(";"," ")
        fach = fach.replace("#"," ")
        fach = fach.replace("!","")
        fach = fach.replace("?","")
        fach = fach.replace("(","")
        fach = fach.replace(")","")
        fach = fach.replace('"','')
        fach = fach.replace("'","")
        fach = fach.replace("&"," und ")
        fach = fach.replace("+"," und ")
        fach = fach.replace("<","")
        fach = fach.replace(">","")
        fach = fach.replace("@","")

        klasse = klasse.replace("."," ")
        klasse = klasse.replace(":","")
        klasse = klasse.replace(","," ")
        klasse = klasse.replace(";"," ")
        klasse = klasse.replace("#"," ")
        klasse = klasse.replace("!","")
        klasse = klasse.replace("?","")
        klasse = klasse.replace("(","")
        klasse = klasse.replace(")","")
        klasse = klasse.replace('"','')
        klasse = klasse.replace("'","")
        klasse = klasse.replace("&"," und ")
        klasse = klasse.replace("+"," und ")
        klasse = klasse.replace("<","")
        klasse = klasse.replace(">","")
        klasse = klasse.replace("@","")

        # bei leerem Feld warnen
        if fach  == "" or klasse == "":
            # WARNUNG
            warn = QtWidgets.QMessageBox()
            warn.setIcon(QtWidgets.QMessageBox.Warning)
            warn.setText("Bitte beide Felder füllen.")
            warn.setWindowTitle("Warnung")
            warn.setWindowIcon(QtGui.QIcon('kursbuch.ico'))
            warn.exec_()
        else:
            schuljahr = self.comboBoxSchuljahr.currentText()
            anzeigename = fach + " " + klasse + " " + schuljahr
            schuljahr_ = schuljahr.replace("/","_")
            tabellenname = (self.db.krzl + "_" + fach + "_" + klasse + "_" + schuljahr_)

            # Sonderzeichen und Leerzeichen im Tabellennamen entfernen
            tabellenname = tabellenname.replace("-","_")
            tabellenname = tabellenname.replace("/","_")
            tabellenname = tabellenname.replace(" ","_")

            # Namen und Schuljahr an Datenbankobjekt übergeben
            self.db.createKurs(anzeigename, tabellenname, schuljahr)
            self.gui.kursauswahlMenue()
            self.kursneudialog.close()

            # Kurs einstellen, anzeigen und Dialog neue Stunde öffnen
            self.gui.comboBoxKurs.setCurrentText(anzeigename)
            self.gui.kursAnzeigen()
            self.gui.neueStunde()

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
        self.changeDatesSeries()
        self.calendarWidget.clicked.connect(self.changeDatesSeries)
        self.comboBoxSerie.setCurrentIndex(0)

        # let non editable combobox in fusion style still respect maxitems
        self.comboBoxSerie.setStyleSheet("combobox-popup: 0;")

        # Key Press Events von Form umleiten
        self.Form.keyPressEvent = self.keyPressEvent

    def keyPressEvent(self, e):
        if e.key()  == QtCore.Qt.Key_Return or e.key() == QtCore.Qt.Key_Enter:
            self.neueStundeAnlegen()
        elif e.key() == QtCore.Qt.Key_Escape :   
            self.abbrechen()   

    def changeDatesSeries(self):
        # Combobox mit Daten füllen
        datum = str(self.calendarWidget.selectedDate().toPyDate())
        datum_std = datum.split("_")
        datum = datum_std[0].split("-")
        day = datum[2]
        month = datum[1]
        year = datum[0]
        thedate = date(int(year), int(month.lstrip("0")), int(day.lstrip("0")))
        self.datelist = []
        i = 1
        while i <= 24:
            thedate = thedate + timedelta(days=7)
            self.datelist.append(thedate.strftime("%d.%m.%Y"))
            i += 1
        self.comboBoxSerie.clear()
        self.comboBoxSerie.addItem("keine Wiederholung")
        self.comboBoxSerie.setCurrentIndex(0)
        self.comboBoxSerie.addItems(self.datelist)

    def neueStundeAnlegen(self):
        datum = str(self.calendarWidget.selectedDate().toPyDate())
        dbdatelist = self.db.getDatelist(self.kurs)
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
            self.message.setWindowIcon(QtGui.QIcon('kursbuch.ico'))
            self.message.setText("Bitte eine Stunde angeben.")
            self.message.exec_()
        else:
            # Datum an Datenbankobjekt übergeben und 
            # new row und new pk erhalten
            
            # Duplikate filtern und Hinweis, wenn kein Serientermin
            if str(datum+"_"+stunde) in dbdatelist:
                if self.comboBoxSerie.currentText() == "keine Wiederholung":
                    msg = QtWidgets.QMessageBox()
                    msg.setIcon(QtWidgets.QMessageBox.Critical)
                    msg.setWindowTitle("Fehler")
                    msg.setWindowIcon(QtGui.QIcon('kursbuch.ico'))
                    msg.setText("Diese Stunde existiert bereits.")
                    msg.exec_()
                else:
                    pass
            else:
                if self.checkBox.isChecked() == True:
                    komp = 1
                else:
                    komp = 0
                newrow = self.db.writeNeueStunde(datum, stunde, self.kurs, komp)
            # Serientermine
            x = int(self.spinBox.text())
            if self.checkBox.isChecked() == True:
                komp = 1
            else:
                komp = 0
            if self.comboBoxSerie.currentText() != "keine Wiederholung":
                for i in range(self.comboBoxSerie.currentIndex()):
                    if i+1 in range(0,60,x):
                        repeatdate = self.datelist[i].split(".")
                        repeatdate = (repeatdate[2]+"-"+repeatdate[1]+"-"+
                                    repeatdate[0])
                        # Duplikate filtern
                        if str(repeatdate+"_"+stunde) in dbdatelist:
                            pass
                        else:
                            newrow = self.db.writeNeueStunde(repeatdate, 
                                                             stunde, 
                                                             self.kurs,
                                                             komp)            
            self.gui.kursAnzeigen()
            try:
                self.gui.tableWidget.selectRow(newrow)
            except:
                pass
            self.gui.datensatzAnzeigen()
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

        # Auf dem Desktop zentrieren
        # geometry of the main window
        qr = self.susverwgui.frameGeometry()
        # center point of screen
        cp = QtWidgets.QDesktopWidget().availableGeometry().center()
        # move rectangle's center point to screen's center point
        qr.moveCenter(cp)
        # Taskleiste abziehen
        qr.setTop(qr.top()-15)
        # top left of rectangle becomes top left of window centering it
        self.susverwgui.move(qr.topLeft())

        self.susverwgui.show()

        self.tableWidget.setColumnWidth(0,190)
        self.tableWidget_2.setColumnWidth(0,190)
        self.tableWidget_3.setColumnWidth(0,190)

        # Listen bereitstellen
        self.liste2 = []
        self.liste2sorted = []
        self.liste3 = []
        self.liste3sorted = []
        
        # Zeigt die Liste der Schüler im Kurs
        self.labelLerngruppe.setText("Mitglieder der Lerngruppe: "+self.kurs)
        self.liste2 = self.db.getSuSListe(self.kurs, "normal")
        self.liste2sorted = self.liste2
        z = 0
        for i in self.liste2sorted:
            self.tableWidget_2.setRowCount(z+1)
            self.tableWidget_2.setItem(
                    z,0,QtWidgets.QTableWidgetItem(i[0]+", "+i[1]))
            self.tableWidget_2.setItem(z,1,QtWidgets.QTableWidgetItem(i[3]))
            z += 1

        # Zeigt die Liste der Abgänger im Kurs
        self.liste3 = self.db.getSuSListe(self.kurs, "abg")
        self.liste3sorted = self.liste3
        z = 0
        for i in self.liste3sorted:
            self.tableWidget_3.setRowCount(z+1)
            self.tableWidget_3.setItem(
                    z,0,QtWidgets.QTableWidgetItem(i[0]+", "+i[1]))
            self.tableWidget_3.setItem(z,1,QtWidgets.QTableWidgetItem(i[3]))
            z += 1



        # Signals and slots
        self.comboBox.activated.connect(self.zeigeKlasse)
        self.pushButtonAddSelected.clicked.connect(self.susadd)
        self.pushButtonDeleteSelected.clicked.connect(self.susdel)
        self.pushButtonAddAll.clicked.connect(self.susaddall)
        self.pushButtonDeleteAll.clicked.connect(self.susdelall)
        self.pushButtonAbgangAdd.clicked.connect(self.abgangAdd)
        self.pushButtonAbgangDel.clicked.connect(self.abgangDel)

        klassen = ["5a", "5b", "5c", "5d", "5e",
                   "6a", "6b", "6c", "6d", "6e",
                   "7a", "7b", "7c", "7d", "7e",
                   "8a", "8b", "8c", "8d", "8e",
                   "9a", "9b", "9c", "9d", "9e",
                   "10a", "10b", "10c", "10d", "10e",
                    "EF", "Q1", "Q2"]
        self.comboBox.addItems(klassen)

    def zeigeKlasse(self):
        """ Zeigt die Liste der Schüler der ausgewählten Klasse """

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
                self.filtered.append([i[1], i[2], i[0], i[3]])
                z += 1

    def susadd(self):
        selection = self.tableWidget.selectionModel().selectedRows()

        for i in selection:
            if self.filtered[i.row()] in self.liste2:
                pass
            else:
                self.liste2.append(self.filtered[i.row()])
        # Liste mit Umlauten korrekt sortieren: üblicherweise 
        # sorted(self.liste2, key=locale.strxfrm), bei Liste von Listen mit
        # labmda Funktion für jede Liste in der Liste
        self.liste2sorted = sorted(self.liste2, key=lambda i: locale.strxfrm(i[0]))

        z = 0
        for i in self.liste2sorted:
            self.tableWidget_2.setRowCount(z+1)
            self.tableWidget_2.setItem(
                    z,0,QtWidgets.QTableWidgetItem(i[0]+", "+i[1]))
            self.tableWidget_2.setItem(z,1,QtWidgets.QTableWidgetItem(i[3]))
            z += 1

        # Auswahl wieder aufheben
        self.tableWidget.clearSelection()

        self.save()

    def susaddall(self):
        try:
            self.tableWidget.clearSelection()
            for i in range(len(self.filtered)):
                self.tableWidget.selectRow(i)
            msg = QtWidgets.QMessageBox()
            msg.setIcon(QtWidgets.QMessageBox.Question)
            msg.setText("Sollen alle Schüler*innen hinzugefügt werden?")
            msg.setWindowTitle("Mitglieder hinzufügen")
            msg.setWindowIcon(QtGui.QIcon('kursbuch.ico'))
            msg.setStandardButtons(QtWidgets.QMessageBox.Ok | QtWidgets.QMessageBox.Cancel)
            abbrbutton = msg.button(QtWidgets.QMessageBox.Cancel)
            abbrbutton.setText("Abbrechen")
            retval = msg.exec_()

            if retval == 1024:
                self.susadd()
            else:
                self.tableWidget.clearSelection()
        except:
            pass

    def susdel(self):
        selection = self.tableWidget_2.selectionModel().selectedRows()
        # in umgekehrter Reihenfolge, da sonst die indexes verrutschen
        for i in sorted(selection, reverse = True):
            del self.liste2sorted[i.row()]
        self.liste2 = self.liste2sorted
        
        z = 0
        for i in self.liste2sorted:
            self.tableWidget_2.setRowCount(z+1)
            self.tableWidget_2.setItem(
                    z,0,QtWidgets.QTableWidgetItem(i[0]+", "+i[1]))
            self.tableWidget_2.setItem(z,1,QtWidgets.QTableWidgetItem(i[3]))
            z += 1

        # Auswahl wieder aufheben
        self.tableWidget_2.clearSelection()
        
        # Wenn liste2sorted leer, verbleibende rows entfernen
        if self.liste2sorted == []:
            self.tableWidget_2.setRowCount(0)

        self.save()

    def susdelall(self):
        try:
            self.tableWidget_2.clearSelection()
            for i in range(len(self.liste2sorted)):
                self.tableWidget_2.selectRow(i)
            msg = QtWidgets.QMessageBox()
            msg.setIcon(QtWidgets.QMessageBox.Question)
            msg.setText("Sollen alle Schüler*innen gelöscht werden?")
            msg.setWindowTitle("Mitglieder löschen")
            msg.setWindowIcon(QtGui.QIcon('kursbuch.ico'))
            msg.setStandardButtons(QtWidgets.QMessageBox.Ok | QtWidgets.QMessageBox.Cancel)
            abbrbutton = msg.button(QtWidgets.QMessageBox.Cancel)
            abbrbutton.setText("Abbrechen")
            retval = msg.exec_()

            if retval == 1024:
                self.susdel()
            else:
                self.tableWidget_2.clearSelection()
        except:
            pass

    def abgangAdd(self):
        selection = self.tableWidget_2.selectionModel().selectedRows()

        for i in selection:
            if self.liste2sorted[i.row()] in self.liste3:
                pass
            else:
                self.liste3.append(self.liste2sorted[i.row()])
        # Liste mit Umlauten korrekt sortieren: üblicherweise 
        # sorted(self.liste2, key=locale.strxfrm), bei Liste von Listen mit
        # labmda Funktion für jede Liste in der Liste
        self.liste3sorted = sorted(self.liste3, key=lambda i: locale.strxfrm(i[0]))

        z = 0
        for i in self.liste3sorted:
            self.tableWidget_3.setRowCount(z+1)
            self.tableWidget_3.setItem(
                    z,0,QtWidgets.QTableWidgetItem(i[0]+", "+i[1]))
            self.tableWidget_3.setItem(z,1,QtWidgets.QTableWidgetItem(i[3]))
            z += 1

        # Eintrag aus Widget 2 löschen und Ansicht aktualisieren
        # in umgekehrter Reihenfolge, da sonst die indexes verrutschen
        for i in sorted(selection, reverse = True):
            del self.liste2sorted[i.row()]
        self.liste2 = self.liste2sorted

        z = 0
        for i in self.liste2sorted:
            self.tableWidget_2.setRowCount(z+1)
            self.tableWidget_2.setItem(
                    z,0,QtWidgets.QTableWidgetItem(i[0]+", "+i[1]))
            self.tableWidget_2.setItem(z,1,QtWidgets.QTableWidgetItem(i[3]))
            z += 1

        # Auswahl wieder aufheben
        self.tableWidget_2.clearSelection()

        self.save()
    
    def abgangDel(self):
        selection = self.tableWidget_3.selectionModel().selectedRows()

        for i in selection:
            if self.liste3sorted[i.row()] in self.liste2:
                pass
            else:
                self.liste2.append(self.liste3sorted[i.row()])
        # Liste mit Umlauten korrekt sortieren: üblicherweise 
        # sorted(self.liste2, key=locale.strxfrm), bei Liste von Listen mit
        # labmda Funktion für jede Liste in der Liste
        self.liste2sorted = sorted(self.liste2, key=lambda i: locale.strxfrm(i[0]))

        z = 0
        for i in self.liste2sorted:
            self.tableWidget_2.setRowCount(z+1)
            self.tableWidget_2.setItem(
                    z,0,QtWidgets.QTableWidgetItem(i[0]+", "+i[1]))
            self.tableWidget_2.setItem(z,1,QtWidgets.QTableWidgetItem(i[3]))
            z += 1

        # Eintrag aus Widget 3 löschen und Ansicht aktualisieren
        # in umgekehrter Reihenfolge, da sonst die indexes verrutschen
        for i in sorted(selection, reverse = True):
            del self.liste3sorted[i.row()]
        self.liste3 = self.liste3sorted

        z = 0
        for i in self.liste3sorted:
            self.tableWidget_3.setRowCount(z+1)
            self.tableWidget_3.setItem(
                    z,0,QtWidgets.QTableWidgetItem(i[0]+", "+i[1]))
            self.tableWidget_3.setItem(z,1,QtWidgets.QTableWidgetItem(i[3]))
            z += 1

        # Auswahl wieder aufheben
        self.tableWidget_3.clearSelection()

        # Wenn liste2sorted leer, verbleibende rows entfernen
        if self.liste3sorted == []:
            self.tableWidget_3.setRowCount(0)
        self.save()

    def save(self):
        self.db.writeSuSListe(self.kurs,self.liste2sorted)
        self.db.addAbgaenger(self.kurs,self.liste3sorted)
        # Wenn Fehlzeitenanzeige offen, direkt aktualisieren
        if self.gui.tabWidget.currentIndex() == 1:
            self.gui.fehlzeitenAnzeige(1)

class Kursbuch_Dialog(Ui_PdfExportieren):
    def __init__(self, tn, kurs, krzl, dbpath, nosus):
        self.PdfExportieren = QtWidgets.QWidget()
        self.setupUi(self.PdfExportieren)
        self.PdfExportieren.show()

        self.tn = tn
        self.kurs = kurs
        self.krzl = krzl
        self.dbpath = dbpath
        self.nosus = nosus

        self.pushButtonExport.clicked.connect(self.ok)
        self.pushButtonAbbrechen.clicked.connect(self.abbrechen)

        # Key Press Events
        self.PdfExportieren.keyPressEvent = self.keyPressEvent

    def keyPressEvent(self, e):
        if e.key()  == QtCore.Qt.Key_Return or e.key() == QtCore.Qt.Key_Enter:
            self.ok()
        elif e.key() == QtCore.Qt.Key_Escape :   
            self.abbrechen() 

    def ok(self):
        if self.radioButtonMitFs.isChecked() == True:
            var = "1"
        if self.radioButtonOhneFS.isChecked() == True:
            var = "2"
        self.PdfExportieren.close()
        report.makeKursbuch(self.tn, self.kurs, self.krzl, var, self.dbpath, self.nosus)

    def abbrechen(self):
        self.PdfExportieren.close()


class Sync(Ui_Syncdialog):
    def __init__(self, db, gui):
        self.Syncdialog = QtWidgets.QDialog()
        self.setupUi(self.Syncdialog)
        self.Syncdialog.show()

        self.db = db
        self.gui = gui

        # aktuelle Einträge aus db einfüllen
        try:
            if self.db.sync == 2:
                self.checkBoxSync.setChecked(2)
        except:
            pass

        try:
            self.lineEditFTPS.setText(self.db.get_FTPS_URL())
            self.lineEditPW.setText(self.db.pw)
        except:
            pass

        # signals and slots
        self.pushButtonUebernehmen.clicked.connect(self.uebernehmen)
        self.pushButtonAbbrechen.clicked.connect(self.abbrechen)

    def uebernehmen(self):
        url = self.lineEditFTPS.text()
        pw = self.lineEditPW.text()
        self.db.save_FTPS_URL(url)
        keyring.set_password("pyKursbuch", self.db.krzl.lower(), pw)
        
        print(self.checkBoxSync.checkState())
        if self.checkBoxSync.checkState() == 2:
            self.db.saveSyncstate(2, self.gui)
        else:
            self.db.saveSyncstate(0, self.gui)

        self.Syncdialog.close()

    def abbrechen(self):
        self.Syncdialog.close()


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
        
        # self.fehlzeitenansicht = 0
        # self.kurswechel = 0

        self.tableWidget.setColumnWidth(0,140)

        # Kürzel in Fenstertitel anzeigen
        self.MainWindow.setWindowTitle("Kursbuch von "+self.db.krzl)  

        # Methoden aurufen
        self.kursauswahlMenue()

        # Signals and slots
        self.comboBoxKurs.activated.connect(self.kursAnzeigen)
        self.tableWidget.clicked.connect(self.datensatzAnzeigen)
        self.pushButtonNeuerKurs.clicked.connect(self.kursNeu)
        self.pushButtonDelKurs.clicked.connect(self.kursDel)
        self.pushButtonKursmitglieder.clicked.connect(self.schuelerVerw)
        self.pushButtonNeueStd.clicked.connect(self.neueStunde)
        self.pushButtonDelStd.clicked.connect(self.stundeDel)
        self.pushButtonKursheftAnzeigen.clicked.connect(self.kursheftAnzeigen)
        self.tabWidget.tabBarClicked.connect(self.fehlzeitenAnzeige)
        self.actionSynchronisation_einrichten.triggered.connect(self.sync)

        if self.db.nosus == 1:
            self.tabWidget.setTabEnabled(1,False)

        self.comboBoxKurs.setStyleSheet("combobox-popup: 0;")

        # alle focusChanged Events der App an self.leave leiten
        self.db.app.focusChanged.connect(self.leave)

        self.MainWindow.closeEvent = self.closeEvent

        self.abouttoclose = 0

    def closeEvent(self, event):
        self.abouttoclose = 1
        if self.kurs != "":
            self.datensatzSpeichern()
        self.db.close()

    def leave(self, old, new):
        # prüfen welche Felder welchen Fokuswechsel haben
        if self.abouttoclose != 1:
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
        self.pushButtonDelStd.setEnabled(False)

    def enableFieldsStd(self):
        self.textEditKurshefteintrag.setEnabled(True)
        self.textEditHausaufgaben.setEnabled(True)
        self.textEdit.setEnabled(True)
        self.checkBox.setEnabled(True)
        self.checkBox_2.setEnabled(True)
        self.pushButtonDelStd.setEnabled(True)

    def enableFieldsKurs(self):
        self.pushButtonDelKurs.setEnabled(True)
        if self.db.nosus == 0:
            self.pushButtonKursmitglieder.setEnabled(True)
        self.pushButtonNeueStd.setEnabled(True)
        self.pushButtonKursheftAnzeigen.setEnabled(True)
    
    def disableFieldsKurs(self):
        self.pushButtonDelKurs.setEnabled(False)
        self.pushButtonKursmitglieder.setEnabled(False)
        self.pushButtonNeueStd.setEnabled(False)
        self.pushButtonKursheftAnzeigen.setEnabled(False)

    def kursAnzeigen(self):
        """ setzt die aktuelle Combobox-Auswahl als Kursvariable
        und führt die Methode zum Füllen des tableWidgets/listbox aus
        """
        self.disableFieldsStd()
        self.kurs = self.comboBoxKurs.currentText()

        self.fillListbox(1)

        self.enableFieldsKurs()

        # self.pk für den aktuellen Datensatz zunächst auf "" setzen
        self.pk = ""

        # Fehlzeiten Widget schließen -> bei Kurswechsel keine falschen Fehlzeiten
        self.verticalLayoutWidget.close()

    def markieren(self, *args):
        pass
        # self.datensatzSpeichern()
        # self.fillListbox()

    def fillListbox(self, lastedit=None):
        self.stdliste = self.db.getListe(self.kurs)
        self.tableWidget.setRowCount(len(self.stdliste))
    
        z = 0
        for i in self.stdliste:
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

        # lastedit auswählen wenn Kurs gerade ausgewählt
        if lastedit == 1:
            print(self.db.getLastedit(self.kurs))
            lastpk = self.db.getLastedit(self.kurs)
            if lastpk == "" or lastpk == None:
                pass
            else:
                dateofpk = self.db.getDateOfPk(self.kurs, lastpk)
                print(dateofpk)
                row = self.db.getRowOfDate(self.kurs, dateofpk)
                print(row)
                self.tableWidget.selectRow(row)


    def datensatzAnzeigen(self):
        self.enableFieldsStd()
        # Aktuelle Datumsauswahl in Variable speichern
        auswahl = self.tableWidget.currentRow()

        # Zugehörigen Primary Key der Auswahl setzen
        self.pk = self.db.getListe(self.kurs)[auswahl][0]
        # Datensatz als liste holen
        liste = self.db.getDatensatz(self.pk, self.kurs)      
        # # Textvariable mit Text aus Datenbankfeld füllen
        self.textEditKurshefteintrag.setText(liste[0][2])
        
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

    def kursDel(self):
        """Löscht einen Kurs ohne die eingetragenen Fehlzeiten"""
        msg = QtWidgets.QMessageBox()
        msg.setIcon(QtWidgets.QMessageBox.Question)
        msg.setText("Soll der Kurs "+self.kurs+" gelöscht werden?\n\n"+
                    "Eingetragene Fehlzeiten werden dabei nicht aus der Datenbank entfernt.")
        msg.setWindowTitle("Kurs löschen")
        msg.setWindowIcon(QtGui.QIcon('kursbuch.ico'))
        msg.setStandardButtons(QtWidgets.QMessageBox.Ok | QtWidgets.QMessageBox.Cancel)
        loeschbutton = msg.button(QtWidgets.QMessageBox.Ok)
        loeschbutton.setText("Löschen")
        abbrbutton = msg.button(QtWidgets.QMessageBox.Cancel)
        abbrbutton.setText("Abbrechen")
        retval = msg.exec_()
        if retval == 1024:
            warn = QtWidgets.QMessageBox()
            warn.setIcon(QtWidgets.QMessageBox.Warning)
            warn.setText("Achtung! Der Kurs und alle Stundeninhalte werden gelöscht.\n\n"+
                        "Wirklich löschen?")
            warn.setWindowTitle("Kurs löschen")
            warn.setWindowIcon(QtGui.QIcon('kursbuch.ico'))
            warn.setStandardButtons(QtWidgets.QMessageBox.Ok | QtWidgets.QMessageBox.Cancel)
            loeschbutton = warn.button(QtWidgets.QMessageBox.Ok)
            loeschbutton.setText("Löschen")
            abbrbutton = warn.button(QtWidgets.QMessageBox.Cancel)
            abbrbutton.setText("Abbrechen")
            retval = warn.exec_()
            if retval == 1024:
                self.db.deleteKurs(self.kurs)
                self.kurs = ""
                self.pk = ""
                self.kursauswahlMenue()
                self.tableWidget.setRowCount(0)
                self.disableFieldsStd()
                self.disableFieldsKurs()
                if self.tabWidget.currentIndex() == 1:
                    self.fehlzeitenAnzeige(1)

    def schuelerVerw(self):
        self.susverw = SuSVerw(self, self.db, self.kurs)

    def neueStunde(self):
        """instanziiert das Objekt KursAnlegen und übergibt 
        sich selbst, db und kurs
        """
        self.neuestd = StundeAnlegen(self, self.db, self.kurs)    

    def stundeDel(self):
        """Löscht die aktuelle Stunde ohne die eingetragenen Fehlzeiten"""
        msg = QtWidgets.QMessageBox()
        msg.setIcon(QtWidgets.QMessageBox.Question)
        msg.setText("Soll die Stunde "+'"'+str(self.db.getCurrentDate(self.kurs, self.pk))+'"'+" gelöscht werden?\n\n"+
                    "Eingetragene Fehlzeiten werden dabei nicht aus der Datenbank entfernt.")
        msg.setWindowTitle("Stunde löschen")
        msg.setWindowIcon(QtGui.QIcon('kursbuch.ico'))
        msg.setStandardButtons(QtWidgets.QMessageBox.Ok | QtWidgets.QMessageBox.Cancel)
        loeschbutton = msg.button(QtWidgets.QMessageBox.Ok)
        loeschbutton.setText("Löschen")
        abbrbutton = msg.button(QtWidgets.QMessageBox.Cancel)
        abbrbutton.setText("Abbrechen")
        retval = msg.exec_()
        if retval == 1024:
            self.db.deleteDatensatz(self.kurs, self.pk)
            self.kursAnzeigen()
            self.tableWidget.clearSelection()

    def datensatzSpeichern(self):
        # Inhalt der aktuellen Felder speichern
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

    def datensatzSpeichernIntervalThread(self):
        inhaltNeu = self.textEditKurshefteintrag.toPlainText()
        haNeu = self.textEditHausaufgaben.toPlainText()
        planungNeu = self.textEdit.toPlainText()
        
        verbindung_thread = sqlite3.connect(self.db.dbpath+"\\kurs.db")
        c_thread = verbindung_thread.cursor()
        tabellenname = list(c_thread.execute("""SELECT tname FROM settings
                                         WHERE Inhalt = ?;
                                      """,
                                      (self.kurs,)))
        tn = tabellenname[0][0]
        c_thread.execute(""" UPDATE """+tn+"""
                    SET Inhalt = ?, 
                    Hausaufgabe = ?, 
                    Planung = ?
                    WHERE pk = ?;
                    """,
                    (inhaltNeu, haNeu, planungNeu, self.pk))
        verbindung_thread.commit()
        c_thread.close()
        verbindung_thread.close()

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

                    if self.sus[i][3] == "0" or "NULL":
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
        fstatus = sender[0]
        pk = self.sus[int(sender[1])][0]
        self.db.writeFehlzeiten(pk,fstatus,self.kurs, self.datum)

    def sync(self):
        self.sdialog = Sync(self.db, self)
    
    def tutmod(self):
        pass
        """ Objekt für Tutorenmodus instanziieren und starten"""

    def kursheftAnzeigen(self):
        # Kursbuch Dialog instanziieren
        self.kdialog = Kursbuch_Dialog(self.db.get_tn(self.kurs), self.kurs, self.db.krzl, self.db.dbpath, self.db.nosus)


if __name__ == "__main__":
    Database()