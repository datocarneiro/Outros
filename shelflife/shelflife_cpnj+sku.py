import pandas as pd

# Carrega os dados de SKU do primeiro arquivo Excel, 
#Atribui o nome do arquivo que contém informações de SKU a uma variável.
arquivo_sku = "sku.xlsx" 
#Lê as informações contidas no arquivo sku.xlsx utilizando a função read_excel() da biblioteca Pandas 
# e armazena essas informações em um objeto DataFrame chamado df_sku.
df_sku = pd.read_excel(arquivo_sku) 

#Lê as informações contidas no arquivo cnpj.xlsx utilizando a função read_excel() da biblioteca Pandas 
# e armazena essas informações em um objeto DataFrame chamado df_cnpjs.
# O parâmetro header=None indica que o arquivo não possui cabeçalho e o parâmetro names=["CNPJ"] 
# adiciona um cabeçalho à coluna com o nome "CNPJ".
arquivo_cnpjs = "cnpj.xlsx"
df_cnpjs = pd.read_excel(arquivo_cnpjs, header=None, names=["CNPJ"])

# Cria um novo objeto DataFrame vazio chamado df_combinado com duas colunas: "SKU" e "CNPJ".
df_combinado = pd.DataFrame(columns=["SKU", "CNPJ"])

# Inicia um loop que percorre cada linha do objeto DataFrame df_cnpjs na coluna "CNPJ".
for cnpj in df_cnpjs["CNPJ"]:
    
    # Cria um novo objeto DataFrame chamado df_temp contendo duas colunas: "SKU", 
    # que recebe os valores da coluna "Cód. Item" do objeto DataFrame df_sku,
    # e "CPF/CNPJ", que recebe o valor da variável cnpj.
    df_temp = pd.DataFrame({"SKU": df_sku["cod"], "CPF/CNPJ": cnpj}) 

    # Adiciona as informações do objeto DataFrame df_temp ao final do objeto DataFrame df_combinado 
    # utilizando a função concat() da biblioteca Pandas. 
    # O parâmetro ignore_index=True reorganiza os índices das linhas após a concatenação.
    df_combinado = pd.concat([df_combinado, df_temp], ignore_index=True)

# Atribui o nome do arquivo que será salvo com as informações combinadas a uma variável.
arquivo_combinado = "arquivo_combinado.xlsx" 

# Salva as informações do objeto DataFrame df_combinado em um arquivo Excel com o nome definido na variável arquivo_combinado 
# utilizando a função to_excel() da biblioteca Pandas. 
# O parâmetro index=False indica que não serão incluídos os índices das linhas no arquivo.
df_combinado.to_excel(arquivo_combinado, index=False)