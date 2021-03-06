"""The script runs the bot."""
import os
from discord.ext import commands
from discord.utils import get
import discord
from utils.consts import Consts

consts = Consts()
bot = commands.Bot(command_prefix="+",
                   status=discord.Status.online,
                   activity=discord.Game(name="Gaming"))


@bot.event
async def on_ready():
    """Run when the bot is ready."""
    print("Ready to go!")
    print(f"Serving: {len(bot.guilds)} servers!")
    await bot.change_presence(status=discord.Status.online,
                              activity=discord.Game(name="Gaming"))


@bot.event
async def on_member_join(ctx):
    """Run when a new member joins."""
    role = get(ctx.guild.roles, name="Newbie")
    await ctx.add_roles(role)
    channel = bot.get_channel(consts.channels['welcome'])
    await ctx.send(consts.welcomeDMMessage.format(ctx.name))
    await channel.send(
        f"Welcome, {ctx.mention} please react to the message to get a role"
    )
    reaction, user = await bot.wait_for('reaction_add')
    role = get(ctx.guild.roles, name='Member')
    await ctx.add_roles(role)


@bot.event
async def on_member_ban(ctx, member):
    """Run when a member gets banned (probably kacper)."""
    channel = bot.get_channel(consts.channels['announcements'])
    await channel.send(f"{member.name} Just got banned from the server")


@bot.event
async def on_message(message):
    """Run when a user sends a message."""
    channel = bot.get_channel(consts.channels['announcements'])
    if message.channel == channel:
        # If the message was NOT send by the bot
        if message.author != bot:
            await message.pin()
    # To stop dan from just saying 'gay'
    if message.author.id == 306175377661886505 and \
            'gay' in message.content.lower():
        await message.delete()
    if any(sp in message.content.lower() for sp in consts.spanishLetters):
        await message.add_reaction(u'\U0001F1EA\U0001F1F8')
    await bot.process_commands(message)


bot.load_extension("cogs.error_handler")
bot.load_extension("cogs.main")
bot.load_extension("cogs.game")
bot.load_extension("cogs.audio")
try:
    token = os.environ['DISCORD_BOT_TOKEN']
except KeyError:
    with open("token.txt", "r") as tokenF:
        token = tokenF.readlines()[0]
bot.run(token)
