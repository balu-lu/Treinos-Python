def obter_numero(mensagem):
    while True:
        try:
            return float(input(mensagem))
        except ValueError:
            print(
                "Erro: Valor inválido! Por favor, insira um número válido (sem letras).")


def iniciar_calculadora():
    def soma(x, y): return x + y
    def subtracao(x, y): return x - y
    def multiplicacao(x, y): return x * y
    def divisao(x, y): return x / y

    nomes_operacoes = ["Soma", "Subtração", "Multiplicação", "Divisão"]
    operacoes = {'1': soma, '2': subtracao, '3': multiplicacao, '4': divisao}

    while True:
        print("\n" + "="*30)
        num1 = obter_numero("Insira o primeiro número: ")
        num2 = obter_numero("Insira o segundo número: ")

        print("\nEscolha uma operação:")

        menu = [f"{i+1} - {op}" for i, op in enumerate(nomes_operacoes)]
        print("\n".join(menu))

        escolha = input("Sua escolha: ").strip()

        if escolha not in ['1', '2', '3', '4']:
            print("Erro: Operação inválida! Tente novamente.")
            continue

        indice_op = int(escolha) - 1
        print(f"Você escolheu: {nomes_operacoes[indice_op]}")

        if escolha == '4':
            while num2 == 0:
                print("Divisão por zero não é permitida.")
                num2 = obter_numero("Por favor, insira outro número: ")

        operacao = operacoes[escolha]
        resultado = operacao(num1, num2)

        if resultado.is_integer():
            print(f"O resultado é: {int(resultado)}")
        else:
            print(f"O resultado é: {resultado}")

        continuar = input(
            "\nDeseja realizar outra operação? (S/N): ").strip().upper()
        if continuar != 'S':
            print("Encerrando a calculadora. Até logo!")
            break


if __name__ == "__main__":
    iniciar_calculadora()
