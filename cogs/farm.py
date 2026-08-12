import discord
from discord.ext import commands
from discord import app_commands
from datetime import datetime
from .common import allowed,week_range
class Review(discord.ui.View):
 def __init__(self,bot,did): super().__init__(timeout=None); self.bot=bot; self.did=did
 async def act(self,i,status):
  if not await allowed(i,'aprovação'): return await i.response.send_message('❌ Sem permissão.',ephemeral=True)
  r=await self.bot.db.one('SELECT * FROM deliveries WHERE id=?',(self.did,))
  if not r or r['status']!='pending': return await i.response.send_message('❌ Já processada.',ephemeral=True)
  await self.bot.db.execute('UPDATE deliveries SET status=?,reviewed_by=?,reviewed_at=? WHERE id=?',(status,i.user.id,datetime.utcnow().isoformat(),self.did)); await self.bot.db.log(i.guild_id,i.user.id,'entrega_'+status,f'id={self.did};qtd={r["quantity"]}'); await i.response.edit_message(content=('🟢 APROVADA' if status=='approved' else '🔴 REPROVADA')+f' — {r["quantity"]}',view=None)
 @discord.ui.button(label='Aprovar',emoji='🟢',style=discord.ButtonStyle.green)
 async def ok(self,i,b): await self.act(i,'approved')
 @discord.ui.button(label='Reprovar',emoji='🔴',style=discord.ButtonStyle.red)
 async def no(self,i,b): await self.act(i,'rejected')
class Farm(commands.Cog):
 def __init__(self,bot): self.bot=bot
 @app_commands.command(name='entrega',description='Registra uma entrega dentro do ticket.')
 async def delivery(self,i,quantidade:int):
  if not await allowed(i,'registro'): return await i.response.send_message('❌ Sem permissão.',ephemeral=True)
  if quantidade<=0:return await i.response.send_message('❌ Quantidade inválida.',ephemeral=True)
  t=await self.bot.db.one("SELECT id,member_id FROM tickets WHERE channel_id=? AND status='open'",(i.channel_id,))
  if not t:return await i.response.send_message('❌ Use este comando em um ticket ativo.',ephemeral=True)
  if t['member_id']!=i.user.id and not await allowed(i,'membros'):return await i.response.send_message('❌ Este ticket pertence a outro membro.',ephemeral=True)
  cfg=await self.bot.db.one('SELECT approval_required FROM guild_config WHERE guild_id=?',(i.guild_id,)); status='pending' if not cfg or cfg['approval_required'] else 'approved'
  did=await self.bot.db.execute('INSERT INTO deliveries(guild_id,ticket_id,member_id,quantity,status,registered_by,created_at) VALUES(?,?,?,?,?,?,?)',(i.guild_id,t['id'],t['member_id'],quantidade,status,i.user.id,datetime.utcnow().isoformat())); await self.bot.db.log(i.guild_id,i.user.id,'entrega_registrada',f'id={did};qtd={quantidade}')
  if status=='pending': await i.response.send_message(f'📦 **{quantidade:,}** pendente de aprovação.'.replace(',','.'),view=Review(self.bot,did))
  else: await i.response.send_message(f'🟢 **{quantidade:,}** aprovada automaticamente.'.replace(',','.'))
 @app_commands.command(name='pendentes',description='Lista entregas pendentes.')
 async def pending(self,i):
  if not await allowed(i,'aprovação'): return await i.response.send_message('❌ Sem permissão.',ephemeral=True)
  rows=await self.bot.db.all("SELECT * FROM deliveries WHERE guild_id=? AND status='pending' ORDER BY id DESC LIMIT 20",(i.guild_id,)); text='\n'.join(f"#{r['id']} — <@{r['member_id']}> — {r['quantity']:,}".replace(',','.') for r in rows) or 'Nenhuma.'; await i.response.send_message('📦 **PENDENTES**\n'+text)
async def setup(bot): await bot.add_cog(Farm(bot))
