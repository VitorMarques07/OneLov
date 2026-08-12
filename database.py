import aiosqlite
from pathlib import Path
from datetime import datetime
SCHEMA='''
CREATE TABLE IF NOT EXISTS guild_config(guild_id INTEGER PRIMARY KEY, weekly_goal INTEGER NOT NULL DEFAULT 2000, approval_required INTEGER NOT NULL DEFAULT 1, ticket_category_id INTEGER DEFAULT 0, log_channel_id INTEGER DEFAULT 0, cobrança_hour INTEGER DEFAULT 9, cobrança_minute INTEGER DEFAULT 0);
CREATE TABLE IF NOT EXISTS permissions(id INTEGER PRIMARY KEY AUTOINCREMENT,guild_id INTEGER NOT NULL,permission TEXT NOT NULL,role_id INTEGER,user_id INTEGER);
CREATE TABLE IF NOT EXISTS weeks(id INTEGER PRIMARY KEY AUTOINCREMENT,guild_id INTEGER NOT NULL,start_date TEXT NOT NULL,end_date TEXT NOT NULL,goal INTEGER NOT NULL,UNIQUE(guild_id,start_date));
CREATE TABLE IF NOT EXISTS tickets(id INTEGER PRIMARY KEY AUTOINCREMENT,guild_id INTEGER NOT NULL,channel_id INTEGER UNIQUE NOT NULL,member_id INTEGER NOT NULL,opened_at TEXT NOT NULL,closed_at TEXT,status TEXT NOT NULL DEFAULT 'open');
CREATE TABLE IF NOT EXISTS deliveries(id INTEGER PRIMARY KEY AUTOINCREMENT,guild_id INTEGER NOT NULL,ticket_id INTEGER,member_id INTEGER NOT NULL,quantity INTEGER NOT NULL,status TEXT NOT NULL DEFAULT 'pending',registered_by INTEGER NOT NULL,reviewed_by INTEGER,created_at TEXT NOT NULL,reviewed_at TEXT);
CREATE TABLE IF NOT EXISTS logs(id INTEGER PRIMARY KEY AUTOINCREMENT,guild_id INTEGER NOT NULL,user_id INTEGER,action TEXT NOT NULL,details TEXT,created_at TEXT NOT NULL);
'''
class Database:
 def __init__(self,path): self.path=Path(path); self.path.parent.mkdir(parents=True,exist_ok=True)
 async def init(self):
  async with aiosqlite.connect(self.path) as db: await db.executescript(SCHEMA); await db.commit()
 async def execute(self,sql,p=()):
  async with aiosqlite.connect(self.path) as db: c=await db.execute(sql,p); await db.commit(); return c.lastrowid
 async def one(self,sql,p=()):
  async with aiosqlite.connect(self.path) as db: db.row_factory=aiosqlite.Row; c=await db.execute(sql,p); return await c.fetchone()
 async def all(self,sql,p=()):
  async with aiosqlite.connect(self.path) as db: db.row_factory=aiosqlite.Row; c=await db.execute(sql,p); return await c.fetchall()
 async def log(self,g,u,a,d=''): await self.execute('INSERT INTO logs(guild_id,user_id,action,details,created_at) VALUES(?,?,?,?,?)',(g,u,a,d,datetime.utcnow().isoformat()))
