# bot.py
import os
import re
import discord
import requests
from dotenv import load_dotenv
from discord.ext.commands import Bot
from discord.ext import commands
from datetime import date

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
    bank_pattern = re.compile(r'\b\d{2,6}-?\d{2,10}\/\d{4}\b', re.IGNORECASE) # example regex pattern
    bank_account = ''
    for msg in messages:
        if re.search(bank_pattern, msg.content):
            bank_account = re.search(bank_pattern, msg.content).group()
            break
    if len(bank_account) > 0:
        answer = 'QR code created with the following account number:\n' + bank_account
    else:
        answer = 'No matches found.'

    if re.search(r'\d{2,6}-', bank_account):
        prefix = re.search(r'\d{2,6}(?=-)', bank_account).group()
    else:
        prefix = None

    number = re.search(r'\d+(?=\/)', bank_account).group()

    bank = re.search(r'(?<=\/)\d{4}', bank_account).group()
    
    url = "http://api.paylibo.com/paylibo/generator/czech/image"
    params = {
        'accountPrefix': prefix,
        'accountNumber': number,
        'bankCode': bank,
        'amount': 0,
        'currency':'CZK',
        'vs':'',
        'ks':'',
        'ss':'',
        'identifier':'',
        'date':str(date.today()),
        'message':'generic message',
        'compress':False,
        'branding':False,
        'size':200
}
    print(params)
    response = requests.get(url = url, params = params, stream=True)
    print(response.status_code)
    if response.status_code == 200:
        with open('img.png', 'wb') as out_file:
            out_file.write(response.content)
    print(response.raw)
    await ctx.send(answer)
    await ctx.send(file = discord.File(fp = open('img.png', 'rb')))
client.run(TOKEN)



### !qrcreate command
### Looks at last ten messages
### Does a Regex-check for the bank account number
### Does a Regex-check for the payment number
### Submits this to the SPAYD API https://qr-platba.cz/pro-vyvojare/restful-api/
### Receive .png file
### Post .png file into chat.