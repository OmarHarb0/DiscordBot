from discord.ext import commands
import os
import random
import discord


class Resepti(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def päivänresepti(self, ctx):
        filename = random.choice(os.listdir("E:/resepti"))
        await ctx.send(file=discord.File(f"E:/resepti/{filename}"))