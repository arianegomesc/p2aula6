"""
Gerenciador de Eventos e Agendamento Simples
==============================================

Um programa educacional para demonstrar conceitos fundamentais de Python:
- Funções e estruturas de controle
- Manipulação de estruturas de dados (listas de dicionários)
- Persistência de dados (JSON)
- Manipulação de datas e horas
- Interação com o sistema de arquivos

Módulos utilizados:
- os: Para criar diretórios e gerenciar caminhos de arquivos
- datetime: Para trabalhar com datas e horas (criação, parsing e comparação)
- time: Para inclusão de pausas programáticas (feedback visual)
- calendar: Para exibição de calendários mensais
- json: Para serialização (salvar) e desserialização (carregar) de dados
"""

import os
import json
from datetime import datetime
import time
import calendar


def configurar_ambiente():
    """
    Configura o ambiente de trabalho do programa.
    """
    # Define o nome da pasta de dados
    pasta_dados = "dados"
    
    # Cria a pasta se ela não existir
    os.makedirs(pasta_dados, exist_ok=True)
    
    # Combina o caminho da pasta com o nome do arquivo
    caminho_arquivo = os.path.join(pasta_dados, "eventos.json")
    
    return caminho_arquivo


def carregar_eventos(caminho_arquivo):
    """
    Carrega a lista de eventos armazenados em um arquivo JSON.
    """
    # Verifica se o arquivo existe usando os.path.exists()
    if os.path.exists(caminho_arquivo):
        try:
            # Abre o arquivo em modo leitura ('r')
            with open(caminho_arquivo, "r", encoding="utf-8") as arquivo:
                # json.load() deserializa o conteúdo do arquivo para uma lista Python
                eventos = json.load(arquivo)
                return eventos
        except (json.JSONDecodeError, IOError):
            # Se houver erro na leitura ou no JSON, retorna lista vazia
            print("⚠️  Erro ao carregar eventos. Iniciando com lista vazia.")
            return []
    else:
        # Arquivo não existe, retorna lista vazia
        return []


def salvar_eventos(eventos, caminho_arquivo):
    """
    Salva a lista de eventos em um arquivo JSON.
    Retorna:
        None
    """
    # Exibe mensagem de feedback
    print("💾 Salvando dados...")
    
    # time.sleep(0.5): Pausa por 0,5 segundos para melhorar a experiência visual
    # Útil para demonstrar operações assíncronas e dar feedback visual ao usuário
    time.sleep(0.5)
    
    try:
        # Abre o arquivo em modo escrita ('w')
        with open(caminho_arquivo, "w", encoding="utf-8") as arquivo:
            # json.dump() serializa a lista Python para o formato JSON no arquivo
            # indent=2: Formata o JSON com indentação de 2 espaços (legibilidade)
            json.dump(eventos, arquivo, indent=2, ensure_ascii=False)
        
        print("✅ Dados salvos com sucesso!\n")
    except IOError as e:
        print(f"❌ Erro ao salvar dados: {e}\n")


def adicionar_evento(eventos, caminho_arquivo):
    """
    Adiciona um novo evento à lista de eventos.
    Retorna:
        None
    """
    print("\n" + "="*50)
    print("ADICIONAR NOVO EVENTO")
    print("="*50)
    
    # Solicita o nome do evento
    nome = input("📝 Nome do evento: ").strip()
    
    if not nome:
        print("❌ O nome do evento não pode estar vazio!\n")
        return
    
    # Variável para controlar a validação
    data_hora_valida = False
    data_hora_str = None
    
    # Loop while para garantir que o usuário insira dados válidos
    while not data_hora_valida:
        try:
            # Solicita a data no formato DD-MM-AAAA
            data_str = input("📅 Data (DD-MM-AAAA): ").strip()
            
            # Solicita a hora no formato HH:MM
            hora_str = input("🕐 Hora (HH:MM): ").strip()
            
            # Combina data e hora em uma única string
            data_hora_completa = f"{data_str} {hora_str}"
            
            # DESAFIO 1: Validação com try-except
            # datetime.strptime() tenta converter a string para um objeto datetime
            # Se o formato estiver errado, lança ValueError
            datetime_obj = datetime.strptime(data_hora_completa, "%d-%m-%Y %H:%M")
            
            # Se chegou aqui, o formato é válido
            data_hora_valida = True
            
            # Converte o objeto datetime para string ISO (serializável em JSON)
            # ISO format: AAAA-MM-DDTHH:MM:SS
            data_hora_str = datetime_obj.isoformat()
            
        except ValueError:
            # Captura erros de formato de data/hora
            print("❌ Formato inválido! Use DD-MM-AAAA para data e HH:MM para hora.\n")
    
    # Cria um dicionário com os dados do evento
    novo_evento = {
        "nome": nome,
        "data_hora": data_hora_str  # Armazenado como string ISO para ser JSON-serializável
    }
    
    # Adiciona o novo evento à lista
    eventos.append(novo_evento)
    
    # Salva os eventos no arquivo
    salvar_eventos(eventos, caminho_arquivo)
    
    print(f"✅ Evento '{nome}' adicionado com sucesso!\n")


