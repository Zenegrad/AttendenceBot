import discord, Common, re, json

#returns true if member has any of the given roles
def member_has_roles(member, role_ids):
  for role in member.roles:
    if role.id in role_ids:
      return True
  return False



#computes the members who haven't voted in the event except for bots and retireds and mercs
async def missing_set_nicks(event_channel: discord.TextChannel, event_bot_id, role_ids):
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
        embed = event_message.embeds[0]
        d = embed.to_dict()
      
      # if re.match(r"(\(http:.*?\)',)", str(d)):
      #     event_message = re.sub(r"(\(http:.*?\)',)", "", str(d), 0, re.MULTILINE)
          
        if re.search(r"(\(http:.*?\))", str(d)):
              d_str = str(d).strip()
              d_str = re.sub("(\(http:.*?\))",'',d_str)
              
              #replace ' with "
              p = re.compile('(?<!\\\\)\'')
              d_str = p.sub('\"', d_str)
              
              d_str = d_str.replace("False", "\"False\"")
              d_str = d_str.replace("True", "\"True\"")
              
              # Find the description and replace any " with ' to not break the json
              description_start = d_str.find('"description":')

              description_match = re.search('(\"description\":\s\".*\",\s\"title\")', d_str)
              desc_text_match = re.search('"description":\s*"(.*)",\s*"title"', description_match.group(1))

              fixed_description = desc_text_match.group(1).replace('"', "'")

              split = d_str.split(desc_text_match.group(1))

              final_str = f"{split[0]}{fixed_description}{split[1]}"
            
              d = json.loads(final_str)

        # Sesh
        if event_bot_id == Common.SESH_ID:
          accepted_msg = d['fields'][1]['name'].lstrip()
          declined_msg = d['fields'][3]['name'].lstrip()
          accepted_list = d['fields'][1]['value'][1:].split('\n')
          declined_list = d['fields'][3]['value'][1:].split('\n')

          for i in range(len(accepted_list)):
            print("test:")
            print(accepted_list[0].lstrip())
            if(accepted_list[0].lstrip() != '-'):
              # Pull only the discord Id.
              if re.search("(\d+)", accepted_list[i]):
                final_accepted.append(int(re.search("(\d+)", accepted_list[i]).group()))
              else:
                break

          for i in range(len(declined_list)):
            if(declined_list[0].lstrip() != '-'):

              # Pull only the discord Id.
              if re.search("(\d+)", declined_list[i]):
                final_declined.append(int(re.search("(\d+)", declined_list[i]).group()))
              else:
                break

          accepted_set = set(final_accepted)
          declined_set = set(final_declined)

          for member in event_channel.members:
            if not member.bot and not member_has_roles(member, role_ids):
            
              memberId = member.id

              total_set.add(memberId)
        
        # Apollo
        elif event_bot_id == Common.APOLLO_ID:

          accepted_msg = d['fields'][2]['name'].split('>')[1].lstrip()
          declined_msg = d['fields'][3]['name'].split('>')[1].lstrip()
          accepted_list = d['fields'][2]['value'][4:].split('\n')
          declined_list = d['fields'][3]['value'][4:].split('\n')

          print(accepted_list)

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

        return total_set.difference(accepted_set).difference(declined_set)
  else:
    print('Could not find event bot message')