# 📅 Gerenciador de Eventos com FastAPI e Streamlit

Este projeto é um sistema simples para gerenciamento de eventos, utilizando uma arquitetura com *backend* e *frontend* separados, o que permite o registro, listagem e visualização de eventos em um banco de dados SQLite.

## ✨ Tecnologias Utilizadas

O projeto utiliza as seguintes tecnologias principais:

* **Linguagem:** Python 3.12 (ou superior), gerenciado via `pyenv-win`.
* **Backend (API):** **FastAPI** e **Uvicorn**
* **Persistência:** **SQLAlchemy** (ORM) e **SQLite** (banco de dados)
* **Frontend (Interface Web):** **Streamlit**
* **Comunicação:** `requests` (para o frontend se comunicar com o backend).
* **Dependências C++:** `pyarrow` (instalado via *wheel* para evitar erros de compilação).

---

## 🚀 Estrutura do Projeto

* `backend.py`: Contém a definição da API (FastAPI), a lógica de banco de dados e o Modelo ORM (SQLAlchemy) para a tabela `eventos`.
* `frontend.py`: Contém a interface gráfica (Streamlit) para interação com o usuário.
* `.venv/`: Pasta do ambiente virtual, que isola as dependências.
* `requirements.txt`: Lista todas as bibliotecas necessárias para instalação.
* `eventos.db`: O arquivo de banco de dados SQLite gerado pelo SQLAlchemy.

---

## 🛠️ Configuração e Instalação (Setup)

Siga estas etapas para configurar e instalar o projeto no seu sistema Windows, garantindo que o ambiente complexo seja configurado corretamente.

### 1. Clonar o Repositório

```bash
git clone [https://github.com/arianegomesc/gerenciador-eventos-fastAPI](https://github.com/arianegomesc/gerenciador-eventos-fastAPI)
cd p2aula6