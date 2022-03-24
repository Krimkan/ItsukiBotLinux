# -*- coding: utf-8 -*-
import asyncio
import functools
import itertools
import math
import random

import discord
import youtube_dl
from async_timeout import timeout
from discord.ext import commands

from discord.ext import tasks
import datetime
import json
import sys
import sqlite3
from discord.utils import get
from discord.ext.commands import MissingPermissions

# Silence useless bug reports messages
youtube_dl.utils.bug_reports_message = lambda: ''


default_config={
    'TOKEN':None,
    'Prefix':'$',
    'Theme':'default',
    'antispam':True,
    'antispamMessages':5,
    'antispamPunish':1,
    'antispamTimer':3,
    'antilink':True,
    'antilinkPunish':1,
    'banDesc':"Забанен новый аккаунт",
    'banNewAccounts': True,
    'requiredDays':2,
    'autoDenyBotRoles':False,
}
connection = sqlite3.connect('server.db',check_same_thread=False)
cursor = connection.cursor()

def themeColors(ThemeName):
    if ThemeName == 'Default':
        color=0x000000
        return color
    elif ThemeName == 'Red':
        color = 0xff4246
        return color
    elif ThemeName == 'Blue':
        color = 0x42ffff
        return color
    elif ThemeName == 'Green':
        color = 0x42ff50
        return color
    elif ThemeName == 'Yellow':
        color = 0xfff142
        return color
    else:
        color = False
        return color

filename = 'config.json'
def configs():
    print('Проверка Настроек..')
    try:
        with open("config.json", "r") as read:
            config = json.load(read)
            try:
                TOKEN = config["TOKEN"]
                pr = config["Prefix"]
                theme=config['Theme']
                antispam = config["antispam"]
                antispamMessages = config['antispamMessages']
                antispamTimer = config['antispamTimer']
                antispamPunish = config['antispamPunish']
                antilink = config['antilink']
                antilinkPunish = config['antilinkPunish']
                banDesc = config["banDesc"]
                autoDenyBotRoles = config['autoDenyBotRoles']
                print('Настройки Найдены')
                print('---------')
                print(f'Чтобы зайти в настройки Напишите Y |Чтобы продолжить нажмите на Enter')
                sIn = input('Подтвердить?')
                if sIn == 'Y' or sIn == 'y':
                    print('---Настройки---')
                    print(f'TOKEN:{TOKEN} |Чтобы Изменить Пропишите TOKEN')
                    print(f'Prefix:{pr} |Чтобы Изменить Пропишите Prefix')
                    print(f'Theme:{theme}|Чтобы Изменить Пропишите theme')
                    print(f'antispamMessages:{antispamMessages}|Чтобы Изменить Пропишите antispamMessages')
                    print(f'antispamTimer:{antispamTimer}|Чтобы Изменить Пропишите antispamTimer')
                    print(f'antilink:{antilink}|Чтобы Изменить Пропишите antilink')
                    print('Чтобы Выйти из настроек введите cancel')
                    com = input(f'Введите Настройку для изменения:')
                    if com == 'TOKEN':
                        print('---------')
                        print(f'Для Отмены Напишите cancel')
                        eTOKEN = input('Новый Токен:')
                        if eTOKEN == 'cancel':
                            print('Отмена и перезапуск..')
                            configs()
                        else:
                            print('Токен Принят Перезагрузка..')
                            config["TOKEN"] = eTOKEN
                            with open("config.json", "w") as write:
                                json.dump(config, write, indent=4)
                            configs()
                    elif com == 'Prefix':
                        print('---------')
                        print(f'Для Отмены Напишите cancel')
                        ePr = input('Новый Префикс:')
                        if ePr == 'cancel':
                            print('Отмена и перезапуск..')
                            configs()
                        else:
                            print('Префикс Принят Перезагрузка..')
                            config["Prefix"] = ePr
                            with open("config.json", "w") as write:
                                json.dump(config, write, indent=4)
                            configs()
                    elif com == 'Theme':
                        print('---------')
                        print(f'Для Отмены Напишите cancel')
                        ePr = input('Новая Тема(Чтобы Изменить на начальные пропишите default):')
                        if ePr == 'cancel':
                            print('Отмена и перезапуск..')
                            configs()
                        else:

                            if themeColors(ePr) == False:
                                print('НЕВЕРНАЯ ТЕМА ВВЕДИТЕ ИЛИ HEX ЦВЕТ ИЛИ ИЗ ЭТИХ тем Red,Green,Blue,Yellow,default'
                                      'в следующий раз'
                                      '\n Перезагрузка..')
                            else:
                                print('Тема Принята Перезагрузка..')
                                config["Prefix"] = ePr
                                with open("config.json", "w") as write:
                                    json.dump(config, write, indent=4)
                                configs()

                        print('---------')
                        print(f'Для Отмены Напишите cancel')
                        eTOKEN = input('Монеты за приглашение:')
                        if eTOKEN == 'cancel':
                            print('Отмена и перезапуск..')
                            configs()
                        else:
                            try:
                                eTOKEN = float(eTOKEN)
                                print(f'Монеты за приглашение :{eTOKEN}\n Приняты Перезагрузка..')
                                config["inviteCoins"] = eTOKEN
                                with open("config.json", "w") as write:
                                    json.dump(config, write, indent=4)
                                configs()
                            except ValueError:
                                print(f'{eTOKEN} Не является цифрой Перезагрузка..')
                                configs()
                    elif com == 'antispamMessages':
                        print('---------')
                        print(f'Для Отмены Напишите cancel')
                        eTOKEN = input('Сколько сообщений можно написать до сброса таймера:')
                        if eTOKEN == 'cancel':
                            print('Отмена и перезапуск..')
                            configs()
                        else:
                            try:
                                eTOKEN = int(eTOKEN)
                                print(f'Сообщений до Сброса :{eTOKEN}\n Принято Перезагрузка..')
                                config["antispamMessages"] = eTOKEN
                                with open("config.json", "w") as write:
                                    json.dump(config, write, indent=4)
                                configs()
                            except ValueError:
                                print(f'{eTOKEN} Не является цифрой Перезагрузка..')
                                configs()
                    elif com == 'antispamTimer':
                        print('---------')
                        print(f'Для Отмены Напишите cancel')
                        eTOKEN = input('Время сброса таймера(секунды):')
                        if eTOKEN == 'cancel':
                            print('Отмена и перезапуск..')
                            configs()
                        else:
                            try:
                                eTOKEN = int(eTOKEN)
                                print(f'Время до Сброса :{eTOKEN}\n Принято Перезагрузка..')
                                config["antispamTimer"] = eTOKEN
                                with open("config.json", "w") as write:
                                    json.dump(config, write, indent=4)
                                configs()
                            except ValueError:
                                print(f'{eTOKEN} Не является цифрой Перезагрузка..')
                                configs()
                    elif com == 'Prefix':
                            print(f'Теперь значение antilink = {antilink} Перезагрузка..')
                            config["antilink"] = not(antilink)
                            with open("config.json", "w") as write:
                                json.dump(config, write, indent=4)
                            configs()
                    elif com == 'cancel':
                        print(f'Отмена Перезагрузка..')
                        configs()
                    else:
                        print(f'Такой Команды не существует! Перезагрузка..')
                        configs()
            except KeyError:
                print(f"Поврежденны Настройки Сбросить Настройки?:")
                key=input(f'Y/N:')
                if key == 'Y':
                    print('Загрузка Настроек По Умолчанию')
                    TOKEN = input('Введите Ваш Токен:')
                    default_config["TOKEN"] = TOKEN
                    print('Ваш Токен Принят')
                    with open("config.json", "w") as write:
                        json.dump(default_config, write, indent=4)
                else:
                    print(f'Посмотрите файл config.json и введите нужные Параметры или свяжитесь по дискорду с Hin200#2960 и скиньте файл:config.json ')
                    sys.exit()
    except FileNotFoundError:
        print('---Настройки Отсутствуют---')
        print('Загрузка Настроек По Умолчанию')
        TOKEN = input('Введите Ваш Токен:')
        default_config["TOKEN"] = TOKEN
        print('Ваш Токен Принят')
        with open("config.json", "w") as write:
            json.dump(default_config, write, indent=4)
        configs()
#TOKEN-------------------------------------------------------------------------------------------------------------------------------------------------

config = configs()

with open("config.json", "r") as read:
    config = json.load(read)
autoDenyBotRoles = config["autoDenyBotRoles"]
TOKEN = config["TOKEN"]
pr = config["Prefix"]
theme=config['Theme']
antispam = config["antispam"]
antispamMessages = config['antispamMessages']
antispamTimer = config['antispamTimer']
antilink = config['antilink']
antispamPunish = config['antispamPunish']
antilinkPunish = config['antilinkPunish']
banDesc = config["banDesc"]
banNewAccounts = config["banNewAccounts"]
requiredDays = config["requiredDays"]
themeColor = themeColors(theme)
print('Бот Запускается..')

invites = {}


def clear_from_opostrov(raw):
    out = str(raw).replace("'", '')
    return out
class VoiceError(Exception):
    pass


class YTDLError(Exception):
    pass


class YTDLSource(discord.PCMVolumeTransformer):
    YTDL_OPTIONS = {
        'format': 'bestaudio/best',
        'extractaudio': True,
        'audioformat': 'mp3',
        'outtmpl': '%(extractor)s-%(id)s-%(title)s.%(ext)s',
        'restrictfilenames': True,
        'noplaylist': True,
        'nocheckcertificate': True,
        'ignoreerrors': False,
        'logtostderr': False,
        'quiet': True,
        'no_warnings': True,
        'default_search': 'auto',
        'source_address': '0.0.0.0',
    }

    FFMPEG_OPTIONS = {
        'before_options': '-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5',
        'options': '-vn',
    }

    ytdl = youtube_dl.YoutubeDL(YTDL_OPTIONS)

    def __init__(self, ctx: commands.Context, source: discord.FFmpegPCMAudio, *, data: dict, volume: float = 0.5):
        super().__init__(source, volume)

        self.requester = ctx.author
        self.channel = ctx.channel
        self.data = data

        self.uploader = data.get('uploader')
        self.uploader_url = data.get('uploader_url')
        date = data.get('upload_date')
        self.upload_date = date[6:8] + '.' + date[4:6] + '.' + date[0:4]
        self.title = data.get('title')
        self.thumbnail = data.get('thumbnail')
        self.description = data.get('description')
        self.duration = self.parse_duration(int(data.get('duration')))
        self.tags = data.get('tags')
        self.url = data.get('webpage_url')
        self.views = data.get('view_count')
        self.likes = data.get('like_count')
        self.dislikes = data.get('dislike_count')
        self.stream_url = data.get('url')

    def __str__(self):
        return '**{0.title}** by **{0.uploader}**'.format(self)

    @classmethod
    async def create_source(cls, ctx: commands.Context, search: str, *, loop: asyncio.BaseEventLoop = None):
        loop = loop or asyncio.get_event_loop()

        partial = functools.partial(cls.ytdl.extract_info, search, download=False, process=False)
        data = await loop.run_in_executor(None, partial)

        if data is None:
            raise YTDLError('Couldn\'t find anything that matches `{}`'.format(search))

        if 'entries' not in data:
            process_info = data
        else:
            process_info = None
            for entry in data['entries']:
                if entry:
                    process_info = entry
                    break

            if process_info is None:
                raise YTDLError('Couldn\'t find anything that matches `{}`'.format(search))

        webpage_url = process_info['webpage_url']
        partial = functools.partial(cls.ytdl.extract_info, webpage_url, download=False)
        processed_info = await loop.run_in_executor(None, partial)

        if processed_info is None:
            raise YTDLError('Couldn\'t fetch `{}`'.format(webpage_url))

        if 'entries' not in processed_info:
            info = processed_info
        else:
            info = None
            while info is None:
                try:
                    info = processed_info['entries'].pop(0)
                except IndexError:
                    raise YTDLError('Couldn\'t retrieve any matches for `{}`'.format(webpage_url))

        return cls(ctx, discord.FFmpegPCMAudio(info['url'], **cls.FFMPEG_OPTIONS), data=info)

    @staticmethod
    def parse_duration(duration: int):
        minutes, seconds = divmod(duration, 60)
        hours, minutes = divmod(minutes, 60)
        days, hours = divmod(hours, 24)

        duration = []
        if days > 0:
            duration.append('{} дней'.format(days))
        if hours > 0:
            duration.append('{} часов'.format(hours))
        if minutes > 0:
            duration.append('{} минут'.format(minutes))
        if seconds > 0:
            duration.append('{} секунд'.format(seconds))

        return ', '.join(duration)


