
# Calculo do primeiro dígito do CPF
#     CPF: 746.824.890-70
#     Colete a soma dos 9 primeiros dígitos do CPF
#     multiplicando cada um dos valores por uma
#     contagem regressiva começando de 10

#     Ex.:  746.824.890-70 (746824890)
#                         10  9  8  7  6  5  4  3  2
#                       *  7  4  6  8  2  4  8  9  0
#     Resultado da conta: 70  36 48 56 12 20 32 27 0

#     Somar todos os resultados: 
#     70+36+48+56+12+20+32+27+0 = 301
#     Multiplicar o resultado anterior por 10
#     301 * 10 = 3010
#     Obter o resto da divisão da conta anterior por 11
#     3010 % 11 = 7
#     Se o resultado anterior for maior que 9:
#         resultado é 0
#     contrário disso:
#         resultado é o valor da conta

#     O primeiro dígito do CPF é 7


# Solicitar ao usuário que digite o CPF
while True:
    print('='*50)
    try:
        cpf_input = input("Digite o CPF [apenas números]: ")
        # Verifica se a entrada contém apenas números
        if not cpf_input.isdigit():
            raise ValueError('Digite apenas números.')
        # cria uma tupla com os numeros digitados
        informado = tuple(map(str, cpf_input))     
        # Verifica se o CPF tem 11 dígitos
        if len(informado) != 11:
            raise ValueError('informe os 11 dígitos.')
        print('='*50)  
        break
    except ValueError:
        print('Erro desconhecido')

#armazenando o CPF digitado para validar ao final do código
cpf_informado = ''.join(informado) # o delimitador é chamado antes
cpf_digitado_armazenado = f'{cpf_informado[:9]}-{cpf_informado[9:]}'
print(f'CPF informado: {cpf_digitado_armazenado}')
print('='*50)

# variavel irá armazenar somente os 9 primeiros dígitos para o calculo                 python cpf.py
nove_digitos = informado[:9]                 #      74682489070

# Calculo do primeiro dígito
resultado = 0
numero_regressivo1 = 10
for i in nove_digitos:
    resultado += int(i) * numero_regressivo1
    numero_regressivo1 -= 1

primeiro_digito = (resultado * 10) % 11 if (resultado * 10) % 11 <= 9 else 0
# print(f"Validando o primeiro dígito:... ' * '") # {primeiro_digito}')

#############################################################################################################

# Calculo do segundo dígito do CPF
# CPF: 746.824.890-70
# Colete a soma dos 9 primeiros dígitos do CPF,
# MAIS O PRIMEIRO DIGITO,
# multiplicando cada um dos valores por uma
# contagem regressiva começando de 11

# Ex.:  746.824.890-70 (7468248907)
#    11 10  9  8  7  6  5  4  3  2
# *  7   4  6  8  2  4  8  9  0  7 <-- PRIMEIRO DIGITO
#    77 40 54 64 14 24 40 36  0 14

# Somar todos os resultados:
# 77+40+54+64+14+24+40+36+0+14 = 363
# Multiplicar o resultado anterior por 10
# 363 * 10 = 3630
# Obter o resto da divisão da conta anterior por 11
# 3630 % 11 = 0
# Se o resultado anterior for maior que 9:
#     resultado é 0
# contrário disso:
#     resultado é o valor da conta

# O segundo dígito do CPF é 0

#concatenando os 9 digitos + o primeiro dígito
dez_digitos = list(nove_digitos)
dez_digitos.append(str(primeiro_digito))

# Calculo para o segundo dígito
resultado = 0
numero_regressivo2 = 11
for i in dez_digitos:
    resultado += int(i) * numero_regressivo2
    numero_regressivo2 -= 1

segundo_digito = (resultado * 10) % 11 if (resultado * 10) % 11 <= 9 else 0
# print(f"Validando o segundo dígito:... ' * '") # {segundo_digito}')
print(f"\t\t ... Validando ...") # {segundo_digito}')
print('='*50)

#concatenando os 9 digitos + o primeiro dígito
onze_digitos = list(dez_digitos)
onze_digitos.append(str(segundo_digito))

cpf_unido = ''.join(onze_digitos) # o delimitador é chamado antes

cpf_validado = f'{cpf_unido[:9]}-{cpf_unido[9:]}'

if cpf_digitado_armazenado == cpf_validado:
    print(f'\n\t ... O cpf "{cpf_validado}" é: VÁLIDO ...\n')
else:
    print(f'\n\t ... O cpf "{cpf_digitado_armazenado}" é: INVÁLIDO ...\n')
print('='*50)

