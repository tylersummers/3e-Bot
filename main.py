from datetime import datetime
import sys
import traceback
import discord
from discord.ext import commands
from discord.ext.commands import Greedy, Context
from discord.utils import get
from typing import Literal, Optional
from discord import app_commands
from random import randint
import platform

import varStore

from dotenv import load_dotenv
from os import getenv
import os
from pathlib import Path

load_dotenv()
token = os.getenv("TOKEN")
class MyBot(commands.Bot):
    def __init__(self):
        super().__init__(
            command_prefix=commands.when_mentioned_or('_'),
            description="""A bot developed by SoulWarden for the IFF. Edited by RAT_DOG for the 3e.""",
            intents=discord.Intents.all(),
            activity=discord.Activity(type=discord.ActivityType.watching, name="me start up"),
            status=discord.Status.online,
            owner_ids=set(varStore.owners),
            help_command=None
            )
        self.cogList = ["adminCmd", "helpCmd", "enlistedCmd", "randomCmd", "backgroundTasks", "attendance"]
        self.synced = False
        
    async def setup_hook(self): 
        for cog in self.cogList:
            await self.load_extension(cog)
        self.tree.copy_global_to(guild=discord.Object(varStore.enlistedGuild))
        await self.tree.sync(guild=discord.Object(varStore.enlistedGuild))
        print("Cogs loaded and tree synced")
        
bot = MyBot()
tree = bot.tree

# Bot starting
@bot.event
async def on_ready():
    now = datetime.now()
    current_time = now.strftime("%H:%M:%S")

    print("Logged in as")
    print(bot.user.name)
    print(bot.user.id)
    print(f"Started at {current_time}")
    
    storageFolder = Path().absolute() / "storage"
    
    memberListTxt = storageFolder / "memberList.txt"
    memberList = open(memberListTxt)
        
    file_lines = memberList.read()
    varStore.members = file_lines.split("\n")
    try:
        varStore.members.remove("")
    finally:
        memberList.close()
        print("Member list updated")

    pastIdTxt = storageFolder / "pastSelectId.txt"
    f = open(pastIdTxt)
        
    file_lines = f.read()
    varStore.pastSelectIds = file_lines.split("\n")
    try:
        varStore.pastSelectIds.remove("")
    finally:
        f.close()
        print("Past ID loaded")

    # Sets prefix
    if platform.system() == 'Windows':
        bot.command_prefix = commands.when_mentioned_or('?')
        print("Platform: Windows")
    else:
        bot.command_prefix = commands.when_mentioned_or('_')
        print("Platform: Linux")
    
    print("Bot ready")

dmChannelId = 961625199109894144


