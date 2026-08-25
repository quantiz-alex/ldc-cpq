-- ============================================================
-- LDC Insumos — Plataforma Comercial (CPQ Inteligente)
-- SEED de dados de exemplo (mock_data/*.json)
-- Ordem topologica de FKs: usuarios -> produtos -> clientes ->
-- precos_por_janela -> pedidos -> pedido_itens ->
-- alertas_consistencia -> recomendacoes
-- ============================================================

-- ============================================================
-- SEED: usuarios
-- ============================================================
SET IDENTITY_INSERT [dbo].[usuarios] ON;
GO

IF NOT EXISTS (SELECT 1 FROM [dbo].[usuarios] WHERE id = 1)
BEGIN
    INSERT INTO [dbo].[usuarios] (id, nome, email, senha_hash, role, rtv_territorio, ativo, created_at, updated_at)
    VALUES (1, 'Administrador do Sistema', 'admin@ldc-cpq.com', '$2b$12$KIXQ5Z0m8h9dQhq7f0m6yO0z8b8b9v9v9v9v9v9v9v9v9v9v9v9v9', 'admin', NULL, 1, '2025-01-25T00:00:00', '2026-02-19T00:00:00');
END
GO
IF NOT EXISTS (SELECT 1 FROM [dbo].[usuarios] WHERE id = 2)
BEGIN
    INSERT INTO [dbo].[usuarios] (id, nome, email, senha_hash, role, rtv_territorio, ativo, created_at, updated_at)
    VALUES (2, 'Marcelo Andrade', 'marcelo.andrade@ldc-cpq.com', '$2b$12$abTraderHashPlaceholder0000000000000000000000000', 'trader', NULL, 1, '2025-02-14T00:00:00', '2026-02-09T00:00:00');
END
GO
IF NOT EXISTS (SELECT 1 FROM [dbo].[usuarios] WHERE id = 3)
BEGIN
    INSERT INTO [dbo].[usuarios] (id, nome, email, senha_hash, role, rtv_territorio, ativo, created_at, updated_at)
    VALUES (3, 'Fernanda Lopes', 'fernanda.lopes@ldc-cpq.com', '$2b$12$abTraderHashPlaceholder0000000000000000000000000', 'trader', NULL, 1, '2025-02-14T00:00:00', '2026-02-09T00:00:00');
END
GO
IF NOT EXISTS (SELECT 1 FROM [dbo].[usuarios] WHERE id = 4)
BEGIN
    INSERT INTO [dbo].[usuarios] (id, nome, email, senha_hash, role, rtv_territorio, ativo, created_at, updated_at)
    VALUES (4, 'Ricardo Nunes', 'ricardo.nunes@ldc-cpq.com', '$2b$12$abTraderHashPlaceholder0000000000000000000000000', 'trader', NULL, 1, '2025-02-14T00:00:00', '2026-02-09T00:00:00');
END
GO
IF NOT EXISTS (SELECT 1 FROM [dbo].[usuarios] WHERE id = 5)
BEGIN
    INSERT INTO [dbo].[usuarios] (id, nome, email, senha_hash, role, rtv_territorio, ativo, created_at, updated_at)
    VALUES (5, 'Carlos Eduardo Silva', 'carlos.eduardo.silva@ldc-cpq.com', '$2b$12$abRtvHashPlaceholder000000000000000000000000000', 'rtv', 'Sorriso-MT', 1, '2025-03-16T00:00:00', '2026-02-14T00:00:00');
END
GO
IF NOT EXISTS (SELECT 1 FROM [dbo].[usuarios] WHERE id = 6)
BEGIN
    INSERT INTO [dbo].[usuarios] (id, nome, email, senha_hash, role, rtv_territorio, ativo, created_at, updated_at)
    VALUES (6, 'Juliana Ramos', 'juliana.ramos@ldc-cpq.com', '$2b$12$abRtvHashPlaceholder000000000000000000000000000', 'rtv', 'Rondonópolis-MT', 1, '2025-03-16T00:00:00', '2026-02-14T00:00:00');
END
GO
IF NOT EXISTS (SELECT 1 FROM [dbo].[usuarios] WHERE id = 7)
BEGIN
    INSERT INTO [dbo].[usuarios] (id, nome, email, senha_hash, role, rtv_territorio, ativo, created_at, updated_at)
    VALUES (7, 'Bruno Tavares', 'bruno.tavares@ldc-cpq.com', '$2b$12$abRtvHashPlaceholder000000000000000000000000000', 'rtv', 'Sinop-MT', 1, '2025-03-16T00:00:00', '2026-02-14T00:00:00');
END
GO
IF NOT EXISTS (SELECT 1 FROM [dbo].[usuarios] WHERE id = 8)
BEGIN
    INSERT INTO [dbo].[usuarios] (id, nome, email, senha_hash, role, rtv_territorio, ativo, created_at, updated_at)
    VALUES (8, 'Patrícia Gomes', 'patricia.gomes@ldc-cpq.com', '$2b$12$abRtvHashPlaceholder000000000000000000000000000', 'rtv', 'Rio Verde-GO', 1, '2025-03-16T00:00:00', '2026-02-14T00:00:00');
END
GO
IF NOT EXISTS (SELECT 1 FROM [dbo].[usuarios] WHERE id = 9)
BEGIN
    INSERT INTO [dbo].[usuarios] (id, nome, email, senha_hash, role, rtv_territorio, ativo, created_at, updated_at)
    VALUES (9, 'Diego Martins', 'diego.martins@ldc-cpq.com', '$2b$12$abRtvHashPlaceholder000000000000000000000000000', 'rtv', 'Cristalina-GO', 1, '2025-03-16T00:00:00', '2026-02-14T00:00:00');
END
GO
IF NOT EXISTS (SELECT 1 FROM [dbo].[usuarios] WHERE id = 10)
BEGIN
    INSERT INTO [dbo].[usuarios] (id, nome, email, senha_hash, role, rtv_territorio, ativo, created_at, updated_at)
    VALUES (10, 'Camila Ferreira', 'camila.ferreira@ldc-cpq.com', '$2b$12$abRtvHashPlaceholder000000000000000000000000000', 'rtv', 'Uberaba-MG', 1, '2025-03-16T00:00:00', '2026-02-14T00:00:00');
END
GO
IF NOT EXISTS (SELECT 1 FROM [dbo].[usuarios] WHERE id = 11)
BEGIN
    INSERT INTO [dbo].[usuarios] (id, nome, email, senha_hash, role, rtv_territorio, ativo, created_at, updated_at)
    VALUES (11, 'André Luiz Costa', 'andré.luiz.costa@ldc-cpq.com', '$2b$12$abRtvHashPlaceholder000000000000000000000000000', 'rtv', 'Primavera do Leste-MT', 1, '2025-03-16T00:00:00', '2026-02-14T00:00:00');
END
GO
IF NOT EXISTS (SELECT 1 FROM [dbo].[usuarios] WHERE id = 12)
BEGIN
    INSERT INTO [dbo].[usuarios] (id, nome, email, senha_hash, role, rtv_territorio, ativo, created_at, updated_at)
    VALUES (12, 'Larissa Pereira', 'larissa.pereira@ldc-cpq.com', '$2b$12$abRtvHashPlaceholder000000000000000000000000000', 'rtv', 'Luís Eduardo Magalhães-BA', 1, '2025-03-16T00:00:00', '2026-02-14T00:00:00');
END
GO

SET IDENTITY_INSERT [dbo].[usuarios] OFF;
GO

-- ============================================================
-- SEED: produtos
-- ============================================================
SET IDENTITY_INSERT [dbo].[produtos] ON;
GO

IF NOT EXISTS (SELECT 1 FROM [dbo].[produtos] WHERE id = 1)
BEGIN
    INSERT INTO [dbo].[produtos] (id, nome_comercial, tipo, classe, ingrediente_ativo, unidade, custo, ativo, created_at, updated_at)
    VALUES (1, 'Glifosato Nortox 480 SL', 'Defensivo', 'Herbicida', 'Glifosato', 'L', 147.16, 1, '2025-05-05T00:00:00', '2026-01-30T00:00:00');
END
GO
IF NOT EXISTS (SELECT 1 FROM [dbo].[produtos] WHERE id = 2)
BEGIN
    INSERT INTO [dbo].[produtos] (id, nome_comercial, tipo, classe, ingrediente_ativo, unidade, custo, ativo, created_at, updated_at)
    VALUES (2, 'Roundup Original DI', 'Defensivo', 'Herbicida', 'Glifosato', 'L', 23.05, 1, '2025-05-05T00:00:00', '2026-01-30T00:00:00');
END
GO
IF NOT EXISTS (SELECT 1 FROM [dbo].[produtos] WHERE id = 3)
BEGIN
    INSERT INTO [dbo].[produtos] (id, nome_comercial, tipo, classe, ingrediente_ativo, unidade, custo, ativo, created_at, updated_at)
    VALUES (3, 'Priori Xtra', 'Defensivo', 'Fungicida', 'Azoxistrobina + Ciproconazol', 'L', 73.56, 1, '2025-05-05T00:00:00', '2026-01-30T00:00:00');
END
GO
IF NOT EXISTS (SELECT 1 FROM [dbo].[produtos] WHERE id = 4)
BEGIN
    INSERT INTO [dbo].[produtos] (id, nome_comercial, tipo, classe, ingrediente_ativo, unidade, custo, ativo, created_at, updated_at)
    VALUES (4, 'Fox Xpro', 'Defensivo', 'Fungicida', 'Bixafem + Protioconazol + Trifloxistrobina', 'L', 63.09, 1, '2025-05-05T00:00:00', '2026-01-30T00:00:00');
END
GO
IF NOT EXISTS (SELECT 1 FROM [dbo].[produtos] WHERE id = 5)
BEGIN
    INSERT INTO [dbo].[produtos] (id, nome_comercial, tipo, classe, ingrediente_ativo, unidade, custo, ativo, created_at, updated_at)
    VALUES (5, 'Engeo Pleno S', 'Defensivo', 'Inseticida', 'Tiametoxam + Lambda-cialotrina', 'L', 166.77, 1, '2025-05-05T00:00:00', '2026-01-30T00:00:00');
END
GO
IF NOT EXISTS (SELECT 1 FROM [dbo].[produtos] WHERE id = 6)
BEGIN
    INSERT INTO [dbo].[produtos] (id, nome_comercial, tipo, classe, ingrediente_ativo, unidade, custo, ativo, created_at, updated_at)
    VALUES (6, 'Connect', 'Defensivo', 'Inseticida', 'Imidacloprido + Betaciflutrina', 'L', 154.69, 1, '2025-05-05T00:00:00', '2026-01-30T00:00:00');
END
GO
IF NOT EXISTS (SELECT 1 FROM [dbo].[produtos] WHERE id = 7)
BEGIN
    INSERT INTO [dbo].[produtos] (id, nome_comercial, tipo, classe, ingrediente_ativo, unidade, custo, ativo, created_at, updated_at)
    VALUES (7, 'Talisman', 'Defensivo', 'Herbicida', 'Dicamba', 'L', 198.22, 1, '2025-05-05T00:00:00', '2026-01-30T00:00:00');
END
GO
IF NOT EXISTS (SELECT 1 FROM [dbo].[produtos] WHERE id = 8)
BEGIN
    INSERT INTO [dbo].[produtos] (id, nome_comercial, tipo, classe, ingrediente_ativo, unidade, custo, ativo, created_at, updated_at)
    VALUES (8, 'Nimbus', 'Defensivo', 'Óleo Adjuvante', 'Óleo Mineral', 'L', 35.56, 1, '2025-05-05T00:00:00', '2026-01-30T00:00:00');
END
GO
IF NOT EXISTS (SELECT 1 FROM [dbo].[produtos] WHERE id = 9)
BEGIN
    INSERT INTO [dbo].[produtos] (id, nome_comercial, tipo, classe, ingrediente_ativo, unidade, custo, ativo, created_at, updated_at)
    VALUES (9, 'Aproach Prima', 'Defensivo', 'Fungicida', 'Ciproconazol + Picoxistrobina', 'L', 103.23, 1, '2025-05-05T00:00:00', '2026-01-30T00:00:00');
END
GO
IF NOT EXISTS (SELECT 1 FROM [dbo].[produtos] WHERE id = 10)
BEGIN
    INSERT INTO [dbo].[produtos] (id, nome_comercial, tipo, classe, ingrediente_ativo, unidade, custo, ativo, created_at, updated_at)
    VALUES (10, 'Verdadero', 'Defensivo', 'Fungicida', 'Fluxapiroxade + Piraclostrobina', 'L', 24.02, 1, '2025-05-05T00:00:00', '2026-01-30T00:00:00');
END
GO
IF NOT EXISTS (SELECT 1 FROM [dbo].[produtos] WHERE id = 11)
BEGIN
    INSERT INTO [dbo].[produtos] (id, nome_comercial, tipo, classe, ingrediente_ativo, unidade, custo, ativo, created_at, updated_at)
    VALUES (11, 'Certero', 'Defensivo', 'Herbicida', 'Cletodim', 'L', 62.16, 1, '2025-05-05T00:00:00', '2026-01-30T00:00:00');
END
GO
IF NOT EXISTS (SELECT 1 FROM [dbo].[produtos] WHERE id = 12)
BEGIN
    INSERT INTO [dbo].[produtos] (id, nome_comercial, tipo, classe, ingrediente_ativo, unidade, custo, ativo, created_at, updated_at)
    VALUES (12, 'Sumilarv 0.5G', 'Defensivo', 'Inseticida', 'Piriproxifem', 'kg', 120.08, 1, '2025-05-05T00:00:00', '2026-01-30T00:00:00');
END
GO
IF NOT EXISTS (SELECT 1 FROM [dbo].[produtos] WHERE id = 13)
BEGIN
    INSERT INTO [dbo].[produtos] (id, nome_comercial, tipo, classe, ingrediente_ativo, unidade, custo, ativo, created_at, updated_at)
    VALUES (13, 'Ureia 45%', 'Fertilizante', 'Nitrogenado', NULL, 't', 1863.69, 1, '2025-05-05T00:00:00', '2026-01-30T00:00:00');
END
GO
IF NOT EXISTS (SELECT 1 FROM [dbo].[produtos] WHERE id = 14)
BEGIN
    INSERT INTO [dbo].[produtos] (id, nome_comercial, tipo, classe, ingrediente_ativo, unidade, custo, ativo, created_at, updated_at)
    VALUES (14, 'MAP 11-52-00', 'Fertilizante', 'Fosfatado', NULL, 't', 2277.21, 1, '2025-05-05T00:00:00', '2026-01-30T00:00:00');
END
GO
IF NOT EXISTS (SELECT 1 FROM [dbo].[produtos] WHERE id = 15)
BEGIN
    INSERT INTO [dbo].[produtos] (id, nome_comercial, tipo, classe, ingrediente_ativo, unidade, custo, ativo, created_at, updated_at)
    VALUES (15, 'KCl 60% (Cloreto de Potássio)', 'Fertilizante', 'Potássico', NULL, 't', 3359.72, 1, '2025-05-05T00:00:00', '2026-01-30T00:00:00');
END
GO
IF NOT EXISTS (SELECT 1 FROM [dbo].[produtos] WHERE id = 16)
BEGIN
    INSERT INTO [dbo].[produtos] (id, nome_comercial, tipo, classe, ingrediente_ativo, unidade, custo, ativo, created_at, updated_at)
    VALUES (16, 'NPK 08-28-16', 'Fertilizante', 'Formulado NPK', NULL, 't', 3107.86, 1, '2025-05-05T00:00:00', '2026-01-30T00:00:00');
END
GO
IF NOT EXISTS (SELECT 1 FROM [dbo].[produtos] WHERE id = 17)
BEGIN
    INSERT INTO [dbo].[produtos] (id, nome_comercial, tipo, classe, ingrediente_ativo, unidade, custo, ativo, created_at, updated_at)
    VALUES (17, 'NPK 20-05-20', 'Fertilizante', 'Formulado NPK', NULL, 't', 2329.06, 1, '2025-05-05T00:00:00', '2026-01-30T00:00:00');
END
GO
IF NOT EXISTS (SELECT 1 FROM [dbo].[produtos] WHERE id = 18)
BEGIN
    INSERT INTO [dbo].[produtos] (id, nome_comercial, tipo, classe, ingrediente_ativo, unidade, custo, ativo, created_at, updated_at)
    VALUES (18, 'Sulfato de Amônio', 'Fertilizante', 'Nitrogenado', NULL, 't', 3214.24, 1, '2025-05-05T00:00:00', '2026-01-30T00:00:00');
END
GO
IF NOT EXISTS (SELECT 1 FROM [dbo].[produtos] WHERE id = 19)
BEGIN
    INSERT INTO [dbo].[produtos] (id, nome_comercial, tipo, classe, ingrediente_ativo, unidade, custo, ativo, created_at, updated_at)
    VALUES (19, 'Super Simples', 'Fertilizante', 'Fosfatado', NULL, 't', 3742.63, 1, '2025-05-05T00:00:00', '2026-01-30T00:00:00');
END
GO
IF NOT EXISTS (SELECT 1 FROM [dbo].[produtos] WHERE id = 20)
BEGIN
    INSERT INTO [dbo].[produtos] (id, nome_comercial, tipo, classe, ingrediente_ativo, unidade, custo, ativo, created_at, updated_at)
    VALUES (20, 'Calcário Dolomítico', 'Fertilizante', 'Corretivo de Solo', NULL, 't', 1815.6, 1, '2025-05-05T00:00:00', '2026-01-30T00:00:00');
END
GO
IF NOT EXISTS (SELECT 1 FROM [dbo].[produtos] WHERE id = 21)
BEGIN
    INSERT INTO [dbo].[produtos] (id, nome_comercial, tipo, classe, ingrediente_ativo, unidade, custo, ativo, created_at, updated_at)
    VALUES (21, 'Gesso Agrícola', 'Fertilizante', 'Corretivo de Solo', NULL, 't', 3733.97, 1, '2025-05-05T00:00:00', '2026-01-30T00:00:00');
END
GO
IF NOT EXISTS (SELECT 1 FROM [dbo].[produtos] WHERE id = 22)
BEGIN
    INSERT INTO [dbo].[produtos] (id, nome_comercial, tipo, classe, ingrediente_ativo, unidade, custo, ativo, created_at, updated_at)
    VALUES (22, 'Cloreto de Potássio Granulado', 'Fertilizante', 'Potássico', NULL, 't', 3475.53, 1, '2025-05-05T00:00:00', '2026-01-30T00:00:00');
END
GO
IF NOT EXISTS (SELECT 1 FROM [dbo].[produtos] WHERE id = 23)
BEGIN
    INSERT INTO [dbo].[produtos] (id, nome_comercial, tipo, classe, ingrediente_ativo, unidade, custo, ativo, created_at, updated_at)
    VALUES (23, 'NPK 12-06-24', 'Fertilizante', 'Formulado NPK', NULL, 't', 2616.6, 1, '2025-05-05T00:00:00', '2026-01-30T00:00:00');
END
GO
IF NOT EXISTS (SELECT 1 FROM [dbo].[produtos] WHERE id = 24)
BEGIN
    INSERT INTO [dbo].[produtos] (id, nome_comercial, tipo, classe, ingrediente_ativo, unidade, custo, ativo, created_at, updated_at)
    VALUES (24, 'Boro Granulado', 'Fertilizante', 'Micronutriente', NULL, 'kg', 2173.15, 1, '2025-05-05T00:00:00', '2026-01-30T00:00:00');
END
GO
IF NOT EXISTS (SELECT 1 FROM [dbo].[produtos] WHERE id = 25)
BEGIN
    INSERT INTO [dbo].[produtos] (id, nome_comercial, tipo, classe, ingrediente_ativo, unidade, custo, ativo, created_at, updated_at)
    VALUES (25, 'Zinco Quelatizado', 'Fertilizante', 'Micronutriente', NULL, 'kg', 4097.31, 1, '2025-05-05T00:00:00', '2026-01-30T00:00:00');
END
GO

SET IDENTITY_INSERT [dbo].[produtos] OFF;
GO

-- ============================================================
-- SEED: clientes
-- ============================================================
SET IDENTITY_INSERT [dbo].[clientes] ON;
GO

IF NOT EXISTS (SELECT 1 FROM [dbo].[clientes] WHERE id = 1)
BEGIN
    INSERT INTO [dbo].[clientes] (id, nome, documento, regiao, cultura_principal, rtv_id, ativo, created_at, updated_at)
    VALUES (1, 'Agropecuária Bom Futuro', '53.204.194/0001-58', 'Rondonópolis-MT', 'Soja', 6, 1, '2025-05-26T00:00:00', '2026-02-09T00:00:00');
END
GO
IF NOT EXISTS (SELECT 1 FROM [dbo].[clientes] WHERE id = 2)
BEGIN
    INSERT INTO [dbo].[clientes] (id, nome, documento, regiao, cultura_principal, rtv_id, ativo, created_at, updated_at)
    VALUES (2, 'Fazenda Santa Luzia', '55.967.452/0001-87', 'Sinop-MT', 'Algodão', 7, 1, '2025-05-27T00:00:00', '2026-02-09T00:00:00');
END
GO
IF NOT EXISTS (SELECT 1 FROM [dbo].[clientes] WHERE id = 3)
BEGIN
    INSERT INTO [dbo].[clientes] (id, nome, documento, regiao, cultura_principal, rtv_id, ativo, created_at, updated_at)
    VALUES (3, 'Grupo Amaggi Filial', '15.847.570/0001-78', 'Rio Verde-GO', 'Soja', 8, 1, '2025-05-28T00:00:00', '2026-02-09T00:00:00');
END
GO
IF NOT EXISTS (SELECT 1 FROM [dbo].[clientes] WHERE id = 4)
BEGIN
    INSERT INTO [dbo].[clientes] (id, nome, documento, regiao, cultura_principal, rtv_id, ativo, created_at, updated_at)
    VALUES (4, 'Fazenda Boa Vista', '58.180.665/0001-47', 'Cristalina-GO', 'Cana-de-açúcar', 9, 1, '2025-05-29T00:00:00', '2026-02-09T00:00:00');
END
GO
IF NOT EXISTS (SELECT 1 FROM [dbo].[clientes] WHERE id = 5)
BEGIN
    INSERT INTO [dbo].[clientes] (id, nome, documento, regiao, cultura_principal, rtv_id, ativo, created_at, updated_at)
    VALUES (5, 'Cooperativa Coopervale', '56.691.296/0001-18', 'Uberaba-MG', 'Soja', 10, 1, '2025-05-30T00:00:00', '2026-02-09T00:00:00');
END
GO
IF NOT EXISTS (SELECT 1 FROM [dbo].[clientes] WHERE id = 6)
BEGIN
    INSERT INTO [dbo].[clientes] (id, nome, documento, regiao, cultura_principal, rtv_id, ativo, created_at, updated_at)
    VALUES (6, 'Fazenda Três Irmãos', '94.333.891/0001-47', 'Primavera do Leste-MT', 'Soja', 11, 1, '2025-05-31T00:00:00', '2026-02-09T00:00:00');
END
GO
IF NOT EXISTS (SELECT 1 FROM [dbo].[clientes] WHERE id = 7)
BEGIN
    INSERT INTO [dbo].[clientes] (id, nome, documento, regiao, cultura_principal, rtv_id, ativo, created_at, updated_at)
    VALUES (7, 'Agrícola Rio Claro', '39.987.203/0001-58', 'Luís Eduardo Magalhães-BA', 'Algodão', 12, 1, '2025-06-01T00:00:00', '2026-02-09T00:00:00');
END
GO
IF NOT EXISTS (SELECT 1 FROM [dbo].[clientes] WHERE id = 8)
BEGIN
    INSERT INTO [dbo].[clientes] (id, nome, documento, regiao, cultura_principal, rtv_id, ativo, created_at, updated_at)
    VALUES (8, 'Fazenda Água Limpa', '68.750.954/0001-56', 'Sorriso-MT', 'Milho', 5, 1, '2025-06-02T00:00:00', '2026-02-09T00:00:00');
END
GO
IF NOT EXISTS (SELECT 1 FROM [dbo].[clientes] WHERE id = 9)
BEGIN
    INSERT INTO [dbo].[clientes] (id, nome, documento, regiao, cultura_principal, rtv_id, ativo, created_at, updated_at)
    VALUES (9, 'Fazenda Cerrado Verde', '57.463.314/0001-95', 'Rondonópolis-MT', 'Algodão', 6, 1, '2025-06-03T00:00:00', '2026-02-09T00:00:00');
END
GO
IF NOT EXISTS (SELECT 1 FROM [dbo].[clientes] WHERE id = 10)
BEGIN
    INSERT INTO [dbo].[clientes] (id, nome, documento, regiao, cultura_principal, rtv_id, ativo, created_at, updated_at)
    VALUES (10, 'Grupo Scheffer', '99.799.763/0001-19', 'Sinop-MT', 'Cana-de-açúcar', 7, 1, '2025-06-04T00:00:00', '2026-02-09T00:00:00');
END
GO
IF NOT EXISTS (SELECT 1 FROM [dbo].[clientes] WHERE id = 11)
BEGIN
    INSERT INTO [dbo].[clientes] (id, nome, documento, regiao, cultura_principal, rtv_id, ativo, created_at, updated_at)
    VALUES (11, 'Fazenda Progresso', '91.275.646/0001-41', 'Rio Verde-GO', 'Milho', 8, 1, '2025-06-05T00:00:00', '2026-02-09T00:00:00');
END
GO
IF NOT EXISTS (SELECT 1 FROM [dbo].[clientes] WHERE id = 12)
BEGIN
    INSERT INTO [dbo].[clientes] (id, nome, documento, regiao, cultura_principal, rtv_id, ativo, created_at, updated_at)
    VALUES (12, 'Agropecuária Del Rey', '69.488.376/0001-91', 'Cristalina-GO', 'Cana-de-açúcar', 9, 1, '2025-06-06T00:00:00', '2026-02-09T00:00:00');
END
GO
IF NOT EXISTS (SELECT 1 FROM [dbo].[clientes] WHERE id = 13)
BEGIN
    INSERT INTO [dbo].[clientes] (id, nome, documento, regiao, cultura_principal, rtv_id, ativo, created_at, updated_at)
    VALUES (13, 'Fazenda Novo Horizonte', '38.801.432/0001-17', 'Uberaba-MG', 'Milho', 10, 1, '2025-06-07T00:00:00', '2026-02-09T00:00:00');
END
GO
IF NOT EXISTS (SELECT 1 FROM [dbo].[clientes] WHERE id = 14)
BEGIN
    INSERT INTO [dbo].[clientes] (id, nome, documento, regiao, cultura_principal, rtv_id, ativo, created_at, updated_at)
    VALUES (14, 'Fazenda Sant''Ana', '14.924.423/0001-61', 'Primavera do Leste-MT', 'Algodão', 11, 1, '2025-06-08T00:00:00', '2026-02-09T00:00:00');
END
GO
IF NOT EXISTS (SELECT 1 FROM [dbo].[clientes] WHERE id = 15)
BEGIN
    INSERT INTO [dbo].[clientes] (id, nome, documento, regiao, cultura_principal, rtv_id, ativo, created_at, updated_at)
    VALUES (15, 'Cooperativa Cotrijal', '18.316.680/0001-50', 'Luís Eduardo Magalhães-BA', 'Milho', 12, 1, '2025-06-09T00:00:00', '2026-02-09T00:00:00');
END
GO
IF NOT EXISTS (SELECT 1 FROM [dbo].[clientes] WHERE id = 16)
BEGIN
    INSERT INTO [dbo].[clientes] (id, nome, documento, regiao, cultura_principal, rtv_id, ativo, created_at, updated_at)
    VALUES (16, 'Fazenda Barra Grande', '93.611.505/0001-92', 'Sorriso-MT', 'Soja/Milho (safrinha)', 5, 1, '2025-06-10T00:00:00', '2026-02-09T00:00:00');
END
GO
IF NOT EXISTS (SELECT 1 FROM [dbo].[clientes] WHERE id = 17)
BEGIN
    INSERT INTO [dbo].[clientes] (id, nome, documento, regiao, cultura_principal, rtv_id, ativo, created_at, updated_at)
    VALUES (17, 'Fazenda Pontal', '28.371.242/0001-41', 'Rondonópolis-MT', 'Cana-de-açúcar', 6, 1, '2025-06-11T00:00:00', '2026-02-09T00:00:00');
END
GO
IF NOT EXISTS (SELECT 1 FROM [dbo].[clientes] WHERE id = 18)
BEGIN
    INSERT INTO [dbo].[clientes] (id, nome, documento, regiao, cultura_principal, rtv_id, ativo, created_at, updated_at)
    VALUES (18, 'Agrícola Santa Fé', '78.369.864/0001-84', 'Sinop-MT', 'Soja/Milho (safrinha)', 7, 1, '2025-06-12T00:00:00', '2026-02-09T00:00:00');
END
GO
IF NOT EXISTS (SELECT 1 FROM [dbo].[clientes] WHERE id = 19)
BEGIN
    INSERT INTO [dbo].[clientes] (id, nome, documento, regiao, cultura_principal, rtv_id, ativo, created_at, updated_at)
    VALUES (19, 'Fazenda Boa Esperança', '84.508.470/0001-38', 'Rio Verde-GO', 'Milho', 8, 1, '2025-06-13T00:00:00', '2026-02-09T00:00:00');
END
GO
IF NOT EXISTS (SELECT 1 FROM [dbo].[clientes] WHERE id = 20)
BEGIN
    INSERT INTO [dbo].[clientes] (id, nome, documento, regiao, cultura_principal, rtv_id, ativo, created_at, updated_at)
    VALUES (20, 'Grupo Bianchini', '75.605.193/0001-16', 'Cristalina-GO', 'Soja', 9, 1, '2025-06-14T00:00:00', '2026-02-09T00:00:00');
END
GO
IF NOT EXISTS (SELECT 1 FROM [dbo].[clientes] WHERE id = 21)
BEGIN
    INSERT INTO [dbo].[clientes] (id, nome, documento, regiao, cultura_principal, rtv_id, ativo, created_at, updated_at)
    VALUES (21, 'Fazenda Colorado', '29.742.263/0001-97', 'Uberaba-MG', 'Soja/Milho (safrinha)', 10, 1, '2025-06-15T00:00:00', '2026-02-09T00:00:00');
END
GO
IF NOT EXISTS (SELECT 1 FROM [dbo].[clientes] WHERE id = 22)
BEGIN
    INSERT INTO [dbo].[clientes] (id, nome, documento, regiao, cultura_principal, rtv_id, ativo, created_at, updated_at)
    VALUES (22, 'Fazenda Marimbondo', '86.165.494/0001-58', 'Primavera do Leste-MT', 'Cana-de-açúcar', 11, 1, '2025-06-16T00:00:00', '2026-02-09T00:00:00');
END
GO
IF NOT EXISTS (SELECT 1 FROM [dbo].[clientes] WHERE id = 23)
BEGIN
    INSERT INTO [dbo].[clientes] (id, nome, documento, regiao, cultura_principal, rtv_id, ativo, created_at, updated_at)
    VALUES (23, 'Agropecuária Planalto', '69.641.357/0001-80', 'Luís Eduardo Magalhães-BA', 'Soja', 12, 1, '2025-06-17T00:00:00', '2026-02-09T00:00:00');
END
GO
IF NOT EXISTS (SELECT 1 FROM [dbo].[clientes] WHERE id = 24)
BEGIN
    INSERT INTO [dbo].[clientes] (id, nome, documento, regiao, cultura_principal, rtv_id, ativo, created_at, updated_at)
    VALUES (24, 'Fazenda Trindade', '97.838.217/0001-97', 'Sorriso-MT', 'Cana-de-açúcar', 5, 1, '2025-06-18T00:00:00', '2026-02-09T00:00:00');
END
GO
IF NOT EXISTS (SELECT 1 FROM [dbo].[clientes] WHERE id = 25)
BEGIN
    INSERT INTO [dbo].[clientes] (id, nome, documento, regiao, cultura_principal, rtv_id, ativo, created_at, updated_at)
    VALUES (25, 'Fazenda São Judas', '44.887.756/0001-53', 'Rondonópolis-MT', 'Soja', 6, 1, '2025-06-19T00:00:00', '2026-02-09T00:00:00');
END
GO
IF NOT EXISTS (SELECT 1 FROM [dbo].[clientes] WHERE id = 26)
BEGIN
    INSERT INTO [dbo].[clientes] (id, nome, documento, regiao, cultura_principal, rtv_id, ativo, created_at, updated_at)
    VALUES (26, 'Cooperativa Comigo', '47.545.261/0001-68', 'Sinop-MT', 'Soja', 7, 1, '2025-06-20T00:00:00', '2026-02-09T00:00:00');
END
GO
IF NOT EXISTS (SELECT 1 FROM [dbo].[clientes] WHERE id = 27)
BEGIN
    INSERT INTO [dbo].[clientes] (id, nome, documento, regiao, cultura_principal, rtv_id, ativo, created_at, updated_at)
    VALUES (27, 'Fazenda Xingu', '43.612.880/0001-32', 'Rio Verde-GO', 'Cana-de-açúcar', 8, 1, '2025-06-21T00:00:00', '2026-02-09T00:00:00');
END
GO
IF NOT EXISTS (SELECT 1 FROM [dbo].[clientes] WHERE id = 28)
BEGIN
    INSERT INTO [dbo].[clientes] (id, nome, documento, regiao, cultura_principal, rtv_id, ativo, created_at, updated_at)
    VALUES (28, 'Agrícola Vale do Sol', '23.991.740/0001-48', 'Cristalina-GO', 'Cana-de-açúcar', 9, 1, '2025-06-22T00:00:00', '2026-02-09T00:00:00');
END
GO
IF NOT EXISTS (SELECT 1 FROM [dbo].[clientes] WHERE id = 29)
BEGIN
    INSERT INTO [dbo].[clientes] (id, nome, documento, regiao, cultura_principal, rtv_id, ativo, created_at, updated_at)
    VALUES (29, 'Fazenda Estrela Dalva', '87.303.256/0001-57', 'Uberaba-MG', 'Milho', 10, 1, '2025-06-23T00:00:00', '2026-02-09T00:00:00');
END
GO
IF NOT EXISTS (SELECT 1 FROM [dbo].[clientes] WHERE id = 30)
BEGIN
    INSERT INTO [dbo].[clientes] (id, nome, documento, regiao, cultura_principal, rtv_id, ativo, created_at, updated_at)
    VALUES (30, 'Fazenda Ipê Roxo', '79.897.643/0001-10', 'Primavera do Leste-MT', 'Cana-de-açúcar', 11, 1, '2025-06-24T00:00:00', '2026-02-09T00:00:00');
END
GO

SET IDENTITY_INSERT [dbo].[clientes] OFF;
GO

-- ============================================================
-- SEED: precos_por_janela
-- ============================================================
SET IDENTITY_INSERT [dbo].[precos_por_janela] ON;
GO

IF NOT EXISTS (SELECT 1 FROM [dbo].[precos_por_janela] WHERE id = 1)
BEGIN
    INSERT INTO [dbo].[precos_por_janela] (id, produto_id, janela_mes, janela_ano, condicao_pagamento, preco, vigente_de, vigente_ate, created_at, updated_at)
    VALUES (1, 1, 1, 2026, '90 dias', 193.08, '2026-01-01', '2026-01-28', '2025-08-13T00:00:00', '2026-02-14T00:00:00');
END
GO
IF NOT EXISTS (SELECT 1 FROM [dbo].[precos_por_janela] WHERE id = 2)
BEGIN
    INSERT INTO [dbo].[precos_por_janela] (id, produto_id, janela_mes, janela_ano, condicao_pagamento, preco, vigente_de, vigente_ate, created_at, updated_at)
    VALUES (2, 1, 1, 2026, '30 dias', 178.77, '2026-01-01', '2026-01-28', '2025-08-13T00:00:00', '2026-02-14T00:00:00');
END
GO
IF NOT EXISTS (SELECT 1 FROM [dbo].[precos_por_janela] WHERE id = 3)
BEGIN
    INSERT INTO [dbo].[precos_por_janela] (id, produto_id, janela_mes, janela_ano, condicao_pagamento, preco, vigente_de, vigente_ate, created_at, updated_at)
    VALUES (3, 2, 1, 2026, '30 dias', 26.77, '2026-01-01', '2026-01-28', '2025-08-13T00:00:00', '2026-02-14T00:00:00');
END
GO
IF NOT EXISTS (SELECT 1 FROM [dbo].[precos_por_janela] WHERE id = 4)
BEGIN
    INSERT INTO [dbo].[precos_por_janela] (id, produto_id, janela_mes, janela_ano, condicao_pagamento, preco, vigente_de, vigente_ate, created_at, updated_at)
    VALUES (4, 2, 1, 2026, '90 dias', 28.92, '2026-01-01', '2026-01-28', '2025-08-13T00:00:00', '2026-02-14T00:00:00');
END
GO
IF NOT EXISTS (SELECT 1 FROM [dbo].[precos_por_janela] WHERE id = 5)
BEGIN
    INSERT INTO [dbo].[precos_por_janela] (id, produto_id, janela_mes, janela_ano, condicao_pagamento, preco, vigente_de, vigente_ate, created_at, updated_at)
    VALUES (5, 3, 6, 2026, '60 dias', 107.17, '2026-06-01', '2026-06-28', '2025-08-13T00:00:00', '2026-02-14T00:00:00');
END
GO
IF NOT EXISTS (SELECT 1 FROM [dbo].[precos_por_janela] WHERE id = 6)
BEGIN
    INSERT INTO [dbo].[precos_por_janela] (id, produto_id, janela_mes, janela_ano, condicao_pagamento, preco, vigente_de, vigente_ate, created_at, updated_at)
    VALUES (6, 3, 6, 2026, 'À vista', 99.96, '2026-06-01', '2026-06-28', '2025-08-13T00:00:00', '2026-02-14T00:00:00');
END
GO
IF NOT EXISTS (SELECT 1 FROM [dbo].[precos_por_janela] WHERE id = 7)
BEGIN
    INSERT INTO [dbo].[precos_por_janela] (id, produto_id, janela_mes, janela_ano, condicao_pagamento, preco, vigente_de, vigente_ate, created_at, updated_at)
    VALUES (7, 4, 2, 2026, '90 dias', 86.83, '2026-02-01', '2026-02-28', '2025-08-13T00:00:00', '2026-02-14T00:00:00');
END
GO
IF NOT EXISTS (SELECT 1 FROM [dbo].[precos_por_janela] WHERE id = 8)
BEGIN
    INSERT INTO [dbo].[precos_por_janela] (id, produto_id, janela_mes, janela_ano, condicao_pagamento, preco, vigente_de, vigente_ate, created_at, updated_at)
    VALUES (8, 4, 5, 2026, '90 dias', 90.68, '2026-05-01', '2026-05-28', '2025-08-13T00:00:00', '2026-02-14T00:00:00');
END
GO
IF NOT EXISTS (SELECT 1 FROM [dbo].[precos_por_janela] WHERE id = 9)
BEGIN
    INSERT INTO [dbo].[precos_por_janela] (id, produto_id, janela_mes, janela_ano, condicao_pagamento, preco, vigente_de, vigente_ate, created_at, updated_at)
    VALUES (9, 4, 5, 2026, '60 dias', 87.32, '2026-05-01', '2026-05-28', '2025-08-13T00:00:00', '2026-02-14T00:00:00');
END
GO
IF NOT EXISTS (SELECT 1 FROM [dbo].[precos_por_janela] WHERE id = 10)
BEGIN
    INSERT INTO [dbo].[precos_por_janela] (id, produto_id, janela_mes, janela_ano, condicao_pagamento, preco, vigente_de, vigente_ate, created_at, updated_at)
    VALUES (10, 5, 1, 2026, '30 dias', 221.79, '2026-01-01', '2026-01-28', '2025-08-13T00:00:00', '2026-02-14T00:00:00');
END
GO
IF NOT EXISTS (SELECT 1 FROM [dbo].[precos_por_janela] WHERE id = 11)
BEGIN
    INSERT INTO [dbo].[precos_por_janela] (id, produto_id, janela_mes, janela_ano, condicao_pagamento, preco, vigente_de, vigente_ate, created_at, updated_at)
    VALUES (11, 5, 2, 2026, '30 dias', 225.12, '2026-02-01', '2026-02-28', '2025-08-13T00:00:00', '2026-02-14T00:00:00');
END
GO
IF NOT EXISTS (SELECT 1 FROM [dbo].[precos_por_janela] WHERE id = 12)
BEGIN
    INSERT INTO [dbo].[precos_por_janela] (id, produto_id, janela_mes, janela_ano, condicao_pagamento, preco, vigente_de, vigente_ate, created_at, updated_at)
    VALUES (12, 5, 2, 2026, '90 dias', 243.13, '2026-02-01', '2026-02-28', '2025-08-13T00:00:00', '2026-02-14T00:00:00');
END
GO
IF NOT EXISTS (SELECT 1 FROM [dbo].[precos_por_janela] WHERE id = 13)
BEGIN
    INSERT INTO [dbo].[precos_por_janela] (id, produto_id, janela_mes, janela_ano, condicao_pagamento, preco, vigente_de, vigente_ate, created_at, updated_at)
    VALUES (13, 6, 1, 2026, '30 dias', 195.03, '2026-01-01', '2026-01-28', '2025-08-13T00:00:00', '2026-02-14T00:00:00');
END
GO
IF NOT EXISTS (SELECT 1 FROM [dbo].[precos_por_janela] WHERE id = 14)
BEGIN
    INSERT INTO [dbo].[precos_por_janela] (id, produto_id, janela_mes, janela_ano, condicao_pagamento, preco, vigente_de, vigente_ate, created_at, updated_at)
    VALUES (14, 7, 3, 2026, '60 dias', 253.91, '2026-03-01', '2026-03-28', '2025-08-13T00:00:00', '2026-02-14T00:00:00');
END
GO
IF NOT EXISTS (SELECT 1 FROM [dbo].[precos_por_janela] WHERE id = 15)
BEGIN
    INSERT INTO [dbo].[precos_por_janela] (id, produto_id, janela_mes, janela_ano, condicao_pagamento, preco, vigente_de, vigente_ate, created_at, updated_at)
    VALUES (15, 8, 2, 2026, 'À vista', 42.21, '2026-02-01', '2026-02-28', '2025-08-13T00:00:00', '2026-02-14T00:00:00');
END
GO
IF NOT EXISTS (SELECT 1 FROM [dbo].[precos_por_janela] WHERE id = 16)
BEGIN
    INSERT INTO [dbo].[precos_por_janela] (id, produto_id, janela_mes, janela_ano, condicao_pagamento, preco, vigente_de, vigente_ate, created_at, updated_at)
    VALUES (16, 8, 5, 2026, 'À vista', 44.08, '2026-05-01', '2026-05-28', '2025-08-13T00:00:00', '2026-02-14T00:00:00');
END
GO
IF NOT EXISTS (SELECT 1 FROM [dbo].[precos_por_janela] WHERE id = 17)
BEGIN
    INSERT INTO [dbo].[precos_por_janela] (id, produto_id, janela_mes, janela_ano, condicao_pagamento, preco, vigente_de, vigente_ate, created_at, updated_at)
    VALUES (17, 9, 1, 2026, 'À vista', 131.32, '2026-01-01', '2026-01-28', '2025-08-13T00:00:00', '2026-02-14T00:00:00');
END
GO
IF NOT EXISTS (SELECT 1 FROM [dbo].[precos_por_janela] WHERE id = 18)
BEGIN
    INSERT INTO [dbo].[precos_por_janela] (id, produto_id, janela_mes, janela_ano, condicao_pagamento, preco, vigente_de, vigente_ate, created_at, updated_at)
    VALUES (18, 10, 4, 2026, '30 dias', 30.64, '2026-04-01', '2026-04-28', '2025-08-13T00:00:00', '2026-02-14T00:00:00');
END
GO
IF NOT EXISTS (SELECT 1 FROM [dbo].[precos_por_janela] WHERE id = 19)
BEGIN
    INSERT INTO [dbo].[precos_por_janela] (id, produto_id, janela_mes, janela_ano, condicao_pagamento, preco, vigente_de, vigente_ate, created_at, updated_at)
    VALUES (19, 10, 1, 2026, '90 dias', 31.67, '2026-01-01', '2026-01-28', '2025-08-13T00:00:00', '2026-02-14T00:00:00');
END
GO
IF NOT EXISTS (SELECT 1 FROM [dbo].[precos_por_janela] WHERE id = 20)
BEGIN
    INSERT INTO [dbo].[precos_por_janela] (id, produto_id, janela_mes, janela_ano, condicao_pagamento, preco, vigente_de, vigente_ate, created_at, updated_at)
    VALUES (20, 10, 1, 2026, '30 dias', 29.33, '2026-01-01', '2026-01-28', '2025-08-13T00:00:00', '2026-02-14T00:00:00');
END
GO
IF NOT EXISTS (SELECT 1 FROM [dbo].[precos_por_janela] WHERE id = 21)
BEGIN
    INSERT INTO [dbo].[precos_por_janela] (id, produto_id, janela_mes, janela_ano, condicao_pagamento, preco, vigente_de, vigente_ate, created_at, updated_at)
    VALUES (21, 11, 5, 2026, '60 dias', 82.21, '2026-05-01', '2026-05-28', '2025-08-13T00:00:00', '2026-02-14T00:00:00');
END
GO
IF NOT EXISTS (SELECT 1 FROM [dbo].[precos_por_janela] WHERE id = 22)
BEGIN
    INSERT INTO [dbo].[precos_por_janela] (id, produto_id, janela_mes, janela_ano, condicao_pagamento, preco, vigente_de, vigente_ate, created_at, updated_at)
    VALUES (22, 11, 5, 2026, 'À vista', 76.68, '2026-05-01', '2026-05-28', '2025-08-13T00:00:00', '2026-02-14T00:00:00');
END
GO
IF NOT EXISTS (SELECT 1 FROM [dbo].[precos_por_janela] WHERE id = 23)
BEGIN
    INSERT INTO [dbo].[precos_por_janela] (id, produto_id, janela_mes, janela_ano, condicao_pagamento, preco, vigente_de, vigente_ate, created_at, updated_at)
    VALUES (23, 12, 2, 2026, '30 dias', 144.64, '2026-02-01', '2026-02-28', '2025-08-13T00:00:00', '2026-02-14T00:00:00');
END
GO
IF NOT EXISTS (SELECT 1 FROM [dbo].[precos_por_janela] WHERE id = 24)
BEGIN
    INSERT INTO [dbo].[precos_por_janela] (id, produto_id, janela_mes, janela_ano, condicao_pagamento, preco, vigente_de, vigente_ate, created_at, updated_at)
    VALUES (24, 12, 2, 2026, 'À vista', 140.3, '2026-02-01', '2026-02-28', '2025-08-13T00:00:00', '2026-02-14T00:00:00');
END
GO
IF NOT EXISTS (SELECT 1 FROM [dbo].[precos_por_janela] WHERE id = 25)
BEGIN
    INSERT INTO [dbo].[precos_por_janela] (id, produto_id, janela_mes, janela_ano, condicao_pagamento, preco, vigente_de, vigente_ate, created_at, updated_at)
    VALUES (25, 12, 1, 2026, '30 dias', 142.5, '2026-01-01', '2026-01-28', '2025-08-13T00:00:00', '2026-02-14T00:00:00');
END
GO
IF NOT EXISTS (SELECT 1 FROM [dbo].[precos_por_janela] WHERE id = 26)
BEGIN
    INSERT INTO [dbo].[precos_por_janela] (id, produto_id, janela_mes, janela_ano, condicao_pagamento, preco, vigente_de, vigente_ate, created_at, updated_at)
    VALUES (26, 13, 2, 2026, 'À vista', 2450.09, '2026-02-01', '2026-02-28', '2025-08-13T00:00:00', '2026-02-14T00:00:00');
END
GO
IF NOT EXISTS (SELECT 1 FROM [dbo].[precos_por_janela] WHERE id = 27)
BEGIN
    INSERT INTO [dbo].[precos_por_janela] (id, produto_id, janela_mes, janela_ano, condicao_pagamento, preco, vigente_de, vigente_ate, created_at, updated_at)
    VALUES (27, 13, 2, 2026, '60 dias', 2626.9, '2026-02-01', '2026-02-28', '2025-08-13T00:00:00', '2026-02-14T00:00:00');
END
GO
IF NOT EXISTS (SELECT 1 FROM [dbo].[precos_por_janela] WHERE id = 28)
BEGIN
    INSERT INTO [dbo].[precos_por_janela] (id, produto_id, janela_mes, janela_ano, condicao_pagamento, preco, vigente_de, vigente_ate, created_at, updated_at)
    VALUES (28, 14, 1, 2026, '30 dias', 2716.14, '2026-01-01', '2026-01-28', '2025-08-13T00:00:00', '2026-02-14T00:00:00');
END
GO
IF NOT EXISTS (SELECT 1 FROM [dbo].[precos_por_janela] WHERE id = 29)
BEGIN
    INSERT INTO [dbo].[precos_por_janela] (id, produto_id, janela_mes, janela_ano, condicao_pagamento, preco, vigente_de, vigente_ate, created_at, updated_at)
    VALUES (29, 14, 1, 2026, '60 dias', 2824.79, '2026-01-01', '2026-01-28', '2025-08-13T00:00:00', '2026-02-14T00:00:00');
END
GO
IF NOT EXISTS (SELECT 1 FROM [dbo].[precos_por_janela] WHERE id = 30)
BEGIN
    INSERT INTO [dbo].[precos_por_janela] (id, produto_id, janela_mes, janela_ano, condicao_pagamento, preco, vigente_de, vigente_ate, created_at, updated_at)
    VALUES (30, 14, 2, 2026, 'À vista', 2674.18, '2026-02-01', '2026-02-28', '2025-08-13T00:00:00', '2026-02-14T00:00:00');
END
GO
IF NOT EXISTS (SELECT 1 FROM [dbo].[precos_por_janela] WHERE id = 31)
BEGIN
    INSERT INTO [dbo].[precos_por_janela] (id, produto_id, janela_mes, janela_ano, condicao_pagamento, preco, vigente_de, vigente_ate, created_at, updated_at)
    VALUES (31, 14, 2, 2026, '60 dias', 2867.16, '2026-02-01', '2026-02-28', '2025-08-13T00:00:00', '2026-02-14T00:00:00');
END
GO
IF NOT EXISTS (SELECT 1 FROM [dbo].[precos_por_janela] WHERE id = 32)
BEGIN
    INSERT INTO [dbo].[precos_por_janela] (id, produto_id, janela_mes, janela_ano, condicao_pagamento, preco, vigente_de, vigente_ate, created_at, updated_at)
    VALUES (32, 15, 2, 2026, '60 dias', 4378.54, '2026-02-01', '2026-02-28', '2025-08-13T00:00:00', '2026-02-14T00:00:00');
END
GO
IF NOT EXISTS (SELECT 1 FROM [dbo].[precos_por_janela] WHERE id = 33)
BEGIN
    INSERT INTO [dbo].[precos_por_janela] (id, produto_id, janela_mes, janela_ano, condicao_pagamento, preco, vigente_de, vigente_ate, created_at, updated_at)
    VALUES (33, 15, 2, 2026, '30 dias', 4210.13, '2026-02-01', '2026-02-28', '2025-08-13T00:00:00', '2026-02-14T00:00:00');
END
GO
IF NOT EXISTS (SELECT 1 FROM [dbo].[precos_por_janela] WHERE id = 34)
BEGIN
    INSERT INTO [dbo].[precos_por_janela] (id, produto_id, janela_mes, janela_ano, condicao_pagamento, preco, vigente_de, vigente_ate, created_at, updated_at)
    VALUES (34, 15, 6, 2026, '90 dias', 4815.73, '2026-06-01', '2026-06-28', '2025-08-13T00:00:00', '2026-02-14T00:00:00');
END
GO
IF NOT EXISTS (SELECT 1 FROM [dbo].[precos_por_janela] WHERE id = 35)
BEGIN
    INSERT INTO [dbo].[precos_por_janela] (id, produto_id, janela_mes, janela_ano, condicao_pagamento, preco, vigente_de, vigente_ate, created_at, updated_at)
    VALUES (35, 16, 5, 2026, '30 dias', 3826.15, '2026-05-01', '2026-05-28', '2025-08-13T00:00:00', '2026-02-14T00:00:00');
END
GO
IF NOT EXISTS (SELECT 1 FROM [dbo].[precos_por_janela] WHERE id = 36)
BEGIN
    INSERT INTO [dbo].[precos_por_janela] (id, produto_id, janela_mes, janela_ano, condicao_pagamento, preco, vigente_de, vigente_ate, created_at, updated_at)
    VALUES (36, 16, 6, 2026, '60 dias', 4035.5, '2026-06-01', '2026-06-28', '2025-08-13T00:00:00', '2026-02-14T00:00:00');
END
GO
IF NOT EXISTS (SELECT 1 FROM [dbo].[precos_por_janela] WHERE id = 37)
BEGIN
    INSERT INTO [dbo].[precos_por_janela] (id, produto_id, janela_mes, janela_ano, condicao_pagamento, preco, vigente_de, vigente_ate, created_at, updated_at)
    VALUES (37, 17, 6, 2026, 'À vista', 2826.2, '2026-06-01', '2026-06-28', '2025-08-13T00:00:00', '2026-02-14T00:00:00');
END
GO
IF NOT EXISTS (SELECT 1 FROM [dbo].[precos_por_janela] WHERE id = 38)
BEGIN
    INSERT INTO [dbo].[precos_por_janela] (id, produto_id, janela_mes, janela_ano, condicao_pagamento, preco, vigente_de, vigente_ate, created_at, updated_at)
    VALUES (38, 18, 5, 2026, '30 dias', 3999.85, '2026-05-01', '2026-05-28', '2025-08-13T00:00:00', '2026-02-14T00:00:00');
END
GO

SET IDENTITY_INSERT [dbo].[precos_por_janela] OFF;
GO

-- ============================================================
-- SEED: pedidos
-- ============================================================
SET IDENTITY_INSERT [dbo].[pedidos] ON;
GO

IF NOT EXISTS (SELECT 1 FROM [dbo].[pedidos] WHERE id = 1)
BEGIN
    INSERT INTO [dbo].[pedidos] (id, cliente_id, rtv_id, cultura_safra, canal_origem, valor_total, observacoes, status, aprovado_por, aprovado_em, comentario_aprovacao, created_at, updated_at)
    VALUES (1, 4, 9, 'Cana-de-açúcar 2025/2026', 'Email', 68444.79, 'Pedido captado via canal informal, revisado pelo RTV.', 'Rascunho', NULL, NULL, NULL, '2025-10-03T00:00:00', '2026-02-19T00:00:00');
END
GO
IF NOT EXISTS (SELECT 1 FROM [dbo].[pedidos] WHERE id = 2)
BEGIN
    INSERT INTO [dbo].[pedidos] (id, cliente_id, rtv_id, cultura_safra, canal_origem, valor_total, observacoes, status, aprovado_por, aprovado_em, comentario_aprovacao, created_at, updated_at)
    VALUES (2, 7, 12, 'Algodão 2025/2026', 'Imagem', 7270.01, 'Pedido captado via canal informal, revisado pelo RTV.', 'Rascunho', NULL, NULL, NULL, '2025-10-04T00:00:00', '2026-02-19T00:00:00');
END
GO
IF NOT EXISTS (SELECT 1 FROM [dbo].[pedidos] WHERE id = 3)
BEGIN
    INSERT INTO [dbo].[pedidos] (id, cliente_id, rtv_id, cultura_safra, canal_origem, valor_total, observacoes, status, aprovado_por, aprovado_em, comentario_aprovacao, created_at, updated_at)
    VALUES (3, 10, 7, 'Cana-de-açúcar 2025/2026', 'Manual', 1664.9, NULL, 'Rascunho', NULL, NULL, NULL, '2025-10-05T00:00:00', '2026-02-19T00:00:00');
END
GO
IF NOT EXISTS (SELECT 1 FROM [dbo].[pedidos] WHERE id = 4)
BEGIN
    INSERT INTO [dbo].[pedidos] (id, cliente_id, rtv_id, cultura_safra, canal_origem, valor_total, observacoes, status, aprovado_por, aprovado_em, comentario_aprovacao, created_at, updated_at)
    VALUES (4, 13, 10, 'Milho 2025/2026', 'WhatsApp', 93436.5, 'Pedido captado via canal informal, revisado pelo RTV.', 'Devolvido', 'Fernanda Lopes', '2026-02-20T00:00:00', 'Cliente nunca comprou este defensivo — favor confirmar quantidade antes de reenviar.', '2025-10-06T00:00:00', '2026-02-19T00:00:00');
END
GO
IF NOT EXISTS (SELECT 1 FROM [dbo].[pedidos] WHERE id = 5)
BEGIN
    INSERT INTO [dbo].[pedidos] (id, cliente_id, rtv_id, cultura_safra, canal_origem, valor_total, observacoes, status, aprovado_por, aprovado_em, comentario_aprovacao, created_at, updated_at)
    VALUES (5, 16, 5, 'Soja/Milho (safrinha) 2025/2026', 'Email', 5991.9, 'Pedido captado via canal informal, revisado pelo RTV.', 'Rascunho', NULL, NULL, NULL, '2025-10-07T00:00:00', '2026-02-19T00:00:00');
END
GO
IF NOT EXISTS (SELECT 1 FROM [dbo].[pedidos] WHERE id = 6)
BEGIN
    INSERT INTO [dbo].[pedidos] (id, cliente_id, rtv_id, cultura_safra, canal_origem, valor_total, observacoes, status, aprovado_por, aprovado_em, comentario_aprovacao, created_at, updated_at)
    VALUES (6, 19, 8, 'Milho 2025/2026', 'Imagem', 6910.57, 'Pedido captado via canal informal, revisado pelo RTV.', 'Pendente Aprovação', NULL, NULL, NULL, '2025-10-08T00:00:00', '2026-02-19T00:00:00');
END
GO
IF NOT EXISTS (SELECT 1 FROM [dbo].[pedidos] WHERE id = 7)
BEGIN
    INSERT INTO [dbo].[pedidos] (id, cliente_id, rtv_id, cultura_safra, canal_origem, valor_total, observacoes, status, aprovado_por, aprovado_em, comentario_aprovacao, created_at, updated_at)
    VALUES (7, 22, 11, 'Cana-de-açúcar 2025/2026', 'Manual', 18833.62, NULL, 'Aprovado', 'Marcelo Andrade', '2026-02-17T00:00:00', 'Pedido consistente com o histórico do cliente. Aprovado.', '2025-10-09T00:00:00', '2026-02-19T00:00:00');
END
GO
IF NOT EXISTS (SELECT 1 FROM [dbo].[pedidos] WHERE id = 8)
BEGIN
    INSERT INTO [dbo].[pedidos] (id, cliente_id, rtv_id, cultura_safra, canal_origem, valor_total, observacoes, status, aprovado_por, aprovado_em, comentario_aprovacao, created_at, updated_at)
    VALUES (8, 25, 6, 'Soja 2025/2026', 'WhatsApp', 60060.04, 'Pedido captado via canal informal, revisado pelo RTV.', 'Rejeitado', 'Fernanda Lopes', '2026-02-16T00:00:00', 'Condição comercial divergente do praticado para a região. Rejeitado.', '2025-10-10T00:00:00', '2026-02-19T00:00:00');
END
GO
IF NOT EXISTS (SELECT 1 FROM [dbo].[pedidos] WHERE id = 9)
BEGIN
    INSERT INTO [dbo].[pedidos] (id, cliente_id, rtv_id, cultura_safra, canal_origem, valor_total, observacoes, status, aprovado_por, aprovado_em, comentario_aprovacao, created_at, updated_at)
    VALUES (9, 28, 9, 'Cana-de-açúcar 2025/2026', 'Email', 1357.22, 'Pedido captado via canal informal, revisado pelo RTV.', 'Devolvido', 'Marcelo Andrade', '2026-02-15T00:00:00', 'Cliente nunca comprou este defensivo — favor confirmar quantidade antes de reenviar.', '2025-10-11T00:00:00', '2026-02-19T00:00:00');
END
GO
IF NOT EXISTS (SELECT 1 FROM [dbo].[pedidos] WHERE id = 10)
BEGIN
    INSERT INTO [dbo].[pedidos] (id, cliente_id, rtv_id, cultura_safra, canal_origem, valor_total, observacoes, status, aprovado_por, aprovado_em, comentario_aprovacao, created_at, updated_at)
    VALUES (10, 1, 6, 'Soja 2025/2026', 'Imagem', 8588.3, 'Pedido captado via canal informal, revisado pelo RTV.', 'Rascunho', NULL, NULL, NULL, '2025-10-12T00:00:00', '2026-02-19T00:00:00');
END
GO
IF NOT EXISTS (SELECT 1 FROM [dbo].[pedidos] WHERE id = 11)
BEGIN
    INSERT INTO [dbo].[pedidos] (id, cliente_id, rtv_id, cultura_safra, canal_origem, valor_total, observacoes, status, aprovado_por, aprovado_em, comentario_aprovacao, created_at, updated_at)
    VALUES (11, 4, 9, 'Cana-de-açúcar 2025/2026', 'Manual', 20743.39, NULL, 'Pendente Aprovação', NULL, NULL, NULL, '2025-10-13T00:00:00', '2026-02-19T00:00:00');
END
GO
IF NOT EXISTS (SELECT 1 FROM [dbo].[pedidos] WHERE id = 12)
BEGIN
    INSERT INTO [dbo].[pedidos] (id, cliente_id, rtv_id, cultura_safra, canal_origem, valor_total, observacoes, status, aprovado_por, aprovado_em, comentario_aprovacao, created_at, updated_at)
    VALUES (12, 7, 12, 'Algodão 2025/2026', 'WhatsApp', 73849.89, 'Pedido captado via canal informal, revisado pelo RTV.', 'Aprovado', 'Fernanda Lopes', '2026-02-12T00:00:00', 'Pedido consistente com o histórico do cliente. Aprovado.', '2025-10-14T00:00:00', '2026-02-19T00:00:00');
END
GO
IF NOT EXISTS (SELECT 1 FROM [dbo].[pedidos] WHERE id = 13)
BEGIN
    INSERT INTO [dbo].[pedidos] (id, cliente_id, rtv_id, cultura_safra, canal_origem, valor_total, observacoes, status, aprovado_por, aprovado_em, comentario_aprovacao, created_at, updated_at)
    VALUES (13, 10, 7, 'Cana-de-açúcar 2025/2026', 'Email', 21139.67, 'Pedido captado via canal informal, revisado pelo RTV.', 'Rejeitado', 'Fernanda Lopes', '2026-02-11T00:00:00', 'Condição comercial divergente do praticado para a região. Rejeitado.', '2025-10-15T00:00:00', '2026-02-19T00:00:00');
END
GO
IF NOT EXISTS (SELECT 1 FROM [dbo].[pedidos] WHERE id = 14)
BEGIN
    INSERT INTO [dbo].[pedidos] (id, cliente_id, rtv_id, cultura_safra, canal_origem, valor_total, observacoes, status, aprovado_por, aprovado_em, comentario_aprovacao, created_at, updated_at)
    VALUES (14, 13, 10, 'Milho 2025/2026', 'Imagem', 95989.75, 'Pedido captado via canal informal, revisado pelo RTV.', 'Devolvido', 'Fernanda Lopes', '2026-02-10T00:00:00', 'Cliente nunca comprou este defensivo — favor confirmar quantidade antes de reenviar.', '2025-10-16T00:00:00', '2026-02-19T00:00:00');
END
GO
IF NOT EXISTS (SELECT 1 FROM [dbo].[pedidos] WHERE id = 15)
BEGIN
    INSERT INTO [dbo].[pedidos] (id, cliente_id, rtv_id, cultura_safra, canal_origem, valor_total, observacoes, status, aprovado_por, aprovado_em, comentario_aprovacao, created_at, updated_at)
    VALUES (15, 16, 5, 'Soja/Milho (safrinha) 2025/2026', 'Manual', 39173.76, NULL, 'Rascunho', NULL, NULL, NULL, '2025-10-17T00:00:00', '2026-02-19T00:00:00');
END
GO
IF NOT EXISTS (SELECT 1 FROM [dbo].[pedidos] WHERE id = 16)
BEGIN
    INSERT INTO [dbo].[pedidos] (id, cliente_id, rtv_id, cultura_safra, canal_origem, valor_total, observacoes, status, aprovado_por, aprovado_em, comentario_aprovacao, created_at, updated_at)
    VALUES (16, 19, 8, 'Milho 2025/2026', 'WhatsApp', 74037.74, 'Pedido captado via canal informal, revisado pelo RTV.', 'Pendente Aprovação', NULL, NULL, NULL, '2025-10-18T00:00:00', '2026-02-19T00:00:00');
END
GO
IF NOT EXISTS (SELECT 1 FROM [dbo].[pedidos] WHERE id = 17)
BEGIN
    INSERT INTO [dbo].[pedidos] (id, cliente_id, rtv_id, cultura_safra, canal_origem, valor_total, observacoes, status, aprovado_por, aprovado_em, comentario_aprovacao, created_at, updated_at)
    VALUES (17, 22, 11, 'Cana-de-açúcar 2025/2026', 'Email', 27217.65, 'Pedido captado via canal informal, revisado pelo RTV.', 'Aprovado', 'Ricardo Nunes', '2026-02-07T00:00:00', 'Pedido consistente com o histórico do cliente. Aprovado.', '2025-10-19T00:00:00', '2026-02-19T00:00:00');
END
GO
IF NOT EXISTS (SELECT 1 FROM [dbo].[pedidos] WHERE id = 18)
BEGIN
    INSERT INTO [dbo].[pedidos] (id, cliente_id, rtv_id, cultura_safra, canal_origem, valor_total, observacoes, status, aprovado_por, aprovado_em, comentario_aprovacao, created_at, updated_at)
    VALUES (18, 25, 6, 'Soja 2025/2026', 'Imagem', 24590.76, 'Pedido captado via canal informal, revisado pelo RTV.', 'Rejeitado', 'Ricardo Nunes', '2026-02-06T00:00:00', 'Condição comercial divergente do praticado para a região. Rejeitado.', '2025-10-20T00:00:00', '2026-02-19T00:00:00');
END
GO
IF NOT EXISTS (SELECT 1 FROM [dbo].[pedidos] WHERE id = 19)
BEGIN
    INSERT INTO [dbo].[pedidos] (id, cliente_id, rtv_id, cultura_safra, canal_origem, valor_total, observacoes, status, aprovado_por, aprovado_em, comentario_aprovacao, created_at, updated_at)
    VALUES (19, 28, 9, 'Cana-de-açúcar 2025/2026', 'Manual', 16168.52, NULL, 'Devolvido', 'Marcelo Andrade', '2026-02-05T00:00:00', 'Cliente nunca comprou este defensivo — favor confirmar quantidade antes de reenviar.', '2025-10-21T00:00:00', '2026-02-19T00:00:00');
END
GO
IF NOT EXISTS (SELECT 1 FROM [dbo].[pedidos] WHERE id = 20)
BEGIN
    INSERT INTO [dbo].[pedidos] (id, cliente_id, rtv_id, cultura_safra, canal_origem, valor_total, observacoes, status, aprovado_por, aprovado_em, comentario_aprovacao, created_at, updated_at)
    VALUES (20, 1, 6, 'Soja 2025/2026', 'WhatsApp', 3162.88, 'Pedido captado via canal informal, revisado pelo RTV.', 'Rascunho', NULL, NULL, NULL, '2025-10-22T00:00:00', '2026-02-19T00:00:00');
END
GO
IF NOT EXISTS (SELECT 1 FROM [dbo].[pedidos] WHERE id = 21)
BEGIN
    INSERT INTO [dbo].[pedidos] (id, cliente_id, rtv_id, cultura_safra, canal_origem, valor_total, observacoes, status, aprovado_por, aprovado_em, comentario_aprovacao, created_at, updated_at)
    VALUES (21, 4, 9, 'Cana-de-açúcar 2025/2026', 'Email', 62647.58, 'Pedido captado via canal informal, revisado pelo RTV.', 'Pendente Aprovação', NULL, NULL, NULL, '2025-10-23T00:00:00', '2026-02-19T00:00:00');
END
GO
IF NOT EXISTS (SELECT 1 FROM [dbo].[pedidos] WHERE id = 22)
BEGIN
    INSERT INTO [dbo].[pedidos] (id, cliente_id, rtv_id, cultura_safra, canal_origem, valor_total, observacoes, status, aprovado_por, aprovado_em, comentario_aprovacao, created_at, updated_at)
    VALUES (22, 7, 12, 'Algodão 2025/2026', 'Imagem', 14745.4, 'Pedido captado via canal informal, revisado pelo RTV.', 'Aprovado', 'Marcelo Andrade', '2026-02-02T00:00:00', 'Pedido consistente com o histórico do cliente. Aprovado.', '2025-10-24T00:00:00', '2026-02-19T00:00:00');
END
GO
IF NOT EXISTS (SELECT 1 FROM [dbo].[pedidos] WHERE id = 23)
BEGIN
    INSERT INTO [dbo].[pedidos] (id, cliente_id, rtv_id, cultura_safra, canal_origem, valor_total, observacoes, status, aprovado_por, aprovado_em, comentario_aprovacao, created_at, updated_at)
    VALUES (23, 10, 7, 'Cana-de-açúcar 2025/2026', 'Manual', 1843.52, NULL, 'Rejeitado', 'Fernanda Lopes', '2026-02-01T00:00:00', 'Condição comercial divergente do praticado para a região. Rejeitado.', '2025-10-25T00:00:00', '2026-02-19T00:00:00');
END
GO
IF NOT EXISTS (SELECT 1 FROM [dbo].[pedidos] WHERE id = 24)
BEGIN
    INSERT INTO [dbo].[pedidos] (id, cliente_id, rtv_id, cultura_safra, canal_origem, valor_total, observacoes, status, aprovado_por, aprovado_em, comentario_aprovacao, created_at, updated_at)
    VALUES (24, 13, 10, 'Milho 2025/2026', 'WhatsApp', 170277.5, 'Pedido captado via canal informal, revisado pelo RTV.', 'Devolvido', 'Ricardo Nunes', '2026-01-31T00:00:00', 'Cliente nunca comprou este defensivo — favor confirmar quantidade antes de reenviar.', '2025-10-26T00:00:00', '2026-02-19T00:00:00');
END
GO
IF NOT EXISTS (SELECT 1 FROM [dbo].[pedidos] WHERE id = 25)
BEGIN
    INSERT INTO [dbo].[pedidos] (id, cliente_id, rtv_id, cultura_safra, canal_origem, valor_total, observacoes, status, aprovado_por, aprovado_em, comentario_aprovacao, created_at, updated_at)
    VALUES (25, 16, 5, 'Soja/Milho (safrinha) 2025/2026', 'Email', 4373.18, 'Pedido captado via canal informal, revisado pelo RTV.', 'Rascunho', NULL, NULL, NULL, '2025-10-27T00:00:00', '2026-02-19T00:00:00');
END
GO

SET IDENTITY_INSERT [dbo].[pedidos] OFF;
GO

-- ============================================================
-- SEED: pedido_itens
-- ============================================================
SET IDENTITY_INSERT [dbo].[pedido_itens] ON;
GO

IF NOT EXISTS (SELECT 1 FROM [dbo].[pedido_itens] WHERE id = 1)
BEGIN
    INSERT INTO [dbo].[pedido_itens] (id, pedido_id, produto_id, quantidade, unidade, janela_mes, janela_ano, formato_entrega, local_entrega, condicao_pagamento, preco_unitario, subtotal, created_at, updated_at)
    VALUES (1, 1, 17, 23.43, 't', 6, 2026, 'CIF', 'Filial LDC Rondonópolis', 'À vista', 2826.2, 66217.87, '2025-10-03T00:00:00', '2026-02-19T00:00:00');
END
GO
IF NOT EXISTS (SELECT 1 FROM [dbo].[pedido_itens] WHERE id = 2)
BEGIN
    INSERT INTO [dbo].[pedido_itens] (id, pedido_id, produto_id, quantidade, unidade, janela_mes, janela_ano, formato_entrega, local_entrega, condicao_pagamento, preco_unitario, subtotal, created_at, updated_at)
    VALUES (2, 1, 8, 50.52, 'L', 5, 2026, 'Entrega Programada', 'Filial LDC Rondonópolis', 'À vista', 44.08, 2226.92, '2025-10-03T00:00:00', '2026-02-19T00:00:00');
END
GO
IF NOT EXISTS (SELECT 1 FROM [dbo].[pedido_itens] WHERE id = 3)
BEGIN
    INSERT INTO [dbo].[pedido_itens] (id, pedido_id, produto_id, quantidade, unidade, janela_mes, janela_ano, formato_entrega, local_entrega, condicao_pagamento, preco_unitario, subtotal, created_at, updated_at)
    VALUES (3, 2, 11, 6.07, 'L', 5, 2026, 'Entrega Programada', 'Armazém Fazenda', '60 dias', 82.21, 499.01, '2025-10-04T00:00:00', '2026-02-19T00:00:00');
END
GO
IF NOT EXISTS (SELECT 1 FROM [dbo].[pedido_itens] WHERE id = 4)
BEGIN
    INSERT INTO [dbo].[pedido_itens] (id, pedido_id, produto_id, quantidade, unidade, janela_mes, janela_ano, formato_entrega, local_entrega, condicao_pagamento, preco_unitario, subtotal, created_at, updated_at)
    VALUES (4, 2, 3, 63.18, 'L', 6, 2026, 'CIF', 'Filial LDC Rondonópolis', '60 dias', 107.17, 6771.0, '2025-10-04T00:00:00', '2026-02-19T00:00:00');
END
GO
IF NOT EXISTS (SELECT 1 FROM [dbo].[pedido_itens] WHERE id = 5)
BEGIN
    INSERT INTO [dbo].[pedido_itens] (id, pedido_id, produto_id, quantidade, unidade, janela_mes, janela_ano, formato_entrega, local_entrega, condicao_pagamento, preco_unitario, subtotal, created_at, updated_at)
    VALUES (5, 3, 8, 37.77, 'L', 5, 2026, 'FOB', 'Filial LDC Rondonópolis', 'À vista', 44.08, 1664.9, '2025-10-05T00:00:00', '2026-02-19T00:00:00');
END
GO
IF NOT EXISTS (SELECT 1 FROM [dbo].[pedido_itens] WHERE id = 6)
BEGIN
    INSERT INTO [dbo].[pedido_itens] (id, pedido_id, produto_id, quantidade, unidade, janela_mes, janela_ano, formato_entrega, local_entrega, condicao_pagamento, preco_unitario, subtotal, created_at, updated_at)
    VALUES (6, 4, 18, 23.36, 't', 5, 2026, 'CIF', 'Filial LDC Sorriso', '30 dias', 3999.85, 93436.5, '2025-10-06T00:00:00', '2026-02-19T00:00:00');
END
GO
IF NOT EXISTS (SELECT 1 FROM [dbo].[pedido_itens] WHERE id = 7)
BEGIN
    INSERT INTO [dbo].[pedido_itens] (id, pedido_id, produto_id, quantidade, unidade, janela_mes, janela_ano, formato_entrega, local_entrega, condicao_pagamento, preco_unitario, subtotal, created_at, updated_at)
    VALUES (7, 5, 4, 68.62, 'L', 5, 2026, 'FOB', 'Filial LDC Rondonópolis', '60 dias', 87.32, 5991.9, '2025-10-07T00:00:00', '2026-02-19T00:00:00');
END
GO
IF NOT EXISTS (SELECT 1 FROM [dbo].[pedido_itens] WHERE id = 8)
BEGIN
    INSERT INTO [dbo].[pedido_itens] (id, pedido_id, produto_id, quantidade, unidade, janela_mes, janela_ano, formato_entrega, local_entrega, condicao_pagamento, preco_unitario, subtotal, created_at, updated_at)
    VALUES (8, 6, 11, 84.06, 'L', 5, 2026, 'FOB', 'Porto Seco Rio Verde', '60 dias', 82.21, 6910.57, '2025-10-08T00:00:00', '2026-02-19T00:00:00');
END
GO
IF NOT EXISTS (SELECT 1 FROM [dbo].[pedido_itens] WHERE id = 9)
BEGIN
    INSERT INTO [dbo].[pedido_itens] (id, pedido_id, produto_id, quantidade, unidade, janela_mes, janela_ano, formato_entrega, local_entrega, condicao_pagamento, preco_unitario, subtotal, created_at, updated_at)
    VALUES (9, 7, 2, 77.94, 'L', 1, 2026, 'FOB', 'Armazém Fazenda', '30 dias', 26.77, 2086.45, '2025-10-09T00:00:00', '2026-02-19T00:00:00');
END
GO
IF NOT EXISTS (SELECT 1 FROM [dbo].[pedido_itens] WHERE id = 10)
BEGIN
    INSERT INTO [dbo].[pedido_itens] (id, pedido_id, produto_id, quantidade, unidade, janela_mes, janela_ano, formato_entrega, local_entrega, condicao_pagamento, preco_unitario, subtotal, created_at, updated_at)
    VALUES (10, 7, 1, 93.68, 'L', 1, 2026, 'Entrega Programada', 'Filial LDC Rondonópolis', '30 dias', 178.77, 16747.17, '2025-10-09T00:00:00', '2026-02-19T00:00:00');
END
GO
IF NOT EXISTS (SELECT 1 FROM [dbo].[pedido_itens] WHERE id = 11)
BEGIN
    INSERT INTO [dbo].[pedido_itens] (id, pedido_id, produto_id, quantidade, unidade, janela_mes, janela_ano, formato_entrega, local_entrega, condicao_pagamento, preco_unitario, subtotal, created_at, updated_at)
    VALUES (11, 8, 18, 14.46, 't', 5, 2026, 'CIF', 'Armazém Fazenda', '30 dias', 3999.85, 57837.83, '2025-10-10T00:00:00', '2026-02-19T00:00:00');
END
GO
IF NOT EXISTS (SELECT 1 FROM [dbo].[pedido_itens] WHERE id = 12)
BEGIN
    INSERT INTO [dbo].[pedido_itens] (id, pedido_id, produto_id, quantidade, unidade, janela_mes, janela_ano, formato_entrega, local_entrega, condicao_pagamento, preco_unitario, subtotal, created_at, updated_at)
    VALUES (12, 8, 5, 9.14, 'L', 2, 2026, 'FOB', 'Filial LDC Sorriso', '90 dias', 243.13, 2222.21, '2025-10-10T00:00:00', '2026-02-19T00:00:00');
END
GO
IF NOT EXISTS (SELECT 1 FROM [dbo].[pedido_itens] WHERE id = 13)
BEGIN
    INSERT INTO [dbo].[pedido_itens] (id, pedido_id, produto_id, quantidade, unidade, janela_mes, janela_ano, formato_entrega, local_entrega, condicao_pagamento, preco_unitario, subtotal, created_at, updated_at)
    VALUES (13, 9, 2, 46.93, 'L', 1, 2026, 'CIF', 'Filial LDC Rondonópolis', '90 dias', 28.92, 1357.22, '2025-10-11T00:00:00', '2026-02-19T00:00:00');
END
GO
IF NOT EXISTS (SELECT 1 FROM [dbo].[pedido_itens] WHERE id = 14)
BEGIN
    INSERT INTO [dbo].[pedido_itens] (id, pedido_id, produto_id, quantidade, unidade, janela_mes, janela_ano, formato_entrega, local_entrega, condicao_pagamento, preco_unitario, subtotal, created_at, updated_at)
    VALUES (14, 10, 4, 94.71, 'L', 5, 2026, 'FOB', 'Filial LDC Sorriso', '90 dias', 90.68, 8588.3, '2025-10-12T00:00:00', '2026-02-19T00:00:00');
END
GO
IF NOT EXISTS (SELECT 1 FROM [dbo].[pedido_itens] WHERE id = 15)
BEGIN
    INSERT INTO [dbo].[pedido_itens] (id, pedido_id, produto_id, quantidade, unidade, janela_mes, janela_ano, formato_entrega, local_entrega, condicao_pagamento, preco_unitario, subtotal, created_at, updated_at)
    VALUES (15, 11, 6, 106.36, 'L', 1, 2026, 'CIF', 'Filial LDC Sorriso', '30 dias', 195.03, 20743.39, '2025-10-13T00:00:00', '2026-02-19T00:00:00');
END
GO
IF NOT EXISTS (SELECT 1 FROM [dbo].[pedido_itens] WHERE id = 16)
BEGIN
    INSERT INTO [dbo].[pedido_itens] (id, pedido_id, produto_id, quantidade, unidade, janela_mes, janela_ano, formato_entrega, local_entrega, condicao_pagamento, preco_unitario, subtotal, created_at, updated_at)
    VALUES (16, 12, 14, 7.4, 't', 1, 2026, 'Entrega Programada', 'Armazém Fazenda', '60 dias', 2824.79, 20903.45, '2025-10-14T00:00:00', '2026-02-19T00:00:00');
END
GO
IF NOT EXISTS (SELECT 1 FROM [dbo].[pedido_itens] WHERE id = 17)
BEGIN
    INSERT INTO [dbo].[pedido_itens] (id, pedido_id, produto_id, quantidade, unidade, janela_mes, janela_ano, formato_entrega, local_entrega, condicao_pagamento, preco_unitario, subtotal, created_at, updated_at)
    VALUES (17, 12, 13, 21.61, 't', 2, 2026, 'CIF', 'Filial LDC Sorriso', 'À vista', 2450.09, 52946.44, '2025-10-14T00:00:00', '2026-02-19T00:00:00');
END
GO
IF NOT EXISTS (SELECT 1 FROM [dbo].[pedido_itens] WHERE id = 18)
BEGIN
    INSERT INTO [dbo].[pedido_itens] (id, pedido_id, produto_id, quantidade, unidade, janela_mes, janela_ano, formato_entrega, local_entrega, condicao_pagamento, preco_unitario, subtotal, created_at, updated_at)
    VALUES (18, 13, 10, 30.64, 'L', 4, 2026, 'Entrega Programada', 'Filial LDC Sorriso', '30 dias', 30.64, 938.81, '2025-10-15T00:00:00', '2026-02-19T00:00:00');
END
GO
IF NOT EXISTS (SELECT 1 FROM [dbo].[pedido_itens] WHERE id = 19)
BEGIN
    INSERT INTO [dbo].[pedido_itens] (id, pedido_id, produto_id, quantidade, unidade, janela_mes, janela_ano, formato_entrega, local_entrega, condicao_pagamento, preco_unitario, subtotal, created_at, updated_at)
    VALUES (19, 13, 13, 7.69, 't', 2, 2026, 'CIF', 'Filial LDC Rondonópolis', '60 dias', 2626.9, 20200.86, '2025-10-15T00:00:00', '2026-02-19T00:00:00');
END
GO
IF NOT EXISTS (SELECT 1 FROM [dbo].[pedido_itens] WHERE id = 20)
BEGIN
    INSERT INTO [dbo].[pedido_itens] (id, pedido_id, produto_id, quantidade, unidade, janela_mes, janela_ano, formato_entrega, local_entrega, condicao_pagamento, preco_unitario, subtotal, created_at, updated_at)
    VALUES (20, 14, 18, 23.54, 't', 5, 2026, 'CIF', 'Filial LDC Rondonópolis', '30 dias', 3999.85, 94156.47, '2025-10-16T00:00:00', '2026-02-19T00:00:00');
END
GO
IF NOT EXISTS (SELECT 1 FROM [dbo].[pedido_itens] WHERE id = 21)
BEGIN
    INSERT INTO [dbo].[pedido_itens] (id, pedido_id, produto_id, quantidade, unidade, janela_mes, janela_ano, formato_entrega, local_entrega, condicao_pagamento, preco_unitario, subtotal, created_at, updated_at)
    VALUES (21, 14, 6, 9.4, 'L', 1, 2026, 'Entrega Programada', 'Porto Seco Rio Verde', '30 dias', 195.03, 1833.28, '2025-10-16T00:00:00', '2026-02-19T00:00:00');
END
GO
IF NOT EXISTS (SELECT 1 FROM [dbo].[pedido_itens] WHERE id = 22)
BEGIN
    INSERT INTO [dbo].[pedido_itens] (id, pedido_id, produto_id, quantidade, unidade, janela_mes, janela_ano, formato_entrega, local_entrega, condicao_pagamento, preco_unitario, subtotal, created_at, updated_at)
    VALUES (22, 15, 14, 10.24, 't', 1, 2026, 'Entrega Programada', 'Filial LDC Sorriso', '30 dias', 2716.14, 27813.27, '2025-10-17T00:00:00', '2026-02-19T00:00:00');
END
GO
IF NOT EXISTS (SELECT 1 FROM [dbo].[pedido_itens] WHERE id = 23)
BEGIN
    INSERT INTO [dbo].[pedido_itens] (id, pedido_id, produto_id, quantidade, unidade, janela_mes, janela_ano, formato_entrega, local_entrega, condicao_pagamento, preco_unitario, subtotal, created_at, updated_at)
    VALUES (23, 15, 9, 86.51, 'L', 1, 2026, 'CIF', 'Filial LDC Sorriso', 'À vista', 131.32, 11360.49, '2025-10-17T00:00:00', '2026-02-19T00:00:00');
END
GO
IF NOT EXISTS (SELECT 1 FROM [dbo].[pedido_itens] WHERE id = 24)
BEGIN
    INSERT INTO [dbo].[pedido_itens] (id, pedido_id, produto_id, quantidade, unidade, janela_mes, janela_ano, formato_entrega, local_entrega, condicao_pagamento, preco_unitario, subtotal, created_at, updated_at)
    VALUES (24, 16, 14, 23.77, 't', 1, 2026, 'FOB', 'Filial LDC Rondonópolis', '30 dias', 2716.14, 64562.65, '2025-10-18T00:00:00', '2026-02-19T00:00:00');
END
GO
IF NOT EXISTS (SELECT 1 FROM [dbo].[pedido_itens] WHERE id = 25)
BEGIN
    INSERT INTO [dbo].[pedido_itens] (id, pedido_id, produto_id, quantidade, unidade, janela_mes, janela_ano, formato_entrega, local_entrega, condicao_pagamento, preco_unitario, subtotal, created_at, updated_at)
    VALUES (25, 16, 4, 108.51, 'L', 5, 2026, 'Entrega Programada', 'Filial LDC Rondonópolis', '60 dias', 87.32, 9475.09, '2025-10-18T00:00:00', '2026-02-19T00:00:00');
END
GO
IF NOT EXISTS (SELECT 1 FROM [dbo].[pedido_itens] WHERE id = 26)
BEGIN
    INSERT INTO [dbo].[pedido_itens] (id, pedido_id, produto_id, quantidade, unidade, janela_mes, janela_ano, formato_entrega, local_entrega, condicao_pagamento, preco_unitario, subtotal, created_at, updated_at)
    VALUES (26, 17, 11, 85.18, 'L', 5, 2026, 'Entrega Programada', 'Filial LDC Sorriso', 'À vista', 76.68, 6531.6, '2025-10-19T00:00:00', '2026-02-19T00:00:00');
END
GO
IF NOT EXISTS (SELECT 1 FROM [dbo].[pedido_itens] WHERE id = 27)
BEGIN
    INSERT INTO [dbo].[pedido_itens] (id, pedido_id, produto_id, quantidade, unidade, janela_mes, janela_ano, formato_entrega, local_entrega, condicao_pagamento, preco_unitario, subtotal, created_at, updated_at)
    VALUES (27, 17, 7, 81.47, 'L', 3, 2026, 'FOB', 'Filial LDC Sorriso', '60 dias', 253.91, 20686.05, '2025-10-19T00:00:00', '2026-02-19T00:00:00');
END
GO
IF NOT EXISTS (SELECT 1 FROM [dbo].[pedido_itens] WHERE id = 28)
BEGIN
    INSERT INTO [dbo].[pedido_itens] (id, pedido_id, produto_id, quantidade, unidade, janela_mes, janela_ano, formato_entrega, local_entrega, condicao_pagamento, preco_unitario, subtotal, created_at, updated_at)
    VALUES (28, 18, 13, 8.29, 't', 2, 2026, 'CIF', 'Porto Seco Rio Verde', 'À vista', 2450.09, 20311.25, '2025-10-20T00:00:00', '2026-02-19T00:00:00');
END
GO
IF NOT EXISTS (SELECT 1 FROM [dbo].[pedido_itens] WHERE id = 29)
BEGIN
    INSERT INTO [dbo].[pedido_itens] (id, pedido_id, produto_id, quantidade, unidade, janela_mes, janela_ano, formato_entrega, local_entrega, condicao_pagamento, preco_unitario, subtotal, created_at, updated_at)
    VALUES (29, 18, 11, 55.81, 'L', 5, 2026, 'Entrega Programada', 'Filial LDC Sorriso', 'À vista', 76.68, 4279.51, '2025-10-20T00:00:00', '2026-02-19T00:00:00');
END
GO
IF NOT EXISTS (SELECT 1 FROM [dbo].[pedido_itens] WHERE id = 30)
BEGIN
    INSERT INTO [dbo].[pedido_itens] (id, pedido_id, produto_id, quantidade, unidade, janela_mes, janela_ano, formato_entrega, local_entrega, condicao_pagamento, preco_unitario, subtotal, created_at, updated_at)
    VALUES (30, 19, 6, 37.64, 'L', 1, 2026, 'Entrega Programada', 'Filial LDC Rondonópolis', '30 dias', 195.03, 7340.93, '2025-10-21T00:00:00', '2026-02-19T00:00:00');
END
GO
IF NOT EXISTS (SELECT 1 FROM [dbo].[pedido_itens] WHERE id = 31)
BEGIN
    INSERT INTO [dbo].[pedido_itens] (id, pedido_id, produto_id, quantidade, unidade, janela_mes, janela_ano, formato_entrega, local_entrega, condicao_pagamento, preco_unitario, subtotal, created_at, updated_at)
    VALUES (31, 19, 3, 82.37, 'L', 6, 2026, 'CIF', 'Filial LDC Sorriso', '60 dias', 107.17, 8827.59, '2025-10-21T00:00:00', '2026-02-19T00:00:00');
END
GO
IF NOT EXISTS (SELECT 1 FROM [dbo].[pedido_itens] WHERE id = 32)
BEGIN
    INSERT INTO [dbo].[pedido_itens] (id, pedido_id, produto_id, quantidade, unidade, janela_mes, janela_ano, formato_entrega, local_entrega, condicao_pagamento, preco_unitario, subtotal, created_at, updated_at)
    VALUES (32, 20, 2, 118.15, 'L', 1, 2026, 'Entrega Programada', 'Armazém Fazenda', '30 dias', 26.77, 3162.88, '2025-10-22T00:00:00', '2026-02-19T00:00:00');
END
GO
IF NOT EXISTS (SELECT 1 FROM [dbo].[pedido_itens] WHERE id = 33)
BEGIN
    INSERT INTO [dbo].[pedido_itens] (id, pedido_id, produto_id, quantidade, unidade, janela_mes, janela_ano, formato_entrega, local_entrega, condicao_pagamento, preco_unitario, subtotal, created_at, updated_at)
    VALUES (33, 21, 14, 18.24, 't', 1, 2026, 'FOB', 'Porto Seco Rio Verde', '60 dias', 2824.79, 51524.17, '2025-10-23T00:00:00', '2026-02-19T00:00:00');
END
GO
IF NOT EXISTS (SELECT 1 FROM [dbo].[pedido_itens] WHERE id = 34)
BEGIN
    INSERT INTO [dbo].[pedido_itens] (id, pedido_id, produto_id, quantidade, unidade, janela_mes, janela_ano, formato_entrega, local_entrega, condicao_pagamento, preco_unitario, subtotal, created_at, updated_at)
    VALUES (34, 21, 13, 4.54, 't', 2, 2026, 'Entrega Programada', 'Armazém Fazenda', 'À vista', 2450.09, 11123.41, '2025-10-23T00:00:00', '2026-02-19T00:00:00');
END
GO
IF NOT EXISTS (SELECT 1 FROM [dbo].[pedido_itens] WHERE id = 35)
BEGIN
    INSERT INTO [dbo].[pedido_itens] (id, pedido_id, produto_id, quantidade, unidade, janela_mes, janela_ano, formato_entrega, local_entrega, condicao_pagamento, preco_unitario, subtotal, created_at, updated_at)
    VALUES (35, 22, 14, 5.22, 't', 1, 2026, 'Entrega Programada', 'Porto Seco Rio Verde', '60 dias', 2824.79, 14745.4, '2025-10-24T00:00:00', '2026-02-19T00:00:00');
END
GO
IF NOT EXISTS (SELECT 1 FROM [dbo].[pedido_itens] WHERE id = 36)
BEGIN
    INSERT INTO [dbo].[pedido_itens] (id, pedido_id, produto_id, quantidade, unidade, janela_mes, janela_ano, formato_entrega, local_entrega, condicao_pagamento, preco_unitario, subtotal, created_at, updated_at)
    VALUES (36, 23, 4, 20.33, 'L', 5, 2026, 'FOB', 'Filial LDC Rondonópolis', '90 dias', 90.68, 1843.52, '2025-10-25T00:00:00', '2026-02-19T00:00:00');
END
GO
IF NOT EXISTS (SELECT 1 FROM [dbo].[pedido_itens] WHERE id = 37)
BEGIN
    INSERT INTO [dbo].[pedido_itens] (id, pedido_id, produto_id, quantidade, unidade, janela_mes, janela_ano, formato_entrega, local_entrega, condicao_pagamento, preco_unitario, subtotal, created_at, updated_at)
    VALUES (37, 24, 18, 22.53, 't', 5, 2026, 'Entrega Programada', 'Porto Seco Rio Verde', '30 dias', 3999.85, 90116.62, '2025-10-26T00:00:00', '2026-02-19T00:00:00');
END
GO
IF NOT EXISTS (SELECT 1 FROM [dbo].[pedido_itens] WHERE id = 38)
BEGIN
    INSERT INTO [dbo].[pedido_itens] (id, pedido_id, produto_id, quantidade, unidade, janela_mes, janela_ano, formato_entrega, local_entrega, condicao_pagamento, preco_unitario, subtotal, created_at, updated_at)
    VALUES (38, 24, 15, 19.04, 't', 2, 2026, 'Entrega Programada', 'Filial LDC Rondonópolis', '30 dias', 4210.13, 80160.88, '2025-10-26T00:00:00', '2026-02-19T00:00:00');
END
GO
IF NOT EXISTS (SELECT 1 FROM [dbo].[pedido_itens] WHERE id = 39)
BEGIN
    INSERT INTO [dbo].[pedido_itens] (id, pedido_id, produto_id, quantidade, unidade, janela_mes, janela_ano, formato_entrega, local_entrega, condicao_pagamento, preco_unitario, subtotal, created_at, updated_at)
    VALUES (39, 25, 8, 55.59, 'L', 5, 2026, 'Entrega Programada', 'Filial LDC Rondonópolis', 'À vista', 44.08, 2450.41, '2025-10-27T00:00:00', '2026-02-19T00:00:00');
END
GO
IF NOT EXISTS (SELECT 1 FROM [dbo].[pedido_itens] WHERE id = 40)
BEGIN
    INSERT INTO [dbo].[pedido_itens] (id, pedido_id, produto_id, quantidade, unidade, janela_mes, janela_ano, formato_entrega, local_entrega, condicao_pagamento, preco_unitario, subtotal, created_at, updated_at)
    VALUES (40, 25, 8, 43.62, 'L', 5, 2026, 'Entrega Programada', 'Armazém Fazenda', 'À vista', 44.08, 1922.77, '2025-10-27T00:00:00', '2026-02-19T00:00:00');
END
GO

SET IDENTITY_INSERT [dbo].[pedido_itens] OFF;
GO

-- ============================================================
-- SEED: alertas_consistencia
-- ============================================================
SET IDENTITY_INSERT [dbo].[alertas_consistencia] ON;
GO

IF NOT EXISTS (SELECT 1 FROM [dbo].[alertas_consistencia] WHERE id = 1)
BEGIN
    INSERT INTO [dbo].[alertas_consistencia] (id, pedido_id, tipo, descricao, severidade, resolvido_por, created_at, updated_at)
    VALUES (1, 5, 'VolumetriaAtipica', 'Quantidade solicitada está fora do padrão histórico do cliente para este produto.', 'Baixa', NULL, '2025-10-07T00:00:00', '2026-02-19T00:00:00');
END
GO
IF NOT EXISTS (SELECT 1 FROM [dbo].[alertas_consistencia] WHERE id = 2)
BEGIN
    INSERT INTO [dbo].[alertas_consistencia] (id, pedido_id, tipo, descricao, severidade, resolvido_por, created_at, updated_at)
    VALUES (2, 25, 'ProdutoAtipico', 'Cliente nunca comprou este produto anteriormente.', 'Media', NULL, '2025-10-27T00:00:00', '2026-02-19T00:00:00');
END
GO
IF NOT EXISTS (SELECT 1 FROM [dbo].[alertas_consistencia] WHERE id = 3)
BEGIN
    INSERT INTO [dbo].[alertas_consistencia] (id, pedido_id, tipo, descricao, severidade, resolvido_por, created_at, updated_at)
    VALUES (3, 8, 'VolumetriaAtipica', 'Quantidade solicitada está fora do padrão histórico do cliente para este produto.', 'Alta', 'Fernanda Lopes', '2025-10-10T00:00:00', '2026-02-19T00:00:00');
END
GO
IF NOT EXISTS (SELECT 1 FROM [dbo].[alertas_consistencia] WHERE id = 4)
BEGIN
    INSERT INTO [dbo].[alertas_consistencia] (id, pedido_id, tipo, descricao, severidade, resolvido_por, created_at, updated_at)
    VALUES (4, 13, 'CondicaoDivergente', 'Condição comercial informada diverge da política padrão para a região.', 'Baixa', 'Fernanda Lopes', '2025-10-15T00:00:00', '2026-02-19T00:00:00');
END
GO
IF NOT EXISTS (SELECT 1 FROM [dbo].[alertas_consistencia] WHERE id = 5)
BEGIN
    INSERT INTO [dbo].[alertas_consistencia] (id, pedido_id, tipo, descricao, severidade, resolvido_por, created_at, updated_at)
    VALUES (5, 24, 'CondicaoDivergente', 'Condição comercial informada diverge da política padrão para a região.', 'Media', 'Ricardo Nunes', '2025-10-26T00:00:00', '2026-02-19T00:00:00');
END
GO
IF NOT EXISTS (SELECT 1 FROM [dbo].[alertas_consistencia] WHERE id = 6)
BEGIN
    INSERT INTO [dbo].[alertas_consistencia] (id, pedido_id, tipo, descricao, severidade, resolvido_por, created_at, updated_at)
    VALUES (6, 7, 'VolumetriaAtipica', 'Quantidade solicitada está fora do padrão histórico do cliente para este produto.', 'Baixa', 'Marcelo Andrade', '2025-10-09T00:00:00', '2026-02-19T00:00:00');
END
GO
IF NOT EXISTS (SELECT 1 FROM [dbo].[alertas_consistencia] WHERE id = 7)
BEGIN
    INSERT INTO [dbo].[alertas_consistencia] (id, pedido_id, tipo, descricao, severidade, resolvido_por, created_at, updated_at)
    VALUES (7, 3, 'VolumetriaAtipica', 'Quantidade solicitada está fora do padrão histórico do cliente para este produto.', 'Media', NULL, '2025-10-05T00:00:00', '2026-02-19T00:00:00');
END
GO
IF NOT EXISTS (SELECT 1 FROM [dbo].[alertas_consistencia] WHERE id = 8)
BEGIN
    INSERT INTO [dbo].[alertas_consistencia] (id, pedido_id, tipo, descricao, severidade, resolvido_por, created_at, updated_at)
    VALUES (8, 14, 'VolumetriaAtipica', 'Quantidade solicitada está fora do padrão histórico do cliente para este produto.', 'Media', 'Fernanda Lopes', '2025-10-16T00:00:00', '2026-02-19T00:00:00');
END
GO
IF NOT EXISTS (SELECT 1 FROM [dbo].[alertas_consistencia] WHERE id = 9)
BEGIN
    INSERT INTO [dbo].[alertas_consistencia] (id, pedido_id, tipo, descricao, severidade, resolvido_por, created_at, updated_at)
    VALUES (9, 18, 'CondicaoDivergente', 'Condição comercial informada diverge da política padrão para a região.', 'Alta', 'Ricardo Nunes', '2025-10-20T00:00:00', '2026-02-19T00:00:00');
END
GO
IF NOT EXISTS (SELECT 1 FROM [dbo].[alertas_consistencia] WHERE id = 10)
BEGIN
    INSERT INTO [dbo].[alertas_consistencia] (id, pedido_id, tipo, descricao, severidade, resolvido_por, created_at, updated_at)
    VALUES (10, 11, 'CondicaoDivergente', 'Condição comercial informada diverge da política padrão para a região.', 'Alta', NULL, '2025-10-13T00:00:00', '2026-02-19T00:00:00');
END
GO
IF NOT EXISTS (SELECT 1 FROM [dbo].[alertas_consistencia] WHERE id = 11)
BEGIN
    INSERT INTO [dbo].[alertas_consistencia] (id, pedido_id, tipo, descricao, severidade, resolvido_por, created_at, updated_at)
    VALUES (11, 9, 'CondicaoDivergente', 'Condição comercial informada diverge da política padrão para a região.', 'Baixa', 'Marcelo Andrade', '2025-10-11T00:00:00', '2026-02-19T00:00:00');
END
GO
IF NOT EXISTS (SELECT 1 FROM [dbo].[alertas_consistencia] WHERE id = 12)
BEGIN
    INSERT INTO [dbo].[alertas_consistencia] (id, pedido_id, tipo, descricao, severidade, resolvido_por, created_at, updated_at)
    VALUES (12, 23, 'VolumetriaAtipica', 'Quantidade solicitada está fora do padrão histórico do cliente para este produto.', 'Baixa', 'Fernanda Lopes', '2025-10-25T00:00:00', '2026-02-19T00:00:00');
END
GO

SET IDENTITY_INSERT [dbo].[alertas_consistencia] OFF;
GO

-- ============================================================
-- SEED: recomendacoes
-- ============================================================
SET IDENTITY_INSERT [dbo].[recomendacoes] ON;
GO

IF NOT EXISTS (SELECT 1 FROM [dbo].[recomendacoes] WHERE id = 1)
BEGIN
    INSERT INTO [dbo].[recomendacoes] (id, cliente_id, produto_id, motivo, score, aceita, gerada_em, created_at, updated_at)
    VALUES (1, 1, 14, 'Sazonalidade', 0.656, 0, '2026-01-16T00:00:00', '2026-01-08T00:00:00', '2026-02-24T00:00:00');
END
GO
IF NOT EXISTS (SELECT 1 FROM [dbo].[recomendacoes] WHERE id = 2)
BEGIN
    INSERT INTO [dbo].[recomendacoes] (id, cliente_id, produto_id, motivo, score, aceita, gerada_em, created_at, updated_at)
    VALUES (2, 2, 24, 'Sazonalidade', 0.454, 0, '2026-01-20T00:00:00', '2026-01-25T00:00:00', '2026-02-24T00:00:00');
END
GO
IF NOT EXISTS (SELECT 1 FROM [dbo].[recomendacoes] WHERE id = 3)
BEGIN
    INSERT INTO [dbo].[recomendacoes] (id, cliente_id, produto_id, motivo, score, aceita, gerada_em, created_at, updated_at)
    VALUES (3, 3, 13, 'MixRegional', 0.7229, 1, '2026-01-18T00:00:00', '2026-02-01T00:00:00', '2026-02-24T00:00:00');
END
GO
IF NOT EXISTS (SELECT 1 FROM [dbo].[recomendacoes] WHERE id = 4)
BEGIN
    INSERT INTO [dbo].[recomendacoes] (id, cliente_id, produto_id, motivo, score, aceita, gerada_em, created_at, updated_at)
    VALUES (4, 4, 15, 'Sazonalidade', 0.4645, 0, '2026-02-15T00:00:00', '2026-01-30T00:00:00', '2026-02-24T00:00:00');
END
GO
IF NOT EXISTS (SELECT 1 FROM [dbo].[recomendacoes] WHERE id = 5)
BEGIN
    INSERT INTO [dbo].[recomendacoes] (id, cliente_id, produto_id, motivo, score, aceita, gerada_em, created_at, updated_at)
    VALUES (5, 5, 11, 'Sazonalidade', 0.8296, 1, '2026-01-06T00:00:00', '2026-02-02T00:00:00', '2026-02-24T00:00:00');
END
GO
IF NOT EXISTS (SELECT 1 FROM [dbo].[recomendacoes] WHERE id = 6)
BEGIN
    INSERT INTO [dbo].[recomendacoes] (id, cliente_id, produto_id, motivo, score, aceita, gerada_em, created_at, updated_at)
    VALUES (6, 6, 3, 'MixRegional', 0.6463, 0, '2026-02-06T00:00:00', '2026-02-14T00:00:00', '2026-02-24T00:00:00');
END
GO
IF NOT EXISTS (SELECT 1 FROM [dbo].[recomendacoes] WHERE id = 7)
BEGIN
    INSERT INTO [dbo].[recomendacoes] (id, cliente_id, produto_id, motivo, score, aceita, gerada_em, created_at, updated_at)
    VALUES (7, 7, 3, 'MixRegional', 0.8422, 1, '2026-02-27T00:00:00', '2026-02-13T00:00:00', '2026-02-24T00:00:00');
END
GO
IF NOT EXISTS (SELECT 1 FROM [dbo].[recomendacoes] WHERE id = 8)
BEGIN
    INSERT INTO [dbo].[recomendacoes] (id, cliente_id, produto_id, motivo, score, aceita, gerada_em, created_at, updated_at)
    VALUES (8, 7, 7, 'MixRegional', 0.8787, 1, '2026-02-20T00:00:00', '2026-01-29T00:00:00', '2026-02-24T00:00:00');
END
GO
IF NOT EXISTS (SELECT 1 FROM [dbo].[recomendacoes] WHERE id = 9)
BEGIN
    INSERT INTO [dbo].[recomendacoes] (id, cliente_id, produto_id, motivo, score, aceita, gerada_em, created_at, updated_at)
    VALUES (9, 8, 4, 'Historico', 0.7053, 0, '2026-02-12T00:00:00', '2026-01-10T00:00:00', '2026-02-24T00:00:00');
END
GO
IF NOT EXISTS (SELECT 1 FROM [dbo].[recomendacoes] WHERE id = 10)
BEGIN
    INSERT INTO [dbo].[recomendacoes] (id, cliente_id, produto_id, motivo, score, aceita, gerada_em, created_at, updated_at)
    VALUES (10, 8, 12, 'MixRegional', 0.4557, 0, '2026-01-14T00:00:00', '2026-02-21T00:00:00', '2026-02-24T00:00:00');
END
GO
IF NOT EXISTS (SELECT 1 FROM [dbo].[recomendacoes] WHERE id = 11)
BEGIN
    INSERT INTO [dbo].[recomendacoes] (id, cliente_id, produto_id, motivo, score, aceita, gerada_em, created_at, updated_at)
    VALUES (11, 9, 10, 'Historico', 0.4181, 0, '2026-01-23T00:00:00', '2026-01-16T00:00:00', '2026-02-24T00:00:00');
END
GO
IF NOT EXISTS (SELECT 1 FROM [dbo].[recomendacoes] WHERE id = 12)
BEGIN
    INSERT INTO [dbo].[recomendacoes] (id, cliente_id, produto_id, motivo, score, aceita, gerada_em, created_at, updated_at)
    VALUES (12, 10, 13, 'Historico', 0.9431, 1, '2026-01-15T00:00:00', '2026-01-06T00:00:00', '2026-02-24T00:00:00');
END
GO
IF NOT EXISTS (SELECT 1 FROM [dbo].[recomendacoes] WHERE id = 13)
BEGIN
    INSERT INTO [dbo].[recomendacoes] (id, cliente_id, produto_id, motivo, score, aceita, gerada_em, created_at, updated_at)
    VALUES (13, 11, 8, 'Sazonalidade', 0.4142, 0, '2026-01-21T00:00:00', '2026-01-08T00:00:00', '2026-02-24T00:00:00');
END
GO
IF NOT EXISTS (SELECT 1 FROM [dbo].[recomendacoes] WHERE id = 14)
BEGIN
    INSERT INTO [dbo].[recomendacoes] (id, cliente_id, produto_id, motivo, score, aceita, gerada_em, created_at, updated_at)
    VALUES (14, 11, 4, 'MixRegional', 0.8516, 0, '2026-02-06T00:00:00', '2026-01-25T00:00:00', '2026-02-24T00:00:00');
END
GO
IF NOT EXISTS (SELECT 1 FROM [dbo].[recomendacoes] WHERE id = 15)
BEGIN
    INSERT INTO [dbo].[recomendacoes] (id, cliente_id, produto_id, motivo, score, aceita, gerada_em, created_at, updated_at)
    VALUES (15, 12, 22, 'MixRegional', 0.5835, 0, '2026-02-28T00:00:00', '2026-01-05T00:00:00', '2026-02-24T00:00:00');
END
GO
IF NOT EXISTS (SELECT 1 FROM [dbo].[recomendacoes] WHERE id = 16)
BEGIN
    INSERT INTO [dbo].[recomendacoes] (id, cliente_id, produto_id, motivo, score, aceita, gerada_em, created_at, updated_at)
    VALUES (16, 13, 16, 'Sazonalidade', 0.4165, 0, '2026-01-06T00:00:00', '2026-01-30T00:00:00', '2026-02-24T00:00:00');
END
GO
IF NOT EXISTS (SELECT 1 FROM [dbo].[recomendacoes] WHERE id = 17)
BEGIN
    INSERT INTO [dbo].[recomendacoes] (id, cliente_id, produto_id, motivo, score, aceita, gerada_em, created_at, updated_at)
    VALUES (17, 14, 5, 'MixRegional', 0.6244, 0, '2026-01-18T00:00:00', '2026-02-11T00:00:00', '2026-02-24T00:00:00');
END
GO
IF NOT EXISTS (SELECT 1 FROM [dbo].[recomendacoes] WHERE id = 18)
BEGIN
    INSERT INTO [dbo].[recomendacoes] (id, cliente_id, produto_id, motivo, score, aceita, gerada_em, created_at, updated_at)
    VALUES (18, 14, 20, 'MixRegional', 0.8592, 0, '2026-01-30T00:00:00', '2026-02-01T00:00:00', '2026-02-24T00:00:00');
END
GO
IF NOT EXISTS (SELECT 1 FROM [dbo].[recomendacoes] WHERE id = 19)
BEGIN
    INSERT INTO [dbo].[recomendacoes] (id, cliente_id, produto_id, motivo, score, aceita, gerada_em, created_at, updated_at)
    VALUES (19, 15, 19, 'Historico', 0.5191, 0, '2026-02-23T00:00:00', '2026-02-11T00:00:00', '2026-02-24T00:00:00');
END
GO
IF NOT EXISTS (SELECT 1 FROM [dbo].[recomendacoes] WHERE id = 20)
BEGIN
    INSERT INTO [dbo].[recomendacoes] (id, cliente_id, produto_id, motivo, score, aceita, gerada_em, created_at, updated_at)
    VALUES (20, 15, 15, 'Sazonalidade', 0.5036, 0, '2026-01-17T00:00:00', '2026-02-04T00:00:00', '2026-02-24T00:00:00');
END
GO
IF NOT EXISTS (SELECT 1 FROM [dbo].[recomendacoes] WHERE id = 21)
BEGIN
    INSERT INTO [dbo].[recomendacoes] (id, cliente_id, produto_id, motivo, score, aceita, gerada_em, created_at, updated_at)
    VALUES (21, 16, 1, 'Sazonalidade', 0.6614, 1, '2026-02-15T00:00:00', '2026-02-06T00:00:00', '2026-02-24T00:00:00');
END
GO
IF NOT EXISTS (SELECT 1 FROM [dbo].[recomendacoes] WHERE id = 22)
BEGIN
    INSERT INTO [dbo].[recomendacoes] (id, cliente_id, produto_id, motivo, score, aceita, gerada_em, created_at, updated_at)
    VALUES (22, 17, 11, 'MixRegional', 0.5262, 0, '2026-02-11T00:00:00', '2026-01-24T00:00:00', '2026-02-24T00:00:00');
END
GO
IF NOT EXISTS (SELECT 1 FROM [dbo].[recomendacoes] WHERE id = 23)
BEGIN
    INSERT INTO [dbo].[recomendacoes] (id, cliente_id, produto_id, motivo, score, aceita, gerada_em, created_at, updated_at)
    VALUES (23, 18, 17, 'Historico', 0.9473, 1, '2026-02-02T00:00:00', '2026-01-28T00:00:00', '2026-02-24T00:00:00');
END
GO
IF NOT EXISTS (SELECT 1 FROM [dbo].[recomendacoes] WHERE id = 24)
BEGIN
    INSERT INTO [dbo].[recomendacoes] (id, cliente_id, produto_id, motivo, score, aceita, gerada_em, created_at, updated_at)
    VALUES (24, 19, 25, 'Sazonalidade', 0.5014, 0, '2026-01-28T00:00:00', '2026-01-31T00:00:00', '2026-02-24T00:00:00');
END
GO
IF NOT EXISTS (SELECT 1 FROM [dbo].[recomendacoes] WHERE id = 25)
BEGIN
    INSERT INTO [dbo].[recomendacoes] (id, cliente_id, produto_id, motivo, score, aceita, gerada_em, created_at, updated_at)
    VALUES (25, 19, 1, 'Historico', 0.4086, 0, '2026-02-13T00:00:00', '2026-02-09T00:00:00', '2026-02-24T00:00:00');
END
GO
IF NOT EXISTS (SELECT 1 FROM [dbo].[recomendacoes] WHERE id = 26)
BEGIN
    INSERT INTO [dbo].[recomendacoes] (id, cliente_id, produto_id, motivo, score, aceita, gerada_em, created_at, updated_at)
    VALUES (26, 20, 19, 'MixRegional', 0.5825, 0, '2026-02-01T00:00:00', '2026-01-12T00:00:00', '2026-02-24T00:00:00');
END
GO
IF NOT EXISTS (SELECT 1 FROM [dbo].[recomendacoes] WHERE id = 27)
BEGIN
    INSERT INTO [dbo].[recomendacoes] (id, cliente_id, produto_id, motivo, score, aceita, gerada_em, created_at, updated_at)
    VALUES (27, 20, 18, 'MixRegional', 0.5584, 0, '2026-02-09T00:00:00', '2026-02-12T00:00:00', '2026-02-24T00:00:00');
END
GO

SET IDENTITY_INSERT [dbo].[recomendacoes] OFF;
GO
