""""
Copyright © Krypton 2021 - https://github.com/kkrypt0nn
Description:
This is a template to create your own discord bot in python.

Version: 3.0
"""
import asyncio
import os
import sys
import json
import discord
from discord.ext import commands
from discord_slash import cog_ext, SlashContext
from subprocess import Popen, PIPE
from discord import FFmpegPCMAudio


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


    def playlistvideos(self, url: str):
        try:
            process = Popen(['youtube-dl.exe', '--flat-playlist', '--dump-single-json', '--playlist-random', url], stdout=PIPE, stderr=PIPE)
            playlist, stderr = process.communicate()
            playlist = json.loads(playlist)["entries"]
            return playlist
        except:
            print("songs not loaded", url)


    def audiourl(self, url: str):
        process = Popen(['youtube-dl.exe', '-g', '-f', 'bestaudio', url], stdout=PIPE, stderr=PIPE)
        audiourl, stderr = process.communicate()
        return audiourl



    @cog_ext.cog_slash(
        name="radio",
        description="enable radio.",
        guild_ids=[245513626381713408, 908764079177478185]
    )
    async def radio(self, context: SlashContext):
        self._videos = self.playlistvideos("https://www.youtube.com/playlist?list=PLmQipPGFsbYbujv3UnOaSYxrthRrakUVl")
        ctx = context
        voice = context.author.voice
        if not voice:
            await ctx.send("Может сперва в канал зайдешь?")
            return
        await ctx.send(" \"У Дебила FM\"")
        try:
            await voice.channel.connect()
        except: pass
        self._index = 0
        self.stream(ctx, self._index)

    def stream(self, context, index):
        video = self._videos[index]
        if not video:
            pass
        audiourl = self.audiourl(video["url"])
        voice = context.voice_client
        voice.stop()
        self._index += 1
        self.sendtitle(video, context)
        voice.play(FFmpegPCMAudio(audiourl), after=lambda x: self.stream(context, self._index))

    @cog_ext.cog_slash(
        name="leave",
        description="disable radio.",
        guild_ids=[245513626381713408, 908764079177478185]
    )
    async def leave(self, context: SlashContext):
        voice = context.voice_client
        voice.stop()
        await voice.disconnect()
        await context.send('Пока-пока')

    def sendtitle(self, video, context: SlashContext):
        msg = video["title"] + "[https://youtube.com/watch?v=" + video["url"] + "]"
        self._client.loop.create_task(context.channel.send(msg))

    @cog_ext.cog_slash(
        name="next",
        description="next song in playlist",
        guild_ids=[245513626381713408, 908764079177478185]
    )
    async def next(self, context: SlashContext):
        context.voice_client.stop()
        await context.send('next song')




def setup(bot):
    bot.add_cog(Radio(bot))
