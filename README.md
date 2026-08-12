# FARM MANAGER

Bot Discord profissional para gestão de farm/meta de organizações de GTA RP.

## Stack
- Python 3.11+
- discord.py 2.5+
- SQLite com camada preparada para futura migração para PostgreSQL
- python-dotenv
- Fuso horário: America/Sao_Paulo

## Recursos
- Administrador Supremo
- Permissões configuráveis por cargo/usuário
- Tickets de farm
- Entregas com aprovação/reprovação
- Meta semanal sem percentuais
- Dashboard e ranking
- Relatório semanal
- Histórico e logs
- .env para segredos

## Instalação
1. Instale Python 3.11+.
2. Copie `.env.example` para `.env`.
3. Preencha o token, Client ID, Guild ID e ID do Administrador Supremo.
4. Execute `iniciar_windows.bat` no Windows ou `./iniciar_linux.sh` no Linux.

## Discord Developer Portal
Crie uma Application, adicione um Bot, copie o token e habilite os intents necessários. Em OAuth2 > URL Generator, marque `bot` e `applications.commands`.

## Segurança
Nunca publique `.env` ou o token do bot. O `.gitignore` já ignora `.env` e o banco local.
