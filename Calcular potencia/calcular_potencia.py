

# Solicita ao usuário a base e o expoente
base = int(input("Insira a base: "))
expoente = int(input("Insira o expoente: "))

# Inicializa o resultado como 1, uma vez que qualquer número elevado a 0 é igual a 1
resultado = 1

# Loop para calcular a potência da base pelo expoente
for i in range(expoente):
    # Multiplica o resultado atual pela base em cada iteração
    resultado = resultado * base

# Exibe o resultado da potenciação
print("Resultado:", resultado)