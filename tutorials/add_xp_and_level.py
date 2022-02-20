#Template to get XP every message and automatically levels up
import leveling

@client.event
async def on_message(message):
    try:
        lvlmember = message.author.id
        leveling.addxp(lvlmember,"1")
        Level = leveling.getlvl(lvlmember)
        rank1 = leveling.getxp(lvlmember)
        if rank1 > 10:
            leveling.addlvl(lvlmember,"1")
            Level = leveling.getlvl(lvlmember)
            leveling.resetxp(lvlmember)
            await message.channel.send(f"{message.author.mention} Ranked up to Level {Level}")
    except:
        pass
    await client.process_commands(message)
