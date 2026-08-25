-- ============================================================
-- LDC Insumos — Plataforma Comercial (CPQ Inteligente)
-- Schema SQL Server 2019+ / Microsoft Fabric Warehouse
-- Ordem de criação respeita dependências de FK (topological sort):
-- usuarios -> produtos -> clientes -> precos_por_janela -> pedidos ->
-- pedido_itens -> alertas_consistencia -> recomendacoes
-- ============================================================

-- ============================================================
-- TABLE: usuarios
-- ============================================================
IF OBJECT_ID(N'[dbo].[usuarios]', N'U') IS NULL
BEGIN
    CREATE TABLE [dbo].[usuarios] (
        id              INT IDENTITY(1,1) PRIMARY KEY,
        nome            VARCHAR(100)  NOT NULL,
        email           VARCHAR(150)  NOT NULL,
        senha_hash      VARCHAR(255)  NOT NULL,
        role            VARCHAR(20)   NOT NULL,   -- enum: admin, trader, rtv
        rtv_territorio  VARCHAR(100)  NULL,
        ativo           BIT           NOT NULL DEFAULT 1,
        created_at      DATETIME2     NOT NULL DEFAULT GETDATE(),
        updated_at      DATETIME2     NOT NULL DEFAULT GETDATE()
    );
END
GO

IF NOT EXISTS (SELECT * FROM sys.indexes WHERE name = 'UQ_usuarios_email' AND object_id = OBJECT_ID('[dbo].[usuarios]'))
    CREATE UNIQUE INDEX UQ_usuarios_email ON [dbo].[usuarios] (email);
GO
IF NOT EXISTS (SELECT * FROM sys.indexes WHERE name = 'IX_usuarios_role' AND object_id = OBJECT_ID('[dbo].[usuarios]'))
    CREATE INDEX IX_usuarios_role ON [dbo].[usuarios] (role);
GO

-- ============================================================
-- TABLE: produtos
-- ============================================================
IF OBJECT_ID(N'[dbo].[produtos]', N'U') IS NULL
BEGIN
    CREATE TABLE [dbo].[produtos] (
        id                  INT IDENTITY(1,1) PRIMARY KEY,
        nome_comercial      VARCHAR(150)   NOT NULL,
        tipo                VARCHAR(20)    NOT NULL,   -- enum: Defensivo, Fertilizante
        classe              VARCHAR(80)    NULL,
        ingrediente_ativo   VARCHAR(150)   NULL,
        unidade             VARCHAR(20)    NOT NULL,
        custo               DECIMAL(15,2)  NOT NULL,
        ativo               BIT            NOT NULL DEFAULT 1,
        created_at          DATETIME2      NOT NULL DEFAULT GETDATE(),
        updated_at          DATETIME2      NOT NULL DEFAULT GETDATE()
    );
END
GO

IF NOT EXISTS (SELECT * FROM sys.indexes WHERE name = 'IX_produtos_tipo' AND object_id = OBJECT_ID('[dbo].[produtos]'))
    CREATE INDEX IX_produtos_tipo ON [dbo].[produtos] (tipo);
GO
IF NOT EXISTS (SELECT * FROM sys.indexes WHERE name = 'IX_produtos_ativo' AND object_id = OBJECT_ID('[dbo].[produtos]'))
    CREATE INDEX IX_produtos_ativo ON [dbo].[produtos] (ativo);
GO

-- ============================================================
-- TABLE: clientes
-- ============================================================
IF OBJECT_ID(N'[dbo].[clientes]', N'U') IS NULL
BEGIN
    CREATE TABLE [dbo].[clientes] (
        id                  INT IDENTITY(1,1) PRIMARY KEY,
        nome                VARCHAR(150)   NOT NULL,
        documento           VARCHAR(20)    NOT NULL,
        regiao              VARCHAR(100)   NOT NULL,
        cultura_principal   VARCHAR(100)   NULL,
        rtv_id              INT            NOT NULL,
        ativo               BIT            NOT NULL DEFAULT 1,
        created_at          DATETIME2      NOT NULL DEFAULT GETDATE(),
        updated_at          DATETIME2      NOT NULL DEFAULT GETDATE(),
        CONSTRAINT FK_clientes_usuarios FOREIGN KEY (rtv_id) REFERENCES [dbo].[usuarios](id)
    );
END
GO

IF NOT EXISTS (SELECT * FROM sys.indexes WHERE name = 'UQ_clientes_documento' AND object_id = OBJECT_ID('[dbo].[clientes]'))
    CREATE UNIQUE INDEX UQ_clientes_documento ON [dbo].[clientes] (documento);
GO
IF NOT EXISTS (SELECT * FROM sys.indexes WHERE name = 'IX_clientes_rtv_id' AND object_id = OBJECT_ID('[dbo].[clientes]'))
    CREATE INDEX IX_clientes_rtv_id ON [dbo].[clientes] (rtv_id);
