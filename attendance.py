import discord
from discord import Embed
from discord.ext import commands
import gspread
import googleapiclient
from googleapiclient.errors import HttpError
from datetime import datetime
import logging
import asyncio
import os


import random
from random import randint


# Initialize logging
logging.basicConfig(level=logging.INFO)

# Grab SPREADSHEET_KEY
SPREADSHEET_KEY = os.getenv("SPREADSHEET_KEY")   # <- read key from env
if not SPREADSHEET_KEY:
    raise RuntimeError("Missing SPREADSHEET_KEY environment variable")

# Service Account to Access Logbook
gc = gspread.service_account(filename='/home/container/storage/e-logbook-420412-0954626b746a.json')
sh = gc.open_by_key(SPREADSHEET_KEY)

class attendanceCog(commands.Cog):
    def __init__(self, bot:commands.Bot):
        self.bot = bot

    @commands.has_any_role(
        772921452135055360, 772921453095944203, 772921882072449075, 772921877953904661
    )
    @commands.group(pass_context=True, aliases=["Logbook"], invoke_without_subcommand=True)
    async def logbook(self, ctx):
        if ctx.invoked_subcommand is None:
            await ctx.reply("No subcommand specified - specify event, training, promotions, or report")
            return

    @logbook.command(name="report", aliases=["Report"])
    async def attendance(self, ctx):
        try:
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
            embed = discord.Embed(title="3e Attendance - REPORT ONLY, NO LOGBOOK CHANGES!", color=0x151798)
            embed.add_field(name="Total Attendance", value=f"{totalUsers}", inline=False)
            embed.add_field(name="Cannon Crew (Total: {})".format(len(artyUsers)), value=", ".join(artyUsers), inline=False)
            embed.add_field(name="Cavalry (Total: {})".format(len(cavUsers)), value=", ".join(cavUsers), inline=False)
            embed.add_field(name="Guards (Total: {})".format(len(guardUsers)), value=", ".join(guardUsers), inline=False)
            embed.add_field(name="Skirmishers (Total: {})".format(len(skirmUsers)), value=", ".join(skirmUsers), inline=False)
            embed.add_field(name="Line & Support Staff (Total: {})".format(len(otherUsers)), value=", ".join(otherUsers), inline=False)
            embed.add_field(name="Mercenaries (Total: {})".format(len(mercUsers)), value=", ".join(mercUsers), inline=False)
            await logbookChannel.send(embed=embed)
        except Exception as e:
            logging.error(f"Error in attendance reporting: {str(e)}")
            await ctx.reply("Failed to generate the attendance report. Please try again later.")

    @logbook.command(name="promotions", aliases=["Promotions"])
    async def promotions(self, ctx):
        try:
            # Define the worksheet
            enlisted_sheet = sh.worksheet('Officer Corps and Enlisted')
        
            # Define the rank requirements
            rank_requirements = {
                "Recrue.": {"linebattles": 0, "trainings": 1, "next_rank": "Cadet."},
                "Cadet.": {"linebattles": 6, "trainings": 2, "next_rank": "Soldat."},
                "Soldat.": {"linebattles": 12, "trainings": 4, "next_rank": "Fusilier."},
                "Fusilier.": {"linebattles": 18, "trainings": 8, "next_rank": "Grenadier."},
                "Grenadier.": {"linebattles": 36, "trainings": 16, "next_rank": "Grenadier de Premier."},
                "Grenadier de Premier.": {"linebattles": float('inf'), "trainings": float('inf'), "next_rank": None}
            }

            # Initialize list for promotions
            users_due_for_promotion = []

            # Fetch all values from the sheet
            values = enlisted_sheet.get_all_values()
            headers = values[0]
            rank_col = headers.index('Rank')  # Assuming the column header is 'Rank'
            training_col = headers.index('Trainings')
            linebattle_col = headers.index('Line Battles')
            name_col = headers.index('Name')

            for i, row in enumerate(values[1:], start=2):  # Start at row 2 (first data row)
                rank = row[rank_col]
                if rank in rank_requirements:
                    # Handle empty string by defaulting to 0
                    trainings = int(row[training_col]) if row[training_col].isdigit() else 0
                    linebattles = int(row[linebattle_col]) if row[linebattle_col].isdigit() else 0
                    requirements = rank_requirements[rank]
                    if trainings >= requirements['trainings'] and linebattles >= requirements['linebattles']:
                        users_due_for_promotion.append({
                            "name": row[name_col],
                            "current_rank": rank,
                            "next_rank": requirements['next_rank']
                        })
                        # Mark the cell for promotion
                        enlisted_sheet.format(f'H{i}', {"backgroundColor": {"red": 0.27, "green": 0.45, "blue": 0.77}})

            # Create an embed to display the users due for promotion
            if users_due_for_promotion:
                embed = discord.Embed(title="Enlisted Due for Promotion", color=0x0000FF)
                for user in users_due_for_promotion:
                    embed.add_field(name=user['name'], value=f"{user['current_rank']} -> {user['next_rank']}", inline=False)
                await ctx.send(embed=embed)
            else:
                await ctx.send("No users are currently due for promotion.")

        except Exception as e:
            logging.error(f"Error checking for promotions: {str(e)}")
            await ctx.send("Failed to check for promotions. Please try again later.")

    @logbook.command(name="event", aliases=["Event"])
    async def fill_event(self, ctx):
        # Ask for confirmation
        confirm = await self.confirm_action(ctx, "Event")
        if confirm:
            await self.fill_attendance(ctx, "Event")
    
    @logbook.command(name="training", aliases=["Training"])
    async def fill_training(self, ctx):
        # Ask for confirmation
        confirm = await self.confirm_action(ctx, "Training")
        if confirm:
            await self.fill_attendance(ctx, "Training")

    async def confirm_action(self, ctx, attendance_type):
        # Send confirmation message
        message = await ctx.send(f"Are you sure you want to take {attendance_type} attendance? Confirm that the attendance type is correct, and that it hasn't been taken already. React with \N{WHITE HEAVY CHECK MARK} to confirm.")
        await message.add_reaction("\N{WHITE HEAVY CHECK MARK}")
        await message.add_reaction("\N{CROSS MARK}")

        def check(reaction, user):
            # Make sure that the reaction is on the correct message and the user is the one who invoked the command
            return user == ctx.author and reaction.message.id == message.id and str(reaction.emoji) in ['\N{WHITE HEAVY CHECK MARK}', '\N{CROSS MARK}']

        try:
            reaction, user = await self.bot.wait_for('reaction_add', timeout=60.0, check=check)
        except asyncio.TimeoutError:
            await ctx.send('Confirmation timed out.')
            return False
        else:
            if reaction.emoji == '\N{WHITE HEAVY CHECK MARK}':
                return True
            else:
                await ctx.send('Action cancelled.')
                return False

    async def fill_attendance(self, ctx, attendance_type):
        try:
            start = datetime.now()
            msg = await ctx.send(f"Filling out the logbook for {attendance_type} attendance now...")
            vc_cat_id = 772918008737038367
            guild = self.bot.get_guild(772917331235438654)

            # Check for the roles that determine the worksheet
            high_command_role = ctx.guild.get_role(772921452135055360)
            support_specialists_role = ctx.guild.get_role(772922207760416829)
            enlisted_role = ctx.guild.get_role(772922211933224960)

            # Define the worksheets
            enlisted_sheet = sh.worksheet('Officer Corps and Enlisted')
            high_command_sheet = sh.worksheet('High Command')
            support_specialists_sheet = sh.worksheet('Regimental Auxiliary Specialists')

            # Dictionary to store the sheets for easy access
            sheets = {
                'High Command': high_command_sheet,
                'Officer Corps and Enlisted': enlisted_sheet,
                'Regimental Auxiliary Specialists': support_specialists_sheet
            }

            column = 'E' if attendance_type == "Event" else 'D'
            missing_users = []

            # Prepare to gather all Discord IDs for batch fetching
            discord_ids = {
                'High Command': [],
                'Officer Corps and Enlisted': [],
                'Regimental Auxiliary Specialists': []
            }

            for vc in guild.voice_channels:
                if vc.category_id == vc_cat_id:
                    for member in vc.members:
                        if high_command_role in member.roles and enlisted_role in member.roles:
                            discord_ids['High Command'].append(str(member.id))
                        elif support_specialists_role in member.roles and enlisted_role in member.roles:
                            discord_ids['Regimental Auxiliary Specialists'].append(str(member.id))
                        elif enlisted_role in member.roles and high_command_role not in member.roles and support_specialists_role not in member.roles:
                            discord_ids['Officer Corps and Enlisted'].append(str(member.id))

            # Batch fetch all values in one go
            for sheet_name, ids in discord_ids.items():
                if ids:
                    worksheet = sheets[sheet_name]
                    values = worksheet.get_all_values()
                
                    # Identify the correct column index for 'Discord User ID'
                    headers = values[0]
                    discord_id_col = headers.index('Discord User ID')
                
                    # Create a dictionary to map Discord IDs to row numbers
                    id_to_row = {str(values[row][discord_id_col]): row + 1 for row in range(1, len(values))}

                    # Prepare batch updates
                    batch_updates = []
                    for discord_id in ids:
                        if discord_id in id_to_row:
                            row = id_to_row[discord_id]
                            target_cell_value = values[row-1][ord(column.upper()) - ord('A')]
                            current_value = int(target_cell_value) if target_cell_value.isdigit() else 0
                            new_value = current_value + 1
                            batch_updates.append({
                                'range': f'{column}{row}',
                                'values': [[new_value]]
                            })
                        else:
                            missing_users.append(f"ID: {discord_id}")

                    # Perform batch update
                    if batch_updates:
                        retries = 0
                        while batch_updates:
                            batch = batch_updates[:100]
                            try:
                                worksheet.batch_update(batch)
                                batch_updates = batch_updates[100:]
                            except HttpError as e:
                                if e.resp.status in [429, 500, 503]:
                                    await asyncio.sleep(2 ** retries + randint(0, 1000) / 1000)
                                    retries += 1
                                    logging.warning(f"Retrying batch update due to API error: {str(e)}")
                                else:
                                    logging.error(f"Failed to update due to API error: {str(e)}")
                                    raise

            end = datetime.now()
            time_taken = end - start
            await msg.edit(content=f"{attendance_type} Attendance updated successfully in {time_taken}!")

            if missing_users:
                await ctx.send(f"**WARNING**: Could not find logbook entries for the following users: {', '.join(missing_users)}")
        except Exception as e:
            logging.error(f"Error updating attendance for {attendance_type}: {str(e)}")
            await msg.edit(content=f"**Failed to update {attendance_type} attendance. Please try again later.**")
        
    # Adding a new command group for '_attendance'
    @commands.group(name="attendance", invoke_without_command=True)
    async def attendance_group(self, ctx):
        if ctx.invoked_subcommand is None:
            await ctx.send("No subcommand specified. Try _attendance check @user")

    @attendance_group.command(name="check")
    async def attendance_events(self, ctx, member: discord.Member):
        # Extract the Discord ID of the pinged user
        discord_id = str(member.id)

        # Define the worksheets
        try:
            enlisted_sheet = sh.worksheet('Officer Corps and Enlisted')
            high_command_sheet = sh.worksheet('High Command')
            support_specialists_sheet = sh.worksheet('Regimental Auxiliary Specialists')
        except gspread.WorksheetNotFound:
            await ctx.send("Error: Worksheet not found - notify an Officer.")
            return

        # Initialize counters for totals
        total_line_battles = 0
        total_trainings = 0
        total_events = 0
        recruitment_date = None
        time_since_joining = ""

        # Define the sheets to loop through
        sheets = [high_command_sheet, enlisted_sheet, support_specialists_sheet]
        user_found = False  # Track if the user is found in any sheet

        # Search for the Discord ID and fetch event counts and recruit date
        for sheet in sheets:
            try:
                cell = sheet.find(discord_id)  # Find the Discord ID in the sheet
                if cell:
                    user_found = True
                    line_battles = sheet.cell(cell.row, 5).value or 0  # Column E is the 5th column
                    trainings = sheet.cell(cell.row, 4).value or 0  # Column D is the 4th column
                    total_events_count = sheet.cell(cell.row, 6).value or 0  # Column F is the 6th column
                    date_string = sheet.cell(cell.row, 11).value  # Column K is the 11th column

                    # Sum the counts from each sheet
                    total_line_battles += int(line_battles)
                    total_trainings += int(trainings)
                    total_events += int(total_events_count)

                    if date_string:
                        recruitment_date = datetime.strptime(date_string, '%d/%m/%Y')
                        days_since = (datetime.now() - recruitment_date).days
                        time_since_joining = f"This member was recruited on {date_string}. Wow, that's {days_since} days since joining!"
                    else:
                        time_since_joining = "Recruitment date unknown."
            except gspread.CellNotFound:
                continue  # Skip to the next sheet if not found

        if not user_found:
            await ctx.send(f"No entry for {member.display_name} found in the logbook - contact an Officer.")
            return

        # Create an Embed message
        embed = Embed(title=f"Attendance Check for {member.display_name}",
                    color=0xadd8e6,  # Light Blue
                    description="")
        embed.add_field(name="Line Battles", value=total_line_battles, inline=False)
        embed.add_field(name="Trainings", value=total_trainings, inline=False)
        embed.add_field(name="Total Events", value=total_events, inline=False)
        embed.add_field(name="Recruitment Details", value=time_since_joining, inline=False)
        embed.set_footer(text="Source: 3e Logbook")

        await ctx.send(embed=embed)

async def setup(bot:commands.Bot):
    await bot.add_cog(attendanceCog(bot))
