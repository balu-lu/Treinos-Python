"""
Template para adicionar mais testes à medida que sua API cresce.

Copie este arquivo como referência quando adicionar novos endpoints.
"""

from app import app, Livro, LivroInput
import sys
import os
import pytest
from fastapi.testclient import TestClient
from unittest.mock import patch, AsyncMock

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'APIs'))


@pytest.fixture
def client():
    """Cliente de teste para a API."""
    return TestClient(app)


# ============================================================================
# TEMPLATE: Teste para POST (Criar novo livro)
# ============================================================================

class TestCriarLivro:
    """
    Template para testes de criação de recursos.
    Descomente e adapte conforme necessário.
    """

    # def test_criar_livro_sucesso(self, client):
    #     """Testa criação de um novo livro."""
    #     novo_livro = {
    #         "titulo": "O Hobbit",
    #         "autor": "J.R.R. Tolkien",
    #         "ano": 1937,
    #         "disponivel": True
    #     }
    #
    #     response = client.post("/livros", json=novo_livro)
    #
    #     assert response.status_code == 201  # Created
    #     data = response.json()
    #     assert data["titulo"] == "O Hobbit"
    #     assert "id" in data
    #
    #
    # def test_criar_livro_dados_invalidos(self, client):
    #     """Testa criação com dados inválidos."""
    #     novo_livro = {
    #         "titulo": "",  # Título vazio!
    #         "autor": "Autor",
    #         "ano": 1937
    #     }
    #
    #     response = client.post("/livros", json=novo_livro)
    #
    #     assert response.status_code == 422  # Validation Error


# ============================================================================
# TEMPLATE: Teste para GET por ID (Buscar um livro específico)
# ============================================================================

class TestBuscarLivroPorId:
    """
    Template para testes de busca por ID.
    """

    # def test_buscar_livro_existente(self, client):
    #     """Testa busca de um livro que existe."""
    #     response = client.get("/livros/1")
    #
    #     assert response.status_code == 200
    #     data = response.json()
    #     assert data["id"] == 1
    #     assert "titulo" in data
    #
    #
    # def test_buscar_livro_inexistente(self, client):
    #     """Testa busca de um livro que não existe."""
    #     response = client.get("/livros/999")
    #
    #     assert response.status_code == 404
    #     assert "Not found" in response.json()["detail"]


# ============================================================================
# TEMPLATE: Teste para PUT (Atualizar livro)
# ============================================================================

class TestAtualizarLivro:
    """
    Template para testes de atualização.
    """

    # def test_atualizar_livro_sucesso(self, client):
    #     """Testa atualização de um livro."""
    #     livro_atualizado = {
    #         "titulo": "O Hobbit (Edição Especial)",
    #         "autor": "J.R.R. Tolkien",
    #         "ano": 1937,
    #         "disponivel": False
    #     }
    #
    #     response = client.put("/livros/1", json=livro_atualizado)
    #
    #     assert response.status_code == 200
    #     data = response.json()
    #     assert data["titulo"] == "O Hobbit (Edição Especial)"
    #     assert data["disponivel"] is False


# ============================================================================
# TEMPLATE: Teste para DELETE (Deletar livro)
# ============================================================================

class TestDeletarLivro:
    """
    Template para testes de exclusão.
    """

    # def test_deletar_livro_sucesso(self, client):
    #     """Testa deleção de um livro."""
    #     response = client.delete("/livros/1")
    #
    #     assert response.status_code == 204  # No Content
    #
    #     # Verifica que foi deletado
    #     response = client.get("/livros/1")
    #     assert response.status_code == 404


# ============================================================================
# TEMPLATE: Testes com Banco de Dados (SQLAlchemy)
# ============================================================================

class TestIntegracaoComBD:
    """
    Template para testes que precisam mockar banco de dados.
    """

    # @patch('app.get_db')
    # def test_livros_do_banco_de_dados(self, mock_db, client):
    #     """Testa leitura de livros do banco de dados."""
    #     mock_db.query.return_value.all.return_value = [
    #         Livro(id=1, titulo="Livro 1", autor="Autor 1", ano=2020),
    #         Livro(id=2, titulo="Livro 2", autor="Autor 2", ano=2021),
    #     ]
    #
    #     response = client.get("/livros")
    #
    #     assert response.status_code == 200
    #     assert len(response.json()) == 2


# ============================================================================
# TEMPLATE: Testes de Performance/Carga
# ============================================================================

