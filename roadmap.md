# LDC Insumos — Plataforma Comercial (CPQ Inteligente)

## Descrição
Plataforma comercial que digitaliza e automatiza o processo de captação, configuração, precificação e cotação (CPQ) de pedidos de defensivos e fertilizantes da LDC Insumos. O sistema recebe demandas que hoje chegam de forma dispersa (WhatsApp, e-mail, texto e imagem), estrutura o pedido em um formulário padronizado e aplica análises automáticas de consistência antes que o pedido siga para o trader.
O problema resolvido: hoje o trader gasta tempo fazendo triagem manual de pedidos que chegam sem padrão, avaliando caso a caso se o pedido faz sentido (produto atípico para o cliente, volumetria fora do padrão histórico, condições comerciais inconsistentes). O sistema torna esse filtro proativo e sistemático, e ainda recomenda produtos com base no histórico e na sazonalidade — como uma cesta de compras.
Usuários: RTVs e a equipe comercial habilitada a vender (que registram os pedidos), traders (que validam e aprovam), e gestores comerciais (que acompanham o desempenho da carteira).

## Stack Tecnológico
<!-- SEÇÃO FIXA — NÃO ALTERAR. O pipeline não suporta outras tecnologias. -->
- **Frontend**: Dash 2.14+ · Dash Bootstrap Components · Dash AG Grid · Plotly · Pandas/NumPy
- **Backend**: FastAPI · SQLAlchemy · Pydantic v2 · JWT (python-jose + bcrypt)
- **Banco**: SQL Server / Microsoft Fabric (SQLite em dev)

---

## Perfis de Acesso
<!-- Roles padrão do pipeline — ajustar nomes/permissões conforme o cliente -->
- **admin**: acesso total — gerenciar usuários, configurações, catálogo de produtos e todos os módulos
- **trader**: visualizar tudo, avaliar pedidos, validar/questionar/aprovar/rejeitar demandas, precificar e liberar cotações
- **rtv**: criar e editar pedidos, configurar itens e condições comerciais, enviar para validação do trader — não aprova nem exclui pedidos de terceiros

---

## Módulos

### Dashboard Comercial
**Prioridade**: high
**Tipo de tela**: dashboard
**Ícone Bootstrap**: speedometer2
**Descrição**: Visão consolidada da operação comercial de insumos — volume de pedidos captados, receita, mix defensivos × fertilizantes, status da fila de validação e desempenho por RTV/região. Apoia o gestor comercial e o trader a enxergar gargalos e priorizar a triagem.
**Participa de workflow**: Workflow Principal (visão de acompanhamento)

**Componentes visuais:**
- **KPIs:** Pedidos captados no mês, Receita acumulada (R$), Ticket médio (R$), Pedidos pendentes de validação, Tempo médio de triagem do trader, % de pedidos com alerta de inconsistência
- **Gráfico principal:** line — evolução de receita e volume de pedidos por semana, com quebra por linha (defensivos × fertilizantes)
- **Gráfico secundário (opcional):** bar — top RTVs por receita captada no período
- **Grid/Tabela:** últimos pedidos captados — cliente, RTV, valor total, mix de produtos, canal de origem (WhatsApp/e-mail/manual), status, flag de alerta
- **Filtros:** data_pedido (date_range), rtv (select), regiao (select), linha_produto (select: Defensivos/Fertilizantes), status (select: Rascunho/Pendente/Validado/Rejeitado)

**Funcionalidades:**
- [F-001] Painel de acompanhamento comercial — consolida KPIs e gráficos com atualização por filtro; permite drill-down do gráfico para a lista de pedidos correspondente
  - Ações disponíveis: [visualizar, exportar-excel, drill-down]
- [F-002] Monitor de fila de triagem — destaca pedidos parados há mais tempo e pedidos com alerta de inconsistência, para priorização do trader
  - Ações disponíveis: [visualizar, drill-down]

**Regras de negócio:**
- [RN-001]: KPIs e gráficos respeitam o escopo do usuário — RTV vê apenas sua própria carteira; trader e gestor veem toda a região sob sua responsabilidade
- [RN-002]: Pedido só entra na contagem de receita após validação do trader

**Acesso por role:**
- admin: full
- trader: [visualizar, exportar-excel, drill-down]
- rtv: [visualizar] (apenas própria carteira)

---

