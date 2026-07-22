import os
from configparser import ConfigParser
from urllib.parse import quote_plus

from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker


# Pasta principal do projeto:
# PROGRAMA_GERAL/
BASE_DIR = os.path.dirname(
    os.path.dirname(os.path.abspath(__file__))
)

CONFIG_PATH = os.path.join(BASE_DIR, "config.ini")

config = ConfigParser()

if not os.path.exists(CONFIG_PATH):
    raise FileNotFoundError(
        f"Ficheiro de configuração não encontrado: {CONFIG_PATH}"
    )

config.read(CONFIG_PATH, encoding="utf-8")

if "DATABASE" not in config:
    raise KeyError(
        "A secção [DATABASE] não foi encontrada no config.ini"
    )

HOST = config.get("DATABASE", "HOST")
PORT = config.get("DATABASE", "PORT", fallback="3306")
DATABASE = config.get("DATABASE", "DATABASE")
USER = config.get("DATABASE", "USER")
PASSWORD = quote_plus(config.get("DATABASE", "PASSWORD"))

DATABASE_URL = (
    f"mysql+pymysql://{USER}:{PASSWORD}"
    f"@{HOST}:{PORT}/{DATABASE}"
)

engine = create_engine(
    DATABASE_URL,
    echo=False,
    pool_pre_ping=True,
    pool_recycle=3600
)

SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine
)

Base = declarative_base()


def get_db():
    """
    Cria uma sessão e garante o seu encerramento.
    """
    session = SessionLocal()

    try:
        yield session
    finally:
        session.close()