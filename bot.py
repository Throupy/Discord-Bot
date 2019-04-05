"""The script runs the bot."""
import os
from discord.ext import commands
from discord.utils import get
import discord
from utils.consts import Consts

consts = Consts()
bot = commands.Bot(command_prefix="~",
                   status=discord.Status.online,
                   activity=discord.Game(name="Fucking bitches"))


@bot.event
async def on_ready():
    """Run when the bot is ready."""
    print("Ready to go!")
    print(f"Serving: {len(bot.guilds)} servers!")
    await bot.change_presence(status=discord.Status.online,
                              activity=discord.Game(name="Fucking bitches"))


@bot.event
async def on_member_join(ctx):
    """Run when a new member joins."""
    channel = get(bot.get_all_channels(),
                  guild__name='Lube Lads',
                  name='welcome')
    await ctx.send(consts.welcomeDMMessage.format(ctx.name))
    await channel.send(f"Welcome, {ctx.mention} to the server!")


@bot.event
async def on_member_ban(ctx, member):
    """Run when a member gets banned (probably kacper)."""
    channel = get(bot.get_all_channels(),
                  guild__name="Lube Lads",
                  name="announcements")
    await channel.send(f"{member.name} Just got banned from the server")

bot.load_extension("cogs.error_handler")
bot.load_extension("cogs.main")
token = os.environ.get("DISCORD_BOT_TOKEN")
bot.run(token)
