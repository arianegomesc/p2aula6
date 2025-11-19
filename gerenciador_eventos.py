import os
import json
from datetime import datetime
import time
import calendar

def configurar_ambiente():
    """Configura o ambiente de trabalho para o gerenciador de eventos."""
    
    pasta_dados = "dados"
    os.makedirs(pasta_dados, exist_ok=True)
    caminho_arquivo = os.path.join(pasta_dados, "eventos.json")

    return caminho_arquivo

def carregar_eventos(caminho_arquivo):
    """Carrega os eventos do arquivo JSON."""

    if os.path.exists(caminho_arquivo):
        try:
            with open(caminho_arquivo, "r") as arquivo:
                eventos = json.load(arquivo)
                return eventos
        except (json.JSONDecodeError, IOError):
            print("Erro ao carregar os eventos. O arquivo pode estar corrompido.")
            return []
        else:
            return [] # retorna uma lista vazia se o arquivo não existir
        
def salvar_eventos(caminho_arquivo, eventos):
    """Salva os eventos no arquivo JSON."""

    try:
        with open(caminho_arquivo, "w", enconding="utf-8") as arquivo:
            json.dump(eventos, arquivo, indent=2, ensure_ascii=False)
        print("Eventos salvos com sucesso.")
    except IOError as e:
        print(f"Erro ao salvar os eventos: {e}")

def adicionar_evento(eventos):
    titulo = input("Digite o título do evento: ").strip()

    if not titulo:
        print("O título do evento não pode ser vazio.")
        return
    data_hora_valida = False
    data_hora_str = None

    while not data_hora_valida:
        try:
            data_hora_str = input("Digite a data e hora do evento (DD-MM-AAAA HH:MM): ")
            datetime_obj = datetime.strptime(data_hora_str, "%d-%m-%Y %H:%M")
            data_hora_valida = True
            data_hora_str = datetime_obj.isoformat()
        except ValueError:
            print("Formato de data/hora inválido. Tente novamente.")

    evento = {
        "titulo": titulo,
        "data_hora": data_hora_str
    }

    eventos.append(evento)
    print(f"Evento '{titulo}' adicionado com sucesso.")

def listar_eventos(eventos):
    if not eventos:
        print("Nenhum evento encontrado.")
        return
    eventos_ordenados = sorted(eventos, key=lambda e: e["data_hora"])
    agora = datetime.now()

    print("Eventos cadastrados:\n")

    for i, evento in enumerate(eventos_ordenados, start=1):
        data_hora_obj = datetime.fromisoformat(evento["data_hora"])

        if data_hora_obj < agora:
            status = "[Passado]" 
        else:
            status = "[Futuro]"
           
        data_hora_formatada = data_hora_obj.strftime("%d-%m-%Y %H:%M")

        print(f"{i}. {evento['titulo']} - {data_hora_formatada} {status}")
        print("-" *40)
    





