
# Solicita valor do investimento inicial
investimento = float(input("Qual o valor do investimento? "))
# Solicita ao usuário o número de meses a serem investidos e o valor do investimento inicial
meses = int(input("Quantos meses será investido? "))
rendimento = 0.01  # Taxa de rendimento mensal de 1%
imposto = 0.15     # Taxa de imposto sobre os rendimentos apenas de 15%
valorinvestido = investimento  # Salva o valor inicial do investimento

print(f"\n", valorinvestido)

# Loop que simula o investimento ao longo dos meses
for i in range(0, meses):
    print('\n-----------------------------------')
    # Salva o valor inicial do investimento no início do mês
    valor_inicial = investimento  
    # Calcula o novo saldo após o rendimento mensal
    investimento += investimento * rendimento  
    print(f"SaldoMensal: {investimento}")
    # Calcula o lucro mensal
    lucro_mes = (investimento - valor_inicial)  

# Calcula o lucro total ao final do período de investimento
lucrototal = investimento - valorinvestido
print(f"Lucro total {lucrototal}")

# Calcula o desconto de imposto sobre o lucro total
descontoImposto = lucrototal * imposto
print(f"Desconto de imposto: {descontoImposto}")

# Calcula o saldo final após o desconto de imposto
saldoFinal = investimento - descontoImposto
print(f"Saldo final: {saldoFinal}")