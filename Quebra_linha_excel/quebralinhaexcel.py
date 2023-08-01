# Importe a biblioteca pandas para trabalhar com arquivos Excel.
import pandas as pd
import os


# Substitua 'caminho/para/' pelo caminho real para o diretório que contém 'base.xlsx'
caminho_arquivo_entrada = os.path.join('C:/Users/dato/OneDrive/Documentos/Datoo/REPOSITORIOS/PYTHON/Quebra_linha_excel', 'base.xlsx')

print(os.getcwd())

# Defina os caminhos do arquivo de entrada e o nome base dos arquivos de saída
nome_base_arquivos_saida = os.path.join('C:/Users/dato/OneDrive/Documentos/Datoo/REPOSITORIOS/PYTHON/Quebra_linha_excel/Arquivos_Combinados', 'saida_arquivo_combinado')

# Leia o arquivo Excel de entrada e armazene-o em um DataFrame (tabela)
df = pd.read_excel(caminho_arquivo_entrada)

# Divida os dados em pedaços de 900 linhas usando list comprehension
pedacos = [df[i:i+100] for i in range(0, len(df), 100)] # dititar a qtd de linha onde vai gerar a quebra

# Itere sobre cada pedaço e salve-o em um novo arquivo Excel
for i, pedaco in enumerate(pedacos):
    nome_arquivo_saida = f"{nome_base_arquivos_saida}{i+1}.xlsx"
    pedaco.to_excel(nome_arquivo_saida, index=False) # O parâmetro `index=False` evita que seja criada uma coluna para índices no arquivo de saída
