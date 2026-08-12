import discord
from discord.ext import commands
from discord import app_commands
from config import settings
from .tickets import TicketView
from .farm import DeliveryView

CHANNELS = {
    'informacoes': '📌・informações',
    'entregas_farm': '📦・entregas-de-farm',
    'entregas': '📋・entregas',
    'metas': '🎯・metas',
    'ranking': '🏆・ranking',
    'perfis': '👤・perfis',
    'tickets': '🎫・tickets',
    'logs': '📑・logs',
}

class Setup(commands.Cog):
    def __init__(self, bot): self.bot = bot

    def supreme(self, member):
        return member.id == settings.super_admin_id or member.id == member.guild.owner_id

    async def role(self, guild, name):
        role = discord.utils.get(guild.roles, name=name)
        return role or await guild.create_role(name=name, reason='OneLov /setup')

    async def channel(self, guild, name, category):
        ch = discord.utils.get(guild.text_channels, name=name)
        if ch:
            if ch.category_id != category.id: await ch.edit(category=category, reason='OneLov /setup')
            return ch
        return await guild.create_text_channel(name, category=category, reason='OneLov /setup')

    async def permissions(self, guild, category, staff, admin, channels):
        everyone = guild.default_role
        bot = guild.me
        base = {
            everyone: discord.PermissionOverwrite(view_channel=True, send_messages=False, read_message_history=True),
            staff: discord.PermissionOverwrite(view_channel=True, send_messages=True, read_message_history=True),
            admin: discord.PermissionOverwrite(view_channel=True, send_messages=True, manage_messages=True, manage_channels=True, read_message_history=True),
        }
        if bot: base[bot] = discord.PermissionOverwrite(view_channel=True, send_messages=True, manage_messages=True, manage_channels=True, embed_links=True, attach_files=True, read_message_history=True)
        await category.edit(overwrites=base, reason='OneLov /setup')
        for key, ch in channels.items():
            ow = dict(base)
            if key in ('entregas', 'logs'):
                ow[everyone] = discord.PermissionOverwrite(view_channel=False)
            if key == 'logs':
                ow[staff] = discord.PermissionOverwrite(view_channel=True, send_messages=False, read_message_history=True)
            await ch.edit(overwrites=ow, reason='OneLov /setup')

    async def panel(self, ch, key):
        marker = f'onelov-panel:{key}'
        async for m in ch.history(limit=20):
            if m.author == self.bot.user and marker in (m.content or ''): return
        embed = discord.Embed(color=discord.Color.from_rgb(249, 215, 239))
        view = None
        if key == 'informacoes':
            embed.title = 'ONELOV — CONTROLE DE FARM'
            embed.description = '👋 **BEM-VINDO AO CONTROLE DE FARM!**\n\n🤖 Este é um sistema automatizado para facilitar o controle e o registro de Farm.\n\n📸 Para registrar uma entrega, será necessário enviar uma foto ou print **do seu Farm**.'
        elif key == 'entregas_farm':
            embed.title = '📦 ONELOV — ENTREGAS DE FARM'
            embed.description = 'Registre seu Farm por este painel.\n\n📦 Material: **Farm Completo**\n🔢 Informe a quantidade.\n📸 Envie uma foto ou print **do seu Farm**.\n🟡 A entrega ficará aguardando aprovação.'
            view = DeliveryView(self.bot)
        elif key == 'entregas':
            embed.title = '📋 ONELOV — PAINEL DE ENTREGAS'
            embed.description = 'Painel reservado à equipe autorizada.\n\n🟡 Pendentes\n🟢 Aprovadas\n🔴 Reprovadas'
        elif key == 'metas':
            embed.title = '🎯 ONELOV — METAS'
            embed.description = '🎯 Meta semanal: **2.000 unidades**\n📅 Ciclo: **terça → terça**\n🟢 Somente Farm aprovado contabiliza.'
        elif key == 'ranking':
            embed.title = '🏆 ONELOV — RANKING'
            embed.description = 'Ranking automático baseado em Farm aprovado.\n\n🥇 Semanal\n📆 Mensal\n🏆 Geral\n\n📅 Ranking semanal: terça → terça.'
        elif key == 'perfis':
            embed.title = '👤 ONELOV — PERFIS'
            embed.description = '🔒 Cada membro consulta **somente o próprio perfil**.\n\nA equipe autorizada pode consultar perfis conforme suas permissões.'
        elif key == 'tickets':
            embed.title = '🎫 ONELOV — CENTRAL DE SUPORTE'
            embed.description = 'Abra um atendimento privado com a equipe autorizada.'
            view = TicketView(self.bot)
        else: return
        embed.set_footer(text=marker)
        await ch.send(embed=embed, view=view)

    @app_commands.command(name='setup', description='Cria e configura toda a estrutura do OneLov.')
    async def setup_command(self, interaction: discord.Interaction):
        if not interaction.guild: return await interaction.response.send_message('❌ Use este comando em um servidor.', ephemeral=True)
        if not self.supreme(interaction.user): return await interaction.response.send_message('❌ Apenas o ADM Supremo pode executar o /setup.', ephemeral=True)
        if not interaction.guild.me.guild_permissions.manage_channels: return await interaction.response.send_message('❌ Preciso da permissão **Gerenciar Canais**.', ephemeral=True)
        await interaction.response.defer(ephemeral=True, thinking=True)
        guild = interaction.guild
        category = discord.utils.get(guild.categories, name='ONELOV') or await guild.create_category('ONELOV', reason='OneLov /setup')
        staff = await self.role(guild, 'OneLov Staff')
        admin = await self.role(guild, 'OneLov Admin')
        channels = {k: await self.channel(guild, n, category) for k, n in CHANNELS.items()}
        await self.permissions(guild, category, staff, admin, channels)
        for key, ch in channels.items():
            if key != 'logs': await self.panel(ch, key)
        await self.bot.db.execute('INSERT OR IGNORE INTO guild_config(guild_id,weekly_goal,approval_required,ticket_category_id,log_channel_id,cobranca_hour,cobranca_minute,auto_charge) VALUES(?,?,?,?,?,?,?,?)', (guild.id, 2000, 1, category.id, channels['logs'].id, 18, 0, 1))
        await self.bot.ensure_week(guild)
        await interaction.followup.send('✅ **ONELOV CONFIGURADO!**\n\n📁 Categoria e canais verificados/criados.\n🔐 Permissões aplicadas.\n🎯 Meta: **2.000 unidades**.\n📅 Ciclo: **terça → terça**.\n\n👥 Cargos criados: **OneLov Staff** e **OneLov Admin**.', ephemeral=True)

async def setup(bot): await bot.add_cog(Setup(bot))
