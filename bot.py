import discord
from discord.ext import commands
from config import settings
from database import Database
intents=discord.Intents.default(); intents.members=True; intents.guilds=True
class FarmManager(commands.Bot):
 def __init__(self): super().__init__(command_prefix='!',intents=intents,application_id=settings.client_id or None); self.db=Database(settings.database_path)
 async def setup_hook(self):
  await self.db.init()
  for ext in ('cogs.admin','cogs.permissions','cogs.tickets','cogs.farm','cogs.dashboard','cogs.reports'):
   await self.load_extension(ext)
  if settings.guild_id: await self.tree.sync(guild=discord.Object(id=settings.guild_id))
  else: await self.tree.sync()
 async def on_ready(self): print(f'FARM MANAGER online: {self.user}')
bot=FarmManager()
if not settings.token: raise RuntimeError('DISCORD_TOKEN não configurado no .env')
bot.run(settings.token)