### Captação de Pedido (CPQ)
**Prioridade**: high
**Tipo de tela**: mixed
**Ícone Bootstrap**: cart-plus
**Descrição**: Coração do sistema. Tela onde o RTV registra o pedido do cliente — seleciona o cliente, adiciona os produtos (defensivos e fertilizantes) e preenche as condições comerciais obrigatórias (formato de entrega, prazo e local de entrega, prazo de pagamento, janela de entrega por parcela). O preço é calculado automaticamente em função do produto, da janela de entrega e das condições. Inclui captura assistida a partir de mensagens recebidas (texto/imagem/e-mail) para pré-preencher o pedido.
**Participa de workflow**: Workflow Principal (step: captação → validação)

**Componentes visuais:**
- **Formulário de cabeçalho:** cliente (select com busca), rtv (auto), cultura/safra (select), observações (text)
- **Captura assistida (modal):** colar texto do WhatsApp/e-mail ou anexar imagem → o sistema extrai itens e sugere o preenchimento (produto, quantidade, unidade) para o RTV revisar antes de confirmar
- **Grid de itens (editável):** produto (select), quantidade, unidade, janela de entrega (mês/ano), formato de entrega (select), preço unitário (calculado), subtotal
- **Bloco de condições comerciais:** prazo de pagamento (select), local de entrega (select), condição logística/incoterm interno (select), permite parcelar a entrega de um mesmo item em múltiplas janelas (ex: 80 un. em janeiro, 20 un. em fevereiro)
- **Painel de consistência:** exibe em tempo real os alertas de inconsistência do pedido (produto atípico, volumetria fora do padrão, condição comercial divergente) antes do envio
- **Painel de recomendação:** sugestões de produtos complementares (cross-sell) com base no histórico do cliente e sazonalidade

**Funcionalidades:**
- [F-003] Registrar pedido manual — preencher cabeçalho, itens e condições comerciais e enviar para validação
  - Ações: [criar, editar, submit_approval]
- [F-004] Captura assistida por mensagem — importar demanda de texto/imagem/e-mail e converter em rascunho de pedido para revisão
  - Ações: [importar-mensagem, criar]
- [F-005] Precificação automática por janela — recalcula o preço unitário conforme a janela de entrega escolhida (ex: entrega em janeiro tem preço diferente de fevereiro) e as condições comerciais
  - Ações: [visualizar]
- [F-006] Entrega parcelada por item — dividir a quantidade de um item em múltiplas janelas de entrega, cada uma com seu preço
  - Ações: [criar, editar]

**Regras de negócio:**
- [RN-003]: Campos obrigatórios para envio — cliente, ao menos 1 item, quantidade, janela de entrega, formato de entrega, prazo de pagamento e local de entrega. Pedido incompleto não pode ser enviado para validação
- [RN-004]: O preço unitário é sempre função de produto + janela de entrega + condição comercial; não é possível editar o preço manualmente sem permissão específica
- [RN-005]: A captura assistida nunca cria pedido diretamente — sempre gera rascunho que exige revisão e confirmação humana do RTV
- [RN-006]: A soma das quantidades parceladas por janela deve ser igual à quantidade total do item

**Acesso por role:**
- admin: full
- trader: [visualizar, editar, precificar]
- rtv: [criar, editar, importar-mensagem, submit_approval]

---

### Fila de Validação do Trader
**Prioridade**: high
**Tipo de tela**: approval_queue
**Ícone Bootstrap**: check2-circle
**Descrição**: Fila onde o trader avalia os pedidos enviados pelos RTVs. Cada pedido chega com os alertas de consistência já sinalizados (produto atípico, volumetria fora do padrão, condição divergente), permitindo que o trader aprove, rejeite ou devolva com questionamento ao RTV. Substitui a triagem manual e dispersa feita hoje.
**Participa de workflow**: Workflow Principal (step: validação → cotação/dashboard)

**Componentes visuais:**
- **KPIs:** Pendentes, Aprovados hoje, Rejeitados/Devolvidos hoje, Tempo médio de validação
- **Grid/Tabela:** pedidos pendentes — cliente, RTV, valor total, mix, canal de origem, alertas (badges), enviado em, status
- **Filtros:** status (select: Pendente/Aprovado/Rejeitado/Devolvido), rtv (select), com_alerta (select: Sim/Não), data de envio (date_range)
- **Painel de detalhe do pedido:** itens, condições comerciais, histórico do cliente para o produto em questão (para embasar o julgamento) e os motivos dos alertas

**Funcionalidades:**
- [F-007] Aprovar pedido — validar e liberar o pedido para cotação/efetivação, com comentário opcional
  - Ações: [approve]
- [F-008] Rejeitar pedido — recusar com comentário obrigatório
  - Ações: [reject]