class Song:
    __slots__ = ('source', 'requester')

    def __init__(self, source: YTDLSource):
        self.source = source
        self.requester = source.requester

    def create_embed(self):
        embed = (discord.Embed(title='Сейчас играет',
                               description='```css\n{0.source.title}\n```'.format(self),
                               color=discord.Color.blurple())
                 .add_field(name='Время прослушивания', value=self.source.duration)
                 .add_field(name='Запросил', value=self.requester.mention)
                 .add_field(name='Автор видео', value='[{0.source.uploader}]({0.source.uploader_url})'.format(self))
                 .add_field(name='Ссылка(кликни)', value='[Click]({0.source.url})'.format(self))
                 .set_thumbnail(url=self.source.thumbnail))

        return embed


class SongQueue(asyncio.Queue):
    def __getitem__(self, item):
        if isinstance(item, slice):
            return list(itertools.islice(self._queue, item.start, item.stop, item.step))
        else:
            return self._queue[item]

    def __iter__(self):
        return self._queue.__iter__()

    def __len__(self):
        return self.qsize()

    def clear(self):
        self._queue.clear()

    def shuffle(self):
        random.shuffle(self._queue)

    def remove(self, index: int):
        del self._queue[index]


class VoiceState:
    def __init__(self, bot: commands.Bot, ctx: commands.Context):
        self.bot = bot
        self._ctx = ctx

        self.current = None
        self.voice = None
        self.next = asyncio.Event()
        self.songs = SongQueue()

        self._loop = False
        self._volume = 0.5
        self.skip_votes = set()

        self.audio_player = bot.loop.create_task(self.audio_player_task())

    def __del__(self):
        self.audio_player.cancel()

    @property
    def loop(self):
        return self._loop

    @loop.setter
    def loop(self, value: bool):
        self._loop = value

    @property
    def volume(self):
        return self._volume

    @volume.setter
    def volume(self, value: float):
        self._volume = value

    @property
    def is_playing(self):
        return self.voice and self.current

    async def audio_player_task(self):
        while True:
            self.next.clear()

            if not self.loop:
                # Try to get the next song within 3 minutes.
                # If no song will be added to the queue in time,
                # the player will disconnect due to performance
                # reasons.
                try:
                    async with timeout(180):  # 3 minutes
                        self.current = await self.songs.get()
                except asyncio.TimeoutError:
                    self.bot.loop.create_task(self.stop())
                    return

            self.current.source.volume = self._volume
            self.voice.play(self.current.source, after=self.play_next_song)
            await self.current.source.channel.send(embed=self.current.create_embed())

            await self.next.wait()

    def play_next_song(self, error=None):
        if error:
            raise VoiceError(str(error))

        self.next.set()

    def skip(self):
        self.skip_votes.clear()

        if self.is_playing:
            self.voice.stop()

    async def stop(self):
        self.songs.clear()

        if self.voice:
            await self.voice.disconnect()
            self.voice = None


