# validação
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
    except ValueError as e:
        print(e)

# validar com modulo re
# import re
# # validação com módulo re
# entrada = input('CPF [746.824.890-70]: ')
# cpf_enviado_usuario = re.sub(r'[^0-9]','', entrada)
# entrada_e_sequencial = entrada == entrada[0] * len(entrada)
# if entrada_e_sequencial:
#     print('Você enviou dados sequenciais.')

#armazenando o CPF digitado para validar ao final do código
cpf_informado = ''.join(informado) # o delimitador é chamado antes
cpf_digitado_armazenado = f'{cpf_informado[:9]}-{cpf_informado[9:]}'
print(f'CPF informado: {cpf_digitado_armazenado}')
# variavel irá armazenar somente os 9 primeiros dígitos para o calculo
nove_digitos = informado[:9]   
# Calculo do primeiro dígito
resultado = 0
numero_regressivo1 = 10
for i in nove_digitos:
    resultado += int(i) * numero_regressivo1
    numero_regressivo1 -= 1
primeiro_digito = (resultado * 10) % 11 if (resultado * 10) % 11 <= 9 else 0
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
#concatenando os 9 digitos + o primeiro dígito
onze_digitos = list(dez_digitos)
onze_digitos.append(str(segundo_digito))
# formatando para exibição
cpf_unido = ''.join(onze_digitos) # o delimitador é chamado antes
cpf_validado = f'{cpf_unido[:9]}-{cpf_unido[9:]}'
# validando o CPF digitado com o que foi calculado
print(f"\t\t ... Validando ...") # {segundo_digito}')
if cpf_digitado_armazenado == cpf_validado:
    print(f'\n\t ... O cpf "{cpf_validado}" é: VÁLIDO ...\n')
else:
    print(f'\n\t ... O cpf "{cpf_digitado_armazenado}" é: INVÁLIDO ...\n')