- [F-009] Devolver com questionamento — devolver ao RTV pedindo confirmação/ajuste (ex: "cliente nunca comprou este defensivo, confirmar"), com comentário obrigatório
  - Ações: [return_to_author]
- [F-010] Consultar histórico de validações — auditar pedidos já avaliados
  - Ações: [visualizar, exportar-excel]

**Regras de negócio:**
- [RN-007]: Somente trader e admin podem aprovar, rejeitar ou devolver pedidos
- [RN-008]: Rejeição e devolução exigem comentário
- [RN-009]: RTV não pode aprovar seus próprios pedidos
- [RN-010]: Pedido devolvido volta ao status Rascunho para edição do RTV e reenvio
- [RN-011]: Pedidos com alerta de inconsistência não são bloqueados, mas exigem que o trader registre a decisão explicitamente

**Acesso por role:**
- admin: full
- trader: [approve, reject, return_to_author, visualizar, exportar-excel]
- rtv: [visualizar] (apenas próprios pedidos)

---

### Motor de Recomendação (Cross-sell)
**Prioridade**: medium
**Tipo de tela**: mixed
**Ícone Bootstrap**: stars
**Descrição**: Módulo proativo que sugere produtos ao RTV com base no comportamento de compra do cliente (cesta de compras), sazonalidade da cultura/safra e mix típico da região. Complementa a triagem reativa da fila de validação com uma abordagem de recomendação, ajudando o RTV a ofertar defensivos e fertilizantes complementares.
**Participa de workflow**: Workflow Principal (apoio na captação)

**Componentes visuais:**
- **Filtros:** cliente (select), cultura/safra (select), regiao (select), linha_produto (select)
- **KPIs:** Produtos recomendados aceitos (%), Receita incremental estimada por recomendação, Cobertura da carteira com recomendação ativa
- **Grid/Tabela:** recomendações por cliente — produto sugerido, motivo (histórico/sazonalidade/mix regional), score de afinidade, comprado antes (Sim/Não)
- **Gráfico:** bar — produtos mais recomendados no período e taxa de aceitação

**Funcionalidades:**
- [F-011] Recomendações por cliente — gerar lista de produtos sugeridos com justificativa e score, com opção de enviar direto para a captação de pedido
  - Ações: [visualizar, adicionar-ao-pedido, exportar-excel]
- [F-012] Análise de sazonalidade — mostrar a janela típica de compra de cada produto por cultura para orientar o timing da oferta
  - Ações: [visualizar]

**Regras de negócio:**
- [RN-012]: Recomendações são sugestões e nunca criam pedido automaticamente
- [RN-013]: O score considera recência, frequência e volume histórico do cliente, além da sazonalidade da cultura
- [RN-014]: RTV só vê recomendações dos clientes de sua carteira

**Acesso por role:**
- admin: full
- trader: [visualizar, exportar-excel]
- rtv: [visualizar, adicionar-ao-pedido]

---

### Relatórios Comerciais
**Prioridade**: medium
**Tipo de tela**: report
**Ícone Bootstrap**: file-earmark-bar-graph
**Descrição**: Relatórios exportáveis de pedidos, receita, mix de produtos, desempenho de RTVs e taxa de aprovação/rejeição, para apoiar reuniões comerciais e prestação de contas.
**Participa de workflow**: Workflow Secundário (análise)

**Componentes visuais:**
- **Filtros:** periodo (date_range), rtv (select), regiao (select), cliente (select), linha_produto (select)
- **Gráfico:** line/bar — receita e volume por período, por linha e por RTV
- **Grid/Tabela exportável:** pedido, cliente, RTV, produtos, valor, condição comercial, status, tempo de ciclo (captação → validação)

**Funcionalidades:**
- [F-013] Relatório de pedidos e receita — filtrar, visualizar e exportar
  - Ações: [visualizar, exportar-excel, exportar-pdf]
- [F-014] Relatório de eficiência de triagem — tempo de ciclo, taxa de aprovação/rejeição/devolução e incidência de alertas
  - Ações: [visualizar, exportar-excel]

**Regras de negócio:**
- [RN-015]: Relatórios respeitam o escopo de carteira/região do usuário

**Acesso por role:**
- admin: full
- trader: [gerar, exportar]
- rtv: [gerar, exportar] (apenas própria carteira)

---

### Administração
**Prioridade**: low
**Tipo de tela**: grid
**Ícone Bootstrap**: people
**Descrição**: Controle de usuários do sistema e do catálogo de produtos/preços.

