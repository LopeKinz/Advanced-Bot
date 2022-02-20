@client.command()
async def level(ctx, Member:discord.Member = None):
    try:  
        if Member == None:
            memberranknone = ctx.author.id
            rank1 = leveling.getlvl(memberranknone)
            await ctx.send(f"{ctx.author.mention} is Level {rank1}")
        else:
            memberrank = Member.id
            rank2 = leveling.getlvl(memberrank)
            await ctx.send(f"{Member.mention} is Level {rank2}")
    except:
        await ctx.send("Error")