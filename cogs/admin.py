import discord
from discord.ext import commands
from discord import app_commands
from .common import allowed
class Admin(commands.Cog):
 def __init__(self,bot): self.bot=bot
 @app_commands.command(name='config',description='Configura meta, aprovação e canais do sistema.')
 @app_commands.describe(meta='Meta semanal',aprovacao='Exigir aprovação?',categoria='Categoria dos tickets',logs='Canal de logs')
 async def config(self,i:discord.Interaction,meta:int=None,aprovacao:bool=None,categoria:discord.CategoryChannel=None,logs:discord.TextChannel=None):
  if not await allowed(i,'configuração'): return await i.response.send_message('❌ Sem permissão.',ephemeral=True)
  old=await self.bot.db.one('SELECT * FROM guild_config WHERE guild_id=?',(i.guild_id,)); vals=(meta if meta is not None else (old['weekly_goal'] if old else 2000),1 if aprovacao else 0 if aprovacao is not None else (old['approval_required'] if old else 1),categoria.id if categoria else (old['ticket_category_id'] if old else 0),logs.id if logs else (old['log_channel_id'] if old else 0))
  await self.bot.db.execute('INSERT INTO guild_config(guild_id,weekly_goal,approval_required,ticket_category_id,log_channel_id) VALUES(?,?,?,?,?) ON CONFLICT(guild_id) DO UPDATE SET weekly_goal=excluded.weekly_goal,approval_required=excluded.approval_required,ticket_category_id=excluded.ticket_category_id,log_channel_id=excluded.log_channel_id',(i.guild_id,*vals))
  await self.bot.db.log(i.guild_id,i.user.id,'config_alterada',str(vals)); await i.response.send_message('✅ Configuração atualizada.')
async def setup(bot): await bot.add_cog(Admin(bot))
