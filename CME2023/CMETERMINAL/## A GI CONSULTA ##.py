import os
import pandas as pd

# pasta onde estão os arquivos excel
folder = 'C:/Users/dato/OneDrive/Documentos/Datoo/REPOSITÓRIOS/python/CME2023/CMETERMINAL'
# lista de arquivos excel na pasta
excel_files = [os.path.join(folder, f) for f in os.listdir(folder) if f.endswith('.xlsx')]

while True:
    palavra_chave = input("DIGITE O NOME DO PACIENTE: ")

    for file in excel_files:
        df = pd.read_excel(file, sheet_name=None)
        for sheet_name in df.keys():
            df[sheet_name] = df[sheet_name].astype(str)
        for sheet_name, sheet_df in df.items():
            resultado = sheet_df.apply(lambda x: x.str.contains(palavra_chave, case=False))

            linhas_com_palavra_chave = sheet_df[resultado.any(axis=1)]
            for indice, linha in linhas_com_palavra_chave.iterrows():
                print()
                print()
                print(f"PACIENTE:'{palavra_chave}' - ENCONTRADO EM:'{sheet_name}'")
                print()
                print(linha)
                print()
                print()
    resposta = input("DESEJA FAZER UMA NOVA CONSULTA? DIGITE: (S/N)")
    if resposta.lower() != "s":
        break
    