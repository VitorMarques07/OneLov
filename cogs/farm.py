import discord
from discord.ext import commands
from discord import app_commands
from .common import allowed

class RejectModal(discord.ui.Modal,title='❌ Motivo da reprovação'):
 motivo=discord.ui.TextInput(label='Motivo',style=discord.TextStyle.paragraph,required=True,max_length=300)
 def __init__(self,bot,did): super().__init__(); self.bot=bot; self.did=did
 async def on_submit(self,i): await self.bot.get_cog('Farm').finish_review(i,self.did,'rejected',str(self.motivo.value))
class Review(discord.ui.View):
 def __init__(self,bot,did): super().__init__(timeout=None); self.bot=bot; self.did=did
 @discord.ui.button(label='Aprovar',emoji='🟢',style=discord.ButtonStyle.green)
 async def ok(self,i,b):
  if not await allowed(i,'aprovação'): return await i.response.send_message('❌ Sem permissão.',ephemeral=True)
  await self.bot.get_cog('Farm').finish_review(i,self.did,'approved','')
 @discord.ui.button(label='Reprovar',emoji='🔴',style=discord.ButtonStyle.red)
 async def no(self,i,b):
  if not await allowed(i,'aprovação'): return await i.response.send_message('❌ Sem permissão.',ephemeral=True)
  await i.response.send_modal(RejectModal(self.bot,self.did))
class DeliveryModal(discord.ui.Modal,title='📦 Registrar Entrega'):
 quantidade=discord.ui.TextInput(label='Quantidade',placeholder='Ex.: 500',required=True,max_length=10)
 observacao=discord.ui.TextInput(label='Observação (opcional)',style=discord.TextStyle.paragraph,required=False,max_length=300)
 comprovante=discord.ui.FileUpload(required=True,min_values=1,max_values=1)
 def __init__(self,bot): super().__init__(); self.bot=bot
 async def on_submit(self,i):
  try: quantidade=int(str(self.quantidade.value).replace('.','').replace(',',''))
  except ValueError: return await i.response.send_message('❌ Informe uma quantidade numérica válida.',ephemeral=True)
  files=list(self.comprovante.values)
  if not files: return await i.response.send_message('❌ O comprovante é obrigatório.',ephemeral=True)
  attachment=files[0]
  if attachment.content_type and not attachment.content_type.startswith('image/'): return await i.response.send_message('❌ Envie uma imagem (JPG, PNG, WEBP etc.) como comprovante.',ephemeral=True)
  await self.bot.get_cog('Farm').register_delivery(i,quantidade,str(self.observacao.value or ''),attachment)
class DeliveryView(discord.ui.View):
 def __init__(self,bot): super().__init__(timeout=None); self.bot=bot
 @discord.ui.button(label='FAZER ENTREGA',emoji='📦',style=discord.ButtonStyle.primary,custom_id='onelov:delivery')
 async def register(self,i,b):
  if not await allowed(i,'registro'): return await i.response.send_message('❌ Sem permissão para registrar entrega.',ephemeral=True)
  await i.response.send_modal(DeliveryModal(self.bot))
