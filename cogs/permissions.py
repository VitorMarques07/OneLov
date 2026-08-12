import discord
from discord.ext import commands
from discord import app_commands
from config import settings
from .common import PERMS
class Permissions(commands.Cog):
 def __init__(self,bot): self.bot=bot
 @app_commands.command(name='permissao',description='Concede uma permissão a cargo ou usuário.')
 @app_commands.describe(permissao='Permissão',cargo='Cargo',usuario='Usuário')
 @app_commands.choices(permissao=[app_commands.Choice(name=p,value=p) for p in PERMS])
 async def grant(self,i,p:app_commands.Choice[str],cargo:discord.Role=None,usuario:discord.Member=None):
  if i.user.id!=settings.super_admin_id: return await i.response.send_message('❌ Apenas o Administrador Supremo.',ephemeral=True)
  if not cargo and not usuario: return await i.response.send_message('❌ Informe cargo ou usuário.',ephemeral=True)
  await self.bot.db.execute('INSERT INTO permissions(guild_id,permission,role_id,user_id) VALUES(?,?,?,?)',(i.guild_id,p.value,cargo.id if cargo else None,usuario.id if usuario else None)); await self.bot.db.log(i.guild_id,i.user.id,'permissao_alterada',p.value)
  await i.response.send_message('✅ Permissão concedida.')
 @app_commands.command(name='permissoes',description='Lista permissões configuradas.')
 async def list(self,i):
  if i.user.id!=settings.super_admin_id: return await i.response.send_message('❌ Apenas o Administrador Supremo.',ephemeral=True)
  rows=await self.bot.db.all('SELECT * FROM permissions WHERE guild_id=?',(i.guild_id,)); text='\n'.join(f"{r['permission']} — cargo {r['role_id'] or '-'} — usuário {r['user_id'] or '-'}" for r in rows) or 'Nenhuma.'
  await i.response.send_message('🔐 **PERMISSÕES**\n'+text)
async def setup(bot): await bot.add_cog(Permissions(bot))
