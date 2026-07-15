import pytest

# Fixture que retorna uma lista de frutas
@pytest.fixture(scope="module")
def lista_frutas():
    print("\n[SETUP] Inicializando a lista de frutas...")
    yield ["maçã", "banana", "laranja"]
    print("\n[TEARDOWN] Limpando a lista de frutas...")

# Fixture que retorna um dicionário de configuração de usuário
@pytest.fixture()
def config_usuario():
    return {"nome": "Maylon", "admin": True, "tema": "escuro"}

# Fixture que retorna uma tupla com coordenadas GPS
@pytest.fixture()
def coordenadas_gps():
    return (-21.97961, -47.88125)

# Teste para a fixture de lista
def test_lista_frutas(lista_frutas):
    assert "banana" in lista_frutas
    assert len(lista_frutas) == 3

# Teste para a fixture de dicionário
def test_config_usuario(config_usuario):
    assert config_usuario["admin"] is True
    assert config_usuario["tema"] == "escuro"

# Teste para a fixture de tupla
def test_coordenadas_gps(coordenadas_gps):
    assert len(coordenadas_gps) == 2
    assert coordenadas_gps[0] == -21.97961

# Testes de reuso para o Exercício 2
def test_reuso_frutas_tamanho(lista_frutas):
    assert len(lista_frutas) == 3

def test_reuso_frutas_conteudo(lista_frutas):
    assert "maçã" in lista_frutas
