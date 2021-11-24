""""
Copyright © Krypton 2021 - https://github.com/kkrypt0nn
Description:
This is a template to create your own discord bot in python.

Version: 3.0
"""
import asyncio
import os
import random
import sys
import json
import discord
import codecs
from discord.ext import commands
from discord_slash import cog_ext, SlashContext
from subprocess import Popen, PIPE
from discord.utils import get

from discord import FFmpegPCMAudio
from discord_slash.utils.manage_commands import create_option



if not os.path.isfile("config.json"):
    sys.exit("'config.json' not found! Please add it and try again.")
else:
    with open("config.json") as file:
        config = json.load(file)


class Radio(commands.Cog, name="radio"):

    def __init__(self, bot):
        self.bot = bot

    _index = 0
    _videos = []
    _client = discord.Client()
    _msg = None


    @cog_ext.cog_slash(
        name="play",
        description="play youtube video by url",
        guild_ids=[245513626381713408, 908764079177478185],
        options=[
            create_option(
                name="url",
                description="The question you want to ask.",
                option_type=3,
                required=True
            )
        ],
    )
    async def play(self, context: SlashContext, url: str):
        await self.add_to_queue(context, url)

    @cog_ext.cog_slash(
        name="radio",
        description="enable radio.",
        guild_ids=[245513626381713408, 908764079177478185]
    )
    async def radio(self, context: SlashContext):
        await self.add_to_queue(context, "https://www.youtube.com/playlist?list=PLmQipPGFsbYbujv3UnOaSYxrthRrakUVl")

    @cog_ext.cog_slash(
        name="voina",
        description="beskonechnaya strelba nad golovoi.",
        guild_ids=[245513626381713408, 908764079177478185]
    )
    async def voina(self, context: SlashContext):
        await self.add_to_queue(context, "https://www.youtube.com/watch?v=QPL0QDBuELw")

    @cog_ext.cog_slash(
        name="next",
        description="next song in playlist",
        guild_ids=[245513626381713408, 908764079177478185]
    )
    async def next(self, context: SlashContext):
        context.voice_client.stop()
        await context.send('next song')

    @cog_ext.cog_slash(
        name="993",
        description="1000-7",
        guild_ids=[245513626381713408, 908764079177478185]
    )
    async def shiza(self, context: SlashContext):
        await self.add_to_queue(context, "https://www.youtube.com/watch?v=eXvPgDmMLDk")

    @cog_ext.cog_slash(
        name="leave",
        description="disable radio.",
        guild_ids=[245513626381713408, 908764079177478185]
    )
    async def leave(self, context: SlashContext):
        self._videos = []
        self._index = 0
        voice = context.voice_client
        await voice.disconnect()
        await context.send('Пока-пока')

    def stream(self, context, index):
        try:
            video = self._videos[index]
        except IndexError:
            return
        audiourl = self.audiourl(video["url"])
        voice = context.voice_client
        try:
            voice.stop()
        except:
            pass
        self._index += 1
        FFMPEG_OPTIONS = {'before_options': '-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5',
                          'options': '-vn'}

        voice.play(FFmpegPCMAudio(audiourl, **FFMPEG_OPTIONS), after=lambda x: self.stream(context, self._index))
        self.sendtitle(video)

    def sendtitle(self, video):
        if "https://" not in video["url"]:
            video["url"] = "https://youtube.com/watch?v=" + video["url"]
        title = video["title"] + " [" + video["url"] + "]"
        self._client.loop.create_task(self._msg.edit(content=title))

    async def add_to_queue(self, context: SlashContext, url: str):
        ctx = context
        await ctx.send("Добавлено в очередь \"У Дебила FM\"")
        if "playlist" in url:
            videos = self.playlistvideos(url)
        else:
            videos =(self.singlevideo(url))
        self._msg = None

        voice = context.author.voice
        if not voice:
            await ctx.send("Может сперва в канал зайдешь?")
            return
        await self.lastmessage(ctx)
        try:
            await voice.channel.connect()
        except: pass
        voice = context.voice_client
        if not voice.is_playing():
            self._videos = videos
            self._index = 0
            self.stream(ctx, self._index)
        else:
            self._videos += videos

    async def lastmessage(self, context):
        message = await context.channel.fetch_message(context.channel.last_message_id)
        if message.author != self._client:
            pass
        self._msg = message


    def playlistvideos(self, url: str):
        try:
            process = Popen([self.getydl(), '--flat-playlist', '--dump-single-json', '--playlist-random', url], stdout=PIPE, stderr=PIPE)
            playlist, stderr = process.communicate()
            playlist = json.loads(playlist)["entries"]
            return playlist
        except:
            print("songs not loaded", url)

    def singlevideo(self, url: str):
            process = Popen([self.getydl(), '-e', url], stdout=PIPE, stderr=PIPE)
            title, stderr = process.communicate()
            song = {}
            song["title"] = codecs.decode(title, 'windows-1251')
            song["url"] = url
            return [song]


    def audiourl(self, url: str):
        process = Popen([self.getydl(), '-g', '-f', 'bestaudio', url], stdout=PIPE, stderr=PIPE)
        audiourl, stderr = process.communicate()
        return audiourl

    def getydl(self):
        ydl = "youtube-dl"
        if sys.platform == 'win32':
            ydl += '.exe'
        return ydl

def setup(bot):
    bot.add_cog(Radio(bot))
