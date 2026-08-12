import discord
from discord.ext import commands, tasks
from config import settings
from database import Database
from datetime import datetime, timedelta

intents=discord.Intents.default(); intents.members=True; intents.guilds=True
class OneLov(commands.Bot):
 def __init__(self):
  super().__init__(command_prefix='!',intents=intents,application_id=settings.client_id or None); self.db=Database(settings.database_path)
  from zoneinfo import ZoneInfo; self.tz=ZoneInfo(settings.timezone)
 def local_now(self): return datetime.now(self.tz).replace(tzinfo=None)
 async def ensure_week(self,guild,now=None):
  now=now or self.local_now(); days_since_tuesday=(now.weekday()-1)%7; start=(now-timedelta(days=days_since_tuesday)).replace(hour=0,minute=0,second=0,microsecond=0); end=start+timedelta(days=7)
  cfg=await self.db.one('SELECT * FROM guild_config WHERE guild_id=?',(guild.id,)); goal=cfg['weekly_goal'] if cfg else settings.default_goal
  await self.db.execute('INSERT OR IGNORE INTO weeks(guild_id,start_date,end_date,goal,created_at) VALUES(?,?,?,?,?)',(guild.id,start.isoformat(),end.isoformat(),goal,now.isoformat())); return await self.db.one('SELECT * FROM weeks WHERE guild_id=? AND start_date=?',(guild.id,start.isoformat()))
 async def setup_hook(self):
  await self.db.init()
  for ext in ('cogs.admin','cogs.permissions','cogs.setup','cogs.tickets','cogs.farm','cogs.dashboard','cogs.reports'): await self.load_extension(ext)
  if settings.guild_id: await self.tree.sync(guild=discord.Object(id=settings.guild_id))
  else: await self.tree.sync()
  self.weekly_automation.start()
 async def on_ready(self):
  for guild in self.guilds: await self.ensure_week(guild)
  print(f'OneLov online: {self.user}')
 @tasks.loop(minutes=1)
 async def weekly_automation(self):
  now=self.local_now()
  for guild in self.guilds:
   await self.ensure_week(guild,now); cfg=await self.db.one('SELECT * FROM guild_config WHERE guild_id=?',(guild.id,))
   # Segunda-feira é o último dia do ciclo atual; a nova semana começa na terça.
   if cfg and cfg['auto_charge'] and now.weekday()==0 and now.hour==cfg['cobranca_hour'] and now.minute==cfg['cobranca_minute']: await self.send_charges(guild,now,False)
 async def send_charges(self,guild,now,manual=False):
  cfg=await self.db.one('SELECT * FROM guild_config WHERE guild_id=?',(guild.id,)); week=await self.ensure_week(guild,now)
  if not cfg: return
  members=await self.db.all('SELECT DISTINCT member_id FROM deliveries WHERE guild_id=? AND week_id=?',(guild.id,week['id']))
  for row in members:
   member=guild.get_member(row['member_id'])
   if not member: continue
   if not manual and await self.db.one('SELECT id FROM charges WHERE week_id=? AND member_id=?',(week['id'],member.id)): continue
   total=(await self.db.one("SELECT COALESCE(SUM(quantity),0) total FROM deliveries WHERE week_id=? AND member_id=? AND status='approved'",(week['id'],member.id)))['total']; remaining=max(0,cfg['weekly_goal']-total)
   if total>=cfg['weekly_goal']: continue
   msg=f'🔔 **OneLov — COBRANÇA SEMANAL**\n\n👤 {member.mention}\n🎯 Meta: **{cfg["weekly_goal"]:,}**\n📦 Farm aprovado: **{total:,}**\n📉 Restante: **{remaining:,}**\n📅 Ciclo: **{datetime.fromisoformat(week["start_date"]):%d/%m/%Y} → {datetime.fromisoformat(week["end_date"]):%d/%m/%Y}**\n\n⚠️ O ciclo encerra na segunda-feira. Um novo ciclo começa na terça-feira.'.replace(',','.')
   try: await member.send(msg)
   except discord.HTTPException: continue
   await self.db.execute('INSERT INTO charges(guild_id,week_id,member_id,channel_id,sent_at,manual) VALUES(?,?,?,?,?,?)',(guild.id,week['id'],member.id,0,now.isoformat(),1 if manual else 0)); await self.db.log(guild.id,self.user.id,'cobranca_enviada',f'membro={member.id};manual={manual}')
 @weekly_automation.before_loop
 async def before_weekly(self): await self.wait_until_ready()
bot=OneLov()
if not settings.token: raise RuntimeError('DISCORD_TOKEN não configurado no .env')
bot.run(settings.token)
