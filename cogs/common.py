import discord
from config import settings
PERMS=('configuração','tickets','registro','aprovação','membros','meta','dashboard','relatórios','cobranças','logs')
async def allowed(interaction,permission):
 if interaction.user.id==settings.super_admin_id: return True
 db=interaction.client.db
 rows=await db.all('SELECT role_id,user_id FROM permissions WHERE guild_id=? AND permission=?',(interaction.guild_id,permission))
 if any(r['user_id']==interaction.user.id for r in rows if r['user_id']): return True
 role_ids={r.id for r in getattr(interaction.user,'roles',[])}
 return any(r['role_id'] in role_ids for r in rows if r['role_id'])
def week_range(now):
 from datetime import timedelta
 start=now-timedelta(days=now.weekday()); return start.replace(hour=0,minute=0,second=0,microsecond=0), (start+timedelta(days=6)).replace(hour=23,minute=59,second=59,microsecond=999999)
