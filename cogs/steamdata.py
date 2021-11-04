from steam import steamid
from discord.ext import commands

class Steamdata(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def setsteam(self, ctx, steam64: int):

        user_id = ctx.author.id
        url = f"https://steamcommunity.com/id/{steam64}"
        steam = steamid.SteamID(steam64)
        steam32 = steam.as_32

        try:
            await self.bot.db.user_add(user_id, steam32, steam64, url)
            await ctx.send(f'Successfully added {steam64} to the database')
        except Exception as error:
            await ctx.send(error)



def setup(bot):
    bot.add_cog(Steamdata(bot))
