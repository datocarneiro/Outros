import pandas as pd
from IPython.display import display
import tkinter as tk
from tkinter import filedialog

# Solicitar ao usuário que selecione o arquivo Excel
root = tk.Tk()
root.withdraw()
file_path = filedialog.askopenfilename()

if not file_path.endswith('.xlsx'):
    raise ValueError("Por favor, selecione um arquivo Excel (.xlsx)")

# Ler o arquivo Excel
df = pd.read_excel(file_path)

# Verificar se as colunas 'ID' e 'CEP' existem no DataFrame
if 'ID' not in df.columns or 'CEP' not in df.columns:
    raise ValueError("O arquivo Excel deve conter colunas com cabeçalhos 'ID' e 'CEP'.")

# Criar o dicionário original a partir do DataFrame
dicionario_original = dict(zip(df['ID'], df['CEP']))

# Dicionário modificado
dicionario_modificado = {}

# Iterar sobre o dicionário original
for chave, valor in dicionario_original.items():
    # Verificar se o valor tem 7 dígitos
    if len(str(valor)) == 7:
        # Acrescentar o zero no início e o caractere "-" entre os dígitos 6 e 7
        valor_modificado = '0' + str(valor)[:4] + '-' + str(valor)[4:]
    # Verificar se o valor tem 8 dígitos
    elif len(str(valor)) == 8:
        # Acrescentar o caractere "-" entre os dígitos 5 e 6
        valor_modificado = str(valor)[:5] + '-' + str(valor)[5:]
    else:
        # Valor inválido, mantém o valor original
        valor_modificado = valor

    # Armazenar o valor modificado no novo dicionário
    dicionario_modificado[chave] = valor_modificado

# Criar um DataFrame do pandas com o dicionário modificado
df_modificado = pd.DataFrame(list(dicionario_modificado.items()), columns=['ID', 'CEP'])

# Solicitar ao usuário que escolha o nome e diretório de saída
arquivo_saida = filedialog.asksaveasfilename(defaultextension=".xlsx", filetypes=[("Arquivos Excel", "*.xlsx")])

# Exibir o DataFrame modificado usando a função display
display(df_modificado)

# Salvar o DataFrame modificado em um arquivo Excel com o nome escolhido pelo usuário
df_modificado.to_excel(arquivo_saida, index=False)

print(f"Arquivo Excel '{arquivo_saida}' criado com sucesso.")
