from re import sub
import discord, json, aiohttp, random, discord.ext
from discord.ext import commands
from discord.ext.commands import has_permissions, MissingPermissions
import praw
import os
from modules import leveling
import time
from datetime import datetime
from asyncio import sleep
import socket

# Get configuration.json
with open("configuration.json", "r") as config: 
	data = json.load(config)
	token = data["token"]
	prefix = data["prefix"]
	owner_id = data["owner_id"]

def ping_server(server: str, port=80, timeout=3):
    """ping server"""
    try:
        socket.setdefaulttimeout(timeout)
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.connect((server, port))
    except OSError as error:
        return False
    else:
        s.close()
        return True

reddit = praw.Reddit(client_id='faXrkys5czbn-A',
                     client_secret='059OT4n2oYlDj8jwPqGPhFlmGEKsEQ',
                     user_agent="Chrome: Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/77.0.3865.90 Safari/537.36")



# Intents
intents = discord.Intents.default()
intents.members = True

# The bot
bot = commands.Bot(prefix, intents = intents, owner_id = owner_id)

def restart_program():
    python = sys.executable
    os.execl(python, python, * sys.argv)

@bot.event
async def on_ready():
	print(f"We have logged in as {bot.user}")
	print(discord.__version__)
	await bot.change_presence(activity=discord.Activity(type=discord.ActivityType.watching, name =f"{bot.command_prefix}commands"))

@bot.event
async def on_member_join(member:discord.Member):
    memberregister = member.id
    leveling.register(memberregister)
    await sleep(60*10)
    for channel in member.guild.channels:
        if channel.name.startswith('⭐⎜All Member'):
            await channel.edit(name=f'⭐⎜All Member: {member.guild.member_count}')
            break
@bot.event
async def on_member_remove(member):
    guild = member.guild
    channel = get(guild.channels, name = '⭐⎜All Member')
    await channel.edit(name = f'⭐⎜All Member: {guild.member_count}')    

@bot.command()
async def pingserver(ctx, arg = None):
    message = await ctx.send(f"Pinging {arg}")
    count = 0
    if arg == None:
        await message.edit(content=f"No IP or Website Given...")
    else:
        for i in range(10):
            count = count +1
            response = ping_server(arg)
            if response == True:
                await message.edit(content=f"{arg} is Online! {count} Pings")
                time.sleep(1)
            else:
                await message.edit(content=f"{arg} is Offline! {count} Pings")
                time.sleep(1)      

@bot.command()
@has_permissions(administrator=True)
async def reload(member:discord.Member):
    for channel in member.guild.channels:
        if channel.name.startswith('⭐⎜All Member:'):
            await channel.edit(name=f'⭐⎜All Member: {member.guild.member_count}')   



@bot.event
async def on_message(message):
    try:
        lvlmember = message.author.id
        xp = random.randint(1, 5)
        leveling.addxp(lvlmember,str(xp))
        Level = leveling.getlvl(lvlmember)
        rank1 = leveling.getxp(lvlmember)
        if rank1 > 1000:
            leveling.addlvl(lvlmember,"1")
            Level = leveling.getlvl(lvlmember)
            leveling.resetxp(lvlmember)
            await message.channel.send(f"{message.author.mention} Ranked up to Level {Level}")
    except:
        pass
    await bot.process_commands(message)

@bot.command()
@has_permissions(administrator=True)
async def delete(ctx, amount=5):
    await ctx.channel.purge(limit=amount)

@bot.command()
@has_permissions(administrator=True)
async def registerall(ctx):
    message = await ctx.send("Registering all Members!")
    x = ctx.guild.members
    for member in x:
        with open("data/level.json", "r") as f:
            users = json.load(f)
            users[str(f"{member.id}")] = "1"
        with open("data/level.json", "w") as f:
            json.dump(users, f, indent=4)
        with open("data/xp.json", "r") as d:
            xp = json.load(d)
            xp[str(f"{member.id}")] = "1"
        with open("data/xp.json", "w") as d:
            json.dump(xp, d, indent=4)
        await message.edit(content=f"Registered {member}!")
        print("Done")

