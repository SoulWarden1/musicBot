import discord
from discord.ext import commands
from random import randint
from datetime import datetime
import asyncio

class musicCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        
    @commands.cooldown(1, 5, commands.BucketType.guild)
    @commands.guild_only()
    @commands.command(aliases=["Join"])
    async def join(self, ctx, *, channel: discord.VoiceChannel = None):
        try: # Attempts to find the authors vc or an inputted vc
            destination = channel or ctx.author.voice.channel 
        except: # If not vc is specified or the author is not in a vc, returns a message
            await ctx.reply("Please join a vc or specify a channel")
        else: # If successful, joins vc and sends msg
            await destination.connect()
            ctx.reply("Bot connected")
            
    @commands.cooldown(1, 5, commands.BucketType.guild)
    @commands.guild_only()
    @commands.command(aliases=["Disconnect","dc"])
    async def disconnect(self, ctx, *, channel: discord.VoiceChannel = None):
        if ctx.voice_client: # If the bot is in a voice channel 
            await ctx.guild.voice_client.disconnect() # Leave the channel
            await ctx.reply('Bot disconnected')
        else: # If the bot is not in a vc
            await ctx.reply("I'm not currently in a vc")

def setup(bot):
    bot.add_cog(musicCog(bot))
