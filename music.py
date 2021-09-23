import discord
from discord.ext import commands
import youtube_dl
from youtube_dl import YoutubeDL
import asyncio
import pafy

class MusicPlayer(commands.Cog):
  def __init__(self,bot):
    self.bot=bot
    self.song_queue={}

    self.setup()
  
  def setup(self):
    for guild in self.bot.guilds:
      self.song_queue[guild.id]=[]

  async def check_queue(self,ctx):
    if len(self.song_queue[ctx.guild.id]) > 0:
      k=self.song_queue[ctx.guild.id]
      m=k.pop(0)
      await self.play_song(ctx,m)

  async def search_song(self,amount,song,get_url=False):

    info = await self.bot.loop.run_in_executor(None, lambda: youtube_dl.YoutubeDL({"format":"bestaudio","quiet": True, "noplaylist": True}).extract_info(f"ytsearch{amount}:{song}",download=False,ie_key="YoutubeSearch"))

    if len(info["entries"]) == 0: 
      return None
    
    return [entry["webpage_url"] for entry in info["entries"]] if get_url else info


  async def play_song(self,ctx,song):

    url=pafy.new(song).getbestaudio().url
    FFMPEG_OPTIONS = {
        'before_options': '-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5', 'options': '-vn'}
    ctx.voice_client.play(discord.PCMVolumeTransformer(discord.FFmpegPCMAudio(url,**FFMPEG_OPTIONS)),after=lambda error:self.bot.loop.create_task(self.check_queue(ctx)))

    ctx.voice_client.source.volume=0.5




  @commands.command()

  async def join(self,ctx):
    if ctx.author.voice is None:
      return await ctx.send("You are not connected to any voice channels")
    
    if ctx.voice_client is not None:
      await ctx.voice_client.disconnect()
    
    await ctx.author.voice.channel.connect()
  
  @commands.command()
  async def leave(self,ctx):
    if ctx.voice_client is not None and ctx.author.voice.channel==ctx.voice_client.channel:
      await ctx.voice_client.disconnect()
    else:
      await ctx.send("I am not connected to your voice channel now")
  
  @commands.command()
  async def play(self,ctx, *,song=None):
    if ctx.author.voice is None:
      return await ctx.send("You are not connected to any voice channels")
    
    if ctx.voice_client is not None and ctx.author.voice.channel!=ctx.voice_client.channel:
      await ctx.voice_client.disconnect()
      await ctx.author.voice.channel.connect()
    if song is None:
      return await ctx.send("You must include a song to play")
    if ctx.voice_client is None:
      await ctx.author.voice.channel.connect()

    #handle song when song isn't a URL
    if not("youtube.com/watch?" in song or "https://youtu.be/" in song):
      
      result=await self.search_song(1,song,get_url=True)
    
      if result is None:
        return await ctx.send("Sorry, song was not found. Try using search command")
      
      song=result[0]

    if ctx.voice_client.source is not None:
      queue_len=len(self.song_queue[ctx.guild.id])

      if queue_len < 20:
        self.song_queue[ctx.guild.id].append(song)
        return await ctx.send(f'I am currently playing a song. This song has been added to the queue at position {queue_len+1}')

      else:
        return await ctx.send("Sorry I can only queue 10 songs at a time. Please wait for current song to finish to queue again")

    await self.play_song(ctx,song)
    await ctx.send(f"Now playing: {song}")

  @commands.command()
  async def stop(self,ctx):
    if ctx.voice_client.source is None:
      return await ctx.send("No song playing currently")
    ctx.voice_client.stop()

  @commands.command()
  async def pause(self,ctx):
    if not ctx.voice_client.is_playing():
      return await ctx.send("No song is playing currently.")
    ctx.voice_client.pause()

  @commands.command()
  async def resume(self,ctx):
    if ctx.voice_client.is_playing():
      return await ctx.send("A song is currently being played.")
    ctx.voice_client.resume()


  @commands.command()
  async def search(self,ctx,*,song=None):
    if song is None: 
      return await ctx.send(f'You did not include a song to search')
    await ctx.send("Searching for song. This might take a few seconds..")

    info=await self.search_song(5,song)
    embed=discord.Embed(title=f'Results for {song}:', description=f'use these URLs to play a specific song you want, if the default search song is not what you were looking for.*\n',color=discord.Color.red())

    amount=0
    for entry in info["entries"]:
      embed.description+=f"[{entry['title']}]({entry['webpage_url']})\n"
      amount+=1

    embed.set_footer(text=f'Displaying the first {amount} results')
    await ctx.send(embed=embed)
  
  
  @commands.command()
  async def queue(self, ctx): # display the current queue
    
    if len(self.song_queue[ctx.guild.id]) == 0:
      return await ctx.send("There are currently no songs in the queue.")

    embed = discord.Embed(title="Song Queue", description="", colour=discord.Colour.dark_gold())
    YDL_OPTIONS = {'format': 'bestaudio', 'noplaylist': True, "quiet": True}
    i = 1
    #for url in self.song_queue[ctx.guild.id]:
     #embed.description += f"{i}) {url}\n"

     #i += 1

    for url in self.song_queue[ctx.guild.id]:
      with YoutubeDL(YDL_OPTIONS) as ydl:
        info_dict = ydl.extract_info(url, download=False)
        title=info_dict.get('title',None)
      embed.description+=f"{i}) [{title}]({url})\n"

      i+=1

    embed.set_footer(text="Displaying current queue.")
    await ctx.send(embed=embed)
  

  @commands.command()
  async def skip(self,ctx):
    if not ctx.voice_client.is_playing():
      return await ctx.send("Not playing any song currently")
    ctx.voice_client.pause()
    await self.check_queue(ctx)

  @commands.command()
  async def help(self,ctx):
    await ctx.send(">>> HELP PAGE \n\n1. !join - Request the bot to join your voice channel\n\n2. !leave - Request the bot to leave your voice channel\n\n3. !play song_name - Request the bot to play the song. If the command is used while a song is already playing, the requested song will be added to a queue, and the requests will be serviced after the current song finished playing. Max queue size is 20.\n\n4. !pause - Request the bot to pause the current song\n\n5. !resume - Request the bot to resume the paused song\n\n6. !skip - Request the bot to skip the current song and move to the next one in the list\n\n7. !search song_name- Request Top 5 search results from Youtube along with their urls (to be used in the play command)\n\n8. !queue - Displays the current queue\n\n  ")










    