import os
import json
# Importa o 'datetime' para registrar a data e hora exatas da conclusão
from datetime import datetime, timedelta


# --- Variáveis Globais ---
# Variável para controlar o ID único de cada tarefa
tarefa_id = 1
# Lista onde todas as tarefas (dicionários) serão armazenadas
lista_de_tarefas = []
tarefas_arquivadas = []
# Listas de opções fixas para validação
lista_de_prioridades = ["Urgente","Alta","Media","Baixa"]
origens = ["E-mail", "Telefone", "Chamado do Sistema"]
# Lista com todos os status possíveis
status_disponiveis = ["Pendente", "Fazendo", "Concluida", "Arquivada", "Excluida"]

def verificar_arquivos(nome_arquivo):
    """
    Função responsável por verificar se os arquivos JSON existem, caso não, serão criados novos arquivos

    Parâmetros: nenhum
    Retorno: Nenhum 
    """

    # Tenta abrir os arquivos, conforme parametro passado no "main"
    if not os.path.exists(nome_arquivo):
        print(f"Arquivo '{nome_arquivo}' não encontrado. Criando novo...")
        try:
            with open(nome_arquivo, "w", encoding="utf-8") as arquivo:
                json.dump([], arquivo, indent=4, ensure_ascii=False)
        except IOError as erro:
            print("Erro ao criar o novo arquivo", erro)
      
def carregar_dados(nome_arquivo):
    """
    Função responsável por carregar os dados dos arquivos JSON para persistência de dados.

    Parâmetros: nome do arquivo (tarefas.json, por exemplo)
    Retorno: Nenhum 
    """
    try:
        with open(nome_arquivo, "r", encoding="utf-8") as arquivo:
            return json.load(arquivo)
    except (FileNotFoundError, json.JSONDecodeError) as erro:
        print("Ocorreu um erro ao carregar os dados", erro)
        return []  # Se o arquivo não existe ou está corrompido

def salvar_dados(nome_arquivo, lista_dados):
    """
    Função responsável por salvar as tarefas nos arquivos JSON

    Parâmetros: nome do arquivo (tarefas.json, por exemplo) e a lista das tarefas (arquivadas ou não)
    Retorno: Nenhum 
    """
    try:
        with open(nome_arquivo, "w", encoding="utf-8") as arquivo:
            json.dump(lista_dados, arquivo, indent=4, ensure_ascii=False, default=str)
    except IOError as erro:
        print("Ocorreu um erro ao salvar os dados", erro)

def limpar_tela():
  """
    Função simples para pausar e limpar o terminal (funciona em Windows 'cls' e Linux/Mac 'clear').

    Parâmetros: Nenhum
    Retorno: Nenhum 
  """
  continuar = input("Aperte Enter para continuar...")
  if os.name == 'nt':
    os.system('cls')
  else:
    os.system('clear')

def menu():
  """
    Função principal que exibe o menu e gerencia a navegação do usuário.

    Parâmetros: Nenhum
    Retorno: Nenhum 
  """
  print("Executando menu...")
  while (True):
    opcao_menu = input("Digite a opção desejada:\n[1] Criar Tarefa\n[2] Verificar Tarefa\n[3] Atualizar Tarefa\n[4] Concluir Tarefa\n[5] Excluir Tarefa\n[6] Arquivar Tarefas\n[7] Relatórios\n[8] Sair\n")
    match opcao_menu:
      case "1":
        tarefa_nova = criar_tarefa(lista_de_prioridades)
        lista_de_tarefas.append(tarefa_nova)
        limpar_tela()
        
      case "2":
        verificar_urgencia(lista_de_tarefas, lista_de_prioridades, status_disponiveis)
        limpar_tela()

      case "3":
        atualizar_prioridade(lista_de_tarefas, lista_de_prioridades)
        limpar_tela()

      case "4":
        concluir_tarefa(lista_de_tarefas, status_disponiveis)
        limpar_tela()

      case "5":
        excluir_tarefa(lista_de_tarefas, status_disponiveis)
        limpar_tela()

      case "6":
        arquivar_tarefas(lista_de_tarefas, status_disponiveis)
        limpar_tela()

      case "7":
        opcao = input("Digite a opção desejada:\n[1] Relatório de tarefas ativas\n[2] Relatório de tarefas arquivadas\n")
        if opcao == "1":
            exibir_relatorio(lista_de_tarefas, status_disponiveis)
            limpar_tela()
        elif opcao == "2":
            exibir_relatorio_arquivados(tarefas_arquivadas, status_disponiveis)
            limpar_tela()
        else:
            print("Digite uma opção válida.")  

      case "8":
        print("Saindo do sistema...")
        salvar_dados("tarefas.json", lista_de_tarefas)
        salvar_dados("tarefas_arquivadas.json", tarefas_arquivadas)
        break

      case _:
        print("Digite uma opção válida (de 1 a 6).")
        limpar_tela()