class Music(commands.Cog):

    @commands.has_permissions(administrator=True)
    @commands.command(name='embedCreate', pass_context=True)
    async def __embedCreate(self,ctx: commands.Context):
            ember = discord.Embed(title=f'Слишком долгий ответ напишите команду еще раз чтобы повторить',
                                  colour=themeColor);

            def check(msg):
                return msg.author == ctx.author and msg.channel == ctx.channel

            emb = discord.Embed(title=f'Напишите Оглавление!', colour=themeColor);
            await ctx.send(embed=emb)
            try:
                itemName = await client.wait_for("message", check=check);
                itemName = itemName.content
                embedRedact = discord.Embed(title="Теперь Введите Что хотите Изменить!",
                                            description="\nname-изменяет Заглавление"
                                                        "\ndesc-Добавляет Описание"
                                                        "\nbImg-Добавляет изображение снизу"
                                                        "\npImg-Добавляет изображение (как карточка)"
                                                        "\nsetFooter-Добавляет Текст снизу"
                                                        "\nauthorName-Добавляет Текст сверху"
                                                        "\nauthorImg-Добавляет Значок"
                                                        "\nchannelSet-Меняет канал куда будет отправлен Пост"
                                                        "\ncolor-Меняет Цвет обводки сообщения"
                                                        "\nFinish-Закончит редактирование и отправит сообщение",
                                            colour=themeColor)
                desc = None;
                bImg = None;
                pImg = None;
                footer = None;
                authorImg = None;
                channelSet = ctx.channel;
                authorName = None;
                col = themeColor

                async def edit_embed(src):  # 0name 1desc 2bImg 3pImg 4footer 5authorImg 6Channel 7authorName 8color
                    if src == "name":
                        redEmb = discord.Embed(title="Введите новое название для Сообщения!")
                        await ctx.send(embed=redEmb)
                        src = await client.wait_for("message", check=check, );
                        src = src.content;
                        src = [0, src]
                        return src  # 0
                    elif src == "desc":
                        redEmb = discord.Embed(title="Введите новое Описание для Сообщения!")
                        await ctx.send(embed=redEmb)
                        src = await client.wait_for("message", check=check, );
                        src = src.content;
                        src = [1, src]
                        return src
                    elif src == "bImg":
                        redEmb = discord.Embed(title="Выложите изображение чтобы поменять сообщение")
                        await ctx.send(embed=redEmb)
                        src = await client.wait_for("message", check=check, );
                        try:
                            src = src.attachments[0];
                            src = [2, f'{src}']
                        except IndexError:
                            src = ['ERROR']
                        return src
                    elif src == "pImg":
                        redEmb = discord.Embed(title="Выложите изображение чтобы поменять сообщение")
                        await ctx.send(embed=redEmb)
                        src = await client.wait_for("message", check=check);
                        try:
                            src = src.attachments[0];
                            src = [3, f'{src}']
                        except IndexError:
                            src = ['ERROR']
                        return src
                    elif src == "setFooter":
                        redEmb = discord.Embed(title="Введите подтекст для Сообщения!")
                        await ctx.send(embed=redEmb)
                        src = await client.wait_for("message", check=check);
                        src = src.content;
                        src = [4, src]
                        return src
                    elif src == "authorImg":
                        redEmb = discord.Embed(title="Введите Значок Автора для Сообщения!")
                        await ctx.send(embed=redEmb)
                        src = await client.wait_for("message", check=check);
                        try:
                            src = src.attachments[0];
                            src = [5, f'{src}']
                        except IndexError:
                            src = ['ERROR']
                        return src
                    elif src == "channelSet":
                        redEmb = discord.Embed(title="Введите ID канала куда будет послано сообщение!")
                        await ctx.send(embed=redEmb)
                        src = await client.wait_for("message", check=check);
                        try:
                            src = int(src.content);
                            src = [6, src]
                        except ValueError:
                            src = "ERROR"
                        return src
                    elif src == "authorName":
                        redEmb = discord.Embed(title="Введите Автора для Сообщения!")
                        await ctx.send(embed=redEmb)
                        src = await client.wait_for("message", check=check);
                        src = src.content;
                        src = [7, src]
                        return src
                    elif src == "color":
                        redEmb = discord.Embed(title="Введите Цвет обводки сообщения!",
                                               description="Доступные:\nКрасный-введите `Red`\nЗеленый-введите `Green`\nСиний-введите `Blue`\nЖелтый-введите `Yellow`\nЧерный-введите `default`")
                        await ctx.send(embed=redEmb)
                        src = await client.wait_for("message", check=check);
                        src = src.content
                        if themeColors(src) == False:
                            await ctx.send(discord.Embed(
                                title='НЕВЕРНАЯ ТЕМА ВВЕДИТЕ ИЗ ЭТИХ тем \nRed,Green,Blue,Yellow,default(Черный) в следующий раз'))
                        else:
                            src = [8, themeColors(src)]
                            return src
                    elif src == "Finish":
                        return True
                    else:
                        return "ERROR"

                GEmbed = discord.Embed(title=itemName, colour=col)
                while True:  # None-s
                    await ctx.send(embed=embedRedact)
                    src = await client.wait_for("message", check=check);
                    complete = await edit_embed(src.content)
                    if type(complete) == list:
                        messg = discord.Embed(title='')
                        if complete[0] == 0:
                            itemName = complete[1]
                        elif complete[0] == 1:
                            desc = complete[1]
                        elif complete[0] == 2:
                            bImg = complete[1]
                        elif complete[0] == 3:
                            pImg = complete[1]
                        elif complete[0] == 4:
                            footer = complete[1]
                        elif complete[0] == 5:
                            authorImg = complete[1]
                        elif complete[0] == 6:
                            channelSet = complete[1]
                        elif complete[0] == 7:
                            authorName = complete[1]
                        elif complete[0] == 8:
                            col = complete[1]
                    elif complete == "ERROR":
                        await ctx.send(embed=discord.Embed(title="Ошибка При введений параметров"), colour=themeColor)
                    elif complete == True:
                        await ctx.send(embed=discord.Embed(title="Сообщение Успешно Отправлено!"))
                        break
                    else:
                        await ctx.send(embed=discord.Embed(title="Ошибка"), colour=themeColor)
                    # make embed
                    if desc != None:
                        GEmbed = discord.Embed(title=itemName, description=desc, colour=col)
                    else:
                        GEmbed = discord.Embed(title=itemName, colour=col)
                    if bImg != None:
                        GEmbed.set_thumbnail(url=bImg)
                    if pImg != None:
                        GEmbed.set_image(url=pImg)
                    if footer != None:
                        GEmbed.set_footer(text=footer)
                    if authorName != None:
                        GEmbed.set_author(name=authorName)
                    if authorImg != None:
                        GEmbed.set_author(icon_url=authorImg)
                    if authorImg != None and authorName != None:
                        GEmbed.set_author(name=authorName, icon_url=authorImg)
                    # sending Embed
                    await ctx.send(embed=GEmbed)
                if type(channelSet) == int:
                    channelSet = client.get_channel(channelSet)
                print(channelSet)
                await channelSet.send(embed=GEmbed)
            except asyncio.TimeoutError:
                await ctx.send(embed=ember)

    # ---------------------------EVENTS---------------------------------------------------

    global cooldown
    cooldown = {}

    @tasks.loop(seconds=antispamTimer)
    async def stats_update():
        global cooldown
        cooldown = {}

    async def warn_action(self, ctx: commands.Context):
        warnActions = cursor.execute("SELECT * FROM warnActions").fetchall()
        for warnAction in warnActions:
            id = warnAction[0]
            warn = warnAction[1]
            Action = warnAction[2]
            deleteWarns = warnAction[3]
            for member in ctx.guild.members:
                if cursor.execute(f"SELECT warns FROM warns WHERE user = {member.id}").fetchone()[0] == warn:
                    if len(Action) == 1:
                        await member.kick(reason="Получение множественных предупреждений")
                    elif Action[0] == '1':
                        await Music._mute(self, ctx=ctx, member=member, amout=Action[1:],
                                    reason="Множественные предупреждения")
                        if deleteWarns == True:
                            cursor.execute(f"UPDATE warns SET warns = 0 WHERE user = {member.id}")
                        else:
                            cursor.execute(f"UPDATE warns SET warns = warns + 1 WHERE user = {member.id}")
                        if deleteWarns == True:
                            cursor.execute(f"UPDATE warns SET warns = 0 WHERE user = {member.id}")
                        else:
                            cursor.execute(f"UPDATE warns SET warns = warns + 1 WHERE user = {member.id}")
                    elif Action[0] == '2':
                        await Music._tempban(self, ctx=ctx, member=member, amout=Action[1:],
                                       reason="Множественные предупреждения")
                        if deleteWarns == True:
                            cursor.execute(f"UPDATE warns SET warns = 0 WHERE user = {member.id}")
                        else:
                            cursor.execute(f"UPDATE warns SET warns = warns + 1 WHERE user = {member.id}")

    # -------------------------------------------ADMIN------------------------------

    @commands.is_owner()
    @commands.command(name='aHelp', pass_context=True)
    async def __ahelp(self, ctx: commands.Context):
        con = False
        if ctx.author == ctx.guild.owner:
            con = True
        if con == True:
            await ctx.message.add_reaction('✅')
            emb = discord.Embed(title="Помощь по Админским Командам!",
                                description=f"\n 1) `{pr}editPrefix [Новый Префикс]` |Изменяет Префикс сейчас стоит:{pr}"
                                            f"\n 2) `{pr}editTheme [Имя Цвета(Доступны:Red,Blue,Green,Yellow)]` |Изменяет Цвет некоторых частей сообщений"
                                            f"\n 3) `{pr}mhelp` | Узнать команды модераций."
                                , color=themeColor)
            emb.set_footer(text="[В этих скобках Обязательные параметры] <Необязательные Параметры>")
            await ctx.channel.send(embed=emb)

    @commands.is_owner()
    @commands.command(name='editPrefix')
    async def __editPrefix(self, ctx: commands.Context, Prefix=None):
        con = True
        if con == True:
            global pr
            if Prefix != None:
                with open("config.json", "r") as read:
                    config = json.load(read)
                pr = Prefix
                client.command_prefix = pr
                config["Prefix"] = pr
                with open("config.json", "w") as write:
                    json.dump(config, write, indent=4)
                emb = discord.Embed(title=f'Ваш Новый Префикс: `{pr}` \n Принят', color=themeColor)
                with open("config.json", "r") as read:
                    config = json.load(read)
                await ctx.channel.send(embed=emb)
            else:
                emb = discord.Embed(title=f'Отправьте команду с префиксом в следующий раз',
                                    description=f'Пример:\n{pr}editPrefix **/**', colour=themeColor)
                await ctx.channel.send(embed=emb)
        else:
            emb = discord.Embed(title=f'Недостаточно Прав', colour=themeColor)
            await ctx.channel.send(embed=emb)

    @commands.is_owner()
    @commands.command(name='editTheme')
    async def __editTheme(self, ctx: commands.Context, NTheme=None):
        global themeColor
        NewTheme = themeColors(NTheme)
        if NewTheme == False:
            if NTheme == None:
                emb = discord.Embed(title=f"Введите Тему(Red,Blue,Green,Yellow,Default) с командой",
                                    color=themeColor)
            else:
                emb = discord.Embed(title=f"{NTheme} Не является ни одной из Тем(Red,Blue,Green,Yellow,Default)",
                                    color=themeColor)
            await ctx.channel.send(embed=emb)
        else:
            themeColor = int(NewTheme)
            with open("config.json", "r") as read:
                config = json.load(read)
            config["Theme"] = NTheme
            with open("config.json", "w") as write:
                json.dump(config, write, indent=4)
            emb = discord.Embed(title=f'Ваша Новая Тема: `{NTheme}` \n Принята!', colour=themeColor)
            await ctx.channel.send(embed=emb)

    # ----------------------------Moderation Events----------------------------------------
    @commands.has_permissions(administrator=True)
    @commands.command(name='antilink')
    async def __antilink(self, ctx: commands.Context):
        emb_user = discord.Embed(title='Выберите Пункт', color=themeColor)
        emb_user.add_field(name='❌ | Выключить\n'
                                '👊 | Выбрать Наказание', value=ctx.author.mention, inline=False)
        s = await ctx.channel.send(embed=emb_user)
        await s.add_reaction('❌');
        await s.add_reaction('👊')

        def check(reaction, user):
            return user == ctx.author and str(reaction.emoji) in ['👊', '❌']

        try:
            global antilink
            reaction, user = await client.wait_for('reaction_add', timeout=60.0, check=check)
            if str(reaction.emoji) == '❌':
                if antilink == True:
                    say = "Выключено"
                else:
                    say = "Включено"
                await s.clear_reactions()
                embed = discord.Embed(title=f"Успешно {say}")
                await s.edit(embed=embed)
                antilink = not (antilink)
                config["antilink"] = antilink
                with open("config.json", "w") as write:
                    json.dump(config, write, indent=4)
            elif str(reaction.emoji) == '👊':
                global antilinkPunish
                emb = discord.Embed(title=f"Выберите Тип Наказания за ссылки", description=
                '⚠| Предупреждение\n'
                '🔇| Мут \n'
                '💥| Бан', colour=themeColor)
                await s.clear_reactions()
                await s.edit(embed=emb)
                await s.add_reaction('⚠')
                await s.add_reaction('🔇')
                await s.add_reaction('💥')

                def check(reaction, user):
                    return user == ctx.author and str(reaction.emoji) in ['⚠', '🔇', '💥']

                reaction, user = await client.wait_for('reaction_add', timeout=60.0, check=check)
                if str(reaction.emoji) == '⚠':
                    antilinkPunish = 1
                    config["antilinkPunish"] = antilinkPunish
                    with open("config.json", "w") as write:
                        json.dump(config, write, indent=4)
                    embed = discord.Embed(title="Теперь Выдается Предупреждение за ссылки", colour=themeColor)
                    await s.clear_reactions()
                    await s.edit(embed=embed)

                elif str(reaction.emoji) == '🔇':
                    embed = discord.Embed(title="Теперь Выдается Мут за ссылки теперь выберите на сколько",
                                          description="(д-дней, ч-часы, м-минут, с-секунды)\n"
                                                      "Пример:\n"
                                                      "1д")
                    await s.clear_reactions()
                    await s.edit(embed=embed)

                    def check(msg):
                        return msg.author == ctx.author and msg.channel == ctx.channel

                    itemName = await client.wait_for("message", check=check, timeout=60)
                    await itemName.delete()
                    itemName = itemName.content
                    try:
                        int(itemName[:-1])
                        if itemName[-1:] not in ['с', 'м', "ч", "д"]:
                            return await s.edit(
                                embed=discord.Embed(title="Вы не правильно ввели Время!", colour=themeColor))
                        antilinkPunish = [2, f'{itemName}']
                    except ValueError:
                        return await s.edit(
                            embed=discord.Embed(title="Вы не правильно ввели Время!", colour=themeColor))
                    embed = discord.Embed(title="Теперь Выдается Мут за ссылки", colour=themeColor)
                    await s.clear_reactions()
                    await s.edit(embed=embed)

                    config["antilinkPunish"] = antilinkPunish
                    with open("config.json", "w") as write:
                        json.dump(config, write, indent=4)

                elif str(reaction.emoji) == '💥':
                    antilinkPunish = 3
                    embed = discord.Embed(title="Теперь Выдается Бан за ссылки", colour=themeColor)
                    await s.clear_reactions()
                    await s.edit(embed=embed)
                    config["antilinkPunish"] = antilinkPunish
                    with open("config.json", "w") as write:
                        json.dump(config, write, indent=4)

        except asyncio.TimeoutError:
            ember = discord.Embed(title=f'Слишком долгий ответ напишите команду еще раз чтобы повторить',
                                  colour=themeColor)
            await s.edit(embed=ember)

    @commands.has_permissions(administrator=True)
    @commands.command(name='antispam')
    async def __antispam(self, ctx: commands.Context):
        emb_user = discord.Embed(title='Выберите Пункт', color=themeColor)
        emb_user.add_field(name='❌ | Выключить\n'
                                '👊 | Выбрать Наказание', value=ctx.author.mention, inline=False)
        s = await ctx.channel.send(embed=emb_user)
        await s.add_reaction('❌');
        await s.add_reaction('👊')

        def check(reaction, user):
            return user == ctx.author and str(reaction.emoji) in ['👊', '❌']

        try:
            global antispam
            reaction, user = await client.wait_for('reaction_add', timeout=60.0, check=check)
            if str(reaction.emoji) == '❌':
                if antispam == True:
                    say = "Выключено"
                else:
                    say = "Включено"
                await s.clear_reactions()
                embed = discord.Embed(title=f"Успешно {say}")
                await s.edit(embed=embed)
                antispam = not (antispam)
                config["antispam"] = antispam
                with open("config.json", "w") as write:
                    json.dump(config, write, indent=4)
            elif str(reaction.emoji) == '👊':
                global antispamPunish
                emb = discord.Embed(title=f"Выберите Тип Наказания за спам", description=
                '⚠| Предупреждение\n'
                '🔇| Мут \n'
                '💥| Бан', colour=themeColor)
                await s.clear_reactions()
                await s.edit(embed=emb)
                await s.add_reaction('⚠')
                await s.add_reaction('🔇')
                await s.add_reaction('💥')

                def check(reaction, user):
                    return user == ctx.author and str(reaction.emoji) in ['⚠', '🔇', '💥']

                reaction, user = await client.wait_for('reaction_add', timeout=60.0, check=check)
                if str(reaction.emoji) == '⚠':
                    antispamPunish = 1
                    config["antispamPunish"] = antispamPunish
                    with open("config.json", "w") as write:
                        json.dump(config, write, indent=4)
                    embed = discord.Embed(title="Теперь Выдается Предупреждение за спам", colour=themeColor)
                    await s.clear_reactions()
                    await s.edit(embed=embed)

                elif str(reaction.emoji) == '🔇':
                    embed = discord.Embed(title="Теперь Выдается Мут за спам теперь выберите на сколько",
                                          description="(д-дней, ч-часы, м-минут, с-секунды)\n"
                                                      "Пример:\n"
                                                      "1д")
                    await s.clear_reactions()
                    await s.edit(embed=embed)

                    def check(msg):
                        return msg.author == ctx.author and msg.channel == ctx.channel

                    itemName = await client.wait_for("message", check=check, timeout=60)
                    await itemName.delete()
                    itemName = itemName.content
                    try:
                        int(itemName[:-1])
                        if itemName[-1:] not in ['с', 'м', "ч", "д"]:
                            return await s.edit(
                                embed=discord.Embed(title="Вы не правильно ввели Время!", colour=themeColor))
                        antispamPunish = [2, f'{itemName}']
                    except ValueError:
                        return await s.edit(
                            embed=discord.Embed(title="Вы не правильно ввели Время!", colour=themeColor))
                    embed = discord.Embed(title="Теперь Выдается мут за спам", colour=themeColor)
                    await s.clear_reactions()
                    await s.edit(embed=embed)

                    config["antispamPunish"] = antispamPunish
                    with open("config.json", "w") as write:
                        json.dump(config, write, indent=4)

                elif str(reaction.emoji) == '💥':
                    antispamPunish = 3
                    embed = discord.Embed(title="Теперь Выдается Бан за спам", colour=themeColor)
                    await s.clear_reactions()
                    await s.edit(embed=embed)
                    config["antispamPunish"] = antispamPunish
                    with open("config.json", "w") as write:
                        json.dump(config, write, indent=4)

        except asyncio.TimeoutError:
            ember = discord.Embed(title=f'Слишком долгий ответ напишите команду еще раз чтобы повторить',
                                  colour=themeColor)
            await ctx.channel.send(embed=ember)

    @commands.has_permissions(administrator=True)
    @commands.command(name='warn_actions')
    async def __warn_actions(self, ctx: commands.Context):
        ember = discord.Embed(title=f'Слишком долгий ответ напишите команду еще раз чтобы повторить',
                              colour=themeColor)
        emb_user = discord.Embed(title='Выберите Пункт', description='📃|Модифицировать существующие действия\n'
                                                                     '📝 | Добавить Новое действие'
                                                                     '🗑| Удалить действия', color=themeColor)
        s = await ctx.channel.send(embed=emb_user)
        await s.add_reaction('📃')
        await s.add_reaction('📝')
        await s.add_reaction('🗑')

        def check(reaction, user):
            return user == ctx.author and str(reaction.emoji) in '🗑📝📃'

        try:
            reaction, user = await client.wait_for('reaction_add', timeout=60.0, check=check)

            def editRules(Rules):
                pass

            id = len(cursor.execute("SELECT * FROM warnActions").fetchall()) + 1

            if str(reaction.emoji) == '📝':
                await s.clear_reactions()
                embed = discord.Embed(title=f"Напишите Количество Варнов для выполнения действия\n Например:`3`")
                await s.edit(embed=embed)

                def check(msg):
                    return msg.author == ctx.author and msg.channel == ctx.channel

                try:
                    warn = await client.wait_for("message", check=check, timeout=60)
                except asyncio.TimeoutError:
                    return await s.edit(embed=ember)

                await warn.delete()

                try:
                    warn = int(warn.content)
                except ValueError:
                    return await s.edit(
                        embed=discord.Embed(title="Вы не правильно ввели Время!", colour=themeColor))

                Action = [warn]
                embed = discord.Embed(title="**Выберите Тип Наказания**"
                                            "\n🔇|Mute"
                                            "\n💥|Ban"
                                            "\n🦵|Kick",
                                      colour=themeColor)
                await s.edit(embed=embed)
                await s.add_reaction('🔇')
                await s.add_reaction('💥')
                await s.add_reaction('🦵')

                def check(reaction, user):
                    return user == ctx.author and str(reaction.emoji) in '🔇💥🦵'

                try:
                    reaction, user = await client.wait_for('reaction_add', timeout=60.0, check=check)
                except asyncio.TimeoutError:
                    return await s.edit(embed=ember)

                if str(reaction.emoji) == '🔇':
                    embed = discord.Embed(
                        title=f"Теперь Выдается Мут за {warn} предупреждений(я) теперь выберите на сколько",
                        description="(д-дней, ч-часы, м-минут, с-секунды)\n"
                                    "Пример:\n"
                                    "1д", colour=themeColor)
                    await s.clear_reactions()
                    await s.edit(embed=embed)

                    def check(msg):
                        return msg.author == ctx.author and msg.channel == ctx.channel

                    itemName = await client.wait_for("message", check=check, timeout=60)
                    await itemName.delete()
                    itemName = itemName.content
                    try:
                        int(itemName[:-1])
                        if itemName[-1:] not in ['с', 'м', "ч", "д"]:
                            return await s.edit(
                                embed=discord.Embed(title="Вы не правильно ввели Время!", colour=themeColor))
                        WhatAction = f"1{itemName}"
                    except ValueError:
                        return await s.edit(
                            embed=discord.Embed(title="Вы не правильно ввели Время!", colour=themeColor))
                    embed = discord.Embed(title="Успешно Выбрано\n"
                                                "Теперь Выберите Нужно ли обнулять количество Предупреждений?\n(Если нет то прибавит 1 предупреждение Следует это учитывать)"
                                                "\n✔| Да"
                                                "\n❌| Нет", colour=themeColor)
                    await s.add_reaction('✔')
                    await s.add_reaction('❌')
                    await s.edit(embed=embed)

                    def check(reaction, user):
                        return user == ctx.author and str(reaction.emoji) in '✔❌'

                    try:
                        reaction, user = await client.wait_for('reaction_add', timeout=60.0, check=check)
                    except asyncio.TimeoutError:
                        return s.edit(embed=ember)

                    if str(reaction.emoji) == '✔':
                        delete = True
                    elif str(reaction.emoji) == '❌':
                        delete = False

                    Action = [warn, WhatAction, delete]
                    cursor.execute(f"INSERT INTO warnActions VALUES ({id},{Action[0]}, '{Action[1]}', {Action[2]})")
                    connection.commit()
                    embed = discord.Embed(title="Успешно Создано\n", colour=themeColor)
                    await s.clear_reactions()
                    return await s.edit(embed=embed)
                elif str(reaction.emoji) == '💥':
                    embed = discord.Embed(
                        title=f"Теперь Выдается Бан за {warn} предупреждений(я) теперь выберите на сколько",
                        description="(д-дней, ч-часы, м-минут, с-секунды)\n"
                                    "Пример:\n"
                                    "1д", colour=themeColor)
                    await s.clear_reactions()
                    await s.edit(embed=embed)

                    def check(msg):
                        return msg.author == ctx.author and msg.channel == ctx.channel

                    itemName = await client.wait_for("message", check=check, timeout=60)
                    await itemName.delete()
                    itemName = itemName.content
                    try:
                        int(itemName[:-1])
                        if itemName[-1:] not in ['с', 'м', "ч", "д"]:
                            return await s.edit(
                                embed=discord.Embed(title="Вы не правильно ввели Время!", colour=themeColor))
                        WhatAction = f"2{itemName}"
                    except ValueError:
                        return await s.edit(
                            embed=discord.Embed(title="Вы не правильно ввели Время!", colour=themeColor))
                    embed = discord.Embed(title="Успешно Выбрано\n"
                                                "Теперь Выберите Нужно ли обнулять количество Предупреждений?"
                                                "\n✔| Да"
                                                "\n❌| Нет", colour=themeColor)
                    await s.add_reaction('✔')
                    await s.add_reaction('❌')
                    await s.edit(embed=embed)

                    def check(reaction, user):
                        return user == ctx.author and str(reaction.emoji) in '✔❌'

                    try:
                        reaction, user = await client.wait_for('reaction_add', timeout=60.0, check=check)
                    except asyncio.TimeoutError:
                        return await s.edit(embed=ember)

                    if str(reaction.emoji) == '✔':
                        delete = True
                    elif str(reaction.emoji) == '❌':
                        delete = False

                    Action = [warn, WhatAction, delete]

                    cursor.execute(f"INSERT INTO warnActions VALUES ({id},{Action[0]}, '{Action[1]}', {Action[2]})")
                    connection.commit()
                    embed = discord.Embed(title="Успешно Создано\n", colour=themeColor)
                    await s.clear_reactions()
                    return await s.edit(embed=embed)
                elif str(reaction.emoji) == '🦵':
                    embed = discord.Embed(
                        title=f"Теперь Кикает за {warn} предупреждений(я) теперь выберите на сколько",
                        colour=themeColor)
                    await s.clear_reactions()
                    await s.edit(embed=embed)
                    embed = discord.Embed(title="Успешно Выбрано\n"
                                                "Теперь Выберите Нужно ли обнулять количество Предупреждений?"
                                                "\n✔| Да"
                                                "\n❌| Нет", colour=themeColor)
                    await s.add_reaction('✔')
                    await s.add_reaction('❌')

                    def check(reaction, user):
                        return user == ctx.author and str(reaction.emoji) in '✔❌'

                    await s.edit(embed=embed)
                    try:
                        reaction, user = await client.wait_for('reaction_add', timeout=60.0, check=check)
                    except asyncio.TimeoutError:
                        return await s.edit(embed=ember)

                    if str(reaction.emoji) == '✔':
                        delete = True
                    elif str(reaction.emoji) == '❌':
                        delete = False

                    Action = [warn, 3, delete]
                    cursor.execute(f"INSERT INTO warnActions VALUES ({id},{Action[0]}, '{Action[1]}', {Action[2]})")
                    connection.commit()
                    embed = discord.Embed(title="Успешно Создано\n", colour=themeColor)
                    await s.clear_reactions()
                    return await s.edit(embed=embed)
            elif str(reaction.emoji) == '🗑':
                pass
            elif str(reaction.emoji) == '📃':
                pass
        except asyncio.TimeoutError:
            await s.edit(embed=ember)

    @commands.has_permissions(administrator=True)
    @commands.command(name='ban_new_users')
    async def __ban_new_users(self, ctx: commands.Context):
        emb_user = discord.Embed(title='Выберите Пункт', color=themeColor)
        emb_user.add_field(name='🔘 | Выключить/Включить\n'
                                '🚪 | Назначить порог автобана(Дни)\n'
                                '📃 | Изменить причину Бана', inline=False)
        s = await ctx.channel.send(embed=emb_user)
        await s.add_reaction('🔘');
        await s.add_reaction('🚪')
        await s.add_reaction('📃')

        def check(reaction, user):
            return user == ctx.author and str(reaction.emoji) in ['📃', '🚪', '🔘']

        try:
            global ban_new_users
            reaction, user = await client.wait_for('reaction_add', timeout=60.0, check=check)
            if str(reaction.emoji) == '🔘':
                if banNewAccounts == True:
                    say = "Выключено"
                else:
                    say = "Включено"
                await s.clear_reactions()
                embed = discord.Embed(title=f"Успешно {say}", colour=themeColor)
                await s.edit(embed=embed)
                banNewAccounts = not (banNewAccounts)
                config["banNewAccounts"] = banNewAccounts
                with open("config.json", "w") as write:
                    json.dump(config, write, indent=4)
            elif str(reaction.emoji) == '🚪':
                global requiredDays
                emb = discord.Embed(title=f"Введите Порог Дней(До Дней будет автоматически банить)",
                                    colour=themeColor)
                await s.clear_reactions()
                await s.edit(embed=emb)

                def check(msg):
                    return msg.author == ctx.author and msg.channel == ctx.channel

                itemName = await client.wait_for("message", check=check, timeout=60)
                await itemName.delete()
                itemName = itemName.content
                try:
                    requiredDays = int(itemName)
                except ValueError:
                    return await s.edit(embed=discord.Embed(title="Вы ввели не число!", colour=themeColor))
                embed = discord.Embed(title="Успешно заданы дни", colour=themeColor)
                await s.edit(embed=embed)

                config["requiredDays"] = requiredDays
                with open("config.json", "w") as write:
                    json.dump(config, write, indent=4)
            if str(reaction.emoji) == '📃':
                await s.clear_reactions()
                global banDesc
                emb = discord.Embed(title=f"Введите Причину Бана", colour=themeColor)
                await s.clear_reactions()
                await s.edit(embed=emb)

                def check(msg):
                    return msg.author == ctx.author and msg.channel == ctx.channel

                itemName = await client.wait_for("message", check=check, timeout=60)
                await itemName.delete()
                banDesc = itemName.content
                await s.edit(embed=embed)

                config["banDesc"] = banDesc
                with open("config.json", "w") as write:
                    json.dump(config, write, indent=4)
        except asyncio.TimeoutError:
            ember = discord.Embed(title=f'Слишком долгий ответ напишите команду еще раз чтобы повторить',
                                  colour=themeColor)
            await ctx.channel.send(embed=ember)

    @commands.has_permissions(administrator=True)
    @commands.command(name='ignore_spam')
    async def __ignore_spam(self, ctx: commands.Context, channel_id=None):
        if channel_id == None:
            channel_id = ctx.channel.id
        cursor.execute(f"UPDATE channels SET antispam = NOT(antispam) WHERE id = {channel_id}")
        spam = cursor.execute(f"SELECT antispam FROM channels WHERE id = {channel_id}").fetchone()[0]
        channel = client.get_channel(channel_id)
        if spam == True:
            spam = "Включен"
        else:
            spam = "Выключен"
        embed = discord.Embed(title=f"Канал:`{channel.name}` \n обновлен теперь antispam:\n`{spam}`",
                              colour=themeColor)
        await ctx.channel.send(embed=embed)
        connection.commit()

    @commands.has_permissions(administrator=True)
    @commands.command(name='ignore_link')
    async def __ignore_link(self, ctx: commands.Context, channel_id=None):
        if channel_id == None:
            channel_id = ctx.channel.id
        cursor.execute(f"UPDATE channels SET antilink = NOT(antilink) WHERE id = {channel_id}")
        spam = cursor.execute(f"SELECT antilink FROM channels WHERE id = {channel_id}").fetchone()[0]
        channel = client.get_channel(channel_id)
        if spam == True:
            spam = "Включен"
        else:
            spam = "Выключен"
        embed = discord.Embed(title=f"Канал:`{channel.name}` \n обновлен теперь antilink:\n`{spam}`",
                              colour=themeColor)
        await ctx.channel.send(embed=embed)
        connection.commit()

    @commands.has_permissions(administrator=True)
    @commands.command(name='antispam_sensitivity')
    async def __antispam_sensitivity(self, ctx: commands.Context, messages=None, timer=None):
        global antispamMessages, antispamTimer
        try:
            antispamMessages = int(messages)
            antispamTimer = int(timer)
            config["antispamTimer"] = antispamTimer
            config["antispamMessages"] = antispamMessages
            with open("config.json", "w") as write:
                json.dump(config, write, indent=4)
            await ctx.send(embed=discord.Embed(
                title=f"Успешно Приняты значения\nСообщений до наказания: `{antispamMessages}`\nТаймер до сброса: `{antispamTimer}`",
                colour=themeColor))
        except ValueError:
            emb = discord.Embed(title='{ctx.author.mention}, вы не правильно ввели параметры!',
                                description=f'\n Пример:`{pr}antispam_sensitivity 10 3`', color=themeColor)

    # ----------------------------Moderation Master----------------------------------------

    @commands.has_permissions(administrator=True)
    @commands.command(name='mhelp')
    async def __mhelp(self, ctx: commands.Context):
        await ctx.message.add_reaction('✅')
        emb = discord.Embed(title="Помощь по Модераторским Командам!",
                            description=
                            f"\n> 1) `{pr}ban [@user] [Причина]` |Банит Участника"
                            f"\n> 2) `{pr}unban [юзер#1234]` |Убирает бан Участника"
                            f"\n> 3) `{pr}kick [@user] [Причина]` |Кикает Участника"
                            f"\n> 4) `{pr}warn [@user] [Причина]` |Дает предупреждение Участнику"
                            f"\n> 5) `{pr}mute [@user] [время:аргументы с:Секунды , м:Минуты , ч:Часов , д:Дней\пример: **30ч**] [Причина]` |Дает Мьют Участнику"
                            f"\n> 6) `{pr}mutes` |Дает Список замьюченных Участников"
                            f"\n> 7) `{pr}unmute_all` |Убирает Мьют со всех Участников"
                            f"\n> 8) `{pr}unmute [@user] [Причина]` |Дает Мьют Участнику"
                            f"\n> 9) `{pr}bans` |Дает Список Забаненных Участников"
                            f"\n> 10) `{pr}mute [@user] [Причина]` |Дает Мьют Участнику"
                            f"\n> 11) `{pr}tempban [@user] [время:аргументы с:Секунды , м:Минуты , ч:Часов , д:Дней\пример: **30ч**] [Причина]` |Дает временный бан Участнику"
                            f"\n> 12) `{pr}embedCreate` | Создать эмбед"
                            f"\n ----------ИВЕНТЫ----------"
                            f"\n> 1) `{pr}antilink` | Позволяет настроить глобальные настройки защиты от ссылок"
                            f"\n> 2) `{pr}antispam` | Позволяет настроить глобальные настройки защиты от спама"
                            f"\n> 3) `{pr}ignore_spam <ID канала>` | Игнорировать спам в канале"
                            f"\n> 4) `{pr}ignore_link <ID канала>` | Игнорировать ссылки в канале"
                            f"\n> 5) `{pr}antispam_sensitivity [сообщений максимум до сброса] [таймер сброса(в сек)]` | Редактирует чувствительность спама"
                            f"\n> 6) `{pr}auto_deny_perms` | Отбирать права у ботов(Вкл/Выкл)"
                            f"\n> 7) `{pr}ban_new_users` | Настройка банов новых аккаунтов"
                            f"\n> 10) `{pr}warn_actions` | Настроенные наказание за варны"

                            ,
                            colour=themeColor)
        emb.set_footer(text="[В этих скобках Обязательные параметры] <Необязательные Параметры>")
        await ctx.channel.send(embed=emb)

    @commands.command(name='ban')
    @commands.has_permissions(administrator=True)
    async def _ban(self, ctx: commands.Context, member: discord.Member = None, *, reason="Не Указано"):
        try:
            times_start = datetime.datetime.today()
            emb_user = discord.Embed(title='**Уведомление - Ban**', color=themeColor)
            emb_user.add_field(name='Нарушитель:', value=member.mention, inline=False)
            emb_user.add_field(name='**Выдал:**', value=ctx.author.mention, inline=False)
            emb_user.add_field(name='**Причина:**', value=reason, inline=False)
            emb_user.set_footer(text=f'Дата: {times_start.strftime("%Y-%m-%d, %H:%M:%S")}')
            if member is None:
                emb = discord.Embed(title='[ERROR] Ban', description=f'{ctx.author.mention}, Укажите пользователя!',
                                    color=themeColor)
                emb.add_field(name='Пример:', value=f'{pr}ban [@участник] [причина]', inline=False)
                emb.add_field(name='Пример 1:', value=f'{pr}ban @Xpeawey пример')
                return await ctx.channel.send(embed=emb)
            else:
                await ctx.channel.send(embed=emb_user)
                await member.send(embed=emb_user)
                await member.ban(reason=reason)
        except ValueError:
            await ctx.channel.send(
                embed=discord.Embed(title=f'{member.name} Нельзя забанить(Выше чем Бот)', colour=themeColor))

    @commands.command(name='kick')
    @commands.has_permissions(administrator=True)
    async def _kick(self, ctx: commands.Context, member: discord.Member, *, reason):
        try:
            await member.kick(reason=reason)
            await ctx.channel.send(embed=discord.Embed(title=f'{member.name} Был Кикнут',
                                                       description=f'Причина: {reason}', colour=themeColor))
        except Exception:
            await ctx.channel.send(
                discord.Embed(title=f'{member.name} Нельзя кикнуть(Выше чем Бот)', colour=themeColor))

    @commands.command(name="unban")
    @commands.has_permissions(administrator=True)
    async def _unban(self, ctx: commands.Context, *, member):
        banned_users = await ctx.guild.bans()
        member_name, member_discriminator = member.split("#")
        for ban_entry in banned_users:
            user = ban_entry.user
            if (user.name, user.discriminator) == (member_name, member_discriminator):
                await ctx.guild.unban(user)
                times_start = datetime.datetime.today()
                emb_user = discord.Embed(title='**Уведомление - Ban**', color=themeColor)
                emb_user.add_field(name='**Разбанил:**', value=ctx.author.mention, inline=False)
                emb_user.set_footer(text=f'Дата: {times_start.strftime("%Y-%m-%d, %H:%M:%S")}')
                await ctx.channel.send(embed=emb_user)
                return

    @commands.command(name='mute')
    @commands.has_permissions(administrator=True)
    async def _mute(self, ctx: commands.Context = None, member: discord.Member = None, amout: str = None, *,
                    reason=None, guild=None):
        times_start = datetime.datetime.today()
        if ctx == None:
            Author = client.user
        else:
            Author = ctx.author.mention
        if guild == None:
            guild = ctx.guild
        emb_user = discord.Embed(title='**Уведомление - Mute**', color=themeColor)
        emb_user.add_field(name='**Выдал:**', value=Author, inline=False)
        emb_user.add_field(name='**Причина:**', value=reason, inline=False)
        emb_user.add_field(name='**Длительность:**', value=amout, inline=False)
        emb_user.set_footer(text=f'Дата: {times_start.strftime("%Y-%m-%d, %H:%M:%S")}')

        emb_user_stop = discord.Embed(title='**Уведомление - Unmute**', color=themeColor)
        emb_user_stop.add_field(name='**Снял:**', value=Author, inline=False)
        emb_user_stop.set_footer(text=f'Дата: {times_start.strftime("%Y-%m-%d, %H:%M:%S")}')
        mute_role = discord.utils.get(ctx.guild.roles, name="Мут")
        if member is None:
            emb = discord.Embed(title='[ERROR] Mute', description=f'{Author}, Укажите пользователя!',
                                color=themeColor)
            emb.add_field(name='Пример:', value=f'{pr}mute [@участник] <время(с, м, ч, д)> [причина]', inline=False)
            emb.add_field(name='Пример 1:', value=f'{pr}mute @Xpeawey 1ч пример')
            emb.add_field(name='Время:', value=f'с - секунды\nм - минуты\nч - часы\nд - дни')
            return await ctx.channel.send(embed=emb)
        if amout == None:
            emb = discord.Embed(title=f'**System - Mute**', color=themeColor)
            emb.add_field(name='Выдал:', value=Author, inline=False)
            emb.add_field(name='Нарушитель:', value=member.mention, inline=False)
            emb.add_field(name='Причина:', value='Не указано', inline=False)
            emb.add_field(name='Длительность:', value='Не Указано')
            emb.set_footer(text=f'Дата: {times_start.strftime("%Y-%m-%d, %H:%M:%S")}')
            await member.add_roles(mute_role)
            await ctx.channel.send(embed=emb)
            await member.send(embed=emb_user)
        else:
            try:
                emb = discord.Embed(title='[ERROR] Mute', description=f'{Author}, вы не правильно ввели время!',
                                    color=themeColor)
                emb.add_field(name='Пример:', value=f'{pr}mute [@участник] <время> [причина]', inline=False)
                emb.add_field(name='Пример 1:', value=f'{pr}mute @Xpeawey 1ч пример')
                emb.add_field(name='Время:', value=f'с - секунды\nм - минуты\nч - часы\nд - дни')
                end_time = amout[-1:]

                if end_time not in ['с', 'м', 'ч', 'д']:
                    return await ctx.channel.send(embed=emb)
                time = int(amout[:-1])
            except ValueError:
                return await ctx.channel.send(embed=emb)
            if time <= 0:
                emb = discord.Embed(title='[ERROR] Mute', description=f'{Author}, Время не может быть меньше 1!',
                                    color=themeColor)
                emb.add_field(name='Пример:', value=f'{pr}mute [@участник] <время> [причина]', inline=False)
                emb.add_field(name='Пример 1:', value=f'{pr}mute @Xpeawey 1ч пример')
                emb.add_field(name='Время:', value=f'с - секунды\nм - минуты\nч - часы\nд - дни')

                await ctx.channel.send(embed=emb)
            else:
                if end_time == 'с':
                    if reason is None:
                        emb = discord.Embed(title=f'**System - Mute**', color=themeColor)
                        emb.add_field(name='Выдал:', value=Author, inline=False)
                        emb.add_field(name='Нарушитель:', value=member.mention, inline=False)

                        emb.add_field(name='Причина:', value='Не указано', inline=False)
                        emb.add_field(name='Длительность:', value='{} секунд'.format(time))
                        emb.set_footer(text=f'Дата: {times_start.strftime("%Y-%m-%d, %H:%M:%S")}')
                        await member.add_roles(mute_role)
                        if ctx != None:
                            await ctx.channel.send(embed=emb)
                        await member.send(embed=emb_user)
                        await asyncio.sleep(time)
                        if mute_role in member.roles:
                            await member.remove_roles(mute_role)
                            await member.send(embed=emb_user_stop)
                    else:
                        emb = discord.Embed(title=f'**System - Mute**', color=themeColor)
                        emb.add_field(name='Выдал:', value=Author, inline=False)
                        emb.add_field(name='Нарушитель:', value=member.mention, inline=False)
                        emb.add_field(name='Причина:', value=reason, inline=False)
                        emb.add_field(name='Длительность:', value='{} секунд'.format(time))
                        emb.set_footer(text=f'Дата: {times_start.strftime("%Y-%m-%d, %H:%M:%S")}')
                        await member.add_roles(mute_role)
                        if ctx != None:
                            await ctx.channel.send(embed=emb)
                        await member.send(embed=emb_user)
                        await asyncio.sleep(time)
                        if mute_role in member.roles:
                            await member.remove_roles(mute_role)
                            await member.send(embed=emb_user_stop)

                elif end_time == 'м':
                    if reason is None:
                        emb = discord.Embed(title=f'**System - Mute**', color=themeColor)
                        emb.add_field(name='Выдал:', value=Author, inline=False)
                        emb.add_field(name='Нарушитель:', value=member.mention, inline=False)

                        emb.add_field(name='Причина:', value='Не указано', inline=False)
                        emb.add_field(name='Длительность:', value='{} минут'.format(time))
                        emb.set_footer(text=f'Дата: {times_start.strftime("%Y-%m-%d, %H:%M:%S")}')
                        await member.add_roles(mute_role)
                        if ctx != None:
                            await ctx.channel.send(embed=emb)
                        await member.send(embed=emb_user)
                        await asyncio.sleep(time * 60)
                        if mute_role in member.roles:
                            await member.remove_roles(mute_role)
                            await member.send(embed=emb_user_stop)
                    else:
                        emb = discord.Embed(title=f'**System - Mute**', color=themeColor)
                        emb.add_field(name='Выдал:', value=Author, inline=False)
                        emb.add_field(name='Нарушитель:', value=member.mention, inline=False)

                        emb.add_field(name='Причина:', value=reason, inline=False)
                        emb.add_field(name='Длительность:', value='{} минут'.format(time))
                        emb.set_footer(text=f'Дата: {times_start.strftime("%Y-%m-%d, %H:%M:%S")}')
                        await member.add_roles(mute_role)
                        if ctx != None:
                            await ctx.channel.send(embed=emb)
                        await member.send(embed=emb_user)
                        await asyncio.sleep(time * 60)
                        if mute_role in member.roles:
                            await member.remove_roles(mute_role)
                            await member.send(embed=emb_user_stop)
                elif end_time == 'ч':
                    if reason is None:
                        emb = discord.Embed(title=f'**System - Mute**', color=themeColor)
                        emb.add_field(name='Выдал:', value=Author, inline=False)
                        emb.add_field(name='Нарушитель:', value=member.mention, inline=False)

                        emb.add_field(name='Причина:', value='Не указано', inline=False)
                        emb.add_field(name='Длительность:', value='{} час(a/ов)'.format(time))
                        emb.set_footer(text=f'Дата: {times_start.strftime("%Y-%m-%d, %H:%M:%S")}')
                        await member.add_roles(mute_role)
                        if ctx != None:
                            await ctx.channel.send(embed=emb)
                        await member.send(embed=emb_user)
                        await asyncio.sleep(time * 60 * 60)
                        if mute_role in member.roles:
                            await member.remove_roles(mute_role)
                            await member.send(embed=emb_user_stop)
                    else:
                        emb = discord.Embed(title=f'**System - Mute**', color=themeColor)
                        emb.add_field(name='**Выдал:**', value=Author, inline=False)
                        emb.add_field(name='**Нарушитель:**', value=member.mention, inline=False)

                        emb.add_field(name='**Причина:**', value=reason, inline=False)
                        emb.add_field(name='**Длительность:**', value='{} час(ов/а)'.format(time))
                        emb.set_footer(text=f'Дата: {times_start.strftime("%Y-%m-%d, %H:%M:%S")}')
                        await member.add_roles(mute_role)
                        if ctx != None:
                            await ctx.channel.send(embed=emb)
                        await member.send(embed=emb_user)
                        await asyncio.sleep(time * 60 * 60)
                        if mute_role in member.roles:
                            await member.remove_roles(mute_role)
                            await member.send(embed=emb_user_stop)
                elif end_time == 'д':
                    if reason is None:
                        emb = discord.Embed(title=f'**System - Mute**', color=themeColor)
                        emb.add_field(name='**Выдал:**', value=Author, inline=False)
                        emb.add_field(name='**Нарушитель:**', value=member.mention, inline=False)
                        emb.add_field(name='**Причина:**', value='Не указано', inline=False)
                        emb.add_field(name='**Длительность:**', value='{} день(ей)'.format(time))
                        emb.set_footer(text=f'Дата: {times_start.strftime("%Y-%m-%d, %H:%M:%S")}')

                        await member.send(embed=emb_user)
                        await member.add_roles(mute_role)
                        if ctx != None:
                            await ctx.channel.send(embed=emb)
                        await member.send(embed=emb_user)
                        await asyncio.sleep(time * 60 * 60 * 24)
                        await member.remove_roles(mute_role)
                        await member.send(embed=emb_user_stop)
                    else:
                        emb = discord.Embed(title=f'**System - Mute**', color=themeColor)
                        emb.add_field(name='**Выдал:**', value=Author, inline=False)
                        emb.add_field(name='**Нарушитель:**', value=member.mention, inline=False)
                        emb.add_field(name='**Причина:**', value=reason, inline=False)
                        emb.add_field(name='**Длительность:**', value='{} день(ей)'.format(time), inline=False)
                        emb.set_footer(text=f'Дата: {times_start.strftime("%Y-%m-%d, %H:%M:%S")}')
                        await member.add_roles(mute_role)
                        if ctx != None:
                            await ctx.channel.send(embed=emb)
                        await member.send(embed=emb_user)
                        await asyncio.sleep(time * 60 * 60 * 24)
                        if mute_role in member.roles:
                            await member.remove_roles(mute_role)
                            await member.send(embed=emb_user_stop)

    @commands.command(name='tempban')
    @commands.has_permissions(administrator=True)
    async def _tempban(self, ctx: commands.Context = None, member: discord.Member = None, amout: str = None, *,
                       reason=None):
        if ctx == None:
            Author = client.user
        else:
            Author = ctx.author.mention
        times_start = datetime.datetime.today()
        emb_user = discord.Embed(title='**Уведомление - Ban**', color=themeColor)
        emb_user.add_field(name='**Выдал:**', value=Author, inline=False)
        emb_user.add_field(name='**Причина:**', value=reason, inline=False)
        emb_user.add_field(name='**Длительность:**', value=amout, inline=False)
        emb_user.set_footer(text=f'Дата: {times_start.strftime("%Y-%m-%d, %H:%M:%S")}')
        if member is None:
            emb = discord.Embed(title='[ERROR] Ban', description=f'{Author}, Укажите пользователя!',
                                color=themeColor)
            emb.add_field(name='Пример:', value=f'{pr}ban [@участник] <время(с, м, ч, д)> [причина]', inline=False)
            emb.add_field(name='Пример 1:', value=f'{pr}ban @Xpeawey 1ч пример')
            emb.add_field(name='Время:', value=f'с - секунды\nм - минуты\nч - часы\nд - дни')
            return await ctx.channel.send(embed=emb)
        if amout == None:
            emb = discord.Embed(title=f'**System - Ban**', color=themeColor)
            emb.add_field(name='Выдал:', value=Author, inline=False)
            emb.add_field(name='Нарушитель:', value=member.mention, inline=False)
            emb.add_field(name='Причина:', value='Не указано', inline=False)
            emb.add_field(name='Длительность:', value='Не Указано')
            emb.set_footer(text=f'Дата: {times_start.strftime("%Y-%m-%d, %H:%M:%S")}')
            await member.ban(reason=reason)
            await ctx.channel.send(embed=emb)
            await member.send(embed=emb_user)
        else:
            try:
                emb = discord.Embed(title='[ERROR] Ban', description=f'{Author}, вы не правильно ввели время!',
                                    color=themeColor)
                emb.add_field(name='Пример:', value=f'{pr}ban [@участник] <время> [причина]', inline=False)
                emb.add_field(name='Пример 1:', value=f'{pr}ban @Xpeawey 1ч пример')
                emb.add_field(name='Время:', value=f'с - секунды\nм - минуты\nч - часы\nд - дни')
                end_time = amout[-1:]

                if end_time not in ['с', 'м', 'ч', 'д']:
                    return await ctx.channel.send(embed=emb)
                time = int(amout[:-1])
            except ValueError:
                return await ctx.channel.send(embed=emb)
            if time <= 0:
                emb = discord.Embed(title='[ERROR] Ban', description=f'{Author}, Время не может быть меньше 1!',
                                    color=themeColor)
                emb.add_field(name='Пример:', value=f'{pr}ban [@участник] <время> [причина]', inline=False)
                emb.add_field(name='Пример 1:', value=f'{pr}ban @Xpeawey 1ч пример')
                emb.add_field(name='Время:', value=f'с - секунды\nм - минуты\nч - часы\nд - дни')

                await ctx.channel.send(embed=emb)
            else:
                if end_time == 'с':
                    if reason is None:
                        emb = discord.Embed(title=f'**System - Ban**', color=themeColor)
                        emb.add_field(name='Выдал:', value=Author, inline=False)
                        emb.add_field(name='Нарушитель:', value=member.mention, inline=False)

                        emb.add_field(name='Причина:', value='Не указано', inline=False)
                        emb.add_field(name='Длительность:', value='{} секунд'.format(time))
                        emb.set_footer(text=f'Дата: {times_start.strftime("%Y-%m-%d, %H:%M:%S")}')
                        if ctx == None:
                            await ctx.channel.send(embed=emb)

                        await member.send(embed=emb_user)
                        await member.ban(reason=reason)
                        await asyncio.sleep(time)
                        await member.unban(reason=reason)

                    else:
                        emb = discord.Embed(title=f'**System - Ban**', color=themeColor)
                        emb.add_field(name='Выдал:', value=Author, inline=False)
                        emb.add_field(name='Нарушитель:', value=member.mention, inline=False)

                        emb.add_field(name='Причина:', value=reason, inline=False)
                        emb.add_field(name='Длительность:', value='{} секунд'.format(time))
                        emb.set_footer(text=f'Дата: {times_start.strftime("%Y-%m-%d, %H:%M:%S")}')
                        if ctx == None:
                            await ctx.channel.send(embed=emb)
                        await member.send(embed=emb_user)
                        await member.ban(reason=reason)
                        await asyncio.sleep(time)
                        await member.unban(reason=reason)

                elif end_time == 'м':
                    if reason is None:
                        emb = discord.Embed(title=f'**System - Ban**', color=themeColor)
                        emb.add_field(name='Выдал:', value=Author, inline=False)
                        emb.add_field(name='Нарушитель:', value=member.mention, inline=False)

                        emb.add_field(name='Причина:', value='Не указано', inline=False)
                        emb.add_field(name='Длительность:', value='{} минут'.format(time))
                        emb.set_footer(text=f'Дата: {times_start.strftime("%Y-%m-%d, %H:%M:%S")}')
                        if ctx == None:
                            await ctx.channel.send(embed=emb)
                        await member.send(embed=emb_user)
                        await member.ban(reason=reason)
                        await asyncio.sleep(time * 60)
                        await member.unban(reason=reason)

                    else:
                        emb = discord.Embed(title=f'**System - Ban**', color=themeColor)
                        emb.add_field(name='Выдал:', value=Author, inline=False)
                        emb.add_field(name='Нарушитель:', value=member.mention, inline=False)

                        emb.add_field(name='Причина:', value=reason, inline=False)
                        emb.add_field(name='Длительность:', value='{} минут'.format(time))
                        emb.set_footer(text=f'Дата: {times_start.strftime("%Y-%m-%d, %H:%M:%S")}')
                        if ctx == None:
                            await ctx.channel.send(embed=emb)
                        await member.send(embed=emb_user)
                        await member.ban(reason=reason)
                        await asyncio.sleep(time * 60)
                        await member.unban(reason=reason)

                elif end_time == 'ч':
                    if reason is None:
                        emb = discord.Embed(title=f'**System - Ban**', color=themeColor)
                        emb.add_field(name='Выдал:', value=Author, inline=False)
                        emb.add_field(name='Нарушитель:', value=member.mention, inline=False)

                        emb.add_field(name='Причина:', value='Не указано', inline=False)
                        emb.add_field(name='Длительность:', value='{} час(a/ов)'.format(time))
                        emb.set_footer(text=f'Дата: {times_start.strftime("%Y-%m-%d, %H:%M:%S")}')
                        if ctx == None:
                            await ctx.channel.send(embed=emb)
                        await member.send(embed=emb_user)
                        await member.ban(reason=reason)
                        await asyncio.sleep(time * 60 * 60)
                        await member.unban(reason=reason)

                    else:
                        emb = discord.Embed(title=f'**System - Ban**', color=themeColor)
                        emb.add_field(name='**Выдал:**', value=Author, inline=False)
                        emb.add_field(name='**Нарушитель:**', value=member.mention, inline=False)

                        emb.add_field(name='**Причина:**', value=reason, inline=False)
                        emb.add_field(name='**Длительность:**', value='{} час(а/ов)'.format(time))
                        emb.set_footer(text=f'Дата: {times_start.strftime("%Y-%m-%d, %H:%M:%S")}')
                        if ctx == None:
                            await ctx.channel.send(embed=emb)
                        await member.send(embed=emb_user)
                        await member.ban(reason=reason)
                        await asyncio.sleep(time * 60 * 60)
                        await member.unban(reason=reason)

                elif end_time == 'д':
                    if reason is None:
                        emb = discord.Embed(title=f'**System - Ban**', color=themeColor)
                        emb.add_field(name='**Выдал:**', value=Author, inline=False)
                        emb.add_field(name='**Нарушитель:**', value=member.mention, inline=False)
                        emb.add_field(name='**Причина:**', value='Не указано', inline=False)
                        emb.add_field(name='**Длительность:**', value='{} день(ей)'.format(time))
                        emb.set_footer(text=f'Дата: {times_start.strftime("%Y-%m-%d, %H:%M:%S")}')

                        await member.send(embed=emb_user)
                        if ctx == None:
                            await ctx.channel.send(embed=emb)
                        await member.send(embed=emb_user)
                        await member.ban(reason=reason)
                        await asyncio.sleep(time * 60 * 60 * 24)
                        await member.unban(reason=reason)

                    else:
                        emb = discord.Embed(title=f'**System - Ban**', color=themeColor)
                        emb.add_field(name='**Выдал:**', value=Author, inline=False)
                        emb.add_field(name='**Нарушитель:**', value=member.mention, inline=False)
                        emb.add_field(name='**Причина:**', value=reason, inline=False)
                        emb.add_field(name='**Длительность:**', value='{} день(ей)'.format(time), inline=False)
                        emb.set_footer(text=f'Дата: {times_start.strftime("%Y-%m-%d, %H:%M:%S")}')
                        if ctx == None:
                            await ctx.channel.send(embed=emb)
                        await member.send(embed=emb_user)
                        await member.ban(reason=reason)
                        await asyncio.sleep(time * 60 * 60 * 24)
                        await member.unban(reason=reason)

    @commands.command(name='mutes')
    @commands.has_permissions(administrator=True)
    async def _mutes(self, ctx: commands.Context):
        desc = ""
        for member in ctx.guild.members:
            mute_role = discord.utils.get(ctx.message.guild.roles, name="Мут")
            if mute_role in member.roles:
                desc = f"{desc}\n{member}"
        emb = discord.Embed(title='Список замьюченных пользователей:', description=desc, colour=themeColor)
        await ctx.channel.send(embed=emb)

    @commands.command(name='bans')
    @commands.has_permissions(administrator=True)
    async def _bans(self, ctx: commands.Context):
        desc = ""
        bans = await ctx.guild.bans()
        for member in bans:
            member = f"{member.user.name}#{member.user.discriminator}"
            desc = f"{desc}\n{member}"
        emb = discord.Embed(title='Список забанненых пользователей:', description=desc, colour=themeColor)
        await ctx.channel.send(embed=emb)

    @commands.command(name='unmute')
    @commands.has_permissions(administrator=True)
    async def _unmute(self, ctx: commands.Context, member: discord.Member = None, *, reason="Не указана"):
        times_start = datetime.datetime.today()
        emb_user = discord.Embed(title='**Уведомление - Unmute**', color=themeColor)
        emb_user.add_field(name='**Выдал:**', value=ctx.author.mention, inline=False)
        emb_user.add_field(name='**Причина:**', value=reason, inline=False)
        emb_user.set_footer(text=f'Дата: {times_start.strftime("%Y-%m-%d, %H:%M:%S")}')
        if member is None:
            emb = discord.Embed(title='[ERROR] Unmute', description=f'{ctx.author.mention}, Укажите пользователя!',
                                color=themeColor)
            emb.add_field(name='Пример:', value=f'{pr}unmute [@участник] <причина>', inline=False)
            emb.add_field(name='Пример 1:', value=f'{pr}unmute @Xpeawey пример')
            return await ctx.channel.send(embed=emb)
        else:
            await ctx.channel.send(embed=emb_user)

            await member.send(embed=emb_user)
            mute_role = discord.utils.get(ctx.guild.roles, name="Мут")
            await member.remove_roles(mute_role)
            await member.send(embed=emb_user)

    @commands.command(name='warn')
    @commands.has_permissions(administrator=True)
    async def _warn(self, ctx: commands.Context, member: discord.Member = None, *, reason="Не указана", bot=False):
        times_start = datetime.datetime.today()
        if member is None:
            emb = discord.Embed(title='[ERROR] Unmute', description=f'{ctx.author.mention}, Укажите пользователя!',
                                color=themeColor)
            emb.add_field(name='Пример:', value=f'{pr}unmute [@участник] <причина>', inline=False)
            emb.add_field(name='Пример 1:', value=f'{pr}unmute @Xpeawey пример')
            return await ctx.channel.send(embed=emb)
        else:
            cursor.execute(f"UPDATE warns SET warns = warns + 1 WHERE user = {member.id}")
            warns = cursor.execute(f"SELECT warns FROM warns WHERE user = {member.id}").fetchone()[0]
            emb_user = discord.Embed(title=f'**Выдано Предупреждение**\n Теперь предупреждений: `{warns}`',
                                     color=themeColor)
            emb_user.add_field(name='Нарушитель:', value=member.mention, inline=False)
            emb_user.add_field(name='**Выдал:**', value=ctx.author.mention, inline=False)
            emb_user.add_field(name='**Причина:**', value=reason, inline=False)
            emb_user.set_footer(text=f'Дата: {times_start.strftime("%Y-%m-%d, %H:%M:%S")}')
            if bot == True:
                await ctx.channel.send(embed=emb_user)
            else:
                await ctx.channel.send(embed=emb_user)
            await member.send(embed=emb_user)
            connection.commit()

    @commands.command(name='unmute_all')
    @commands.has_permissions(administrator=True)
    async def _unmuteAll(self, ctx: commands.Context, *, reason="Не указана"):
        times_start = datetime.datetime.today()
        emb_user = discord.Embed(title='**Уведомление - Unmute Всех**', color=themeColor)
        emb_user.add_field(name='**Выдал:**', value=ctx.author.mention, inline=False)
        emb_user.add_field(name='**Причина:**', value=reason, inline=False)
        emb_user.set_footer(text=f'Дата: {times_start.strftime("%Y-%m-%d, %H:%M:%S")}')
        for member in ctx.guild.members:
            mute_role = discord.utils.get(ctx.guild.roles, name="Мут")
            if mute_role in member.roles:
                try:
                    await member.remove_roles(mute_role)
                    await member.send(embed=emb_user)
                except:
                    pass
        await ctx.channel.send(embed=emb_user)


    @commands.command(name='auto_deny_perms')
    @commands.has_permissions(administrator=True)
    async def _auto_deny_perms(self, ctx: commands.Context):
        global autoDenyBotRoles
        if autoDenyBotRoles == True:
            of="Выключено"
        else:
            of="Включено"
        embed=discord.Embed(title=f"Успешно {of}", color=themeColor)
        await ctx.send(embed=embed)
        autoDenyBotRoles=not(autoDenyBotRoles)
        config["autoDenyBotRoles"] = autoDenyBotRoles
        with open("config.json", "w") as write:
            json.dump(config, write, indent=4)
    # ----------------------------------user----------------------------------------
    def __init__(self, bot: commands.Bot):
        self.bot = bot
        self.voice_states = {}

    def get_voice_state(self, ctx: commands.Context):
        state = self.voice_states.get(ctx.guild.id)
        if not state:
            state = VoiceState(self.bot, ctx)
            self.voice_states[ctx.guild.id] = state

        return state

    def cog_unload(self):
        for state in self.voice_states.values():
            self.bot.loop.create_task(state.stop())

    def cog_check(self, ctx: commands.Context):
        if not ctx.guild:
            raise commands.NoPrivateMessage('Эта команда не используется в ЛС (Личные сообщения)')

        return True

    async def cog_before_invoke(self, ctx: commands.Context):
        ctx.voice_state = self.get_voice_state(ctx)

    async def cog_command_error(self, ctx: commands.Context, error: commands.CommandError):
        await ctx.send('Произошла ошибка: {}'.format(str(error)))
