DB configurations
MongoDB

Collections:
history - list of all actions that occur
{
    action,
    event_id,
    channel_id,
    guild_id,
    user_id
}
events - catalog of events detected
{
    id
    bot_detected,
    name,
    description,
    start,
    end,
    guild_id
    pinged_roles { roles }
    users_accepted { users },
    users_declined { users },
    users_tenative { users },

}

roles - catalog of roles added to be pinged
{
    role_id == discord_role_id,
    name,
    guild_id,


}

guild - guilds/servers detected that have used AttendenceBot
{
    id,
    name,
    pinged_roles { roles }, -- roles that will get pinged on /warnping
    allowed_roles { roles } -- roles that are allowed to run /warnping
}

users - users being pinged
{
    id, 
    username
}