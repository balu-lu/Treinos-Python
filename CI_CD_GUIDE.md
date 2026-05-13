# 🚀 CI/CD Pipeline com GitHub Actions - FastAPI

## 📋 Visão Geral

Este projeto está configurado com um pipeline completo de CI/CD via GitHub Actions. Toda vez que você fizer um push ou abrir um Pull Request na branch `main`, os testes rodam automaticamente.

---

## 📁 Arquivos Criados

### 1. `.github/workflows/python-app.yml`
**Workflow do GitHub Actions que:**
- ✅ Roda em `ubuntu-latest`
- ✅ Testa com Python 3.13
- ✅ Instala Poetry e dependências
- ✅ Cach as dependências do Poetry para acelerar builds
- ✅ Executa os testes com pytest
- ✅ Gera relatório de cobertura
- ✅ Faz upload do coverage para Codecov

### 2. `tests/test_main.py`
**Testes funcionais que:**
- ✅ Usam `TestClient` do FastAPI (não requer servidor rodando)
- ✅ Mockam a conexão com Redis (testes rodam sem Redis)
- ✅ Validam status 200 do endpoint GET `/livros`
- ✅ Testam estrutura de resposta
- ✅ Verificam dados iniciais

### 3. `tests/conftest.py`
**Configuração global dos testes:**
- ✅ Define o path para importações
- ✅ É carregado automaticamente pelo pytest

### 4. `pytest.ini`
**Configuração do pytest:**
- ✅ Define diretório de testes: `tests/`
- ✅ Padrão de descoberta de testes
- ✅ Configurações de output e markers

### 5. `.coveragerc`
**Configuração de cobertura de código:**
- ✅ Define source a ser analisado: `APIs/`
- ✅ Exclui arquivos de teste e venv
- ✅ Exclui padrões comuns de código não testável

### 6. `SETUP_TESTES.md`
**Guia de setup das dependências de teste**

---

## 🛠️ Setup Inicial

### Passo 1: Adicionar dependências de desenvolvimento

```bash
poetry add --group dev pytest httpx pytest-cov pytest-asyncio
```

### Passo 2: Instalar todas as dependências

```bash
poetry install
```

### Passo 3: Rodar os testes localmente

```bash
poetry run pytest -v
```

---

## 📊 Estrutura dos Testes

### Testes Implementados

```
tests/
├── test_main.py
│   ├── TestEndpointLivros
│   │   ├── test_listar_livros_status_200() ✅
│   │   ├── test_listar_livros_com_redis_online() ✅
│   │   ├── test_listar_livros_estrutura_resposta() ✅
│   │   └── test_listar_livros_dados_iniciais() ✅
│   └── TestHealthCheck
│       └── test_app_is_running() ✅
└── conftest.py
```

### Exemplo de Teste

Os testes usam `unittest.mock` para mockar o Redis:

```python
def test_listar_livros_status_200(self, client):
    with patch('app.obter_conexao_redis', new_callable=AsyncMock) as mock_redis:
        mock_redis.return_value = None  # Redis offline
        
        response = client.get("/livros")
        
        assert response.status_code == 200
        assert isinstance(response.json(), list)
```

---

## 🔄 Fluxo de CI/CD

```
┌─────────────────────┐
│  Push/PR na main    │
└──────────┬──────────┘
           │
           ▼
┌──────────────────────────────┐
│ GitHub Actions Triggers      │
│ (python-app.yml)             │
└──────────┬───────────────────┘
           │
           ▼
┌──────────────────────────────┐
│ 1. Checkout do código        │
└──────────┬───────────────────┘
           │
           ▼
┌──────────────────────────────┐
│ 2. Setup Python 3.13         │
└──────────┬───────────────────┘
           │
           ▼
┌──────────────────────────────┐
│ 3. Instalar Poetry           │
└──────────┬───────────────────┘
           │
           ▼
┌──────────────────────────────┐
│ 4. Cache dependências        │
└──────────┬───────────────────┘
           │
           ▼
┌──────────────────────────────┐
│ 5. Instalar dependências     │
│    (poetry install)          │
└──────────┬───────────────────┘
           │
           ▼
┌──────────────────────────────┐
│ 6. Rodar pytest              │
│    (poetry run pytest)       │
└──────────┬───────────────────┘
           │
           ▼
┌──────────────────────────────┐
│ 7. Upload coverage Codecov   │
└──────────┬───────────────────┘
           │
           ▼
     ✅ ou ❌
```

---

## 🔧 Comandos Úteis

### Rodar testes
```bash
poetry run pytest -v
```

### Rodar com cobertura
```bash
poetry run pytest -v --cov=APIs --cov-report=html
```

### Rodar teste específico
```bash
poetry run pytest -v tests/test_main.py::TestEndpointLivros::test_listar_livros_status_200
```

### Rodar com output detalhado de falhas
```bash
poetry run pytest -v --tb=long
```

### Rodar e parar no primeiro erro
```bash
poetry run pytest -v -x
```

---

## 🐳 Docker & Kubernetes

Se você estiver usando Docker/Kubernetes (como visto em `deployment.yaml`, `service.yaml`, etc.), o pipeline também validará:
- ✅ Sintaxe do código Python
- ✅ Testes unitários e funcionais
- ✅ Cobertura de código

Antes de fazer deploy, esses testes devem passar!

---

## 📈 Monitoramento

### Verificar status do workflow
1. Vá para a aba **Actions** no seu repositório GitHub
2. Veja o status dos últimos workflows
3. Clique em um workflow para ver detalhes

### Codecov (opcional)
Se integrado, você verá um relatório de cobertura em:
- https://app.codecov.io/gh/seu-usuario/seu-repo

---

## 🚀 Próximas Melhorias

- [ ] Adicionar testes de integração com Redis real
- [ ] Testes de performance/load
- [ ] Testes de endpoints POST/PUT/DELETE
- [ ] Análise estática com pylint/flake8
- [ ] Testes de segurança com bandit
- [ ] Deploy automático em staging após testes passarem

---

## 📚 Referências

- [FastAPI Testing](https://fastapi.tiangolo.com/advanced/testing-dependencies/)
- [Pytest Documentation](https://docs.pytest.org/)
- [GitHub Actions with Python](https://github.com/actions/setup-python)
- [Poetry Documentation](https://python-poetry.org/)
