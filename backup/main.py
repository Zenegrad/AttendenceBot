import os
import discord
from util_warnlist import warnlist, warnping

intents = discord.Intents().all()
client = discord.Client(intents=intents)
token = "MTE0OTAzOTY0MTY2NDY4ODI0OA.GF_0Qw.WVWsDeBX5bTR3VdgrT8p3MNtjSRexZBm2aWIrU"

@client.event
async def on_ready():
  print('We have logged in as {0.user}'.format(client))

@client.event
async def on_message(message):
  if message.author == client.user:
    return
  if not message.guild:
    return
  msg_channel = message.channel
  event_bot_id = check_bot_type(msg_channel)
  clan_reps = 284108903858438155
  blood_eagles_role = 1140038135904997388
  friend_of_rat_role = 1137088085889384509
  if message.content.startswith("warnlist"):
    await warnlist(msg_channel, event_bot_id, [clan_reps, blood_eagles_role, friend_of_rat_role])
  elif message.content.startswith("warnping"):
    await warnping(msg_channel, event_bot_id, [clan_reps, blood_eagles_role, friend_of_rat_role])

def check_bot_type(msg_channel):
  for member in msg_channel.members:
      if member.bot:
        if member.id == 475744554910351370:
          return 475744554910351370
        elif member.id == 616754792965865495:
          return 616754792965865495
        
  print("could not identify bot")
  return "bot not found"

client.run(token) 
