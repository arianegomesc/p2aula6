import os
import json
from datetime import datetime
import time
import calendar

def configurar_ambiente():
    """
    Configura o ambiente de trabalho para o gerenciador de eventos.
    
    """
    pasta_dados = "dados"
    os.makedirs(pasta_dados, exist_ok=True)
    caminho_arquivo = os.path.join(pasta_dados, "eventos.json")

    return caminho_arquivo

def carregar_eventos(caminho_arquivo):

    if os.path.exists(caminho_arquivo):
        try:
            with open(caminho_arquivo, "r") as arquivo:
                eventos = json.load(arquivo)
                return eventos
        except (json.JSONDecodeError, IOError):
            print("Erro ao carregar os eventos. Iniciando com uma lista vazia.")
            return []
    else:
        return []
    
def salvar_eventos(caminho_arquivo, eventos):
    try:
        with open(caminho_arquivo, "w", encoding="utf-8") as arquivo:
            json.dump(eventos, arquivo, indent=2, ensure_ascii=False)
        print("Eventos salvos com sucesso.")
    except IOError as e:
        print(f"Erro ao salvar os eventos: {e}")

def adicionar_evento(eventos,caminho_arquivo):
    titulo = input("Digite o título do evento: ").strip()

    if not titulo:
        print("O título do evento não pode ser vazio.")
        return
    
    data_hora_valida = False
    data_hora_str = None

    while not data_hora_valida:
        try:
            data_hora_str = input("Digite a data e hora do evento (formato: DD/MM/AAAA HH:MM): ").strip()
            datetime_obj = datetime.strptime(data_hora_str, "%d/%m/%Y %H:%M")
            data_hora_valida = True
            data_hora_str = datetime_obj.isoformat()
        except ValueError:    
            print("Formato de data e hora inválido. Por favor, tente novamente.")

    evento = {
        "titulo": titulo,
        "data_hora": data_hora_str
    }
    eventos.append(evento)

     # Salva os eventos no arquivo
    salvar_eventos(caminho_arquivo, eventos )

    print(f"Evento '{titulo}'adicionado com sucesso.")

def listar_eventos(eventos):
    if not eventos:
        print("Nenhum evento cadastrado.")
        return
    eventos_ordenados = sorted(eventos, key=lambda e: e["data_hora"])
    agora = datetime.now()

    print("\n📋 Eventos cadastrados:\n")

    for i, evento in enumerate(eventos_ordenados, start=1):
        data_hora_obj = datetime.fromisoformat(evento["data_hora"])

        if data_hora_obj < agora:
            status = "[Passado]"
        else:
            status = "[Futuro]"

        data_formatada = data_hora_obj.strftime("%d/%m/%Y %H:%M")

        print(f"{i}. {evento['titulo']} - {data_formatada} {status}")
        print("-" * 40)

def menu_principal():
    """
    Menu principal do programa.
    Args:
        None
    Retorna:
        None
    """
    # Configura o ambiente (cria pastas e define caminhos)
    caminho_arquivo = configurar_ambiente()
    
    # Carrega os eventos existentes
    eventos = carregar_eventos(caminho_arquivo)
    
    # Loop principal do programa
    # Continua até que o usuário escolha sair (opção 5)
    while True:
        print("\n" + "="*50)
        print("📅 GERENCIADOR DE EVENTOS E AGENDAMENTO")
        print("="*50)
        print("\n1️⃣  Adicionar evento")
        print("2️⃣  Listar eventos")
        print("3️⃣  Visualizar calendário")
        print("4️⃣  Sair")
        print("\n" + "="*50)
        
        # Solicita a opção do usuário
        opcao = input("\n👉 Escolha uma opção (1-4): ").strip()
        
        # Estrutura if/elif/else para tratar cada opção
        if opcao == "1":
            # Opção 1: Adicionar evento
            adicionar_evento(eventos, caminho_arquivo)
            # Recarrega os eventos após adicionar
            eventos = carregar_eventos(caminho_arquivo)
            
        elif opcao == "2":
            # Opção 2: Listar eventos
            listar_eventos(eventos)
            
        #elif opcao == "3":
            # Opção 3: Visualizar calendário
            #visualizar_calendario()
            
        elif opcao == "4":
            # Opção 4: Sair do programa
            print("\n👋 Até logo! Programa encerrado.\n")
            break
            
        else:
            # Opção inválida
            print("❌ Opção inválida! Por favor, escolha 1, 2, 3 ou 4.\n")

if __name__ == "__main__":
    menu_principal()





