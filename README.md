# Discord+Stoat Bridge Bot

Made by: roxanne.wolf. (On Discord) / RoxanneWolf#6117 (On Stoat.chat)

Fork: @jmg_studios (discord) / @JMG#59804 (stoat)

## About:

This Discord+Stoat Bridge Bot source code allows you to connect your Discord and Stoat community together. This will allow your Discord and Stoat members to communicate with each other. This code is meant to be a simple and memory-efficient way to bridge your Discord and Stoat community.

This project will only work for 1 Discord and 1 Stoat server.

## Requirements:

- Python 3.10 or newer.
- Some basic knowledge of Python
- A Discord AND stoat.chat bot
- At least 512mb ram free and 512mb disk free.

## Setup:

Here is the steps needed to get started with using this source code.

1. Download/Fork this source code and upload it to your server
2. Create a Discord and Stoat bot.
- For Discord: Go to https://discord.com/developers/applications and create a new application. Under the bot section, enable the Message content intent so the bot can check the messages and send them to the set Stoat channel.
- For Stoat: Go to https://old.stoat.chat/settings/bots and create a new bot. Make sure to copy the token.
3. Open config.json and fill in everything it asks for:
```json
{
	"discordbottoken": "", #Put in your Discord bot token here
	"discordbotprefix": "!", #Put in the prefix for the Discord bot (not used)
	"stoatbottoken": "", #Put in your Stoat.chat bot token.
	"stoatbotprefix": "!", #Put in the prefix for the Stoat.chat bot.
	"discordchannelid": DISCORD_CHANNEL_ID_HERE, => Replace DISCORD_CHANNEL_ID_HERE with your Discord channel ID
	"discordwebhookurl": "", => Put in your Discord webhook url here.
	"stoatchannelid": "", => Put in the Stoat channel ID here (Make sure the Stoat.chat bot has the "Use Masquerade" permission.
}
```
4. Invite your Discord and Stoat bot to your servers
- For the Discord bot, make sure it has the Read Messages permission on the channel you are trying to bridge to your Stoat channel.
- For the Stoat bot, make sure the bot has the "View Channel", "Send Messages", "Send Embeds", and "Use Masquerade" permissions (check channel overrides as well)
5. Install everything from the requirements.txt file.
6. Run the main.py file. Assuming you did all steps correctly, your Discord+Stoat bridge bot should work.
| German (de)  | :x:                   | Google Translate                                   |

| Turkish (tr) | :x:                   | Google Translate                                   |
