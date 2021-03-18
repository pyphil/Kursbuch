@echo off
rmdir build /s /q
rmdir dist /s
pyinstaller --icon kursbuch.ico --noconsole kursbuch.py
rem pyinstaller --icon kursbuch.ico kursbuch.py
copy add-member.png dist\kursbuch\
copy add-members.png dist\kursbuch\
copy delete-member.png dist\kursbuch\
copy delete-members.png dist\kursbuch\
copy kursbuch.ico dist\kursbuch\
copy LICENSE dist\kursbuch\
copy ferien.db dist\kursbuch\
xcopy /E .\curl\ .\dist\kursbuch\curl\
cd dist
rem powershell Compress-Archive kursbuch\* kursbuch.zip