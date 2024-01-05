# entrada de dados com validação, perem gera somnete um cpf
# while True:   
#     while True:
#         try:
#             cpf_input = input("Digite 9 digitos [apenas números]: ")
#             # Verifica se a entrada contém apenas números
#             if not cpf_input.isdigit():
#                 raise ValueError('Digite apenas números.')    
#             informado = tuple(map(str, cpf_input))              
#             # Verifica se o CPF tem 11 dígitos
#             if len(informado) != 9:
#                 raise ValueError('informe somente 9 dígitos.')         
#             break
#         except ValueError as e:
#             print(e)

import random

qtd_cpf = int(input('Quantos deseja gerar?: '))

for i in range(qtd_cpf):
    # gerando 9 digitos
    nove_digitos = ''
    for i in range(9):
        nove_digitos += str(random.randint(0, 9))

    #calculando o primeiro dígito
    resultado = 0
    numero_regressivo1 = 10
    for i in nove_digitos:
        resultado += int(i) * numero_regressivo1
        numero_regressivo1 -= 1
    primeiro_digito = (resultado * 10) % 11 if (resultado * 10) % 11 <= 9 else 0
    # print(f'Gerando o primeiro dígito:... {primeiro_digito}')
    #concatenando os 9 digitos com o primeiro dígito
    dez_digitos = list(nove_digitos)
    dez_digitos.append(str(primeiro_digito))
    #calculando o segundo dígito
    resultado = 0
    numero_regressivo2 = 11
    for i in dez_digitos:
        resultado += int(i) * numero_regressivo2
        numero_regressivo2 -= 1
    segundo_digito = (resultado * 10) % 11 if (resultado * 10) % 11 <= 9 else 0
    # print(f'Gerando o segundo dígito:... {segundo_digito}')
    #concatenando os 10 digitos com o segundo dígito
    resultado_cpf = dez_digitos
    resultado_cpf.append(str(segundo_digito)) 
    # formatando exibição
    cpf_unido = ''.join(resultado_cpf) # o delimitador é chamado antes
    cpf_validado = f'{cpf_unido[:9]}-{cpf_unido[9:]}'
    print(f'\t{cpf_validado}')