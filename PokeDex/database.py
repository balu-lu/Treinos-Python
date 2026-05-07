from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.orm import sessionmaker, declarative_base

SQLALCHEMY_DATABASE_URL = "sqlite:///./pokedex.db"

engine = create_engine(
    SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}
)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

# Modelo da tabela de users


class UsuarioDB(Base):
    __tablename__ = "usuarios"
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True, nullable=False)
    password = Column(String, nullable=False)


# Modelo da tabela de pokemons
class PokemonDB(Base):
    __tablename__ = "pokemons"
    id = Column(Integer, primary_key=True, index=True)
    nome = Column(String, unique=True, index=True, nullable=False)
    tipo = Column(String, nullable=False)
    nivel = Column(Integer, nullable=False)
    capturas = Column(Integer, default=0)


# Cria o arquivo SQLite e as tabelas
Base.metadata.create_all(bind=engine)

# Injeção de dependência para pegar a sessão do banco


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


# ajuda a entender no terminal se o arquivo já foi rodado
if __name__ == "__main__":
    print("Criando tabelas no banco de dados...")
    Base.metadata.create_all(bind=engine)
    print("Banco de dados criado com sucesso!")