#-----------------------------------------------------------------------------






#-----------------------------------------------------------------------------
    @commands.command(name='help')
    async def __help(self, ctx: commands.Context):
        await ctx.message.add_reaction('✅')
        emb = discord.Embed(title="Помощь по Командам!",
                            description=
                            f"\n> 1) `{pr}join` |Присоединяет Бота к каналу в котором вы сидите"
                            f"\n> 2) (Админ)`{pr}summon <Канал>` |Присоединяет Бота к каналу в котором вы сидите или названному"
                            f"\n> 3) (Админ)`{pr}leave` |Отключает бота с канала + Очищает треки в очереди"
                            f"\n> 4) `{pr}volume` |Меняет Громкость Музыки в канале(От 0 до 100)"
                            f"\n> 5) `{pr}now` |Показывает Трек идущий сейчас"
                            f"\n> 6) `{pr}pause` |Приостанавливает Трек идущий сейчас"
                            f"\n> 7) `{pr}resume` |Возобновляет Трек идущий сейчас"
                            f"\n> 8) (Админ)`{pr}stop` |Останавливает треки и удаляет очередь"
                            f"\n> 9) `{pr}skip` |Пропускает трек"
                            f"\n> 10) `{pr}queue` |Показывает очередь треков"
                            f"\n> 11) `{pr}shuffle` |Перемешивает треки в очереди"
                            f"\n> 12) (Админ)`{pr}remove <по очереди номер>` | Удаляет трек по очереди"
                            f"\n> 12) `{pr}loop` | Повторять трек"
                            f"\n> 13) `{pr}play <название или ссылка на музыку>` | Запускает Музыку"
                            ,
                            colour=themeColor)
        emb.set_footer(text="[В этих скобках Обязательные параметры] <Необязательные Параметры>")
        await ctx.channel.send(embed=emb)

    @commands.command(name='join', invoke_without_subcommand=True)
    async def _join(self, ctx: commands.Context):
        """Joins a voice channel."""

        destination = ctx.author.voice.channel
        if ctx.voice_state.voice:
            await ctx.voice_state.voice.move_to(destination)
            return

        ctx.voice_state.voice = await destination.connect()

    @commands.command(name='summon')
    @commands.has_permissions(administrator=True)
    async def _summon(self, ctx: commands.Context, *, channel: discord.VoiceChannel = None):
        """Summons the bot to a voice channel.
        If no channel was specified, it joins your channel.
        """

        if not channel and not ctx.author.voice:
            raise VoiceError('Вы не подключены к голосовому каналу. И не указали куда подключаться.')

        destination = channel or ctx.author.voice.channel
        if ctx.voice_state.voice:
            await ctx.voice_state.voice.move_to(destination)
            return

        ctx.voice_state.voice = await destination.connect()

    @commands.command(name='leave', aliases=['disconnect'])
    @commands.has_permissions(administrator=True)
    async def _leave(self, ctx: commands.Context):
        """Clears the queue and leaves the voice channel."""

        if not ctx.voice_state.voice:
            return await ctx.send('Бот не подключен к каналу')

        await ctx.voice_state.stop()
        del self.voice_states[ctx.guild.id]

    @commands.command(name='volume')
    async def _volume(self, ctx: commands.Context, *, volume: int):
        """Sets the volume of the player."""

        if not ctx.voice_state.is_playing:
            return await ctx.send('Нельзя настройть громкость(Вы не включили музыку).')

        if 0 > volume > 100:
            return await ctx.send('Громкость должна быть не ниже 0 и не выше 100')

        ctx.voice_state.volume = volume / 100
        await ctx.send('Громкость изменена на {}%'.format(volume))

    @commands.command(name='now', aliases=['current', 'playing'])
    async def _now(self, ctx: commands.Context):
        """Displays the currently playing song."""

        await ctx.send(embed=ctx.voice_state.current.create_embed())

    @commands.command(name='pause')
    @commands.has_permissions(administrator=True)
    async def _pause(self, ctx: commands.Context):
        """Pauses the currently playing song."""

        if ctx.voice_state.voice.is_playing():
            ctx.voice_state.voice.pause()
            await ctx.message.add_reaction('⏯')

    @commands.command(name='resume')
    @commands.has_permissions(administrator=True)
    async def _resume(self, ctx: commands.Context):
        """Resumes a currently paused song."""

        if not ctx.voice_state.is_playing and ctx.voice_state.voice.is_paused():
            ctx.voice_state.voice.resume()
            await ctx.message.add_reaction('⏯')

    @commands.command(name='stop')
    @commands.has_permissions(administrator=True)
    async def _stop(self, ctx: commands.Context):
        """Stops playing song and clears the queue."""

        ctx.voice_state.songs.clear()

        if not ctx.voice_state.is_playing:
            ctx.voice_state.voice.stop()
            await ctx.message.add_reaction('⏹')

    @commands.command(name='skip')
    async def _skip(self, ctx: commands.Context):
        """Vote to skip a song. The requester can automatically skip.
        3 skip votes are needed for the song to be skipped.
        """

        if not ctx.voice_state.is_playing:
            return await ctx.send('Сейчас музыка не играет,зачем её пропускать? Можете включить.')

        voter = ctx.message.author
        if voter == ctx.voice_state.current.requester:
            await ctx.message.add_reaction('⏭')
            ctx.voice_state.skip()

        elif voter.id not in ctx.voice_state.skip_votes:
            ctx.voice_state.skip_votes.add(voter.id)
            total_votes = len(ctx.voice_state.skip_votes)

            if total_votes >= 3:
                await ctx.message.add_reaction('⏭')
                ctx.voice_state.skip()
            else:
                await ctx.send('Голосование за пропуск добавлено. Проголосовали: **{}/3**'.format(total_votes))

        else:
            await ctx.send('Вы уже голосовали за пропуск этого трека.')

    @commands.command(name='queue')
    async def _queue(self, ctx: commands.Context, *, page: int = 1):
        """Shows the player's queue.
        You can optionally specify the page to show. Each page contains 10 elements.
        """

        if len(ctx.voice_state.songs) == 0:
            return await ctx.send('В очереди нет треков.')

        items_per_page = 10
        pages = math.ceil(len(ctx.voice_state.songs) / items_per_page)

        start = (page - 1) * items_per_page
        end = start + items_per_page

        queue = ''
        for i, song in enumerate(ctx.voice_state.songs[start:end], start=start):
            queue += '`{0}.` [**{1.source.title}**]({1.source.url})\n'.format(i + 1, song)

        embed = (discord.Embed(description='**{} tracks:**\n\n{}'.format(len(ctx.voice_state.songs), queue))
                 .set_footer(text='Viewing page {}/{}'.format(page, pages)))
        await ctx.send(embed=embed)

    @commands.command(name='shuffle')
    async def _shuffle(self, ctx: commands.Context):
        """Shuffles the queue."""

        if len(ctx.voice_state.songs) == 0:
            return await ctx.send('В очереди нет треков.')

        ctx.voice_state.songs.shuffle()
        await ctx.message.add_reaction('✅')

    @commands.has_permissions(administrator=True)
    @commands.command(name='remove')
    async def _remove(self, ctx: commands.Context, index: int):
        """Removes a song from the queue at a given index."""

        if len(ctx.voice_state.songs) == 0:
            return await ctx.send('В очереди нет треков.')

        ctx.voice_state.songs.remove(index - 1)
        await ctx.message.add_reaction('✅')

    @commands.command(name='loop')
    async def _loop(self, ctx: commands.Context):
        """Loops the currently playing song.
        Invoke this command again to unloop the song.
        """

        if not ctx.voice_state.is_playing:
            return await ctx.send('Ничего не играет в данный момент.')

        # Inverse boolean value to loop and unloop.
        ctx.voice_state.loop = not ctx.voice_state.loop
        await ctx.message.add_reaction('✅')

    @commands.command(name='play')
    async def _play(self, ctx: commands.Context, *, search: str):
        """Plays a song.
        If there are songs in the queue, this will be queued until the
        other songs finished playing.
        This command automatically searches from various sites if no URL is provided.
        A list of these sites can be found here: https://rg3.github.io/youtube-dl/supportedsites.html
        """

        if not ctx.voice_state.voice:
            await ctx.invoke(self._join)

        async with ctx.typing():
            try:
                source = await YTDLSource.create_source(ctx, search, loop=self.bot.loop)
            except YTDLError as e:
                await ctx.send('Произошла ошибка при обработке этого запроса: {}'.format(str(e)))
            else:
                song = Song(source)

                await ctx.voice_state.songs.put(song)
                await ctx.send('Успешно добавлено {}'.format(str(source)))

    @_join.before_invoke
    @_play.before_invoke
    async def ensure_voice_state(self, ctx: commands.Context):
        if not ctx.author.voice or not ctx.author.voice.channel:
            raise commands.CommandError('Сначала подключитесь к голосовому каналу.')

        if ctx.voice_client:
            if ctx.voice_client.channel != ctx.author.voice.channel:
                raise commands.CommandError('Бот уже подключен с голосовому каналу.')