def listar_eventos(eventos):
    """
    Lista todos os eventos armazenados, indicando se são passados ou futuros.
    Esta função ordena os eventos cronologicamente e exibe-os com formatação.
    Retorna:
        None
    """
    print("\n" + "="*50)
    print("LISTAR EVENTOS")
    print("="*50)
    
    # Simula tempo de carregamento dos dados
    print("⏳ Carregando eventos...")
    # time.sleep(1): Pausa por 1 segundo (demonstra operações que levam tempo)
    time.sleep(1)
    
    # Verifica se existem eventos
    if not eventos:
        print("📭 Nenhum evento cadastrado.\n")
        return
    
    # Ordena os eventos pela data_hora
    # Usa a função sorted() com uma função lambda para extrair a chave de ordenação
    # lambda: função anônima que retorna o valor a ser usado na ordenação
    eventos_ordenados = sorted(eventos, key=lambda e: e["data_hora"])
    
    # Obtém a data/hora atual para comparação
    agora = datetime.now()
    
    print("\n📋 Eventos cadastrados:\n")
    
    # Itera sobre os eventos ordenados
    for i, evento in enumerate(eventos_ordenados, 1):
        # Converte a string ISO de volta para um objeto datetime
        # datetime.fromisoformat() é o inverso de isoformat()
        data_hora_obj = datetime.fromisoformat(evento["data_hora"])
        
        # DESAFIO 2: Comparação de datas para identificar eventos passados/futuros
        if data_hora_obj < agora:
            # Evento já passou
            status = "[PASSADO]"
            emoji = "⏰"
        else:
            # Evento ainda não aconteceu
            status = "[FUTURO]"
            emoji = "🔮"
        
        # Formata a data/hora para exibição: DD/MM/AAAA às HH:MM
        data_formatada = data_hora_obj.strftime("%d/%m/%Y às %H:%M")
        
        # Exibe o evento com formatação clara
        print(f"{i}. {evento['nome']}")
        print(f"   {emoji} {data_formatada} {status}")
        print()


def visualizar_calendario():
    """
    Exibe o calendário de um mês específico.
    Args:
        None    
    Retorna:
        None
    """
    print("\n" + "="*50)
    print("VISUALIZAR CALENDÁRIO")
    print("="*50)
    
    try:
        # Solicita o ano
        ano = int(input("\n📅 Ano (ex: 2025): "))
        
        # Solicita o mês
        mes = int(input("📅 Mês (1-12): "))
        
        # Validação simples do mês
        if mes < 1 or mes > 12:
            print("❌ Mês deve estar entre 1 e 12.\n")
            return
        
        # Obtém o nome do mês em português (usando índices de uma lista)
        nomes_meses = [
            "", "Janeiro", "Fevereiro", "Março", "Abril", "Maio", "Junho",
            "Julho", "Agosto", "Setembro", "Outubro", "Novembro", "Dezembro"
        ]
        
        print(f"\n🗓️  Calendário de {nomes_meses[mes]} de {ano}\n")
        
        # calendar.month(ano, mes): Retorna a representação do calendário como string
        # Essa função é útil para exibir calendários de forma organizada
        calendario = calendar.month(ano, mes)
        print(calendario)
        
    except ValueError:
        print("❌ Entrada inválida! Use números inteiros para ano e mês.\n")


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
            
        elif opcao == "3":
            # Opção 3: Visualizar calendário
            visualizar_calendario()
            
        elif opcao == "4":
            # Opção 4: Sair do programa
            print("\n👋 Até logo! Programa encerrado.\n")
            break
            
        else:
            # Opção inválida
            print("❌ Opção inválida! Por favor, escolha 1, 2, 3 ou 4.\n")


# Ponto de entrada do programa
if __name__ == "__main__":
    """
    Este bloco é executado apenas quando o arquivo é executado diretamente,
    não quando é importado como módulo em outro arquivo.
    """
    menu_principal()