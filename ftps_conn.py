from ftplib import FTP_TLS
import ssl

class FTPS_conn:
    def __init__(self, url, krzl, pw, dbpath):
        self.url = url
        self.krzl = krzl
        self.pw = pw
        self.dbpath = dbpath

    def connect(self):
        ftp = FTP_TLS()
        # using TLS version 1.2
        # ftp.ssl_version = ssl.PROTOCOL_TLSv1_2
        # ftp.debugging = 2
        try:
            ftp.connect(self.url, 21)
        except:
            return "hosterr"
        else:
            try:
                ftp.login(self.krzl, self.pw)
            except:
                return "loginerr"
            else:
                ftp.prot_p()
                return ftp

    def download_kursdb(self):
        ftp = self.connect()
        if ftp == "hosterr":
            return "hosterr"
        elif ftp == "loginerr":
            return "loginerr"
        else:
            # Datei herunterladen
            with open (self.dbpath+'kurs.db','wb') as localfile:
                ftp.retrbinary('RETR kurs.db', localfile.write)
            ftp.close()

    def upload_kursdb(self):
        ftp = self.connect()
        if ftp == "hosterr":
            return "hosterr"
        elif ftp == "loginerr":
            return "loginerr"
        else:    
            # Datei hochladen rb -> read binary
            with open (self.dbpath+'kurs.db','rb') as fp:
                ftp.storbinary('STOR kurs.db', fp)
            ftp.close()

    def delete_kursdb(self):
        ftp = self.connect()
        if ftp == "hosterr":
            return "hosterr"
        elif ftp == "loginerr":
            return "loginerr"
        else:    
            # Datei löschen
            ftp.delete('kurs.db')
            ftp.close()
            
    def download_timestamp(self):
        ftp = self.connect()
        if ftp == "hosterr":
            return "hosterr"
        elif ftp == "loginerr":
            return "loginerr"
        else:
            # Datei herunterladen
            with open (self.dbpath+'timestamp','wb') as localfile:
                ftp.retrbinary('RETR timestamp', localfile.write)
            ftp.close()

    def upload_timestamp(self):
        ftp = self.connect()
        if ftp == "hosterr":
            return "hosterr"
        elif ftp == "loginerr":
            return "loginerr"
        else:    
            # Datei hochladen rb -> read binary
            with open (self.dbpath+'timestamp','rb') as fp:
                ftp.storbinary('STOR timestamp', fp)
            ftp.close()

if __name__ == "__main__":
    conn = FTPS_conn("url","krz","pw","dbpath")
    conn.download_kursdb()