intents = discord.Intents.all()
client = commands.Bot(command_prefix=f'{pr}', intents=intents)
client.remove_command('help')
client.add_cog(Music(client))




@client.event
async def on_ready():
    cursor.execute("""CREATE TABLE IF NOT EXISTS warns (user INT, warns INT)""")  # warns
    cursor.execute("""CREATE TABLE IF NOT EXISTS channels (id INT, antispam BOOLEAN, antilink BOOLEAN)""")
    cursor.execute(
        """CREATE TABLE IF NOT EXISTS warnActions (id INT, warn INT, Action TEXT, DeleteWarns BOOLEAN)""")
    for guild in client.guilds:  # Перебор всех на сервере и занос в БД
        mute_role = discord.utils.get(guild.roles, name="Мут")
        if mute_role == None:
            await guild.create_role(name="Мут")
            mute_role = discord.utils.get(guild.roles, name="Мут")
        for channel in guild.text_channels:
            if cursor.execute(f"SELECT id FROM channels WHERE id = {channel.id}").fetchone() is None:
                cursor.execute(f"INSERT INTO channels VALUES ({channel.id}, True, True)")
            await channel.set_permissions(mute_role, send_messages=False)

        for channel in guild.voice_channels:
            await channel.set_permissions(mute_role, connect=False)
        for member in guild.members:
            if cursor.execute(f"SELECT user FROM warns WHERE user = {member.id}").fetchone() is None:
                cursor.execute(f"INSERT INTO warns VALUES ( {member.id}, 0)")
    connection.commit()
    print("______Бот Запущен!______")


