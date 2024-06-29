import discord, re, Common, util, json

from Event import Event


# Generates the event message
async def generate(msg_channel: discord.TextChannel, event_bot_id):
    
    event: Event = parse(msg_channel, event_bot_id)
    print(f"generated: {event}")    


async def parse(event_channel: discord.TextChannel, event_bot_id) -> Event:

    final_accepted = []
    final_tenative = []
    final_declined = []

    event: Event = None

    total_set = set()

    async for m in event_channel.history(limit=500):

        if event_bot_id == m.author.id:
            event_message = m

        if event_message:
            embed = event_message.embeds[0]
            d = embed.to_dict()
        

        # Pull the description from event. ( Current is for Sesh not tested on Apollo )
        description_match = re.search('(\"description\":\s\".*\",\s\"title\")', d_str)
        desc_text_match = re.search('"description":\s*"(.*)",\s*"title"', description_match.group(1))
        event.description = desc_text_match


        title_match = re.search(r'"title":\s*"(.*)"', str(d).strip())
        title_text = title_match.group(1)



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

            event.description = desc_text_match

            fixed_description = desc_text_match.group(1).replace('"', "'")

            split = d_str.split(desc_text_match.group(1))

            final_str = f"{split[0]}{fixed_description}{split[1]}"
            
            d = json.loads(final_str)

        # Sesh
        if event_bot_id == Common.SESH_ID:
            accepted_list = d['fields'][1]['value'][1:].split('\n')
            tenative_list = d['fields'][2]['value'][1:].split('\n')
            declined_list = d['fields'][3]['value'][1:].split('\n')

            for i in range(len(accepted_list)):
                print("test:")
                print(accepted_list[0].lstrip())
                if(accepted_list[0].lstrip() != '-'):
                    final_accepted.append(int(re.search("(\d+)", accepted_list[i]).group()))

            for i in range(len(declined_list)):

                if(declined_list[0].lstrip() != '-'):
                    final_declined.append(int(re.search("(\d+)", declined_list[i]).group()))

            for i in range(len(tenative_list)):

                if(tenative_list[0].lstrip() != '-'):
                    final_tenative.append(int(re.search("(\d+)", declined_list[i]).group()))
            

            # Assigns user to the event
            event.tenative = set(final_tenative)
            event.accepted = set(final_accepted)
            event.declined = set(final_declined)
    
        # Apollo
        elif event_bot_id == 475744554910351370:
            accepted_list = d['fields'][2]['value'][4:].split('\n')
            declined_list = d['fields'][3]['value'][4:].split('\n')
            # for i in range(len(accepted_list)):
            #   final_accepted.append(accepted_list[i])

            # for i in range(len(declined_list)):
            #   final_declined.append(declined_list[i])

            for member in event_channel.members:
                if not member.bot and not util.member_has_roles(member, role_ids):
                    if member.display_name in accepted_list:
                        final_accepted.append(member.id)
                    if member.display_name in declined_list:
                        final_declined.append(member.id)
                    if member.display_name in tenative_list:
                        final_tenative.append(member.id)
                
                total_set.add(member.id)

            # Assigns user to the event
            event.tenative = set(final_tenative)
            event.accepted = set(final_accepted)
            event.declined = set(final_declined)

    return event
