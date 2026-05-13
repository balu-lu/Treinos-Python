# ⚡ Quick Start - CI/CD & Testes

## 🎯 Objetivo
Configurar CI/CD automático no GitHub Actions com testes que funcionam sem dependências externas (Redis).

---

## 1️⃣ Instalar Dependências de Teste

Execute no terminal da raiz do projeto:

```bash
poetry add --group dev pytest httpx pytest-cov pytest-asyncio
```

> ⏱️ Leva ~30-60 segundos

---

## 2️⃣ Rodar Testes Localmente

```bash
poetry run pytest -v
```

**Resultado esperado:**
```
tests/test_main.py::TestEndpointLivros::test_listar_livros_status_200 PASSED
tests/test_main.py::TestEndpointLivros::test_listar_livros_com_redis_online PASSED
tests/test_main.py::TestEndpointLivros::test_listar_livros_estrutura_resposta PASSED
tests/test_main.py::TestEndpointLivros::test_listar_livros_dados_iniciais PASSED
tests/test_main.py::TestHealthCheck::test_app_is_running PASSED

===================== 5 passed in 0.12s =====================
```

---

## 3️⃣ Gerar Relatório de Cobertura

```bash
poetry run pytest -v --cov=APIs --cov-report=html
```

Depois, abra `htmlcov/index.html` no navegador para ver a cobertura.

---

## 4️⃣ Fazer Push para GitHub

```bash
git add .
git commit -m "ci: add GitHub Actions workflow and tests"
git push origin main
```

**O que acontece automaticamente:**
- GitHub Actions detecta o push
- Cria um runner com Python 3.13
- Instala Poetry
- Roda pytest
- Gera relatório de cobertura
- Status aparece no PR/commit

---

## 📂 Arquivos Criados

| Arquivo | Descrição |
|---------|-----------|
| `.github/workflows/python-app.yml` | Workflow do GitHub Actions |
| `tests/test_main.py` | Testes funcionais (5 testes) |
| `tests/conftest.py` | Configuração global dos testes |
| `pytest.ini` | Configurações do pytest |
| `.coveragerc` | Configurações de cobertura |
| `CI_CD_GUIDE.md` | Documentação completa |
| `SETUP_TESTES.md` | Guia de dependências |

---

## 🔍 Como os Testes Funcionam Sem Redis?

**Mock do Redis:**
```python
with patch('app.obter_conexao_redis', new_callable=AsyncMock) as mock_redis:
    mock_redis.return_value = None  # Simula Redis offline
    response = client.get("/livros")
    assert response.status_code == 200  # ✅ Ainda retorna 200!
```

Isso funciona porque sua API (`APIs/app.py`) trata o Redis como opcional:
```python
redis_conn = await obter_conexao_redis()
if redis_conn is None:
    # Retorna os dados em memória normalmente
    return livros
```

---

## 🚨 Troubleshooting

### Erro: `ModuleNotFoundError: No module named 'app'`
**Solução:**
```bash
poetry install
poetry run pytest
```

### Erro: `ImportError: cannot import name 'TestClient'`
**Solução:**
```bash
poetry add --group dev httpx
poetry install
```

### Testes não são encontrados
**Solução:**
```bash
# Verifique a estrutura
ls tests/test_*.py

# Rode com descoberta verbosa
poetry run pytest --collect-only
```

---

## 📊 Próximo Passo: Validação no GitHub

1. Faça push do código
2. Abra um Pull Request
3. Observe a aba "Checks" no PR
4. Veja o workflow rodando em tempo real
5. Espere passar ✅

---

## 🎓 Estrutura Final do Projeto

```
Python/
├── .github/
│   └── workflows/
│       └── python-app.yml          ← CI/CD Workflow
├── APIs/
│   ├── app.py                       ← Sua API
│   ├── main.py
│   └── auth.py
├── tests/
│   ├── test_main.py                 ← Testes (5 casos)
│   └── conftest.py                  ← Configuração
├── .gitignore                       ← Já configurado
├── .coveragerc                      ← Config de cobertura
├── pytest.ini                       ← Config do pytest
├── pyproject.toml                   ← Dependências
├── CI_CD_GUIDE.md                   ← Docs detalhadas
└── SETUP_TESTES.md                  ← Comandos
```

---

## ✅ Checklist de Conclusão

- [ ] Executei `poetry add --group dev pytest httpx pytest-cov pytest-asyncio`
- [ ] Rodei `poetry run pytest -v` e os 5 testes passaram
- [ ] Verifiquei que `.github/workflows/python-app.yml` foi criado
- [ ] Fiz commit e push dos arquivos
- [ ] GitHub Actions rodou automaticamente (verificar aba Actions)
- [ ] O workflow passou (verde) ✅

---

## 🎉 Parabéns!

Seu projeto FastAPI agora tem:
- ✅ CI/CD automático com GitHub Actions
- ✅ Testes funcionais que não dependem de Redis
- ✅ Relatórios de cobertura de código
- ✅ Cache de dependências para builds mais rápidos
- ✅ Validação em todo push/PR

**Seu pipeline está pronto para produção!** 🚀
