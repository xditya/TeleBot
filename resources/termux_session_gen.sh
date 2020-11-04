# Termux session string generator for TeleBot
echo Termux Session Genenrator - TeleBot
#!/bin/bash
echo Starting dependency installation in 5 seconds...
sleep 5
apt-get update
apt-get upgrade -y
pkg upgrade -y
pkg install python wget -y
wget https://raw.githubusercontent.com/xditya/TeleBot/master/telesetup.py
pip install telethon
python telesetup.py
