from fastapi import FastAPI, HTTPException, Depends, status, Query
from fastapi.security import HTTPBasic, HTTPBasicCredentials
from pydantic import BaseModel
import secrets

# importando do banco de dados
from sqlalchemy import create_engine, Column, Integer, String, Boolean
from sqlalchemy.orm import sessionmaker, Session, declarative_base

app = FastAPI()
security = HTTPBasic()

# configurando o banco de dados (sqlite)
SQLALCHEMY_DATABASE_URL = "sqlite:///./tarefas.db"

engine = create_engine(
    SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}
)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

# criar e fechar o banco


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# MODELO / substituição disso: tarefas: list[Tarefa] = []


class TarefaDB(Base):
    __tablename__ = "tarefas"

    id = Column(Integer, primary_key=True, index=True)
    nome = Column(String, unique=True, index=True)
    descricao = Column(String)
    concluida = Column(Boolean, default=False)


# criar o arquivo e as tabelas
Base.metadata.create_all(bind=engine)

# validação


class TarefaSchema(BaseModel):
    nome: str
    descricao: str
    concluida: bool = False

    class Config:
        from_attributes = True

# PARTE DE SEGURANÇA


def verificar_auth(credentials: HTTPBasicCredentials = Depends(security)):
    is_user_ok = secrets.compare_digest(credentials.username, "daniel.hrl")
    is_pass_ok = secrets.compare_digest(credentials.password, "api123")

    if not (is_user_ok and is_pass_ok):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Usuário ou senha incorretos",
            headers={"WWW-Authenticate": "Basic"},
        )
    return credentials.username


# PARTE DE ROTAS
@app.post("/tarefas", dependencies=[Depends(verificar_auth)])
def adicionar_tarefa(tarefa: TarefaSchema, db: Session = Depends(get_db)):
    # adicionando verificação de duplicatas
    tarefa_existente = db.query(TarefaDB).filter(
        TarefaDB.nome == tarefa.nome).first()
    if tarefa_existente:
        raise HTTPException(
            status_code=400, detail="Uma tarefa com esse nome já existe.")

    # Convertendo o pydantic para o sqlalchemy
    nova_tarefa = TarefaDB(
        nome=tarefa.nome, descricao=tarefa.descricao, concluida=tarefa.concluida)
    db.add(nova_tarefa)
    db.commit()
    db.refresh(nova_tarefa)

    return {"mensagem": "Tarefa adicionada com sucesso!", "tarefa": nova_tarefa}


@app.get("/tarefas")
def listar_tarefas(
    user: str = Depends(verificar_auth),
    page: int = Query(1, ge=1, description="Número da página"),
    size: int = Query(5, ge=1, le=100, description="Itens por página"),
    sort_by: str = Query("nome", pattern="^(nome|descricao)$"),
    # injetando o banco
    db: Session = Depends(get_db)
):
    # PAGINAÇÃO (banco de dados faz a matematica do offset
    offset = (page - 1) * size

    # ORDENAÇÃO delegando para o SQL
    if sort_by == "nome":
        query = db.query(TarefaDB).order_by(TarefaDB.nome)
    else:
        query = db.query(TarefaDB).order_by(TarefaDB.descricao)

    # busca apenas os itens da pagina e conta o total do banco
    tarefas_paginadas = query.offset(offset).limit(size).all()
    total_tarefas = db.query(TarefaDB).count()

    return {
        "usuário": user,
        "total": total_tarefas,
        "página": page,
        "resultado": tarefas_paginadas
    }


@app.put("/tarefas/{nome}", dependencies=[Depends(verificar_auth)])
def concluir_tarefa(nome: str, db: Session = Depends(get_db)):
    # busca a tarefa pelo nome
    tarefa = db.query(TarefaDB).filter(TarefaDB.nome == nome).first()

    if not tarefa:
        raise HTTPException(status_code=404, detail="Tarefa não encontrada.")

    # Atualiza status
    tarefa.concluida = True
    db.commit()

    return {"mensagem": "Tarefa marcada como concluída!", "tarefa": tarefa}


@app.delete("/tarefas/{nome}", dependencies=[Depends(verificar_auth)])
def remover_tarefa(nome: str, db: Session = Depends(get_db)):
    tarefa = db.query(TarefaDB).filter(TarefaDB.nome == nome).first()

    if not tarefa:
        raise HTTPException(status_code=404, detail="Tarefa não encontrada.")

    db.delete(tarefa)
    db.commit()

    return {"mensagem": f"Tarefa '{nome}' removida com sucesso!"}