def criar_tarefa(prioridades):
    """
    Função para criar uma nova tarefa (dicionário) e adicioná-la à lista.
    Valida as entradas numéricas do usuário.

    Parâmetros: lista que contém as prioridades
    Retorno: Nova tarefa que será colocada na lista global
    """
    print("Executando função de criação de tarefas...")
    
    # Declarando a váriavel global
    global tarefa_id 
    
    # Cria o dicionário da nova tarefa, já com status "Pendente"
    nova_tarefa = {"Status": status_disponiveis[0]}
    
    titulo_atualizado = str(input("Adicione um título: "))
    nova_tarefa["Titulo"] = titulo_atualizado.lower()
    nova_tarefa["ID"] = tarefa_id
    nova_tarefa["Data de Criação"] = datetime.now()
    descricao = str(input("Digite a descrição da tarefa: "))
    nova_tarefa["Descricao"] = descricao.lower()
    
    # --- Validação da Prioridade ---
    # Loop 'while True' para garantir que o usuário digite uma opção válida
    while True:
        try:
            prioridade_atualizada = int(input("Qual a prioridade?\n[1] Urgente\n[2] Alta\n[3] Média\n[4] Baixa\n"))
            # Verifica se o número está dentro do intervalo válido (1 a 4)
            if 1 <= prioridade_atualizada <= 4:
                nova_tarefa["Prioridade"] = prioridades[prioridade_atualizada - 1]
                break # Se for válido, sai do loop
            else:
                print("Opção inválida. Digite um número de 1 a 4.")
        except ValueError:
           print("Entrada inválida. Digite um valor numérico.")
  
    # Outro loop para validar a origem
    while True:
        try:
            origem_atualizado = int(input("Qual a origem?\n[1] E-mail\n[2] Telefone\n[3] Chamado do Sistema\n"))
            # Verifica se o número está dentro do intervalo válido (1 a 3)
            if 1 <= origem_atualizado <= 3:
                nova_tarefa["Origem"] = origens[origem_atualizado - 1]
                break # Se for válido, sai do loop
            else:
                print("Opção Inválida. Digite um número de 1 a 3.")
        except ValueError:
           print("Entrada inválida. Digite um valor numérico.")

    # Incrementa o ID global para a próxima tarefa
    tarefa_id += 1
    
    print(f"\nTarefa '{nova_tarefa['Titulo']}' (ID: {nova_tarefa['ID']}) criada com sucesso!")
    return nova_tarefa

def verificar_urgencia(tarefas, prioridades, status):
    """
    Verifica a próxima tarefa prioritária 'Pendente' e a muda para 'Fazendo'.
    Garante que apenas uma tarefa esteja 'Fazendo' por vez.

    Parâmetros: lista das tarefas, lista das prioridades e lista dos status disponíveis
    Retorno: Nenhum 
    """
    print("Executando função de verificar prioridade...")

    # Requisito: Verifica se alguma tarefa JÁ ESTÁ "Fazendo"
    for tarefa in tarefas:
        if tarefa["Status"] == status[1]:
            print(f"Erro: A tarefa '{tarefa['Titulo']}' (ID: {tarefa['ID']}) já está em execução.")
            return # Sai da função imediatamente

    # 2. Se nenhuma estiver "Fazendo", procura a próxima prioritária
    for prioridade in prioridades:
        for tarefa in tarefas:
            # Procura uma tarefa que tenha a prioridade da vez E esteja "Pendente"
            if tarefa["Prioridade"] == prioridade and tarefa["Status"] == status[0]:
                tarefa["Status"] = status[1] # Muda o status para "Fazendo"
                print(f"Próxima tarefa a ser feita: {tarefa['Titulo']} (ID: {tarefa['ID']})")
                return # Para a função assim que encontra a primeira

    print("Não há tarefas pendentes a serem feitas.")

