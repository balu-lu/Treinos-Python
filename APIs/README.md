# API de Livros com FastAPI e Redis

API REST assíncrona para gerenciamento de livros com FastAPI e cache em Redis.
Os dados principais ficam em memória e o endpoint `GET /livros` usa Redis como cache para acelerar chamadas repetidas.

## Arquivo principal

- `APIs/app.py`

## Requisitos

- Python 3.10 ou superior
- Redis
- Docker e Docker Compose ou Docker Desktop (opcional, para subir o Redis em contêiner)

## Dependências Python

Se quiser instalar manualmente:

```powershell
pip install fastapi uvicorn redis
```

Se estiver usando Poetry:

```powershell
poetry install
```

## Como executar

### 1. Ative um ambiente virtual (opcional)

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
```

### 2. Inicie o Redis

#### Opção A: Redis local

Se você já tiver Redis instalado localmente, basta iniciar o serviço da forma usual no seu sistema.

#### Opção B: Redis com Docker

No diretório do projeto:

```powershell
docker-compose up -d redis
```

Isso iniciará um contêiner Redis com a porta `6379` exposta.

#### Opção C: API e Redis com Docker Compose

Se quiser subir tudo com Docker:

```powershell
docker-compose up -d --build
```

Nesse caso:

- a API sobe no serviço `api_livros`
- o Redis sobe no serviço `redis`
- a API continuará disponível em `http://127.0.0.1:8000`

### 3. Inicie a API

```powershell
uvicorn APIs.app:app --reload
```

A aplicação ficará disponível em:

- `http://127.0.0.1:8000`
- `http://127.0.0.1:8000/docs`

## Configuração do Redis

A aplicação lê estas variáveis de ambiente:

- `REDIS_HOST` com padrão `localhost`
- `REDIS_PORT` com padrão `6379`
- `REDIS_DB` com padrão `0`

O TTL do cache está definido no código pela constante `CACHE_TTL = 300`, ou seja, 5 minutos.

## Comportamento do cache

- `GET /livros` tenta ler primeiro a chave `livros` no Redis
- se não encontrar cache, usa a lista em memória e salva o resultado no Redis
- `POST /livros`, `PUT /livros/{id}` e `DELETE /livros/{id}` invalidam a chave `livros`

Se o Redis não estiver disponível, a API continua funcionando com a lista em memória.

## Endpoints

- `GET /livros` lista todos os livros
- `POST /livros` cria um novo livro
- `PUT /livros/{livro_id}` atualiza um livro existente
- `DELETE /livros/{livro_id}` remove um livro

## Modelo de dados

### Entrada para criação e atualização

```json
{
  "titulo": "O Hobbit",
  "autor": "J.R.R. Tolkien",
  "ano": 1937,
  "disponivel": true
}
```

### Resposta da API

```json
{
  "id": 3,
  "titulo": "O Hobbit",
  "autor": "J.R.R. Tolkien",
  "ano": 1937,
  "disponivel": true
}
```

## Exemplos de teste

### Listar livros

```powershell
$response = Invoke-WebRequest -Uri "http://localhost:8000/livros" -Method GET
$response.Content
```

Na primeira chamada, a API busca da lista em memória e salva no Redis.
Nas chamadas seguintes, a resposta pode vir do cache enquanto a chave ainda existir.

### Criar um livro

```powershell
$body = @{
    titulo = "O Hobbit"
    autor = "J.R.R. Tolkien"
    ano = 1937
    disponivel = $true
} | ConvertTo-Json

Invoke-WebRequest -Uri "http://localhost:8000/livros" `
  -Method POST `
  -ContentType "application/json" `
  -Body $body
```

### Atualizar um livro

```powershell
$body = @{
    titulo = "O Hobbit - Edição Revisada"
    autor = "J.R.R. Tolkien"
    ano = 1937
    disponivel = $true
} | ConvertTo-Json

Invoke-WebRequest -Uri "http://localhost:8000/livros/3" `
  -Method PUT `
  -ContentType "application/json" `
  -Body $body
```

### Deletar um livro

```powershell
Invoke-WebRequest -Uri "http://localhost:8000/livros/3" -Method DELETE
```

## Como verificar o conteúdo do Redis

### Com `redis-cli` local

```powershell
redis-cli
```

Depois, no prompt do Redis:

```text
GET livros
TTL livros
```

### Com Redis em Docker

```powershell
docker exec -it redis_cache redis-cli
```

Depois, no prompt do Redis:

```text
GET livros
TTL livros
```

## Como parar o Redis

Se você iniciou apenas o serviço Redis com Docker:

```powershell
docker-compose stop redis
```

Se quiser remover os contêineres definidos no `docker-compose.yml`:

```powershell
docker-compose down
```

## Estrutura da implementação

O arquivo `APIs/app.py` contém:

- modelos Pydantic para validação dos livros
- função de conexão com Redis
- função `salvar_livros_redis`
- função `deletar_livros_redis`
- endpoints assíncronos para listar, criar, atualizar e remover livros

## Observações

- o cache usa a chave `livros`
- o cache é invalidado após operações de escrita
- a persistência principal desta atividade é uma lista em memória, não um banco de dados real
