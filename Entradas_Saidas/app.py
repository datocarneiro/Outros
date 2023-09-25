import pandas as pd
import csv
import os

# Define os caminhos dos arquivos de entrada e saída usando as variáveis 'diretorioPlanilha', 'nome_arquivo' e 'nomeSalvar'.
diretorioPlanilha = 'C:/Users/dato/OneDrive/Documentos/Datoo/REPOSITORIOS/PYTHON/Entradas_Saidas/ameixa.csv'

# Inicializa uma lista chamada 'dados' com o cabeçalho das colunas: ['Data', 'Descricao', 'Gastos'].
dados = [['Data', 'Descricao', 'Gastos']]

# Define a função 'obter_numero_do_mes(mes)' que recebe um mês abreviado como entrada e retorna o número do mês correspondente.
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

# Abre o arquivo CSV especificado em 'diretorioPlanilha' para leitura (mode='r') e cria um objeto 'leitor_csv' para ler o conteúdo do arquivo no formato de dicionário.
with open(diretorioPlanilha, mode='r') as arquivo_csv:
    leitor_csv = csv.DictReader(arquivo_csv)
    
    # Itera sobre cada linha do arquivo CSV utilizando um loop for.
    for linha in leitor_csv:
        # Extrai o ano da coluna 'Ano'.
        # ano = linha['Ano']
        # Divide a coluna 'date' em partes separadas por espaço e pega apenas a segunda parte (representando o mês).
        date = linha['date'].split(' ')[1]
        # Substitui os caracteres '.' por vazio e ',' por '.' na coluna 'amount' e converte o resultado para um número de ponto flutuante.
        amount = float(linha['amount'].replace('.', '').replace(',', '.'))
        # Se o valor for negativo, define-o como zero.
        if amount < 0:
            amount = 0
        # Formata a data no formato 'dd/mm/aaaa' e adiciona à lista 'dados' a data, descrição e gasto da linha atual.
        data = linha['date'].split(' ')[0] + '/' + str(obter_numero_do_mes(date)) + '/' + ano
        dados.append([data, linha['description'], amount])

# Abre o arquivo 'nome_arquivo' para escrita (mode='w') 
with open(nome_arquivo, mode='w', newline='') as arquivo_csv:
    # Cria um objeto 'escritor_csv' para escrever os dados no formato CSV.
    escritor_csv = csv.writer(arquivo_csv)
    
    # Itera sobre cada linha em 'dados' e escreve-a no arquivo CSV.
    for linha in dados:
        escritor_csv.writerow(linha)

# Imprime uma mensagem informando que o arquivo CSV foi criado com sucesso.
print(f'O arquivo CSV "{nome_arquivo}" foi criado com sucesso.')

# Lê o arquivo CSV recém-criado em um DataFrame usando a biblioteca pandas.
df = pd.read_csv(nome_arquivo)

# Converte a coluna 'Data' para formato de data usando 'pd.to_datetime'.
df['Data'] = pd.to_datetime(df['Data'])

# Cria duas novas colunas no DataFrame, 'Ano' e 'Mes', que correspondem ao ano e mês extraídos da coluna 'Data'.
df['Ano'] = df['Data'].dt.year
df['Mes'] = df['Data'].dt.month

# Agrupa os dados por ano e mês e soma os gastos.
resultado = df.groupby(['Ano', 'Mes'])['Gastos'].sum().reset_index()

# Se o arquivo 'nome_arquivo' existir, ele é removido.
if os.path.exists(nome_arquivo):
    os.remove(nome_arquivo)
    # Imprime uma mensagem informando que o arquivo CSV foi excluído com sucesso.
    print(f'O arquivo CSV "{nome_arquivo}" foi excluído com sucesso.')

# Salva o resultado no arquivo 'nomeSalvar' no formato CSV, sem incluir o índice.
resultado.to_csv(nomeSalvar, index=False)

# Limpa a tela do console.
os.system('cls')
print('-' * 100)
print(f'O arquivo CSV "{nomeSalvar}" foi criado com sucesso.')
print('-' * 100)
