from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker, DeclarativeBase
from backend.config import settings


class Base(DeclarativeBase):
    pass


def _get_engine():
    if settings.use_sqlite and not settings.database_url:
        return create_engine(
            settings.sqlite_url,
            connect_args={"check_same_thread": False},
            echo=settings.app_debug,
        )
    return create_engine(
        settings.sqlserver_url,
        pool_size=10,
        max_overflow=20,
        pool_pre_ping=True,
        echo=settings.app_debug,
    )


engine = _get_engine()

SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine,
)


def get_db():
    """Dependency do FastAPI — injeta sessão de banco de dados."""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def create_tables() -> None:
    """Cria todas as tabelas definidas nos models SQLAlchemy."""
    Base.metadata.create_all(bind=engine)


def health_check() -> bool:
    """Verifica conexão com o banco de dados."""
    try:
        with engine.connect() as conn:
            conn.execute(text("SELECT 1"))
        return True
    except Exception:
        return False