@client.event
async def on_member_join(member):
    if member.bot == True:
        if autoDenyBotRoles == True:
            for role in member.roles:
                if role.is_bot_managed() == True:
                    permissions = discord.Permissions()
                    permissions.update(kick_members=False, ban_members=False, request_to_speak=False, use_slash_commands=False, manage_emojis=False, manage_webhooks=False, manage_permissions=False, manage_roles=False, manage_nicknames=False, change_nickname=False, use_voice_activation=False, move_members=False, deafen_members=False, mute_members=False, speak=False, connect=False, view_guild_insights=False, use_external_emojis=False, external_emojis=False, mention_everyone=False, read_message_history=False, attach_files=False, embed_links=False, manage_messages=False, send_tts_messages=False, send_messages=False, view_channel=False, read_messages=False, stream=False, priority_speaker=False, view_audit_log=False, add_reactions=False, manage_guild=False, manage_channels=False, administrator=False, create_instant_invite=False)
                    await role.edit(reason=None, permissions=permissions)
    else:
        from_time = datetime.datetime.today() - member.created_at
        if from_time.days < requiredDays and banNewAccounts == True:
            await member.ban(reason=f"{banDesc}")
        else:
            if cursor.execute(f"SELECT user FROM warns WHERE user = {member.id}").fetchone() is None:
                cursor.execute(f"INSERT INTO warns VALUES ({member.id}, 0 )")
            connection.commit()


