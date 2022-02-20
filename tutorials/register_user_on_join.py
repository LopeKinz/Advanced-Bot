#automatically register a user on join
import leveling

@client.event
async def on_member_join(self, member:discord.Member):
    memberregister = member.id
    leveling.register(memberregister)