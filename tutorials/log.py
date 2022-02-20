#Logging
import leveling
import discord

#loggs register
@client.event
async def on_member_join(self, member:discord.Member):
    memberregister = member.id
    leveling.register(memberregister)
    Channel = client.get_channel(channle_id)
    log = leveling.log_register(memberregister)
    await channel.send(log)