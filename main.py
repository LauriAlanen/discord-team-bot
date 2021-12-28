import discord
from discord.ext import commands
import random

bot = commands.Bot(command_prefix="/", help_command=None)

emoji = '\N{THUMBS UP SIGN}'
shuffle_dict = {}

bot.channel_id = int()
bot.msg_id = int()
bot.autochannel_state = 1  # Muista vaihtaa 0



@bot.command()
async def help(ctx):
    embed = discord.Embed(title="How to use the Team Bot?")
    embed.add_field(name="/teams", value="Start the the team poll")
    embed.add_field(name="/autochannel_on", value="Autocreate a channel when shuffling")
    embed.add_field(name="/autochannel_off", value="Don't create a channel when shuffling")
    embed.add_field(name="/shuffle", value="Randomize and divide the teams")
    embed.add_field(name="/aim", value="See how good your aim is")
    embed.add_field(name="/source", value="See the source code")
    await ctx.send(embed=embed)


@bot.command()
async def teams(ctx):
    voice_channels = []
    bot.guild = ctx.message.guild

    if bot.autochannel_state == 1:
        for channel in ctx.message.guild.voice_channels:
            voice_channels.append(channel.name)

        if "Team-1" in voice_channels and "Team-2" in voice_channels:
            print("Channel Already Exists.")

        elif "Team-1" not in voice_channels and "Team-2" in voice_channels:
            await bot.guild.create_voice_channel("Team-1")

        elif "Team-1" in voice_channels and "Team-2" not in voice_channels:
            await bot.guild.create_voice_channel("Team-2")

        else:
            await bot.guild.create_voice_channel("Team-1")
            await bot.guild.create_voice_channel("Team-2")

    poll = await ctx.send("React with thumbs up to this message to join the poll.", delete_after=60)
    await poll.add_reaction(emoji)

    bot.msg_id = poll.id
    bot.channel_id = poll.channel

    bot.team1_id = discord.utils.get(bot.guild.channels, name="Team-1").id
    bot.team2_id = discord.utils.get(bot.guild.channels, name="Team-2").id
    bot.team1 = bot.get_channel(bot.team1_id)
    bot.team2 = bot.get_channel(bot.team2_id)

    voice_channels.clear()


@bot.command()
async def shuffle(ctx):
    if shuffle_dict:
        embed = discord.Embed(
            title="Divided Teams",
            colour=discord.Colour.blue()
        )

        items = list(shuffle_dict.items())
        random.shuffle(items)

        players1 = dict(list(shuffle_dict.items())[len(shuffle_dict) // 2:])
        players2 = dict(list(shuffle_dict.items())[:len(shuffle_dict) // 2])

        embed.add_field(name="Team 1", value=f"{players1}")
        embed.add_field(name="Team 2", value=f"{players2}")
        await ctx.send(embed=embed)

        for member in players1:
            print(member)
        for member in players2:
            print(member)


        msg = await bot.channel_id.fetch_message(bot.msg_id)
        await msg.delete()
        shuffle_dict.clear()

    else:
        await ctx.send("The poll seems to be empty...")


@bot.command()
async def autochannel_on(ctx):
    print("On state")
    bot.autochannel_state = 1
    await ctx.send("Channels will be created for each team when /shuffle is used.")


@bot.command()
async def autochannel_off(ctx):
    print("Off state")
    bot.autochannel_state = 0
    await ctx.send("There will be no channels created when /shuffle is used.")


@bot.command()
async def aim(ctx):
    if "Martti" in ctx.author.name:
        await ctx.send("Mestari Sotilas Martti's headshot accuracy is 100%")
    else:
        await ctx.send(f"{ctx.author.name}'s headshot accuracy is {random.randrange(0, 30)}%")

@bot.command()
async def source(ctx):
    await ctx.send("https://github.com/LauriAlanen/discord-team-bot/blob/main/main.py")




@bot.event
async def on_reaction_add(reaction, user):
    if user != bot.user:
        if str(reaction.emoji) == emoji:
            shuffle_dict[user.name] = user.id




bot.run("token")
