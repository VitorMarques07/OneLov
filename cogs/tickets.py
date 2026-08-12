import discord
from discord.ext import commands
from discord import app_commands
from datetime import datetime
from .common import allowed
class TicketView(discord.ui.View):
 def __init__(self,bot): super().__init__(timeout=None); self.bot=bot
 @discord.ui.button(label='ABRIR TICKET',style=discord.ButtonStyle.green,custom_id='fm:ticket')
 async def open(self,i,b):
  if not await allowed(i,'tickets'): return await i.response.send_message('❌ Sem permissão para abrir tickets.',ephemeral=True)
  row=await self.bot.db.one("SELECT channel_id FROM tickets WHERE guild_id=? AND member_id=? AND status='open'",(i.guild_id,i.user.id))
  if row:
   c=i.guild.get_channel(row['channel_id']); return await i.response.send_message(f'❌ Ticket já aberto: {c.mention if c else row["channel_id"]}.',ephemeral=True)
  cfg=await self.bot.db.one('SELECT ticket_category_id FROM guild_config WHERE guild_id=?',(i.guild_id,)); cat=i.guild.get_channel(cfg['ticket_category_id']) if cfg and cfg['ticket_category_id'] else None
  ow={i.guild.default_role:discord.PermissionOverwrite(view_channel=False),i.user:discord.PermissionOverwrite(view_channel=True,send_messages=True),i.guild.me:discord.PermissionOverwrite(view_channel=True,send_messages=True)}
  c=await i.guild.create_text_channel(f'farm-{i.user.name}'[:90],category=cat,overwrites=ow); tid=await self.bot.db.execute('INSERT INTO tickets(guild_id,channel_id,member_id,opened_at) VALUES(?,?,?,?)',(i.guild_id,c.id,i.user.id,datetime.utcnow().isoformat())); await self.bot.db.log(i.guild_id,i.user.id,'ticket_criado',f'ticket={tid}'); await c.send(f'🎫 Ticket de {i.user.mention}\nUse `/entrega quantidade:500`.'); await i.response.send_message(f'✅ {c.mention}',ephemeral=True)
class Tickets(commands.Cog):
 def __init__(self,bot): self.bot=bot; bot.add_view(TicketView(bot))
 @app_commands.command(name='painel',description='Envia o painel de tickets.')
 async def panel(self,i):
  if not await allowed(i,'tickets'): return await i.response.send_message('❌ Sem permissão.',ephemeral=True)
  await i.response.send_message('🎫 **FARM MANAGER**\nClique para abrir seu ticket.',view=TicketView(self.bot))
 @app_commands.command(name='fecharticket',description='Fecha o ticket atual.')
 async def close(self,i):
  row=await self.bot.db.one("SELECT * FROM tickets WHERE channel_id=? AND status='open'",(i.channel_id,))
  if not row: return await i.response.send_message('❌ Não é um ticket ativo.',ephemeral=True)
  if i.user.id!=row['member_id'] and not await allowed(i,'tickets'): return await i.response.send_message('❌ Sem permissão.',ephemeral=True)
  await self.bot.db.execute("UPDATE tickets SET status='closed',closed_at=? WHERE id=?",(datetime.utcnow().isoformat(),row['id'])); await self.bot.db.log(i.guild_id,i.user.id,'ticket_fechado',f'ticket={row["id"]}'); await i.response.send_message('🔒 Ticket fechado. Histórico preservado.'); await i.channel.set_permissions(i.guild.default_role,view_channel=False)
async def setup(bot): await bot.add_cog(Tickets(bot))
