import discord
from discord.ext import commands
from discord import app_commands
from datetime import datetime
from .common import allowed,week_range
class Reports(commands.Cog):
 def __init__(self,bot): self.bot=bot
 @app_commands.command(name='relatorio',description='Gera relatório semanal.')
 async def report(self,i):
  if not await allowed(i,'relatórios'): return await i.response.send_message('❌ Sem permissão.',ephemeral=True)
  start,end=week_range(datetime.now()); cfg=await self.bot.db.one('SELECT weekly_goal FROM guild_config WHERE guild_id=?',(i.guild_id,)); goal=cfg['weekly_goal'] if cfg else 2000
  rows=await self.bot.db.all("SELECT member_id,SUM(quantity) total FROM deliveries WHERE guild_id=? AND status='approved' AND created_at>=? AND created_at<=? GROUP BY member_id ORDER BY total DESC",(i.guild_id,start.isoformat(),end.isoformat())); total=sum(r['total'] for r in rows); hit=sum(r['total']>=goal for r in rows)
  e=discord.Embed(title='📋 RELATÓRIO SEMANAL',description=f'📅 {start:%d/%m/%Y} → {end:%d/%m/%Y}\n🎯 Meta por pessoa: {goal:,}\n👥 Membros com entregas: {len(rows)}\n📦 Total aprovado: {total:,}\n🟢 Metas batidas: {hit}\n🔴 Não bateram: {len(rows)-hit}'.replace(',','.'))
  for r in rows:
   m=i.guild.get_member(r['member_id']); name=m.display_name if m else str(r['member_id']); e.add_field(name=name,value=f'{r["total"]:,} / {goal:,} — '+('🟢 Meta batida' if r['total']>=goal else '🔴 Não bateu').replace(',','.'),inline=False)
  await self.bot.db.log(i.guild_id,i.user.id,'relatorio_gerado'); await i.response.send_message(embed=e)
 @app_commands.command(name='perfil',description='Mostra o perfil de farm de um membro.')
 async def profile(self,i,usuario:discord.Member=None):
  if not await allowed(i,'dashboard'): return await i.response.send_message('❌ Sem permissão.',ephemeral=True)
  u=usuario or i.user; start,end=week_range(datetime.now()); cfg=await self.bot.db.one('SELECT weekly_goal FROM guild_config WHERE guild_id=?',(i.guild_id,)); goal=cfg['weekly_goal'] if cfg else 2000
  total=(await self.bot.db.one("SELECT COALESCE(SUM(quantity),0) total FROM deliveries WHERE guild_id=? AND member_id=? AND status='approved' AND created_at>=? AND created_at<=?",(i.guild_id,u.id,start.isoformat(),end.isoformat())))['total']; a=(await self.bot.db.one("SELECT COUNT(*) n FROM deliveries WHERE guild_id=? AND member_id=? AND status='approved'",(i.guild_id,u.id)))['n']; r=(await self.bot.db.one("SELECT COUNT(*) n FROM deliveries WHERE guild_id=? AND member_id=? AND status='rejected'",(i.guild_id,u.id)))['n']; t=(await self.bot.db.one("SELECT COUNT(*) n FROM tickets WHERE guild_id=? AND member_id=?",(i.guild_id,u.id)))['n']; rem=max(0,goal-total); sit='🟢 META BATIDA' if rem==0 else '🟡 EM ANDAMENTO'
  e=discord.Embed(title=f'👤 PERFIL — {u.display_name}',description=f'🎯 Meta semanal: {goal:,}\n📦 Total aprovado: {total:,}\n📉 Restante: {rem:,}\n📌 Situação: {sit}\n🎫 Tickets: {t}\n🟢 Entregas aprovadas: {a}\n🔴 Entregas reprovadas: {r}'.replace(',','.')); await i.response.send_message(embed=e)
async def setup(bot): await bot.add_cog(Reports(bot))
