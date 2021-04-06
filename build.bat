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
    kursbuch.py
copy add-member.png dist\kursbuch\
copy add-members.png dist\kursbuch\
copy delete-member.png dist\kursbuch\
copy delete-members.png dist\kursbuch\
copy kursbuch.ico dist\kursbuch\
copy LICENSE dist\kursbuch\
copy ferien.db dist\kursbuch\
rem xcopy /E .\curl\ .\dist\kursbuch\curl\
rem cd dist
rem powershell Compress-Archive kursbuch\* kursbuch.zip