class TestPerformance:
    """
    Template para testes de performance.
    Requer: pytest-benchmark
    """

    # def test_listar_livros_performance(self, client, benchmark):
    #     """Testa performance do endpoint."""
    #     def fazer_requisicao():
    #         return client.get("/livros")
    #
    #     result = benchmark(fazer_requisicao)
    #     assert result.status_code == 200


# ============================================================================
# TEMPLATE: Testes de Autenticação/Autorização
# ============================================================================

class TestAutenticacao:
    """
    Template para testes de autenticação.
    """

    # def test_endpoint_protegido_sem_token(self, client):
    #     """Testa acesso a endpoint protegido sem token."""
    #     response = client.get("/livros/admin")
    #
    #     assert response.status_code == 401  # Unauthorized
    #
    #
    # def test_endpoint_protegido_com_token(self, client):
    #     """Testa acesso a endpoint protegido com token válido."""
    #     token = "seu_token_aqui"
    #     headers = {"Authorization": f"Bearer {token}"}
    #
    #     response = client.get("/livros/admin", headers=headers)
    #
    #     assert response.status_code == 200


# ============================================================================
# TEMPLATE: Testes de Validação de Entrada
# ============================================================================

class TestValidacaoDeEntrada:
    """
    Template para testes de validação.
    """

    # def test_validar_ano_negativo(self, client):
    #     """Testa validação de ano negativo."""
    #     novo_livro = {
    #         "titulo": "Livro",
    #         "autor": "Autor",
    #         "ano": -1900,  # Ano inválido
    #     }
    #
    #     response = client.post("/livros", json=novo_livro)
    #
    #     assert response.status_code == 422
    #
    #
    # def test_validar_titulo_vazio(self, client):
    #     """Testa validação de título vazio."""
    #     novo_livro = {
    #         "titulo": "",  # Vazio!
    #         "autor": "Autor",
    #         "ano": 2020,
    #     }
    #
    #     response = client.post("/livros", json=novo_livro)
    #
    #     assert response.status_code == 422


# ============================================================================
# TEMPLATE: Testes Parametrizados (múltiplos casos com um teste)
# ============================================================================

class TestParametrizados:
    """
    Template para testes parametrizados.
    Útil para testar múltiplos cenários com uma função.
    """

    # @pytest.mark.parametrize("ano", [1900, 1950, 2000, 2023])
    # def test_livros_de_diferentes_anos(self, client, ano):
    #     """Testa livros de diferentes anos."""
    #     novo_livro = {
    #         "titulo": f"Livro de {ano}",
    #         "autor": "Autor",
    #         "ano": ano,
    #     }
    #
    #     response = client.post("/livros", json=novo_livro)
    #
    #     assert response.status_code == 201
    #     assert response.json()["ano"] == ano


# ============================================================================
# DICAS E BOAS PRÁTICAS
# ============================================================================

"""
DICAS PARA ESCREVER BONS TESTES:

1. **Nomeação Clara**
   - test_[função/endpoint]_[cenário]_[resultado esperado]
   - ✅ test_criar_livro_com_dados_validos_retorna_201
   - ❌ test_livro

2. **AAA Pattern** (Arrange-Act-Assert)
   - Arrange: Preparar dados
   - Act: Executar a ação
   - Assert: Verificar resultado
   
3. **Um Assert Principal**
   - Teste deve verificar UMA coisa principal
   - Asserts adicionais são OK para contexto
   - Muito complexo? Quebra em testes menores

4. **Fixtures para Reutilização**
   - Use @pytest.fixture para dados/clients compartilhados
   - Evita duplicação de código

5. **Mocks com Propósito**
   - Mocke apenas dependências externas (Redis, BD, APIs)
   - Não mocke seu próprio código
   - Mock de um retorno None? Teste ambos os casos

6. **Testes Independentes**
   - Cada teste deve ser autossuficiente
   - Não dependa da ordem de execução
   - Testes podem rodar em qualquer ordem

7. **Cobertura vs Qualidade**
   - 100% de cobertura não significa código bom
   - Teste cenários importantes e casos extremos
   - Edge cases são importantes

8. **Velocidade**
   - Testes devem rodar rápido (< 1s por teste)
   - Use mocks em vez de I/O real
   - Considere testes de integração separados

9. **Documentação**
   - Docstring clara: o que testa e por quê
   - Código legível é auto-documentável

10. **Marcadores Úteis**
    @pytest.mark.slow       # Para testes lentos
    @pytest.mark.skip       # Para pular
    @pytest.mark.parametrize # Para múltiplos casos
"""
