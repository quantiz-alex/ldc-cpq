from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from backend.api.routes import (
    alertas_consistencia,
    auth,
    clientes,
    pedido_itens,
    pedidos,
    precos_por_janela,
    produtos,
    recomendacoes,
    usuarios,
)
from backend.config import settings
from backend.database import create_tables, health_check

app = FastAPI(
    title="LDC Insumos — Plataforma Comercial (CPQ Inteligente) API",
    version="1.0.0",
    docs_url="/docs" if not settings.is_production else None,
    redoc_url="/redoc" if not settings.is_production else None,
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origins,
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "DELETE", "OPTIONS"],
    allow_headers=["*"],
)

app.include_router(auth.router, prefix="/api/v1")
app.include_router(usuarios.router, prefix="/api/v1")
app.include_router(produtos.router, prefix="/api/v1")
app.include_router(clientes.router, prefix="/api/v1")
app.include_router(precos_por_janela.router, prefix="/api/v1")
app.include_router(pedidos.router, prefix="/api/v1")
app.include_router(pedido_itens.router, prefix="/api/v1")
app.include_router(alertas_consistencia.router, prefix="/api/v1")
app.include_router(recomendacoes.router, prefix="/api/v1")


@app.on_event("startup")
async def startup() -> None:
    create_tables()


@app.get("/health")
def health() -> dict:
    return {"status": "ok", "db": health_check()}
