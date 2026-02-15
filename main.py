import discord
import stoat
from stoat.ext import commands
import json
import asyncio
from discord import SyncWebhook
import os

with open('config.json') as f:
    config = json.load(f)

DISCORDBOTTOKEN = config.get('discordbottoken')
DISCORDBOTPREFIX = config.get('discordbotprefix')
REVOLTBOTTOKEN = config.get('stoatbottoken')
REVOLTBOTPREFIX = config.get('stoatbotprefix')
DISCORDCHANNELID = config.get('discordchannelid')
DISCORDWEBHOOKURL = config.get('discordwebhookurl')
REVOLTCHANNELID = config.get('stoatchannelid')

stoatclient = commands.Bot(token=REVOLTBOTTOKEN, command_prefix=REVOLTBOTPREFIX)

@stoatclient.on(stoat.MessageCreateEvent)
async def on_message(event: stoat.MessageCreateEvent):
    message = event.message
    if message.author_id == stoatclient.state.my_id:
        return
    if message.channel.id == REVOLTCHANNELID:
        webhook = SyncWebhook.from_url(DISCORDWEBHOOKURL)
        webhook.send(
            f"{message.content}",
            username=f"{message.author.name}",
            avatar_url=f"{message.author.internal_avatar.attach_state(message.author.state, 'avatars').url()}",
            allowed_mentions=discord.AllowedMentions(everyone=False)
        )

@stoatclient.command()
async def help(ctx):
    embed = stoat.SendableEmbed(
        title=f"{stoatclient.user.name}",
        description=(
            f"{REVOLTBOTPREFIX}help - Shows this help message\n"
            f"{REVOLTBOTPREFIX}ping - Pong!\n"
            f"{REVOLTBOTPREFIX}botinfo - Info about the bot\n"
            f"{REVOLTBOTPREFIX}debug - Debug information\n"
            f"{REVOLTBOTPREFIX}say\n"
            f"{REVOLTBOTPREFIX}presence\n"
            f"{REVOLTBOTPREFIX}status\n"
            f"{REVOLTBOTPREFIX}statusreset"
        )
    )
    await ctx.channel.send(embeds=[embed])

@stoatclient.command()
async def ping(ctx):
    await ctx.channel.send("Pong!")

@stoatclient.command()
async def botinfo(ctx):
    embed = stoat.SendableEmbed(
        title=f"{stoatclient.user.name} Information",
        description=(
            f"Made by: RoxanneWolf#6117\n"
            f"GitLab: https://gitlab.com/roxannewolf/discordrevoltbridgebot\n"
            f"Codeberg: https://codeberg.org/roxannewolf/DiscordRevoltBridgeBot"
        )
    )
    await ctx.channel.send(embeds=[embed])

@stoatclient.command()
async def debug(ctx, debugoption=""):
    if debugoption == "config":
        try:
            embed = stoat.SendableEmbed(
                title=f"{stoatclient.user.name} Debug",
                description=(
                    f"Discord Channel: {DISCORDCHANNELID}\n"
                    f"Revolt Channel: {REVOLTCHANNELID}\n"
                    f"Discord Prefix: {DISCORDBOTPREFIX}\n"
                    f"Revolt Prefix: {REVOLTBOTPREFIX}"
                )
            )
            await ctx.channel.send(embeds=[embed])
        except:
            await ctx.channel.send("An error occurred.")
    elif debugoption == "troubleshoot":
        embed = stoat.SendableEmbed(title=f"{stoatclient.user.name} Debug", description="Troubleshoot info here.")
        await ctx.channel.send(embeds=[embed])
    elif debugoption == "bot":
        embed = stoat.SendableEmbed(
            title=f"{stoatclient.user.name} Debug",
            description=f"Bot ID: {stoatclient.state.my_id}\nUsers: {len(stoatclient.users)}"
        )
        await ctx.channel.send(embeds=[embed])
    elif debugoption == "server":
        embed = stoat.SendableEmbed(
            title=f"{stoatclient.user.name} Debug",
            description=(
                f"Server Name: {ctx.server.name}\n"
                f"Server ID: {ctx.server.id}\n"
                f"Owner ID: {ctx.server.owner_id}\n"
                f"Discoverable: {ctx.server.discoverable}"
            )
        )
        await ctx.channel.send(embeds=[embed])

@stoatclient.command()
@commands.is_owner()
async def say(ctx, *, message: str):
    await ctx.channel.send(message)

@stoatclient.command()
@commands.is_owner()
async def presence(ctx, presencetype=""):
    presence_map = {
        "online": stoat.Presence.online,
        "idle": stoat.Presence.idle,
        "focus": stoat.Presence.focus,
        "dnd": stoat.Presence.busy,
        "invisible": stoat.Presence.invisible,
    }
    if presencetype in presence_map:
        await stoatclient.http.edit_my_user(status=stoat.UserStatusEdit(presence=presence_map[presencetype]))
        await ctx.channel.send("Bot presence has been changed.")
    else:
        await ctx.channel.send("Invalid presence type. Use: online, idle, focus, dnd, invisible")

@stoatclient.command()
@commands.is_owner()
async def status(ctx, *, statustext):
    await stoatclient.http.edit_my_user(status=stoat.UserStatusEdit(text=f"{statustext}"))
    await ctx.channel.send("Bot status has been changed.")

@stoatclient.command()
@commands.is_owner()
async def statusreset(ctx):
    await stoatclient.http.edit_my_user(status=stoat.UserStatusEdit(text=None))
    await ctx.channel.send("Bot status has been reset.")


class DiscordBot(discord.Client):
    def __init__(self):
        intents = discord.Intents.default()
        intents.message_content = True
        super().__init__(intents=intents)

    async def on_message(self, message):
        if message.author == self.user:
            return
        if message.webhook_id:
            return
        if message.channel.id == int(DISCORDCHANNELID):
            await stoatclient.http.send_message(
                REVOLTCHANNELID,
                f"{message.content}",
                masquerade=stoat.MessageMasquerade(name=f"{message.author.name}", avatar=f"{message.author.avatar}")
            )


if __name__ == "__main__":
    async def main():
        discordclient = DiscordBot()
        await asyncio.gather(
            discordclient.start(DISCORDBOTTOKEN),
            stoatclient.start(),
        )

    asyncio.run(main())