def atualizar_prioridade(tarefas, prioridades):
    """
    Função para encontrar uma tarefa pelo ID e alterar sua prioridade.
    Valida a nova prioridade inserida.

    Parâmetros: lista das tarefas e lista de prioridades
    Retorno: Nenhum 
    """
    print("Executando função de atualizar prioridade...")
    
    try:
        tarefa_procurada = int(input("Digite o ID da tarefa para editar sua prioridade: "))
    except ValueError:
       print("ID inválido. Digite um valor numérico.")
       return # Sai da função se o ID for inválido

    tarefa_encontrada = False
    for tarefa in tarefas:
        if tarefa["ID"] == tarefa_procurada:
            tarefa_encontrada = True
            print(f"Tarefa encontrada: {tarefa['Titulo']} (Prioridade atual: {tarefa['Prioridade']})")

            # --- Validação da Nova Prioridade ---
            while True:
                try:
                    prioridade_atualizada = int(input("Qual a nova prioridade?\n[1] Urgente\n[2] Alta\n[3] Média\n[4] Baixa\n"))
                    # Validação de intervalo (range) para evitar IndexError
                    if 1 <= prioridade_atualizada <= len(prioridades):
                        tarefa["Prioridade"] = prioridades[prioridade_atualizada - 1]
                        print(f"Tarefa {tarefa['Titulo']} teve sua prioridade atualizada com sucesso")
                        break # Sai do loop de prioridade
                    else:
                        print("Opção inválida. Digite um número de 1 a 4.")
                except ValueError:
                   print("Entrada inválida. Digite um valor numérico.")
            
            break

    if tarefa_encontrada == False:
        print(f"Tarefa com ID {tarefa_procurada} não encontrada.")
    
def concluir_tarefa(tarefas, status):
    """
    Função para concluir uma tarefa. Só pode concluir tarefas que estão 'Fazendo'.
    Registra a data/hora exata da conclusão.

    Parâmetros: lista das tarefas e lista de status
    Retorno: Nenhum 
    """
    print("Executando função de concluir tarefas...")
    
    try:
        tarefa_procurada = int(input("Digite o ID da tarefa para concluir: "))
    except ValueError:
       print("ID inválido. Digite um valor numérico.")
       return

    tarefa_encontrada = False
    for tarefa in tarefas:
        # Encontra a tarefa pelo ID
        if tarefa["ID"] == tarefa_procurada:
            tarefa_encontrada = True
            
            # Verifica o status da tarefa ENCONTRADA
            if tarefa["Status"] == status[1]:
                
                # Requisito: Salva a data/hora ATUAL
                tarefa["Data de Conclusão"] = datetime.now() 
                tarefa["Status"] = status[2]
                
                # Formata a data para um formato mais visivel
                data_formatada = tarefa["Data de Conclusão"].strftime("%d/%m/%Y às %H:%M")
                print(f"Tarefa {tarefa['Titulo']} concluida com sucesso em {data_formatada}!")

            elif tarefa["Status"] == status[2]:
                print(f"Erro: A tarefa '{tarefa['Titulo']}' (ID: {tarefa['ID']}) já está concluída.")
            
            else: # Se o status for "Pendente"
                print(f"Erro: A tarefa '{tarefa['Titulo']}' (ID: {tarefa['ID']}) precisa ser iniciada (estar 'Fazendo') antes de ser concluída.")

            break

    # Esta verificação acontece após o loop terminar
    if tarefa_encontrada == False:
        print(f"Tarefa com ID {tarefa_procurada} não encontrada.")

def excluir_tarefa(tarefas, status):
    """
    Função cuja finalidade é excluir as tarefas
    As tarefas excluidas tem seu status alterado para 'Excluida' e são colocadas nas tarefas arquivadas

    Parâmetros: lista das tarefas e lista de status
    Retorno: Nenhum 
    """

    print("Executando função de excluir tarefa.")

    try:
        id_procurado = int(input("Digite o ID da tarefa desejada: "))
    except ValueError:
        print("Digite um número válido.")
        return

    encontrou = False # Flag de controle
    for tarefa in tarefas:
        if tarefa["ID"] == id_procurado:
            tarefa["Status"] = status[4]
            global tarefas_arquivadas
            tarefas_arquivadas.append(tarefa)
            print(f"Tarefa {id_procurado} excluída com sucesso.")
            encontrou = True
            break # Para de procurar assim que acha

    if not encontrou: # Só printa isso SE rodou tudo e não achou
        print("Tarefa não encontrada.")

