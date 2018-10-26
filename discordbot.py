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
        page_link = 'https://www.sodexo.fi/tty-tietotalo'
        page_response = requests.get(page_link, timeout=5)
        page_content = BeautifulSoup(page_response.content, "html.parser")
        food = page_content.findAll('div', attrs={"class": "lunch_desc inline"})

        food = re.findall(r'title">(.*?)</span>', str(food))
        hertsi = "Hertsi:\n"
        i = 0
        while i <= 8:
            hertsi += food[i]
            if i < 8:
                hertsi += "\n"
            i += 2

        # newton
        page_link = 'http://www.juvenes.fi/tabid/337/moduleid/1149/RSS.aspx'
        page_response = requests.get(page_link, timeout=5)
        page_content = BeautifulSoup(page_response.content, "html.parser")
        food = re.findall(r'</title><description>(.*?)</description><pubdate>', str(page_content))
        food = food[0]
        food = re.sub(' +', ' ', food)
        food = food[1:]
        wordList = re.sub("[^\w]", " ", food).split()
        unaccepted_words = ['Ravintola', 'Newton', 'Lounas', 'KELA', 'G', 'M', 'L', 'KA', 'VE', 'K', 'VS',
                            'PAPR', 'SOIJA', 'Tumma', 'riisi', 'SI', 'KAL', 'SITRUS', 'Päivittäin', 'vaihtuva',
                            'lämmin', 'kasvislisäke', 'Perunat', ]
        food_items = []
        for word in wordList[7:]:
            if word not in unaccepted_words:
                food_items.append(word)
        food = ""
        for word in food_items:
            food += word
            index = food_items.index(word)
            if index < (len(food_items) - 1):
                next = food_items[index + 1]
                if next != next.lower():
                    food += ","
            food += " "
        newton = "\nNewton:\n{:s}".format(food)
        await message.channel.send("```py\n{:s}\n{:s}```".format(hertsi, newton))

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