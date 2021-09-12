@echo off
rmdir build /s /q
rmdir dist /s
rem pyinstaller --icon kursbuch.ico -w kursbuch.py
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
rem copy add-member.png dist\kursbuch\
rem copy add-members.png dist\kursbuch\
rem copy delete-member.png dist\kursbuch\
rem copy delete-members.png dist\kursbuch\
rem copy kursbuch.ico dist\kursbuch\
rem copy LICENSE dist\kursbuch\
rem copy ferien.db dist\kursbuch\
rem xcopy /E .\curl\ .\dist\kursbuch\curl\
cd dist
powershell Compress-Archive kursbuch\* kursbuch.zip