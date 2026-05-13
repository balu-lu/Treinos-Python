"""
Testes funcionais para a API de Livros.

Utiliza o TestClient do FastAPI para fazer requisições sem precisar
de um servidor rodando. Redis será mockado para testes sem dependências externas.
"""

from app import app, Livro, LivroInput
import sys
import os
import pytest
from fastapi.testclient import TestClient
from unittest.mock import patch, AsyncMock

# Adiciona o diretório APIs ao path para importação
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'APIs'))

# Importa a aplicação FastAPI


@pytest.fixture
def client():
    """Fixture que cria um cliente de teste para a API."""
    return TestClient(app)


class TestEndpointLivros:
    """Testes para o endpoint GET /livros."""

    def test_listar_livros_status_200(self, client):
        """
        Testa se o endpoint GET /livros retorna status 200 OK
        mesmo quando Redis está offline.
        """
        # Mock da conexão com Redis para simular indisponibilidade
        with patch('app.obter_conexao_redis', new_callable=AsyncMock) as mock_redis:
            mock_redis.return_value = None  # Redis offline

            response = client.get("/livros")

            # Validação: status code deve ser 200
            assert response.status_code == 200

            # Validação: resposta deve conter uma lista
            data = response.json()
            assert isinstance(data, list)

    def test_listar_livros_com_redis_online(self, client):
        """
        Testa se o endpoint GET /livros retorna status 200
        quando Redis está disponível (simulado).
        """
        import json

        with patch('app.obter_conexao_redis', new_callable=AsyncMock) as mock_redis:
            # Simula Redis disponível com dados em cache
            mock_redis_instance = AsyncMock()
            mock_redis_instance.ping.return_value = True

            # Mocka o método .get() para retornar dados em JSON
            livros_json = json.dumps([
                {"id": 1, "titulo": "O Senhor dos Anéis",
                    "autor": "J.R.R. Tolkien", "ano": 1954, "disponivel": True},
                {"id": 2, "titulo": "1984", "autor": "George Orwell",
                    "ano": 1949, "disponivel": True}
            ], ensure_ascii=False)
            mock_redis_instance.get.return_value = livros_json

            mock_redis.return_value = mock_redis_instance

            response = client.get("/livros")

            # Validação
            assert response.status_code == 200
            data = response.json()
            assert isinstance(data, list)
            assert len(data) >= 2

    def test_listar_livros_estrutura_resposta(self, client):
        """
        Testa se a resposta contém a estrutura correta de um Livro.
        """
        with patch('app.obter_conexao_redis', new_callable=AsyncMock) as mock_redis:
            mock_redis.return_value = None

            response = client.get("/livros")
            data = response.json()

            # Validação: deve ter pelo menos um livro
            assert len(data) > 0

            # Validação: cada item deve ter os campos obrigatórios
            for livro in data:
                assert "id" in livro
                assert "titulo" in livro
                assert "autor" in livro
                assert "ano" in livro
                assert "disponivel" in livro

                # Validação de tipos
                assert isinstance(livro["id"], int)
                assert isinstance(livro["titulo"], str)
                assert isinstance(livro["autor"], str)
                assert isinstance(livro["ano"], int)
                assert isinstance(livro["disponivel"], bool)

    def test_listar_livros_dados_iniciais(self, client):
        """
        Testa se os dados iniciais da API estão corretos.
        """
        with patch('app.obter_conexao_redis', new_callable=AsyncMock) as mock_redis:
            mock_redis.return_value = None

            response = client.get("/livros")
            data = response.json()

            # Validação: deve ter pelo menos 2 livros iniciais
            assert len(data) >= 2

            # Validação: verificar presença de livros conhecidos
            titulos = [livro["titulo"] for livro in data]
            assert "O Senhor dos Anéis" in titulos
            assert "1984" in titulos


class TestHealthCheck:
    """Testes gerais da API."""

    def test_app_is_running(self, client):
        """
        Testa se a aplicação FastAPI está respondendo
        através de um endpoint simples.
        """
        # Testa o endpoint raiz (geralmente retorna docs ou 404)
        # Aqui apenas validamos que a app não está quebrada
        response = client.get("/docs")
        assert response.status_code == 200  # Swagger UI deve estar disponível


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
