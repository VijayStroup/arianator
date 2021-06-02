import asyncio
import re
import sys
import aiohttp
import discord
from discord.ext import commands

bot = commands.Bot(
    command_prefix='yaaas ',
    activity=discord.Activity(type=discord.ActivityType.listening, name='Positions')
)
bot.remove_command('help')


@bot.event
async def on_ready():
    # get total number of pages of Ariana
    async with aiohttp.ClientSession() as session:
        coroutines = [ariana.request(session, ariana.url + '1')]
        data = await asyncio.gather(*coroutines)
        if not data:
            print('error requesting url')
            return
        
        pagesSearch = re.search(ariana.rePages, data[0])
        if not pagesSearch:
            print('error getting total pages')
            return

        try:
            ariana.nPages = int(pagesSearch.group(0).split('>')[1].split('<')[0])
        except ValueError:
            print('error parsing pages int')
            return

    print(f'Logged in as {bot.user}')


class Ariana:
    def __init__(self):
        self.url = 'https://www.gettyimages.com/photos/ariana-grande?page='
        self.reImgs = re.compile('/<img class="gallery-asset__thumb gallery-mosaic-asset__thumb"(.*?)>/g')
        self.reThumb = re.compile('/https:\/\/(.*?)"/g')
        self.rePages = re.compile('<span class="PaginationRow-module__lastPage___2pChH">(.*?)<\/span>')
        self.rePage = re.compile('/>(.*?)</g')
        self.rePage = re.compile('/>(.*?)</g')
        self.nPages = 0
    
    @staticmethod
    async def request(session: aiohttp.ClientSession, url: str):
        """Preform asynchronous http request"""

        try:
            async with session.get(url, timeout=2) as response:
                data = await response.read()
                return data.decode()
        except asyncio.TimeoutError: return None
        except Exception as e:
            print('Error with request:', e)
            return None


@bot.command(aliases=['ariana', 'ari'])
async def queen(ctx: commands.Context):
    await ctx.send('queen')


if __name__ == '__main__':
    ariana = Ariana()
    token = sys.argv[1]
    bot.run(token)
