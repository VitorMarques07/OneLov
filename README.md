# ONELOV

Bot Discord para controle automatizado de Farm.

## Funcionalidades
- ADM Supremo permanente via `SUPER_ADMIN_ID`.
- `/setup` cria/verifica a categoria, canais, cargos, permissões e painéis do OneLov.
- `/setup` é idempotente e não duplica a estrutura existente.
- Permissões por cargo ou usuário.
- 📦 Entrega com material fixo **Farm Completo**, quantidade e **foto/print do seu Farm obrigatória**.
- Entregas ficam pendentes para análise e podem ser aprovadas ou reprovadas com motivo.
- Somente entregas aprovadas contam para meta e ranking.
- Meta semanal padrão de **2.000 unidades**, sem percentuais.
- Ciclo semanal do Farm de **terça-feira a terça-feira seguinte**.
- Ranking semanal, mensal e geral.
- Perfil individual privado: membro consulta somente o próprio perfil; equipe autorizada pode consultar outros.
- Tickets de suporte separados do fluxo de entrega.
- Cobrança automática no último dia do ciclo (segunda-feira), além de `/cobrar` manual.
- Logs de ações no SQLite.
- Comprovantes e registros de revisão persistidos no banco.
- Fuso padrão `America/Sao_Paulo`.

## Canais criados pelo `/setup`
```text
📁 ONELOV
├── 📌・informações
├── 📦・entregas-de-farm
├── 📋・entregas
├── 🎯・metas
├── 🏆・ranking
├── 👤・perfis
├── 🎫・tickets
└── 📑・logs
```

## Dependência importante
O formulário de entrega usa o componente nativo de upload de arquivos do Discord; por isso o projeto requer `discord.py>=2.7`.

## Configuração
Copie `.env.example` para `.env` e preencha pelo menos `DISCORD_TOKEN` e `SUPER_ADMIN_ID`.

O bot precisa de permissões para gerenciar canais, criar cargos e enviar/gerenciar mensagens nos canais do OneLov.
