import discord

async def send_msg(ctx, msg):
  await ctx.send(msg)

async def send_embed(ctx, title, description, color):
  await ctx.send(embed=discord.Embed(title=title, description=description, color=color))