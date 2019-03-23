import discord
from discord.ext import commands
from discord.ext.commands import has_permissions, CheckFailure, BadArgument
from discord.utils import get

token = ''

client = commands.Bot (command_prefix = '.')

#say works only in commands, not in events
#change spamcheck to mod-log before pushing

@client.event
async def on_ready():
    print ('Logged in as {}'.format(client.user))
    await client.change_presence(game=discord.Game(name="FIFA 19"))

@client.event
async def on_message (message):
    print (message.channel, message.author, message.author.name, message.content)
    
    if message.author.name == 'Dyno':
        await client.add_reaction(message, '😡')
    
    await client.process_commands(message)

@client.command()
async def ping():
    await client.say ('Pong!')

@client.command()
async def info():
    await client.say ('Find more information about the bot at https://shohamc1.gitlab.io/smallytchannelbot')

#kick user
@client.command(pass_context = True, name = 'kick')
@has_permissions (manage_roles = True, ban_members = True)
async def kick (ctx, member: discord.User):
    await client.kick (member)
    await client.say ('{} has been kicked!'.format(member.name))
    channel = discord.utils.get (member.server.channels, name = 'spamcheck')
    embed = discord.Embed (title = '{} successfully kicked'.format(member.name), color=0xcc3300)
    await client.send_message (channel, embed = embed)

@kick.error
async def kick_error (error, ctx):
    #userid = '<@' + ctx.message.author.id + '>'
    text = 'Sorry {}, you can\'t do that!'.format(ctx.message.author.mention)
    await client.say (text)

#ban user
@client.command(pass_context = True, name = 'ban')
@has_permissions (manage_roles = True, ban_members = True)
async def ban (ctx, member: discord.User):
    await client.ban (member)
    await client.say ('{} has been banned!'.format(member.name))
    channel = discord.utils.get (member.server.channels, name = 'spamcheck')
    embed = discord.Embed (title = '{} successfully banned'.format(member.name), color=0xcc3300)
    await client.send_message (channel, embed = embed)

@ban.error
async def ban_error (error, ctx):
    #userid = '<@' + ctx.message.author.id + '>'
    text = 'Sorry {}, you can\'t do that!'.format(ctx.message.author.mention)
    await client.say (text)

#show edited message
@client.event
async def on_message_edit (before, after):
    if after.author == client.user:
        return
    
    channel = discord.utils.get (after.server.channels, name = 'spamcheck') #replace spamcheck with dumpground
    embed = discord.Embed (title = 'Message by {} edited in {}'.format(after.author.name, after.channel.name), color=0x66ff33) #add the link
    embed.add_field (name = 'Before', value= before.content, inline = False)
    embed.add_field (name = 'After', value = after.content, inline = False)
    await client.send_message (channel, embed = embed)

@client.event
async def on_message_delete (message):
    if message.author == client.user:
        return
    
    channel = discord.utils.get (message.server.channels, name = 'spamcheck')
    embed = discord.Embed (title = 'Message by {} deleted in {}'.format(message.author.name, message.channel.name), color=0xff0000)
    embed.add_field (name = 'Content', value = message.content, inline = False)
    await client.send_message (channel, embed = embed)

client.run (token)