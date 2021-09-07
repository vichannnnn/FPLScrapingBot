from discord.ext import commands
import cogs.colourEmbed as functions
from bs4 import BeautifulSoup
import aiohttp
import json
import discord
import urllib.request
import math

async def fetch(session, url):
    async with session.get(url) as response:
        return await response.text()

class UserCommands(commands.Cog, name="⚙ User Commands"):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(description=f"stc**\n\nA list of Player's name, rank, total and entry name given in a paginated embed.")
    @commands.cooldown(1, 5, commands.BucketType.user)
    async def stc(self, ctx):

        async def main():
            with urllib.request.urlopen("https://fantasy.premierleague.com/api/leagues-classic/32073/standings/") as url:
                data = json.loads(url.read().decode())
                playerList = [player for player in data['standings']['results']]
                return playerList

        async def embedCreator(playerList, i):
            everyPage = [item for item in playerList[10 * (i - 1):i * 10]]

            description = "**Ranks**\n"
            for player in everyPage:
                description += f"{player['rank']}. {player['player_name']} " \
                               f"(Entry Name: {player['entry_name']} | Total: {player['total']})\n"

            embed = discord.Embed(title="STC List", description=description, colour=functions.embedColour(ctx.guild.id))
            embed.set_footer(text=f"Page {i} of {pages}", icon_url=ctx.author.avatar_url)
            return embed

        playerList = await main()
        i = 1
        pages = math.ceil(len(playerList) / 10)
        embed = await embedCreator(list(playerList), i)
        msg = await ctx.send(embed=embed)
        await msg.add_reaction('⏪')
        await msg.add_reaction('⏩')

        def check(reaction, user):
            return str(reaction.emoji) in ['⏪',
                                           '⏩'] and user == ctx.message.author and reaction.message.id == msg.id

        async def handle_rotate(reaction, msg, check, i):
            await msg.remove_reaction(reaction, ctx.message.author)

            if str(reaction.emoji) == '⏩':
                i += 1
                if i > pages:

                    embed = discord.Embed(description=f"You have reached the end of the pages!")
                    embed.set_thumbnail(url=f"{ctx.message.guild.icon_url}")
                    embed.set_footer(text=f"Press '⏪' to go back.", icon_url=ctx.author.avatar_url)
                    await msg.edit(embed=embed)

                else:
                    embed = await embedCreator(playerList, i)
                    await msg.edit(embed=embed)

            elif str(reaction.emoji) == '⏪':
                i -= 1
                if i <= 0:
                    embed = discord.Embed(description=f"You have reached the end of the pages!")
                    embed.set_thumbnail(url=f"{ctx.message.guild.icon_url}")
                    embed.set_footer(text=f"Press '⏩' to go back.", icon_url=ctx.author.avatar_url)
                    await msg.edit(embed=embed)

                else:
                    embed = await embedCreator(playerList, i)
                    await msg.edit(embed=embed)

            else:
                return

            reaction, user = await self.bot.wait_for('reaction_add', check=check, timeout=30)
            await handle_rotate(reaction, msg, check, i)
        reaction, user = await self.bot.wait_for('reaction_add', check=check, timeout=30)
        await handle_rotate(reaction, msg, check, i)

    @commands.command(description=f"sth2h**\n\nPlayer's rank, name, entry name, total, matches played, matches won, matches drawn, matches lost, points given in a paginated embed.")
    @commands.cooldown(1, 5, commands.BucketType.user)
    async def sth2h(self, ctx):

        async def main():
            with urllib.request.urlopen("https://fantasy.premierleague.com/api/leagues-h2h/800996/standings/") as url:
                data = json.loads(url.read().decode())
                playerList = [player for player in data['standings']['results']]
                return playerList

        async def embedCreator(playerList, i):
            everyPage = [item for item in playerList[10 * (i - 1):i * 10]]

            description = "**Ranks**\n"
            for player in everyPage:
                description += f"{player['rank']}. {player['player_name']} " \
                               f"\n(Entry Name: {player['entry_name']} | Total: {player['total']} | Points: {player['points_for']})\n" \
                               f"(Played: {playerList[i]['matches_played']} | Won: {playerList[i]['matches_won']} | Lost: {playerList[i]['matches_lost']} " \
                               f"| Drawn: {playerList[i]['matches_drawn']})\n\n"

            embed = discord.Embed(title="STH2H List", description=description, colour=functions.embedColour(ctx.guild.id))
            embed.set_footer(text=f"Page {i} of {pages}", icon_url=ctx.author.avatar_url)
            return embed

        playerList = await main()
        i = 1
        pages = math.ceil(len(playerList) / 10)
        embed = await embedCreator(list(playerList), i)
        msg = await ctx.send(embed=embed)
        await msg.add_reaction('⏪')
        await msg.add_reaction('⏩')


        def check(reaction, user):
            return str(reaction.emoji) in ['⏪',
                                           '⏩'] and user == ctx.message.author and reaction.message.id == msg.id

        async def handle_rotate(reaction, msg, check, i):
            await msg.remove_reaction(reaction, ctx.message.author)

            if str(reaction.emoji) == '⏩':
                i += 1
                if i + 1 > pages:

                    embed = discord.Embed(description=f"You have reached the end of the pages!")
                    embed.set_thumbnail(url=f"{ctx.message.guild.icon_url}")
                    embed.set_footer(text=f"Press '⏪' to go back.", icon_url=ctx.author.avatar_url)
                    await msg.edit(embed=embed)

                else:
                    embed = await embedCreator(i)
                    await msg.edit(embed=embed)

            elif str(reaction.emoji) == '⏪':
                i -= 1
                if i <= 0:
                    embed = discord.Embed(description=f"You have reached the end of the pages!")
                    embed.set_thumbnail(url=f"{ctx.message.guild.icon_url}")
                    embed.set_footer(text=f"Press '⏩' to go back.", icon_url=ctx.author.avatar_url)
                    await msg.edit(embed=embed)

                else:
                    embed = await embedCreator(i)
                    await msg.edit(embed=embed)

            else:
                return

            reaction, user = await self.bot.wait_for('reaction_add', check=check, timeout=30)
            await handle_rotate(reaction, msg, check, i)
        reaction, user = await self.bot.wait_for('reaction_add', check=check, timeout=30)
        await handle_rotate(reaction, msg, check, i)

    @commands.command(description=f"lineup [Match ID]**\n\nChecks for the current line-up of a specific match ID.")
    @commands.cooldown(1, 5, commands.BucketType.user)
    async def lineup(self, ctx, matchID: int):

        async def main():

            playerList = []
            substituteList = []

            async with aiohttp.ClientSession() as session:
                html = await fetch(session, f"https://www.premierleague.com/match/{matchID}")
                parsed_html = BeautifulSoup(html, features="lxml")
                productDivs = parsed_html.body.find("div", attrs={'class': 'mcTabsContainer'})
                jsonData = json.loads(productDivs.attrs["data-fixture"])  # Convert to JSON Object.
                teamNames = [team['team']['name'] for team in jsonData['teams']]

                for team in jsonData['teamLists']:
                    playerList.append([player['name']['display'] for player in team['lineup']])
                    substituteList.append([player['name']['display'] for player in team['substitutes']])

            return teamNames, playerList, substituteList

        teamNames, playerList, substituteList = await main()

        embed = discord.Embed(title=f"{teamNames[0]} vs. {teamNames[1]}", colour=functions.embedColour(ctx.guild.id))

        description = "**Players**\n\n"
        description += '\n'.join(playerList[0])
        description += '\n\n'
        description += "**Substitutes**\n\n"
        description += '\n'.join(substituteList[0])
        embed.add_field(name=teamNames[0], value=description, inline=True)

        description = "**Players**\n\n"
        description += '\n'.join(playerList[1])
        description += '\n\n'
        description += "**Substitutes**\n\n"
        description += '\n'.join(substituteList[1])
        embed.add_field(name=teamNames[1], value=description, inline=True)

        await ctx.send(embed=embed)






def setup(bot):
    bot.add_cog(UserCommands(bot))
