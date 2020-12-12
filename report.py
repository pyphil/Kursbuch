from reportlab.platypus import Paragraph, Table, TableStyle, SimpleDocTemplate
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.pagesizes import A4
from reportlab.lib import colors
import sqlite3
from datetime import datetime
import locale
from os import system, path
import subprocess


def getData(tn):
    locale.setlocale(locale.LC_ALL, 'deu_deu')
    # Verbindung zur lokalen Datenbank herstellen
    verbindung = sqlite3.connect("U:\\kurs.db")
    c = verbindung.cursor()

    # Verbindung zur zentralen SuS-Datenbank herstellen
    susverbindung = sqlite3.connect("sus.db")
    susc = susverbindung.cursor()

    # Daten aus der lokalen Datenbank lesen
    text = list(c.execute("""SELECT Datum, Inhalt, Hausaufgabe, Ausfall 
                             FROM """+tn+"""
                             ORDER BY Datum ASC;
                          """))
   
    datumsliste = []
    for i in text:
        #print(i[0])
        datumsliste.append(i[0])

    # Liste der Primary Keys holen
    kurssus = tn+"_sus"
    #print(kurssus)
    pkliste = list(c.execute("""SELECT pk 
                            FROM """+kurssus+""" 
                            """))
    #print(pkliste)
    fehlzeiten = []

    for d in datumsliste:
        # Anführungsstriche um das Datum setzen
        d = '"'+d+'"'
        f = ""
        for pk in pkliste:
            item = list(susc.execute("""SELECT Name,Vorname,"""+d+""" 
                                            FROM "sus"
                                            WHERE pk = ?;
                                        """,
                                        (pk[0],)))
            #print(item)
            # nur den ersten Buchstaben des Vornamens verwenden [:1]
            if item[0][2] == "1":
                f += ("a) "+item[0][0]+", "+str(item[0][1])[:1]+".<br/>")
            if item[0][2] == "2":
                f += ("a) "+item[0][0]+", "+str(item[0][1])[:1]+". (e)<br/>")
            if item[0][2] == "3":
                f += ("b) "+item[0][0]+", "+str(item[0][1])[:1]+". <br/>")
            if item[0][2] == "4":
                f += ("Q) "+item[0][0]+", "+str(item[0][1])[:1]+". <br/>")
        fehlzeiten.append(f)
    #print(fehlzeiten)
    c.close()
    verbindung.close()


    liste = []
    liste.append(["Datum", "Stundeninhalt", "Hausaufgabe", "Fehlzeiten", "Krzl", "Ausf."])
    z = 0
    for i in text:
        string = str(i[0]).split("_")
        datum = datetime.strptime(string[0], '%Y-%m-%d')
        datum = datum.strftime('%a, %d. %b %Y')
        datum = datum + "<br/> - " + string[1] +". Std. -"
        liste.append([datum,i[1],i[2],fehlzeiten[z],'',i[3]])
        z += 1

    return liste


def makeKursbuch(tn, k, krz, var):

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

    my_data_raw = getData(tn)

    my_data = []
    
    for i in my_data_raw:  
        if i[5] != 1:
            P1 = Paragraph(i[0], smallerStyle)
            P2 = Paragraph(i[1], smallerStyle)
            P3 = Paragraph(i[2], smallerStyle)
            # Wenn ohne Fehlzeiten:
            if var == '2':
                P4 = Paragraph("", smallerStyle)
            else:
                P4 = Paragraph(i[3], smallerStyle)
            P5 = Paragraph(i[4], smallerStyle)

            my_data.append([P1,P2,P3,P4,P5])

        if i[5] == 1:
            P1 = Paragraph(i[0], grayStyle)
            P2 = Paragraph(i[1], grayStyle)
            P3 = Paragraph(i[2], grayStyle)
            P4 = Paragraph(i[3], grayStyle)
            P5 = Paragraph(i[4], grayStyle)

            my_data.append([P1,P2,P3,P4,P5])

    if path.exists("U:\\Kursbuch-Export") == False:
        system("mkdir U:\\Kursbuch-Export")

    filename = "U:\\Kursbuch-Export\\"+str(tn+"-"+str(datetime.now().date())+".pdf")

    doc = SimpleDocTemplate(filename, pagesize=A4, leftMargin=60,
                            rightMargin=20, topMargin=20, bottomMargin=20)
    story = []
    story.append(Paragraph('Kurs: '+krz+" "+k, styles['Normal']))
    t = Table(my_data, repeatRows=1)
    t._argW[0]=95
    t._argW[1]=160
    t._argW[2]=100
    t._argW[3]=120
    t._argW[4]=30
    t.hAlign = 'LEFT'
    t.spaceBefore =  10
    t.spaceAfter = 10
    t.setStyle(TableStyle(
        [('BOX', (0,0), (-1,-1), 0.5, colors.black),
        ('INNERGRID', (0,0), (-1,-1), 0.5, colors.black),
        ('VALIGN', (0,0), (-1,-1),'TOP'),
        ('BACKGROUND', (0,0), (4,0), colors.lightgrey),]))
    story.append(t)
    story.append(Paragraph('', styles['Normal']))
    doc.build(story)


    # system("start "+filename)
    subprocess.call("C:\\Program Files (x86)\\Google\\Chrome\\Application\\chrome.exe "+filename)
    # cmd = 'start C:\\"Program Files (x86)\\Google\\Chrome\\Application\\chrome.exe" '+filename
    # system(cmd)
    

if __name__ == "__main__":
    makeKursbuch("Tabellenname", "Kursname", "Kürzel", "1")