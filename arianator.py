import asyncio
import io
import random
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

    pages_search = re.search(ariana.re_pages, data[0])
    if not pages_search:
        print('error getting total pages')
        return

    try:
        ariana.n_pages = int(pages_search.group(0).split('>')[1].split('<')[0])
    except ValueError:
        print('error parsing pages int')
        return

    print(f'Logged in as {bot.user}')


class Ariana:
    def __init__(self):
        self.url = 'https://www.gettyimages.com/photos/ariana-grande?page='
        self.re_imgs = re.compile('<img class="gallery-asset__thumb gallery-mosaic-asset__thumb"(.*?)>')
        self.re_thumb = re.compile('https://(.*?)"')
        self.re_pages = re.compile('<span class="PaginationRow-module__lastPage___2pChH">(.*?)<\/span>')
        self.n_pages = 0

    async def get_ari(self):
        page = random.randint(1, self.n_pages)

        async with aiohttp.ClientSession() as session:
            coroutines = [self.request(session, self.url + str(page))]
            data = await asyncio.gather(*coroutines)
            if not data:
                print('error requesting url')
                return

        img_search = re.findall(self.re_imgs, data[0])
        if not img_search:
            print('error img_search')
            return

        n = random.randint(0, len(img_search) - 1)

        img_url = re.search(self.re_thumb, img_search[n])
        if not img_url:
            print('error img_url')
            return

        img_url = img_url.group(0).replace('amp;', '')

        return img_url[:-1]

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
    ari = await ariana.get_ari()
    if not ari:
        ctx.reply('No Ariana Available.')
        return
    
    async with aiohttp.ClientSession() as session:
        print(ari)
        async with session.get(ari) as r:
            if r.status != 200: return
            ari = io.BytesIO(await r.read())
            await ctx.reply(file=discord.File(ari, filename='ari.jpg'))


if __name__ == '__main__':
    ariana = Ariana()
    token = sys.argv[1]
    bot.run(token)
