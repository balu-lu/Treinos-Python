# Treinos-Python
Treinos de alguns projetos

# Em alguns dispositivos vai ser necessário após instalar o pip
pip install poetry-plugin-shell
py -m poetry shell

## PokeDex - FastAPI Application

Este repositório contém uma aplicação FastAPI para gerenciar uma Pokédex, baseada no script app.py.

### Pré-requisitos
- Docker
- Docker Compose

### Como executar
1. Clone o repositório:
   ```
   git clone <url-do-repositorio>
   cd <nome-do-repositorio>
   ```

2. Construa e execute os contêineres:
   ```
   docker-compose up --build -d
   ```

3. Acesse a aplicação em http://localhost:8000

4. Para parar os contêineres:
   ```
   docker-compose down
   ```

### Estrutura do Projeto
- `PokeDex/app.py`: Código-fonte da aplicação FastAPI
- `pyproject.toml`: Configuração do Poetry
- `poetry.lock`: Lock file das dependências
- `Dockerfile`: Configuração da imagem Docker
- `docker-compose.yml`: Configuração do Docker Compose 