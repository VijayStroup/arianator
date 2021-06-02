import sys
import discord
from discord.ext import commands


bot = commands.Bot(
    command_prefix='yaaas ',
    activity=discord.Activity(type=discord.ActivityType.listening, name='Positions')
)
bot.remove_command('help')


@bot.command(aliases=['ariana', 'ari'])
async def queen(ctx: commands.Context):
    await ctx.send('queen')


if __name__ == '__main__':
    token = sys.argv[1]
    bot.run(token)