GO
IF NOT EXISTS (SELECT * FROM sys.indexes WHERE name = 'IX_clientes_regiao' AND object_id = OBJECT_ID('[dbo].[clientes]'))
    CREATE INDEX IX_clientes_regiao ON [dbo].[clientes] (regiao);
GO

-- ============================================================
-- TABLE: precos_por_janela
-- ============================================================
IF OBJECT_ID(N'[dbo].[precos_por_janela]', N'U') IS NULL
BEGIN
    CREATE TABLE [dbo].[precos_por_janela] (
        id                  INT IDENTITY(1,1) PRIMARY KEY,
        produto_id          INT            NOT NULL,
        janela_mes          INT            NOT NULL,
        janela_ano          INT            NOT NULL,
        condicao_pagamento  VARCHAR(50)    NOT NULL,
        preco               DECIMAL(15,2)  NOT NULL,
        vigente_de          DATE           NOT NULL,
        vigente_ate         DATE           NULL,
        created_at          DATETIME2      NOT NULL DEFAULT GETDATE(),
        updated_at          DATETIME2      NOT NULL DEFAULT GETDATE(),
        CONSTRAINT FK_precos_por_janela_produtos FOREIGN KEY (produto_id) REFERENCES [dbo].[produtos](id)
    );
END
GO

IF NOT EXISTS (SELECT * FROM sys.indexes WHERE name = 'UQ_precos_por_janela_lookup' AND object_id = OBJECT_ID('[dbo].[precos_por_janela]'))
    CREATE UNIQUE INDEX UQ_precos_por_janela_lookup ON [dbo].[precos_por_janela] (produto_id, janela_mes, janela_ano, condicao_pagamento);
GO

-- ============================================================
-- TABLE: pedidos
-- ============================================================
IF OBJECT_ID(N'[dbo].[pedidos]', N'U') IS NULL
BEGIN
    CREATE TABLE [dbo].[pedidos] (
        id                      INT IDENTITY(1,1) PRIMARY KEY,
        cliente_id              INT            NOT NULL,
        rtv_id                  INT            NOT NULL,
        cultura_safra           VARCHAR(100)   NULL,
        canal_origem            VARCHAR(20)    NOT NULL,   -- enum: WhatsApp, Email, Imagem, Manual
        valor_total             DECIMAL(15,2)  NOT NULL DEFAULT 0,
        observacoes             TEXT           NULL,
        status                  VARCHAR(30)    NOT NULL DEFAULT 'Rascunho',  -- enum status_pedido
        aprovado_por            VARCHAR(100)   NULL,
        aprovado_em             DATETIME2      NULL,
        comentario_aprovacao    TEXT           NULL,
        created_at              DATETIME2      NOT NULL DEFAULT GETDATE(),
        updated_at              DATETIME2      NOT NULL DEFAULT GETDATE(),
        CONSTRAINT FK_pedidos_clientes FOREIGN KEY (cliente_id) REFERENCES [dbo].[clientes](id),
        CONSTRAINT FK_pedidos_usuarios FOREIGN KEY (rtv_id) REFERENCES [dbo].[usuarios](id)
    );
END
GO

IF NOT EXISTS (SELECT * FROM sys.indexes WHERE name = 'IX_pedidos_cliente_id' AND object_id = OBJECT_ID('[dbo].[pedidos]'))
    CREATE INDEX IX_pedidos_cliente_id ON [dbo].[pedidos] (cliente_id);
GO
IF NOT EXISTS (SELECT * FROM sys.indexes WHERE name = 'IX_pedidos_rtv_id' AND object_id = OBJECT_ID('[dbo].[pedidos]'))
    CREATE INDEX IX_pedidos_rtv_id ON [dbo].[pedidos] (rtv_id);
GO
IF NOT EXISTS (SELECT * FROM sys.indexes WHERE name = 'IX_pedidos_status' AND object_id = OBJECT_ID('[dbo].[pedidos]'))
    CREATE INDEX IX_pedidos_status ON [dbo].[pedidos] (status);
GO

-- ============================================================
-- TABLE: pedido_itens
-- ============================================================
IF OBJECT_ID(N'[dbo].[pedido_itens]', N'U') IS NULL
BEGIN
    CREATE TABLE [dbo].[pedido_itens] (
        id                  INT IDENTITY(1,1) PRIMARY KEY,
        pedido_id           INT            NOT NULL,
        produto_id          INT            NOT NULL,
        quantidade          DECIMAL(15,2)  NOT NULL,
        unidade             VARCHAR(20)    NOT NULL,
        janela_mes          INT            NOT NULL,
        janela_ano          INT            NOT NULL,
        formato_entrega     VARCHAR(50)    NOT NULL,
        local_entrega       VARCHAR(150)   NOT NULL,
        condicao_pagamento  VARCHAR(50)    NOT NULL,   -- lookup em precos_por_janela (RN-004)
        preco_unitario      DECIMAL(15,2)  NOT NULL,
        subtotal            DECIMAL(15,2)  NOT NULL,
        created_at          DATETIME2      NOT NULL DEFAULT GETDATE(),
        updated_at          DATETIME2      NOT NULL DEFAULT GETDATE(),
        CONSTRAINT FK_pedido_itens_pedidos FOREIGN KEY (pedido_id) REFERENCES [dbo].[pedidos](id),
        CONSTRAINT FK_pedido_itens_produtos FOREIGN KEY (produto_id) REFERENCES [dbo].[produtos](id)
    );
