
import os
from datetime import datetime, date, time
import random
from discord.ext import commands
import re
import json
from cryptography.fernet import Fernet


with open('enc.json','rb') as f:
    data = f.read()
    key = Fernet(os.getenv("FERNETKEY"))
    file_data = key.decrypt(data)
fireDict = json.loads(file_data)

# Firebase
import firebase_admin
from firebase_admin import credentials
from firebase_admin import db

cred = credentials.Certificate(fireDict)
firebase_admin.initialize_app(cred, {'databaseURL': 'https://reminderbot-d9927-default-rtdb.asia-southeast1.firebasedatabase.app'})
print("firebase initialized")

ref = db.reference('reminderList')
date_ref = ref.child('dates')


#variables
today_date = date.today()


# Bot commands
bot = commands.Bot(command_prefix='$')
@bot.command(name='hello')
async def greeting(ctx):
  greeting_quotes = ["Hello there!", " Good Day!"]
  response = random.choice(greeting_quotes)
  await ctx.send(response)



@bot.command(name='remindme')
async def remindSet(ctx):
  await ctx.send("Enter a Time and Date as YYYY-MM-DD hh:mm ")
  def check(msg):
    return msg.author == ctx.author and msg.channel == ctx.channel
  msg = await bot.wait_for("message", check=check)
  

  # Extract date and time and title from userinputs
  match_str_date = re.search(r'\d{4}-\d{2}-\d{2}', msg.content)
  my_date = datetime.strptime(match_str_date.group(), '%Y-%m-%d').date()
  match_str_time = re.search(r'\d{2}:\d{2}',msg.content)
  my_time = datetime.strptime(match_str_time.group(), '%H:%M').time()
  # combine into datetime
  my_datetime = datetime.combine(my_date,my_time)
  

  def substring_after(s, delim):
    return s.partition(delim)[2]
  my_title = substring_after(msg.content, "Title:")
  
  
  # upload to db after checking
  if(my_date < today_date):
    await ctx.send("Invalid Date")
  else:
    await ctx.send("Date: " + str(my_date) + "  Time: " + str(my_time))
    date_ref.set({
      str(my_date) : {
        'alertDateTime' : my_datetime.isoformat(),
        'alertTitle': my_title

      }
    })



bot.run(os.getenv('TOKEN'))