**Componentes visuais:**
- **Grid/Tabela:** lista de usuários — nome, email, role, RTV vinculado, ativo
- **Filtros:** role (select), ativo (select: Sim/Não)
- **Formulário:** nome (text), email (text), role (select), RTV/território vinculado (select), senha temporária (text)

**Funcionalidades:**
- [F-015] Gestão de usuários — criar, editar e desativar usuários
  - Ações: [criar, editar, desativar]
- [F-016] Manutenção de catálogo (produtos, preços por janela e políticas comerciais)
  - Ações: [criar, editar, importar-csv]

**Regras de negócio:**
- [RN-016]: Somente admin pode criar ou desativar usuários e editar o catálogo/preços
- [RN-017]: Email deve ser único no sistema

**Acesso por role:**
- admin: full

---

## Workflows e Jornadas de Usuário

### Workflow Principal: Captação e Validação de Pedido
**Categoria**: implementação
**Descrição**: Jornada completa do pedido, da entrada da demanda (canal informal) até a liberação pelo trader, com apoio de recomendação e de análise automática de consistência.
**Roles**: [rtv, trader, admin]

**Steps:**
1. **Captação de Pedido (CPQ)** → RTV recebe a demanda (WhatsApp/e-mail/imagem/manual), usa a captura assistida para pré-preencher, seleciona cliente e produtos, define condições comerciais e janelas de entrega. O Motor de Recomendação sugere itens complementares.
   - Dados fornecidos: cliente_id, itens (produto, quantidade, janela, formato entrega), condicoes_comerciais
   - Próximo passo: Fila de Validação do Trader

2. **Fila de Validação do Trader** → Trader recebe o pedido com os alertas de consistência sinalizados e o histórico do cliente à vista. Decide aprovar, rejeitar ou devolver com questionamento.
   - Dados recebidos: pedido_id, itens, condicoes_comerciais, alertas_consistencia, historico_cliente
   - Dados fornecidos: decisao (aprovado/rejeitado/devolvido), comentario
   - Próximo passo: Dashboard Comercial (se aprovado) ou retorno à Captação (se devolvido — condição: RN-010)

3. **Dashboard Comercial** → Pedido aprovado passa a compor a receita e os indicadores; trader e gestor acompanham a carteira.
   - Dados recebidos: pedido_aprovado
   - Ações finais: visualizar desempenho, priorizar próximos pedidos, gerar relatórios

**Exemplo de fluxo comum:**
```
Demanda (WhatsApp/e-mail/imagem) → Captura Assistida → Captação de Pedido (itens + condições + janelas) →
Recomendação de complementos → Envio para Validação → Fila do Trader → Aprovar/Devolver/Rejeitar →
Dashboard (reflete receita) 
```

### Workflow Secundário: Análise e Recomendação
**Categoria**: análise
**Descrição**: Uso proativo dos dados históricos para orientar a oferta e acompanhar desempenho — recomendação por cliente/sazonalidade e relatórios comerciais.
**Roles**: [rtv, trader, admin]

**Steps:**
1. Motor de Recomendação gera sugestões por cliente e sazonalidade
2. RTV incorpora sugestões na captação; gestor acompanha aceitação e receita incremental nos Relatórios

**Notas sobre Workflows:**
- Workflows são gerados automaticamente pelo sistema baseado nos módulos definidos
- Captação + validação (fila do trader) formam o workflow principal automático
- Dashboards + relatórios criam o workflow de análise
- Dados fluem automaticamente entre telas do mesmo workflow (o pedido carrega itens e condições da captação até a validação)

---

## Entidades de Dados

### Cliente
**Descrição**: Produtor rural ou revenda atendido pela LDC Insumos; base para histórico de compras, recomendação e análise de consistência
**Campos principais**: nome varchar(150), documento varchar(20), regiao varchar(100), cultura_principal varchar(100), rtv_responsavel varchar(100), ativo bit
**Relacionamentos**: tem muitos Pedidos, atendido por um RTV (Usuarios)
**Módulo**: Captação de Pedido, Motor de Recomendação

### Produto
**Descrição**: SKU de defensivo ou fertilizante do catálogo da LDC (aprox. 90 SKUs); base para itens de pedido e precificação
**Campos principais**: nome_comercial varchar(150), tipo enum(Defensivo/Fertilizante), classe varchar(80), ingrediente_ativo varchar(150), unidade varchar(20), custo decimal(15,2), ativo bit
**Relacionamentos**: aparece em muitos PedidoItem, tem muitos PrecoPorJanela
**Módulo**: Captação de Pedido, Administração

