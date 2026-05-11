# INSTRUÇÕES:
# 1. Certifique-se de ter o Python instalado (versão 3.x).
# 2. Siga as instruções do menu para gerenciar seus Pokémon.

def obter_dados_pokemon(nome, tipo, nivel):
    
    # Função para formatar os dados de um Pokémon em uma string.
    return f"{nome} - {tipo} - {nivel}"

def obter_nivel_pokemon(entrada):

    # Função para obter e validar o nível do Pokémon.
    # Verifica se é um inteiro dentro do intervalo
    try:
        nivel = int(entrada)
        if 1 <= nivel <= 100:
            return nivel
        else:
            return "Erro: O nível deve estar entre 1 e 100."
    except ValueError:
        return "Erro: Entrada inválida. Por favor, digite um número inteiro."

def validar_pokemon_existe(nome, pokedex):

    # Função para verificar se um Pokémon existe
    if nome in pokedex:
        return True
    return False

def adicionar_pokemon(nome, tipo, nivel, pokedex):

    # Função para adicionar um novo Pokémon à Pokédex.
    if validar_pokemon_existe(nome, pokedex):
        return "Erro: Este Pokémon já está cadastrado."
    
    pokedex[nome] = {'tipo': tipo, 'nivel': nivel, 'capturado': 0}
    return f"Pokémon {nome} adicionado com sucesso!"

def listar_pokemon(pokedex):

    #Função para listar todos os Pokémon cadastrados na Pokédex em ordem alfabética.
    if not pokedex:
        return "A Pokédex está vazia."
    
    resultado = []
    # sorted(pokedex.items()) ordena as chaves (nomes) alfabeticamente
    for nome, dados in sorted(pokedex.items()):
        info = obter_dados_pokemon(nome, dados['tipo'], dados['nivel'])
        resultado.append(info)
    
    return "\n".join(resultado)

def remover_pokemon(nome, pokedex):

    # Função para remover um Pokémon da Pokédex.

    if not validar_pokemon_existe(nome, pokedex):
        return "Erro: Pokémon não encontrado."
    
    del pokedex[nome]
    return f"Pokémon {nome} removido com sucesso."

def atualizar_nivel_pokemon(nome, novo_nivel, pokedex):

    # Função para atualizar o nível de um Pokémon existente.

    if not validar_pokemon_existe(nome, pokedex):
        return "Erro: Pokémon não encontrado."
    
    pokedex[nome]['nivel'] = novo_nivel
    return f"Nível do Pokémon {nome} atualizado para {novo_nivel}."

def registrar_captura(nome, quantidade, pokedex, historico):

    # Função para registrar a captura de um ou mais Pokémon.

    if not validar_pokemon_existe(nome, pokedex):
        return "Erro: Pokémon não encontrado."
    
    if quantidade <= 0:
        return "Erro: A quantidade de capturas deve ser maior que zero."
    
    pokedex[nome]['capturado'] += quantidade
    historico.append((nome, quantidade))
    return f"Captura de {quantidade} {nome}(s) registrada com sucesso!"

def exibir_historico_capturas(historico):

    # Função para exibir o histórico de capturas de Pokémon.

    if not historico:
        return "Nenhuma captura registrada no histórico."
    
    return "\n".join([f"Pokémon: {nome} | Quantidade: {qtd}" for nome, qtd in historico])

def exibir_menu():

    # Função para exibir as opções do menu.

    return (
        "\n--- Menu Pokédex ---"
        "\n1. Adicionar Pokémon"
        "\n2. Listar Pokémon"
        "\n3. Remover Pokémon"
        "\n4. Atualizar Nível"
        "\n5. Registrar Captura"
        "\n6. Exibir Histórico de Capturas"
        "\n7. Sair"
    )

def main():

    # Função principal que gerencia o loop do programa.

    pokedex = {}
    historico_capturas = []

    while True:
        print(exibir_menu())
        opcao = input("Escolha uma opção: ")

        if opcao == '1':
            nome = input("Nome do Pokémon: ")
            tipo = input("Tipo do Pokémon: ")
            nivel_raw = input("Nível (1-100): ")
            nivel_validado = obter_nivel_pokemon(nivel_raw)
            
            if isinstance(nivel_validado, int):
                print(adicionar_pokemon(nome, tipo, nivel_validado, pokedex))
            else:
                print(nivel_validado)

        elif opcao == '2':
            print("\nPokémons cadastrados:")
            print(listar_pokemon(pokedex))

        elif opcao == '3':
            nome = input("Nome do Pokémon a remover: ")
            print(remover_pokemon(nome, pokedex))

        elif opcao == '4':
            nome = input("Nome do Pokémon: ")
            nivel_raw = input("Novo nível (1-100): ")
            nivel_validado = obter_nivel_pokemon(nivel_raw)
            
            if isinstance(nivel_validado, int):
                print(atualizar_nivel_pokemon(nome, nivel_validado, pokedex))
            else:
                print(nivel_validado)

        elif opcao == '5':
            nome = input("Nome do Pokémon capturado: ")
            try:
                capturas = int(input("Quantidade capturada: "))
                print(registrar_captura(nome, capturas, pokedex, historico_capturas))
            except ValueError:
                print("Erro: A quantidade deve ser um número inteiro.")

        elif opcao == '6':
            print("\nHistórico de Capturas:")
            print(exibir_historico_capturas(historico_capturas))

        elif opcao == '7':
            print("Encerrando o programa... Até logo, mestre Pokémon!")
            break

        else:
            print("Opção inválida! Tente novamente.")

if __name__ == "__main__":
    main()