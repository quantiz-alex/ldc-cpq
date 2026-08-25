-- ============================================================
-- LDC Insumos — Views de consulta (JOINs com campos descritivos)
-- ============================================================

CREATE OR ALTER VIEW [dbo].[vw_clientes] AS
SELECT
    c.id, c.nome, c.documento, c.regiao, c.cultura_principal, c.ativo,
    c.rtv_id, u.nome AS rtv_nome, u.rtv_territorio,
    c.created_at, c.updated_at
FROM [dbo].[clientes] c
LEFT JOIN [dbo].[usuarios] u ON u.id = c.rtv_id;
GO

CREATE OR ALTER VIEW [dbo].[vw_precos_por_janela] AS
SELECT
    pj.id, pj.produto_id, p.nome_comercial AS produto_nome, p.tipo AS produto_tipo, p.unidade,
    pj.janela_mes, pj.janela_ano, pj.condicao_pagamento, pj.preco,
    pj.vigente_de, pj.vigente_ate, pj.created_at, pj.updated_at
FROM [dbo].[precos_por_janela] pj
LEFT JOIN [dbo].[produtos] p ON p.id = pj.produto_id;
GO

CREATE OR ALTER VIEW [dbo].[vw_pedidos] AS
SELECT
    ped.id, ped.cliente_id, c.nome AS cliente_nome, c.regiao AS cliente_regiao,
    ped.rtv_id, u.nome AS rtv_nome,
    ped.cultura_safra, ped.canal_origem, ped.valor_total, ped.observacoes,
    ped.status, ped.aprovado_por, ped.aprovado_em, ped.comentario_aprovacao,
    ped.created_at, ped.updated_at
FROM [dbo].[pedidos] ped
LEFT JOIN [dbo].[clientes] c ON c.id = ped.cliente_id
LEFT JOIN [dbo].[usuarios] u ON u.id = ped.rtv_id;
GO

CREATE OR ALTER VIEW [dbo].[vw_pedido_itens] AS
SELECT
    pi.id, pi.pedido_id, ped.status AS pedido_status,
    pi.produto_id, p.nome_comercial AS produto_nome, p.tipo AS produto_tipo,
    pi.quantidade, pi.unidade, pi.janela_mes, pi.janela_ano,
    pi.formato_entrega, pi.local_entrega, pi.condicao_pagamento,
    pi.preco_unitario, pi.subtotal, pi.created_at, pi.updated_at
FROM [dbo].[pedido_itens] pi
LEFT JOIN [dbo].[pedidos] ped ON ped.id = pi.pedido_id
LEFT JOIN [dbo].[produtos] p ON p.id = pi.produto_id;
GO

CREATE OR ALTER VIEW [dbo].[vw_alertas_consistencia] AS
SELECT
    a.id, a.pedido_id, ped.status AS pedido_status, ped.cliente_id, c.nome AS cliente_nome,
    a.tipo, a.descricao, a.severidade, a.resolvido_por, a.created_at, a.updated_at
FROM [dbo].[alertas_consistencia] a
LEFT JOIN [dbo].[pedidos] ped ON ped.id = a.pedido_id
LEFT JOIN [dbo].[clientes] c ON c.id = ped.cliente_id;
GO

CREATE OR ALTER VIEW [dbo].[vw_recomendacoes] AS
SELECT
    r.id, r.cliente_id, c.nome AS cliente_nome, c.regiao AS cliente_regiao,
    r.produto_id, p.nome_comercial AS produto_nome, p.tipo AS produto_tipo,
    r.motivo, r.score, r.aceita, r.gerada_em, r.created_at, r.updated_at
FROM [dbo].[recomendacoes] r
LEFT JOIN [dbo].[clientes] c ON c.id = r.cliente_id
LEFT JOIN [dbo].[produtos] p ON p.id = r.produto_id;
GO

CREATE OR ALTER VIEW [dbo].[vw_produtos] AS
SELECT
    p.id, p.nome_comercial, p.tipo, p.classe, p.ingrediente_ativo, p.unidade,
    p.custo, p.ativo, p.created_at, p.updated_at
FROM [dbo].[produtos] p;
GO

CREATE OR ALTER VIEW [dbo].[vw_usuarios] AS
SELECT
    u.id, u.nome, u.email, u.role, u.rtv_territorio, u.ativo,
    u.created_at, u.updated_at
FROM [dbo].[usuarios] u;
GO
