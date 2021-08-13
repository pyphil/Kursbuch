from reportlab.platypus import Paragraph, Table, TableStyle, SimpleDocTemplate
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.pagesizes import A4
from reportlab.lib import colors
# from reportlab.pdfgen import canvas
import sqlite3
from datetime import datetime
import locale
import os
import sys
import subprocess
import threading


def getData(tn, dbpath, nosus):
    if sys.platform == "win32":
        locale.setlocale(locale.LC_ALL, 'deu_deu')
    elif sys.platform == "darwin":
        locale.setlocale(locale.LC_ALL, 'de_DE.UTF-8')
    # Verbindung zur lokalen Datenbank herstellen
    verbindung = sqlite3.connect(dbpath+"kurs.db")
    c = verbindung.cursor()

    # Verbindung zur zentralen SuS-Datenbank herstellen wenn sus.db
    if nosus == 0:
        susverbindung = sqlite3.connect("sus.db")
        susc = susverbindung.cursor()

    # Daten aus der lokalen Datenbank lesen
    text = list(c.execute("""SELECT Datum, Inhalt, Hausaufgabe,
                                    Ausfall, Kompensation
                             FROM """+tn+"""
                             ORDER BY Datum ASC;
                          """))

    datumsliste = []
    for i in text:
        # print(i[0])
        datumsliste.append(i[0])

    # Liste der Primary Keys holen
    kurssus = tn+"_sus"

    pkliste = list(c.execute("""SELECT pk, zuab, Datum
                            FROM """+kurssus+"""
                            """))

    fehlzeiten = []

    if nosus == 0:
        for dateraw in datumsliste:
            # Anführungsstriche um das Datum setzen
            date = '"'+dateraw+'"'
            f = ""
            for i in pkliste:
                if i[1] == 0 and i[2] is None:
                    item = list(susc.execute(
                                """SELECT Name, Vorname, """+date+"""
                                FROM "sus"
                                WHERE pk = ?;
                                """,
                                (i[0],)))
                    # nur den ersten Buchstaben des Vornamens verwenden [:1]
                    if item[0][2] == "1":
                        f += ("a) "+item[0][0]+", " +
                              str(item[0][1])[:1]+".<br/>")
                    if item[0][2] == "2":
                        f += ("a) "+item[0][0]+", " +
                              str(item[0][1])[:1]+". (e)<br/>")
                    if item[0][2] == "3":
                        f += ("b) "+item[0][0]+", " +
                              str(item[0][1])[:1]+". <br/>")
                    if item[0][2] == "4":
                        f += ("Q) "+item[0][0]+", " +
                              str(item[0][1])[:1]+". <br/>")

                # Zugänger filtern (Datum vorhanden)
                elif i[1] == 0 and i[2] is not None:
                    start = datetime.strptime(i[2], "%Y-%m-%d")
                    dateobj = datetime.strptime(
                        dateraw.split("_")[0], "%Y-%m-%d")
                    if start <= dateobj:
                        item = list(susc.execute(
                            """SELECT Name, Vorname, """+date+"""
                                FROM "sus"
                                WHERE pk = ?;
                                """,
                            (i[0],)))
                        # nur den ersten Buchstaben des Vornamens
                        # verwenden [:1]
                        if item[0][2] == "1":
                            f += ("a) "+item[0][0]+", " +
                                  str(item[0][1])[:1]+".<br/>")
                        if item[0][2] == "2":
                            f += ("a) "+item[0][0]+", " +
                                  str(item[0][1])[:1]+". (e)<br/>")
                        if item[0][2] == "3":
                            f += ("b) "+item[0][0]+", " +
                                  str(item[0][1])[:1]+". <br/>")
                        if item[0][2] == "4":
                            f += ("Q) "+item[0][0]+", " +
                                  str(item[0][1])[:1]+". <br/>")

                # Abgänger filtern (zuab = 1 und Datum vorhanden)
                elif i[1] == 1 and i[2] is not None:
                    start = datetime.strptime(i[2], "%Y-%m-%d")
                    dateobj = datetime.strptime(
                        dateraw.split("_")[0], "%Y-%m-%d")
                    if start >= dateobj:
                        item = list(susc.execute(
                            """SELECT Name, Vorname, """+date+"""
                                FROM "sus"
                                WHERE pk = ?;
                                """,
                            (i[0],)))
                        # nur den ersten Buchstaben des Vornamens
                        # verwenden [:1]
                        if item[0][2] == "1":
                            f += ("a) "+item[0][0]+", " +
                                  str(item[0][1])[:1]+".<br/>")
                        if item[0][2] == "2":
                            f += ("a) "+item[0][0]+", " +
                                  str(item[0][1])[:1]+". (e)<br/>")
                        if item[0][2] == "3":
                            f += ("b) "+item[0][0]+", " +
                                  str(item[0][1])[:1]+". <br/>")
                        if item[0][2] == "4":
                            f += ("Q) "+item[0][0]+", " +
                                  str(item[0][1])[:1]+". <br/>")

            fehlzeiten.append(f)
    else:
        # keine Fehlzeiten im ohne sus.db
        pass

    # print(fehlzeiten)
    c.close()
    verbindung.close()

    liste = []
    liste.append(["Datum", "Stundeninhalt", "Lernzeit- /<br/>Hausaufgabe",
                 "Fehlzeiten", "Krzl", "Ausf.", ""])
    z = 0
    for i in text:
        string = str(i[0]).split("_")
        datum = datetime.strptime(string[0], '%Y-%m-%d')
        datum = datum.strftime('%a, %d. %b %Y')
        if "B" in string[1]:
            std = string[1].split("-")[1]
            datum = datum + "<br/> " + "BLOCK (" + std + ". Std.)"
        else:
            datum = datum + "<br/> - " + string[1] + ". Std. -"
        # if i[4] == 1:
        #     datum = datum + "<br/><b/>KOMPENSATION"
        if nosus == 0:
            liste.append([datum, i[1], i[2], fehlzeiten[z], '', i[3], i[4]])
        else:
            liste.append([datum, i[1], i[2], '', '', i[3], i[4]])
        z += 1

    return liste


