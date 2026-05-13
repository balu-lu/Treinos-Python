# 📋 Comandos para Configurar Dependências de Teste

Execute os comandos abaixo no terminal para adicionar as dependências necessárias para os testes:

## Adicionar pytest como dependência de desenvolvimento

```bash
poetry add --group dev pytest
```

## Adicionar httpx (necessária para TestClient do FastAPI)

```bash
poetry add --group dev httpx
```

## Adicionar pytest-cov para relatórios de cobertura de código

```bash
poetry add --group dev pytest-cov
```

## Alternativa: Adicionar todas as dependências de teste em um único comando

```bash
poetry add --group dev pytest httpx pytest-cov pytest-asyncio
```

---

## ✅ Verificar as dependências instaladas

Após executar os comandos, verifique se tudo foi instalado corretamente:

```bash
poetry show --only dev
```

## 🚀 Rodar os testes localmente

Antes de fazer push, teste localmente:

```bash
poetry run pytest -v
```

### Com relatório de cobertura:

```bash
poetry run pytest -v --cov=APIs --cov-report=html
```

Isso gera um relatório HTML em `htmlcov/index.html`

---

## 📝 Arquivo pyproject.toml será atualizado automaticamente

Quando você executar os comandos `poetry add`, o arquivo `pyproject.toml` será atualizado automaticamente. 
Você verá uma nova seção `[tool.poetry.group.dev.dependencies]` contendo as dependências de desenvolvimento.

**Exemplo de como ficará:**

```toml
[tool.poetry.group.dev.dependencies]
pytest = "^8.0.0"
httpx = "^0.27.0"
pytest-cov = "^5.0.0"
pytest-asyncio = "^0.24.0"
```
