import pandas as pd
import csv
import os

diretorioPlanilha = 'D:\Repositórios GitHub\AutomacaoNubank\chargeData.csv'
nome_arquivo = 'D:\Repositórios GitHub\AutomacaoNubank\ArquivoTemporario.csv'
nomeSalvar = 'D:\Repositórios GitHub\AutomacaoNubank\\resultado.csv'
# diretorioPlanilha = 'chargeData.csv'
# nome_arquivo = 'ArquivoTemporario.csv'
# nomeSalvar = 'resultado.csv'

dados = [['Data','Descricao','Gastos']]

def obter_numero_do_mes(mes):
    meses = {
        'Jan': 1,
        'Fev': 2,
        'Mar': 3,
        'Abr': 4,
        'Mai': 5,
        'Jun': 6,
        'Jul': 7,
        'Ago': 8,
        'Set': 9,
        'Out': 10,
        'Nov': 11,
        'Dez': 12
    }
    return meses.get(mes, None)

with open(diretorioPlanilha, mode='r') as arquivo_csv:
    leitor_csv = csv.DictReader(arquivo_csv)
    

    for linha in leitor_csv:
        ano = linha['Ano']
        date = linha['date'].split(' ')[1]
        amount = float(linha['amount'].replace('.','').replace(',','.'))

        if(amount < 0):
            amount = 0

        data = linha['date'].split(' ')[0] + '/' + str(obter_numero_do_mes(linha['date'].split(' ')[1])) + '/' + ano
        dados.append([data, linha['description'], amount])


    # Abra o arquivo CSV em modo de escrita
    with open(nome_arquivo, mode='w', newline='') as arquivo_csv:
        # Crie um objeto escritor CSV
        escritor_csv = csv.writer(arquivo_csv)
        
        # Escreva os dados no arquivo CSV
        for linha in dados:
            escritor_csv.writerow(linha)

    print(f'O arquivo CSV "{nome_arquivo}" foi criado com sucesso.')

# Ler a planilha para um DataFrame (substitua 'seuarquivo.csv' pelo caminho do seu arquivo CSV)
df = pd.read_csv(nome_arquivo)

# Certifique-se de que a coluna 'Data' está no formato de data
df['Data'] = pd.to_datetime(df['Data'])

# Criar colunas separadas para o mês e o ano
df['Ano'] = df['Data'].dt.year
df['Mes'] = df['Data'].dt.month

# Agrupar os dados por mês e ano e somar os gastos
resultado = df.groupby(['Ano', 'Mes'])['Gastos'].sum().reset_index()

if os.path.exists(nome_arquivo):
    # Exclua o arquivo
    os.remove(nome_arquivo)
    print(f'O arquivo CSV "{nome_arquivo}" foi excluido com sucesso.')

# Exibir o resultado
# print(resultado)
resultado.to_csv(nomeSalvar, index=False)
os.system('cls')
print('-'*100)
print(f'O arquivo CSV "{nomeSalvar}" foi Criado com sucesso.')
print('-'*100)