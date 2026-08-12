import os
from dataclasses import dataclass
from dotenv import load_dotenv
load_dotenv()
@dataclass(frozen=True)
class Settings:
    token:str=os.getenv('DISCORD_TOKEN','')
    client_id:int=int(os.getenv('DISCORD_CLIENT_ID','0') or 0)
    guild_id:int=int(os.getenv('DISCORD_GUILD_ID','0') or 0)
    super_admin_id:int=int(os.getenv('SUPER_ADMIN_ID','0') or 0)
    database_path:str=os.getenv('DATABASE_PATH','data/farm_manager.db')
    timezone:str=os.getenv('TIMEZONE','America/Sao_Paulo')
    default_goal:int=int(os.getenv('DEFAULT_WEEKLY_GOAL','2000'))
settings=Settings()