def footer(canvas, doc):
    styles = getSampleStyleSheet()
    styleN = ParagraphStyle('small',
                            parent=styles['BodyText'],
                            fontSize=8,
                            leading=13,
                            alignment=2,)
    canvas.saveState()
    P = Paragraph("Kenntnisnahme der Abteilungsleitung: __________ ",
                  styleN)
    w, h = P.wrap(doc.width, doc.bottomMargin)
    P.drawOn(canvas, doc.leftMargin, h)
    canvas.restoreState()


def makeKursbuch(tn, k, krz, var, dbpath, nosus):

    styles = getSampleStyleSheet()
    smallerStyle = ParagraphStyle('small',
                                  parent=styles['BodyText'],
                                  fontSize=10,
                                  leading=13,)
    grayStyle = ParagraphStyle('gray',
                               parent=styles['BodyText'],
                               fontSize=10,
                               leading=13,
                               textColor=colors.gray,)

    my_data_raw = getData(tn, dbpath, nosus)

    my_data = []

    for i in my_data_raw:
        if i[5] != 1:
            # Ggf. Kompensation kennzeichnen
            if i[6] == 1:
                P1 = Paragraph(
                    i[0] + "<br/>" +
                    "<b><font color=green>KOMPENSATION</font></b>",
                    smallerStyle)
            else:
                P1 = Paragraph(i[0], smallerStyle)
            P2 = Paragraph(i[1], smallerStyle)
            P3 = Paragraph(i[2], smallerStyle)
            # Wenn ohne Fehlzeiten:
            if var == '2':
                P4 = Paragraph("", smallerStyle)
            else:
                P4 = Paragraph(i[3], smallerStyle)
            P5 = Paragraph(i[4], smallerStyle)

            my_data.append([P1, P2, P3, P4, P5])

        # Bei Ausfall graue Schrift
        if i[5] == 1:
            # Ggf. Kompensation kennzeichnen
            if i[6] == 1:
                P1 = Paragraph(
                    i[0] + "<br/>" +
                    "<b><font color=green>KOMPENSATION</font></b>",
                    grayStyle)
            else:
                P1 = Paragraph(i[0], grayStyle)

            P2 = Paragraph(i[1], grayStyle)
            P3 = Paragraph(i[2], grayStyle)
            P4 = Paragraph(i[3], grayStyle)
            P5 = Paragraph(i[4], grayStyle)

            my_data.append([P1, P2, P3, P4, P5])

    # if path.exists("U:\\Kursbuch-Export") == False:
    #     system("mkdir U:\\Kursbuch-Export")

    filename = dbpath+str(tn+"-"+str(datetime.now().date())+".pdf")

    doc = SimpleDocTemplate(filename, pagesize=A4, leftMargin=60,
                            rightMargin=20, topMargin=20, bottomMargin=40,
                            title=krz + " " + k)
    story = []
    story.append(Paragraph('Kurs: '+krz+" "+k, styles['Normal']))
    t = Table(my_data, repeatRows=1)
    t._argW[0] = 95
    t._argW[1] = 160
    t._argW[2] = 100
    t._argW[3] = 120
    t._argW[4] = 30
    t.hAlign = 'LEFT'
    t.spaceBefore = 10
    t.spaceAfter = 10
    t.setStyle(TableStyle(
        [('BOX', (0, 0), (-1, -1), 0.5, colors.black),
         ('INNERGRID', (0, 0), (-1, -1), 0.5, colors.black),
         ('VALIGN', (0, 0), (-1, -1), 'TOP'),
         ('BACKGROUND', (0, 0), (4, 0), colors.lightgrey), ]))
    story.append(t)
    story.append(Paragraph('', styles['Normal']))
    doc.build(story, onFirstPage=footer, onLaterPages=footer)

    def openChrome_x86():
        CREATE_NO_WINDOW = 0x08000000
        subprocess.call("C:\\Program Files (x86)\\Google\\Chrome\\Application\\chrome.exe " +
                        filename, creationflags=CREATE_NO_WINDOW)
    def openChrome():
        CREATE_NO_WINDOW = 0x08000000
        subprocess.call("C:\\Program Files\\Google\\Chrome\\Application\\chrome.exe " +
                        filename, creationflags=CREATE_NO_WINDOW)

    if sys.platform == "win32":
        if os.path.isfile("C:\\Program Files (x86)\\Google\\Chrome\\Application\\chrome.exe") is True:
            thread = threading.Thread(target=openChrome_x86, daemon=True)
            thread.start()
        elif os.path.isfile("C:\\Program Files\\Google\\Chrome\\Application\\chrome.exe") is True:
            thread = threading.Thread(target=openChrome, daemon=True)
            thread.start()
        else:
            os.startfile(filename)
    elif sys.platform == "darwin":
        subprocess.call(('open', filename))
    elif sys.platform == "linux":
        subprocess.call(('xdg-open', filename))


if __name__ == "__main__":
    makeKursbuch("Tabellenname", "Kursname", "Kürzel", "1", "", "0")
