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
            title="Attendance",
            description="Can you make it tonight? React with :thumbsup: , :thumbsdown: , or :person_shrugging:",
            color=0x109319
        )
        embed.add_field(name="Coming: ", value=f"No-one attending! :(", inline=False)
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

        embed = discord.Embed(
            title="Training & HQ",
            description="Are you happy to take training :teacher: ? Are you happy to help with training :handshake: ? Are you happy to take HQ <:3e:1205672874166325281> ?",
            color=0x109319
        )
        embed.add_field(name="Happy to take training: ", value=f"No-one happy to take training :(", inline=False)
        embed.add_field(name="Count: ", value=f"0", inline=False)
        embed.add_field(name="Happy to help with training: ", value=f"No-one happy to help with training", inline=False)
        embed.add_field(name="Count: ", value=f"0", inline=False)
        embed.add_field(name="Happy to take HQ: ", value=f"No-one happy to take HQ", inline=False)
        embed.add_field(name="Count: ", value=f"0", inline=False)

        msg = await leadershipChannel.send(embed=embed)

        await msg.add_reaction("🧑‍🏫")
        await msg.add_reaction("🤝")
        await msg.add_reaction("<:3e:1205672874166325281>")
        varStore.trainingMsgId = msg.id

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
            vcCatId = 1474947912638398639
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
        772921452135055360, 772921453095944203
    )
    @commands.guild_only()
    @commands.cooldown(1, 10, commands.BucketType.guild)
    @commands.command(aliases=["regimentRules"])
    async def regimentrules(self, ctx):
        rulesChannel = self.bot.get_channel(772920947912736818)
        await rulesChannel.send(file=discord.File('/home/container/files/rules.png'))
        await rulesChannel.send('**Violation of this code may result in a removal from the regiment depending on the severity.** \n\n:one: Act in a mature, respectful and professional manner at all times - this includes in-game chat. Trolling, bullying and hateful conduct will not be tolerated at any time. \n\n:two: The 3e does not have an attendance policy. However, all members are encouraged to attend events where possible - please refer to the <#772921029550931989>. \n\n:three: Training, War Games, and any other regimental event is to be taken seriously. Any other mentality will not be tolerated as it wastes time. \n\n:four: Ensure your in-game name is formatted exactly as it appears on Discord. \n\n:five: Follow the Chain of Command at all times. \n\n:six: Never intentionally teamwound or teamkill. If you do so, apologise at the earliest safe break in combat.  \n\n:seven: Ensure you are lined up properly before live. \n\n:eight: Politics and all political related chat must be kept exclusive to the politics text channel or voice-chat. Remember to abide by Discord Terms of Service. The use of racial slurs, including the N-word and its derivatives, is strictly forbidden. Discrimination or derogatory language regarding race, ethnicity, or identity will result in immediate disciplinary action. \n\n:nine: The regiment is only as strong as the weakest link. Make new members feel welcome, and assist them in gaining important skills. \n\n:keycap_ten: Keep personal problems, disputes regarding event administration, and any type of drama inside the regiment. If you have a serious issue, take it up with an officer privately.\n\n**A list of Officers can be found in the <#961650074268618813> channel.**')

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
        await enlistmentChannel.send('**Copy/Paste the following format below, answering each question to enlist in the 3e:**\n```**What is your in-game name?**\n**Have you read and do you agree to follow our Regiment Rules?**\n**Are you aged 16 years or older (if not you can still enlist)?**\n**Are you currently in a different Holdfast regiment? If so, which one?**\n**How did you find the 3e?**\n**What region are you from?**\n**What platform are you on (PC / Xbox / Playstation)?**\n@Officer Corps```\n**Need help?** Just <@&772921877953904661> in this channel and you will be assisted.')

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
        # Enlisted Medals Title ----------------------------------------------------
        enlistmedalsEmbed=discord.Embed(title="Enlisted Medals", description="", color=0xff0000)
        enlistmedalsEmbed.set_thumbnail(url="https://cdn.discordapp.com/attachments/847486338685206528/950004623207465001/unknown.png")

        # Enlisted Medals ------------------------------------------------------------------------------------
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

        # Infanterie Medals Title ----------------------------------------------------
        infmedalsEmbed=discord.Embed(title="Infanterie Medals", description="", color=0xff0000)
        infmedalsEmbed.set_thumbnail(url="https://cdn.discordapp.com/attachments/847486338685206528/950004623207465001/unknown.png")

        # Infanterie Medals ----------------------------------------------------
        orderofthelionEmbed=discord.Embed(description="Achieve the weekly challenge.\n<@&TODO_ROLE_ID>", color=0xfd8282)
        orderofthelionEmbed.set_author(name="Order of the Lion", icon_url="https://images.emojiterra.com/twitter/512px/1f396.png")

        grenadierexperimenteEmbed=discord.Embed(description="As a Grenadier, achieve 4 shooting kills in a single round.\n<@&TODO_ROLE_ID>", color=0xfd8282)
        grenadierexperimenteEmbed.set_author(name="Grenadier expérimenté", icon_url="https://images.emojiterra.com/twitter/512px/1f396.png")

        fleurdelisEmbed=discord.Embed(description="Finish top 2 while playing infanterie class.\n<@&TODO_ROLE_ID>", color=0xfd8282)
        fleurdelisEmbed.set_author(name="Fleur-de-lis", icon_url="https://images.emojiterra.com/twitter/512px/1f396.png")

        bombechanceuseEmbed=discord.Embed(description="As Grenadiers get two kills with one grenade.\n<@&TODO_ROLE_ID>", color=0xfd8282)
        bombechanceuseEmbed.set_author(name="Bombe chanceuse", icon_url="https://images.emojiterra.com/twitter/512px/1f396.png")

        ticktickboomEmbed=discord.Embed(description="Blow up enemy arty or kill an enemy horse with your grenade.\n<@&TODO_ROLE_ID>", color=0xfd8282)
        ticktickboomEmbed.set_author(name="Tick Tick Boom", icon_url="https://images.emojiterra.com/twitter/512px/1f396.png")

        holyhandgrenadesEmbed=discord.Embed(description="As a line successfully overrun and kill an enemy line after throwing Grenadiers.\n<@&TODO_ROLE_ID>", color=0xfd8282)
        holyhandgrenadesEmbed.set_author(name="Holy Hand Grenades", icon_url="https://images.emojiterra.com/twitter/512px/1f396.png")


        # Garde Medals Title ------------------------------------------------------------------------------------------------------
        gardemedalsEmbed=discord.Embed(title="Garde Medals", description="", color=0x810505)
        gardemedalsEmbed.set_thumbnail(url="https://media.discordapp.net/attachments/960873839036887061/1148913727953961040/image.png")
        # Garde Medals ------------------------------------------------------------------------------------------------------------
        sabreEmbed=discord.Embed(description="Obtain 2 kills with your Sabre in a single round.\n<@&1132544038441074748>", color=0xb20b0b)
        sabreEmbed.set_author(name="Sabre Connoisseur", icon_url="https://images.emojiterra.com/twitter/512px/1f396.png")

        gardeimperialeEmbed=discord.Embed(description="Obtain 5 melee Kills in a single round.\n<@&1148913866361819207>", color=0xb20b0b)
        gardeimperialeEmbed.set_author(name="Garde Imperiale", icon_url="https://images.emojiterra.com/twitter/512px/1f396.png")

        rodetoruinEmbed=discord.Embed(description="Kill 3 enemy cavalry in a single round (includes HQ scouts)\n<@&1148915957398523925>", color=0xb20b0b)
        rodetoruinEmbed.set_author(name="Rode to Ruin", icon_url="https://images.emojiterra.com/twitter/512px/1f396.png")

        musketeerEmbed=discord.Embed(description="Obtain 3 kills via shooting in a single round.\n<@&1148918057591394334>", color=0xb20b0b)
        musketeerEmbed.set_author(name="Musketeer", icon_url="https://images.emojiterra.com/twitter/512px/1f396.png")
        
        elitemusketeerEmbed=discord.Embed(description="Obtain 5 kills via shooting in a single round.\n<@&1299985991422971904>", color=0xb20b0b)
        elitemusketeerEmbed.set_author(name="Elite Musketeer", icon_url="https://images.emojiterra.com/twitter/512px/1f396.png")

        # Garde Medals - New Achievements (Part 2) ----------------------------------------------------------------------------------
        bronzeLionEmbed=discord.Embed(description="Achieve 3 melee kills AND 2 shooting kills in a single round\n<@&TODO_ROLE_ID>", color=0xb20b0b)
        bronzeLionEmbed.set_author(name="Bronze Lion", icon_url="https://images.emojiterra.com/twitter/512px/1f396.png")

        silverLionEmbed=discord.Embed(description="Achieve 6 melee kills AND 3 shooting kills in a single round\n<@&TODO_ROLE_ID>", color=0xb20b0b)
        silverLionEmbed.set_author(name="Silver Lion", icon_url="https://images.emojiterra.com/twitter/512px/1f396.png")

        goldLionEmbed=discord.Embed(description="Achieve 10 melee kills AND 4 shooting kills in a single round\n<@&TODO_ROLE_ID>", color=0xb20b0b)
        goldLionEmbed.set_author(name="Gold Lion", icon_url="https://images.emojiterra.com/twitter/512px/1f396.png")

        dragzHonorEmbed=discord.Embed(description="Achieve Gren IX (2.4 KPR) over the entire month\n<@&TODO_ROLE_ID>", color=0xb20b0b)
        dragzHonorEmbed.set_author(name="Dragz Honor", icon_url="https://images.emojiterra.com/twitter/512px/1f396.png")

        loneWolfEmbed=discord.Embed(description="Continue a charge alone after your line is wiped, survive, and kill the enemy line you were attacking\n<@&TODO_ROLE_ID>", color=0xb20b0b)
        loneWolfEmbed.set_author(name="The Lone Wolf", icon_url="https://images.emojiterra.com/twitter/512px/1f396.png")

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

        imnumberoneEmbed=discord.Embed(description="Obtain double the amount of kills as the first player on the enemy team.\n<@&1015950941075296307>", color=0xddc890)
        imnumberoneEmbed.set_author(name="I'm Number One!", icon_url="https://images.emojiterra.com/twitter/512px/1f396.png")

        saberSpearsEmbed=discord.Embed(description="1 vs 1 an enemy sgt (while mounted) and kill them with a saber.\n<@&TODO_ROLE_ID>", color=0xddc890)
        saberSpearsEmbed.set_author(name="Saber > Spear", icon_url="https://images.emojiterra.com/twitter/512px/1f396.png")

        thisroundismeEmbed=discord.Embed(description="Kill 10 or more people in a round.\n<@&TODO_ROLE_ID>", color=0xddc890)
        thisroundismeEmbed.set_author(name="This Round Is On Me", icon_url="https://images.emojiterra.com/twitter/512px/1f396.png")

        pikecasualEmbed=discord.Embed(description="Shoot 2 enemy sgts in a round.\n<@&TODO_ROLE_ID>", color=0xddc890)
        pikecasualEmbed.set_author(name="Pike this you filthy casual", icon_url="https://images.emojiterra.com/twitter/512px/1f396.png")

        offwiththeirsheadsEmbed=discord.Embed(description="Kill 3 officers and/or sgts in a round.\n<@&TODO_ROLE_ID>", color=0xddc890)
        offwiththeirsheadsEmbed.set_author(name="Off With Their Heads", icon_url="https://images.emojiterra.com/twitter/512px/1f396.png")

        yipikeyaEmbed=discord.Embed(description="Get at least 2 kills with a saber while getting a kill with your horse in the same kill feed.\n<@&TODO_ROLE_ID>", color=0xddc890)
        yipikeyaEmbed.set_author(name="YIPIKIYA mother f$&@er", icon_url="https://images.emojiterra.com/twitter/512px/1f396.png")


        # Artillerie Medals Title ------------------------------------------------------------------------------------------------------
        artymedalsEmbed=discord.Embed(title="Artillerie Medals", description="", color=0x1e21dc)
        artymedalsEmbed.set_thumbnail(url="https://cdn.discordapp.com/attachments/846669911812210698/1015535128958730251/unknown.png")
        # Artillerie Medals  ------------------------------------------------------------------------------------------------------
        grandbombardierEmbed=discord.Embed(description="Eliminate 5 or more enemy players with a single cannon shot.\n<@&772932119877517362>", color=0x7879e5)
        grandbombardierEmbed.set_author(name="Grand Bombardier", icon_url="https://images.emojiterra.com/twitter/512px/1f396.png")

        sixtyninesbaneEmbed=discord.Embed(description="Wipe out a 69th artillery piece.\n<@&TODO_ROLE_ID>", color=0x7879e5)
        sixtyninesbaneEmbed.set_author(name="69th's Bane", icon_url="https://images.emojiterra.com/twitter/512px/1f396.png")

        grandbombardierEmbed=discord.Embed(description="Eliminate 5 or more enemy players with a single cannon shot.\n<@&772932119877517362>", color=0x7879e5)
        grandbombardierEmbed.set_author(name="Grand Bombardier", icon_url="https://images.emojiterra.com/twitter/512px/1f396.png")

        someassemblyrequiredEmbed=discord.Embed(description="As a Sapper, finish the round top of the leaderboard with no kills.\n<@&TODO_ROLE_ID>", color=0x7879e5)
        someassemblyrequiredEmbed.set_author(name="Some Assembly Required", icon_url="https://images.emojiterra.com/twitter/512px/1f396.png")

        unrelentingbarrageEmbed=discord.Embed(description="Obtain 10 or more kills with any artillery piece(s) in a single line battle round.\n<@&772932588729270302>", color=0x7879e5)
        unrelentingbarrageEmbed.set_author(name="Unrelenting Barrage", icon_url="https://images.emojiterra.com/twitter/512px/1f396.png")

        taxcollectorEmbed=discord.Embed(description="Kill 5 officers in a single event with artillery.\n<@&TODO_ROLE_ID>", color=0x7879e5)
        taxcollectorEmbed.set_author(name="Tax Collector", icon_url="https://images.emojiterra.com/twitter/512px/1f396.png")

        siryourpackageEmbed=discord.Embed(description="Kill just a single player with round shot.\n<@&1003634796737605682>", color=0x7879e5)
        siryourpackageEmbed.set_author(name="Sir, your package", icon_url="https://images.emojiterra.com/twitter/512px/1f396.png")

        finderskeepersEmbed=discord.Embed(description="Steal an enemy cannon.\n<@&1003635610348703844>", color=0x7879e5)
        finderskeepersEmbed.set_author(name="Finders Keepers", icon_url="https://images.emojiterra.com/twitter/512px/1f396.png")

        ceasefireEmbed=discord.Embed(description="Achieve 20+ artillery kills in a round.\n<@&TODO_ROLE_ID>", color=0x7879e5)
        ceasefireEmbed.set_author(name="Cease Fire? Never Heard of Her", icon_url="https://images.emojiterra.com/twitter/512px/1f396.png")
        
        rocketmanEmbed=discord.Embed(description="Achieve 5+ kills in one round using rockets.\n<@&1388038131093082242>", color=0x9a82b0)
        rocketmanEmbed.set_author(name="Rocket Man", icon_url="https://images.emojiterra.com/twitter/512px/1f396.png")

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
        
        recruitmentmedalEmbed=discord.Embed(description="Awarded to a member that recruits 5 players within a week.\n<@&772935148021743637>", color=0x644d43)
        recruitmentmedalEmbed.set_author(name="Recruitment Medal", icon_url="https://images.emojiterra.com/twitter/512px/1f396.png")

        # Pub Awards --------------------------------------------------------------------------------------------------
        pubawardsEmbed=discord.Embed(title="Pub Awards", description="The following awards can only be achieved on Official Holdfast Public Servers. These awards are given on command and not read out during ceremonies.", color=0x9f03a4)
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

        await ctx.send(embed=enlistmedalsEmbed)
        await ctx.send(embed=dieliketherestEmbed)
        await ctx.send(embed=tisbutascratchEmbed)
        await ctx.send(embed=supremacymedalEmbed)
        await ctx.send(embed=clenchEmbed)
        await ctx.send(embed=eyeforaneyeEmbed)
        await ctx.send(embed=leadoversteelEmbed)
        await ctx.send(embed=firstbloodEmbed)
        await ctx.send(embed=whymeEmbed)
        await ctx.send(embed=ruthlessEmbed)
        await ctx.send(embed=specsaversEmbed)
        await ctx.send(embed=knucklesEmbed)
        await ctx.send(embed=infmedalsEmbed)
        await ctx.send(embed=orderofthelionEmbed)
        await ctx.send(embed=grenadierexperimenteEmbed)
        await ctx.send(embed=fleurdelisEmbed)
        await ctx.send(embed=bombechanceuseEmbed)
        await ctx.send(embed=ticktickboomEmbed)
        await ctx.send(embed=holyhandgrenadesEmbed)
        await ctx.send(embed=gardemedalsEmbed)
        await ctx.send(embed=sabreEmbed)
        await ctx.send(embed=gardeimperialeEmbed)
        await ctx.send(embed=rodetoruinEmbed)
        await ctx.send(embed=musketeerEmbed)
        await ctx.send(embed=elitemusketeerEmbed)
        await ctx.send(embed=bronzeLionEmbed)
        await ctx.send(embed=silverLionEmbed)
        await ctx.send(embed=goldLionEmbed)
        await ctx.send(embed=dragzHonorEmbed)
        await ctx.send(embed=loneWolfEmbed)
        await ctx.send(embed=skirmmedalsEmbed)
        await ctx.send(embed=itscalledstealthEmbed)
        await ctx.send(embed=expertmarksmanEmbed)
        await ctx.send(embed=aimtrueEmbed)
        await ctx.send(embed=zaitsevEmbed)
        await ctx.send(embed=headshotEmbed)
        await ctx.send(embed=cavmedalsEmbed)
        await ctx.send(embed=whataclutchEmbed)
        await ctx.send(embed=trustisthekeyEmbed)
        await ctx.send(embed=imnumberoneEmbed)
        await ctx.send(embed=saberSpearsEmbed)
        await ctx.send(embed=thisroundismeEmbed)
        await ctx.send(embed=pikecasualEmbed)
        await ctx.send(embed=offwiththeirsheadsEmbed)
        await ctx.send(embed=yipikeyaEmbed)
        await ctx.send(embed=sixtyninesbaneEmbed)
        await ctx.send(embed=artymedalsEmbed)
        await ctx.send(embed=someassemblyrequiredEmbed)
        await ctx.send(embed=taxcollectorEmbed)
        await ctx.send(embed=ceasefireEmbed)
        await ctx.send(embed=sixtyninesbaneEmbed)
        await ctx.send(embed=supportmedalsEmbed)
        await ctx.send(embed=healinghandEmbed)
        await ctx.send(embed=dyinghandEmbed)
        await ctx.send(embed=poorprognosisEmbed)
        await ctx.send(embed=hitemwithpatriotismEmbed)
        await ctx.send(embed=onlyflagsEmbed)
        await ctx.send(embed=dontstopbelievingEmbed)
        await ctx.send(embed=onionEmbed)
        await medalsChannel.send(embed=redcrossEmbed)
        await ctx.send(embed=officermedalsEmbed)
        await ctx.send(embed=grandtacticianEmbed)
        await ctx.send(embed=assaultdoctrineEmbed)
        await ctx.send(embed=wehavemoremenEmbed)
        await ctx.send(embed=againstalloddsEmbed)
        await ctx.send(embed=ribbonsEmbed)
        await ctx.send(embed=marksmanribbonsEmbed)
        await ctx.send(embed=scorerribbonsEmbed)
        await medalsChannel.send(embed=recruitmentmedalEmbed)
        await medalsChannel.send(embed=pubawardsEmbed)
        await medalsChannel.send(embed=xpawardsEmbed)
        await medalsChannel.send(embed=killawardsEmbed)
        await medalsChannel.send(embed=challengeawardsEmbed)
        await medalsChannel.send(embed=medalapplicationEmbed)
        await medalsChannel.send('*All submissions require the following format (please do not ping medals):*\n```**Medal Requested:**\n**Date/Event of Achievement:**\n**Witnesses (if applicable):**\n**Evidence:**\n@Officer Corps```')

    #Post Honours
    @commands.has_any_role(
        772921452135055360, 772921453095944203
    )
    @commands.guild_only()
    @commands.cooldown(1, 10, commands.BucketType.guild)
    @commands.command(aliases=["Honours"])
    async def honours(self, ctx):
        honoursChannelId = 1427838366488989727

        async with ctx.channel.typing():
            if ctx.channel.id == honoursChannelId:
                async for message in ctx.channel.history(limit = 100):
                    if message is None:
                        break
                    elif message.author.bot:
                        await message.delete()

            await ctx.send(file=discord.File('/home/container/files/honours.png'))
            
            jacksoncrossEmbed=discord.Embed(description="Awarded to members who have successfully received all medals, or otherwise issued for extremely special displays of abilities. This medal is named after a previous leader of the regiment.\n<@&772935853076643840>", color=0x644d43)
            jacksoncrossEmbed.set_author(name="Jackson Cross", icon_url="https://images.emojiterra.com/twitter/512px/1f3c6.png")
            jacksoncrossList = [
                "(ex) 3e | CdB. Wessforde",
                "(ex) 3e | Sgt. Quasar",
                "(ex) 3e | Cpl. Niggy",
                "(ex) 3e | CdB. Iceman",
                "(ex) 3e | Cpt. ScareWest",
                "3e | VGrd. Sinned",
                "3e | Tbr-cpl. Fairus"
            ]
            jacksoncrossListString = "\n".join(jacksoncrossList)
            jacksoncrossListEmbed = discord.Embed(color=0xf2e442)
            jacksoncrossListEmbed.add_field(name="Recipients", value=jacksoncrossListString, inline=False)

            darkflameHeartEmbed=discord.Embed(description="Awarded to members who have been highly regarded for their exemplary dedication and cherished contributions to the 3e community.\n<@&1428984330822221923>", color=0x644d43)
            darkflameHeartEmbed.set_author(name="Darkflame Heart", icon_url="https://images.emojiterra.com/twitter/512px/1f3c6.png")
            darkflameHeartList = [
            "3e | Pte-Aigle. JungleHeart",            
            ]
            darkflameHeartListString = "\n".join(darkflameHeartList)
            darkflameHeartListEmbed = discord.Embed(color=0xf2e442)
            darkflameHeartListEmbed.add_field(name="Recipients", value=darkflameHeartListString, inline=False)
            
            clutchEmbed=discord.Embed(description="Awarded to a member who, as the last surviving player wins the round fighting 3 or more enemies.\n<@&772935250522800129>", color=0x644d43)
            clutchEmbed.set_author(name="Creepy Clutch", icon_url="https://images.emojiterra.com/twitter/512px/1f3c6.png")
            clutchList = [
                "(ex) 3e | Maj. Creedo",
                "3e | Adj. RAT_DOG",
                "(ex) 3e | Capt. Plot",
                "3e | Capt. TANKIGAMER",
                "3e | VGrd. Sinned",
                "3e | Fch. Dragz",
                "3e | Pte-Aigle. JungleHeart",
                "(ex) 3e | Sgt. Ryland", 
                "3e | Sgt. Garfunkel"
            ]
            clutchListString = "\n".join(clutchList)
            clutchListEmbed = discord.Embed(color=0xf2e442)
            clutchListEmbed.add_field(name="Recipients", value=clutchListString, inline=False)

            fourdchessEmbed=discord.Embed(description="While being the last one alive, get 3 or more enemies to team kill each other.\n<@&772935536293576734>", color=0x644d43)
            fourdchessEmbed.set_author(name="Taragorne Touchdown", icon_url="https://images.emojiterra.com/twitter/512px/1f3c6.png")
            fourdchessList = [
                "3e | Maj. TANKIGAMER",
                "3e | VGrd. Sinned",
                "3e | Lt. Danx",
                "3e | Pte-Aigle. JungleHeart",
                "(ex) 3e | Gren. Yuukari",
                "3e | VGrd. Kiwifruit",
                "3e | Sgt. Garfunkel",
                "3e | VGrd. Ray"
            ]
            fourdchessListString = "\n".join(fourdchessList)
            fourdchessListEmbed = discord.Embed(color=0xf2e442)
            fourdchessListEmbed.add_field(name="Recipients", value=fourdchessListString, inline=False)

            hardcoreenlistedEmbed=discord.Embed(description="Finish all 5 rounds of an event in 1st place on the scoreboard.\n<@&1241680967157157938>", color=0x644d43)
            hardcoreenlistedEmbed.set_author(name="Hardcore 3e", icon_url="https://images.emojiterra.com/twitter/512px/1f3c6.png")

            pourlemeriteEmbed=discord.Embed(description="Obtain 8 or more kills in a single line battle round.\n<@&772928362280517653>", color=0x644d43)
            pourlemeriteEmbed.set_author(name="Pour le Merite", icon_url="https://images.emojiterra.com/twitter/512px/1f3c6.png")
            pourlemeriteList = [
                "(ex) 3e | Maj. Creedo",
                "(ex) 3e | Sgt. Quasar",
                "(ex) 3e | Capt. Plot",
                "3e | Maj. TANKIGAMER",
                "3e | VGrd. Sinned",
                "3e | Adj. RAT_DOG",
                "3e | GdP. ItzTank", 
                "3e | Adj. CaptainThunder",
                "3e | Lt. Danx",
                "3e | GdP. Cube",
                "3e | Fch. Dragz",
                "3e | Tlr. Tim",
                "3e | Chef. Meateor",
                "3e | GdP. Quacks",
                "(ex) 3e | Capt. Dropbear",
                "3e | Adj. BalisongBlue",
                "3e | Tbr-cpl. Fairus",
                "3e | CpF. Kruber",
                "3e | Sdt. Douglas Mawson",
                "3e | Col. Shady",
                "3e | Pte-aigle. JungleHeart",
                "3e | Chas. Jeby",
                "3e | Cpl. Xander",
                "3e | VGrd. Leaf",
                "3e | Sous-Lt. AsianSharpe",
                "(ex) 3e | Sgt-Maj. Lexi",
                "3e | VGrd. Lachlan",
                "(ex) 3e | Cpl. Jacjacheed",
                "(ex) 3e | CpF. Ryno",
                "3e | Gren. Spikes",
                "(ex) 3e | Cpl. Slothboi44",
                "(ex) 3e | Gren. Ghost",
                "(ex) 3e | Gren. Yuukari",
                "(ex) 3e | Sdt. Prince",
                "3e | GdP. Crazyshadowfax",
                "3e | VGrd. Kiwifruit",
                "3e | Trlr. Zigzag",
                "3e | Sgt. Garfunkel",
                "3e | Sous-Lt. Spyro",
                "3e | VGrd. Santa",
                "3e | VGrd. Ray",
                "3e | Gren. Buckname",
                "3e | CpF. Wogsauce", 
                "3e | Cpl. Kage",
                
            ]
            pourlemeriteListString = "\n".join(pourlemeriteList)
            pourlemeriteListEmbed = discord.Embed(color=0xf2e442)
            pourlemeriteListEmbed.add_field(name="Recipients", value=pourlemeriteListString, inline=False)

            # Service Crosses, when someone reaches a higher level of service cross, remove them from the lower one they earned previously. Add them to the bottom of the new list. Sort by date recruited desc. when you batch add people to a new rank.
            servicecross400Embed=discord.Embed(description="Awarded to members who have attended at least 400 line battles.\n<@&1299989565280485376>", color=0x644d43)
            servicecross400Embed.set_author(name="Service Cross 400", icon_url="https://images.emojiterra.com/twitter/512px/1f3c6.png")
            servicecross400List = [
                "3e | VGrd. Sinned",
                "3e | Lt. Danx",
                "3e | Msc. Fairus",
                "3e | Col. Shady",
                "(ex) 3e | Maj. Jackson",
                "3e | Maj. TANKIGAMER",
                "3e | Pte-aigle. JungleHeart"
            ]
            servicecross400ListString = "\n".join(servicecross400List)
            servicecross400ListEmbed = discord.Embed(color=0xf2e442)
            servicecross400ListEmbed.add_field(name="Recipients", value=servicecross400ListString, inline=False)

            servicecross300Embed=discord.Embed(description="Awarded to members who have attended at least 300 line battles.\n<@&1299988796410036266>", color=0x644d43)
            servicecross300Embed.set_author(name="Service Cross 300", icon_url="https://images.emojiterra.com/twitter/512px/1f3c6.png")
            servicecross300List = [
                "3e | Trlr. Billy",
                "3e | CpF. Kruber",
                "3e | Sgt-Maj. Taragorn",
                "3e | VGrd. Leaf",
                "3e | Chas. Jeby",
                "3e | Sous-Lt. AsianSharpe",
                "3e | Sous-Lt. Spyro",
                "3e | Sgt-Maj. Ganthador"
            ]
            servicecross300ListString = "\n".join(servicecross300List)
            servicecross300ListEmbed = discord.Embed(color=0xf2e442)
            servicecross300ListEmbed.add_field(name="Recipients", value=servicecross300ListString, inline=False)

            servicecross200Embed=discord.Embed(description="Awarded to members who have attended at least 200 line battles.\n<@&1299988766831935508>", color=0x644d43)
            servicecross200Embed.set_author(name="Service Cross 200", icon_url="https://images.emojiterra.com/twitter/512px/1f3c6.png")
            servicecross200List = [
                "3e | Adj. RAT_DOG",
                "3e | GdP. Cube",
                "3e | Trlr. Tim",
                "3e | Trlr. ZigZag",
                "3e | Cpl. Xander",
                "(ex) 3e | Sgt-Maj. Lexi",
                "3e | Sdt. Douglas Mawson",
                "3e | Fch. Mugi",
                "3e | Cvlr. General",
                "3e | GdP. Cloud Jumper",
                "3e | Cpl. HelixOrion",
                "3e | VGrd. Lachlan"
            ]                
            servicecross200ListString = "\n".join(servicecross200List)
            servicecross200ListEmbed = discord.Embed(color=0xf2e442)
            servicecross200ListEmbed.add_field(name="Recipients", value=servicecross200ListString, inline=False)

            servicecrossEmbed=discord.Embed(description="Awarded to members who have attended at least 75 line battles.\n<@&1003642674873651260>", color=0x644d43)
            servicecrossEmbed.set_author(name="Service Cross", icon_url="https://images.emojiterra.com/twitter/512px/1f3c6.png")
            servicecrossList = [
                "(ex) 3e | Cpt. ScareWest",
                "3e | GdP. ItzTank",
                "3e | GdP. Mr. MLG",
                "3e | Adj. CaptainThunder",
                "3e | GdP. Cobby",
                "3e | GdP. EamonRamon",
                "3e | Volt. Adelin",
                "3e | Chef. Meateor",
                "3e | GdP. Quacks",
                "(ex) 3e | Capt. Dropbear",
                "3e | Adj. BalisongBlue",
                "3e | Cvlr. Windfire&Cum",
                "3e | GdP. Commonly",
                "3e | GdP. Jaiko",
                "3e | GdP. LetMeSolo",
                "3e | GdP. InflatedSteak",
                "(ex) 3e | Chas. Jacjacheed",
                "(ex) 3e | CpF. Ryno",
                "(ex) 3e | Sous-Ofc. Kohan",
                "3e | Ins. Theatr1cal1ty",
                "3e | GdP. Viking",
                "3e | Adj. Sparc", 
                "3e | Cnr. Tumo",
                "3e | Msc. Deadreaper",
                "3e | CpF. Wogsauce", 
                "3e | Sgt. 2big2bear13",
                "3e | GdP. CrazyShadowfax",
                "3e | Gren. Sir Unnameable",
                "3e | Cvlr. Dogat",
                "3e | Cpl. Rabbit",
                "3e | Cnr. Ghostii",
                "3e | MGrd. Pepperr",
                "3e | VGrd. Ray",
                "3e | GdP. Wulfric",
                "3e | GdP. Napoleon 2.0",
                "3e | GdP. PiratesBites",
                "3e | Gren. Viv La Soviet",
                "3e | GdP. Smore",
                "3e | JGrd. Dylan",
                "3e | Sgt. Garfunkel",
                "3e | Fch. Dragz",
                "3e | Cpl. Kage",
                "3e | VGrd. Santa",
                "3e | Cpl. Fartic",
                "3e | CpF. Pin0",  
                
            ]
            servicecrossListString = "\n".join(servicecrossList)
            servicecrossListEmbed = discord.Embed(color=0xf2e442)
            servicecrossListEmbed.add_field(name="Recipients", value=servicecrossListString, inline=False)

            infantryLongshotEmbed=discord.Embed(description="Longshot Champions.", color=0x644d43)
            infantryLongshotEmbed.set_author(name="Eagle's Eye", icon_url="https://images.emojiterra.com/twitter/512px/1f3c6.png")
            infantryLongshotList = [
                "🥇 - 3e | Sgt. Garfunkel - 2025-10-10 - 358.2m",
                "🥈 - (ex) 3e | GdP. Schnitzel - 2025-07-09 - 342.7m",
                "🥉 - 3e | Trlr. Zigzag - 2026-03-11 - 340.1m",
            ]
            infantryLongshotListString = "\n".join(infantryLongshotList)
            infantryLongshotListEmbed = discord.Embed(color=0xf2e442)
            infantryLongshotListEmbed.add_field(name="Recipients", value=infantryLongshotListString, inline=False)

            ratdogsResistanceEmbed=discord.Embed(description="Killstreak Champions.", color=0x644d43)
            ratdogsResistanceEmbed.set_author(name="Rat Dog's Resistance", icon_url="https://images.emojiterra.com/twitter/512px/1f3c6.png")
            ratdogsResistanceList = [
                "🥇 - 3e | Cpl. Xander - 2025-07-25 - 20 kills",
                "🥈 - 3e | VGrd. Kiwifruit - 2025-12-06 - 18 kills",
                "🥈 - 3e | Lt. Danx - 2025-12-12 - 18 kills",
                "🥉 - 3e | Pte-Aigle. JungleHeart - 2025-08-19 - 15 kills"
            ]
            ratdogsResistanceListString = "\n".join(ratdogsResistanceList)
            ratdogsResistanceListEmbed = discord.Embed(color=0xf2e442)
            ratdogsResistanceListEmbed.add_field(name="Recipients", value=ratdogsResistanceListString, inline=False)
            
            await ctx.send(embed=jacksoncrossEmbed)
            await ctx.send(embed=jacksoncrossListEmbed)
            await ctx.send(embed=darkflameHeartEmbed)
            await ctx.send(embed=darkflameHeartListEmbed)
            await ctx.send(embed=clutchEmbed)
            await ctx.send(embed=clutchListEmbed)
            await ctx.send(embed=fourdchessEmbed)
            await ctx.send(embed=fourdchessListEmbed)
            await ctx.send(embed=hardcoreenlistedEmbed)
            await ctx.send(embed=pourlemeriteEmbed)
            await ctx.send(embed=pourlemeriteListEmbed)
            await ctx.send(embed=servicecross400Embed)
            await ctx.send(embed=servicecross400ListEmbed)
            await ctx.send(embed=servicecross300Embed)
            await ctx.send(embed=servicecross300ListEmbed)
            await ctx.send(embed=servicecross200Embed)
            await ctx.send(embed=servicecross200ListEmbed)
            await ctx.send(embed=servicecrossEmbed)
            await ctx.send(embed=servicecrossListEmbed)
            await ctx.send(embed=infantryLongshotEmbed)
            await ctx.send(embed=infantryLongshotListEmbed)
            await ctx.send(embed=ratdogsResistanceEmbed)
            await ctx.send(embed=ratdogsResistanceListEmbed)

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
                fchlist = []
                sgtmajlist = []
                sgtList = []
                for user in ctx.guild.members:
                        if companyRole in user.roles:
                            if ncoRole in user.roles:
                                if "Adj." in user.display_name:
                                    nick = (user.display_name).replace("Adj. ", "Adjutant ")
                                    adjList.append(nick)                         
                                elif "Fch. " in user.display_name:
                                    nick = (user.display_name).replace("Fch. ", "Fanrich ")
                                    fchlist.append(nick)    
                                elif "Sgt-Maj. " in user.display_name:
                                    nick = (user.display_name).replace("Sgt-Maj. ", "Sergeant-Major ")
                                    sgtmajlist.append(nick)
                                elif "Sgt. " in user.display_name:
                                    nick = (user.display_name).replace("Sgt. ", "Sergeant ")
                                    sgtList.append(nick)
                adjList.sort()
                fchlist.sort()
                sgtmajlist.sort()
                sgtList.sort()

                ncoList = [adjList, fchlist, sgtmajlist, sgtList]
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

            def enlistedCalc(companyRole):
                insList = []
                chgList = []
                lcsList = []
                mscList = []
                tbrcplList = []
                pteaigleList = []
                chgmajList = []
                chefList = []
                jgrdList = []
                mgrdList = []
                vgrdList = []
                trlrList = []
                voltList = []
                cnrList = []
                bmdList = []
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
                        elif "JGrd. " in user.display_name:
                            nick = (user.display_name).replace("JGrd. ", "Jeune Garde ")
                            jgrdList.append(nick)
                        elif "MGrd. " in user.display_name:
                            nick = (user.display_name).replace("MGrd. ", "Moyenne Garde ")
                            mgrdList.append(nick)    
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
                        elif "Bmd. " in user.display_name:
                            nick = (user.display_name).replace("Bmd. ", "Bombardier ")
                            bmdList.append(nick)
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
                jgrdList.sort()
                mgrdList.sort()
                vgrdList.sort()
                trlrList.sort()
                voltList.sort()
                cnrList.sort()
                bmdList.sort()
                cvlrList.sort()
                chasList.sort()
                lcsList.sort()
                gdpList.sort()
                grenList.sort()
                fusList.sort()
                sdtList.sort()

                enlistedList = [lcsList, chgmajList, chgList, pteaigleList, insList, tbrcplList, mscList, vgrdList, mgrdList, jgrdList, voltList, trlrList, bmdList, cnrList, chasList, cvlrList, gdpList, grenList, fusList, sdtList]
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
                        elif "JGrd. " in user.display_name:
                            enlistedCount += 1
                        elif "MGrd. " in user.display_name:
                            enlistedCount += 1
                        elif "VGrd. " in user.display_name:
                            enlistedCount += 1
                        elif "Trlr. " in user.display_name:
                            enlistedCount += 1
                        elif "Volt. " in user.display_name:
                            enlistedCount += 1
                        elif "Cnr. " in user.display_name:
                            enlistedCount += 1
                        elif "Bmd. " in user.display_name:
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
            soEmbed.add_field(name="Colonel Shady", value="1 IC of the 3e", inline=False)
            soEmbed.add_field(name="Major TANKIGAMER", value="2IC of the 3e, Leader of Cavalerie, Keeper of the Tale", inline=False)

            # Commissioned Officers ----------------------------------------------------
            coEmbed=discord.Embed(title="Commissioned Officers", description="", color=0x112074)
            coEmbed.set_thumbnail(url="attachment://commissionedofficer.png")
            coEmbed.add_field(name="Lieutenant Danx", value="Leader of the Legere", inline=False)
            coEmbed.add_field(name="Sous-Lieutenant AsianSharpe", value="Leader of the Artillerie, Minister of Diplomacy", inline=False)
            coEmbed.add_field(name="Sous-Lieutenant Spyro", value="Leader of the Infanterie, Minister of Security", inline=False)

            # Adjutant Council (Disabled) ----------------------------------------------------
            #adjEmbed=discord.Embed(title="Adjutant Council", description="", color=0x2b56c8)
            #adjEmbed.set_thumbnail(url="attachment://adjutant.png")
            #adjEmbed.add_field(name="Adjutant Dayrahl", value="", inline=False)
            #adjEmbed.add_field(name="Adjutant Mugi", value="", inline=False)

            # Non-Commissioned Officers ----------------------------------------------------
            ncoEmbed=discord.Embed(title="Non-Commissioned Officers", description="", color=0x192fa7)
            ncoEmbed.set_thumbnail(url="attachment://nco.png")
            ncoEmbed.add_field(name="Fahnrich Dragz", value="Leader of the Garde", inline=False)                       
            ncoEmbed.add_field(name="Fahnrich Mugi", value="Legere Leader, Minister of Security", inline=False)
            ncoEmbed.add_field(name="Sergeant-Major Ganthador", value="Artillerie Leader, Minister of Propaganda", inline=False)
            ncoEmbed.add_field(name="Sergeant-Major Taragorn", value="Infanterie Leader, Minister of Culture", inline=False)
            ncoEmbed.add_field(name="Sergeant Garfunkel", value="Garde Leader", inline=False)
            ncoEmbed.add_field(name="Sergeant 2big2bear13", value="Cavalerie Leader", inline=False)

            # Corporals ----------------------------------------------------
            cplEmbed=discord.Embed(title="Corporals", description="", color=0x1e39cd)
            cplEmbed.set_thumbnail(url="attachment://cpl.jpg")
            cplEmbed.add_field(name="Caporal-Fourrier Kruber", value="", inline=False)
            cplEmbed.add_field(name="Caporal-Fourrier Wogsauce", value="", inline=False)
            cplEmbed.add_field(name="Caporal-Fourrier Krizzle", value="", inline=False)
            cplEmbed.add_field(name="Caporal-Fourrier Pin0", value="", inline=False)
            cplEmbed.add_field(name="Caporal HelixOrion", value="", inline=False)
            cplEmbed.add_field(name="Caporal Fartic", value="", inline=False)
            cplEmbed.add_field(name="Caporal Kage", value="", inline=False)
            cplEmbed.add_field(name="Caporal Xander", value="", inline=False)
            cplEmbed.add_field(name="Caporal Gaming Rabbit", value="", inline=False)
            cplEmbed.add_field(name="Caporal Socturnan", value="", inline=False)


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
            await ctx.send(file=guardImg, embed=guardEmbed)
            await ctx.send(file=skirmImg, embed=skirmEmbed)
            await ctx.send(file=cavImg, embed=cavEmbed)
            await ctx.send(file=artyImg, embed=artyEmbed)
            await ctx.send(file=supportstaffImg, embed=supportstaffEmbed)

async def setup(bot):
    await bot.add_cog(enlistedCog(bot))
