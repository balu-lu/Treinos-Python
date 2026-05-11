from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import Dict, List, Tuple

app = FastAPI(title="Pokédex")

# In-memory storage
pokedex: Dict[str, Dict] = {}
historico_capturas: List[Tuple[str, int]] = []

# Pydantic models


class PokemonCreate(BaseModel):
    nome: str
    tipo: str
    nivel: int


class Captura(BaseModel):
    quantidade: int

# Helper functions (adapted from original)


def validar_pokemon_existe(nome: str) -> bool:
    return nome in pokedex


def adicionar_pokemon_api(nome: str, tipo: str, nivel: int):
    if validar_pokemon_existe(nome):
        raise HTTPException(
            status_code=400, detail="Pokémon já cadastrado na Pokédex.")
    pokedex[nome] = {'tipo': tipo, 'nivel': nivel, 'capturado': 0}
    return {"message": f"Pokémon {nome} adicionado com sucesso!"}


def listar_pokemon_api():
    if not pokedex:
        return {"pokemons": []}
    pokemons = [{"nome": nome, **dados}
                for nome, dados in sorted(pokedex.items())]
    return {"pokemons": pokemons}


def remover_pokemon_api(nome: str):
    if not validar_pokemon_existe(nome):
        raise HTTPException(status_code=404, detail="Pokémon não encontrado.")
    del pokedex[nome]
    return {"message": f"Pokémon {nome} removido com sucesso."}


def atualizar_nivel_pokemon_api(nome: str, novo_nivel: int):
    if not validar_pokemon_existe(nome):
        raise HTTPException(status_code=404, detail="Pokémon não encontrado.")
    pokedex[nome]['nivel'] = novo_nivel
    return {"message": f"Nível do Pokémon {nome} atualizado para {novo_nivel}."}


def registrar_captura_api(nome: str, quantidade: int):
    if not validar_pokemon_existe(nome):
        raise HTTPException(status_code=404, detail="Pokémon não encontrado.")
    if quantidade <= 0:
        raise HTTPException(
            status_code=400, detail="A quantidade de capturas deve ser maior que zero.")
    pokedex[nome]['capturado'] += quantidade
    historico_capturas.append((nome, quantidade))
    return {"message": f"Captura de {quantidade} {nome}(s) registrada com sucesso!"}


def exibir_historico_capturas_api():
    return {"historico": [{"nome": nome, "quantidade": qtd} for nome, qtd in historico_capturas]}

# API Routes


@app.post("/pokemon/")
def adicionar_pokemon(pokemon: PokemonCreate):
    return adicionar_pokemon_api(pokemon.nome, pokemon.tipo, pokemon.nivel)


@app.get("/pokemon/")
def listar_pokemon():
    return listar_pokemon_api()


@app.delete("/pokemon/{nome}")
def remover_pokemon(nome: str):
    return remover_pokemon_api(nome)


@app.put("/pokemon/{nome}/nivel")
def atualizar_nivel(nome: str, nivel: int):
    return atualizar_nivel_pokemon_api(nome, nivel)


@app.post("/pokemon/{nome}/captura")
def registrar_captura(nome: str, captura: Captura):
    return registrar_captura_api(nome, captura.quantidade)


@app.get("/historico/")
def exibir_historico():
    return exibir_historico_capturas_api()