### PrecoPorJanela
**Descrição**: Preço vigente de um produto para uma janela de entrega específica (o preço muda conforme o mês de entrega — ex: janeiro × fevereiro)
**Campos principais**: produto_id int, janela_mes int, janela_ano int, condicao_pagamento varchar(50), preco decimal(15,2), vigente_de date, vigente_ate date
**Relacionamentos**: pertence a Produto
**Módulo**: Captação de Pedido (precificação automática), Administração

### Pedido
<!-- Entidade com fluxo de aprovação -->
**Descrição**: Pedido comercial captado pelo RTV, submetido à validação do trader
**Campos principais**: cliente_id int, rtv_id int, cultura_safra varchar(100), canal_origem enum(WhatsApp/Email/Imagem/Manual), valor_total decimal(15,2), observacoes text, e os campos de aprovação abaixo são OBRIGATÓRIOS para o fluxo:
  - status enum(Rascunho/Pendente Aprovação/Aprovado/Rejeitado/Devolvido) default Rascunho
  - aprovado_por varchar(100) nullable
  - aprovado_em datetime2 nullable
  - comentario_aprovacao text nullable
**Relacionamentos**: pertence a Cliente, pertence a Usuarios (rtv_id), tem muitos PedidoItem, tem muitos AlertaConsistencia
**Módulo**: Captação de Pedido (+ Fila de Validação do Trader)

### PedidoItem
**Descrição**: Item do pedido, incluindo o parcelamento da entrega por janela (uma linha por janela de entrega do mesmo produto)
**Campos principais**: pedido_id int, produto_id int, quantidade decimal(15,2), unidade varchar(20), janela_mes int, janela_ano int, formato_entrega varchar(50), local_entrega varchar(150), preco_unitario decimal(15,2), subtotal decimal(15,2)
**Relacionamentos**: pertence a Pedido, referencia Produto
**Módulo**: Captação de Pedido

### AlertaConsistencia
**Descrição**: Registro dos alertas gerados automaticamente na análise do pedido (produto atípico para o cliente, volumetria fora do padrão histórico, condição comercial divergente)
**Campos principais**: pedido_id int, tipo enum(ProdutoAtipico/VolumetriaAtipica/CondicaoDivergente), descricao text, severidade enum(Baixa/Media/Alta), resolvido_por varchar(100) nullable
**Relacionamentos**: pertence a Pedido
**Módulo**: Captação de Pedido, Fila de Validação do Trader

### Recomendacao
**Descrição**: Sugestão de produto gerada para um cliente com base em histórico e sazonalidade
**Campos principais**: cliente_id int, produto_id int, motivo enum(Historico/Sazonalidade/MixRegional), score decimal(8,4), aceita bit default 0, gerada_em datetime2
**Relacionamentos**: pertence a Cliente, referencia Produto
**Módulo**: Motor de Recomendação

### Usuarios
**Descrição**: Usuários do sistema com autenticação JWT
**Campos principais**: nome varchar(100), email varchar(150) único, senha_hash varchar(255), role enum(admin/trader/rtv), rtv_territorio varchar(100) nullable, ativo bit
**Relacionamentos**: um Usuario (rtv) atende muitos Clientes e cria muitos Pedidos
**Módulo**: Administração

---

## Branding
- **Cor primária**: #1045C8
- **Logo**: assets/logo.png
- **Nome na sidebar**: LDC Insumos

---

## Integrações
- **Microsoft Dynamics CRM**: API REST — sincronização de clientes e carteira dos RTVs (o cliente já utiliza CRM da Microsoft hoje). No mockup, simulada com dados de exemplo.
- **SAP**: Database/API — origem de catálogo de produtos, preços e efetivação do pedido aprovado. No mockup, simulada.
- **Canais de entrada de demanda (WhatsApp/E-mail)**: Arquivo/API — captura de mensagens para a funcionalidade de captura assistida. No mockup, entrada manual de texto/imagem para demonstração.

---

## Requisitos Não-Funcionais
- **Performance**: Consultas < 3s com volume médio de dados (aprox. 90 SKUs, dezenas de RTVs, milhares de pedidos/safra)
- **Segurança**: JWT com expiração de 8h, senhas com bcrypt, HTTPS em produção
- **Escalabilidade**: Suporte a ~250 usuários simultâneos (33 RTVs + mais de 200 vendedores habilitados)
- **Disponibilidade**: disponível em horário comercial estendido, 6h–20h (janela de plantio/safra)
