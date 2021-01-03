@echo off
rmdir build /s /q
rmdir dist /s
pyinstaller kursbuch.pyw
copy add-member.png dist\kursbuch\
copy add-members.png dist\kursbuch\
copy delete-member.png dist\kursbuch\
copy delete-members.png dist\kursbuch\
copy kursbuch.ico dist\kursbuch\
copy LICENSE dist\kursbuch\
cd dist
powershell Compress-Archive kursbuch\* kursbuch.zip