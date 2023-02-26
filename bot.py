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
async def qrcreate(ctx, money = "0.00"):
    #messages = [message async for message in ctx.channel.history(limit=10)]# gets the last 10 messages in the channel
    messages = []
    try:
        money = float(money)
    except ValueError:
        money = float(0)
    
    if money < 0 or money > 1000000:
        money = float(0)
    else: 
        money = round(float(money), 2)

    async for message in ctx.channel.history(limit=10):
        if message.author != client.user:
            messages.append(message)
    
    bank_pattern = re.compile(r'((?<=\D)|(?<=\b))\d{2,6}-?\d{2,10}\/\d{4}((?=\D)|(?=\b))', re.IGNORECASE) # example regex pattern
    #crown_pattern = re.compile(r'\d+(?=\skč)|(?<=czk\s)\d+', re.IGNORECASE)
    bank_account = ''
    for msg in messages:
        if re.search(bank_pattern, msg.content):
            bank_account = re.search(bank_pattern, msg.content).group()
            #if re.search(crown_pattern, msg.content):
                #money = int(re.search(crown_pattern, msg.content).group())
            #else:
                #money = 0
            break
    if len(bank_account) > 0:
        answer = 'QR code created with the following account number: ' + bank_account + '\nAmount: ' + str(money) + ' Kč.' 
    else:
        await ctx.send('No matches found.')
        return()

    print(messages)

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
        'amount': money,
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
        await ctx.send(answer)
        await ctx.send(file = discord.File(fp = open('img.png', 'rb')))
    else:
        await ctx.send("Invalid bank account number detected. Mission aborted.")
    
client.run(TOKEN)



### !qrcreate command
### Looks at last ten messages
### Does a Regex-check for the bank account number
### Does a Regex-check for the payment number
### Submits this to the SPAYD API https://qr-platba.cz/pro-vyvojare/restful-api/
### Receive .png file
### Post .png file into chat.