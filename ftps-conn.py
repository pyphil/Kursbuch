from ftplib import FTP_TLS
import ssl

class FTPS_conn:
    def __init__(self, url, krzl, pw):
        self.url = url
        self.krzl = krzl
        self.pw = pw

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
            print("Servername falsch")
        elif ftp == "loginerr":
            print("Login falsch")
        else:
            # Datei herunterladen
            with open ('kurs.db','wb') as localfile:
                ftp.retrbinary('RETR kurs.db', localfile.write)
            ftp.close()

    def upload_kursdb(self):
        ftp = self.connect()
        if ftp == "hosterr":
            print("Servername falsch")
        elif ftp == "loginerr":
            print("Login falsch")
        else:    
            # Datei hochladen rb -> read binary
            with open ('kurs.db','rb') as fp:
                ftp.storbinary('STOR kurs.db', fp)
            ftp.close()

    def upload_timestamp(self):
        pass

if __name__ == "__main__":
    conn = FTPS_conn("url","krz","pw")
    conn.download_kursdb()