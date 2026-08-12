import discord
from discord.ext import commands
from discord import app_commands
from config import settings
from .tickets import TicketView
from .farm import DeliveryView

CHANNELS={'informacoes':'📌・informações','entregas_farm':'📦・entregas-de-farm','entregas':'📋・entregas','metas':'🎯・metas','ranking':'🏆・ranking','perfis':'👤・perfis','tickets':'🎫・tickets','logs':'📑・logs'}

class Setup(commands.Cog):
 def __init__(self,bot): self.bot=bot
 def supreme(self,member): return member.id==settings.super_admin_id or member.id==member.guild.owner_id
 async def role(self,guild,name):
  role=discord.utils.get(guild.roles,name=name); return role or await guild.create_role(name=name,reason='OneLov /setup')
 async def channel(self,guild,name,category):
  ch=discord.utils.get(guild.text_channels,name=name)
  if ch:
   if ch.category_id!=category.id: await ch.edit(category=category,reason='OneLov /setup')
   return ch
  return await guild.create_text_channel(name,category=category,reason='OneLov /setup')
 async def permissions(self,guild,category,staff,admin,channels):
  everyone=guild.default_role; bot=guild.me
  base={everyone:discord.PermissionOverwrite(view_channel=True,send_messages=False,read_message_history=True),staff:discord.PermissionOverwrite(view_channel=True,send_messages=False,read_message_history=True),admin:discord.PermissionOverwrite(view_channel=True,send_messages=False,manage_messages=True,manage_channels=True,read_message_history=True)}
  if bot: base[bot]=discord.PermissionOverwrite(view_channel=True,send_messages=True,manage_messages=True,manage_channels=True,embed_links=True,attach_files=True,read_message_history=True)
  await category.edit(overwrites=base,reason='OneLov /setup')
  for key,ch in channels.items():
   ow=dict(base)
   if key=='entregas': ow[everyone]=discord.PermissionOverwrite(view_channel=False); ow[staff]=discord.PermissionOverwrite(view_channel=True,send_messages=False,read_message_history=True)
   if key=='logs': ow[everyone]=discord.PermissionOverwrite(view_channel=False); ow[staff]=discord.PermissionOverwrite(view_channel=True,send_messages=False,read_message_history=True)
   if key=='perfis': ow[everyone]=discord.PermissionOverwrite(view_channel=True,send_messages=False,read_message_history=True)
   await ch.edit(overwrites=ow,reason='OneLov /setup')
 async def grant_defaults(self,guild,staff,admin):
  perms=['aprovação','registro','membros','meta','dashboard','relatórios','cobranças','logs','tickets']
  for role in (staff,admin):
   for p in perms:
    await self.bot.db.execute('INSERT OR IGNORE INTO permissions(guild_id,permission,role_id,user_id) VALUES(?,?,?,NULL)',(guild.id,p,role.id))
  for p in ('configuração','aprovação','registro','membros','meta','dashboard','relatórios','cobranças','logs','tickets'):
   await self.bot.db.execute('INSERT OR IGNORE INTO permissions(guild_id,permission,role_id,user_id) VALUES(?,?,NULL,?)',(guild.id,p,settings.super_admin_id))
 async def panel(self,ch,key):
  marker=f'onelov-panel:{key}'
  async for m in ch.history(limit=30):
   if m.author==self.bot.user and marker in (m.content or ''): return
  e=discord.Embed(color=discord.Color.from_rgb(249,215,239)); view=None
  if key=='informacoes': e.title='ONELOV'; e.description='👋 **BEM-VINDO AO CONTROLE DE FARM!**\n\n🤖 Este é um sistema automatizado para facilitar o controle e o registro de Farm.\n\n📸 Para registrar uma entrega, envie uma foto ou print **do seu Farm**.'
  elif key=='entregas_farm': e.title='📦 ONELOV — ENTREGAS DE FARM'; e.description='Registre seu Farm por este painel.\n\n📦 Material: **Farm Completo**\n🔢 Informe a quantidade.\n📸 Envie uma foto ou print **do seu Farm**.\n🟡 A entrega ficará aguardando aprovação.'; view=DeliveryView(self.bot)
  elif key=='entregas': e.title='📋 ONELOV — PAINEL DE ENTREGAS'; e.description='Painel reservado à equipe autorizada.\n\n🟡 Pendentes\n🟢 Aprovadas\n🔴 Reprovadas'
  elif key=='metas': e.title='🎯 ONELOV — METAS'; e.description='🎯 Meta semanal: **2.000 unidades**\n📅 Ciclo: **terça → terça**\n🟢 Somente Farm aprovado contabiliza.'
  elif key=='ranking': e.title='🏆 ONELOV — RANKING'; e.description='Ranking automático baseado em Farm aprovado.\n\n🥇 Semanal\n📆 Mensal\n🏆 Geral\n\n📅 Ranking semanal: terça → terça.'
  elif key=='perfis': e.title='👤 ONELOV — PERFIS'; e.description='🔒 Cada membro consulta **somente o próprio perfil**.\n\nUse `/perfil` para consultar seu perfil. A equipe autorizada pode consultar perfis conforme suas permissões.'
  elif key=='tickets': e.title='🎫 ONELOV — CENTRAL DE SUPORTE'; e.description='Abra um atendimento privado com a equipe autorizada.'; view=TicketView(self.bot)
  else: return
  e.set_footer(text=marker); await ch.send(embed=e,view=view)
 @app_commands.command(name='setup',description='Cria e configura toda a estrutura do OneLov.')
 async def setup_command(self,interaction:discord.Interaction):
  if not interaction.guild: return await interaction.response.send_message('❌ Use este comando em um servidor.',ephemeral=True)
  if not self.supreme(interaction.user): return await interaction.response.send_message('❌ Apenas o ADM Supremo pode executar o /setup.',ephemeral=True)
  me=interaction.guild.me
  if not me or not me.guild_permissions.manage_channels: return await interaction.response.send_message('❌ Preciso da permissão **Gerenciar Canais**.',ephemeral=True)
  await interaction.response.defer(ephemeral=True,thinking=True); guild=interaction.guild
  category=discord.utils.get(guild.categories,name='ONELOV') or await guild.create_category('ONELOV',reason='OneLov /setup')
  staff=await self.role(guild,'OneLov Staff'); admin=await self.role(guild,'OneLov Admin'); channels={k:await self.channel(guild,n,category) for k,n in CHANNELS.items()}
  await self.permissions(guild,category,staff,admin,channels); await self.grant_defaults(guild,staff,admin)
  for key,ch in channels.items():
   if key!='logs': await self.panel(ch,key)
  await self.bot.db.execute('INSERT INTO guild_config(guild_id,weekly_goal,approval_required,ticket_category_id,log_channel_id,cobranca_hour,cobranca_minute,auto_charge) VALUES(?,?,?,?,?,?,?,?) ON CONFLICT(guild_id) DO UPDATE SET weekly_goal=2000,approval_required=1,ticket_category_id=excluded.ticket_category_id,log_channel_id=excluded.log_channel_id',(guild.id,2000,1,category.id,channels['logs'].id,18,0,1))
  await self.bot.ensure_week(guild)
  await interaction.followup.send('✅ **ONELOV CONFIGURADO!**\n\n📁 Categoria e canais verificados/criados.\n🔐 Permissões aplicadas.\n🎯 Meta: **2.000 unidades**.\n📅 Ciclo: **terça → terça**.\n📸 Comprovante obrigatório ativado.\n\n👥 Cargos: **OneLov Staff** e **OneLov Admin**.',ephemeral=True)
async def setup(bot): await bot.add_cog(Setup(bot))
