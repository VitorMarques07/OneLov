import discord
from discord.ext import commands
from discord import app_commands
from datetime import datetime
from .common import allowed
class Reports(commands.Cog):
 def __init__(self,bot): self.bot=bot
 @app_commands.command(name='relatorio',description='Gera relatório semanal.')
 async def report(self,i):
  if not await allowed(i,'relatórios'): return await i.response.send_message('❌ Sem permissão.',ephemeral=True)
  w=await self.bot.ensure_week(i.guild); goal=w['goal']; rows=await self.bot.db.all("SELECT member_id,SUM(quantity) total FROM deliveries WHERE week_id=? AND status='approved' GROUP BY member_id ORDER BY total DESC",(w['id'],)); total=sum(r['total'] for r in rows); hit=sum(r['total']>=goal for r in rows)
  e=discord.Embed(title='📋 RELATÓRIO SEMANAL',description=f'📅 {datetime.fromisoformat(w["start_date"]):%d/%m/%Y} → {datetime.fromisoformat(w["end_date"]):%d/%m/%Y}\n🎯 Meta por pessoa: {goal:,}\n👥 Membros com entregas: {len(rows)}\n📦 Total aprovado: {total:,}\n🟢 Metas batidas: {hit}\n🔴 Não bateram: {len(rows)-hit}'.replace(',','.'))
  for r in rows:
   m=i.guild.get_member(r['member_id']); name=m.display_name if m else str(r['member_id']); e.add_field(name=name,value=f'{r["total"]:,} / {goal:,} — '+('🟢 Meta batida' if r['total']>=goal else '🔴 Não bateu').replace(',','.'),inline=False)
  await self.bot.db.log(i.guild_id,i.user.id,'relatorio_gerado'); await i.response.send_message(embed=e,ephemeral=True)
 @app_commands.command(name='perfil',description='Mostra o seu perfil de Farm; equipe autorizada pode consultar outro membro.')
 async def profile(self,i,usuario:discord.Member=None):
  if usuario and usuario.id!=i.user.id and not await allowed(i,'dashboard'): return await i.response.send_message('🔒 Você só pode consultar o seu próprio perfil.',ephemeral=True)
  u=usuario or i.user; w=await self.bot.ensure_week(i.guild); goal=w['goal']; total=(await self.bot.db.one("SELECT COALESCE(SUM(quantity),0) total FROM deliveries WHERE week_id=? AND member_id=? AND status='approved'",(w['id'],u.id)))['total']; a=(await self.bot.db.one("SELECT COUNT(*) n FROM deliveries WHERE guild_id=? AND member_id=? AND status='approved'",(i.guild_id,u.id)))['n']; r=(await self.bot.db.one("SELECT COUNT(*) n FROM deliveries WHERE guild_id=? AND member_id=? AND status='rejected'",(i.guild_id,u.id)))['n']; rem=max(0,goal-total); sit='🟢 META BATIDA' if rem==0 else '🟡 EM ANDAMENTO'
  e=discord.Embed(title=f'👤 PERFIL — {u.display_name}',description=f'🎯 Meta semanal: {goal:,}\n📦 Farm aprovado: {total:,}\n📉 Restante: {rem:,}\n📌 Situação: {sit}\n🟢 Entregas aprovadas: {a}\n🔴 Entregas reprovadas: {r}'.replace(',','.')); await i.response.send_message(embed=e,ephemeral=True)
async def setup(bot): await bot.add_cog(Reports(bot))
