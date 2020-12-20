import sqlite3

# Exportdatei öffnen, Datenbank öffnen
f = open('Export.txt','r',encoding="utf-8")
verbindung = sqlite3.connect("sus.db")
c = verbindung.cursor()

exporttext = ""
for zeile in f:
    zeile = zeile.replace('"','')
    zeile = zeile.replace('{','')
    zeile = zeile.replace('}','')
    # Jede Zeile zur Variable exporttext hinzufügen
    exporttext += zeile
    # Zeilen in Liste auftrennen
    item = zeile.split(";")
    # Kopfzeile ausnehmen
    if "eindeutige Nummer" in item[0]:
        pass
    else:
        #  Wenn guid nicht in db -> [], dann anlegen, sonst updated
        db = list(c.execute(""" SELECT guid, Name, Vorname, Klasse FROM sus
                                WHERE guid = ?
                            """,
                            (item[0],)))
        if db == []:
            # anlegen
            # Strip zur Entfernung des Zeilenumbruchs im letzten Feld
            c.execute(""" INSERT INTO sus
                        ("Abgang", "guid", "Name", "Vorname", "Klasse")
                        VALUES (0,?,?,?,?); """, 
                        (item[0],item[1],item[2],item[3].strip()))
            verbindung.commit()           
            print("Neuer Eintrag: "+item[1],item[2],item[3].strip())
        else:
            if db[0][1] != item[1] or db[0][2] != item[2] or db[0][3] != item[3]:
                # updaten
                c.execute(""" UPDATE sus
                            SET Name = ?,
                                Vorname = ?,
                                Klasse = ?
                            WHERE guid = ?
                        """,
                        (item[1],item[2],item[3].strip(),item[0]))
                verbindung.commit()
                print("Aktualisierter Eintrag: "+item[1],item[2],item[3].strip())

f.close()

# guids in db durchgehen und wenn nicht in exporttext vorhanden, 
# Abgang auf 1 setzen, sonst 0

# Liste der guids in db holen
guidlist = list(c.execute("SELECT guid FROM sus"))

for i in guidlist:
    if str(i[0]) in exporttext:
        # Abgang auf 0 setzen
        c.execute(""" UPDATE sus
                    SET Abgang = 0
                    WHERE guid = ?
                """,
                (i[0],))
        verbindung.commit()
    else:
        # Abgang auf 1 setzen
        c.execute(""" UPDATE sus
                    SET Abgang = 1
                    WHERE guid = ?
                """,
                (i[0],))
        verbindung.commit()

print("Abgänger manuell in db überprüfen!")
print("Fertig")