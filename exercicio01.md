## 📝 Projeto Prático de Fundamentos de Python: Gerenciador de Eventos e Agendamento Simples

Olá, alunos! Este projeto "mão na massa" tem como objetivo consolidar os conhecimentos essenciais de Python, focando na manipulação de **datas, horários e gerenciamento de arquivos**. Ao final, teremos um sistema funcional de agendamento que resolve um problema prático do dia a dia.

---

### 🎯 O Desafio: Construindo um Gerenciador de Eventos

Iremos construir um programa capaz de **registrar, salvar e visualizar eventos** (reuniões, prazos, etc.) de forma organizada.

#### Módulos Centrais (Fundamentos Obrigatórios)

O sucesso deste projeto depende do uso correto e didático dos seguintes módulos da biblioteca padrão do Python.

| Módulo | Finalidade no Projeto | Conceito Principal |
| :--- | :--- | :--- |
| **`datetime`** | Manipulação e formatação de datas e horas exatas. | Criar objetos `datetime`, usar `strptime()` para converter *string* em objeto e `strftime()` para formatar a saída. |
| **`os`** | Interação com o sistema operacional (arquivos e diretórios). | Criar a pasta de dados (`dados/`) e definir o caminho do arquivo de persistência. |
| **`calendar`** | Visualização de datas em formato de calendário. | Exibir o calendário mensal completo para ajudar o usuário a escolher a data do evento. |
| **`time`** | Introdução ao controle de fluxo temporal. | Usar `time.sleep()` para simular um "carregamento" ou "salvamento" de dados, melhorando a experiência de usuário. |
| **`json`** | Persistência de dados. | Salvar e carregar a lista de eventos (que será uma lista de dicionários) em um arquivo (`eventos.json`). |

---

### 🛠️ Estrutura do Código e Funcionalidades

O projeto será dividido em funções lógicas para reforçar a modularidade do Python:

1.  **`configurar_ambiente()`**:
    * **Uso do `os`:** Garante que o diretório `dados/` exista no sistema para armazenar nossos eventos.
2.  **`adicionar_evento()`**:
    * Coleta o nome, a data e a hora do evento.
    * **Uso do `datetime`:** Combina os *inputs* e os converte em um objeto `datetime` para registro.
    * Salva o evento na lista principal e chama a função de salvamento.
3.  **`visualizar_calendario()`**:
    * **Uso do `calendar`:** Pede o ano e o mês, e exibe o calendário correspondente no terminal.
4.  **`listar_eventos()`**:
    * Carrega os dados do arquivo.
    * **Uso do `time`:** Inclui uma pausa de carregamento.
    * **Uso do `datetime`:** Formata as datas dos eventos para uma exibição amigável ao usuário.
5.  **`menu_principal()`**:
    * O *loop* infinito (`while True`) que controla a execução do programa e a navegação entre as funções.

---

### ⭐ Desafios Extras (Para aprimorar o aprendizado)

Estes desafios elevam a complexidade e a robustez do projeto, aplicando fundamentos essenciais de manipulação de erros e lógica de comparação.

#### Desafio 1: Validação de Entrada Robusta (Módulo `datetime`)
* **Problema:** Se o usuário digitar uma data ou hora em formato incorreto (ex: "32/12/2025"), o programa irá falhar.
* **Implementação:** Implementar um bloco **`try...except`** ao receber a data e hora do usuário na função `adicionar_evento()`. O bloco deve usar `datetime.strptime()` para tentar converter a *string*. Se ocorrer um erro (`ValueError`), o programa deve notificar o usuário e pedir a entrada novamente, garantindo que o código não "quebre".

#### Desafio 2: Classificação Temporal de Eventos (Módulo `datetime`)
* **Problema:** O usuário precisa saber rapidamente se um evento está no futuro ou já aconteceu.
* **Implementação:** Na função `listar_eventos()`, use **`datetime.now()`** para obter a data e hora atuais. Para cada evento listado, compare sua data registrada com a data atual.
    * Se a data do evento for **menor** que `datetime.now()`, exiba `[PASSADO]`.
    * Se a data do evento for **maior ou igual**, exiba `[FUTURO]`.