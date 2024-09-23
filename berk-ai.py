# son raporlar :
#
# 
#
#
#

from tqdm import tqdm

print("İmporting libs...")
for i in tqdm(range(10)):
    from collections import defaultdict
    import difflib
    import threading
    import json
    import random
    import time
    import colorama
    import discord
    from database.database import discord_api_token, argo, user
    from colorama import Fore
    from discord.ext import commands
    from difflib import get_close_matches
    import sys
    from datetime import datetime
    import psutil
    import platform

print("\n"*1)

#### !!!!!!!!
for i in tqdm(range(10)):
    trainingMode = True
    systemLock = False

print("\n"*1)

def get_cpu_model():
    with open("/proc/cpuinfo") as f:
        for line in f:
            if "model name" in line:
                return line.split(":")[1].strip()

for i in tqdm(range(10)):
    server_cpu = get_cpu_model()
    ram_info = psutil.virtual_memory()
    server_ram = psutil.virtual_memory().total / (1024 ** 3)

print("\n"*1)


for i in tqdm(range(10)):
    ai_mode = False

    intents = discord.Intents.default()
    intents.message_content = True

    colorama.init(autoreset=True)
    log = False
    temp = " "
    number = 0
    vip = False

    with open('aidatabase.json', 'r', encoding='utf-8') as f:
        aidatabase = json.load(f)
    keys = list(aidatabase.keys())

print("\n"*1)

def save_json(filename, data):
    with open(filename, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=4)


def load_json(filename):
    with open(filename, 'r', encoding='utf-8') as f:
        return json.load(f)


def add_or_update_entry(filename, key, value):
    data = load_json(filename)
    data[key] = value
    save_json(filename, data)


def moderator(inputt, argo, ex=0.7):
    for word in argo:
        diff = difflib.SequenceMatcher(None, inputt, word).ratio()
        if diff >= ex:
            return True



recent_messages = defaultdict(list)


