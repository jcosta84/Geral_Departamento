from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
from urllib.parse import quote_plus

# Configurações do MySQL
server = "localhost"      # IP ou localhost
database = "SistemaGestao"    # Nome do banco
user = "jpaulo"               # Usuário
password = "loucoste9850053" # Senha

# URL de conexão com MySQL usando PyMySQL
DATABASE_URL = f"mysql+pymysql://{user}:{password}@{server}/{database}"

# Criação do engine
engine = create_engine(DATABASE_URL, echo=True)  # echo=True para debug

# Criação da sessão
SessionLocal = sessionmaker(bind=engine)

# Base declarativa
Base = declarative_base()

