from datetime import datetime
import discord
from discord.ext import commands
from discord.ext import tasks
from random import randint, choice
import asyncio
import varStore
import attendance

#from randomCmd import testMsg

class backgroundTasks(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        
    # Rotates the status
    @tasks.loop(seconds=60.0)
    async def statusRotation(self):
        statuses = ["_help", 
                    "Xander's cannon wipes", 
                    "Jungle bear the flag", 
                    "your teamkills", 
                    "your aim", 
                    "you spin",
                    "the Legere", 
                    "the Garde",  
                    "the Artillerie", 
                    "the Support Staff", 
                    "the Infanterie", 
                    "the Cavalerie", 
                    "Les cent Suisse",
                    "the Donations come in",
                    "Liberte News"]
        
        # Initialize current_time
        eventDays = [2, 4, 5]
        trainingDays = [5]
        now = datetime.now()
        current_time = now.strftime("%H:%M")

        holiday_start = datetime(2024, 12, 22)
        holiday_end = datetime(2025, 1, 7)
        if holiday_start <= now <= holiday_end:
            await self.bot.change_presence(activity=discord.Activity(type=discord.ActivityType.watching, name=f"{choice(statuses)}"))
            return

        await self.bot.change_presence(activity=discord.Activity(type=discord.ActivityType.watching, name=f"{choice(statuses)}"))

        # Auto leadership attendance ping
        if current_time == "13:00" and datetime.today().weekday() in eventDays:
            leadershipChannel = self.bot.get_channel(961625199109894144)

            embed = discord.Embed(title="Officer Attendance", description="Can you make it tonight? React with :thumbsup: or :thumbsdown:", color=0x109319)
            embed.add_field(name="Coming: ", value=f"No Officers attending! :(", inline=False)
            embed.add_field(name="Tonight's Officer Count: ", value=f"0", inline=False)
            embed.add_field(name="Not coming: ", value=f"No apologies received. :)", inline=False)
            embed.add_field(name="Tonight's Absent Count: ", value=f"0", inline=False)
            embed.add_field(name="Maybe coming/might be late: ", value=f"No timely attendance in doubt!", inline=False)
            embed.add_field(name="Count: ", value=f"0", inline=False)

            msg = await leadershipChannel.send(embed=embed)

            await msg.add_reaction("\N{THUMBS UP SIGN}")
            await msg.add_reaction("\N{THUMBS DOWN SIGN}")
            await msg.add_reaction("\N{SHRUG}")
            varStore.leaderPingMsgId = msg.id
            
    # Auto roll call
        elif current_time == "20:20" and datetime.today().weekday() in eventDays:
            vcCatId = 772918008737038367
            enlistedGuild = self.bot.get_guild(772917331235438654)
            vcChannelsIds = [channel.id for channel in enlistedGuild.voice_channels if channel.category_id == vcCatId]
            
            artyUsers = []
            guardUsers = []
            skirmUsers = []
            cavUsers = []
            otherUsers = []
            mercUsers = []

            artyRole = enlistedGuild.get_role(845614864629235712)
            guardRole = enlistedGuild.get_role(802900303648653322)
            skirmRole = enlistedGuild.get_role(826778081531658280)
            cavRole = enlistedGuild.get_role(973152930330968094)
            mercRole = enlistedGuild.get_role(773055184049405974)

            totalUsers = 0

            for channelId in vcChannelsIds:
                channel = self.bot.get_channel(channelId)
                if channel:
                    totalUsers += len(channel.members)
                    for member in channel.members:
                        if artyRole in member.roles:
                            artyUsers.append(member.display_name)
                        elif guardRole in member.roles:
                            guardUsers.append(member.display_name)
                        elif skirmRole in member.roles:
                            skirmUsers.append(member.display_name)
                        elif cavRole in member.roles:
                            cavUsers.append(member.display_name)
                        elif mercRole in member.roles:
                            mercUsers.append(member.display_name)
                        else:
                            otherUsers.append(member.display_name)

            logbookChannel = self.bot.get_channel(772919594016571442)

            embed=discord.Embed(title="3e Event Attendance - AUTOMATIC REPORT ONLY, NO LOGBOOK CHANGES!", description="", color=0x151798)
            embed.add_field(name="Total Attendance", value=f"{totalUsers}", inline=False)
            embed.add_field(name="Cannon Crew (Total: {})".format(len(artyUsers)), value=", ".join(artyUsers), inline=False)
            embed.add_field(name="Cavalry (Total: {})".format(len(cavUsers)), value=", ".join(cavUsers), inline=False)
            embed.add_field(name="Guards (Total: {})".format(len(guardUsers)), value=", ".join(guardUsers), inline=False)
            embed.add_field(name="Skirmishers (Total: {})".format(len(skirmUsers)), value=", ".join(skirmUsers), inline=False)
            embed.add_field(name="Line & Support Staff (Total: {})".format(len(otherUsers)), value=", ".join(otherUsers), inline=False)
            embed.add_field(name="Mercenaries (Total: {})".format(len(mercUsers)), value=", ".join(mercUsers), inline=False)
            await logbookChannel.send(embed=embed)

        elif current_time == "19:20" and datetime.today().weekday() in trainingDays:
            vcCatId = 772918008737038367
            enlistedGuild = self.bot.get_guild(772917331235438654)
            vcChannelsIds = [channel.id for channel in enlistedGuild.voice_channels if channel.category_id == vcCatId]
            
            artyUsers = []
            guardUsers = []
            skirmUsers = []
            cavUsers = []
            otherUsers = []
            mercUsers = []

            artyRole = enlistedGuild.get_role(845614864629235712)
            guardRole = enlistedGuild.get_role(802900303648653322)
            skirmRole = enlistedGuild.get_role(826778081531658280)
            cavRole = enlistedGuild.get_role(973152930330968094)
            mercRole = enlistedGuild.get_role(773055184049405974)

            totalUsers = 0

            for channelId in vcChannelsIds:
                channel = self.bot.get_channel(channelId)
                if channel:
                    totalUsers += len(channel.members)
                    for member in channel.members:
                        if artyRole in member.roles:
                            artyUsers.append(member.display_name)
                        elif guardRole in member.roles:
                            guardUsers.append(member.display_name)
                        elif skirmRole in member.roles:
                            skirmUsers.append(member.display_name)
                        elif cavRole in member.roles:
                            cavUsers.append(member.display_name)
                        elif mercRole in member.roles:
                            mercUsers.append(member.display_name)
                        else:
                            otherUsers.append(member.display_name)

            logbookChannel = self.bot.get_channel(772919594016571442)

            embed=discord.Embed(title="3e Training Attendance - AUTOMATIC REPORT ONLY, NO LOGBOOK CHANGES!", description="", color=0x151798)
            embed.add_field(name="Total Attendance", value=f"{totalUsers}", inline=False)
            embed.add_field(name="Cannon Crew (Total: {})".format(len(artyUsers)), value=", ".join(artyUsers), inline=False)
            embed.add_field(name="Cavalry (Total: {})".format(len(cavUsers)), value=", ".join(cavUsers), inline=False)
            embed.add_field(name="Guards (Total: {})".format(len(guardUsers)), value=", ".join(guardUsers), inline=False)
            embed.add_field(name="Skirmishers (Total: {})".format(len(skirmUsers)), value=", ".join(skirmUsers), inline=False)
            embed.add_field(name="Line & Support Staff (Total: {})".format(len(otherUsers)), value=", ".join(otherUsers), inline=False)
            embed.add_field(name="Mercenaries (Total: {})".format(len(mercUsers)), value=", ".join(mercUsers), inline=False)
            await logbookChannel.send(embed=embed)
            
    @tasks.loop(seconds=5)
    async def rgb(self):
        while True:
            await self.bot.change_presence(status=discord.Status.idle)
            await asyncio.sleep(5)
            await self.bot.change_presence(status=discord.Status.dnd)
            await asyncio.sleep(5)
            await self.bot.change_presence(status=discord.Status.online)
            await asyncio.sleep(5)
            
    @commands.Cog.listener()
    async def on_ready(self):
        self.statusRotation.start()
        print("Background tasks started")
        
async def setup(bot):
    await bot.add_cog(backgroundTasks(bot))
