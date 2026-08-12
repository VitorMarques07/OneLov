import discord
from discord.ext import commands
from discord import app_commands
from datetime import datetime
from .common import allowed
class Dashboard(commands.Cog):
 def __init__(self,bot): self.bot=bot
 async def build(self,i):
  w=await self.bot.ensure_week(i.guild); goal=w['goal']; rows=await self.bot.db.all("SELECT member_id,SUM(quantity) total FROM deliveries WHERE week_id=? AND status='approved' GROUP BY member_id ORDER BY total DESC",(w['id'],)); total=sum(r['total'] for r in rows); hit=sum(r['total']>=goal for r in rows)
  e=discord.Embed(title='🏢 FARM MANAGEMENT',description=f'📅 Semana: {datetime.fromisoformat(w["start_date"]):%d/%m/%Y} → {datetime.fromisoformat(w["end_date"]):%d/%m/%Y}\n🎯 Meta: {goal:,}\n👥 Membros: {len(i.guild.members)}\n📦 Farm aprovado: {total:,}\n🟢 Metas batidas: {hit}\n🟡 Em acompanhamento: {max(0,len(rows)-hit)}'.replace(',','.'),color=discord.Color.green()); lines=[]
  for n,r in enumerate(rows[:15],1):
   m=i.guild.get_member(r['member_id']); name=m.display_name if m else str(r['member_id']); rem=max(0,goal-r['total']); sit='🟢 META BATIDA' if rem==0 else ('🔴 PRECISA DE ATENÇÃO' if r['total']<goal//2 else '🟡 EM ANDAMENTO'); lines.append(f'{n}. **{name}** — {r["total"]:,} / {goal:,} — {sit}\n   Restante: {rem:,}'.replace(',','.'))
  e.add_field(name='🏆 RANKING',value='\n'.join(lines) or 'Nenhuma entrega aprovada.',inline=False); return e
 @app_commands.command(name='dashboard',description='Dashboard da semana atual.')
 async def dashboard(self,i):
  if not await allowed(i,'dashboard'): return await i.response.send_message('❌ Sem permissão.',ephemeral=True)
  await i.response.send_message(embed=await self.build(i))
async def setup(bot): await bot.add_cog(Dashboard(bot))
