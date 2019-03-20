import discord
from discord.ext import commands
from discord.ext.commands import has_permissions, CheckFailure, BadArgument
token = 'NTU3NTc2NzQzODEzMjUxMTEy.D3KT1w.3bEK0CsU6g3a4va0ciUJlq4F4sg'

client = commands.Bot (command_prefix = '!')


@client.event
async def on_ready():
    print ('Logged in as {}'.format(client.user))

@client.event
async def on_message (message):
    print (message.channel, message.author, message.author.name, message.content)

    if message.content.startswith ('!hello'):
        await client.send_message (message.author , content = "Hello there!")
    
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

@ban.error
async def ban_error (error, ctx):
    userid = '<@' + ctx.message.author.id + '>'
    text = 'Sorry {}, you can\'t do that!'.format(userid)
    await client.say (text)

client.run (token)