@bot.command()
async def memberlist(ctx):
    x = ctx.guild.members
    for member in x:
        await ctx.author.send(member)

@bot.command()
async def register(ctx , Member:discord.Member):
    message = await ctx.send(f"Registering {Member}!")
    time.sleep(2)
    regmember = Member.id
    leveling.register(regmember)
    await message.edit(content=f"Succsessfully Registered {Member}!")

@bot.command()
@has_permissions(administrator=True)
async def msg(ctx, *, args = None):
    await bot.wait_until_ready()
    if args == None:
        message_content = "Please wait, we will be with you shortly!"
    else:
        message_content = "".join(args)
        em = discord.Embed(title="", description="{}".format(message_content))
        em.set_footer(text=f"{ctx.author}")
        await ctx.send(embed=em)
        await ctx.message.delete()
        

@bot.command()
async def userinfo(ctx, *, user: discord.Member = None):
    if user is None:
        user = ctx.author      
    date_format = "%a, %d %b %Y %I:%M %p"
    embed = discord.Embed(color=0xdfa3ff, description=user.mention)
    embed.set_author(name=str(user), icon_url=user.avatar_url)
    embed.set_thumbnail(url=user.avatar_url)
    embed.add_field(name="Joined", value=user.joined_at.strftime(date_format))
    members = sorted(ctx.guild.members, key=lambda m: m.joined_at)
    embed.add_field(name="Join position", value=str(members.index(user)+1))
    embed.add_field(name="Registered", value=user.created_at.strftime(date_format))
    if len(user.roles) > 1:
        role_string = ' '.join([r.mention for r in user.roles][1:])
        embed.add_field(name="Roles [{}]".format(len(user.roles)-1), value=role_string, inline=False)
    perm_string = ', '.join([str(p[0]).replace("_", " ").title() for p in user.guild_permissions if p[1]])
    embed.add_field(name="Guild permissions", value=perm_string, inline=False)
    embed.set_footer(text='ID: ' + str(user.id))
    return await ctx.send(embed=embed)

@bot.command()
async def level(ctx, Member:discord.Member = None):
    message = await ctx.send("Getting Level!")
    try:  
        if Member == None:
            memberranknone = ctx.author.id
            rank1 = leveling.getlvl(memberranknone)
            xp1 = leveling.getxp(memberranknone)
            embed=discord.Embed(title="**Level System**", description=f"**{ctx.author}**", color=0xff0000)
            embed.set_thumbnail(url=ctx.author.avatar_url)
            embed.add_field(name="Level: ", value=f"{rank1}", inline=False)
            embed.add_field(name="XP", value=f"{xp1}/1000 XP", inline=False)
            embed.set_footer(text=f"Requested by {ctx.author}")
            await message.edit(embed=embed)
        else:
            memberrank = Member.id
            rank2 = leveling.getlvl(memberrank)
            xp2 = leveling.getxp(memberrank)
            embed=discord.Embed(title="**Level System**", description=f"**{Member}**", color=0xff0000)
            embed.set_thumbnail(url=Member.avatar_url)
            embed.add_field(name="Level: ", value=f"{rank2}", inline=False)
            embed.add_field(name="XP", value=f"{xp2}/1000 XP", inline=False)
            embed.set_footer(text=f"Requested by {ctx.author}")
            await message.edit(embed=embed)
    except:
        await message.edit(content=f"Error while getting {Member}'s Level")

@bot.command()
async def ping(ctx):
    before = time.monotonic()
    message = await ctx.send(":ping_pong: Pong!")
    ping = (time.monotonic() - before) * 1000
    await message.edit(content=f":ping_pong: Pong!  `{int(ping)}ms`")

