investimento = float(input('qual é o valor do investimento? '))
meses = int(input('Por quantos meses? '))

imposto = 0.15
rendimentos = 0.01

for i in range(0, meses):
    lucroreal = 0
    valor_inicial = investimento ++ lucroreal
    investimento +=  investimento * rendimentos
    rendeu = investimento - valor_inicial
    descontoimposto = rendeu * imposto
    lucroreal = rendeu - descontoimposto
    saldo = investimento - descontoimposto
    investimento = investimento - descontoimposto
    print(f'Saldo mensal: R$ {investimento}')
    print("-"*50)