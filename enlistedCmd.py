from ntpath import join
import discord
from discord.ext import commands
from discord.utils import get
import varStore
from random import randint
import datetime
import asyncio

officers = [
    661521548061966357,
    660353960514813952,
    661522627646586893,
    948862889815597079,
]


class enlistedCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    # Senior Officers, COs, NCOs, Officer Corps
    @commands.has_any_role(
        772921452135055360, 772921453095944203, 772921882072449075, 772921877953904661
    )

    @commands.cooldown(1, 1, commands.BucketType.user)
    @commands.command(aliases=["Schedule", "timetable", "Timetable"])
    async def schedule(self, ctx):
        await ctx.reply("You can find our event schedule in #event-schedule")

    @commands.cooldown(1, 1, commands.BucketType.user)
    @commands.command(aliases=["Ranks", "rank", "Rank"])
    async def ranks(self, ctx):
        await ctx.reply("You can find the ranks in #regiment-ranks")

    #Leadership attendance ping
    @commands.guild_only()
    @commands.cooldown(1, 10, commands.BucketType.guild)
    @commands.command(aliases=["leadattend","leadershipAttendnace"])
    async def leadAttend(self, ctx):
        leadershipChannel = self.bot.get_channel(961625199109894144)

        embed = discord.Embed(
            title="Officer Attendance",
            description="Can you make it tonight? React with :thumbsup: , :thumbsdown: , or :person_shrugging:",
            color=0x109319
        )
        embed.add_field(name="Coming: ", value=f"No Officers attending! :(", inline=False)
        embed.add_field(name="Count: ", value=f"0", inline=False)
        embed.add_field(name="Not coming: ", value=f"No apologies received. :)", inline=False)
        embed.add_field(name="Count: ", value=f"0", inline=False)
        embed.add_field(name="Maybe coming/might be late: ", value=f"No timely attendance in doubt!", inline=False)
        embed.add_field(name="Count: ", value=f"0", inline=False)

        msg = await leadershipChannel.send(embed=embed)

        await msg.add_reaction("\N{THUMBS UP SIGN}")
        await msg.add_reaction("\N{THUMBS DOWN SIGN}")
        await msg.add_reaction("\N{SHRUG}")

        varStore.leaderPingMsgId = msg.id

    #Move all users in current vc to campfire
    @commands.has_any_role(
        772921452135055360, 772921453095944203, 772921882072449075, 772921877953904661
    )
    @commands.guild_only()
    @commands.cooldown(1, 10, commands.BucketType.guild)
    @commands.command(aliases=["Campfire"])
    async def campfire(self, ctx):
        async with ctx.channel.typing():
            await ctx.reply("Moving users now")
            campfireTunes = self.bot.get_channel(772920468515848213)
            connectedUsers = ctx.author.voice.channel.members

            for user in connectedUsers:
                await user.move_to(campfireTunes)

    #Move everyone to Campfire + Tunes
    @commands.has_any_role(
        772921452135055360, 772921453095944203, 772921882072449075, 772921877953904661
    )
    @commands.guild_only()
    @commands.cooldown(1, 10, commands.BucketType.guild)
    @commands.command(aliases=["Forcecampfire","unfuck","return"])
    async def forcecampfire(self, ctx):
        async with ctx.channel.typing():
            await ctx.reply("Moving users now")
            vcCatId = 772918008737038367
            campfireTunes = self.bot.get_channel(772920468515848213)

            for channel in ctx.guild.voice_channels:
                if channel.category_id == vcCatId and channel.category_id != 772920468515848213:
                    for user in channel.members:
                        await user.move_to(campfireTunes)
        await ctx.reply("Done!")

    #Post Welcome
    @commands.has_any_role(
        772921452135055360, 772921453095944203
    )
    @commands.guild_only()
    @commands.cooldown(1, 10, commands.BucketType.guild)
    @commands.command(aliases=["welcomeMat"])
    async def welcomemat(self, ctx):
        welcomeChannel = self.bot.get_channel(936199253695533127)
        embed=discord.Embed(color=0xc81105)
        embed.set_author(name="3eRegiment.com", url="https://www.3eregiment.com/", icon_url="https://i.ibb.co/ysrY8Bz/27.webp")
        embed.set_footer(text="Check out our website!")
        await welcomeChannel.send(embed=embed)
        embed=discord.Embed(color=0xff0000)
        embed.set_author(name="YouTube", url="https://www.youtube.com/@3eR%C3%A9gimentSuisse", icon_url="https://cdn-icons-png.flaticon.com/128/3128/3128307.png")
        embed.set_footer(text="View our latest highlights, news & more!")
        await welcomeChannel.send(embed=embed)
        embed=discord.Embed(color=0x23268a)
        embed.set_author(name="Steam Group", url="https://steamcommunity.com/groups/3eRegimentDsuisse", icon_url="https://upload.wikimedia.org/wikipedia/commons/thumb/8/83/Steam_icon_logo.svg/2048px-Steam_icon_logo.svg.png")
        embed.set_footer(text="Connect with us on Steam!")
        await welcomeChannel.send(embed=embed)
        embed=discord.Embed(color=0x242782)
        embed.set_author(name="Map and Uniform Workshop Collection", url="https://steamcommunity.com/sharedfiles/filedetails/?id=2309633935", icon_url="https://upload.wikimedia.org/wikipedia/commons/thumb/a/aa/Tools-spanner-hammer.svg/1200px-Tools-spanner-hammer.svg.png")
        embed.set_footer(text="A collection of our mods!")
        await welcomeChannel.send(embed=embed)
        embed=discord.Embed(color=0xf3ff3e)
        embed.set_author(name="3e & OCE Melee Hub Server Fund", url="https://www.buymeacoffee.com/ratdog", icon_url="https://cdn.buymeacoffee.com/uploads/profile_pictures/2023/03/apwYSl9ouoxVE1Rf.jpg@300w_0e.webp")
        embed.set_footer(text="Thank you to our donors from the 3e & OCE Melee Hub.")
        await welcomeChannel.send(embed=embed)

    #Post rules
    @commands.has_any_role(
        772921452135055360
    )
    @commands.guild_only()
    @commands.cooldown(1, 10, commands.BucketType.guild)
    @commands.command(aliases=["regimentRules"])
    async def regimentrules(self, ctx):
        rulesChannel = self.bot.get_channel(772920947912736818)
        await rulesChannel.send(file=discord.File('/home/container/files/rules.png'))
        await rulesChannel.send('**Violation of this code may result in a removal from the regiment depending on the severity.** \n\n:one: Act in a mature, respectful and professional manner at all times - this includes in-game chat. Trolling will not be tolerated at any time. \n\n:two: The 3e does not have an attendance policy. However, all members are encouraged to attend events where possible - please refer to the <#772921029550931989>. \n\n:three: Training, War Games, and any other regimental event is to be taken seriously. Any other mentality will not be tolerated as it wastes time. \n\n:four: Ensure your in-game name is formatted exactly as it appears on Discord. \n\n:five: Follow the Chain of Command at all times. \n\n:six: Never intentionally teamwound or teamkill. If you do so, apologise at the earliest safe break in combat.  \n\n:seven: Ensure you are lined up properly before live. \n\n:eight: Politics and all political related chat must be kept exclusive to the politics text channel or voice-chat. Remember to abide by Discord Terms of Service. \n\n:nine: The regiment is only as strong as the weakest link. Make new members feel welcome, and assist them in gaining important skills. \n\n:keycap_ten: Keep personal problems, disputes regarding event administration, and any type of drama inside the regiment. If you have a serious issue, take it up with an officer privately.\n\n**A list of Officers can be found in the <#961650074268618813> channel.**')

    #Post ranks
    @commands.has_any_role(
        772921452135055360, 772921453095944203
    )
    @commands.guild_only()
    @commands.cooldown(1, 10, commands.BucketType.guild)
    @commands.command(aliases=["regimentRanks"])
    async def regimentranks(self, ctx):
        ranksChannel = self.bot.get_channel(772920969458614272)
        await ranksChannel.send(file=discord.File('/home/container/files/ranks.png'))
        await ranksChannel.send('**The 3e rank structure is designed such that each member has the opportunity to hold a rank which takes into account their preferred playstyle, and time commitment.**')
        await ranksChannel.send(file=discord.File('/home/container/files/high_ranks.png'))
        await ranksChannel.send(file=discord.File('/home/container/files/specialist_ranks.png'))
        await ranksChannel.send(file=discord.File('/home/container/files/enlisted_ranks.png'))
        await ranksChannel.send(file=discord.File('/home/container/files/rank_progression.png'))
        await ranksChannel.send(file=discord.File('/home/container/files/table_requirements.png'))
        await ranksChannel.send(file=discord.File('/home/container/files/table_description.png'))

    #Post event schedule
    @commands.has_any_role(
        772921452135055360
    )
    @commands.guild_only()
    @commands.cooldown(1, 10, commands.BucketType.guild)
    @commands.command(aliases=["eventSchedule"])
    async def eventschedule(self, ctx):
        eventscheduleChannel = self.bot.get_channel(772921029550931989)
        await eventscheduleChannel.send(file=discord.File('/home/container/files/schedule.png'))
        await eventscheduleChannel.send('**Note:** Event reminders are posted in <#927893298486603776>. South-East Asian events are attended on a casual basis - receive notifications for these events by obtaining <@&970256306046918676> in <#801687314736349186>.\n\n:flag_au: **__Wednesday__** :flag_nz:\n<t:1712743200:t> | *"Scrub Night" Line Battle*\n\n:flag_au: **__Friday__** :flag_nz:\n<t:1712914200:t> | *War Games*\n\n<t:1712916000:t> | *Line Battle*\n\n:flag_au: **__Saturday__** :flag_nz:\n<t:1712998800:t> | *Training*\n\n<t:1713002400:t> | *Line Battle*\n\n\n<:SEAEvent:1000298069629349969>__South-East Asian Events__<:SEAEvent:1000298069629349969>\n*Sunday SEA Event*\n<t:1713096000:t>')

     #Post enlistment office form
    @commands.has_any_role(
        772921452135055360, 772921453095944203
    )
    @commands.guild_only()
    @commands.cooldown(1, 10, commands.BucketType.guild)
    @commands.command(aliases=["enlistmentOffice"])
    async def enlistmentoffice(self, ctx):
        enlistmentChannel = self.bot.get_channel(801687726356824075)
        await enlistmentChannel.send(file=discord.File('/home/container/files/enlistment.png'))
        await enlistmentChannel.send('**Copy/Paste the following format below, answering each question to enlist in the 3e:**\n```**What is your in-game name?**\n**Have you read and do you agree to follow our Regiment Rules?**\n**Are you aged 13 years or older?**\n**Are you currently in a different Holdfast regiment? If so, which one?**\n**How did you find the 3e?**\n**What region are you from?**\n**What platform are you on (PC / Xbox / Playstation)?**\n@Officer Corps```\n**Need help?** Just <@&772921877953904661> in this channel and you will be assisted.')

     #Post suggestion box
    @commands.has_any_role(
        772921452135055360
    )
    @commands.guild_only()
    @commands.cooldown(1, 10, commands.BucketType.guild)
    @commands.command(aliases=["suggestionBox"])
    async def suggestionbox(self, ctx):
        suggestionChannel = self.bot.get_channel(881363079756144691)
        await suggestionChannel.send(file=discord.File('/home/container/files/suggestion.png'))
        await suggestionChannel.send('In hopes of having more of an organised set of suggestions and feedback for the officer corps; this channel has been made available for all members of the 3e to make suggestions for the benefit of the regiment.\n\n:pencil: **__How to make a Suggestion__**\n\n:one: Post a suggestion by typing !suggest followed by your suggestion e.g. ``!suggest more melee training``. You will be messaged by a bot informing you that your message has been deleted and that your suggestion has been sent through.\n\n:two: Your suggestion will remain in the channel until reviewed by Officers.\n\n**Note:** Suggestions are anonymous only **after** posting.')

     #Post Medals
    @commands.has_any_role(
        772921452135055360, 772921453095944203
    )
    @commands.guild_only()
    @commands.cooldown(1, 10, commands.BucketType.guild)
    @commands.command(aliases=["Medals"])
    async def medals(self, ctx):
        medalsChannel = self.bot.get_channel(772921078095937567)
        await medalsChannel.send(file=discord.File('/home/container/files/medals.png'))
        # Infanterie Medals Title ----------------------------------------------------
        infmedalsEmbed=discord.Embed(title="Infanterie Medals", description="", color=0xff0000)
        infmedalsEmbed.set_thumbnail(url="https://cdn.discordapp.com/attachments/847486338685206528/950004623207465001/unknown.png")

        # Infanterie Medals ----------------------------------------------------
        pourlemeriteEmbed=discord.Embed(description="Obtain 8 or more kills in a single line battle round.\n<@&772928362280517653>", color=0xfd8282)
        pourlemeriteEmbed.set_author(name="Pour le Merite", icon_url="https://images.emojiterra.com/twitter/512px/1f396.png")

        dieliketherestEmbed=discord.Embed(description="Kill any enemy officer.\n<@&772929237136965653>", color=0xfd8282)
        dieliketherestEmbed.set_author(name="Die Like the Rest", icon_url="https://images.emojiterra.com/twitter/512px/1f396.png")

        tisbutascratchEmbed=discord.Embed(description="Survive a round with an empty health bar.\n<@&772931210820976651>", color=0xfd8282)
        tisbutascratchEmbed.set_author(name="Tis But a Scratch", icon_url="https://images.emojiterra.com/twitter/512px/1f396.png")

        supremacymedalEmbed=discord.Embed(description="Finish a round of a line battle first on the leaderboard.\n<@&772931937476018177>", color=0xfd8282)
        supremacymedalEmbed.set_author(name="3e Supremacy", icon_url="https://images.emojiterra.com/twitter/512px/1f396.png")

        clenchEmbed=discord.Embed(description="Be the soul survivor when the rest of your line has been wiped out in a volley.\n<@&772932036746149948>", color=0xfd8282)
        clenchEmbed.set_author(name="Clench", icon_url="https://images.emojiterra.com/twitter/512px/1f396.png")

        eyeforaneyeEmbed=discord.Embed(description="Kill the same player who had killed you or someone else in your line previously, in the same event.\n<@&1003631109432680478>", color=0xfd8282)
        eyeforaneyeEmbed.set_author(name="Eye for an Eye", icon_url="https://images.emojiterra.com/twitter/512px/1f396.png")

        leadoversteelEmbed=discord.Embed(description="Shoot and kill most of a line charging your own line.\n<@&1003632642996064298>", color=0xfd8282)
        leadoversteelEmbed.set_author(name="Lead > Steel", icon_url="https://images.emojiterra.com/twitter/512px/1f396.png")

        firstbloodEmbed=discord.Embed(description="Get the first kill on your team for the round.\n<@&1003638134921252904>", color=0xfd8282)
        firstbloodEmbed.set_author(name="First Blood", icon_url="https://images.emojiterra.com/twitter/512px/1f396.png")

        whymeEmbed=discord.Embed(description="Be the first to die on your team in the round.\n<@&1003639875070869514>", color=0xfd8282)
        whymeEmbed.set_author(name="Why me...", icon_url="https://images.emojiterra.com/twitter/512px/1f396.png")

        ruthlessEmbed=discord.Embed(description="Achieve 16 or more kills as a unit.\n*Awarded to everyone in the line*.\n<@&1003640669107138601>", color=0xfd8282)
        ruthlessEmbed.set_author(name="Ruthless", icon_url="https://images.emojiterra.com/twitter/512px/1f396.png")

        builtdifferentEmbed=discord.Embed(description="Obtain at least double the amount of points as the first player on the enemy team.\n<@&1003642353124380712>", color=0xfd8282)
        builtdifferentEmbed.set_author(name="3e Built Different", icon_url="https://images.emojiterra.com/twitter/512px/1f396.png")

        specsaversEmbed=discord.Embed(description="Accidentally shoot your own team mate.\n*Will not be awarded for intentional teamkills.*\n<@&1003634330251300904>", color=0xfd8282)
        specsaversEmbed.set_author(name="Should've gone to Specsavers...", icon_url="https://images.emojiterra.com/twitter/512px/1f396.png")

        knucklesEmbed=discord.Embed(description="Punch the last player to death.\n<@&1003643053979992064>", color=0xfd8282)
        knucklesEmbed.set_author(name="Knuckles", icon_url="https://images.emojiterra.com/twitter/512px/1f396.png")
        
        hardcoreenlistedEmbed=discord.Embed(description="Finish all 5 rounds of an event in 1st place on the scoreboard.\n<@&1241680967157157938>", color=0xfd8282)
        hardcoreenlistedEmbed.set_author(name="Hardcore Enlisted", icon_url="https://images.emojiterra.com/twitter/512px/1f396.png")

        # Garde Medals Title ------------------------------------------------------------------------------------------------------
        gardemedalsEmbed=discord.Embed(title="Garde Medals", description="", color=0x810505)
        gardemedalsEmbed.set_thumbnail(url="https://media.discordapp.net/attachments/960873839036887061/1148913727953961040/image.png")
        # Garde Medals ------------------------------------------------------------------------------------------------------------
        sabreEmbed=discord.Embed(description="Obtain 2 kills with your Sabre in a single round.\n<@&1132544038441074748>", color=0xb20b0b)
        sabreEmbed.set_author(name="Sabre Connoisseur", icon_url="https://images.emojiterra.com/twitter/512px/1f396.png")

        gardeimperialeEmbed=discord.Embed(description="Obtain 5 melee Kills in a single round.\n<@&1148913866361819207>", color=0xb20b0b)
        gardeimperialeEmbed.set_author(name="Garde Imperiale", icon_url="https://images.emojiterra.com/twitter/512px/1f396.png")

        rodetoruinEmbed=discord.Embed(description="Kill 3 Enemy Cavalry in a single round (includes HQ scouts)\n<@&1148915957398523925>", color=0xb20b0b)
        rodetoruinEmbed.set_author(name="Rode to Ruin", icon_url="https://images.emojiterra.com/twitter/512px/1f396.png")

        musketeerEmbed=discord.Embed(description="Obtain 3 kills via shooting in a single round\n<@&1148918057591394334>", color=0xb20b0b)
        musketeerEmbed.set_author(name="Musketeer", icon_url="https://images.emojiterra.com/twitter/512px/1f396.png")
        
        elitemusketeerEmbed=discord.Embed(description="Obtain 5 kills via shooting in a single round\n<@&1299985991422971904>", color=0xb20b0b)
        elitemusketeerEmbed.set_author(name="Elite Musketeer", icon_url="https://images.emojiterra.com/twitter/512px/1f396.png")

        # Skirm Medals Title ------------------------------------------------------------------------------------------------------
        skirmmedalsEmbed=discord.Embed(title="Legere Medals", description="", color=0xf2e442)
        skirmmedalsEmbed.set_thumbnail(url="https://cdn.discordapp.com/attachments/846669911812210698/1015533371264344064/unknown.png")
        # Skirm Medals ------------------------------------------------------------------------------------------------------------
        itscalledstealthEmbed=discord.Embed(description="Survive until force charge, two rounds in a row.\n<@&910758087361712128>", color=0xeee8a1)
        itscalledstealthEmbed.set_author(name="I wasn't hiding, it's called stealth", icon_url="https://images.emojiterra.com/twitter/512px/1f396.png")

        expertmarksmanEmbed=discord.Embed(description="Kill 5 or more enemies in a single round.\n<@&910758274629009418>", color=0xeee8a1)
        expertmarksmanEmbed.set_author(name="Expert Marksman", icon_url="https://images.emojiterra.com/twitter/512px/1f396.png")

        aimtrueEmbed=discord.Embed(description="Headshot two enemy officers in a single round.\n<@&910756810632343593>", color=0xeee8a1)
        aimtrueEmbed.set_author(name="Aim True", icon_url="https://images.emojiterra.com/twitter/512px/1f396.png")

        zaitsevEmbed=discord.Embed(description="Achieve at least 700 points in a single round.\n<@&910756995974459433>", color=0xeee8a1)
        zaitsevEmbed.set_author(name="Vasily Zaitsev", icon_url="https://images.emojiterra.com/twitter/512px/1f396.png")
        
        headshotEmbed=discord.Embed(description="Headshot 3 enemies in a single round.\n<@&1299984844855447686>", color=0xeee8a1)
        headshotEmbed.set_author(name="Head Hunter", icon_url="https://images.emojiterra.com/twitter/512px/1f396.png")

        # Cav Medals Title ------------------------------------------------------------------------------------------------------
        cavmedalsEmbed=discord.Embed(title="Cavalerie Medals", description="", color=0xcf9704)
        cavmedalsEmbed.set_thumbnail(url="https://cdn.discordapp.com/attachments/960873839036887061/1182518293832146995/image.png?ex=6584fcfb&is=657287fb&hm=afb1942e2f5dc7edd47b8679d06e4b5970921e106c09a68d0fadf3ed6f019ccd&")
        # Cav Medals ------------------------------------------------------------------------------------------------------
        whataclutchEmbed=discord.Embed(description="Wipe the rest of an enemy line as the last remaining cavalry.\n<@&1015950224944013352>", color=0xddc890)
        whataclutchEmbed.set_author(name="What a Clutch", icon_url="https://images.emojiterra.com/twitter/512px/1f396.png")

        trustisthekeyEmbed=discord.Embed(description="Wipe out an entire enemy line without losing any cavalry.\n<@&1015950744035270666>", color=0xddc890)
        trustisthekeyEmbed.set_author(name="Team Work makes the Dream Work", icon_url="https://images.emojiterra.com/twitter/512px/1f396.png")

        imnumberoneEmbed=discord.Embed(description="Obtain double the amount of kills than the first player on the enemy team.\n<@&1015950941075296307>", color=0xddc890)
        imnumberoneEmbed.set_author(name="I'm Number One!", icon_url="https://images.emojiterra.com/twitter/512px/1f396.png")

        ghostriderEmbed=discord.Embed(description="Survive until force charge (or the end of a round) on a horse with an empty health bar.\n<@&1015951080175185930>", color=0xddc890)
        ghostriderEmbed.set_author(name="Ghost Rider", icon_url="https://images.emojiterra.com/twitter/512px/1f396.png")

        themongolianEmbed=discord.Embed(description="Obtain 4 kills by shooting the enemy in a single round.\n<@&1148911940584874015>", color=0xddc890)
        themongolianEmbed.set_author(name="THE Mongolian", icon_url="https://images.emojiterra.com/twitter/512px/1f396.png")

        # Artillerie Medals Title ------------------------------------------------------------------------------------------------------
        artymedalsEmbed=discord.Embed(title="Artillerie Medals", description="", color=0x1e21dc)
        artymedalsEmbed.set_thumbnail(url="https://cdn.discordapp.com/attachments/846669911812210698/1015535128958730251/unknown.png")
        # Artillerie Medals  ------------------------------------------------------------------------------------------------------
        grandbombardierEmbed=discord.Embed(description="Eliminate 5 or more enemy players with a single cannon shot.\n<@&772932119877517362>", color=0x7879e5)
        grandbombardierEmbed.set_author(name="Grand Bombardier", icon_url="https://images.emojiterra.com/twitter/512px/1f396.png")

        chimneysweepEmbed=discord.Embed(description="Kill an enemy at a distance of less than 5 m with round shot.\n<@&772932461923139595>", color=0x7879e5)
        chimneysweepEmbed.set_author(name="Chimney Sweep", icon_url="https://images.emojiterra.com/twitter/512px/1f396.png")

        unrelentingbarrageEmbed=discord.Embed(description="Obtain 10 or more kills with any artillery piece(s) in a single line battle round.\n<@&772932588729270302>", color=0x7879e5)
        unrelentingbarrageEmbed.set_author(name="Unrelenting Barrage", icon_url="https://images.emojiterra.com/twitter/512px/1f396.png")

        ramitralphEmbed=discord.Embed(description="Obtain 2 or more kills in a single round using a ramrod.\n<@&910495447095857194>", color=0x7879e5)
        ramitralphEmbed.set_author(name="Ram it Ralph", icon_url="https://images.emojiterra.com/twitter/512px/1f396.png")

        siryourpackageEmbed=discord.Embed(description="Kill just a single player with round shot.\n<@&1003634796737605682>", color=0x7879e5)
        siryourpackageEmbed.set_author(name="Sir, your package", icon_url="https://images.emojiterra.com/twitter/512px/1f396.png")

        finderskeepersEmbed=discord.Embed(description="Steal an enemy cannon.\n<@&1003635610348703844>", color=0x7879e5)
        finderskeepersEmbed.set_author(name="Finders Keepers", icon_url="https://images.emojiterra.com/twitter/512px/1f396.png")

        myvirginsifyoupleaseEmbed=discord.Embed(description="As a sapper, kill 2 or more enemies with a shovel.\n<@&772933962255433728>", color=0x7879e5)
        myvirginsifyoupleaseEmbed.set_author(name="My Virgins, If you Please", icon_url="https://images.emojiterra.com/twitter/512px/1f396.png")

        # Aux Medals Title ------------------------------------------------------------------------------------------------------
        supportmedalsEmbed=discord.Embed(title="Auxiliary Staff Medals", description="", color=0x620db1)
        supportmedalsEmbed.set_thumbnail(url="https://media.discordapp.net/attachments/960873839036887061/1148913007791964262/image.png")
        # Support Medals ------------------------------------------------------------------------------------------------------
        healinghandEmbed=discord.Embed(description="As a surgeon, acquire 600+ points  in a single line battle round.\n<@&772933588333232140>", color=0x9a82b0)
        healinghandEmbed.set_author(name="Healing Hand", icon_url="https://images.emojiterra.com/twitter/512px/1f396.png")

        dyinghandEmbed=discord.Embed(description="As a surgeon, die while healing another player.\n<@&1003637390751051826>", color=0x9a82b0)
        dyinghandEmbed.set_author(name="Dying Hand", icon_url="https://images.emojiterra.com/twitter/512px/1f396.png")

        poorprognosisEmbed=discord.Embed(description="As a surgeon, obtain 5 or more kills in a single round.\n<@&1003636852294697061>", color=0x9a82b0)
        poorprognosisEmbed.set_author(name="Poor Prognosis", icon_url="https://images.emojiterra.com/twitter/512px/1f396.png")

        hitemwithpatriotismEmbed=discord.Embed(description="As a Flag Bearer, kill 2 or more enemies with a flag.\n<@&772934135655694347>", color=0x9a82b0)
        hitemwithpatriotismEmbed.set_author(name="Hit 'Em with Patriotism", icon_url="https://images.emojiterra.com/twitter/512px/1f396.png")

        onlyflagsEmbed=discord.Embed(description="As a Flag Bearer, slay an enemy flag-bearer using your flag.\n<@&1182504893471260712>", color=0x9a82b0)
        onlyflagsEmbed.set_author(name="OnlyFlags", icon_url="https://images.emojiterra.com/twitter/512px/1f396.png")

        dontstopbelievingEmbed=discord.Embed(description="As a Musician, get on the end of round leaderboard without getting any kills.\n<@&1182501582395428904>", color=0x9a82b0)
        dontstopbelievingEmbed.set_author(name="Don't Stop Believin'", icon_url="https://images.emojiterra.com/twitter/512px/1f396.png")

        onionEmbed=discord.Embed(description="As a Musician, get at least 300 points.\n<@&1182503557790969916>", color=0x9a82b0)
        onionEmbed.set_author(name="Chanson de l'Oignon", icon_url="https://images.emojiterra.com/twitter/512px/1f396.png")
        
        rocketmanEmbed=discord.Embed(description="Achieve 5+ kills in one round using rockets.\n<@&1388038131093082242>", color=0x9a82b0)
        rocketmanEmbed.set_author(name="Rocket Man", icon_url="https://images.emojiterra.com/twitter/512px/1f396.png")
        
        redcrossEmbed=discord.Embed(description="For those members who have achieved all of the Auxiliary Medals, or have been long-standing, formative members of the Auxiliary.\n<@&1387422882140917854>", color=0x9a82b0)
        redcrossEmbed.set_author(name="Red Cross", icon_url="https://images.emojiterra.com/twitter/512px/1f396.png")

        # Officer Medals Title ------------------------------------------------------------------------------------------------------
        officermedalsEmbed=discord.Embed(title="Officer Medals", description="", color=0x209de4)
        officermedalsEmbed.set_thumbnail(url="https://cdn.discordapp.com/attachments/846669911812210698/1015541675466166332/unknown.png")
        # Officer Medals ------------------------------------------------------------------------------------------------------
        grandtacticianEmbed=discord.Embed(description="Awarded to an Officer that secures 3 consecutive victories in a line battle.\n<@&772934262566682624>", color=0xa2cde6)
        grandtacticianEmbed.set_author(name="Grand Tactician", icon_url="https://images.emojiterra.com/twitter/512px/1f396.png")

        assaultdoctrineEmbed=discord.Embed(description="Awarded to an Officer that successfully eliminates an enemy line without sustaining a single casualty to their line.\n<@&772934390970843166>", color=0xa2cde6)
        assaultdoctrineEmbed.set_author(name="Assault Doctrine", icon_url="https://images.emojiterra.com/twitter/512px/1f396.png")

        wehavemoremenEmbed=discord.Embed(description="As an Officer, successfully command your line to overrun and slay an enemy line in melee.\n<@&772934634534469653>", color=0xa2cde6)
        wehavemoremenEmbed.set_author(name="We have more men than you have bullets!", icon_url="https://images.emojiterra.com/twitter/512px/1f396.png")

        againstalloddsEmbed=discord.Embed(description="As an Officer, stop a cavalry charge without losing any troops.\n<@&1003633857830076487>", color=0xa2cde6)
        againstalloddsEmbed.set_author(name="Against All Odds", icon_url="https://images.emojiterra.com/twitter/512px/1f396.png")

        # Bonus Medals Title ------------------------------------------------------------------------------------------------------
        bonusmedalsEmbed=discord.Embed(title="Bonus Medals", description="", color=0x682105)
        bonusmedalsEmbed.set_thumbnail(url="https://cdn.discordapp.com/attachments/846669911812210698/1015920295376326667/unknown.png")
        # Bonus Medals ------------------------------------------------------------------------------------------------------
        recruitmentmedalEmbed=discord.Embed(description="Awarded to a member that recruits 5 players within a week.\n<@&772935148021743637>", color=0x644d43)
        recruitmentmedalEmbed.set_author(name="Recruitment Medal", icon_url="https://images.emojiterra.com/twitter/512px/1f396.png")

        clutchEmbed=discord.Embed(description="Awarded to a member who, as the last surviving player wins the round fighting 3 or more enemies.\n<@&772935250522800129>", color=0x644d43)
        clutchEmbed.set_author(name="Clutch Medal", icon_url="https://images.emojiterra.com/twitter/512px/1f396.png")

        fourdchessEmbed=discord.Embed(description="While being the last one alive, get 3 or more enemies to team kill each other.\n<@&772935536293576734>", color=0x644d43)
        fourdchessEmbed.set_author(name="4D Chess", icon_url="https://images.emojiterra.com/twitter/512px/1f396.png")

        servicecrossEmbed=discord.Embed(description="Awarded to members who have attended at least 75 line battles.\n<@&1003642674873651260>", color=0x644d43)
        servicecrossEmbed.set_author(name="Service Cross", icon_url="https://images.emojiterra.com/twitter/512px/1f396.png")
        
        servicecross200Embed=discord.Embed(description="Awarded to members who have attended at least 200 line battles.\n<@&1299988766831935508>", color=0x644d43)
        servicecross200Embed.set_author(name="Service Cross 200", icon_url="https://images.emojiterra.com/twitter/512px/1f396.png")
        
        servicecross300Embed=discord.Embed(description="Awarded to members who have attended at least 300 line battles.\n<@&1299988796410036266>", color=0x644d43)
        servicecross300Embed.set_author(name="Service Cross 300", icon_url="https://images.emojiterra.com/twitter/512px/1f396.png")
        
        servicecross400Embed=discord.Embed(description="Awarded to members who have attended at least 400 line battles.\n<@&1299989565280485376>", color=0x644d43)
        servicecross400Embed.set_author(name="Service Cross 400", icon_url="https://images.emojiterra.com/twitter/512px/1f396.png")

        jacksoncrossEmbed=discord.Embed(description="Awarded to members who have successfully received all medals, or otherwise issued for extremely special displays of abilities. This medal is named after a previous leader of the regiment.\n<@&772935853076643840>", color=0x644d43)
        jacksoncrossEmbed.set_author(name="Jackson Cross", icon_url="https://images.emojiterra.com/twitter/512px/1f396.png")

        # Ribbons ------------------------------------------------------------------------------------------------------
        ribbonsEmbed=discord.Embed(title="Ribbons", description="", color=0xf0ea14)
        ribbonsEmbed.set_thumbnail(url="https://images.emojiterra.com/twitter/512px/1f396.png")

        marksmanribbonsEmbed=discord.Embed(title="Marksman Ribbons", description="", color=0xf3f1b5)
        marksmanribbonsEmbed.set_thumbnail(url="https://cdn.discordapp.com/attachments/846669911812210698/1015931151803764746/unknown.png")
        marksmanribbonsEmbed.add_field(name="100 m - 124.9 m Kill", value="<@&772935922345181235>", inline=False)
        marksmanribbonsEmbed.add_field(name="125 m - 149.9 m Kill", value="<@&772936039479246878>", inline=False)
        marksmanribbonsEmbed.add_field(name="150 m - 174.9 m Kill", value="<@&772936113190731786>", inline=False)
        marksmanribbonsEmbed.add_field(name="175 m - 199.9 m Kill", value="<@&772936127358304266>", inline=False)
        marksmanribbonsEmbed.add_field(name="200 m+ Kill", value="<@&772936128096763954>", inline=False)
        marksmanribbonsEmbed.add_field(name="Attainment of all Marksman Ribbons", value="<@&772936128399540234>", inline=False)

        scorerribbonsEmbed=discord.Embed(title="Scorer Ribbons", description="", color=0xf3f1b5)
        scorerribbonsEmbed.set_thumbnail(url="https://images.emojiterra.com/google/android-10/512px/1f3c6.png")
        scorerribbonsEmbed.add_field(name="Score 200 - 399 points in a Line Battle", value="<@&772936129493991515>", inline=False)
        scorerribbonsEmbed.add_field(name="Score 400 - 599 points in a Line Battle", value="<@&772936505357762591>", inline=False)
        scorerribbonsEmbed.add_field(name="Score 600 - 799 points in a Line Battle", value="<@&772936506130169868>", inline=False)
        scorerribbonsEmbed.add_field(name="Score 800 - 999 points in a Line Battle", value="<@&772936507245068308>", inline=False)
        scorerribbonsEmbed.add_field(name="Score 1000+ points in a Line Battle", value="<@&772936508272803850>", inline=False)
        scorerribbonsEmbed.add_field(name="Attainment of all Scorer Ribbons", value="<@&772936509313515550>", inline=False)

        # Pub Awards --------------------------------------------------------------------------------------------------
        pubawardsEmbed=discord.Embed(title="Pub Awards", description="The following awards can only be achieved on Official Holdfast Public Servers.", color=0x9f03a4)
        pubawardsEmbed.set_thumbnail(url="https://cdn.discordapp.com/attachments/846669911812210698/1015935782873202698/unknown.png")

        xpawardsEmbed=discord.Embed(title="XP Awards", description="In a single round, achieve...", color=0xa388a4)
        xpawardsEmbed.add_field(name="5,000 points", value="<@&820099098132742185>", inline=False)
        xpawardsEmbed.add_field(name="4,000 points", value="<@&820100608521404437>", inline=False)
        xpawardsEmbed.add_field(name="3,000 points", value="<@&820100610954625054>", inline=False)
        xpawardsEmbed.add_field(name="2,000 points", value="<@&820100613517344800>", inline=False)
        xpawardsEmbed.add_field(name="1,000 points", value="<@&820100616280866836>", inline=False)
        xpawardsEmbed.add_field(name="2,000 points without getting any kills", value="<@&820100621230538792>", inline=False)

        killawardsEmbed=discord.Embed(title="Kill Awards", description="In a single round, achieve...", color=0xa388a4)
        killawardsEmbed.add_field(name="50 kills", value="<@&820100617996730378>", inline=False)
        killawardsEmbed.add_field(name="40 kills", value="<@&820100618521411646>", inline=False)
        killawardsEmbed.add_field(name="30 kills", value="<@&820100619585978419>", inline=False)
        killawardsEmbed.add_field(name="20 kills", value="<@&820100620425232405>", inline=False)
        killawardsEmbed.add_field(name="10 kills", value="<@&820100620459049010>", inline=False)
        killawardsEmbed.add_field(name="1 kill from > 200 m (artillery does not count)", value="<@&820107316736950283>", inline=False)

        challengeawardsEmbed=discord.Embed(title="Challenges", description="Extra Challenges for Public Servers", color=0xa388a4)
        challengeawardsEmbed.add_field(name="1st, 2nd and 3rd taken by 3e members", value="<@&1182508921240440942>", inline=False)
        challengeawardsEmbed.add_field(name="Kill a 3e member", value="<@&1182509572267716659>", inline=False)
        challengeawardsEmbed.add_field(name="Kill 5 or more Enemies with an Explosive Barrel at once", value="<@&1182510008013959241>", inline=False)
        challengeawardsEmbed.add_field(name="As Cavalry, finish the round in the Top 5", value="<@&1182510172699107378>", inline=False)
        challengeawardsEmbed.add_field(name="Kill 5 or more players with one swivel shot", value="<@&1182510886892605470>", inline=False)
        challengeawardsEmbed.add_field(name="Form a marching band with 3 other 3e Members", value="<@&1182511927642050560>", inline=False)
        challengeawardsEmbed.add_field(name="As Light Infantry or Rifleman, get a headshot from at least 100 m", value="<@&1182512195628707850>", inline=False)

        # Medal Application
        medalapplicationEmbed=discord.Embed(title="Medal Submission", description="Claim your Medals, Ribbons and Awards by copy and pasting the medal application form below!", color=0xffffff)
        medalapplicationEmbed.set_thumbnail(url="https://emojipedia-us.s3.amazonaws.com/source/microsoft-teams/337/clipboard_1f4cb.png")

        await medalsChannel.send(embed=infmedalsEmbed)
        await medalsChannel.send(embed=pourlemeriteEmbed)
        await medalsChannel.send(embed=dieliketherestEmbed)
        await medalsChannel.send(embed=tisbutascratchEmbed)
        await medalsChannel.send(embed=supremacymedalEmbed)
        await medalsChannel.send(embed=clenchEmbed)
        await medalsChannel.send(embed=eyeforaneyeEmbed)
        await medalsChannel.send(embed=leadoversteelEmbed)
        await medalsChannel.send(embed=firstbloodEmbed)
        await medalsChannel.send(embed=whymeEmbed)
        await medalsChannel.send(embed=ruthlessEmbed)
        await medalsChannel.send(embed=builtdifferentEmbed)
        await medalsChannel.send(embed=specsaversEmbed)
        await medalsChannel.send(embed=knucklesEmbed)
        await medalsChannel.send(embed=hardcoreenlistedEmbed)
        await medalsChannel.send(embed=gardemedalsEmbed)
        await medalsChannel.send(embed=sabreEmbed)
        await medalsChannel.send(embed=gardeimperialeEmbed)
        await medalsChannel.send(embed=rodetoruinEmbed)
        await medalsChannel.send(embed=musketeerEmbed)
        await medalsChannel.send(embed=elitemusketeerEmbed)
        await medalsChannel.send(embed=skirmmedalsEmbed)
        await medalsChannel.send(embed=itscalledstealthEmbed)
        await medalsChannel.send(embed=expertmarksmanEmbed)
        await medalsChannel.send(embed=aimtrueEmbed)
        await medalsChannel.send(embed=zaitsevEmbed)
        await medalsChannel.send(embed=headshotEmbed)
        await medalsChannel.send(embed=cavmedalsEmbed)
        await medalsChannel.send(embed=whataclutchEmbed)
        await medalsChannel.send(embed=trustisthekeyEmbed)
        await medalsChannel.send(embed=imnumberoneEmbed)
        await medalsChannel.send(embed=ghostriderEmbed)
        await medalsChannel.send(embed=themongolianEmbed)
        await medalsChannel.send(embed=artymedalsEmbed)
        await medalsChannel.send(embed=grandbombardierEmbed)
        await medalsChannel.send(embed=chimneysweepEmbed)
        await medalsChannel.send(embed=unrelentingbarrageEmbed)
        await medalsChannel.send(embed=ramitralphEmbed)
        await medalsChannel.send(embed=siryourpackageEmbed)
        await medalsChannel.send(embed=finderskeepersEmbed)
        await medalsChannel.send(embed=myvirginsifyoupleaseEmbed)
        await medalsChannel.send(embed=supportmedalsEmbed)
        await medalsChannel.send(embed=healinghandEmbed)
        await medalsChannel.send(embed=dyinghandEmbed)
        await medalsChannel.send(embed=poorprognosisEmbed)
        await medalsChannel.send(embed=hitemwithpatriotismEmbed)
        await medalsChannel.send(embed=onlyflagsEmbed)
        await medalsChannel.send(embed=dontstopbelievingEmbed)
        await medalsChannel.send(embed=onionEmbed)
        await medalsChannel.send(embed=rocketmanEmbed)
        await medalsChannel.send(embed=redcrossEmbed)
        await medalsChannel.send(embed=officermedalsEmbed)
        await medalsChannel.send(embed=grandtacticianEmbed)
        await medalsChannel.send(embed=assaultdoctrineEmbed)
        await medalsChannel.send(embed=wehavemoremenEmbed)
        await medalsChannel.send(embed=againstalloddsEmbed)
        await medalsChannel.send(embed=bonusmedalsEmbed)
        await medalsChannel.send(embed=recruitmentmedalEmbed)
        await medalsChannel.send(embed=clutchEmbed)
        await medalsChannel.send(embed=fourdchessEmbed)
        await medalsChannel.send(embed=servicecrossEmbed)
        await medalsChannel.send(embed=servicecross200Embed)
        await medalsChannel.send(embed=servicecross300Embed)
        await medalsChannel.send(embed=servicecross400Embed)
        await medalsChannel.send(embed=jacksoncrossEmbed)
        await medalsChannel.send(embed=ribbonsEmbed)
        await medalsChannel.send(embed=marksmanribbonsEmbed)
        await medalsChannel.send(embed=scorerribbonsEmbed)
        await medalsChannel.send(embed=pubawardsEmbed)
        await medalsChannel.send(embed=xpawardsEmbed)
        await medalsChannel.send(embed=killawardsEmbed)
        await medalsChannel.send(embed=challengeawardsEmbed)
        await medalsChannel.send(embed=medalapplicationEmbed)
        await medalsChannel.send('*All submissions require the following format (please do not ping medals):*\n```**Medal Requested:**\n**Date/Event of Achievement:**\n**Witnesses (if applicable):**\n**Evidence:**\n@Officer Corps```')
    #Muster roll
    @commands.has_any_role(
        772921452135055360, 772921453095944203, 772921882072449075, 772921877953904661
    )
    @commands.cooldown(1, 10, commands.BucketType.guild)
    @commands.guild_only()
    @commands.command(aliases=["Muster"])
    async def muster(self, ctx):
        musterChannelId = 961650074268618813
        artyRole = ctx.guild.get_role(845614864629235712)
        skirmRole = ctx.guild.get_role(826778081531658280)
        guardRole = ctx.guild.get_role(802900303648653322)
        cavRole = ctx.guild.get_role(973152930330968094)
        supportstaffRole = ctx.guild.get_role(772922207760416829)
        soRole = ctx.guild.get_role(772921452135055360)
        coRole = ctx.guild.get_role(772921453095944203)
        ncoRole = ctx.guild.get_role(772921882072449075)
        cplRole = ctx.guild.get_role(910758407055736902)
        ocdtRole = ctx.guild.get_role(1393465069370605629)

        async with ctx.channel.typing():
            if ctx.channel.id == musterChannelId:
                async for message in ctx.channel.history(limit = 10):
                    if message is None:
                        break
                    elif message.author.bot:
                        await message.delete()

            workingMsg = await ctx.reply("Generating now...")
            #Creates functions for calculating muster roll
            def soCalc(companyRole):
                colList = []
                ltcolList = []
                majList = []
                deuxmajList = []
                cdbList = []
                captList = []
                for user in ctx.guild.members:
                    if companyRole in user.roles:
                        if soRole in user.roles:
                            if "Col. " in user.display_name:
                                nick = (user.display_name).replace("Col. ", "Colonel ")
                                colList.append(nick)
                            elif "Lt Col. " in user.display_name:
                                nick = (user.display_name).replace("Lt Col. ", "Colonel en second ")
                                ltcolList.append(nick)
                            elif "Maj. " in user.display_name:
                                nick = (user.display_name).replace("Maj. ", "Major ")
                                majList.append(nick)
                            elif "Deux-Maj. " in user.display_name:
                                nick = (user.display_name).replace("Deux-Maj. ", "Deuxieme-Major ")
                                deuxmajList.append(nick)
                            elif "CdB. " in user.display_name:
                                nick = (user.display_name).replace("CdB. ", "Chef de Battalion ")
                                cdbList.append(nick)
                            elif "Capt. " in user.display_name:
                                nick = (user.display_name).replace("Capt. ", "Capitaine ")
                                captList.append(nick)
                colList.sort()
                ltcolList.sort()
                majList.sort()
                deuxmajList.sort()
                cdbList.sort()
                captList.sort()

                soList = [colList, ltcolList, majList, cdbList, captList]
                flatSoList = [name for list in soList for name in list]

                return flatSoList

            def coCalc(companyRole):
                ltList = []
                sousltList = []
                for user in ctx.guild.members:
                    if companyRole in user.roles:
                        if coRole in user.roles:
                            if "Lt. " in user.display_name:
                                nick = (user.display_name).replace("Lt. ", "Lieutenant ")
                                ltList.append(nick)
                            elif "Sous-Lt. " in user.display_name:
                                nick = (user.display_name).replace("Sous-Lt. ", "Sous-Lieutenant ")
                                sousltList.append(nick)
                ltList.sort()
                sousltList.sort()

                coList = [ltList, sousltList]
                flatCoList = [name for list in coList for name in list]

                return flatCoList

            def ncoCalc(companyRole):
                adjList = []
                sgtmajlist = []
                sgtList = []
                for user in ctx.guild.members:
                        if companyRole in user.roles:
                            if ncoRole in user.roles:
                                if "Adj." in user.display_name:
                                    nick = (user.display_name).replace("Adj. ", "Adjutant ")
                                    adjList.append(nick)
                                elif "Sgt-Maj. " in user.display_name:
                                    nick = (user.display_name).replace("Sgt-Maj. ", "Sergeant-Major ")
                                    sgtmajlist.append(nick)
                                elif "Sgt. " in user.display_name:
                                    nick = (user.display_name).replace("Sgt. ", "Sergeant ")
                                    sgtList.append(nick)
                adjList.sort()
                sgtmajlist.sort()
                sgtList.sort()

                ncoList = [adjList, sgtmajlist, sgtList]
                flatNcoList = [name for list in ncoList for name in list]

                return flatNcoList

            def cplCalc(companyRole):
                jcplList = []
                cplList = []
                cpfList = []
                for user in ctx.guild.members:
                        if companyRole in user.roles:
                            if cplRole in user.roles:
                                if "JCpl. " in user.display_name:
                                    nick = (user.display_name).replace("JCpl. ", "Junior Caporal ")
                                    jcplList.append(nick)
                                elif "Cpl. " in user.display_name:
                                    nick = (user.display_name).replace("Cpl. ", "Caporal ")
                                    cplList.append(nick)
                                elif "CpF. " in user.display_name:
                                    nick = (user.display_name).replace("CpF. ", "Caporal-Fourrier ")
                                    cpfList.append(nick)
                            cplList.sort()
                jcplList.sort()
                cplList.sort()
                cpfList.sort()

                cplFullList = [cpfList, cplList, jcplList]
                flatCplFullList = [name for list in cplFullList for name in list]

                return flatCplFullList

            def ocdtCalc(companyRole):
                ocdtList = []
                for user in ctx.guild.members:
                        if companyRole in user.roles:
                            if ocdtRole in user.roles:
                                if "Ocdt. " in user.display_name:
                                    nick = (user.display_name).replace("Ocdt. ", "Officer Cadet ")
                                    ocdtList.append(nick)
                ocdtList.sort()

                return ocdtList

            def enlistedCalc(companyRole):
                insList = []
                chgList = []
                lcsList = []
                mscList = []
                tbrcplList = []
                pteaigleList = []
                chgmajList = []
                chefList = []
                gdrList = []
                vgrdList = []
                trlrList = []
                voltList = []
                cnrList = []
                artgList = []
                cvlrList = []
                chasList = []
                gdpList = []
                grenList = []
                fusList = []
                sdtList = []

                for user in ctx.guild.members:
                    if companyRole in user.roles:
                        if "Sdt. " in user.display_name:
                            nick = (user.display_name).replace("Sdt. ", "Soldat ")
                            sdtList.append(nick)
                        elif "Fus. " in user.display_name:
                            nick = (user.display_name).replace("Fus. ", "Fusilier ")
                            fusList.append(nick)
                        elif "Gren. " in user.display_name:
                            nick = (user.display_name).replace("Gren. ", "Grenadiere ")
                            grenList.append(nick)
                        elif "GdP. " in user.display_name:
                            nick = (user.display_name).replace("GdP. ", "Grenadiere de premiere classe ")
                            gdpList.append(nick)
                        elif "LcS. " in user.display_name:
                            nick = (user.display_name).replace("LcS. ", "Les cent Suisse ")
                            lcsList.append(nick)
                        elif "Chg. " in user.display_name:
                            nick = (user.display_name).replace("Chg. ", "Chirurgienne ")
                            chgList.append(nick)
                        elif "Ins. " in user.display_name:
                            nick = (user.display_name).replace("Ins. ", "Insigne ")
                            insList.append(nick)
                        elif "Msc. " in user.display_name:
                            nick = (user.display_name).replace("Msc. ", "Musicien ")
                            mscList.append(nick)
                        elif "Tbr-cpl. " in user.display_name:
                            nick = (user.display_name).replace("Tbr-cpl. ", "Tambour-caporal ")
                            tbrcplList.append(nick)
                        elif "Pte-aigle. " in user.display_name:
                            nick = (user.display_name).replace("Pte-aigle. ", "Porte-aigle ")
                            pteaigleList.append(nick)
                        elif "C-Maj. " in user.display_name:
                            nick = (user.display_name).replace("C-Maj. ", "Chirurgien-major ")
                            chgmajList.append(nick)
                        elif "Chg-Maj. " in user.display_name:
                            nick = (user.display_name).replace("Chg-Maj. ", "Chirurgien-major ")
                            chgmajList.append(nick)
                        elif "Chef. " in user.display_name:
                            nick = (user.display_name).replace("Chef. ", "Chef ")
                            chgmajList.append(nick)
                        elif "Gdr. " in user.display_name:
                            nick = (user.display_name).replace("Gdr. ", "Gendarmerie ")
                            gdrList.append(nick)
                        elif "VGrd. " in user.display_name:
                            nick = (user.display_name).replace("VGrd. ", "Vieille Garde ")
                            vgrdList.append(nick)
                        elif "Trlr. " in user.display_name:
                            nick = (user.display_name).replace("Trlr. ", "Tirailleur ")
                            trlrList.append(nick)
                        elif "Volt. " in user.display_name:
                            nick = (user.display_name).replace("Volt. ", "Voltigeur Elite ")
                            voltList.append(nick)
                        elif "Cnr. " in user.display_name:
                            nick = (user.display_name).replace("Cnr. ", "Canonnier ")
                            cnrList.append(nick)
                        elif "ArtG. " in user.display_name:
                            nick = (user.display_name).replace("ArtG. ", "Artillerie Gouttelettes ")
                            artgList.append(nick)
                        elif "Cvlr. " in user.display_name:
                            nick = (user.display_name).replace("Cvlr. ", "Cavalier ")
                            cvlrList.append(nick)
                        elif "Chas. " in user.display_name:
                            nick = (user.display_name).replace("Chas. ", "Chassuer-a-Cheval ")
                            chasList.append(nick)
                insList.sort()
                chgList.sort()
                mscList.sort()
                tbrcplList.sort()
                pteaigleList.sort()
                chefList.sort()
                chgmajList.sort()
                gdrList.sort()
                vgrdList.sort()
                trlrList.sort()
                voltList.sort()
                cnrList.sort()
                artgList.sort()
                cvlrList.sort()
                chasList.sort()
                lcsList.sort()
                gdpList.sort()
                grenList.sort()
                fusList.sort()
                sdtList.sort()

                enlistedList = [lcsList, chgmajList, chgList, pteaigleList, insList, tbrcplList, mscList, vgrdList, gdrList, voltList, trlrList, artgList, cnrList, chasList, cvlrList, gdpList, grenList, fusList, sdtList]
                flatEnlistedList = [name for list in enlistedList for name in list]

                return flatEnlistedList

            def enlistedCountCalc(companyRole):
                enlistedCount = 0
                for user in ctx.guild.members:
                    if companyRole in user.roles:
                        if "Sdt." in user.display_name:
                            enlistedCount += 1
                        elif "Fus. " in user.display_name:
                            enlistedCount += 1
                        elif "Gren. " in user.display_name:
                            enlistedCount += 1
                        elif "GdP. " in user.display_name:
                            enlistedCount += 1
                        elif "LcS. " in user.display_name:
                            enlistedCount += 1
                        elif "Ocdt. " in user.display_name:
                            enlistedCount += 1
                        elif "Chg. " in user.display_name:
                            enlistedCount += 1
                        elif "Ins. " in user.display_name:
                            enlistedCount += 1
                        elif "Msc. " in user.display_name:
                            enlistedCount += 1
                        elif "Chef. " in user.display_name:
                            enlistedCount += 1
                        elif "Tbr-cpl. " in user.display_name:
                            enlistedCount += 1
                        elif "Pte-aigle. " in user.display_name:
                            enlistedCount += 1
                        elif "C-Maj. " in user.display_name:
                            enlistedCount += 1
                        elif "Gdr. " in user.display_name:
                            enlistedCount += 1
                        elif "VGrd. " in user.display_name:
                            enlistedCount += 1
                        elif "Trlr. " in user.display_name:
                            enlistedCount += 1
                        elif "Volt. " in user.display_name:
                            enlistedCount += 1
                        elif "Cnr. " in user.display_name:
                            enlistedCount += 1
                        elif "ArtG. " in user.display_name:
                            enlistedCount += 1
                        elif "Cvlr. " in user.display_name:
                            enlistedCount += 1
                        elif "Chas. " in user.display_name:
                            enlistedCount += 1
                return enlistedCount

            #Stuff for creating muster roll
            companies = ["arty", "skirm", "cav", "guard", "supportstaff"]
            lists = ["So", "Co", "Nco", "Cpl", "Ocdt", "Enlisted"]
            muster = {}

            #Creates muster roll information
            for company in companies:
                if company == "arty": role = artyRole
                elif company == "skirm": role = skirmRole
                elif company == "cav": role = cavRole
                elif company == "guard": role = guardRole
                elif company == "supportstaff": role = supportstaffRole

                for list in lists:
                    if list == "So": func = soCalc
                    elif list == "Co": func = coCalc
                    elif list == "Nco": func = ncoCalc
                    elif list == "Cpl": func = cplCalc
                    elif list == "Ocdt": func = ocdtCalc
                    elif list == "Enlisted": func = enlistedCalc

                    muster[f"{company}{list}"] = func(role)
                    muster[f"{company}{list}"] = "\n".join(muster[f"{company}{list}"])

            artyEnlistedCount = enlistedCountCalc(artyRole)
            skirmEnlistedCount = enlistedCountCalc(skirmRole)
            cavEnlistedCount = enlistedCountCalc(cavRole)
            guardEnlistedCount = enlistedCountCalc(guardRole)
            supportstaffEnlistedCount = enlistedCountCalc(supportstaffRole)
            # Senior Officers Pic
            try:
                soImg = discord.File(
                    "files/seniorofficer.png",
                    filename="seniorofficer.png",
                )
            except:
                soImg = discord.File(
                    "/home/container/files/seniorofficer.png", filename="seniorofficer.png"
                )

            # CO Pic
            try:
                coImg = discord.File(
                    "files/commissionedofficer.png",
                    filename="commissionedofficer.png",
                )
            except:
                coImg = discord.File(
                    "/home/container/files/commissionedofficer.png", filename="commissionedofficer.png"
                )

            # Adj Pic
            try:
                adjImg = discord.File(
                    "files/adjutant.png",
                    filename="adjutant.png",
                )
            except:
                adjImg = discord.File(
                    "/home/container/files/adjutant.png", filename="adjutant.png"
                )

            # NCO pic
            try:
                ncoImg = discord.File(
                    "files/nco.png",
                    filename="nco.png",
                )
            except:
                ncoImg = discord.File(
                    "/home/container/files/nco.png", filename="nco.png"
                )

            # Cpl pic
            try:
                cplImg = discord.File(
                    "files/cpl.jpg",
                    filename="cpl.jpg",
                )
            except:
                cplImg = discord.File(
                    "/home/container/files/cpl.jpg", filename="cpl.jpg"
                )

            # Ocdt pic
            try:
                ocdtImg = discord.File(
                    "files/ocdt.jpg",
                    filename="ocdt.jpg",
                )
            except:
                ocdtImg = discord.File(
                    "/home/container/files/ocdt.jpg", filename="ocdt.jpg"
                )
                
            # Guards
            try:
                guardImg = discord.File(
                    "files/guard.png",
                    filename="guard.png",
                )
            except:
                guardImg = discord.File(
                    "/home/container/files/guard.png", filename="guard.png"
                )

            # Skirms
            try:
                skirmImg = discord.File(
                    "files/skirms.png",
                    filename="skirms.png",
                )
            except:
                skirmImg = discord.File(
                    "/home/container/files/skirms.png", filename="skirms.png"
                )
            # Cav
            try:
                cavImg = discord.File(
                    "files/cav.png",
                    filename="cav.png",
                )
            except:
                cavImg = discord.File(
                    "/home/container/files/cav.png", filename="cav.png"
                )

            # Arty
            try:
                artyImg = discord.File(
                    "files/arty.png",
                    filename="arty.png",
                )
            except:
                artyImg = discord.File(
                    "/home/container/files/arty.png", filename="arty.png"
                )

            # Support Staff
            try:
                supportstaffImg = discord.File(
                    "files/supportstaff.png",
                    filename="supportstaff.png",
                )
            except:
                supportstaffImg = discord.File(
                    "/home/container/files/supportstaff.png", filename="supportstaff.png"
                )
            #TODO: Automate this listing so that we don't have to update it manually everytime a position changes

            # Officers

            # Senior Officers ----------------------------------------------------
            soEmbed=discord.Embed(title="Senior Officers", description="", color=0x0d195a)
            soEmbed.set_thumbnail(url="attachment://seniorofficer.png")
            soEmbed.add_field(name="Major Shady", value="1 IC of the 3e", inline=False)
            soEmbed.add_field(name="Capitaine TANKIGAMER", value="2 IC of the 3e", inline=False)

            # Commissioned Officers ----------------------------------------------------
            coEmbed=discord.Embed(title="Commissioned Officers", description="", color=0x112074)
            coEmbed.set_thumbnail(url="attachment://commissionedofficer.png")
            coEmbed.add_field(name="Lieutenant Danx", value="Leader of the Legere", inline=False)
            coEmbed.add_field(name="Sous-Lieutenant AsianSharpe", value="Leader of the Artillerie", inline=False)

            # Adjutant Council (Disabled) ----------------------------------------------------
            #adjEmbed=discord.Embed(title="Adjutant Council", description="", color=0x2b56c8)
            #adjEmbed.set_thumbnail(url="attachment://adjutant.png")
            #adjEmbed.add_field(name="Adjutant Dayrahl", value="", inline=False)
            #adjEmbed.add_field(name="Adjutant Mugi", value="", inline=False)

            # Non-Commissioned Officers ----------------------------------------------------
            ncoEmbed=discord.Embed(title="Non-Commissioned Officers", description="", color=0x192fa7)
            ncoEmbed.set_thumbnail(url="attachment://nco.png")
            ncoEmbed.add_field(name="Sergeant Dragz", value="Leader of the Garde", inline=False)                       
            ncoEmbed.add_field(name="Sergeant Mugi", value="", inline=False)
            ncoEmbed.add_field(name="Sergeant Sparc", value="", inline=False)

            # Corporals ----------------------------------------------------
            cplEmbed=discord.Embed(title="Corporals", description="", color=0x1e39cd)
            cplEmbed.set_thumbnail(url="attachment://cpl.jpg")
            cplEmbed.add_field(name="Caporal-Fourrier Kruber", value="", inline=False)
            cplEmbed.add_field(name="Caporal-Fourrier Ganthador", value="", inline=False)
            cplEmbed.add_field(name="Caporal-Fourrier Spyro", value="", inline=False)
            cplEmbed.add_field(name="Caporal HelixOrion", value="", inline=False)
            cplEmbed.add_field(name="Caporal CaptainThunder", value="", inline=False)
            cplEmbed.add_field(name="Caporal Garat", value="", inline=False)
            cplEmbed.add_field(name="Caporal Jackson", value="", inline=False)
            cplEmbed.add_field(name="Caporal Chips", value="", inline=False)

            # Officer Cadets ----------------------------------------------------
            ocdtEmbed=discord.Embed(title="Officer Cadets", description="", color=0x2444f3)
            ocdtEmbed.set_thumbnail(url="attachment://ocdt.jpg")
            ocdtEmbed.add_field(name="Officer Cadet P4tr1ck", value="", inline=False)
            ocdtEmbed.add_field(name="Officer Cadet GamingRabbit15", value="", inline=False)
            ocdtEmbed.add_field(name="Officer Cadet AussieOrange", value="", inline=False)
            ocdtEmbed.add_field(name="Officer Cadet Fairus", value="", inline=False)
            

            # Garde ---------------------------------------------------------------------
            guardEmbed = discord.Embed(
                title="Garde",
                description="",
                color=0x860404,
            )
            guardEmbed.set_thumbnail(url="attachment://guard.png")
            list = muster.get('guardSo')
            if list and list.strip():
                guardEmbed.add_field(
                    name=f"Senior Officers", value=f"\u200b{muster['guardSo']}", inline=False
                )
                guardEmbed.add_field(
                    name=f"\u200b",
                    value=f"=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=",
                    inline=False,
                )
            list = muster.get('guardCo')
            if list and list.strip():
                guardEmbed.add_field(
                    name=f"Commissioned Officers", value=f"\u200b{muster['guardCo']}", inline=False
                )
                guardEmbed.add_field(
                    name=f"\u200b",
                    value=f"=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=",
                    inline=False,
                )
            list = muster.get('guardNco')
            if list and list.strip():
                guardEmbed.add_field(
                    name=f"Non-Commissioned Officers",
                    value=f"\u200b{muster['guardNco']}",
                    inline=False,
                )
                guardEmbed.add_field(
                    name=f"\u200b",
                    value=f"=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=",
                    inline=False,
                )
            list = muster.get('guardCpl')
            if list and list.strip():
                guardEmbed.add_field(
                    name=f"Corporals", value=f"\u200b{muster['guardCpl']}", inline=False
                )
                guardEmbed.add_field(
                    name=f"\u200b",
                    value=f"=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=",
                    inline=False,
                )
            list = muster.get('guardOcdt')
            if list and list.strip():
                guardEmbed.add_field(
                    name=f"Officer Cadets", value=f"\u200b{muster['guardOcdt']}", inline=False
                )
                guardEmbed.add_field(
                    name=f"\u200b",
                    value=f"=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=",
                    inline=False,
                )
            list = muster.get('guardEnlisted')
            if list and list.strip():
                guardEmbed.add_field(
                    name=f"Enlisted", value=f"\u200b{muster['guardEnlisted']}", inline=False
                )

            # Legere ---------------------------------------------------------------------
            skirmEmbed = discord.Embed(
                title="Legere",
                description="",
                color=0xf2e442,
            )
            skirmEmbed.set_thumbnail(url="attachment://skirms.png")
            list = muster.get('skirmSo')
            if list and list.strip():
                skirmEmbed.add_field(
                    name=f"Senior Officers", value=f"\u200b{muster['skirmSo']}", inline=False
                )
                skirmEmbed.add_field(
                    name=f"\u200b",
                    value=f"=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=",
                    inline=False,
                )
            list = muster.get('skirmCo')
            if list and list.strip():
                skirmEmbed.add_field(
                    name=f"Commissioned Officers", value=f"\u200b{muster['skirmCo']}", inline=False
                )
                skirmEmbed.add_field(
                    name=f"\u200b",
                    value=f"=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=",
                    inline=False,
                )
            list = muster.get('skirmNco')
            if list and list.strip():
                skirmEmbed.add_field(
                    name=f"Non-Commissioned Officers",
                    value=f"\u200b{muster['skirmNco']}",
                    inline=False,
                )
                skirmEmbed.add_field(
                    name=f"\u200b",
                    value=f"=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=",
                    inline=False,
                )
            list = muster.get('skirmCpl')
            if list and list.strip():
                skirmEmbed.add_field(
                    name=f"Corporals", value=f"\u200b{muster['skirmCpl']}", inline=False
                )
                skirmEmbed.add_field(
                    name=f"\u200b",
                    value=f"=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=",
                    inline=False,
                )
            list = muster.get('skirmOcdt')
            if list and list.strip():
                skirmEmbed.add_field(
                    name=f"Officer Cadets", value=f"\u200b{muster['skirmOcdt']}", inline=False
                )
                skirmEmbed.add_field(
                    name=f"\u200b",
                    value=f"=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=",
                    inline=False,
                )
            list = muster.get('skirmEnlisted')
            if list and list.strip():
                skirmEmbed.add_field(
                    name=f"Enlisted", value=f"\u200b{muster['skirmEnlisted']}", inline=False
                )

            # Cavalerie ---------------------------------------------------------------------
            cavEmbed = discord.Embed(
                title="Cavalerie",
                description="",
                color=0xff8c00,
            )
            cavEmbed.set_thumbnail(url="attachment://cav.png")
            list = muster.get('cavSo')
            if list and list.strip():
                cavEmbed.add_field(
                    name=f"Senior Officers", value=f"\u200b{muster['cavSo']}", inline=False
                )
                cavEmbed.add_field(
                    name=f"\u200b",
                    value=f"=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=",
                    inline=False,
                )
            list = muster.get('cavCo')
            if list and list.strip():
                cavEmbed.add_field(
                    name=f"Commissioned Officers", value=f"\u200b{muster['cavCo']}", inline=False
                )
                cavEmbed.add_field(
                    name=f"\u200b",
                    value=f"=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=",
                    inline=False,
                )
            list = muster.get('cavNco')
            if list and list.strip():
                cavEmbed.add_field(
                    name=f"Non-Commissioned Officers",
                    value=f"\u200b{muster['cavNco']}",
                    inline=False,
                )
                cavEmbed.add_field(
                    name=f"\u200b",
                    value=f"=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=",
                    inline=False,
                )
            list = muster.get('cavCpl')
            if list and list.strip():
                cavEmbed.add_field(
                    name=f"Corporals", value=f"\u200b{muster['cavCpl']}", inline=False
                )
                cavEmbed.add_field(
                    name=f"\u200b",
                    value=f"=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=",
                    inline=False,
                )
            list = muster.get('cavOcdt')
            if list and list.strip():
                cavEmbed.add_field(
                    name=f"Officer Cadets", value=f"\u200b{muster['cavOcdt']}", inline=False
                )
                cavEmbed.add_field(
                    name=f"\u200b",
                    value=f"=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=",
                    inline=False,
                )
            list = muster.get('cavEnlisted')
            if list and list.strip():
                cavEmbed.add_field(
                    name=f"Enlisted", value=f"\u200b{muster['cavEnlisted']}", inline=False
                )

            # Artillerie ---------------------------------------------------------------------
            artyEmbed = discord.Embed(
                title="Artillerie",
                description="",
                color=0x061f6b,
            )
            artyEmbed.set_thumbnail(url="attachment://arty.png")
            list = muster.get('artySo')
            if list and list.strip():
                artyEmbed.add_field(
                    name=f"Senior Officers", value=f"\u200b{muster['artySo']}", inline=False
                )
                artyEmbed.add_field(
                    name=f"\u200b",
                    value=f"=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=",
                    inline=False,
                )
            list = muster.get('artyCo')
            if list and list.strip():
                artyEmbed.add_field(
                    name=f"Commissioned Officers", value=f"\u200b{muster['artyCo']}", inline=False
                )
                artyEmbed.add_field(
                    name=f"\u200b",
                    value=f"=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=",
                    inline=False,
                )
            list = muster.get('artyNco')
            if list and list.strip():
                artyEmbed.add_field(
                    name=f"Non-Commissioned Officers", value=f"\u200b{muster['artyNco']}", inline=False
                )
                artyEmbed.add_field(
                    name=f"\u200b",
                    value=f"=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=",
                    inline=False,
                )
            list = muster.get('artyCpl')
            if list and list.strip():
                artyEmbed.add_field(
                    name=f"Corporals", value=f"\u200b{muster['artyCpl']}", inline=False
                )
                artyEmbed.add_field(
                    name=f"\u200b",
                    value=f"=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=",
                    inline=False,
                )
            list = muster.get('artyOcdt')
            if list and list.strip():
                artyEmbed.add_field(
                    name=f"Officer Cadets", value=f"\u200b{muster['artyOcdt']}", inline=False
                )
                artyEmbed.add_field(
                    name=f"\u200b",
                    value=f"=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=",
                    inline=False,
                )
            list = muster.get('artyEnlisted')
            if list and list.strip():
                artyEmbed.add_field(
                    name=f"Enlisted", value=f"\u200b{muster['artyEnlisted']}", inline=False
                )

            # Support Staff ---------------------------------------------------------------------
            supportstaffEmbed = discord.Embed(
                title="Auxiliary Staff",
                description="",
                color=0x5d27a1,
            )
            supportstaffEmbed.set_thumbnail(url="attachment://supportstaff.png")
            supportstaffEmbed.add_field(
                name=f"Enlisted", value=f"\u200b{muster['supportstaffEnlisted']}", inline=False
            )

            await workingMsg.delete()

            await ctx.send(file=soImg, embed=soEmbed)
            await ctx.send(file=coImg, embed=coEmbed)
            #await ctx.send(file=adjImg, embed=adjEmbed)
            await ctx.send(file=ncoImg, embed=ncoEmbed)
            await ctx.send(file=cplImg, embed=cplEmbed)
            await ctx.send(file=ocdtImg, embed=ocdtEmbed)
            await ctx.send(file=guardImg, embed=guardEmbed)
            await ctx.send(file=skirmImg, embed=skirmEmbed)
            await ctx.send(file=cavImg, embed=cavEmbed)
            await ctx.send(file=artyImg, embed=artyEmbed)
            await ctx.send(file=supportstaffImg, embed=supportstaffEmbed)

async def setup(bot):
    await bot.add_cog(enlistedCog(bot))
