# Importe a biblioteca pandas para trabalhar com arquivos Excel.
import pandas as pd

# Defina os caminhos do arquivo de entrada e o nome base dos arquivos de saída
caminho_arquivo_entrada = "Arquivo_combinado_com_cadastro.xlsx"
nome_base_arquivos_saida = "saida_arquivo_combinado"

# Leia o arquivo Excel de entrada e armazene-o em um DataFrame (tabela)
df = pd.read_excel(caminho_arquivo_entrada)

# Divida os dados em pedaços de 900 linhas usando list comprehension
pedacos = [df[i:i+900] for i in range(0, len(df), 900)] # dititar a qtd de linha onde vai gerar a quebra

# Itere sobre cada pedaço e salve-o em um novo arquivo Excel
for i, pedaco in enumerate(pedacos):
    nome_arquivo_saida = f"{nome_base_arquivos_saida}{i+1}.xlsx"
    pedaco.to_excel(nome_arquivo_saida, index=False) # O parâmetro `index=False` evita que seja criada uma coluna para índices no arquivo de saída
