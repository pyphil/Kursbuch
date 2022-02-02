@echo off
rmdir build /s /q
rmdir dist /s

python.exe -OO -m PyInstaller ^
    --windowed ^
    --icon kursbuch.ico ^
    --exclude-module=tkinter ^
    --exclude-module=tk ^
    --exclude-module=FixTk ^
    --exclude-module=_tkinter ^
    --exclude-module=Tkinter ^
    --exclude-module=tcl ^
    --add-data add-member.png;. ^
    --add-data add-members.png;. ^
    --add-data delete-member.png;. ^
    --add-data delete-members.png;. ^
    --add-data delcourse.png;. ^
    --add-data delstunde.png;. ^
    --add-data kursmitglieder.png;. ^
    --add-data neuestunde.png;. ^
    --add-data new_course.png;. ^
    --add-data pdf.png;. ^
    --add-data tutor.png;. ^
    --add-data kursbuch.ico;. ^
    --add-data LICENSE;. ^
    --add-data ferien.db;. ^
    kursbuch.py

cd dist
powershell sleep 10
powershell Compress-Archive kursbuch\* kursbuch1.3.3.zip