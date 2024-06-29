import discord
import re
import json
from util_message import send_msg, send_embed
import Common
from util import missing_set_nicks, member_has_roles



#warnlist
async def warnlist(msg_channel: discord.TextChannel, event_bot_id, role_ids):
  missing_set = await missing_set_nicks(msg_channel, event_bot_id, role_ids)
  display_message = ""

  for member in msg_channel.members:
      if not member.bot and not member_has_roles(member, role_ids):
        if(member.id in missing_set):
            display_message = display_message + member.display_name + '\n'

  await send_embed(msg_channel, "Wall of Shame: ", display_message,
                   discord.Color.green())

#warnping
async def warnping(msg_channel: discord.TextChannel, event_bot_id, role_ids):
  missing_set = await missing_set_nicks(msg_channel, event_bot_id, role_ids)
  display_message = ""
  for member in msg_channel.members:
    if not member.bot and not member_has_roles(member, role_ids):
      if(member.id in missing_set):
        display_message = display_message + member.mention
  display_message = display_message + ""
  await send_msg(msg_channel, display_message) 


#Apollo message w/ 1 accepted but no declines
# <Message id=1149152753667543050 channel=<TextChannel id=1149152500927172719 name='testing-channel' position=41 nsfw=False news=False category_id=1134971309802143784> type=<MessageType.default: 0> author=<Member id=475744554910351370 name='Apollo' global_name=None bot=True nick=None guild=<Guild id=1133496553072492654 name='BLOOD EAGLES' shard_id=0 chunked=True member_count=155>> flags=<MessageFlags value=0>>
# {'footer': {'text': 'Created by Zenegrad'
#     }, 'fields': [
#         {'name': 'Time', 'value': '<t: 1694067760:F>\n<:countdown: 878391707727716413> <t: 1694067760:R>', 'inline': False
#         },
#         {'name': 'Links', 'value': '[Add to Google Calendar
#             ](http: //www.google.com/calendar/event?action=TEMPLATE&text=test&details=&location=&dates=20230907T062240Z/20230907T062240Z)', 'inline': False}, {'name': '<:accepted:713124484436983971> Accepted (1)', 'value': '>>> Zenegrad', 'inline': True}, {'name': '<:declined:713124484688642068> Declined', 'value': '-', 'inline': True}, {'name': '<:tentative:713214962641666109> Tentative', 'value': '-', 'inline': True}], 'color': 15844367, 'type': 'rich', 'title': 'test'}

#Apollo message w/ 1 accepted & 1 declined
# <Message id=1149152753667543050 channel=<TextChannel id=1149152500927172719 name='testing-channel' position=41 nsfw=False news=False category_id=1134971309802143784> type=<MessageType.default: 0> author=<Member id=475744554910351370 name='Apollo' global_name=None bot=True nick=None guild=<Guild id=1133496553072492654 name='BLOOD EAGLES' shard_id=0 chunked=True member_count=155>> flags=<MessageFlags value=0>>
# {'footer': {'text': 'Created by Zenegrad'}, 'fields': [{'name': 'Time', 'value': '<t:1694067760:F>\n<:countdown:878391707727716413> <t:1694067760:R>', 'inline': False}, {'name': 'Links', 'value': '[Add to Google Calendar](http://www.google.com/calendar/event?action=TEMPLATE&text=test&details=&location=&dates=20230907T062240Z/20230907T062240Z)', 'inline': False}, {'name': '<:accepted:713124484436983971> Accepted (1)', 'value': '>>> Zenegrad', 'inline': True}, {'name': '<:declined:713124484688642068> Declined (1)', 'value': '>>> 『BΞ』Miralay', 'inline': True}, {'name': '<:tentative:713214962641666109> Tentative', 'value': '-', 'inline': True}], 'color': 15844367, 'type': 'rich', 'title': 'test'}

#<Message id=1149152753667543050 channel=<TextChannel id=1149152500927172719 name='testing-channel' position=41 nsfw=False news=False category_id=1134971309802143784> type=<MessageType.default: 0> author=<Member id=475744554910351370 name='Apollo' global_name=None bot=True nick=None guild=<Guild id=1133496553072492654 name='BLOOD EAGLES' shard_id=0 chunked=True member_count=155>> flags=<MessageFlags value=0>>
#{'footer': {'text': 'Created by Zenegrad'}, 'fields': [{'name': 'Time', 'value': '<t:1694067760:F>\n<:countdown:878391707727716413> <t:1694067760:R>', 'inline': False}, {'name': 'Links', 'value': '[Add to Google Calendar](http://www.google.com/calendar/event?action=TEMPLATE&text=test&details=&location=&dates=20230907T062240Z/20230907T062240Z)', 'inline': False}, {'name': '<:accepted:713124484436983971> Accepted (2)', 'value': '>>> Zenegrad\n『BΞ』Miralay', 'inline': True}, {'name': '<:declined:713124484688642068> Declined', 'value': '-', 'inline': True}, {'name': '<:tentative:713214962641666109> Tentative', 'value': '-', 'inline': True}], 'color': 15844367, 'type': 'rich', 'title': 'test'}