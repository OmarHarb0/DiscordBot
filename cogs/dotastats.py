import requests
import discord
from discord.ext import commands
from steam import steamid
from wordcloud import WordCloud, STOPWORDS

import matplotlib.pyplot as plt

URL = 'https://api.opendota.com/api/players/'


class Dotastats(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def mmr(self, ctx, account=None):

        if not account:

            try:
                row = await self.bot.db.get_steam_id(ctx.author.id)
                steam32 = int(row["steamid32"])

            except:
                await ctx.send(
                    "Set your steam id using command !setsteam <steamid64> or use !mmr <steamid64>")
                return
        elif len(account) == 17:
            try:
                acc = int(account)
                uid = steamid.SteamID(acc)
                steam32 = uid.as_32

            except ValueError:
                await ctx.send("steamid64 must be an integer")
                return
        else:
            await ctx.send(f"{account} is not a steam64 id")
            return

        url = URL + str(steam32)
        data = requests.get(url)
        infodict = {}
        response = data.json()

        if bool(response.items()):
            for key, value in response.items():
                if key == "tracked_until" and value is None:
                    await ctx.send(f"Account {account} not found")
                    return
                elif key == "mmr_estimate":
                    infodict["mmr"] = value['estimate']
                elif key == "profile":
                    infodict["steamurl"] = value['profileurl']

            embed = discord.Embed(
                title=str("Steam Profile Link"), url=infodict["steamurl"])
            embed.set_author(
                name="Opendota stats",
                icon_url="https://i.imgur.com/YiCKaPR.jpg")
            embed.add_field(name="mmr estimate:", value=infodict["mmr"])
            # embed.add_field(name="most played hero", value=infodict["mmr"])

            embed.set_thumbnail(url="https://i.imgur.com/04f5QEx.jpeg")
            await ctx.send(embed=embed)

    @commands.command()
    async def wordcloud(self, ctx, account=None):

        if not account:

            try:
                row = await self.bot.db.get_steam_id(ctx.author.id)
                steam32 = int(row["steamid32"])

            except:
                await ctx.send(
                    "Set your steam id using command !setsteam <steamid64> or use !mmr <steamid64>")
                return
        elif len(account) == 17:
            try:
                acc = int(account)
                uid = steamid.SteamID(acc)
                steam32 = uid.as_32

            except ValueError:
                await ctx.send("steamid64 must be an integer")
                return
        else:
            await ctx.send(f"{account} is not a steam64 id")
            return

        url = URL + str(steam32) + "/wordcloud"
        data = requests.get(url)
        response = data.json()
        text = None

        # Collect data and add it into one long string
        if bool(response.items()):
            for key, value in response.items():
                if key == "my_word_counts":
                    for word in value:
                        for _ in range(int(value[word])):
                            if text is None:
                                text = word
                            else:
                                text = text + "  " + str(word)

            # Create and generate a word cloud image:
            try:
                wordcloud = WordCloud(
                    max_font_size=60, max_words=300, background_color="white",
                    relative_scaling=0.4, collocations=False, stopwords=STOPWORDS,
                    width=800, height=400
                ).generate(text)

                # Display the generated image:
                plt.figure(figsize=(18, 10))
                plt.imshow(wordcloud, interpolation='bilinear')
                plt.axis("off")
                plt.savefig("plots/image.png", transparent=True)
                plt.show()

                await ctx.send(file=discord.File("plots/image.png"))

            except:
                await ctx.send("** ERROR: DATA NOT FOUND **")


def setup(bot):
    bot.add_cog(Dotastats(bot))
