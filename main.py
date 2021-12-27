import discord
from discord.ext import commands
import random

bot = commands.Bot(command_prefix="/")

emoji = '\N{THUMBS UP SIGN}'
raffle_list = []

bot.channel_id = int()
bot.msg_id = int()


@bot.command()
async def teams(ctx):
    pool = await ctx.send("React with thumbs up to this message to join the pool.")
    await pool.add_reaction(emoji)
    bot.msg_id = pool.id
    bot.channel_id = pool.channel


@bot.command()
async def shuffle(ctx):
    if raffle_list:
        middle_index = len(raffle_list) // 2
        random.shuffle(raffle_list)
        print(raffle_list)
        embed = discord.Embed(
            title="Divided Teams",
            colour=discord.Colour.blue()
        )
        embed.add_field(name="Team 1", value=f"{raffle_list[:middle_index]}")
        embed.add_field(name="Team 2", value=f"{raffle_list[middle_index:]}")
        await ctx.send(embed=embed)

        msg = await bot.channel_id.fetch_message(bot.msg_id)
        await msg.delete()
        raffle_list.clear()

    else:
        await ctx.send("The pool seems to be empty...")


@bot.event
async def on_reaction_add(reaction, user):
    if user != bot.user:
        if str(reaction.emoji) == emoji:
            raffle_list.append(user.name)
            print(raffle_list)


bot.run("Token")
