import discord
import sys
from bs4 import BeautifulSoup
import requests
import re
import urllib.request
import urllib.parse

token = asd  # ent  er your token here
guild_number = asd  # enter your gild number here

client = discord.Client()

@client.event # event decorator/wrapper
async def on_ready():
    print(f"We have logged in as {client.user}")

@client.event
async def on_message(message):
    print(f"{message.channel}: {message.author}: {message.author.name}: {message.content}")

    guild = client.get_guild(guild_number)


    if "!members" == message.content:
        await message.channel.send(f"```py\n{guild.member_count}```")

    elif "!kick_gnomebot" in message.content:
        await client.close()
        sys.exit


    elif "!commands" == message.content:
        await message.channel.send(f"```py\n!MEMBERS: states the amount of users on the server\n"
                                   f"!KICK_GNOMEBOT: turns MrBigBot off\n"
                                   f"!UNISAFKA: prints today's menu @tty\n"
                                   f"!YOUTUBE (search): prints first Youtube search result\n"
                                   f"use all commands lowercase```")

    elif "!unisafka" == message.content:
        url = "https://unisafka.fi/tty/"

        # create a new Firefox session
        driver = webdriver.Chrome(r"C:\Program Files (x86)\Google\Chrome\Application\chromedrive.exe")
        driver.implicitly_wait(30)
        driver.get(url)

        python_button = driver.find_element_by_id('wrapper')  # FHSU
        python_button.click()  # click fhsu link

        soup_level1 = BeautifulSoup(driver.page_source, 'html.parser')
        menu_text = ""
        hertsi = re.findall(r'Hertsi(.*?)BLANK', str(soup_level1))
        hertsi_ruoka = re.findall(r'meal_part_name">(.*?)</div', str(hertsi))
        menu_text += "Hertsi\n"
        for food in hertsi_ruoka:
            menu_text += " "
            menu_text += food
            menu_text += "\n"

        menu_text += "\n"
        newton = re.findall(r'Newton(.*?)BLANK', str(soup_level1))
        newton_ruoka = re.findall(r'meal_part_name">(.*?)</div', str(newton))
        menu_text += "Newton\n"
        for food in newton_ruoka:
            menu_text += " "
            menu_text += food
            menu_text += "\n"
        menu_text += "\n"

        reaktori = re.findall(r'Reaktori(.*?)BLANK', str(soup_level1))
        reaktori_ruoka = re.findall(r'meal_part_name">(.*?)</div', str(reaktori))
        menu_text += "Reaktori\n"
        for food in reaktori_ruoka:
            menu_text += " "
            menu_text += food
            menu_text += "\n"

        await message.channel.send(menu_text)
        driver.quit()

    elif "!youtube" in message.content:
        command = message.content
        query = command[9:]
        query = re.sub("\s+", "+", query.strip())
        url = "https://www.youtube.com/results?search_query={:s}".format(query)
        headers = {}
        headers[
            "User-Agent"] = "Mozilla/5.0 (X11; Linux i686) AppleWebKit/537.17 (KHTML, like Gecko) Chrome/24.0.1312.27 Safari/537.17"
        req = urllib.request.Request(url, headers=headers)
        resp = urllib.request.urlopen(req)
        respData = resp.read()
        link = re.findall(r'<a href="/watch(.*?)"', str(respData))
        link = link[0]
        link = "https://www.youtube.com/watch{:s}".format(link)
        await message.channel.send(link)


client.run(token)