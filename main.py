import discord
from discord.ext import commands
import os
from music import MusicPlayer
from keep_awake import keep_awake

intents=discord.Intents.all()
intents.members=True

bot=commands.Bot(command_prefix='!',intent=intents)
bot.remove_command("help")
TOKEN=os.environ['TOKEN']

@bot.event
async def on_ready():
  print(f'{bot.user.name} has been activated')


async def setup():
  await bot.wait_until_ready()
  bot.add_cog(MusicPlayer(bot))


bot.loop.create_task(setup())
keep_awake()
bot.run(TOKEN)
