import discord
from discord.ext import commands
from discord import app_commands
from datetime import datetime
from .common import allowed, week_range
from config import settings

class AdminPanel(discord.ui.View):
    def __init__(self, bot): super().__init__(timeout=300); self.bot=bot
    @discord.ui.button(label='🎯 Meta', style=discord.ButtonStyle.primary)
    async def goal(self,i,b):
        if i.user.id!=settings.super_admin_id: return await i.response.send_message('❌ Apenas o Administrador Supremo.',ephemeral=True)
        c=await self.bot.db.one('SELECT weekly_goal FROM guild_config WHERE guild_id=?',(i.guild_id,)); await i.response.send_message(f'🎯 Meta atual: **{c["weekly_goal"] if c else settings.default_goal:,}**'.replace(',','.'),ephemeral=True)
    @discord.ui.button(label='🔐 Permissões', style=discord.ButtonStyle.secondary)
    async def perms(self,i,b):
        if i.user.id!=settings.super_admin_id:return await i.response.send_message('❌ Sem acesso.',ephemeral=True)
        rows=await self.bot.db.all('SELECT permission,role_id,user_id FROM permissions WHERE guild_id=?',(i.guild_id,)); txt='\n'.join(f"• {r['permission']}: cargo {r['role_id'] or '-'} usuário {r['user_id'] or '-'}" for r in rows) or 'Nenhuma configuração.'; await i.response.send_message('🔐 **PERMISSÕES**\n'+txt,ephemeral=True)

class Advanced(commands.Cog):
    def __init__(self,bot): self.bot=bot
    @app_commands.command(name='admin',description='Painel do Administrador Supremo.')
    async def admin(self,i):
        if i.user.id!=settings.super_admin_id:return await i.response.send_message('❌ Apenas o Administrador Supremo.',ephemeral=True)
        await i.response.send_message('👑 **FARM MANAGER — PAINEL ADMINISTRATIVO**',view=AdminPanel(self.bot),ephemeral=True)
    @app_commands.command(name='cobrar',description='Envia cobrança manual nos tickets ativos.')
    async def charge(self,i):
        if not await allowed(i,'cobranças'):return await i.response.send_message('❌ Sem permissão.',ephemeral=True)
        await self.bot.send_charges(i.guild,datetime.now(self.bot.tz),True); await i.response.send_message('🔔 Cobrança manual enviada nos tickets ativos.',ephemeral=True)
    @app_commands.command(name='historico',description='Consulta o histórico de semanas.')
    async def history(self,i):
        if not await allowed(i,'relatórios'):return await i.response.send_message('❌ Sem permissão.',ephemeral=True)
        rows=await self.bot.db.all('SELECT * FROM weeks WHERE guild_id=? ORDER BY start_date DESC LIMIT 12',(i.guild_id,)); txt='\n'.join(f"📅 {r['start_date'][:10]} → {r['end_date'][:10]} — 🎯 {r['goal']:,}".replace(',','.') for r in rows) or 'Nenhuma semana registrada.'; await i.response.send_message('📅 **HISTÓRICO**\n'+txt)
    @app_commands.command(name='logs',description='Consulta logs recentes.')
    async def logs(self,i):
        if not await allowed(i,'logs'):return await i.response.send_message('❌ Sem permissão.',ephemeral=True)
        rows=await self.bot.db.all('SELECT * FROM logs WHERE guild_id=? ORDER BY id DESC LIMIT 20',(i.guild_id,)); txt='\n'.join(f"`{r['created_at'][:19]}` <@{r['user_id']}> — **{r['action']}** — {r['details'] or ''}" for r in rows) or 'Nenhum log.'; await i.response.send_message('📝 **LOGS**\n'+txt,ephemeral=True)
    @app_commands.command(name='backup',description='Cria uma cópia lógica do banco em backup local.')
    async def backup(self,i):
        if i.user.id!=settings.super_admin_id:return await i.response.send_message('❌ Apenas o Administrador Supremo.',ephemeral=True)
        import shutil, pathlib
        src=pathlib.Path(settings.database_path); dest=src.parent/f'backup_{datetime.now():%Y%m%d_%H%M%S}.db'; shutil.copy2(src,dest); await self.bot.db.log(i.guild_id,i.user.id,'backup_criado',str(dest)); await i.response.send_message(f'💾 Backup criado: `{dest.name}`',ephemeral=True)
async def setup(bot): await bot.add_cog(Advanced(bot))
