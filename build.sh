rm -r build
rm -r dist

python3 -OO -m PyInstaller \
    --windowed \
    --icon kursbuch.ico \
    --exclude-module=tkinter \
    --exclude-module=tk \
    --exclude-module=FixTk \
    --exclude-module=_tkinter \
    --exclude-module=Tkinter \
    --exclude-module=tcl \
    --add-data add-member.png:. \
    --add-data add-members.png:. \
    --add-data delete-member.png:. \
    --add-data delete-members.png:. \
    --add-data kursbuch.ico:. \
    --add-data LICENSE:. \
    --add-data ferien.db:. \
    kursbuch.py