class MyClient(discord.Client):
    async def on_ready(self):
        print(f'Logged on as {self.user}!')
        await client.change_presence(activity=discord.Activity(type=discord.ActivityType.watching, name="Porno"))

    async def on_message(self, message):
        global ai_mode
        global log
        global temp
        global vip
        global number
        global trainingMode

        if message.author == self.user:
            return
        

        # Moderation
        # Bad Words

        i = 0
        while len(message.content.split()) > i:
            if moderator(message.content.split()[i].lower(),argo):
                await message.channel.send(f"UYARI : {message.author} lütfen argo kullanma !")
                pass
            

            i = i + 1

        # Spam Moderation

        user_id = message.author.id
        content = message.content.strip().lower()

        recent_messages[user_id].append(content)
        
        if len(recent_messages[user_id]) > 5:
            recent_messages[user_id].pop(0)

        if len(recent_messages[user_id]) == 5 and all(msg == content for msg in recent_messages[user_id]):
            await message.channel.send(f"{message.author.mention}, lütfen aynı mesajı spam yapma!")
            recent_messages[user_id] = []


        print(f"{message.channel}")
        print(f'{Fore.CYAN}Message from {message.author}: {message.content}')
        if any(role.id == int(user) for role in message.author.roles):
            if message.content.startswith("!aimode"):
                if message.content.split()[1] == "True":
                    await message.channel.send("AiMode başarıyla etkinleştirildi !")
                    ai_mode = True
                elif message.content.split()[1] == "False":
                    await message.channel.send("AiMode kapatıldı tezgahın önünü kapatmayın !")
                    ai_mode = False
                else:
                    await message.channel.send(
                        "Yanlış kullanım ! Doğru kullanımı --help ```komutu``` ile öğrenebilirsiniz")
            elif message.content.startswith("!trainingMode"):
                if message.content.split()[1] == "True":
                    await message.channel.send("Eğitim modu etkinleştirildi !")
                    trainingMode = True
                elif message.content.split()[1] == "False":
                    await message.channel.send("Eğitim modu kapatıldı !")
                    trainingMode = False
                else:
                    await message.channel.send(
                        "Yanlış kullanım ! Doğru kullanımı --help ```komutu``` ile öğrenebilirsiniz")
            elif message.content.startswith("!hello"):
                parts = message.content.split()
                if len(parts) == 2:
                    await message.channel.send(f"OOO {parts[1]} Hoşgeldin")
                else:
                    await message.channel.send("Yanlış bir kullanım, doğru kullanıma --help komutu ile ulaşabilirsiniz")
            elif message.content.startswith("!clear"):
                parts = message.content.split()
                if len(parts) == 2:
                    try:
                        number = int(parts[1])
                        if number > 0:
                            deleted = await message.channel.purge(limit=number)
                            await message.channel.send(f'{len(deleted)} mesaj silindi.')
                        else:
                            await message.channel.send("Lütfen pozitif bir sayı giriniz.")
                    except ValueError:
                        await message.channel.send("Geçersiz sayı formatı.")

                    await message.channel.send("Kullanım: !clear sayı")

            elif message.content.startswith("!off"):
                await message.channel.send("Berk-ai Kapatılıyor! Sonra görüşmek üzere")
                sys.exit()
            elif message.content.startswith("!cpu"):
                if message.content.split()[1] == "ping":
                    await message.channel.send("Test başladı: CPu için bir adet ek paket gönderiliyor")

            elif message.content.startswith("!spam"):
                parts = message.content.split()
                if len(parts) == 3:
                    user = parts[1]
                    try:
                        count = int(parts[2])
                        if count > 0:
                            for _ in range(count):
                                await message.channel.send(user)
                        else:
                            await message.channel.send("Lütfen pozitif bir sayı giriniz.")
                    except ValueError:
                        await message.channel.send("Geçersiz sayı formatı.")
                else:
                    await message.channel.send("Kullanım: !spam @user sayı")
            elif message.content == "!serverinfo":
                ram_info = psutil.virtual_memory()
                used_ram = ram_info.used / (1024 ** 3)
                cpu_usage = psutil.cpu_percent(interval=1)

                await message.channel.send(f"RAM {used_ram:.2f}/{server_ram:.2f}")
                await message.channel.send(f"CPU {server_cpu} (usage:{cpu_usage}%)")
            elif message.content == "!ban":
                await message.channel.send("")
            elif message.content == "sa":
                await message.channel.send("as")
            elif message.content == "--help" or message.content == "!help":
                await message.channel.send("```!randommeme  -argüman almaz                   =>  random meme üretir```")
                await message.channel.send("```!randomnude  -argüman almaz                   =>  random nude üretir```")
                await message.channel.send(
                    "```!argo        -argüman almaz                   =>  random küfür üretir```")
                await message.channel.send("```!spam        (kullanıcı) (sayı)               =>  kullanıcıyı zorlar```")
                await message.channel.send(
                    "```!hello       (kullanıcı)                      =>  sıcak bir karşılama ```")
                await message.channel.send(
                    "```!load        (link)                           =>  veri tabanını günceller```")
                await message.channel.send("```!clear       (sayı)                           =>  sohbeti temizler```")
                await message.channel.send("```!aimode      (durum(True/False))              =>  Ai modunu ayarlar```")
                await message.channel.send("```!cpu         (işlem)     (bilinmeyen)         =>  CPU işlemleri için```")
            elif log == True:
                add_or_update_entry('aidatabase.json', temp, message.content)
                await message.channel.send(f"Yeni anahtar-değer çifti eklendi: {temp} -> {message.content}")
                log = False
            else:  # komut değil
                if ai_mode == True:
                    if trainingMode==True:
                        cutoff = 0.80
                    elif trainingMode==False:
                        cutoff = 0.55
                    matches = get_close_matches(message.content.lower(), keys, n=1, cutoff=cutoff) # defould 0.55
                    if matches:
                        closest_match = matches[0]
                        reply = aidatabase[closest_match]
                        if ai_mode == True:

                            if reply == "cevap":
                                await message.channel.send(f"Saat Şuan {datetime.now().strftime("%H:%M:%S")}")
                            elif reply == "exit":
                                await message.channel.send("Berk-ai kapatılıldı! Yaşamak güzeldi..")
                                sys.exit()
                            else:
                                await message.channel.send(reply)
                        elif ai_mode == False:
                            await message.channel.send("Bu özellik kullanım dışı")
                    else:
                        if ai_mode == True:
                            await message.channel.send("Bu cümleyi anlayamadım🤔")
                            await message.channel.send(
                                "Lütfen gelişmeme katkıda bulunmak için bu cümleye karşı ne cevap vermem gerektiğini söyle :")
                        elif ai_mode == False:
                            await message.channel.send("Bu özellik kullanım dışı")
                        temp = message.content
                        log = True


intents = discord.Intents.default()
intents.message_content = True

client = MyClient(intents=intents)
client.run(discord_api_token)