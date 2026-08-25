-- ============================================================
-- LDC Insumos — Stored Procedures CRUD por entidade
-- ============================================================

-- ===================== usuarios =====================
CREATE OR ALTER PROCEDURE dbo.usp_usuarios_get_all @skip INT = 0, @limit INT = 100 AS
BEGIN
    SELECT * FROM [dbo].[usuarios] ORDER BY id OFFSET @skip ROWS FETCH NEXT @limit ROWS ONLY;
END
GO

CREATE OR ALTER PROCEDURE dbo.usp_usuarios_get_by_id @id INT AS
BEGIN
    SELECT * FROM [dbo].[usuarios] WHERE id = @id;
END
GO

CREATE OR ALTER PROCEDURE dbo.usp_usuarios_insert
    @nome VARCHAR(100), @email VARCHAR(150), @senha_hash VARCHAR(255),
    @role VARCHAR(20), @rtv_territorio VARCHAR(100) = NULL, @ativo BIT = 1
AS
BEGIN
    INSERT INTO [dbo].[usuarios] (nome, email, senha_hash, role, rtv_territorio, ativo, created_at, updated_at)
    OUTPUT inserted.id
    VALUES (@nome, @email, @senha_hash, @role, @rtv_territorio, @ativo, GETDATE(), GETDATE());
END
GO

CREATE OR ALTER PROCEDURE dbo.usp_usuarios_update
    @id INT, @nome VARCHAR(100), @email VARCHAR(150), @role VARCHAR(20),
    @rtv_territorio VARCHAR(100) = NULL, @ativo BIT = 1
AS
BEGIN
    UPDATE [dbo].[usuarios]
    SET nome = @nome, email = @email, role = @role, rtv_territorio = @rtv_territorio,
        ativo = @ativo, updated_at = GETDATE()
    WHERE id = @id;
END
GO

CREATE OR ALTER PROCEDURE dbo.usp_usuarios_delete @id INT AS
BEGIN
    UPDATE [dbo].[usuarios] SET ativo = 0, updated_at = GETDATE() WHERE id = @id;
END
GO

-- ===================== produtos =====================
CREATE OR ALTER PROCEDURE dbo.usp_produtos_get_all @skip INT = 0, @limit INT = 100 AS
BEGIN
    SELECT * FROM [dbo].[produtos] ORDER BY id OFFSET @skip ROWS FETCH NEXT @limit ROWS ONLY;
END
GO

CREATE OR ALTER PROCEDURE dbo.usp_produtos_get_by_id @id INT AS
BEGIN
    SELECT * FROM [dbo].[produtos] WHERE id = @id;
END
GO

CREATE OR ALTER PROCEDURE dbo.usp_produtos_insert
    @nome_comercial VARCHAR(150), @tipo VARCHAR(20), @classe VARCHAR(80) = NULL,
    @ingrediente_ativo VARCHAR(150) = NULL, @unidade VARCHAR(20), @custo DECIMAL(15,2), @ativo BIT = 1
AS
BEGIN
    INSERT INTO [dbo].[produtos] (nome_comercial, tipo, classe, ingrediente_ativo, unidade, custo, ativo, created_at, updated_at)
    OUTPUT inserted.id
    VALUES (@nome_comercial, @tipo, @classe, @ingrediente_ativo, @unidade, @custo, @ativo, GETDATE(), GETDATE());
END
GO

CREATE OR ALTER PROCEDURE dbo.usp_produtos_update
    @id INT, @nome_comercial VARCHAR(150), @tipo VARCHAR(20), @classe VARCHAR(80) = NULL,
    @ingrediente_ativo VARCHAR(150) = NULL, @unidade VARCHAR(20), @custo DECIMAL(15,2), @ativo BIT = 1
AS
BEGIN
    UPDATE [dbo].[produtos]
    SET nome_comercial = @nome_comercial, tipo = @tipo, classe = @classe,
        ingrediente_ativo = @ingrediente_ativo, unidade = @unidade, custo = @custo,
        ativo = @ativo, updated_at = GETDATE()
    WHERE id = @id;
END
GO

CREATE OR ALTER PROCEDURE dbo.usp_produtos_delete @id INT AS
BEGIN
    UPDATE [dbo].[produtos] SET ativo = 0, updated_at = GETDATE() WHERE id = @id;
END
GO

-- ===================== clientes =====================
CREATE OR ALTER PROCEDURE dbo.usp_clientes_get_all @skip INT = 0, @limit INT = 100 AS
BEGIN
    SELECT * FROM [dbo].[clientes] ORDER BY id OFFSET @skip ROWS FETCH NEXT @limit ROWS ONLY;