@client.event
async def on_guild_channel_create(channel):
    mute_role = discord.utils.get(channel.guild.roles, name="Мут")
    await channel.set_permissions(mute_role, connect=False)
    await channel.set_permissions(mute_role, send_messages=False)

@client.event
async def on_command_error(ctx, error):
    if isinstance(error, MissingPermissions):
        await ctx.channel.send(embed=discord.Embed(title="Недостаточно Прав", colour=themeColor))
    else:
        raise error

@client.event
async def on_message(ctx):
    global cooldown
    if not ctx.author.bot and not (ctx.author.guild_permissions.administrator):
        try:
            if antispam == True and \
                    cursor.execute(f"SELECT antispam FROM channels WHERE id = {ctx.channel.id}").fetchone()[
                        0] == True:
                if cooldown[ctx.author.id] < antispamMessages:
                    cooldown[ctx.author.id] += 1
                else:
                    if antispamPunish == 1:
                        WarningUser = ctx.author
                        ctx.author = client.user
                        await Music._warn(None, ctx, WarningUser, reason="СПАМ", bot=True)
                        await Music.warn_action(None, ctx)
                        return await ctx.delete()
                    elif type(antispamPunish) == list:
                        WarningUser = ctx.author
                        ctx.author = client.user
                        await Music._mute(None, ctx, WarningUser, antispamPunish[1], reason="СПАМ", )
                        return await ctx.delete()
                    elif antispamPunish == 3:
                        WarningUser = ctx.author
                        ctx.author = client.user
                        await Music._ban(None, ctx, WarningUser, reason="СПАМ")
        except KeyError:
            cooldown[ctx.author.id] = 1
        if antilink == True:
            if 'https://' in ctx.content:
                if antilinkPunish == 1:
                    WarningUser = ctx.author
                    ctx.author = client.user
                    await Music._warn(None, ctx, WarningUser, reason="ССЫЛКИ", bot=True)
                    await Music.warn_action(None,ctx)
                    return await ctx.delete()
                elif type(antilinkPunish) == list:
                    WarningUser = ctx.author
                    ctx.author = client.user
                    await Music._mute(None, ctx, WarningUser, antilinkPunish[1], reason="ССЫЛКИ", )
                    return await ctx.delete()
                elif antilinkPunish == 3:
                    WarningUser = ctx.author
                    ctx.author = client.user
                    await Music._ban(None, ctx, WarningUser, reason="ССЫЛКИ")
                return
    await client.process_commands(ctx)

client.run(TOKEN, bot=True)
