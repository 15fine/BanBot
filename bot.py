import os

import discord
from discord.ext import commands
from discord.ext.commands import has_permissions
from discord.utils import get
from discord import DMChannel

from dotenv import load_dotenv

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')

bot = commands.Bot(command_prefix='!')

@bot.event
async def on_ready():
    print("Bot is online!")

@bot.event
async def on_member_join(member: discord.Member):
    print(f"{member.id} has joined {member.guild.id}")
    with open("banned.txt") as banlist:
        print("opened")
        entry = banlist.readlines()
        for line in entry:
            ids = line.split()
            if int(ids[0]) == member.guild.id:
                if int(ids[1]) == member.id:
                    print("True")
                    BanRole = discord.utils.get(member.guild.roles,name="Banned")
                    await member.add_roles(BanRole)

@bot.command(name="config", help="Configure the ban appeal channel for this server")
@has_permissions(administrator=True)
async def configure(ctx, channel: discord.TextChannel=None):
    if channel is None:
        await ctx.channel.send("Failed to configure the ticket as an argument was not given or was invalid. Usage: `!config <channelid>`")
    else:
        with open("channels.txt", "a") as chnllist:
            chnllist.write(f"{ctx.guild.id} {channel.id}\n")
            await ctx.guild.create_role(name="Banned")
            print(ctx.guild.text_channels)
            for achannel in ctx.guild.text_channels:
                if achannel.id != channel.id:
                    await achannel.set_permissions(discord.utils.get(ctx.guild.roles,name="Banned"), read_messages=False, send_messages=False)
            for achannel in ctx.guild.voice_channels:
                await achannel.set_permissions(discord.utils.get(ctx.guild.roles,name="Banned"), view_channel=False)
            await ctx.channel.send("Configured!")

@bot.command(name="ban", help="Ban a user")
@has_permissions(ban_members=True)
async def ban(ctx, member: discord.Member, reason="None given"):
    await member.edit(roles=[])
    await member.add_roles(discord.utils.get(ctx.guild.roles,name="Banned"))
    with open("banned.txt", "a") as banlist:
        banlist.write(f"{ctx.guild.id} {member.id}\n")
    await DMChannel.send(member, f"You have been banned from {ctx.guild.name} for reason: {reason}. You may appeal in the appeal channel.")
    

bot.run(TOKEN)