import json
import discord
from discord.ext import commands
import varStore
import requests
from random import randint, choice
import asyncio
from dotenv import load_dotenv
from os import getenv
import os
import time
import json
from urllib.request import urlopen
import re

        
class randomCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        
    #Testing ping command with latency
    @commands.is_owner()
    @commands.cooldown(1, 1, commands.BucketType.user)
    @commands.command(aliases=["pong", "Ping", "Pong"])
    async def ping(self,ctx):
        if ctx.invoked_with == "ping":
            start_time = time.time()
            message = await ctx.send("Testing Ping...")
            end_time = time.time()

            await message.edit(content=f"Pong!\nResponse Time: {round(self.bot.latency * 1000)}ms\nAPI Latency: {round(((end_time - start_time)-self.bot.latency) * 1000)}ms\nTotal Latency: {round((end_time - start_time) * 1000)}ms")
            #await ctx.reply(f"Pong! (Response time: {round(self.bot.latency*1000, 2)}ms)")
        elif ctx.invoked_with == "pong":
            start_time = time.time()
            message = await ctx.send("Testing Pong...")
            end_time = time.time()

            await message.edit(content=f"Ping!\nResponse Time: {round(self.bot.latency * 1000)}ms\nAPI Latency: {round(((end_time - start_time)-self.bot.latency) * 1000)}ms\nTotal Latency: {round((end_time - start_time) * 1000)}ms")

    #Converts id to username
    @commands.cooldown(1, 1, commands.BucketType.user)
    @commands.command(aliases=["Username","user","User","name","Name"], pass_context=True)
    async def username(self, ctx, id: int):
        if len(str(id)) == 18:
            username = await self.bot.fetch_user(id)
            await ctx.reply(f"Discord Username is {username}")
        else:
            await ctx.reply("Invalid User ID! Try again.")
                
    #Converts user to id
    @commands.command(aliases=["ID","Id"])
    async def id(self, ctx, user: discord.User):
        await ctx.reply(f"User ID is {user.id}")
        
    #Send dm's through bot
    @commands.is_owner()
    @commands.command(aliases=["DM","Dm"])
    async def dm(self, ctx, user: discord.User, *, message):
        user = self.bot.get_user(user.id)
        await user.send(message)
        await ctx.reply("Message sent")
        
    #Echo command 
    @commands.command(aliases=["mirror","Mirror","Echo"])
    async def echo(self, ctx, *, message):
        if ctx.message.author.id in varStore.admins:
            try:
                await ctx.message.delete()
            finally:
                await ctx.send(message)
        else:
            await ctx.reply("Invalid perms", ephemeral=True)
        
    #Minecraft username to UUID
    @commands.cooldown(1, 1, commands.BucketType.user)
    @commands.command()
    async def mcid(self, ctx, username: str):
        response = requests.get(f"https://api.mojang.com/users/profiles/minecraft/{username}")

        if response.status_code == 200:
            await ctx.reply(f"The Minecraft UUID of the username is: {response.json()['id']}")
        elif response.status_code == 204:
            await ctx.reply("Username has not been used before")
        else:
            await ctx.reply(f"Error. Code {response.status_code}")
            
    #UUID to Past username
    @commands.command()
    async def mcname(self, ctx, uuid : str):
        data = requests.get(f"https://sessionserver.mojang.com/session/minecraft/profile/{uuid}").json()
        await ctx.reply(f"Minecraft username is: " + data["name"])

    #Fetch Avatar
    @commands.cooldown(1, 1, commands.BucketType.user)
    @commands.command(aliases=["Avatar","pfp"])
    async def avatar(self, ctx, *,  avamember : discord.Member=None):
        userAvatarUrl = avamember.avatar
        await ctx.send(userAvatarUrl)
        
    #Dice command with custom sides
    @commands.cooldown(1, 1, commands.BucketType.user)
    @commands.command(aliases=["Dice"])
    async def dice(self, ctx, num: int = None):
        if num is None or not isinstance(num, int) or num < 1:
            await ctx.send("Please enter a valid positive integer for the number of sides on the dice.")
        else:
            dice_roll = randint(1, num)
            await ctx.reply(f"You've rolled a {dice_roll} out of {num} sides")
    
    #Eight ball
    @commands.cooldown(1, 1, commands.BucketType.user)
    @commands.command(name = "eightball", aliases=["EightBall","8ball"])
    async def  eightball(self, ctx:commands.Context):
        msgs = ["It is certain.", "It is decidedly so.","Without a doubt.","Yes definitely.","You may rely on it","As I see it, yes.","Most likely.","Outlook good.","Yes.","Signs point to yes","Reply hazy, try again.","Ask again later.","Better not tell you now.","Cannot predict now.","Concentrate and ask again","Don't count on it.","My reply is no.","My sources say no.","Outlook not so good.", "Very doubtful."]
        choice = randint(0, len(msgs)-1)
        await ctx.reply(msgs[choice])
            
    @commands.command(name = "github", aliases=["git","Git", "GitHub"])
    @commands.cooldown(1, 5, commands.BucketType.user)
    async def github(self, ctx:commands.Context):
        await ctx.reply("This bot was originally developed by SoulWarden and is available in its original form on GitHub: https://github.com/SoulWarden1/IFF-Bot")
        
    @commands.hybrid_command(name = "xkcd", description='Grabs a XKCD comic')
    @commands.cooldown(1, 5, commands.BucketType.user)
    async def xkcd_command(self, ctx: commands.Context, comic_num: int = commands.parameter(default = None, description ="Optionally input the comic number you're after")) -> None:
        if comic_num is None: 
            xkcdUrl = "https://xkcd.com/info.0.json"
        else: 
            try:
                xkcdUrl = f"https://xkcd.com/{comic_num}/info.0.json "
            except:
                await ctx.send("An invalid comic number was inputted")
            
        response = urlopen(xkcdUrl)
        xkcdData = json.loads(response.read())
        await ctx.send(f"#{xkcdData.get('num')} {xkcdData.get('title')}\n{xkcdData.get('alt')}\n{xkcdData.get('img')}")
    
    @commands.command(name = "math")
    @commands.cooldown(1, 3, commands.BucketType.user)
    async def math(self, ctx, *, equation: str = None):
        if equation is None:
            await ctx.send("Please enter an equation...")
            return

        # Validate the equation to only contain numbers and operators +, -, *, /
        if not re.match(r"^[0-9\+\-\*\/\(\) ]+$", equation):
            await ctx.send("Please enter a valid equation using only numbers and +, -, *, / operators.")
            return

        # Attempt to evaluate the equation safely
        try:
            result = eval(equation)
            await ctx.send(f"The result is: {result}")
        except Exception as e:
            await ctx.send("There was an error evaluating your equation. Please check your syntax!")
    
async def setup(bot):
    await bot.add_cog(randomCog(bot))
