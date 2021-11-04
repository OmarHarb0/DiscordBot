from discord.ext import commands
import os
import random
import discord


class Spam(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def niilo(self, ctx):
        filename = random.choice(os.listdir("E:/niilo22"))
        await ctx.send(file=discord.File(f"E:/niilo22/{filename}"))

    @commands.command()
    async def ricardo(self, ctx):
        filename = random.choice(os.listdir("E:/ricardo"))
        await ctx.send(file=discord.File(f"E:/ricardo/{filename}"))


def setup(bot):
    bot.add_cog(Spam(bot))
