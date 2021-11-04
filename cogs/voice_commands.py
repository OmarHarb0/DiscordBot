from discord.ext import commands

import discord
from time import sleep


class Voice_Commands(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def ear(self, ctx):

        voice_channel = ctx.message.author.voice.channel

        if voice_channel is not None:
            vc = await voice_channel.connect()
            vc.play(discord.FFmpegPCMAudio(executable="C:/ffmpeg/bin/ffmpeg.exe",
                                           source="E:/sounds/baba.mp3"))
            # Sleep while audio is playing.
            while vc.is_playing():
                sleep(.1)
            await vc.disconnect()

        else:
            await ctx.send(str(ctx.author.name) + "is not in a channel.")

    @commands.command()
    async def xd(self, ctx):

        voice_channel = ctx.message.author.voice.channel

        if voice_channel is not None:
            vc = await voice_channel.connect()
            vc.play(
                discord.FFmpegPCMAudio(executable="C:/ffmpeg/bin/ffmpeg.exe",
                                       source="E:/sounds/xd.mp3"))
            # Sleep while audio is playing.
            while vc.is_playing():
                sleep(.1)
            await vc.disconnect()

        else:
            await ctx.send(str(ctx.author.name) + "is not in a channel.")

    @commands.command()
    async def gg(self, ctx):

        voice_channel = ctx.message.author.voice.channel

        if voice_channel is not None:
            vc = await voice_channel.connect()
            vc.play(
                discord.FFmpegPCMAudio(executable="C:/ffmpeg/bin/ffmpeg.exe",
                                       source="E:/sounds/upagainstthewind.mp3"))
            # Sleep while audio is playing.
            while vc.is_playing():
                sleep(.1)
            await vc.disconnect()

        else:
            await ctx.send(str(ctx.author.name) + "is not in a channel.")

    @commands.command()
    async def black(self, ctx):

        try:
            voice_channel = ctx.message.author.voice.channel
            vc = await voice_channel.connect()
            await ctx.send("https://gfycat.com/agilepointlesshornshark")
            vc.play(
                discord.FFmpegPCMAudio(executable="C:/ffmpeg/bin/ffmpeg.exe",
                                       source="E:/sounds/black.mp3"))
            # Sleep while audio is playing.
            while vc.is_playing():
                sleep(.1)
            await vc.disconnect()

        except:
            await ctx.send(file=discord.File("E:/kuva/asd.jpg"))

def setup(bot):
    bot.add_cog(Voice_Commands(bot))
