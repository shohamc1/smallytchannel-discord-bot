import discord
from discord.ext import commands
from discord.ext.commands import has_permissions, CheckFailure, BadArgument
from discord.utils import get

token = '' #enter your own token here

client = commands.Bot (command_prefix = '.')

#say works only in commands, not in events

@client.event
async def on_ready():
    print ('Logged in as {}'.format(client.user))

@client.event
async def on_message (message):
    print (message.channel, message.author, message.author.name, message.content)

    if message.content.startswith ('!hello'):
        await client.send_message (message.channel, content = "Hello there!")

    if message.author.name == 'Dyno':
        await client.add_reaction(message, '😡')
    
    await client.process_commands(message)

@client.command()
async def ping():
    await client.say ('Pong')

#kick user
@client.command(pass_context = True, name = 'kick')
@has_permissions (manage_roles = True, ban_members = True)
async def kick (ctx, member: discord.User):
    await client.kick (member)
    await client.say ('{} has been kicked!'.format(member.name))
    channel = discord.utils.get (member.server.channels, name = 'spamcheck')
    embed = discord.Embed (title = 'Member successfully kicked', description = 'A member has been kicked', color=0xcc3300)
    embed.add_field (name = 'Member', value= member.name)
    await client.send_message (channel, embed = embed)

@kick.error
async def kick_error (error, ctx):
    userid = '<@' + ctx.message.author.id + '>'
    text = 'Sorry {}, you can\'t do that!'.format(userid)
    await client.say (text)

#ban user
@client.command(pass_context = True, name = 'ban')
@has_permissions (manage_roles = True, ban_members = True)
async def ban (ctx, member: discord.User):
    await client.ban (member)
    await client.say ('{} has been banned!'.format(member.name))
    channel = discord.utils.get (member.server.channels, name = 'spamcheck')
    embed = discord.Embed (title = 'Member successfully banned', description = 'A member has been banned', color=0xcc3300)
    embed.add_field (name = 'Member', value= member.name)
    await client.send_message (channel, embed = embed)

@ban.error
async def ban_error (error, ctx):
    userid = '<@' + ctx.message.author.id + '>'
    text = 'Sorry {}, you can\'t do that!'.format(userid)
    await client.say (text)

#show edited message
@client.event
async def on_message_edit (before, after):
    if after.author == client.user:
        return
    
    channel = discord.utils.get (after.server.channels, name = 'spamcheck') #replace spamcheck with dumpground
    embed = discord.Embed (title = 'Message edited', description = 'A message has been edited', color=0x66ff33)
    embed.add_field (name = 'Before', value= before.content)
    embed.add_field (name = 'After', value = after.content)
    embed.add_field (name = 'Channel', value = after.channel.name)
    embed.add_field (name = 'User', value = after.author.name)
    #await client.send_message (channel , 'Before: {}\nAfter: {}'.format(before.content, after.content))
    await client.send_message (channel, embed = embed)

@client.event
async def on_message_delete (message):
    if message.author == client.user:
        return
    
    channel = discord.utils.get (message.server.channels, name = 'spamcheck')
    embed = discord.Embed (title = 'Message deleted', description = 'A message has been deleted', color=0xff0000)
    embed.add_field (name = 'Contents', value = message.content)
    embed.add_field (name = 'User', value = message.author.name)
    embed.add_field (name = 'Channel', value = message.channel.name)
    await client.send_message (channel, embed = embed)

client.run (token)