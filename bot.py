# bot.py
import os

import discord
from dotenv import load_dotenv
from discord.ext.commands import Bot
from discord.ext import commands

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')

intents = discord.Intents.default()
client = commands.Bot(command_prefix = "!", intents = intents)

@client.event
async def on_ready():
    print(f'{client.user} has connected to Discord!')

client.run(TOKEN



### !qrcreate command
### Looks at last ten messages
### Does a Regex-check for the bank account number
### Does a Regex-check for the payment number
### Submits this to the SPAYD API https://qr-platba.cz/pro-vyvojare/restful-api/
### Receive .png file
### Post .png file into chat.