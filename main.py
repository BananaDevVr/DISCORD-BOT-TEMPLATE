import discord
from discord.ext import commands

intents = discord.Intents.default()
intents.members = True
intents.messages = True  
intents.message_content = True
bot = commands.Bot(command_prefix='!', intents=intents)
bot.remove_command('help')

@bot.event
async def on_ready():
    await bot.change_presence(activity=discord.Game(name="with moderation commands | ;help"))

@bot.command(name='kick', help='Kick a member from the server')
@commands.has_permissions(kick_members=True)
async def kick(ctx, member: discord.Member, *, reason=None):
    await member.kick(reason=reason)

@bot.command(name='ban', help='Ban a member from the server')
@commands.has_permissions(ban_members=True)
async def ban(ctx, member: discord.Member, *, reason=None):
    await member.ban(reason=reason)

@ban.error
async def ban_error(ctx, error):
    if isinstance(error, commands.MissingPermissions):
        await ctx.send("You don't have permission to ban members.")

@kick.error
async def kick_error(ctx, error):
    if isinstance(error, commands.MissingPermissions):
        await ctx.send("You don't have permission to kick members.")
@bot.command(name='mute', help='Mute a member in the server')
@commands.has_permissions(kick_members=True)
async def mute(ctx, member: discord.Member, *, reason=None):
    await ctx.send(f'{member} has been muted for {reason}')

@bot.command(name='unmute', help='Unmute a member in the server')
@commands.has_permissions(kick_members=True)
async def unmute(ctx, member: discord.Member):
    await ctx.send(f'{member} has been unmuted')
  
@bot.command(name='warn', help='Warn a member in the server')
@commands.has_permissions(kick_members=True)
async def warn(ctx, member: discord.Member, *, reason=None):
    await ctx.send(f'{member} has been warned for {reason}')

@bot.command(name='clear', help='Clear messages in the server')
@commands.has_permissions(manage_messages=True)
async def clear(ctx, amount=5):
    await ctx.channel.purge(limit=amount)

@bot.command(name='tempban', help='Temporarily ban a member from the server')
@commands.has_permissions(ban_members=True)
async def tempban(ctx, member: discord.Member, duration, *, reason=None):
    await member.ban(reason=reason)
    await asyncio.sleep(duration)
    await member.unban()

@bot.command(name='tempmute', help='Temporarily mute a member in the server')
@commands.has_permissions(kick_members=True)
async def tempmute(ctx, member: discord.Member, duration, *, reason=None):
    role = discord.utils.get(ctx.guild.roles, name="Muted")
    await member.add_roles(role)
    await ctx.send(f'{member} has been muted for {duration} {reason}')
    await asyncio.sleep(duration)
    await member.remove_roles(role)

@bot.command(name='nickname', help='Change the nickname of a member in the server')
async def nickname(ctx, member: discord.Member, nick):
    await member.edit(nick=nick)

@bot.command(name='help', help='Display the list of available commands')
async def help(ctx):
    help_embed = discord.Embed(
        title="Bot Commands",
        description="List of available commands:",
        color=discord.Color.green()
    )
    help_embed.add_field(name=";kick", value="Kick a member from the server", inline=False)
    help_embed.add_field(name=";ban", value="Ban a member from the server", inline=False)
    help_embed.add_field(name=";mute", value="Mute a member in the server", inline=False)
    help_embed.add_field(name=";unmute", value="Unmute a member in the server", inline=False)
    help_embed.add_field(name=";warn", value="Warn a member in the server", inline=False)
    help_embed.add_field(name=";clear", value="Clear messages in the server", inline=False)
    help_embed.add_field(name=";tempban", value="Temporarily ban a member from the server", inline=False)
    help_embed.add_field(name=";tempmute", value="Temporarily mute a member in the server", inline=False)
    help_embed.add_field(name=";nickname", value="Change the nickname of a member in the server", inline=False)
    await ctx.send(embed=help_embed)


bot.run('DISCORD_TOKEN_HERE')