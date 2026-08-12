# FARM MANAGER

Bot Discord para gestão diária de farm/meta de organizações GTA RP.

## Funcionalidades
- Administrador Supremo permanente via `SUPER_ADMIN_ID`.
- Permissões por cargo ou usuário.
- Tickets individuais, histórico e prevenção de duplicados.
- Entregas dentro do ticket com aprovação/reprovação.
- Meta semanal padrão de 2.000, configurável e sem percentuais.
- **Ciclo semanal do Farm de terça-feira a terça-feira.**
- Ranking, metas e relatórios semanais seguem o ciclo de terça a terça.
- Histórico persistente das semanas anteriores.
- Cobrança automática no início de cada novo ciclo semanal, em horário configurável, e `/cobrar` manual.
- Dashboard, ranking, `/perfil` e `/relatorio`.
- Logs de ações no SQLite.
- SQLite com camada isolada para futura migração PostgreSQL.
- Fuso `America/Sao_Paulo`.

## Comandos
- `/painel` — envia o botão ABRIR TICKET.
- `/entrega quantidade` — registra farm no ticket.
- `/fecharticket` — fecha o ticket sem apagar histórico.
- `/pendentes` — lista entregas pendentes para aprovação.
- `/dashboard` — dashboard e ranking da semana.
- `/perfil [usuario]` — meta, aprovado, restante, situação, tickets e histórico de aprovações/reprovações.
- `/relatorio` — relatório semanal.
- `/config` — meta, aprovação, categoria, canal de logs, horário e cobrança automática.
- `/permissao` — concede uma permissão a cargo/usuário.
- `/permissoes` — lista permissões.
- `/iniciarsemana` — inicializa a semana atual manualmente.
- `/cobrar` — envia cobrança manual nos tickets ativos.

## Período semanal do Farm
O OneLov considera como semana oficial o período **terça-feira 00:00:00 até segunda-feira 23:59:59**, reiniciando automaticamente na terça-feira seguinte.

Exemplo: `11/08/2026 → 17/08/2026`. O novo ciclo começa em `18/08/2026`.

As entregas aprovadas são contabilizadas no ciclo correspondente. Entregas pendentes não entram no ranking até serem aprovadas.

## Permissões
As chaves disponíveis são: `configuração`, `tickets`, `registro`, `aprovação`, `membros`, `meta`, `dashboard`, `relatórios`, `cobranças` e `logs`.
O `SUPER_ADMIN_ID` sempre tem acesso e não pode ser removido por configuração comum.

## Configuração
Copie `.env.example` para `.env` e preencha:
- `DISCORD_TOKEN`: token do bot.
- `DISCORD_CLIENT_ID`: Application ID.
- `DISCORD_GUILD_ID`: ID do servidor para sincronização rápida dos slash commands.
- `SUPER_ADMIN_ID`: seu ID Discord.
- `DATABASE_PATH`: caminho do SQLite.
- `TIMEZONE`: `America/Sao_Paulo`.
- `DEFAULT_WEEKLY_GOAL`: `2000`.

As configurações de meta, aprovação, categoria, logs e cobrança também podem ser alteradas pelo `/config`.

## Instalação Windows
```bat
python --version
copy .env.example .env
iniciar_windows.bat
```

## Instalação Linux/VPS
```bash
python3 --version
cp .env.example .env
chmod +x iniciar_linux.sh
./iniciar_linux.sh
```

Para manter 24/7, use systemd, Docker ou um supervisor de processos. Exemplo systemd:
```ini
[Unit]
Description=FARM MANAGER Discord Bot
After=network.target

[Service]
WorkingDirectory=/opt/Farm_Manager
ExecStart=/usr/bin/python3 /opt/Farm_Manager/bot.py
Restart=always
RestartSec=5
EnvironmentFile=/opt/Farm_Manager/.env

[Install]
WantedBy=multi-user.target
```

## Discord Developer Portal
1. Crie uma Application.
2. Crie o Bot e copie o token.
3. Ative `Server Members Intent` em Privileged Gateway Intents.
4. OAuth2 → URL Generator: marque `bot` e `applications.commands`.
5. Dê ao bot permissões para criar canais, gerenciar permissões, enviar mensagens, incorporar links e usar slash commands.
6. Configure `SUPER_ADMIN_ID` com seu ID Discord.

## Segurança
Nunca coloque o token no código ou no GitHub. `.env` e `data/*.db` são ignorados pelo Git.
Se um token for exposto, revogue-o no Developer Portal imediatamente.

## Arquitetura
`bot.py` contém o ciclo principal e automação. `database.py` contém persistência e migrações SQLite. `cogs/` separa administração, permissões, tickets, farm, dashboard e relatórios.

O histórico das semanas, tickets, entregas e logs fica no banco; iniciar uma nova semana não apaga semanas anteriores.
