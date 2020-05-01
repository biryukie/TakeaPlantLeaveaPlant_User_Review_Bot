## bot.py
#import os
#import random

#import discord

#credentials = open(open("locd.txt", "r").readline().strip(), "r")

#TOKEN = credentials.readline().strip()

#client = discord.Client()

#@client.event
#async def on_ready():
#    print(client.user.name + " has connected to Discord!")

#@client.event
#async def on_message(message):
#	# Make sure it's not recursive
#    if message.author == client.user:
#        return

#    if message.content == 'Hi!':
#        await message.channel.send("Beep boop!!")

#client.run(TOKEN)

# bot.py
import os

import discord
from discord.ext import commands

credentials = open(open("locd.txt", "r").readline().strip(), "r")

TOKEN = credentials.readline().strip()

bot = commands.Bot(command_prefix='')

@bot.command(name='input')
@commands.has_role('plantfriend')
async def inputReview(ctx, username: str, rating: int, url: str):
	await ctx.send("Success! Username = " + username + ", rating = " + str(rating) + ", url = " + url)

@inputReview.error
async def inputReviewError(ctx, error):
    if isinstance(error, commands.errors.CheckFailure):
        await ctx.send("Sorry, you don't have permissions!")
    if isinstance(error, commands.errors.MissingRequiredArgument):
        await ctx.send("You are missing an argument:\n`input` `USERNAME` `RATING` `URL`.")
    if isinstance(error, commands.errors.BadArgument):
        await ctx.send("Ensure correct format:\n`input` `USERNAME` `RATING` `URL`.")

bot.run(TOKEN)

