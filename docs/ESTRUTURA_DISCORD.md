# OneLov — Estrutura e Permissões do Discord

Este documento registra a estrutura visual e as regras de acesso definidas para o OneLov. **Não altera a implementação Lite do bot**; serve como especificação para a organização do servidor e para futuras evoluções.

## Estrutura recomendada

```text
📁 ONELOV
├── 📌・informações
├── 📊・dashboard
├── 📦・entregas
├── 🎯・metas
├── 🏆・ranking
├── 👤・perfis
├── 🎫・tickets
├── 📑・logs
│
└── ⚙️ ADMINISTRAÇÃO
    ├── 🔐・permissões
    └── ⚙️・configuração
```

## Regra geral

Canais que servem principalmente para consulta devem ficar bloqueados para mensagens de membros. O OneLov publica/atualiza as informações e a equipe autorizada pode administrar quando necessário.

| Canal | ADM Supremo | Admin/Gerente | Supervisor | Membro | Mensagens de membros |
|---|---|---|---|---|---|
| 📌・informações | editar | editar se autorizado | visualizar | visualizar | ❌ |
| 📊・dashboard | visualizar/administrar | visualizar/administrar | visualizar | sem acesso | ❌ |
| 📦・entregas | administrar | administrar | administrar conforme permissão | sem acesso ao canal; usa o formulário/ticket | ❌ |
| 🎯・metas | administrar | administrar conforme permissão | visualizar | visualizar a própria meta | ❌ |
| 🏆・ranking | visualizar/administrar | visualizar | visualizar | visualizar | ❌ |
| 👤・perfis | administrar | visualizar/administrar | visualizar conforme permissão | visualizar o próprio perfil | ❌ |
| 🎫・tickets | acesso total | atender conforme permissão | atender conforme permissão | interagir somente no próprio ticket | ✅ controladas |
| 📑・logs | acesso total | visualizar se autorizado | sem acesso por padrão | sem acesso | ❌ |
| 🔐・permissões | acesso total | sem acesso por padrão | sem acesso | sem acesso | ❌ |
| ⚙️・configuração | acesso total | sem acesso por padrão | sem acesso | sem acesso | ❌ |

## 👑 ADM Supremo

O `SUPER_ADMIN_ID` continua sendo a autoridade máxima. O ADM Supremo tem acesso a todos os canais e pode definir quais cargos ou usuários recebem permissões adicionais.

## 📌・informações

Canal somente para leitura dos membros. Deve conter:

- Boas-vindas e explicação do OneLov.
- Como registrar uma entrega.
- Como consultar a meta.
- Como consultar o ranking e perfil.
- Como abrir um ticket.
- Regras importantes de utilização.
- Status do sistema.

## 📊・dashboard

Canal de consulta. O conteúdo é mantido pelo OneLov e não deve virar canal de conversa.

## 📦・entregas

As entregas devem ser registradas por interação/formulário ou dentro do fluxo de ticket, e não por mensagens soltas no canal. A equipe autorizada trata aprovação e reprovação.

## 🎯・metas, 🏆・ranking e 👤・perfis

São canais de consulta. O membro não precisa escrever neles. O OneLov apresenta os dados e os atualiza conforme as ações aprovadas.

## 🎫・tickets

É a exceção: o membro precisa conseguir interagir, mas somente dentro do ticket criado para ele. Tickets devem ser privados para o membro e para a equipe autorizada.

## 📑・logs

Somente leitura para usuários autorizados. O OneLov registra ações importantes, como aprovações, reprovações, alterações de configuração, permissões e cobranças.

## ⚙️ Administração

A administração deve ser restrita ao ADM Supremo e às pessoas/cargos que ele autorizar explicitamente. Membros comuns não devem sequer visualizar esses canais.

## Objetivo

Manter o servidor limpo, impedir spam nos canais automáticos e separar claramente **consulta**, **interação** e **administração**.
