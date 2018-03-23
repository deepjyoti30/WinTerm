@echo off
cls
echo Generating exe file....
pyinstaller -F -i Terminal.ico Terminal.py
echo File generated. Should be in dist\
pause