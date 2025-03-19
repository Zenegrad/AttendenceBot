import discord
import re
import json
from util_message import send_msg, send_embed

#returns true if member has any of the given roles
def member_has_roles(member, role_ids):
  for role in member.roles:
    if role.id in role_ids:
      return True
  return False



#computes the members who haven't voted in the event except for bots and retireds and mercs
async def missing_set_nicks(event_channel, event_bot_id, role_ids):
  event_message = None
  
  final_accepted = []
  final_declined = []
  accepted_set = set()
  declined_set = set()
  total_set = set()

  async for m in event_channel.history(limit=500):
    if event_bot_id == m.author.id:
      event_message = m
  
  if event_message:

    
    
    #print(event_message)
    embed = event_message.embeds[0]
    d = embed.to_dict()

    if "google.com/calendar" in str(d):
          d_str = re.sub('(\(http:.*?\))','',str(d))
          
          #replace ' with "
          p = re.compile('(?<!\\\\)\'')
          d_str = p.sub('\"', d_str)
          
          d_str = d_str.replace("False", "\"False\"")
          d_str = d_str.replace("True", "\"True\"")
          
          d = json.loads(d_str)
          
    print(d)
    #print(d)

    # Sesh
    if event_bot_id == 616754792965865495:
      accepted_msg = d['fields'][1]['name'].lstrip()
      declined_msg = d['fields'][3]['name'].lstrip()
      accepted_list = d['fields'][1]['value'][1:].split('\n')
      declined_list = d['fields'][3]['value'][1:].split('\n')

      for i in range(len(accepted_list)):

        if(accepted_list[0].lstrip() != '-'):
          final_accepted.append(int(re.search("(\d{18})", accepted_list[i]).group()))

      for i in range(len(declined_list)):

        if(declined_list[0].lstrip() != '-'):
          final_declined.append(int(re.search("(\d{18})", declined_list[i]).group()))
      accepted_set = set(final_accepted)
      declined_set = set(final_declined)

      for member in event_channel.members:
        if not member.bot and not member_has_roles(member, role_ids):
        
          memberId = member.id

          total_set.add(memberId)
    
    # Apollo
    elif event_bot_id == 475744554910351370:


      accepted_msg = d['fields'][2]['name'].split('>')[1].lstrip()
      declined_msg = d['fields'][3]['name'].split('>')[1].lstrip()
      accepted_list = d['fields'][2]['value'][4:].split('\n')
      declined_list = d['fields'][3]['value'][4:].split('\n')

      print("acc list")
      print(accepted_list)

      print("dec list")
      print(declined_list)

      # for i in range(len(accepted_list)):
      #   final_accepted.append(accepted_list[i])

      # for i in range(len(declined_list)):
      #   final_declined.append(declined_list[i])



      for member in event_channel.members:
        if not member.bot and not member_has_roles(member, role_ids):
          if member.display_name in accepted_list:
            final_accepted.append(member.id)
          if member.display_name in declined_list:
            final_declined.append(member.id)
          
          total_set.add(member.id)

      accepted_set = set(final_accepted)
      declined_set = set(final_declined)


      print("accepted")
      print(accepted_set)

      print("declined")
      print(declined_set)

      print("total")
      print(total_set)

# 125678499884171264
# {125678499884171264, 315612303758327808, 152187546464550912, 290894292900118528, 323831917478674432, 341307961647300609, 406393804661325834, 536648476524806155, 978405706980012082, 759833106977914908}
# {125678499884171264, 315612303758327808, 152187546464550912, 290894292900118528, 323831917478674432, 341307961647300609, 406393804661325834, 536648476524806155, 978405706980012082, 759833106977914908}
    
    

    # for member in event_channel.members:
    #   if not member.bot and not member_has_roles(member, role_ids):
      
    #     memberId = member.id

    #     total_set.add(memberId)
    
    return total_set.difference(accepted_set).difference(declined_set)
  else:
    print('Could not find event bot message')

#warnlist
async def warnlist(msg_channel, event_bot_id, role_ids):
  missing_set = await missing_set_nicks(msg_channel, event_bot_id, role_ids)
  display_message = "React\n"

  for member in msg_channel.members:
      if not member.bot and not member_has_roles(member, role_ids):
        if(member.id in missing_set):
            display_message = display_message + member.display_name + '\n'

  await send_embed(msg_channel, "show up or die", display_message,
                   discord.Color.green())

#warnping
async def warnping(msg_channel, event_bot_id, role_ids):
  missing_set = await missing_set_nicks(msg_channel, event_bot_id, role_ids)
  display_message = "Please react Yes/No to the event. \n"
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
