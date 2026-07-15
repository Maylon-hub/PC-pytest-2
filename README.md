# Exercícios de Introdução ao Pytest (Parte 2) — Fixtures

Este repositório contém a resolução da lista de exercícios práticos da aula **Engenharia de Software II — Introdução ao pytest (Parte 2)**, ministrada pelo **Prof. Vinicius H. S. Durelli** (vinicius.durelli@ufscar.br).

O objetivo deste projeto é exercitar os conceitos de **fixtures** do pytest:
* Criação de fixtures simples;
* Reutilização de fixtures;
* Modificação do escopo das fixtures (`scope="module"`);
* Gerenciamento de setup e teardown utilizando `yield` e captura de stdout com `-s`.

---

## 🛠️ Instalação e Configuração

Para executar este projeto localmente, siga os passos abaixo no seu terminal (em sistemas Windows/PowerShell):

### 1. Criar o Ambiente Virtual
```powershell
python -m venv .venv
```

### 2. Ativar o Ambiente Virtual
```powershell
.venv\Scripts\Activate.ps1
```

### 3. Instalar as Dependências
```powershell
pip install -r requirements.txt
```

---

## 📂 Estrutura de Arquivos
* `test_fixtures.py`: Arquivo de teste contendo todas as fixtures e funções de testes implementadas para os exercícios 1 a 4.
* `requirements.txt`: Arquivo com a especificação e congelamento das dependências do projeto (versão do `pytest`).
* `README.md`: Este documento explicativo da resolução e execução das tarefas.

---

## 📝 Resolução dos Exercícios

Abaixo está o detalhamento de cada uma das partes resolvidas no arquivo [test_fixtures.py](file:///d:/GitHub/ES2/PC%20pytest%202/test_fixtures.py).

### Parte 1: Criando Fixtures Simples (Exercício 1)
Foram declaradas três fixtures retornando tipos primitivos/coleções e um teste para validar cada uma delas:
1. `lista_frutas`: Retorna uma lista de strings (`["maçã", "banana", "laranja"]`).
2. `config_usuario`: Retorna um dicionário de configuração de usuário (`{"nome": "Maylon", "admin": True, "tema": "escuro"}`).
3. `coordenadas_gps`: Retorna uma tupla contendo latitude e longitude (`(-21.97961, -47.88125)`).

### Parte 2: Reutilizando Fixtures (Exercício 2)
Escolheu-se a fixture `lista_frutas` para ser reutilizada por múltiplos testes. Adicionou-se mais dois testes no arquivo:
* `test_reuso_frutas_tamanho`: verifica se o tamanho da lista é igual a 3.
* `test_reuso_frutas_conteudo`: verifica se a fruta `"maçã"` está presente na lista.

Executou-se o teste com a flag `--setup-show`:
```powershell
pytest --setup-show test_fixtures.py
```

**Resultado:**
O pytest executou o SETUP e o TEARDOWN da fixture `lista_frutas` de forma independente antes e depois de cada teste (`SETUP F lista_frutas`), pois o escopo padrão é por função (`function`).

---

### Parte 3: Alterando o Escopo da Fixture (Exercício 3)
Alterou-se o escopo da fixture `lista_frutas` adicionando o argumento `scope="module"` ao decorador:
```python
@pytest.fixture(scope="module")
def lista_frutas():
    ...
```

Executou-se novamente o comando:
```powershell
pytest --setup-show test_fixtures.py
```

**Saída Obtida:**
```text
test_fixtures.py 
    SETUP    M lista_frutas
        test_fixtures.py::test_lista_frutas (fixtures used: lista_frutas) .
        SETUP    F config_usuario
        test_fixtures.py::test_config_usuario (fixtures used: config_usuario) .
        TEARDOWN F config_usuario
        SETUP    F coordenadas_gps
        test_fixtures.py::test_coordenadas_gps (fixtures used: coordenadas_gps) .
        TEARDOWN F coordenadas_gps
        test_fixtures.py::test_reuso_frutas_tamanho (fixtures used: lista_frutas) .
        test_fixtures.py::test_reuso_frutas_conteudo (fixtures used: lista_frutas) .
    TEARDOWN M lista_frutas
```

**O que mudou?**
O prefixo do setup mudou de `F` (função) para `M` (módulo). Com o escopo `"module"`, o setup da fixture `lista_frutas` passou a ser executado apenas **uma única vez** antes do primeiro teste que o necessita (`test_lista_frutas`), e o teardown foi executado apenas **uma vez** após o último teste do arquivo que a utilizou (`test_reuso_frutas_conteudo`). Isso evita recriar o recurso desnecessariamente a cada teste.

---

### Parte 4: Usando `yield` (Exercício 4)
Para implementar o ciclo completo de vida (Setup e Teardown) com controle de liberação de recursos, alterou-se a fixture `lista_frutas` substituindo o `return` por `yield` e adicionando mensagens de depuração:

```python
@pytest.fixture(scope="module")
def lista_frutas():
    print("\n[SETUP] Inicializando a lista de frutas...")
    yield ["maçã", "banana", "laranja"]
    print("\n[TEARDOWN] Limpando a lista de frutas...")
```

Executou-se o comando com a flag `-s` para desabilitar a captura do stdout do pytest e `-v` para visualização detalhada:
```powershell
pytest -s -v test_fixtures.py
```

**Saída Obtida no Terminal:**
```text
test_fixtures.py::test_lista_frutas 
[SETUP] Inicializando a lista de frutas...
PASSED
test_fixtures.py::test_config_usuario PASSED
test_fixtures.py::test_coordenadas_gps PASSED
test_fixtures.py::test_reuso_frutas_tamanho PASSED
test_fixtures.py::test_reuso_frutas_conteudo PASSED
[TEARDOWN] Limpando a lista de frutas...
```

Percebe-se claramente o log de `[SETUP]` sendo printado imediatamente antes da execução do primeiro teste que depende da fixture, e o log de `[TEARDOWN]` sendo executado somente ao término de toda a execução de testes do arquivo.

---

## 🎯 Código Completo de Testes (`test_fixtures.py`)

Abaixo está a listagem do código final gerado para a resolução de todos os exercícios da aula:

```python
import pytest

# Fixture que retorna uma lista de frutas com escopo de módulo e controle por yield
@pytest.fixture(scope="module")
def lista_frutas():
    print("\n[SETUP] Inicializando a lista de frutas...")
    yield ["maçã", "banana", "laranja"]
    print("\n[TEARDOWN] Limpando a lista de frutas...")

# Fixture que retorna um dicionário de configuração de usuário (escopo padrão: function)
@pytest.fixture()
def config_usuario():
    return {"nome": "Maylon", "admin": True, "tema": "escuro"}

# Fixture que retorna uma tupla com coordenadas GPS (escopo padrão: function)
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
```

---

## 📬 Entrega do Repositório
Este repositório está estruturado e pronto para envio por e-mail para o professor. Recomenda-se compactar a pasta do projeto (desconsiderando o diretório `.venv` e `.pytest_cache`) ou fornecer o link do repositório remoto para avaliação.
