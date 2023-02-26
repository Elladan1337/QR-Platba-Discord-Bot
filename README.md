# QR-Platba-Discord-Bot
A simple Discord Bot that detects messages which contain payment information and creates a handy QR code based on Czech Central bank standards to enable payment.

## bot.py
The Discord bot itself.
Use !qrcreate to have the bot look at the last ten messages for a bank account no. and create the QR code.
Use !qrcreate <amount> to have it create a QR code for the specified amount. 
## apitest.py
A useful test call to the QR image creator API written in Python.