def arquivar_tarefas(tarefas, status):
    """
    Função que arquiva tarefas concluidas a mais de uma semana desde sua criação

    Parâmetros: lista das tarefas e lista de status
    Retorno: Nenhum 
    """

    print("Executando função de arquivar tarefas")

    semana_concluida = timedelta(weeks=1)
    data_atual = datetime.now()
    for tarefa in tarefas:
        if tarefa["Status"] == status[2]:
        # Verifica se existe a data e se ela é uma STRING (pois veio do JSON)
            if "Data de Conclusão" in tarefa and isinstance(tarefa["Data de Conclusão"], str):
                # Converte de texto para datetime para fazer a conta
                data_conclusao = datetime.fromisoformat(tarefa["Data de Conclusão"])
            
            # Se a tarefa acabou de ser criada na memória e ainda é datetime
            elif "Data de Conclusão" in tarefa:
                data_conclusao = tarefa["Data de Conclusão"]
            else:
                continue # Se não tem data, pula

            # Agora faz a conta com a variável convertida
            if (data_atual - data_conclusao) > semana_concluida:
                tarefa["Status"] = status[3]
                global tarefas_arquivadas
                tarefas_arquivadas.append(tarefa)

def exibir_relatorio(tarefas, status):
    """
    Função para exibir um relatório formatado de todas as tarefas na lista.

    Parâmetros: lista das tarefas e lista de status
    Retorno: Nenhum 
    """
    print("Executando função de exibir relatório...")

    if not tarefas:
        print("\nNenhuma tarefa cadastrada na lista.")
        return

    print("\n--- Relatório de Tarefas ---")
    for tarefa in tarefas:
        if tarefa["Status"] not in [status[3], status[4]]:
            #Se a chave não existir, ele retorna 'N/A'
            print(f"ID: {tarefa.get('ID', 'N/A')}")
            print(f"  Título: {tarefa.get('Titulo', 'N/A')}")
            print(f"  Status: {tarefa.get('Status', 'N/A')}")
            print(f"  Prioridade: {tarefa.get('Prioridade', 'N/A')}")
        
            # Só exibe a data de conclusão se a tarefa tiver essa informação
            if "Data de Conclusão" in tarefa:
                data_conclusao = tarefa["Data de Conclusão"]
                data_criacao = tarefa["Data de Criação"]

                # Tratamento para garantir que ambos sejam datetime (por causa do JSON)
                if isinstance(data_conclusao, str):
                    data_conclusao = datetime.fromisoformat(data_conclusao)
                if isinstance(data_criacao, str):
                    data_criacao = datetime.fromisoformat(data_criacao)

                print(f"  Concluída em: {data_conclusao.strftime('%d/%m/%Y às %H:%M')}")
                
                # CÁLCULO DO TEMPO (O que faltava)
                tempo_execucao = data_conclusao - data_criacao
                # Remove os milissegundos para ficar bonito
                tempo_limpo = str(tempo_execucao).split('.')[0] 
                print(f"  Tempo de execução: {tempo_limpo}")
            
            print("-" * 25) # Separador

def exibir_relatorio_arquivados(tarefas_arquivadas, status):
    """
    Função utilizada para exibir um relatório com as tarefas arquivadas e suas informações

    Parâmetros: lista das tarefas arquivadas e lista de status
    Retorno: Nenhum 
    """

    print("Executando função de exibir relatório das tarefas arquivadas...")
    # Condicional para ver se existem tarefas arquivadas na lista
    if not tarefas_arquivadas:
        print("Nenhuma tarefa arquivada encontrada.")
        return

    print("\n--- Relatório de Tarefas Arquivadas ---")
    for tarefa in tarefas_arquivadas:
        if tarefa["Status"] != status[4]:       
            print(f"ID: {tarefa.get('ID', 'N/A')}")
            print(f"  Título: {tarefa.get('Titulo', 'N/A')}")
            print(f"  Status: {tarefa.get('Status', 'N/A')}")
            print(f"  Prioridade: {tarefa.get('Prioridade', 'N/A')}")

        print("-" * 25)

# Bloco que executa o programa (chama o menu)
if __name__ == "__main__":
    print("Verificando a integridade dos arquivos...")
    verificar_arquivos("tarefas.json")
    verificar_arquivos("tarefas_arquivadas.json")
    lista_de_tarefas = carregar_dados("tarefas.json")
    tarefas_arquivadas = carregar_dados("tarefas_arquivadas.json")

    maior_id = 0

    if lista_de_tarefas:
        for tarefa in lista_de_tarefas:
            if tarefa["ID"] > maior_id:
                maior_id = tarefa["ID"]

    tarefa_id = maior_id + 1
    menu()
