import aiosqlite
from pathlib import Path
from datetime import datetime, timezone
SCHEMA='''
CREATE TABLE IF NOT EXISTS guild_config(guild_id INTEGER PRIMARY KEY,weekly_goal INTEGER NOT NULL DEFAULT 2000,approval_required INTEGER NOT NULL DEFAULT 1,ticket_category_id INTEGER DEFAULT 0,log_channel_id INTEGER DEFAULT 0,cobranca_hour INTEGER NOT NULL DEFAULT 18,cobranca_minute INTEGER NOT NULL DEFAULT 0,duplicate_tickets INTEGER NOT NULL DEFAULT 1,auto_charge INTEGER NOT NULL DEFAULT 1);
CREATE TABLE IF NOT EXISTS permissions(id INTEGER PRIMARY KEY AUTOINCREMENT,guild_id INTEGER NOT NULL,permission TEXT NOT NULL,role_id INTEGER,user_id INTEGER,UNIQUE(guild_id,permission,role_id,user_id));
CREATE TABLE IF NOT EXISTS weeks(id INTEGER PRIMARY KEY AUTOINCREMENT,guild_id INTEGER NOT NULL,start_date TEXT NOT NULL,end_date TEXT NOT NULL,goal INTEGER NOT NULL,created_at TEXT NOT NULL,UNIQUE(guild_id,start_date));
CREATE TABLE IF NOT EXISTS tickets(id INTEGER PRIMARY KEY AUTOINCREMENT,guild_id INTEGER NOT NULL,channel_id INTEGER UNIQUE NOT NULL,member_id INTEGER NOT NULL,opened_at TEXT NOT NULL,closed_at TEXT,status TEXT NOT NULL DEFAULT 'open');
CREATE TABLE IF NOT EXISTS deliveries(id INTEGER PRIMARY KEY AUTOINCREMENT,guild_id INTEGER NOT NULL,week_id INTEGER,ticket_id INTEGER,member_id INTEGER NOT NULL,quantity INTEGER NOT NULL,status TEXT NOT NULL DEFAULT 'pending',registered_by INTEGER NOT NULL,reviewed_by INTEGER,created_at TEXT NOT NULL,reviewed_at TEXT,attachment_url TEXT,attachment_name TEXT,review_channel_id INTEGER,review_message_id INTEGER);
CREATE TABLE IF NOT EXISTS charges(id INTEGER PRIMARY KEY AUTOINCREMENT,guild_id INTEGER NOT NULL,week_id INTEGER,member_id INTEGER,channel_id INTEGER,sent_at TEXT NOT NULL,manual INTEGER NOT NULL DEFAULT 0);
CREATE TABLE IF NOT EXISTS logs(id INTEGER PRIMARY KEY AUTOINCREMENT,guild_id INTEGER NOT NULL,user_id INTEGER,action TEXT NOT NULL,details TEXT,created_at TEXT NOT NULL);
'''
class Database:
 def __init__(self,path): self.path=Path(path); self.path.parent.mkdir(parents=True,exist_ok=True)
 async def init(self):
  async with aiosqlite.connect(self.path) as db:
   await db.executescript(SCHEMA)
   migrations={'guild_config':{'cobranca_hour':'INTEGER NOT NULL DEFAULT 18','cobranca_minute':'INTEGER NOT NULL DEFAULT 0','duplicate_tickets':'INTEGER NOT NULL DEFAULT 1','auto_charge':'INTEGER NOT NULL DEFAULT 1'},'deliveries':{'week_id':'INTEGER','attachment_url':'TEXT','attachment_name':'TEXT','review_channel_id':'INTEGER','review_message_id':'INTEGER'}}
   for table,cols in migrations.items():
    cur=await db.execute(f'PRAGMA table_info({table})'); existing={r[1] for r in await cur.fetchall()}
    for name,definition in cols.items():
     if name not in existing: await db.execute(f'ALTER TABLE {table} ADD COLUMN {name} {definition}')
   await db.commit()
 async def execute(self,sql,p=()):
  async with aiosqlite.connect(self.path) as db: c=await db.execute(sql,p); await db.commit(); return c.lastrowid
 async def one(self,sql,p=()):
  async with aiosqlite.connect(self.path) as db: db.row_factory=aiosqlite.Row; c=await db.execute(sql,p); return await c.fetchone()
 async def all(self,sql,p=()):
  async with aiosqlite.connect(self.path) as db: db.row_factory=aiosqlite.Row; c=await db.execute(sql,p); return await c.fetchall()
 async def log(self,g,u,a,d=''): await self.execute('INSERT INTO logs(guild_id,user_id,action,details,created_at) VALUES(?,?,?,?,?)',(g,u,a,d,datetime.now(timezone.utc).isoformat()))
