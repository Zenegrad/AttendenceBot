import os
import discord
from util_warnlist import warnlist, warnping
import Common
from discord import app_commands
from discord.ext import commands
import Config

intents = discord.Intents().all()
#client = discord.Client(intents=intents)
#tree = app_commands.CommandTree(client)
bot = commands.Bot(command_prefix="/", intents=intents)

event_bot_id = None

token = Config.token


# @bot.event
# async def on_message(message):
#   if message.author == bot.user:
#     return
#   if not message.guild:
#     return
#   msg_channel = message.channel
#   clan_reps_role = 284108903858438155
#   blood_eagles_role = 1140038135904997388
#   friend_of_rat_role = 1137088085889384509
#   test_role = 984130470671450203
#   if message.content.startswith("warnlist"):
#     await warnlist(msg_channel, event_bot_id, [clan_reps_role, blood_eagles_role, friend_of_rat_role, test_role])
#   # elif message.content.startswith("warnping"):
#   #   await warnping(msg_channel, event_bot_id, [clan_reps_role, blood_eagles_role, friend_of_rat_role, test_role])


@bot.tree.command(
    name="generate",
    description="Syncs bot to take care of this event for you."
)
async def slash_generate(interaction: discord.Interaction):
  text_channel: discord.TextChannel = bot.get_channel(interaction.channel_id)
  event_bot_id = check_bot_type(text_channel)

@bot.tree.command(
    name="warnping",
    description="Sends a ping to all members not signed up.",
)
async def slash_warnping(interaction: discord.Interaction):
  text_channel: discord.TextChannel = bot.get_channel(interaction.channel_id)
  event_bot_id = check_bot_type(text_channel)
  
  roles = [984130470671450203]
  await interaction.response.send_message("Please react Yes/No to the event")
  await warnping(text_channel, event_bot_id, roles)


@bot.tree.command(
    name="warnlist",
    description="Sends a ping to all members not signed up.",
)
async def slash_warnping(interaction: discord.Interaction):
  text_channel: discord.TextChannel = bot.get_channel(interaction.channel_id)
  event_bot_id = check_bot_type(text_channel)
  
  roles = [984130470671450203]
  await interaction.response.send_message("Members not reacted: ")
  await warnlist(text_channel, event_bot_id, roles)


def check_bot_type(msg_channel: discord.TextChannel):
  for member in msg_channel.members:
      if member.bot:
        if member.id == Common.APOLLO_ID:
          return Common.APOLLO_ID
        elif member.id == Common.SESH_ID:
          return Common.SESH_ID
        
  print("could not identify bot")
  return "bot not found"

@bot.event
async def on_ready():
  await bot.change_presence(status=discord.Status.online)
  await bot.tree.sync(guild=discord.Object(id=945811633471639552))
  print('We have logged in as {0.user}'.format(bot))

bot.run(token) 