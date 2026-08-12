import discord
from discord.ext import commands
from discord import app_commands
from datetime import datetime
from .common import allowed
class DashboardView(discord.ui.View):
 def __init__(self,cog): super().__init__(timeout=900); self.cog=cog
 @discord.ui.button(label='Atualizar',emoji='🔄',style=discord.ButtonStyle.blurple)
 async def refresh_btn(self,i,b):
  if not await allowed(i,'dashboard'): return await i.response.send_message('❌ Sem permissão.',ephemeral=True)
  await i.response.edit_message(embed=await self.cog.build(i),view=self)
 @discord.ui.button(label='Ranking',emoji='🏆',style=discord.ButtonStyle.green)
 async def ranking_btn(self,i,b): await self.cog.ranking(i)
 @discord.ui.button(label='Perfil',emoji='👤',style=discord.ButtonStyle.gray)
 async def profile_btn(self,i,b): await i.response.send_message('Use `/perfil usuario:@usuario` para consultar um perfil.',ephemeral=True)
 @discord.ui.button(label='Relatório',emoji='📋',style=discord.ButtonStyle.gray)
 async def report_btn(self,i,b): await self.cog.report(i)
class Dashboard(commands.Cog):
 def __init__(self,bot): self.bot=bot
 async def build(self,i):
  w=await self.bot.ensure_week(i.guild); goal=w['goal']; rows=await self.bot.db.all("SELECT member_id,SUM(quantity) total FROM deliveries WHERE week_id=? AND status='approved' GROUP BY member_id ORDER BY total DESC",(w['id'],)); total=sum(r['total'] for r in rows); hit=sum(r['total']>=goal for r in rows); pending=(await self.bot.db.one("SELECT COUNT(*) n FROM deliveries WHERE guild_id=? AND status='pending'",(i.guild_id,)))['n']; tickets=(await self.bot.db.one("SELECT COUNT(*) n FROM tickets WHERE guild_id=? AND status='open'",(i.guild_id,)))['n']
  e=discord.Embed(title='🏢 FARM MANAGEMENT',description=f'📅 Semana: {datetime.fromisoformat(w["start_date"]):%d/%m/%Y} → {datetime.fromisoformat(w["end_date"]):%d/%m/%Y}\n🎯 Meta: {goal:,}\n👥 Membros: {len(i.guild.members)}\n📦 Farm aprovado: {total:,}\n🟢 Metas batidas: {hit}\n🟡 Em acompanhamento: {max(0,len(rows)-hit)}\n🎫 Tickets ativos: {tickets}\n📦 Entregas pendentes: {pending}'.replace(',','.'),color=discord.Color.green()); lines=[]
  for n,r in enumerate(rows[:15],1):
   m=i.guild.get_member(r['member_id']); name=m.display_name if m else str(r['member_id']); rem=max(0,goal-r['total']); sit='🟢 META BATIDA' if rem==0 else ('🔴 PRECISA DE ATENÇÃO' if r['total']<goal//2 else '🟡 EM ANDAMENTO'); lines.append(f'{n}. **{name}** — {r["total"]:,} / {goal:,} — {sit}\n   Restante: {rem:,}'.replace(',','.'))
  e.add_field(name='🏆 RANKING',value='\n'.join(lines) or 'Nenhuma entrega aprovada.',inline=False); return e
 async def ranking(self,i):
  if not await allowed(i,'dashboard'): return await i.response.send_message('❌ Sem permissão.',ephemeral=True)
  w=await self.bot.ensure_week(i.guild); rows=await self.bot.db.all("SELECT member_id,SUM(quantity) total FROM deliveries WHERE week_id=? AND status='approved' GROUP BY member_id ORDER BY total DESC LIMIT 25",(w['id'],)); text=[f'{n}. <@{r["member_id"]}> — {r["total"]:,} / {w["goal"]:,}'.replace(',','.') for n,r in enumerate(rows,1)]; await i.response.send_message('🏆 **RANKING**\n'+('\n'.join(text) or 'Nenhum dado.'),ephemeral=True)
 async def report(self,i):
  cog=i.client.get_cog('Reports'); await cog.report(i) if cog else await i.response.send_message('❌ Relatório indisponível.',ephemeral=True)
 @app_commands.command(name='dashboard',description='Dashboard profissional da semana atual.')
 async def dashboard(self,i):
  if not await allowed(i,'dashboard'): return await i.response.send_message('❌ Sem permissão.',ephemeral=True)
  await i.response.send_message(embed=await self.build(i),view=DashboardView(self))
async def setup(bot): await bot.add_cog(Dashboard(bot))
