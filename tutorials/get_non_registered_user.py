#If a user is not leveling up he needs to type the register command in order to level up!
import leveling

@client.command()
async def register(ctx , Member:discord.Member):
    regmember = Member.id
    leveling.register(regmember)