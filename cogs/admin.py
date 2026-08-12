import discord
from discord.ext import commands
from discord import app_commands
from .common import allowed
class Admin(commands.Cog):
 def __init__(self,bot): self.bot=bot
 @app_commands.command(name='config',description='Configura o sistema OneLov.')
 @app_commands.describe(meta='Meta semanal',aprovacao='Exigir aprovação?',categoria='Categoria dos tickets',logs='Canal de logs',hora_cobranca='Hora da cobrança de segunda (0-23)',minuto_cobranca='Minuto da cobrança (0-59)',cobranca_automatica='Ativar cobrança automática?')
 async def config(self,i,meta:int=None,aprovacao:bool=None,categoria:discord.CategoryChannel=None,logs:discord.TextChannel=None,hora_cobranca:int=None,minuto_cobranca:int=None,cobranca_automatica:bool=None):
  if not await allowed(i,'configuração'): return await i.response.send_message('❌ Sem permissão.',ephemeral=True)
  if meta is not None and meta<0:return await i.response.send_message('❌ Meta inválida.',ephemeral=True)
  if hora_cobranca is not None and not 0<=hora_cobranca<=23:return await i.response.send_message('❌ Hora deve ser 0-23.',ephemeral=True)
  if minuto_cobranca is not None and not 0<=minuto_cobranca<=59:return await i.response.send_message('❌ Minuto deve ser 0-59.',ephemeral=True)
  old=await self.bot.db.one('SELECT * FROM guild_config WHERE guild_id=?',(i.guild_id,)); vals=(meta if meta is not None else (old['weekly_goal'] if old else 2000),1 if aprovacao else 0 if aprovacao is not None else (old['approval_required'] if old else 1),categoria.id if categoria else (old['ticket_category_id'] if old else 0),logs.id if logs else (old['log_channel_id'] if old else 0),hora_cobranca if hora_cobranca is not None else (old['cobranca_hour'] if old else 18),minuto_cobranca if minuto_cobranca is not None else (old['cobranca_minute'] if old else 0),1 if cobranca_automatica else 0 if cobranca_automatica is not None else (old['auto_charge'] if old else 1))
  await self.bot.db.execute('INSERT INTO guild_config(guild_id,weekly_goal,approval_required,ticket_category_id,log_channel_id,cobranca_hour,cobranca_minute,auto_charge) VALUES(?,?,?,?,?,?,?,?) ON CONFLICT(guild_id) DO UPDATE SET weekly_goal=excluded.weekly_goal,approval_required=excluded.approval_required,ticket_category_id=excluded.ticket_category_id,log_channel_id=excluded.log_channel_id,cobranca_hour=excluded.cobranca_hour,cobranca_minute=excluded.cobranca_minute,auto_charge=excluded.auto_charge',(i.guild_id,*vals)); await self.bot.db.log(i.guild_id,i.user.id,'config_alterada',str(vals)); await i.response.send_message('✅ Configuração atualizada.',ephemeral=True)
 @app_commands.command(name='iniciarsemana',description='Inicializa a semana atual imediatamente.')
 async def startweek(self,i):
  if not await allowed(i,'meta'):return await i.response.send_message('❌ Sem permissão.',ephemeral=True)
  await self.bot.ensure_week(i.guild); await i.response.send_message('✅ Semana atual inicializada.',ephemeral=True)
 @app_commands.command(name='cobrar',description='Executa a cobrança manual para membros abaixo da meta.')
 async def charge(self,i):
  if not await allowed(i,'cobranças'):return await i.response.send_message('❌ Sem permissão.',ephemeral=True)
  await self.bot.ensure_week(i.guild); await self.bot.send_charges(i.guild,self.bot.local_now(),True); await self.bot.db.log(i.guild_id,i.user.id,'cobranca_manual'); await i.response.send_message('🔔 Cobrança manual processada para membros abaixo da meta.',ephemeral=True)
async def setup(bot): await bot.add_cog(Admin(bot))
