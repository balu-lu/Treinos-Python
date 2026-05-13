from __future__ import annotations

import asyncio
import json
import logging
import os
from typing import List

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import redis.asyncio as redis

# Configuração de logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI(title="API de Livros Assíncrona com Redis", version="2.0")

# Configurações do Redis
REDIS_HOST = os.getenv("REDIS_HOST", "localhost")
REDIS_PORT = int(os.getenv("REDIS_PORT", "6379"))
REDIS_DB = int(os.getenv("REDIS_DB", "0"))
CACHE_TTL = 300  # Time To Live do cache em segundos (5 minutos)

# Modelo de dados usado para criar e atualizar livros.


class LivroInput(BaseModel):
    titulo: str
    autor: str
    ano: int
    disponivel: bool = True

# Modelo de dados retornado pela API, incluindo o ID.


class Livro(LivroInput):
    id: int


# Lista em memória que simula um banco de dados de livros.
livros: List[Livro] = [
    Livro(id=1, titulo="O Senhor dos Anéis",
          autor="J. R. R. Tolkien", ano=1954),
    Livro(id=2, titulo="1984", autor="George Orwell", ano=1949),
]


# FUNÇÕES DE CONEXÃO E GERENCIAMENTO DO REDIS

async def obter_conexao_redis() -> redis.Redis:

    # Obtém uma conexão com o Redis.
    # Utiliza redis.asyncio para operações assíncronas.
    try:
        r = redis.Redis(
            host=REDIS_HOST,
            port=REDIS_PORT,
            db=REDIS_DB,
            decode_responses=True,
            socket_connect_timeout=5
        )
        # Testa a conexão
        await r.ping()
        return r
    except ConnectionError as e:
        logger.warning("Falha ao conectar ao Redis: %s", e)
        return None


async def salvar_livros_redis(redis_conn: redis.Redis, livros_lista: List[Livro]) -> bool:

    # Salva a lista de livros no Redis com uma chave 'livros'.
    # Serializa os livros em JSON e define um TTL (Time To Live) para o cache.

    # Args:
    #     redis_conn: Conexão com o Redis.
    #     livros_lista: Lista de objetos Livro a ser armazenada.

    # Returns:
    #     True se salvo com sucesso, False caso contrário.
    try:
        if redis_conn is None:
            logger.warning(
                "Conexão com Redis indisponível, cache não foi salvo")
            return False

        # Serializa a lista de livros para JSON
        livros_json = json.dumps(
            [livro.dict() for livro in livros_lista],
            ensure_ascii=False
        )

        # Salva no Redis com TTL de CACHE_TTL segundos
        await redis_conn.setex("livros", CACHE_TTL, livros_json)
        logger.info("Lista de livros salva no Redis com TTL de %ds", CACHE_TTL)
        return True
    except redis.RedisError as e:
        logger.error("Erro ao salvar livros no Redis: %s", e)
        return False


async def deletar_livros_redis(redis_conn: redis.Redis) -> bool:

    # Deleta a chave de livros do Redis.
    # Utilizada para invalidar o cache quando os dados são modificados.

    # Args:
    #     redis_conn: Conexão com o Redis.

    # Returns:
    #     True se deletado com sucesso, False caso contrário.
    try:
        if redis_conn is None:
            logger.warning(
                "Conexão com Redis indisponível, cache não foi deletado")
            return False

        resultado = await redis_conn.delete("livros")
        logger.info(
            "Cache de livros deletado do Redis (chaves removidas: %d)", resultado)
        return True
    except redis.RedisError as e:
        logger.error("Erro ao deletar livros do Redis: %s", e)
        return False


async def simular_io() -> None:
    # Simula uma operação de I/O assíncrona para demonstrar async/await.
    await asyncio.sleep(0)


@app.get("/livros", response_model=List[Livro])
async def listar_livros() -> List[Livro]:

    # Lista todos os livros cadastrados.

    # Estratégia de cache:
    # 1. Primeiro, tenta obter os dados do Redis (cache).
    # 2. Se não estiver no cache, busca da lista em memória.
    # 3. Salva a lista em memória no Redis para futuras requisições.
    # 4. Se Redis falhar, retorna os dados da lista em memória normalmente.
    await simular_io()

    # Tenta obter conexão com Redis
    redis_conn = await obter_conexao_redis()

    if redis_conn:
        try:
            # Tenta obter dados do cache
            livros_cache = await redis_conn.get("livros")

            if livros_cache:
                logger.info("Dados obtidos do cache Redis")
                livros_do_cache = [
                    Livro(**livro_dict)
                    for livro_dict in json.loads(livros_cache)
                ]
                return livros_do_cache
            else:
                logger.info(
                    "Dados não encontrados no cache, buscando da lista em memória")
        except redis.RedisError as e:
            logger.warning("Erro ao consultar Redis: %s", e)

    # Se Redis não estiver disponível ou dados não estão em cache,
    # busca da lista em memória e tenta salvar no Redis
    if redis_conn:
        await salvar_livros_redis(redis_conn, livros)

    return livros


@app.post("/livros", response_model=Livro, status_code=201)
async def criar_livro(novo_livro: LivroInput) -> Livro:

    # Cria um novo livro e adiciona à lista em memória.
    # Após a criação, invalida o cache do Redis.
    await simular_io()
    novo_id = max((livro.id for livro in livros), default=0) + 1
    livro_criado = Livro(id=novo_id, **novo_livro.dict())
    livros.append(livro_criado)

    # Invalida o cache do Redis
    redis_conn = await obter_conexao_redis()
    if redis_conn:
        await deletar_livros_redis(redis_conn)

    logger.info("Livro criado com ID %d, cache invalidado", novo_id)
    return livro_criado


@app.put("/livros/{livro_id}", response_model=Livro)
async def atualizar_livro(livro_id: int, dados: LivroInput) -> Livro:

    # Atualiza os dados de um livro existente.
    # Após a atualização, invalida o cache do Redis.
    await simular_io()
    for indice, livro in enumerate(livros):
        if livro.id == livro_id:
            livro_atualizado = Livro(id=livro_id, **dados.dict())
            livros[indice] = livro_atualizado

            # Invalida o cache do Redis
            redis_conn = await obter_conexao_redis()
            if redis_conn:
                await deletar_livros_redis(redis_conn)

            logger.info(
                "Livro com ID %d atualizado, cache invalidado", livro_id)
            return livro_atualizado

    raise HTTPException(status_code=404, detail="Livro não encontrado")


@app.delete("/livros/{livro_id}", status_code=204)
async def deletar_livro(livro_id: int) -> None:

    # Remove um livro da lista pelo seu ID.
    # Após a exclusão, invalida o cache do Redis.
    await simular_io()
    for indice, livro in enumerate(livros):
        if livro.id == livro_id:
            livros.pop(indice)

            # Invalida o cache do Redis
            redis_conn = await obter_conexao_redis()
            if redis_conn:
                await deletar_livros_redis(redis_conn)

            logger.info("Livro com ID %d deletado, cache invalidado", livro_id)
            return

    raise HTTPException(status_code=404, detail="Livro não encontrado")