@bot.command()
async def commands(ctx):
    embed=discord.Embed(title="**Commands List**", description="Shows all Commands", color=0xff0000)
    embed.add_field(name="Commands", value="Usage: <commands | Shows Command List!", inline=False)
    embed.add_field(name="Meme", value="Usage: <meme | Sends a random Meme!", inline=False)
    embed.add_field(name="Memeberlist", value="Usage: <memberlist | Sends all Members in a Guild!", inline=False)
    embed.add_field(name="UserInfo", value="Usage: <userinfo or <userinfo @member | Sends User Info!", inline=False)
    embed.add_field(name="GetReddit", value="Usage: <getreddit subreddit | Gets a Random Post of chosen Subreddit!", inline=False)
    embed.add_field(name="Info", value="Usage: <info | Shows Info about the Bot and Server!", inline=False)
    embed.add_field(name="Ping", value="Usage: <ping | Shows Ping of the Bot", inline=False)
    embed.add_field(name="Ping Server", value="Usage: <pingserver ip | Shows reachability if an IP Adress!", inline=False)
    embed.add_field(name="Register", value="Usage: <register @member | Register a Member to the Leveling System!", inline=False)
    embed.add_field(name="Level", value="Usage: <level or <level @member | Shows the Current Level of a Member!", inline=False)
    embed.add_field(name="Embed Message", value="[Admin] Usage: <msg message | Sends a Embed message!", inline=False)
    embed.add_field(name="Delete Messages", value="[Admin] Usage: <delete or <delete amount | Deletes Messages!", inline=False)
    embed.add_field(name="Restart", value="[Admin] Usage: <restart | Restarts the Bot!", inline=False)
    embed.add_field(name="Reload", value="[Admin] Usage: <reload | Reloads Userlist", inline=False)
    embed.set_footer(text=f"Requested by {ctx.author}")
    await ctx.send(embed=embed)

@bot.command()
async def meme(ctx):
    try:
        message = await ctx.send("Getting good meme...")
        memes_submissions = reddit.subreddit('memes').new()
        post_to_pick = random.randint(1, 100)
        for i in range(0, post_to_pick):
            submission = next(x for x in memes_submissions if not x.stickied)
        await message.edit(content=submission.url)
    except:
        await message.edit(content=f"Error while getting random Meme!")



@bot.command()
@has_permissions(administrator=True)
async def restart(ctx):
    restart_program()

@bot.command()
async def getreddit(ctx, arg=None):
    message = await ctx.send(f"Gettting random Post of {arg}!")
    if arg == None:
        await message.edit(content=f"No Subreddit Entered!")
    else:
        try:
            subreddit = str(arg)
            memes_submissions = reddit.subreddit(subreddit).new()
            post_to_pick = random.randint(1, 100)
            for i in range(0, post_to_pick):
                submission = next(x for x in memes_submissions if not x.stickied)
            await message.edit(content=submission.url)
        except:
            await message.edit(content=f"Error while getting random Post from {subreddit}!")

@bot.command()
async def info(ctx):
    from datetime import datetime
    now = datetime.now()
    current_time = now.strftime("%H:%M")
    member_count = len(ctx.guild.members)
    true_member_count = len([m for m in ctx.guild.members if not m.bot])
    bots = member_count - true_member_count
    embed=discord.Embed(title="Infomation", description="", color=0xff0000)
    embed.add_field(name="All Members : ", value=f"{member_count}", inline=False)
    embed.add_field(name="Human Member : ", value=f"{true_member_count}", inline=False)
    embed.add_field(name="Bots : ", value=f"{bots}", inline=False)
    embed.add_field(name="Channels:", value=len(ctx.guild.channels), inline=False)
    embed.add_field(name="Ping:", value=f"{round(bot.latency * 1000)}ms", inline=False)
    embed.set_footer(text=f"Requested by {ctx.author} at {current_time}")
    await ctx.send(embed=embed)

bot.run(token)