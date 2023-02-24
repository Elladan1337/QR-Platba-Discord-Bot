# bot.py
import os
import re
import discord
from dotenv import load_dotenv
from discord.ext.commands import Bot
from discord.ext import commands

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')

intents = discord.Intents.default()
intents.message_content = True
client = commands.Bot(command_prefix = "!", intents = intents)

@client.event
async def on_ready():
    print(f'{client.user} has connected to Discord!')

@client.command()
async def qrcreate(ctx):
        messages = [message async for message in ctx.channel.history(limit=10)]# gets the last 10 messages in the channel
        pattern = re.compile(r'[A-Z]', re.IGNORECASE) # example regex pattern
        matches = []
        for msg in messages:
            if pattern.search(msg.content):
                matches.append(msg.content)
        if len(matches) > 0:
            response = 'QR code created with the following messages:\n' + '\n'.join(matches)
        else:
            response = 'No matches found.'
        await ctx.send(response)

client.run(TOKEN)



### !qrcreate command
### Looks at last ten messages
### Does a Regex-check for the bank account number
### Does a Regex-check for the payment number
### Submits this to the SPAYD API https://qr-platba.cz/pro-vyvojare/restful-api/
### Receive .png file
### Post .png file into chat.