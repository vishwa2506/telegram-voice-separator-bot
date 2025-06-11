# Telegram Voice Separator Bot

Send an MP3 file to this bot and it will separate the voice and background music using Spleeter.

## login vps(example azure vps CLI)
ssh youruser@your_azure_vps_ip


## Setup
##repo clone
sudo apt update
sudo apt install git -y
git clone https://github.com/yourusername/telegram-voice-separator-bot.git
cd telegram-voice-separator-bot

##Python3, pip, ffmpeg install
sudo apt install python3 python3-pip ffmpeg -y


1. Install dependencies: `pip install -r requirements.txt` 1a
   1a. Install dependencies if before not run: `pip install --user -r requirements.txt`
                                               or `pip3 install --user -r requirements.txt`

3. Set environment variable: `export BOT_TOKEN="your_telegram_bot_token"`
4. Run the bot: `python3 bot.py`
