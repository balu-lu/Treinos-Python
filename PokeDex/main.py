from fastapi import FastAPI, HTTPException, Depends, Query
from pydantic import BaseModel, Field
from sqlalchemy.orm import Session

from database import SessionLocal, get_db, PokemonDB, UsuarioDB
from auth import verificar_auth

app = FastAPI(title="Pokédex")

# Cria um usuário padrão ao iniciar o app


def criar_usuario_padrao():
    db = SessionLocal()
    if not db.query(UsuarioDB).filter(UsuarioDB.username == "treinador").first():
        admin = UsuarioDB(username="treinador", password="123")
        db.add(admin)
        db.commit()
    db.close()


criar_usuario_padrao()


# validação de tipos
class PokemonCreate(BaseModel):
    nome: str
    tipo: str
    nivel: int = Field(ge=1, le=100)

    class Config:
        from_attributes = True


class PokemonLevelUpdate(BaseModel):
    nivel: int = Field(ge=1, le=100)


class PokemonCatch(BaseModel):
    quantidade: int = Field(gt=0)


# rotas da api
@app.post("/pokemon/", dependencies=[Depends(verificar_auth)])
def adicionar_pokemon(pokemon: PokemonCreate, db: Session = Depends(get_db)):
    pokemon_existente = db.query(PokemonDB).filter(
        PokemonDB.nome == pokemon.nome).first()
    if pokemon_existente:
        raise HTTPException(
            status_code=400, detail="Pokémon já cadastrado na Pokédex.")

    novo_pokemon = PokemonDB(
        nome=pokemon.nome, tipo=pokemon.tipo, nivel=pokemon.nivel)
    db.add(novo_pokemon)
    db.commit()
    db.refresh(novo_pokemon)

    return {"mensagem": "Pokémon adicionado com sucesso!", "pokemon": novo_pokemon}


@app.get("/pokemon/")
def listar_pokemon(
    user: str = Depends(verificar_auth),
    page: int = Query(1, ge=1, description="Número da página"),
    size: int = Query(5, ge=1, le=100, description="Itens por página"),
    db: Session = Depends(get_db)
):
    """Lista os Pokémon em ordem alfabética com paginação"""
    offset = (page - 1) * size

    # ordem alfabetica
    pokemons_db = db.query(PokemonDB).order_by(
        PokemonDB.nome.asc()).offset(offset).limit(size).all()
    total_pokemons = db.query(PokemonDB).count()

    # formatação da listagem
    lista_formatada = [f"{p.nome} - {p.tipo} - {p.nivel}" for p in pokemons_db]

    return {
        "treinador_logado": user,
        "total_cadastrados": total_pokemons,
        "página": page,
        "pokemons": lista_formatada
    }


@app.delete("/pokemon/{nome}", dependencies=[Depends(verificar_auth)])
def remover_pokemon(nome: str, db: Session = Depends(get_db)):
    db_pokemon = db.query(PokemonDB).filter(PokemonDB.nome == nome).first()
    if not db_pokemon:
        raise HTTPException(status_code=404, detail="Pokémon não encontrado.")

    db.delete(db_pokemon)
    db.commit()
    return {"mensagem": f"Pokémon '{nome}' removido com sucesso."}


@app.put("/pokemon/{nome}/nivel", dependencies=[Depends(verificar_auth)])
def atualizar_nivel(nome: str, update_data: PokemonLevelUpdate, db: Session = Depends(get_db)):
    db_pokemon = db.query(PokemonDB).filter(PokemonDB.nome == nome).first()
    if not db_pokemon:
        raise HTTPException(status_code=404, detail="Pokémon não encontrado.")

    db_pokemon.nivel = update_data.nivel
    db.commit()
    return {"mensagem": f"Nível de '{nome}' atualizado para {update_data.nivel}."}


@app.post("/pokemon/{nome}/captura", dependencies=[Depends(verificar_auth)])
def registrar_captura(nome: str, captura_data: PokemonCatch, db: Session = Depends(get_db)):
    db_pokemon = db.query(PokemonDB).filter(PokemonDB.nome == nome).first()
    if not db_pokemon:
        raise HTTPException(status_code=404, detail="Pokémon não encontrado.")

    db_pokemon.capturas += captura_data.quantidade
    db.commit()
    return {"mensagem": f"Captura! '{nome}' foi capturado {db_pokemon.capturas} vez(es) ao todo."}


@app.get("/historico/", dependencies=[Depends(verificar_auth)])
def exibir_historico(db: Session = Depends(get_db)):
    pokemons_capturados = db.query(PokemonDB).filter(
        PokemonDB.capturas > 0).all()

    historico = [
        {"nome": p.nome, "quantidade_capturas": p.capturas}
        for p in pokemons_capturados
    ]
    return {"historico_de_capturas": historico}