END
GO

CREATE OR ALTER PROCEDURE dbo.usp_clientes_get_by_id @id INT AS
BEGIN
    SELECT * FROM [dbo].[clientes] WHERE id = @id;
END
GO

CREATE OR ALTER PROCEDURE dbo.usp_clientes_insert
    @nome VARCHAR(150), @documento VARCHAR(20), @regiao VARCHAR(100),
    @cultura_principal VARCHAR(100) = NULL, @rtv_id INT, @ativo BIT = 1
AS
BEGIN
    INSERT INTO [dbo].[clientes] (nome, documento, regiao, cultura_principal, rtv_id, ativo, created_at, updated_at)
    OUTPUT inserted.id
    VALUES (@nome, @documento, @regiao, @cultura_principal, @rtv_id, @ativo, GETDATE(), GETDATE());
END
GO

CREATE OR ALTER PROCEDURE dbo.usp_clientes_update
    @id INT, @nome VARCHAR(150), @regiao VARCHAR(100), @cultura_principal VARCHAR(100) = NULL,
    @rtv_id INT, @ativo BIT = 1
AS
BEGIN
    UPDATE [dbo].[clientes]
    SET nome = @nome, regiao = @regiao, cultura_principal = @cultura_principal,
        rtv_id = @rtv_id, ativo = @ativo, updated_at = GETDATE()
    WHERE id = @id;
END
GO

CREATE OR ALTER PROCEDURE dbo.usp_clientes_delete @id INT AS
BEGIN
    UPDATE [dbo].[clientes] SET ativo = 0, updated_at = GETDATE() WHERE id = @id;
END
GO

-- ===================== precos_por_janela =====================
CREATE OR ALTER PROCEDURE dbo.usp_precos_por_janela_get_all @skip INT = 0, @limit INT = 100 AS
BEGIN
    SELECT * FROM [dbo].[precos_por_janela] ORDER BY id OFFSET @skip ROWS FETCH NEXT @limit ROWS ONLY;
END
GO

CREATE OR ALTER PROCEDURE dbo.usp_precos_por_janela_get_by_id @id INT AS
BEGIN
    SELECT * FROM [dbo].[precos_por_janela] WHERE id = @id;
END
GO

-- Lookup usado pela Captação de Pedido para precificação automática (RN-004)
CREATE OR ALTER PROCEDURE dbo.usp_precos_por_janela_lookup
    @produto_id INT, @janela_mes INT, @janela_ano INT, @condicao_pagamento VARCHAR(50)
AS
BEGIN
    SELECT TOP 1 * FROM [dbo].[precos_por_janela]
    WHERE produto_id = @produto_id AND janela_mes = @janela_mes AND janela_ano = @janela_ano
      AND condicao_pagamento = @condicao_pagamento
      AND (vigente_ate IS NULL OR vigente_ate >= GETDATE())
    ORDER BY vigente_de DESC;
END
GO

CREATE OR ALTER PROCEDURE dbo.usp_precos_por_janela_insert
    @produto_id INT, @janela_mes INT, @janela_ano INT, @condicao_pagamento VARCHAR(50),
    @preco DECIMAL(15,2), @vigente_de DATE, @vigente_ate DATE = NULL
AS
BEGIN
    INSERT INTO [dbo].[precos_por_janela] (produto_id, janela_mes, janela_ano, condicao_pagamento, preco, vigente_de, vigente_ate, created_at, updated_at)
    OUTPUT inserted.id
    VALUES (@produto_id, @janela_mes, @janela_ano, @condicao_pagamento, @preco, @vigente_de, @vigente_ate, GETDATE(), GETDATE());
END
GO

CREATE OR ALTER PROCEDURE dbo.usp_precos_por_janela_update
    @id INT, @preco DECIMAL(15,2), @vigente_de DATE, @vigente_ate DATE = NULL
AS
BEGIN
    UPDATE [dbo].[precos_por_janela]
    SET preco = @preco, vigente_de = @vigente_de, vigente_ate = @vigente_ate, updated_at = GETDATE()
    WHERE id = @id;
END
GO

CREATE OR ALTER PROCEDURE dbo.usp_precos_por_janela_delete @id INT AS
BEGIN
    DELETE FROM [dbo].[precos_por_janela] WHERE id = @id;
END
GO

-- ===================== pedidos =====================
CREATE OR ALTER PROCEDURE dbo.usp_pedidos_get_all @skip INT = 0, @limit INT = 100 AS
BEGIN
    SELECT * FROM [dbo].[pedidos] ORDER BY id OFFSET @skip ROWS FETCH NEXT @limit ROWS ONLY;