@bot.event
async def on_reaction_add(reaction, user):
    # Ignore bot's own reactions
    if user == bot.user:
        return

    channel_id = 963321651620118568

    # ------------------------------------------------------------------
    # Attendance message handling (thumbsup / thumbsdown / shrug)
    # ------------------------------------------------------------------
    if reaction.message.channel.id == channel_id and \
       reaction.message.id == varStore.leaderPingMsgId:

        msg = await reaction.message.fetch()   # same as before
        thumbUp   = discord.utils.get(msg.reactions, emoji="\N{THUMBS UP SIGN}")
        thumbDown = discord.utils.get(msg.reactions, emoji="\N{THUMBS DOWN SIGN}")
        shrug     = discord.utils.get(msg.reactions, emoji="\N{SHRUG}")

        async def names_from_reaction(reac):
            if not reac:
                return "-"
            ids = [u async for u in reac.users() if u != bot.user]
            return ", ".join(u.name for u in ids) or "-"

        thumbUpNameStr   = await names_from_reaction(thumbUp)
        thumbDownNameStr = await names_from_reaction(thumbDown)
        shrugStr         = await names_from_reaction(shrug)

        embed = discord.Embed(
            title="Officer Attendance",
            description="Can you make it tonight? React with :thumbsup: / :thumbsdown: / :shrug:",
            color=0x109319,
        )
        embed.add_field(name="Coming:", value=f"\u200b{thumbUpNameStr}", inline=False)
        embed.add_field(name="Tonight's Officer Count:", value=f"\u200b{str((thumbUp.count-1) if thumbUp else 0)}", inline=False)
        embed.add_field(name="Not coming:", value=f"\u200b{thumbDownNameStr}", inline=False)
        embed.add_field(name="Tonight's Absent Count:", value=f"\u200b{str((thumbDown.count-1) if thumbDown else 0)}", inline=False)
        embed.add_field(name="Maybe coming/might be late:", value=f"\u200b{shrugStr}", inline=False)
        embed.add_field(name="Count:", value=f"\u200b{str((shrug.count-1) if shrug else 0)}", inline=False)

        await msg.edit(embed=embed)

    # ------------------------------------------------------------------
    # Training / HQ message handling (teacher / handshake / custom emoji)
    # ------------------------------------------------------------------
    elif reaction.message.channel.id == channel_id and \
         reaction.message.id == varStore.trainingMsgId:

        msg = await reaction.message.fetch()

        teacherReac   = discord.utils.get(msg.reactions, emoji="🧑‍🏫")
        helpReac      = discord.utils.get(msg.reactions, emoji="🤝")
        hqReac        = discord.utils.get(msg.reactions, emoji=discord.utils.get(msg.guild.emojis, name="3e"))

        async def names_from_reaction(reac):
            if not reac:
                return "-"
            ids = [u async for u in reac.users() if u != bot.user]
            return ", ".join(u.name for u in ids) or "-"

        teacherStr = await names_from_reaction(teacherReac)
        helpStr    = await names_from_reaction(helpReac)
        hqStr      = await names_from_reaction(hqReac)

        embed = discord.Embed(
            title="Training & HQ",
            description="Are you happy to take training :teacher: ? Are you happy to help with training :handshake: ? Are you happy to take HQ <:3e:1205672874166325281> ?",
            color=0x109319,
        )
        embed.add_field(name="Happy to take training:", value=f"\u200b{teacherStr}", inline=False)
        embed.add_field(name="Count:", value=f"\u200b{str((teacherReac.count-1) if teacherReac else 0)}", inline=False)
        embed.add_field(name="Happy to help with training:", value=f"\u200b{helpStr}", inline=False)
        embed.add_field(name="Count:", value=f"\u200b{str((helpReac.count-1) if helpReac else 0)}", inline=False)
        embed.add_field(name="Happy to take HQ:", value=f"\u200b{hqStr}", inline=False)
        embed.add_field(name="Count:", value=f"\u200b{str((hqReac.count-1) if hqReac else 0)}", inline=False)

        await msg.edit(embed=embed)


@bot.event
async def on_reaction_remove(reaction, user):
    if (
        reaction.message.channel.id == 961625199109894144
        and reaction.message.id == varStore.leaderPingMsgId
    ):
        msg = await (reaction.message.channel).fetch_message(reaction.message.id)
        thumbUp = discord.utils.get(msg.reactions, emoji="\N{THUMBS UP SIGN}")
        thumbDown = discord.utils.get(msg.reactions, emoji="\N{THUMBS DOWN SIGN}")
        shrug = discord.utils.get(msg.reactions, emoji="\N{SHRUG}")
        thumbUpCount = str(thumbUp.count - 1)
        thumbDownCount = str(thumbDown.count - 1)
        shrugCount = str(shrug.count - 1)

        for reactions in msg.reactions:
            if str(reactions) == "\N{THUMBS UP SIGN}":
                thumbUpIds = [
                    user async for user in reactions.users() if user != bot.user
                ]
                thumbUpNames = []

                for user in thumbUpIds:
                    thumbUpNames.append(user.name)
                thumbUpNameStr = ", ".join(thumbUpNames)

        for reactions in msg.reactions:
            if str(reactions) == "\N{THUMBS DOWN SIGN}":
                thumbDownIds = [
                    user async for user in reactions.users() if user != bot.user
                ]
                thumbDownNames = []

                for user in thumbDownIds:
                    thumbDownNames.append(user.name)
                thumbDownNameStr = ", ".join(thumbDownNames)

        for reactions in msg.reactions:
            if str(reactions) == "\N{SHRUG}":
                shrugIds = [
                    user async for user in reactions.users() if user != bot.user
                ]
                shrugNames = []

                for user in shrugIds:
                    shrugNames.append(user.name)
                shrugStr = ", ".join(shrugNames)

        if thumbUpNameStr == "":
            thumbUpNameStr = "-"
        if thumbDownNameStr == "":
            thumbDownNameStr = "-"
        if shrugStr == "":
            shrugStr = "-"

        embed = discord.Embed(
            title="Leadership Attendance",
            description="Can you make it tonight? React with :thumbsup: / :thumbsdown: / :shrug:",
            color=0x109319,
        )
        embed.add_field(name="Coming: ", value=f"\u200b{thumbUpNameStr}", inline=False)
        embed.add_field(name="Tonight's Officer Count: ", value=f"\u200b{thumbUpCount}", inline=False)
        embed.add_field(
            name="Not coming: ", value=f"\u200b{thumbDownNameStr}", inline=False
        )
        embed.add_field(name="Tonight's Absent Count: ", value=f"\u200b{thumbDownCount}", inline=False)
        embed.add_field(name="Maybe coming/might be late: ", value=f"\u200b{shrugStr}", inline=False)
        embed.add_field(name="Count: ", value=f"\u200b{shrugCount}", inline=False)

        await msg.edit(embed=embed)


