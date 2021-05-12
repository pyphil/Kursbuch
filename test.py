from urllib.request import urlopen

content = urlopen('https://raw.githubusercontent.com/pyphil/Kursbuch/main/version')

version = str(content.read())
version = version.split("'")[1].split("\\")[0]

current_version = "1.2.0"

if current_version == version:
    print("pyKursbuch ist aktuell.")
else:
    print("Eine neue Version ist verfügbar: https://github.com/pyphil/Kursbuch/releases/tag/v"+version)