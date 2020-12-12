import sqlite3
import tkinter as tk
from tkinter import ttk
#from ttkthemes import ThemedTk
#from tkcalendar import Calendar, DateEntry
#from time import strftime
#from tkinter import font
import locale
 
locale.setlocale(locale.LC_ALL, 'deu_deu')


class SuSVerwaltung:
    def __init__(self, g, db, k):
        self.gui = g
        self.db = db
        self.kurs = k

        # Main Window erzeugen
        #self.master = ThemedTk(theme="arc")
        self.susvtop = tk.Tk()

        # Default Font setzten für Plattformkompatibilität
        # def_font = font.nametofont("TkDefaultFont")
        # def_font.configure(family="Segoe UI", size=9)

        self.susvtop.title("Schüler*innen Verwaltung - "+
                          "Kursbuch von " + self.db.krzl)
        self.susvtop.geometry('790x672')
        # Größenänderungen kontrollieren
        #self.susvtop.minsize(width=900, height=600)
        #self.susvtop.resizable(width=False, height=False)

        # Main Window in der Mitte des Bildschirms positionieren.
        position_x= int(self.susvtop.winfo_screenwidth()/2 - 395)
        position_y= int(self.susvtop.winfo_screenheight()/2 - 366)
        self.susvtop.geometry("+{}+{}".format(position_x, position_y))

        # Window Deletion abfangen, speichern und Datenbank schließen
        # def on_closing():
            #if self.kurs != "":
            #    self.datensatzSpeichern()
            # self.db.close()
            # self.susvtop.destroy()

        # self.susvtop.protocol("WM_DELETE_WINDOW", on_closing)
        
        # Variable für den aktuellen Primary Key
        self.pk = ""
        
        # Frame Links
        self.frameLinks = ttk.Frame(self.susvtop, borderwidth=10)
        self.frameLinks.pack(side="left", fill="y", anchor="w", expand=1)
        
        # Frame Klassenmenü
        self.frameKlassenmenue = ttk.Frame(self.frameLinks)
        self.frameKlassenmenue.pack()
        # Label Filter Klasse
        self.labelFilter = ttk.Label(self.frameKlassenmenue, 
                                       text="Filter auf: ")
        self.labelFilter.pack(side="left", anchor="w")
        
        # Kontrollvariable für OptionsMenu
        self.var = tk.StringVar()

        klassen = ["5a", "5b", "5c", "5d", "5e",
                   "6a", "6b", "6c", "6d", "6e",
                   "7a", "7b", "7c", "7d", "7e",
                   "8a", "8b", "8c", "8d", "8e",
                   "9a", "9b", "9c", "9d", "9e",
                   "10a", "10b", "10c", "10d", "10e",
                    "EF", "Q1", "Q2"]

        # Klassenmenü 
        self.menuKlassen = ttk.OptionMenu(self.frameKlassenmenue, self.var, 
                                          "Klasse",
                                          *klassen,
                                          command=self.zeigeKlasse)
        self.menuKlassen.configure(width=10)
        self.menuKlassen.pack(anchor="w", padx=10)
        
        
        
        # Frame für Gesamtliste
        self.frameGesamtliste = ttk.Frame(self.frameLinks, borderwidth=0)
        self.frameGesamtliste.pack(fill="y", expand=1)
        self.scrollbar = ttk.Scrollbar(self.frameGesamtliste)
        # Listbox für Datum, die Option exportselection=False führt dazu, dass
        # der gewählte Eintrag immer aktiv bleibt und keine leeren Tupel 
        # ausgegeben werden
        self.listbox = tk.Listbox(self.frameGesamtliste, exportselection=False,
                                yscrollcommand = self.scrollbar.set, width=50)  
        self.scrollbar.config(command=self.listbox.yview)
        self.listbox.pack(side="left", fill = "both")
        self.scrollbar.pack(side = "left", fill = "y")

        # Frame Mitte
        self.frameMitte = ttk.Frame(self.susvtop, borderwidth=10)
        self.frameMitte.pack(side="left", anchor="w", expand=1, pady=50)

        # Hinzufügen Button
        self.susAddButton = ttk.Button(self.frameMitte, width=5,
                                       text="+",
                                       command=self.susadd)
        self.susAddButton.pack()

        # Löschen Button
        self.susDelButton = ttk.Button(self.frameMitte, width=5,
                                            text="-",
                                            command=self.susdel)
        self.susDelButton.pack(pady=20)

        # Übernehmen Button
        self.uebernehmenButton = ttk.Button(self.frameMitte, width=12,
                                            text="übernehmen",
                                            command=self.uebernehmen)
        self.uebernehmenButton.pack(pady=50)

        # Frame Rechts
        self.frameRechts = ttk.Frame(self.susvtop, borderwidth=10)
        self.frameRechts.pack(side="left", fill="y", anchor="w", expand=1)

        # Label Schülerliste Kurs
        self.labelSuSListe = ttk.Label(self.frameRechts, 
                                       text="Schüler*innen im Kurs "+self.kurs)
        self.labelSuSListe.pack(pady=1)

        # SuSListe
        self.frameSuSListe = ttk.Frame(self.frameRechts, borderwidth=0)
        self.frameSuSListe.pack(side="left", fill="y")
        self.scrollbar2 = ttk.Scrollbar(self.frameSuSListe)
        # Listbox für Datum, die Option exportselection=False führt dazu, dass
        # der gewählte Eintrag immer aktiv bleibt und keine leeren Tupel 
        # ausgegeben werden
        self.listbox2 = tk.Listbox(self.frameSuSListe, exportselection=False,
                                yscrollcommand = self.scrollbar2.set, width=50)  
        self.scrollbar2.config(command=self.listbox2.yview)
        self.listbox2.pack(side="left", fill = "y")
        self.scrollbar2.pack(side = "left", fill = "y")        
        
        # Listen bereitstellen
        self.liste2 = []
        self.liste2sorted = []

        # Zeigt die Liste der Schüler im Kurs
        self.listbox2.delete(0,'end')
        self.liste2 = self.db.getSuSListe(self.kurs)
        self.liste2sorted = self.liste2
        z = 0
        for i in self.liste2sorted:
            z += 1
            self.listbox2.insert(tk.END, str(z)+". "+i[0]+", "+i[1])

        self.zeigeKlasse(0)
    
        self.susvtop.mainloop()

    def zeigeKlasse(self, k):
        """ Zeigt die Liste der Schüler der ausgewählten Klasse, bzw. wenn
        noch keine Auswahl erfolgt ist, einen Hinweis
        """
        # Listbox leeren
        self.listbox.delete(0,'end')

        # gefilterte Liste bei jedem Aufruf leer bereitstellen
        self.filtered = []

        # Wenn aus init Methode mit 0 aufgerufen -> Hinweis anzeigen
        # TODO: Unlogisch, das kann auch direkt in die init-Methode...

        if k == 0:
            self.listbox.insert(tk.END, "Bitte eine Klasse/Stufe auswählen")

        # Filtern nach OptionMenu Eintrag
        else:
            alle = self.db.getGesamtliste()
            z = 0
            for i in alle:
                if i[3] == k:
                    z += 1
                    self.listbox.insert(tk.END, str(z)+". "+i[1]+", "+i[2]+
                                        " -- "+i[3])
                    self.filtered.append([i[1], i[2], i[0]])

    def susadd(self):
        self.liste2.append(self.filtered[self.listbox.curselection()[0]])
        self.listbox2.delete(0,'end')
        z = 0
        # Liste mit Umlauten korrekt sortieren: üblicherweise 
        # sorted(self.liste2, key=locale.strxfrm), bei Liste von Listen mit
        # labmda Funktion für jedes Liste in der Liste
        self.liste2sorted = sorted(self.liste2, key=lambda i: locale.strxfrm(i[0]))

        for i in self.liste2sorted:
            z += 1
            self.listbox2.insert(tk.END, str(z)+". "+i[0]+", "+i[1])

    def susdel(self):
        del self.liste2sorted[self.listbox2.curselection()[0]]
        self.liste2 = self.liste2sorted
        self.listbox2.delete(0,'end')
        z = 0
        for i in self.liste2sorted:
            z += 1
            self.listbox2.insert(tk.END, str(z)+". "+i[0]+", "+i[1])

    def uebernehmen(self):
        self.db.writeSuSListe(self.kurs,self.liste2sorted)
        self.gui.fehlzeitenAnzeige(1)
        self.susvtop.destroy()