# Prints out errors to console
@bot.event
async def on_command_error(ctx, error):
    """The event triggered when an error is raised while invoking a command.
    Parameters
    ------------
    ctx: commands.Context
        The context used for command invocation.
    error: commands.CommandError
        The Exception raised.
    """

    # This prevents any commands with local handlers being handled here in on_command_error.
    if hasattr(ctx.command, 'on_error'):
        return

    # This prevents any cogs with an overwritten cog_command_error being handled here.
    cog = ctx.cog
    if cog:
        if cog._get_overridden_method(cog.cog_command_error) is not None:
            return

    ignored = (commands.CommandNotFound, )

    # Allows us to check for original exceptions raised and sent to CommandInvokeError.
    # If nothing is found. We keep the exception passed to on_command_error.
    error = getattr(error, 'original', error)

    # Anything in ignored will return and prevent anything happening.
    if isinstance(error, ignored):
        return

    if isinstance(error, commands.DisabledCommand):
        await ctx.send(f'{ctx.command} has been disabled.')

    elif isinstance(error, commands.NoPrivateMessage):
        try:
            await ctx.author.send(f'{ctx.command} can not be used in Private Messages.')
        except discord.HTTPException:
            pass

    # For this error example we check to see where it came from...
    elif isinstance(error, commands.BadArgument):
        if ctx.command.qualified_name == 'tag list':  # Check if the command being invoked is 'tag list'
            await ctx.send('I could not find that member. Please try again.')

    else:
        # All other Errors not returned come here. And we can just print the default TraceBack.
        print('Ignoring exception in command {}:'.format(ctx.command), file=sys.stderr)
        traceback.print_exception(type(error), error, error.__traceback__, file=sys.stderr)
            
# Prints when a guild is joined
@bot.event
async def on_guild_join(ctx, error):
    now = datetime.now()
    current_time = now.strftime("%H:%M:%S")
    print(f"Bot has joined {ctx.guild} at {current_time}")


# Prints when a guild if left
@bot.event
async def on_guild_remove(ctx, error):
    now = datetime.now()
    current_time = now.strftime("%H:%M:%S")
    print(f"Bot has left {ctx.guild} at {current_time}")
    
# For giving return members their roles back
@bot.event
async def on_member_remove(member):
    enlistedGuild = bot.get_guild(772917331235438654)
    enlistedRole = get(enlistedGuild.roles, id = 772922211933224960)
    
    storageFolder = Path().absolute() / "storage"
    leftMembersFile = storageFolder / "leftMembers.txt"
    
    # Checks if the guild is the 3e guild and if they have the Enlisted role
    if member.guild != enlistedGuild or enlistedRole not in member.roles:
        return
    
    # Checks if the user is already in the left members list and removes any previous versions
    with open(leftMembersFile, "r") as file:
        lines = file.readlines()
        lines_to_remove = []
        
        for i,line in enumerate(lines):
            if line.strip() == str(member.id):
                lines_to_remove.append(i)
                lines_to_remove.append(i+1)
                
    with open(leftMembersFile, "w") as file:
        for i, line in enumerate(lines):
            if i not in lines_to_remove:
                file.write(line)
    
    roleIds = []
    
    # Gets all the roles from a user and makes a list of strings with the role id's
    for role in member.roles:
        roleIds.append(str(role.id))
    
    # Converts the list into a string seperated by commas
    roleIds = ",".join(roleIds)

    # Writes the user ID with the following line containing the role id's
    with open(leftMembersFile, "a") as file:
        file.write(str(member.id) + "\n" + roleIds + "\n")
        