class Farm(commands.Cog):
 def __init__(self,bot): self.bot=bot; bot.add_view(DeliveryView(bot))
 async def cog_load(self):
  for r in await self.bot.db.all("SELECT id,review_message_id FROM deliveries WHERE status='pending' AND review_message_id IS NOT NULL"):
   try: self.bot.add_view(Review(self.bot,r['id']),message_id=r['review_message_id'])
   except (discord.HTTPException,discord.ClientException): pass
 async def register_delivery(self,i,quantidade,observacao,attachment):
  if quantidade<=0:return await i.response.send_message('❌ Quantidade inválida.',ephemeral=True)
  week=await self.bot.ensure_week(i.guild); now=self.bot.local_now(); cfg=await self.bot.db.one('SELECT * FROM guild_config WHERE guild_id=?',(i.guild_id,)); status='pending' if not cfg or cfg['approval_required'] else 'approved'
  did=await self.bot.db.execute('INSERT INTO deliveries(guild_id,week_id,ticket_id,member_id,quantity,status,registered_by,created_at,attachment_url,attachment_name) VALUES(?,?,?,?,?,?,?,?,?,?)',(i.guild_id,week['id'],None,i.user.id,quantidade,status,i.user.id,now.isoformat(),attachment.url,attachment.filename)); await self.bot.db.log(i.guild_id,i.user.id,'entrega_registrada',f'id={did};qtd={quantidade};arquivo={attachment.filename};obs={observacao}')
  if status=='approved': return await i.response.send_message(f'🟢 **Entrega #{did} aprovada automaticamente.**\n📦 Farm Completo: **{quantidade:,}**'.replace(',','.'),ephemeral=True)
  log_channel_id=cfg['log_channel_id'] if cfg else 0; channel=i.guild.get_channel(log_channel_id) if log_channel_id else None
  if not channel: channel=discord.utils.get(i.guild.text_channels,name='📋・entregas')
  if not channel: return await i.response.send_message(f'📦 Entrega #{did} registrada, mas o painel da equipe não foi encontrado.',ephemeral=True)
  embed=discord.Embed(title=f'📋 ENTREGA #{did}',description=f'👤 Membro: {i.user.mention}\n📦 Material: **Farm Completo**\n🔢 Quantidade: **{quantidade:,}**\n🟡 Status: **Aguardando aprovação**\n📝 Observação: {observacao or "-"}'.replace(',','.'),color=discord.Color.orange()); embed.set_image(url=attachment.url); embed.set_footer(text=f'Comprovante: {attachment.filename}')
  msg=await channel.send(embed=embed,view=Review(self.bot,did)); await self.bot.db.execute('UPDATE deliveries SET review_channel_id=?,review_message_id=? WHERE id=?',(channel.id,msg.id,did)); await i.response.send_message(f'✅ **Entrega #{did} enviada para análise.**\n🟡 Aguarde a aprovação da equipe.',ephemeral=True)
 async def finish_review(self,i,did,status,reason):
  r=await self.bot.db.one('SELECT * FROM deliveries WHERE id=?',(did,))
  if not r or r['status']!='pending': return await i.response.send_message('❌ Essa entrega já foi processada.',ephemeral=True)
  now=self.bot.local_now(); await self.bot.db.execute('UPDATE deliveries SET status=?,reviewed_by=?,reviewed_at=? WHERE id=?',(status,i.user.id,now.isoformat(),did)); await self.bot.db.log(i.guild_id,i.user.id,'entrega_'+status,f'id={did};qtd={r["quantity"]};motivo={reason}')
  text='🟢 **ENTREGA APROVADA**' if status=='approved' else f'🔴 **ENTREGA REPROVADA**\n📝 Motivo: {reason}'
  try: await i.response.edit_message(content=text,view=None)
  except discord.InteractionResponded: pass
  member=i.guild.get_member(r['member_id'])
  if member:
   try: await member.send(f'🤖 **OneLov**\n\n{text}\n📋 Registro: **#{did}**\n📦 Farm Completo: **{r["quantity"]:,}**'.replace(',','.'))
   except discord.HTTPException: pass
 @app_commands.command(name='entrega',description='Registra uma entrega de Farm.')
 async def delivery(self,i,quantidade:int): await i.response.send_message('📦 Use o botão **FAZER ENTREGA** em #📦・entregas-de-farm para anexar o comprovante.',ephemeral=True)
 @app_commands.command(name='pendentes',description='Lista entregas pendentes.')
 async def pending(self,i):
  if not await allowed(i,'aprovação'): return await i.response.send_message('❌ Sem permissão.',ephemeral=True)
  rows=await self.bot.db.all("SELECT * FROM deliveries WHERE guild_id=? AND status='pending' ORDER BY id DESC LIMIT 20",(i.guild_id,)); text='\n'.join(f"#{r['id']} — <@{r['member_id']}> — {r['quantity']:,}".replace(',','.') for r in rows) or 'Nenhuma.'; await i.response.send_message('📦 **PENDENTES**\n'+text,ephemeral=True)
async def setup(bot): await bot.add_cog(Farm(bot))