END
GO

IF NOT EXISTS (SELECT * FROM sys.indexes WHERE name = 'IX_pedido_itens_pedido_id' AND object_id = OBJECT_ID('[dbo].[pedido_itens]'))
    CREATE INDEX IX_pedido_itens_pedido_id ON [dbo].[pedido_itens] (pedido_id);
GO
IF NOT EXISTS (SELECT * FROM sys.indexes WHERE name = 'IX_pedido_itens_produto_id' AND object_id = OBJECT_ID('[dbo].[pedido_itens]'))
    CREATE INDEX IX_pedido_itens_produto_id ON [dbo].[pedido_itens] (produto_id);
GO
IF NOT EXISTS (SELECT * FROM sys.indexes WHERE name = 'IX_pedido_itens_preco_lookup' AND object_id = OBJECT_ID('[dbo].[pedido_itens]'))
    CREATE INDEX IX_pedido_itens_preco_lookup ON [dbo].[pedido_itens] (produto_id, janela_mes, janela_ano, condicao_pagamento);
GO

-- ============================================================
-- TABLE: alertas_consistencia
-- ============================================================
IF OBJECT_ID(N'[dbo].[alertas_consistencia]', N'U') IS NULL
BEGIN
    CREATE TABLE [dbo].[alertas_consistencia] (
        id              INT IDENTITY(1,1) PRIMARY KEY,
        pedido_id       INT            NOT NULL,
        tipo            VARCHAR(30)    NOT NULL,   -- enum: ProdutoAtipico, VolumetriaAtipica, CondicaoDivergente
        descricao       TEXT           NOT NULL,
        severidade      VARCHAR(10)    NOT NULL,   -- enum: Baixa, Media, Alta
        resolvido_por   VARCHAR(100)   NULL,
        created_at      DATETIME2      NOT NULL DEFAULT GETDATE(),
        updated_at      DATETIME2      NOT NULL DEFAULT GETDATE(),
        CONSTRAINT FK_alertas_consistencia_pedidos FOREIGN KEY (pedido_id) REFERENCES [dbo].[pedidos](id)
    );
END
GO

IF NOT EXISTS (SELECT * FROM sys.indexes WHERE name = 'IX_alertas_consistencia_pedido_id' AND object_id = OBJECT_ID('[dbo].[alertas_consistencia]'))
    CREATE INDEX IX_alertas_consistencia_pedido_id ON [dbo].[alertas_consistencia] (pedido_id);
GO
IF NOT EXISTS (SELECT * FROM sys.indexes WHERE name = 'IX_alertas_consistencia_severidade' AND object_id = OBJECT_ID('[dbo].[alertas_consistencia]'))
    CREATE INDEX IX_alertas_consistencia_severidade ON [dbo].[alertas_consistencia] (severidade);
GO

-- ============================================================
-- TABLE: recomendacoes
-- ============================================================
IF OBJECT_ID(N'[dbo].[recomendacoes]', N'U') IS NULL
BEGIN
    CREATE TABLE [dbo].[recomendacoes] (
        id          INT IDENTITY(1,1) PRIMARY KEY,
        cliente_id  INT            NOT NULL,
        produto_id  INT            NOT NULL,
        motivo      VARCHAR(20)    NOT NULL,   -- enum: Historico, Sazonalidade, MixRegional
        score       DECIMAL(8,4)   NOT NULL,
        aceita      BIT            NOT NULL DEFAULT 0,
        gerada_em   DATETIME2      NOT NULL,
        created_at  DATETIME2      NOT NULL DEFAULT GETDATE(),
        updated_at  DATETIME2      NOT NULL DEFAULT GETDATE(),
        CONSTRAINT FK_recomendacoes_clientes FOREIGN KEY (cliente_id) REFERENCES [dbo].[clientes](id),
        CONSTRAINT FK_recomendacoes_produtos FOREIGN KEY (produto_id) REFERENCES [dbo].[produtos](id)
    );
END
GO

IF NOT EXISTS (SELECT * FROM sys.indexes WHERE name = 'IX_recomendacoes_cliente_id' AND object_id = OBJECT_ID('[dbo].[recomendacoes]'))
    CREATE INDEX IX_recomendacoes_cliente_id ON [dbo].[recomendacoes] (cliente_id);
GO
IF NOT EXISTS (SELECT * FROM sys.indexes WHERE name = 'IX_recomendacoes_produto_id' AND object_id = OBJECT_ID('[dbo].[recomendacoes]'))
    CREATE INDEX IX_recomendacoes_produto_id ON [dbo].[recomendacoes] (produto_id);
GO