@bot.event
async def on_member_join(member):
    storageFolder = Path().absolute() / "storage"
    leftMembersFile = storageFolder / "leftMembers.txt"
    regimentBotTestChannel = bot.get_channel(832452992137166908)
    
    with open(leftMembersFile, "r") as file:
        lines = file.readlines()
        
        for line in lines:
            if line.strip() == str(member.id):
                await regimentBotTestChannel.send(f"{member.display_name} has previously been in the 3e server and can have their roles returned with </return_role:1125667822815694950>")
                break
        
    
    
@bot.command()
@commands.guild_only()
@commands.is_owner()
async def sync(
  ctx: Context, guilds: Greedy[discord.Object], spec: Optional[Literal["~", "*", "^"]] = None) -> None:
    if not guilds:
        if spec == "~":
            synced = await ctx.bot.tree.sync(guild=ctx.guild)
        elif spec == "*":
            ctx.bot.tree.copy_global_to(guild=ctx.guild)
            synced = await ctx.bot.tree.sync(guild=ctx.guild)
        elif spec == "^":
            ctx.bot.tree.clear_commands(guild=ctx.guild)
            await ctx.bot.tree.sync(guild=ctx.guild)
            synced = []
        else:
            synced = await ctx.bot.tree.sync()

        await ctx.send(
            f"Synced {len(synced)} commands {'globally' if spec is None else 'to the current guild.'}"
        )
        return

    ret = 0
    for guild in guilds:
        try:
            await ctx.bot.tree.sync(guild=guild)
        except discord.HTTPException:
            pass
        else:
            ret += 1

    await ctx.send(f"Synced the tree to {ret}/{len(guilds)}.")
    
@bot.command()
@commands.is_owner()
async def clear(ctx):
    tree.clear_commands(guild=discord.Object(id = varStore.enlistedGuild))
    await tree.sync(guild=discord.Object(id = varStore.enlistedGuild))
    await ctx.reply("Tree cleared")
    
# Reload cogs command
@bot.command()
@commands.is_owner()
async def reload(ctx, extension: str = None):
    count = 1
    if extension is None:
        embed = discord.Embed(
            title="Reload", description="Reloaded cogs: ", color=0xFF00C8
        )
        for x in bot.cogList:
            await bot.reload_extension(x)
            embed.add_field(name=f"**#{count}**", value=f"{x} reloaded", inline=False)
            count += 1
        await ctx.send(embed=embed)
        print("All cogs reloaded")
    else:
        await bot.reload_extension(f"{extension}")
        embed = discord.Embed(
            title="Reload",
            description=f"{extension} successfully reloaded",
            color=0xFF00C8,
        )
        await ctx.send(embed=embed)
        print(f"{extension} reloaded")

# Unload cogs command
@bot.command()
@commands.is_owner()
async def unload(ctx, extension: str = None):
    count = 1
    if extension is None:
        embed = discord.Embed(
            title="Unload", description="Unloaded cogs", color=0x109319
        )
        for x in bot.cogList:
            try:
                await bot.unload_extension(x)
            except commands.ExtensionNotLoaded:
                embed.add_field(
                    name=f"**#{count}**", value=f"{x} is already unloaded", inline=False
                )
                count += 1
            else:
                embed.add_field(
                    name=f"**#{count}**", value=f"{x} unloaded", inline=False
                )
                count += 1
        await ctx.send(embed=embed)
    else:
        await bot.unload_extension(extension)
        embed = discord.Embed(
            title="Unload", description=f"{extension} cog unloaded", color=0x109319
        )
        await ctx.reply(embed=embed)


# Load cogs command
@bot.command()
@commands.is_owner()
async def load(ctx, extension: str = None):
    count = 1
    if extension is None:
        embed = discord.Embed(title="Load", description="Loaded cogs", color=0x109319)
        for x in bot.cogList:
            try:
                await bot.load_extension(x)
            except commands.ExtensionAlreadyLoaded:
                embed.add_field(
                    name=f"**#{count}**", value=f"{x} is already loaded", inline=False
                )
                count += 1
            else:
                embed.add_field(name=f"**#{count}**", value=f"{x} loaded", inline=False)
                count += 1
        await ctx.send(embed=embed)
    else:
        await bot.load_extension(extension)
        embed = discord.Embed(
            title="Load", description=f"{extension} cog loaded", color=0x109319
        )
        await ctx.reply(embed=embed)

bot_token = os.getenv("BOT_TOKEN")   # <- read the token from env
if not bot_token:
    raise RuntimeError("Missing BOT_TOKEN environment variable")

bot.run(bot_token)
