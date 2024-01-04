while True:   
    while True:
        print('='*50)
        try:
            cpf_input = input("Digite 9 digitos [apenas números]: ")
            # Verifica se a entrada contém apenas números
            if not cpf_input.isdigit():
                raise ValueError('Digite apenas números.')
            
            
            informado = tuple(map(str, cpf_input))          # python gerar_CPF.py
            
            # Verifica se o CPF tem 11 dígitos
            if len(informado) != 9:
                raise ValueError('informe somente 9 dígitos.')
            print('='*50)            
            break
        except ValueError as e:
            print(e)

    nove_digitos = informado

    #calculando o primeiro dígito
    resultado = 0
    numero_regressivo1 = 10
    for i in nove_digitos:
        resultado += int(i) * numero_regressivo1
        numero_regressivo1 -= 1

    primeiro_digito = (resultado * 10) % 11 if (resultado * 10) % 11 <= 9 else 0
    print(f'Validando o primeiro dígito:... {primeiro_digito}')

    #concatenando os 9 digitos + o primeiro dígito
    dez_digitos = list(nove_digitos)
    dez_digitos.append(str(primeiro_digito))

    #calculando o segundo dígito
    resultado = 0
    numero_regressivo2 = 11
    for i in dez_digitos:
        resultado += int(i) * numero_regressivo2
        numero_regressivo2 -= 1

    segundo_digito = (resultado * 10) % 11 if (resultado * 10) % 11 <= 9 else 0
    print(f'Validando o segundo dígito:... {segundo_digito}')

    resultado_cpf = dez_digitos

    resultado_cpf.append(str(segundo_digito)) 

    cpf_unido = ''.join(resultado_cpf) # o delimitador é chamado antes

    cpf_validado = f'{cpf_unido[:9]}-{cpf_unido[9:]}'
    print(f'\n\t{cpf_validado}\n')

    continuar = input('Gerar outro? [s]im  [n]ão: ')
    if 's' in continuar:
        continue
    else:
        print('Você encerrou o programa\n')
        print('='*50)
        break
