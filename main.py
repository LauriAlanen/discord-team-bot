import discord
from discord.ext import commands
import discord.utils
import random

bot = commands.Bot(command_prefix="/", help_command=None)

emoji = '\N{THUMBS UP SIGN}'
shuffle_dict = {}

bot.channel_id = int()
bot.msg_id = int()
bot.autochannel_state = 1  # Muista vaihtaa 0

bot.counter = 0


@bot.command()
async def help(ctx):
    embed = discord.Embed(title="How to use the Team Bot?")
    embed.add_field(name="/team", value="Start the the team poll")
    embed.add_field(name="/autochannel_on", value="Create voice channels when /team is used")
    embed.add_field(name="/autochannel_off", value="Don't create voice channels when /team is used")
    embed.add_field(name="/shuffle", value="Randomize and divide the teams")
    embed.add_field(name="/aim", value="See how good your aim is")
    embed.add_field(name="/source", value="See the source code")
    embed.add_field(name="/count", value="Start the counter")
    await ctx.send(embed=embed)


@bot.command()
async def team(ctx):
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

    bot.channel1_id = discord.utils.get(bot.guild.channels, name="Team-1").id
    bot.channel2_id = discord.utils.get(bot.guild.channels, name="Team-2").id
    bot.channel1 = bot.get_channel(bot.channel1_id)
    bot.channel2 = bot.get_channel(bot.channel2_id)

    voice_channels.clear()


@bot.command()
async def shuffle(ctx):
    if shuffle_dict:

        items = list(shuffle_dict.items())
        random.shuffle(items)
        players1 = dict(list(shuffle_dict.items())[len(shuffle_dict) // 2:])
        players2 = dict(list(shuffle_dict.items())[:len(shuffle_dict) // 2])

        embed = discord.Embed(
            title="Divided Teams",
            colour=discord.Colour.blue()
        )
        embed.add_field(name="Team 1", value=f"{list(players1)}")
        embed.add_field(name="Team 2", value=f"{list(players2)}")
        await ctx.send(embed=embed)

        if bot.autochannel_state == 1:
            for user in players1:
                await players1[user].move_to(bot.channel1)
            for user in players2:
                await players2[user].move_to(bot.channel2)

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
async def count(ctx):
    bot.counter += 1
    await ctx.send(f"Counter is at {bot.counter}")



@bot.command()
async def aim(ctx):
    if "Martti" in ctx.author.name or "martti" in ctx.author.name:
        await ctx.send(f"{ctx.author.name}'s headshot accuracy is 100%")
    else:
        await ctx.send(f"{ctx.author.name}'s headshot accuracy is {random.randrange(0, 30)}%")


@bot.command()
async def source(ctx):
    await ctx.send("https://github.com/LauriAlanen/discord-team-bot/blob/main/main.py")

@bot.event
async def on_reaction_add(reaction, user):
    if user != bot.user:
        if str(reaction.emoji) == emoji:
            shuffle_dict[user.name] = user

bot.run("token")
