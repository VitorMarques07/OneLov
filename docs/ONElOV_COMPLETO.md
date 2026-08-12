# 🤖 OneLov — Visão completa do sistema

## Estrutura de canais

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

## 📌・informações

Central de informações do OneLov.

Conteúdo principal:
- ONELOV
- CONTROLE DE FARM
- Sistema automatizado
- Como registrar uma entrega
- Regras importantes
- Botão 📦 FAZER ENTREGA

O canal é somente leitura para membros.

## 📦・entregas-de-farm

Central para o membro registrar o Farm.

Fluxo:
1. Clicar em 📦 FAZER ENTREGA.
2. Material: somente **Farm Completo**.
3. Informar quantidade.
4. Anexar foto ou print **do seu Farm** — obrigatório.
5. Informar observação — opcional.
6. Conferir os dados.
7. Confirmar o envio.
8. Registro fica 🟡 Aguardando aprovação.

Membros não enviam mensagens comuns no canal.

## 📋・entregas

Painel exclusivo da equipe autorizada para análise.

Cada registro apresenta membro, Farm Completo, quantidade, comprovante, observação e status.

Ações:
- 🔎 Analisar
- ✅ Aprovar
- ❌ Reprovar

Ao reprovar, deve existir um motivo. Aprovação e reprovação são registradas nos logs.

## 🎯・metas

Meta semanal padrão: **2.000 unidades**.

Ciclo: **terça-feira → terça-feira seguinte**.

Somente entregas 🟢 aprovadas contam para a meta.

Exemplo de painel:

```text
🎯 SUA META SEMANAL
📅 11/08 → 18/08
🎯 Meta: 2.000 unidades
📦 Farm aprovado: 1.350 unidades
📉 Restante: 650 unidades
🟡 META EM ANDAMENTO
```

Não utilizar porcentagens.

## 🏆・ranking

Ranking automático baseado somente em entregas aprovadas.

Períodos disponíveis:
- 🥇 Semanal — terça → terça
- 📆 Mensal
- 🏆 Geral

O membro também pode consultar sua própria posição.

Empates podem ser resolvidos pela ordem em que a quantidade foi alcançada.

O canal é somente leitura para membros.

## 👤・perfis

Perfil individual com:
- Nome/membro
- Meta semanal
- Farm aprovado no ciclo
- Posição no ranking
- Total geral
- Histórico de entregas

## 🎫・tickets

Central de atendimento. O canal principal fica sem mensagens comuns.

O membro escolhe o motivo e o OneLov cria um ticket privado para o usuário e a equipe autorizada.

Categorias previstas:
- 📦 Problema com entrega
- 🎯 Problema com meta
- 👤 Problema com perfil
- ❓ Outro

## 📑・logs

Canal restrito para registro de ações importantes, incluindo:
- Entregas aprovadas/reprovadas
- Responsável pela ação
- Alterações administrativas
- Tickets
- Alterações relevantes do sistema

## 🔔 Cobranças

A cobrança considera a meta de **2.000 unidades** e o ciclo terça → terça.

Enquanto o membro estiver abaixo da meta, o OneLov pode enviar mensagens de acompanhamento e cobrança conforme a configuração.

Ao atingir ou ultrapassar 2.000 unidades aprovadas, a cobrança daquele membro no ciclo é encerrada.

Entregas pendentes e reprovadas não entram no cálculo.

## 👑 Administração

O usuário definido como **ADM Supremo** possui controle máximo sobre as configurações.

O acesso administrativo pode ser concedido de forma configurável a cargos ou pessoas específicas.

Configurações previstas:
- Permissões
- Metas
- Farm
- Cobranças
- Ranking
- Tickets
- Logs
- Configurações gerais

## 🔄 Fluxo completo

```text
👤 MEMBRO
   ↓
📦 REGISTRA FARM
   ↓
📸 COMPROVANTE OBRIGATÓRIO
   ↓
🔎 CONFIRMAÇÃO
   ↓
🟡 AGUARDANDO APROVAÇÃO
   ↓
👮 EQUIPE ANALISA
   ├── ✅ APROVA → 📊 CONTABILIZA
   │                  ├── 🎯 META
   │                  ├── 🏆 RANKING
   │                  └── 👤 PERFIL
   │
   └── ❌ REPROVA → NÃO CONTABILIZA

🔔 COBRANÇAS acompanham a meta de 2.000
📅 CICLO: terça → terça
```
