"""Cog for main commands."""
import os
import requests
import datetime
import random
from dateutil.relativedelta import relativedelta
import discord
import youtube_dl
from bs4 import BeautifulSoup
from discord.utils import get
from discord.ext import commands
from utils.consts import Consts
from utils.embedgenerator import Embed


class MainCog:
    """Main cog."""

    CONSTS = Consts()

    def __init__(self, bot):
        """Initialize the cog."""
        print("Main cog Initialized")
        self.bot = bot

    @commands.command()
    @commands.cooldown(1, 1, commands.BucketType.user)
    async def roll(self, ctx, max: int = None):
        """Run when the roll command is called."""
        if not type(max) == int or not max or max < 0:
            return await ctx.channel.send("Please do ~roll <max(int)>")
        number = random.randint(1, max)
        return await ctx.channel.send(f"`You rolled a {number}`")

    @commands.command(aliases=['cls'])
    @commands.cooldown(1, 15, commands.BucketType.user)
    async def clear(self, ctx, number: int = 10):
        """Clear messages."""
        print("Clear called")
        if "administrator" in [y.name.lower() for y in ctx.author.roles]:
            if number > 0 and number < 75:
                deleted = await ctx.channel.purge(limit=number + 1)
                await ctx.channel.send(
                            f"Deleted {len(deleted) - 1} messages")
            return await ctx.channel.send(
                            "You can specify a number of messages (1 - 75)")
        return await ctx.channel.send(
                            "You don't have the `administrator` role!")

    @commands.command(aliases=['who'])
    @commands.cooldown(1, 5, commands.BucketType.user)
    async def whois(self, ctx, member: discord.Member = None):
        """Run when the whois command is called."""
        if member is None:
            return await ctx.channel.send("Please do: ~whois @user")
        embed = Embed([("Display Username", f":name_badge: {member.name}"),
                       ("Status", f":o:{str(member.status)}"),
                       ("Joined On", f":date: {member.joined_at.date()}"),
                       ("Role(s)", f":bow:" + ''.join(
                        [str(role.mention) for role in member.roles[1:]]))])
        embed.author = ctx.message.author
        embed.thumbnail = member.avatar_url
        embed = embed.generate_embed()
        return await ctx.channel.send(embed=embed)

    @commands.command()
    @commands.cooldown(1, 120, commands.BucketType.user)
    async def report(self, ctx, victim: discord.Member, reason: str):
        """Run when the report command is called."""
        if victim is None or reason is None:
            return await ctx.channel.send("Please do ~report <user> <reason>")
        for member in ctx.guild.members:
            for role in member.roles:
                print(f"{role.name} - {role.id}")
                # Administrator or owner
                if role.id in self.CONSTS.administrators:
                    try:
                        await member.send("{} reported {} for {}".format(
                                                ctx.author.name, victim, reason
                                                ))
                    # User has DMs from members disabled
                    except discord.errors.HTTPException:
                        pass
        return await ctx.channel.send(":white_check_mark: Thank you")

    @commands.command(aliases=['say'])
    @commands.cooldown(1, 5, commands.BucketType.user)
    async def echo(self, ctx, *args):
        """Run when the echo command is called."""
        if args is None:
            return await ctx.channel.send("Please do ~echo <message>")
        return await ctx.channel.send(f"`{' '.join([x for x in args])}`")

    @commands.command(aliases=['serverinfo', 'svinfo'])
    @commands.cooldown(1, 30, commands.BucketType.user)
    async def server(self, ctx):
        """Run when the server command is called - gives info about server."""
        guild = ctx.message.author.guild
        embed = Embed([("Server Name", f":name_badge: {guild.name}"),
                       ("Region", f":o:{guild.region}"),
                       ("Owner", f":person_with_blond_hair: {guild.owner}"),
                       ("Member Count", f":100: {guild.member_count}"),
                       ("Date Created", f":date: {guild.created_at}")])
        embed.thumbnail = guild.icon_url
        embed = embed.generate_embed()
        return await ctx.channel.send(embed=embed)

    @commands.command(aliases=['depressme', 'exams'])
    @commands.cooldown(1, 10, commands.BucketType.user)
    async def gcses(self, ctx):
        """Run when the gcse countdown command is called."""
        today = datetime.datetime.today()
        td = relativedelta(datetime.datetime(2019, 5, 13, 9, 0, 0), today)
        return await ctx.channel.send(
            "`{} months, {} weeks, {} days, {} hours {} minutes until GCSES!`"
            .format(
                td.months, td.weeks, td.days, td.hours, td.minutes
            ))

    @commands.command(aliases=['word', 'wordoftheday', 'spaword'])
    @commands.cooldown(1, 15, commands.BucketType.user)
    async def wotd(self, ctx):
        """Run when the wotd command is called."""
        r = requests.get("https://www.spanishdict.com/")
        soup = BeautifulSoup(r.content, features="lxml")
        spa = soup.find('a', {'class': 'wotd-sidebar-word'}).text
        eng = soup.find('div', {'class': 'wotd-sidebar-translation'}).text
        return await ctx.channel.send(f":flag_es:`{spa} - {eng}`:flag_es:")


def setup(bot):
    """Initialize and add to main script."""
    bot.add_cog(MainCog(bot))