END
GO

CREATE OR ALTER PROCEDURE dbo.usp_pedidos_get_by_id @id INT AS
BEGIN
    SELECT * FROM [dbo].[pedidos] WHERE id = @id;
END
GO

CREATE OR ALTER PROCEDURE dbo.usp_pedidos_insert
    @cliente_id INT, @rtv_id INT, @cultura_safra VARCHAR(100) = NULL, @canal_origem VARCHAR(20),
    @observacoes TEXT = NULL
AS
BEGIN
    INSERT INTO [dbo].[pedidos] (cliente_id, rtv_id, cultura_safra, canal_origem, valor_total, observacoes, status, created_at, updated_at)
    OUTPUT inserted.id
    VALUES (@cliente_id, @rtv_id, @cultura_safra, @canal_origem, 0, @observacoes, 'Rascunho', GETDATE(), GETDATE());
END
GO

CREATE OR ALTER PROCEDURE dbo.usp_pedidos_update
    @id INT, @cultura_safra VARCHAR(100) = NULL, @observacoes TEXT = NULL, @valor_total DECIMAL(15,2) = NULL
AS
BEGIN
    UPDATE [dbo].[pedidos]
    SET cultura_safra = @cultura_safra, observacoes = @observacoes,
        valor_total = ISNULL(@valor_total, valor_total), updated_at = GETDATE()
    WHERE id = @id;
END
GO

-- Transições de status (RN-005, RN-007, RN-009, RN-010)
CREATE OR ALTER PROCEDURE dbo.usp_pedidos_submit @id INT AS
BEGIN
    UPDATE [dbo].[pedidos] SET status = 'Pendente Aprovação', updated_at = GETDATE()
    WHERE id = @id AND status = 'Rascunho';
END
GO

CREATE OR ALTER PROCEDURE dbo.usp_pedidos_approve @id INT, @aprovado_por VARCHAR(100), @comentario TEXT = NULL AS
BEGIN
    UPDATE [dbo].[pedidos]
    SET status = 'Aprovado', aprovado_por = @aprovado_por, aprovado_em = GETDATE(),
        comentario_aprovacao = @comentario, updated_at = GETDATE()
    WHERE id = @id;
END
GO

CREATE OR ALTER PROCEDURE dbo.usp_pedidos_reject @id INT, @aprovado_por VARCHAR(100), @comentario TEXT AS
BEGIN
    UPDATE [dbo].[pedidos]
    SET status = 'Rejeitado', aprovado_por = @aprovado_por, aprovado_em = GETDATE(),
        comentario_aprovacao = @comentario, updated_at = GETDATE()
    WHERE id = @id;
END
GO

CREATE OR ALTER PROCEDURE dbo.usp_pedidos_return @id INT, @aprovado_por VARCHAR(100), @comentario TEXT AS
BEGIN
    -- RN-010: pedido devolvido volta ao status Rascunho
    UPDATE [dbo].[pedidos]
    SET status = 'Rascunho', aprovado_por = @aprovado_por, aprovado_em = GETDATE(),
        comentario_aprovacao = @comentario, updated_at = GETDATE()
    WHERE id = @id;
END
GO

CREATE OR ALTER PROCEDURE dbo.usp_pedidos_delete @id INT AS
BEGIN
    DELETE FROM [dbo].[pedidos] WHERE id = @id AND status = 'Rascunho';
END
GO

-- ===================== pedido_itens =====================
CREATE OR ALTER PROCEDURE dbo.usp_pedido_itens_get_all @skip INT = 0, @limit INT = 100 AS
BEGIN
    SELECT * FROM [dbo].[pedido_itens] ORDER BY id OFFSET @skip ROWS FETCH NEXT @limit ROWS ONLY;
END
GO

CREATE OR ALTER PROCEDURE dbo.usp_pedido_itens_get_by_id @id INT AS
BEGIN
    SELECT * FROM [dbo].[pedido_itens] WHERE id = @id;
END
GO

CREATE OR ALTER PROCEDURE dbo.usp_pedido_itens_insert
    @pedido_id INT, @produto_id INT, @quantidade DECIMAL(15,2), @unidade VARCHAR(20),
    @janela_mes INT, @janela_ano INT, @formato_entrega VARCHAR(50), @local_entrega VARCHAR(150),
    @condicao_pagamento VARCHAR(50), @preco_unitario DECIMAL(15,2)
