import discord
from discord.ext import commands

class helpCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
    @commands.group(pass_context=True)
    @commands.cooldown(1, 2, commands.BucketType.user)
    async def help(self, ctx):
        if ctx.invoked_subcommand is None:
            #### Create the initial embed object ####
            helpMsg=discord.Embed(title="3e Bot Command List", description="Insert an _ immediately before each command to run them.", color=0x17169a)
            helpMsg.add_field(name="Ping", value="Test command for testing bot response time", inline=False)
            helpMsg.add_field(name="Dice <number>", value="Input a number, rolls a dice with that many sides", inline=False)
            helpMsg.add_field(name="mcid <minecraft username>", value="Input the username of a minecraft player, outputs their UUID", inline=False)
            helpMsg.add_field(name="mcname <minecraft UUID>", value="Input the uuid of a minecraft player, outputs their username", inline=False)
            helpMsg.add_field(name="id <Discord User ID>", value="Input the discord id of a user, output their username", inline=False)
            helpMsg.add_field(name="Avatar <@user>", value="Posts the image of a pinged users avatar", inline=False)
            helpMsg.add_field(name="ID <@user>", value="Converts a pinged user to their ID", inline=False)
            helpMsg.add_field(name="User <Discord User ID>", value="Converts an inputted User ID to username", inline=False)
            helpMsg.add_field(name="Eight Ball", value="It's a magic eight ball", inline=False)
            helpMsg.add_field(name="GitHub", value="Returns a URL to SoulWarden's IFF-Bot Repo", inline=False)
            helpMsg.add_field(name="xkcd <number>", value="Shows the xkcd comic corresponding to the User's input", inline=False)
            helpMsg.add_field(name="math <input>", value="Evaluates an equation", inline=False)
            helpMsg.add_field(name="attendance check @user", value="Shows a snapshot of a user's events and time in the regiment", inline=False)
            helpMsg.set_footer(text="3e Bot created by soulwarden & rat_dog")
            helpMsg.set_author(name=ctx.author.display_name)

            await ctx.send(embed=helpMsg)

    #Officer HELP --------------------------------------------------------
    @commands.has_any_role(
        772921452135055360, 772921453095944203, 772921877953904661, 772921882072449075
    )
    @help.group(pass_context=True, aliases=["officer"])
    async def Officer(self,ctx):
        if ctx.invoked_subcommand is None:
            embed=discord.Embed(title="3e Bot Officer Command List", description="Insert an _ immediately before each command to run them.",color=0x17169a)
            embed.add_field(name="logbook report", value="[All Officers] Shows a list of Members connected to the VCs.", inline=False)
            embed.add_field(name="logbook event", value="[All Officers] Gives 1 event in the Logbook to all users present.", inline=False)
            embed.add_field(name="logbook training", value="[All Officers] Gives 1 training in the Logbook to all users present.", inline=False)
            embed.add_field(name="campfire", value="[All Officers] Moves all users in the current connected voice chat to Campfire + Tunes", inline=False)
            embed.add_field(name="forceCampfire", value="[All Officers] Moves **all** users in ALL regiment camp channels to Campfire + Tunes", inline=False)
            embed.add_field(name="dm <ping> <message>", value="[All Officers] DM a user via the bot.", inline=False)
            embed.add_field(name="echo <message>", value="[All Officers] The bot will copy what you write & delete your original message.", inline=False)
            embed.add_field(name="muster", value="[All Officers] Generates the muster roll - run this command in #muster-roll", inline=False)
            embed.add_field(name="leadAttend", value="[All Officers] Creates leadership attendance ping", inline=False)
            embed.add_field(name="welcomeMat", value="[Senior Officers Only] Posts hard-coded message in #welcome-mat channel", inline=False)
            embed.add_field(name="regimentRules", value="[Senior Officers Only] Posts hard-coded message in #regiment-rules channel", inline=False)
            embed.add_field(name="regimentRanks", value="[Senior Officers Only] Posts hard-coded message in #regiment-ranks channel", inline=False)
            embed.add_field(name="eventSchedule", value="[Senior Officers Only] Posts hard-coded message in #event-schedule channel", inline=False)
            embed.add_field(name="enlistmentOffice", value="[Senior Officers Only] Posts hard-coded message in #enlistment-office channel", inline=False)
            embed.add_field(name="medals", value="[Senior Officers Only] Posts hard-coded message in #medals channel", inline=False)
            embed.add_field(name="suggestionBox", value="[Senior Officers Only] Posts hard-coded message in #suggestion-box channel", inline=False)
            embed.set_author(name=ctx.author.display_name)
            await ctx.send(embed=embed)
    #Admin HELP --------------------------------------------------------
    @commands.has_any_role(
        772921452135055360, 772921453095944203, 772921877953904661, 772921882072449075
    )
    @help.group(pass_context=True, aliases=["admin"])
    async def Admin(self,ctx):
        if ctx.invoked_subcommand is None:
            embed=discord.Embed(title="3e Bot Administrative Command List", description="Insert an _ immediately before each command to run them.",color=0x17169a)
            embed.add_field(name="ad quit", value="[Administrative Use Only] Shutdown Bot", inline=False)
            embed.add_field(name="ad up", value="[Administrative Use Only] Update Discord Member List variable (NOT attendance command)", inline=False)
            embed.add_field(name="ad cogstatus", value="[Administrative Use Only] Check cog status", inline=False)
            embed.add_field(name="ad status", value="[Administrative Use Only] Set custom Discord bot status", inline=False)
            embed.add_field(name="ad rotate", value="[Administrative Use Only] Turn on auto pre-defined status rotation", inline=False)
            embed.add_field(name="ad join", value="[Administrative Use Only] Bring bot into connected VC", inline=False)
            embed.add_field(name="ad leave", value="[Administrative Use Only] Make bot leave current VC", inline=False)
            embed.add_field(name="ad rgb", value="[Administrative Use Only] Toggle RGB Mode", inline=False)
            embed.add_field(name="ad get members", value="[Administrative Use Only] Prints list of hard-coded members and IDs", inline=False)
            embed.add_field(name="ad get servers", value="[Administrative Use Only] Prints list of Discord servers running 3e Bot", inline=False)
            embed.add_field(name="ad get time", value="[Administrative Use Only] Check that the bot is in-time", inline=False)
            embed.add_field(name="ad get platform", value="[Administrative Use Only] Check that the bot is running on the VPS", inline=False)
            embed.add_field(name="ad get cogs", value="[Administrative Use Only] Print list of cogs", inline=False)
            embed.add_field(name="reload", value="[Administrative Use Only] Reload cogs", inline=False)
            embed.add_field(name="load", value="[Administrative Use Only] Load cogs", inline=False)
            embed.add_field(name="unload", value="[Administrative Use Only] Unload cogs", inline=False)
            embed.set_author(name=ctx.author.display_name)
            await ctx.send(embed=embed)

async def setup(bot):
    await bot.add_cog(helpCog(bot))
