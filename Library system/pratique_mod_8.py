def gerenciar_biblioteca():
    # Dicionário para armazenar os livros
    livros = {}
    # Lista para armazenar o histórico de empréstimos
    historico_emprestimos = []

    while True:
        print("\n" + "="*30)
        print("Menu da Biblioteca")
        print("="*30)
        print("1. Adicionar livro")
        print("2. Listar livros")
        print("3. Remover livro")
        print("4. Atualizar quantidade de livros")
        print("5. Registrar empréstimo")
        print("6. Exibir histórico de empréstimos")
        print("7. Sair")

        opcao = input("\nEscolha uma opção (1-7): ").strip()

        if opcao == '1':
            titulo = input("Digite o título do livro: ").strip()
            autor = input("Digite o nome do autor: ").strip()
            try:
                quantidade = int(input("Digite a quantidade de exemplares: "))
                if quantidade < 0:
                    print("Erro: A quantidade não pode ser negativa.")
                else:
                    # Armazena o livro no dicionário com a estrutura solicitada
                    livros[titulo] = {"autor": autor, "quantidade": quantidade}
                    print(f"Sucesso: Livro '{titulo}' adicionado!")
            except ValueError:
                print(
                    "Erro: Por favor, digite um número inteiro válido para a quantidade.")

        elif opcao == '2':
            if not livros:
                print("A biblioteca está vazia no momento.")
            else:
                print("\n--- Lista de Livros Cadastrados ---")
                # Ordena os livros alfabeticamente pelo título (chaves do dicionário)
                for titulo in sorted(livros.keys()):
                    dados = livros[titulo]
                    print(
                        f"{titulo} - {dados['autor']} - {dados['quantidade']} disponíveis")

        elif opcao == '3':
            titulo = input("Digite o título do livro a ser removido: ").strip()
            if titulo in livros:
                del livros[titulo]
                print(f"Sucesso: O livro '{titulo}' foi removido.")
            else:
                print(
                    f"Erro: O livro '{titulo}' não foi encontrado no sistema.")

        elif opcao == '4':
            titulo = input(
                "Digite o título do livro para atualizar a quantidade: ").strip()
            if titulo in livros:
                try:
                    nova_quantidade = int(
                        input("Digite a nova quantidade de exemplares: "))
                    if nova_quantidade < 0:
                        print("Erro: A quantidade não pode ser negativa.")
                    else:
                        livros[titulo]["quantidade"] = nova_quantidade
                        print(
                            f"Sucesso: Quantidade do livro '{titulo}' atualizada para {nova_quantidade}.")
                except ValueError:
                    print("Erro: Por favor, digite um número inteiro válido.")
            else:
                print(
                    f"Erro: O livro '{titulo}' não foi encontrado no sistema.")

        elif opcao == '5':
            titulo = input(
                "Digite o título do livro para empréstimo: ").strip()
            if titulo in livros:
                try:
                    qtd_emprestada = int(
                        input("Digite a quantidade a ser emprestada: "))

                    if qtd_emprestada <= 0:
                        print("Erro: A quantidade deve ser maior que zero.")
                    elif livros[titulo]["quantidade"] >= qtd_emprestada:
                        # Atualiza a quantidade no dicionário de livros
                        livros[titulo]["quantidade"] -= qtd_emprestada
                        # Adiciona o registro no formato de dicionário dentro da lista de histórico
                        historico_emprestimos.append(
                            {"titulo": titulo, "quantidade": qtd_emprestada})
                        print(
                            f"Sucesso: Empréstimo de {qtd_emprestada} exemplar(es) de '{titulo}' registrado!")
                    else:
                        print(
                            "Erro: Não há exemplares suficientes disponíveis para esse empréstimo.")
                except ValueError:
                    print("Erro: Por favor, digite um número inteiro válido.")
            else:
                print(
                    f"Erro: O livro '{titulo}' não foi encontrado no sistema.")

        elif opcao == '6':
            if not historico_emprestimos:
                print("Nenhum empréstimo registrado até o momento.")
            else:
                print("\n--- Histórico de Empréstimos ---")
                for registro in historico_emprestimos:
                    print(
                        f"Livro: {registro['titulo']} | Quantidade emprestada: {registro['quantidade']}")

        elif opcao == '7':
            print("Encerrando o programa... Até logo!")
            break

        else:
            print("Erro: Opção inválida. Por favor, escolha um número de 1 a 7.")


# Executa o programa principal
if __name__ == "__main__":
    gerenciar_biblioteca()