AS
BEGIN
    -- RN-004: preco_unitario deve vir do lookup usp_precos_por_janela_lookup antes desta chamada
    INSERT INTO [dbo].[pedido_itens]
        (pedido_id, produto_id, quantidade, unidade, janela_mes, janela_ano, formato_entrega, local_entrega,
         condicao_pagamento, preco_unitario, subtotal, created_at, updated_at)
    OUTPUT inserted.id
    VALUES
        (@pedido_id, @produto_id, @quantidade, @unidade, @janela_mes, @janela_ano, @formato_entrega, @local_entrega,
         @condicao_pagamento, @preco_unitario, @quantidade * @preco_unitario, GETDATE(), GETDATE());
END
GO

CREATE OR ALTER PROCEDURE dbo.usp_pedido_itens_update
    @id INT, @quantidade DECIMAL(15,2), @preco_unitario DECIMAL(15,2)
AS
BEGIN
    UPDATE [dbo].[pedido_itens]
    SET quantidade = @quantidade, preco_unitario = @preco_unitario,
        subtotal = @quantidade * @preco_unitario, updated_at = GETDATE()
    WHERE id = @id;
END
GO

CREATE OR ALTER PROCEDURE dbo.usp_pedido_itens_delete @id INT AS
BEGIN
    DELETE FROM [dbo].[pedido_itens] WHERE id = @id;
END
GO

-- ===================== alertas_consistencia =====================
CREATE OR ALTER PROCEDURE dbo.usp_alertas_consistencia_get_all @skip INT = 0, @limit INT = 100 AS
BEGIN
    SELECT * FROM [dbo].[alertas_consistencia] ORDER BY id OFFSET @skip ROWS FETCH NEXT @limit ROWS ONLY;
END
GO

CREATE OR ALTER PROCEDURE dbo.usp_alertas_consistencia_get_by_id @id INT AS
BEGIN
    SELECT * FROM [dbo].[alertas_consistencia] WHERE id = @id;
END
GO

CREATE OR ALTER PROCEDURE dbo.usp_alertas_consistencia_insert
    @pedido_id INT, @tipo VARCHAR(30), @descricao TEXT, @severidade VARCHAR(10)
AS
BEGIN
    INSERT INTO [dbo].[alertas_consistencia] (pedido_id, tipo, descricao, severidade, created_at, updated_at)
    OUTPUT inserted.id
    VALUES (@pedido_id, @tipo, @descricao, @severidade, GETDATE(), GETDATE());
END
GO

CREATE OR ALTER PROCEDURE dbo.usp_alertas_consistencia_update @id INT, @resolvido_por VARCHAR(100) AS
BEGIN
    -- RN-011: registro explícito da decisão do trader sobre o alerta
    UPDATE [dbo].[alertas_consistencia] SET resolvido_por = @resolvido_por, updated_at = GETDATE() WHERE id = @id;
END
GO

CREATE OR ALTER PROCEDURE dbo.usp_alertas_consistencia_delete @id INT AS
BEGIN
    DELETE FROM [dbo].[alertas_consistencia] WHERE id = @id;
END
GO

-- ===================== recomendacoes =====================
CREATE OR ALTER PROCEDURE dbo.usp_recomendacoes_get_all @skip INT = 0, @limit INT = 100 AS
BEGIN
    SELECT * FROM [dbo].[recomendacoes] ORDER BY id OFFSET @skip ROWS FETCH NEXT @limit ROWS ONLY;
END
GO

CREATE OR ALTER PROCEDURE dbo.usp_recomendacoes_get_by_id @id INT AS
BEGIN
    SELECT * FROM [dbo].[recomendacoes] WHERE id = @id;
END
GO

CREATE OR ALTER PROCEDURE dbo.usp_recomendacoes_insert
    @cliente_id INT, @produto_id INT, @motivo VARCHAR(20), @score DECIMAL(8,4)
AS
BEGIN
    -- RN-013: score calculado pelo serviço de recomendação (backend/services), não nesta procedure
    INSERT INTO [dbo].[recomendacoes] (cliente_id, produto_id, motivo, score, aceita, gerada_em, created_at, updated_at)
    OUTPUT inserted.id
    VALUES (@cliente_id, @produto_id, @motivo, @score, 0, GETDATE(), GETDATE(), GETDATE());
END
GO

CREATE OR ALTER PROCEDURE dbo.usp_recomendacoes_update @id INT, @aceita BIT AS
BEGIN
    -- RN-012: aceita=1 somente após ação explícita "adicionar-ao-pedido" do RTV
    UPDATE [dbo].[recomendacoes] SET aceita = @aceita, updated_at = GETDATE() WHERE id = @id;
END
GO

CREATE OR ALTER PROCEDURE dbo.usp_recomendacoes_delete @id INT AS
BEGIN
    DELETE FROM [dbo].[recomendacoes] WHERE id = @id;
END
GO
