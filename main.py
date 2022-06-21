from datetime import datetime
import sys
import discord
from discord.ext import commands
from random import randint
from dotenv import load_dotenv
from os import getenv
import os

# Gets bot token
load_dotenv()
token = os.getenv("TOKEN")

# Pre setup for bot
intents = discord.Intents.default()
owners = [499816773122654219]

# Sets up bot
description = """A bot developed by SoulWarden for the IFF"""
activity = discord.Activity(type=discord.ActivityType.watching, name="me start up")
bot = commands.Bot(
    command_prefix=commands.when_mentioned_or('_'),
    description=description,
    intents=intents,
    activity=activity,
    status=discord.Status.online,
    owner_ids=set(owners),
    help_command=None,
    strip_after_prefix = True,
)

# Loading cogs
bot.cogList = ["musicCog","randomCog","backgroundCog"]
for cog in bot.cogList:
    bot.load_extension(cog)
    
# Bot starting
@bot.event
async def on_ready():
    now = datetime.now()
    current_time = now.strftime("%H:%M:%S")
    
    # Printing status messages
    print("Logged in as")
    print(bot.user.name)
    print(bot.user.id)
    print(f"Started at {current_time}")
    
    # Sets prefix
    if sys.platform.startswith('win32'):
        bot.command_prefix = commands.when_mentioned_or('+')
        print(f"Prefix is +")
    elif sys.platform.startswith('linux'):
        bot.command_prefix = commands.when_mentioned_or("\\")
        print(f"Prefix is \\")

@bot.event
async def on_command_error(ctx, error):
    if isinstance(error, commands.CommandOnCooldown):
        await ctx.reply(f"Slow down! {round(error.retry_after, 2)} seconds left on cooldown")
    else:
        print(error)

# Reload cogs command
@bot.command()
@commands.is_owner()
async def reload(ctx, extension: str = None):
    count = 1
    # Checks if a cog was inputted
    if extension is None:
        # If no cog was inputted, create a reload embed
        embed = discord.Embed(
            title="Reload", description="Reloaded cogs: ", color=0xFF00C8
        )
        # Interate through all cogs and reload them
        for x in bot.cogList:
            bot.reload_extension(x)
            embed.add_field(name=f"**#{count}**", value=f"{x} reloaded", inline=False)
            count += 1
        # Send embed
        await ctx.send(embed=embed)
    else:
        # If a cog was inputted, reloads that cog
        bot.reload_extension(f"{extension}")
        embed = discord.Embed(
            title="Reload",
            description=f"{extension} successfully reloaded",
            color=0xFF00C8,
        )
        await ctx.send(embed=embed)


# Unload cogs command
@bot.command()
@commands.is_owner()
async def unload(ctx, extension: str = None):
    count = 1
    if extension is None:
        embed = discord.Embed(
            title="Unload", description="Unloaded cogs", color=0x109319
        )
        for x in bot.cogList:
            try:
                bot.unload_extension(x)
            except commands.ExtensionNotLoaded:
                embed.add_field(
                    name=f"**#{count}**", value=f"{x} is already unloaded", inline=False
                )
                count += 1
            else:
                embed.add_field(
                    name=f"**#{count}**", value=f"{x} unloaded", inline=False
                )
                count += 1
        await ctx.send(embed=embed)
    else:
        bot.unload_extension(extension)
        embed = discord.Embed(
            title="Unload", description=f"{extension} cog unloaded", color=0x109319
        )
        await ctx.reply(embed=embed)


# Load cogs command
@bot.command()
@commands.is_owner()
async def load(ctx, extension: str = None):
    count = 1
    if extension is None:
        embed = discord.Embed(title="Load", description="Loaded cogs", color=0x109319)
        for x in bot.cogList:
            try:
                bot.load_extension(x)
            except commands.ExtensionAlreadyLoaded:
                embed.add_field(
                    name=f"**#{count}**", value=f"{x} is already loaded", inline=False
                )
                count += 1
            else:
                embed.add_field(name=f"**#{count}**", value=f"{x} loaded", inline=False)
                count += 1
        await ctx.send(embed=embed)
    else:
        bot.load_extension(extension)
        embed = discord.Embed(
            title="Load", description=f"{extension} cog loaded", color=0x109319
        )
        await ctx.reply(embed=embed) 
        
bot.run(token)
