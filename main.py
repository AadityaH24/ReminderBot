
import os
from datetime import datetime
import random
from discord.ext import commands
import re

bot = commands.Bot(command_prefix='$')
@bot.command(name='hello')
async def greeting(ctx):
  greeting_quotes = ["Hello there!", " Good Day!"]
  response = random.choice(greeting_quotes)
  await ctx.send(response)

@bot.command(name = 'remindme')
async def reminder(ctx):
  response = "Set Reminder Time and Date"
  await ctx.send(response)


@bot.command(name='input')
async def getDateTime(ctx):
  await ctx.send("Enter a Time and Date as YYYY-MM-DD hh:mm ")
  def check(msg):
    return msg.author == ctx.author and msg.channel == ctx.channel
  msg = await bot.wait_for("message", check=check)
  
  # Extract date and time from userinput
  match_str_date = re.search(r'\d{4}-\d{2}-\d{2}', msg.content)
  my_date = datetime.strptime(match_str_date.group(), '%Y-%m-%d').date()
  match_str_time = re.search(r'\d{2}:\d{2}',msg.content)
  my_time = datetime.strptime(match_str_time.group(), '%H:%M').time()
  
  await ctx.send("Date: " + str(my_date) + "  Time: " + str(my_time))
#sample textasda

bot.run(os.getenv('TOKEN'))
