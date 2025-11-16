import os
# Importa o 'datetime' para podermos registrar a data e hora exatas da conclusão
from datetime import datetime
 
print()
print("- - - - - - - - - - - - - - - - - - - - -")
print("- - - Bloco de Codigo: Tarefas   - - -")
print("- - - - - - - - - - - - - - - - - - - - -")
 
# --- Variáveis Globais ---
# Variável para controlar o ID único de cada tarefa
tarefa_id = 1
# Lista onde todas as tarefas (dicionários) serão armazenadas
lista_de_tarefas = []
# Listas de opções fixas para validação
lista_de_prioridades = ["Urgente","Alta","Media","Baixa"]
origens = ["E-mail", "Telefone", "Chamado do Sistema"]
# Lista com todos os status possíveis (adicionado "Pendente")
status_disponiveis = ["Fazendo", "Concluida", "Pendente"]
 
def limpar_tela():
  """
  Função simples para pausar e limpar o terminal (funciona em Windows 'cls' e Linux/Mac 'clear').
  """
  continuar = input("Aperte Enter para continuar...")
  if os.name == 'nt':
    os.system('cls')
  else:
    os.system('clear')
 
 
def menu():
  """
  Função principal que exibe o menu e gerencia a navegação do usuário.
  """
  print("Executando menu...")
  while (True):
    # O menu permanece o mesmo que você criou
    opcao_menu = input("Digite a opção desejada:\n[1] Criar Tarefa\n[2] Verificar Tarefa\n[3] Atualizar Tarefa\n[4] Concluir Tarefa\n[5] Relatório\n[6] Sair\n")
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
        exibir_relatorio(lista_de_tarefas)
        limpar_tela()
 
      case "6":
        print("Saindo do sistema...")
        break
 
      case _:
        print("Digite uma opção válida (de 1 a 6).")
        limpar_tela()
 
 
def criar_tarefa(prioridades):
    """
    Função para criar uma nova tarefa (dicionário) e adicioná-la à lista.
    Valida as entradas numéricas do usuário.
    """
    print("Executando função de criação de tarefas...")
    
    # É uma boa prática declarar o uso do 'global' no início da função
    global tarefa_id 
    
    # Cria o dicionário da nova tarefa, já com status "Pendente"
    nova_tarefa = {"Status": status_disponiveis[2]} # status_disponiveis[2] é "Pendente"
    
    titulo_atualizado = str(input("Adicione um título: "))
    nova_tarefa["Titulo"] = titulo_atualizado.lower()
    nova_tarefa["ID"] = tarefa_id
    
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
  
    # Outro loop 'while True' para validar a origem
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
    """
    print("Executando função de verificar prioridade...")
 
    # Requisito: Verifica se alguma tarefa JÁ ESTÁ "Fazendo"
    for tarefa in tarefas:
        if tarefa["Status"] == status[0]: # status[0] é "Fazendo"
            print(f"Erro: A tarefa '{tarefa['Titulo']}' (ID: {tarefa['ID']}) já está em execução.")
            return # Sai da função imediatamente
 
    # 2. Se nenhuma estiver "Fazendo", procura a próxima prioritária
    for prioridade in prioridades:
        for tarefa in tarefas:
            # Procura uma tarefa que tenha a prioridade da vez E esteja "Pendente"
            if tarefa["Prioridade"] == prioridade and tarefa["Status"] == status[2]: # status[2] é "Pendente"
                tarefa["Status"] = status[0] # Muda o status para "Fazendo"
                print(f"Próxima tarefa a ser feita: {tarefa["Titulo"]} (ID: {tarefa['ID']})")
                return # Para a função assim que encontra a primeira
 
    print("Não há tarefas pendentes a serem feitas.")
 
 
def atualizar_prioridade(tarefas, prioridades):
    """
    Função para encontrar uma tarefa pelo ID e alterar sua prioridade.
    Valida a nova prioridade inserida.
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
            if tarefa["Status"] == status[0]: # status[0] é "Fazendo"
                
                # Requisito: Salva a data/hora ATUAL
                tarefa["Data de Conclusão"] = datetime.now() 
                tarefa["Status"] = status[1] # status[1] é "Concluida"
                
                # Formata a data para um formato mais visivel
                data_formatada = tarefa["Data de Conclusão"].strftime("%d/%m/%Y às %H:%M")
                print(f"Tarefa {tarefa['Titulo']} concluida com sucesso na data {data_formatada}!")
 
            elif tarefa["Status"] == status[1]: # status[1] é "Concluida"
                print(f"Erro: A tarefa '{tarefa['Titulo']}' (ID: {tarefa['ID']}) já está concluída.")
            
            else: # Se o status for "Pendente"
                print(f"Erro: A tarefa '{tarefa['Titulo']}' (ID: {tarefa['ID']}) precisa ser iniciada (estar 'Fazendo') antes de ser concluída.")
 
            break
 
    # Esta verificação acontece após o loop terminar
    if tarefa_encontrada == False:
        print(f"Tarefa com ID {tarefa_procurada} não encontrada.")
 
def exibir_relatorio(tarefas):
    """
    Função para exibir um relatório formatado de todas as tarefas na lista.
    """
    print("Executando função de exibir relatório...")
 
    if not tarefas:
        print("\nNenhuma tarefa cadastrada na lista.")
        return
 
    print("\n--- Relatório de Tarefas ---")
    for tarefa in tarefas:
        #Se a chave não existir, ele retorna 'N/A'
        print(f"ID: {tarefa.get('ID', 'N/A')}")
        print(f"  Título: {tarefa.get('Titulo', 'N/A')}")
        print(f"  Status: {tarefa.get('Status', 'N/A')}")
        print(f"  Prioridade: {tarefa.get('Prioridade', 'N/A')}")
        
        # Só exibe a data de conclusão se a tarefa tiver essa informação
        if "Data de Conclusão" in tarefa:
            data = tarefa["Data de Conclusão"]
            # Verifica se a data é um objeto datetime
            if isinstance(data, datetime):
                print(f"  Concluída em: {data.strftime('%d/%m/%Y às %H:%M')}")
            else:
                print(f"  Concluída em: {data}") # Mostra a data antiga em string, se houver
        
        print("-" * 25) # Separador
 
# Bloco que executa o programa (chama o menu)
if __name__ == "__main__":
  menu()
