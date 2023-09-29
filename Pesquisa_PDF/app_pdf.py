import os
import PyPDF2 # necessario instalar - pip install PyPDF2
import pandas as pd # necessario instalar - pip install pandas
from IPython.display import display

#crei uma lista com os valores que deseja consultar, nesse exemplo usei o CEP
lista = [
            '48280-000',
            '66053-000',
            '78050-000',
            '57036-840',
            '70670-051',
            '49032-000',
            '78065-000',
            '49026-010',
            '77001-080',
            '49140-970',
            '78060-601',
            '78050-000',
            '55012-290',
            '45028-100',
            '54410-010',
            '66023-902',
            '68501-680',
            '68507-445',
            '57051-140',
            '49020-120',
            '55024-715',
            '45200-970',
            '79002-200',
            '49015-230',
            '57100-971',
            '29165-610',
            '49035-500',
            '52041-430',
            '77410-010',
            '46430-000',
            '68508-070',
            '53030-010',
            '57036-840',
            '65073-212',
            '65066-160',
            '65075-060',
            '51110-160',
            '57030-170',
            '78040-365',
            '48903-560',
            '51020-900',
            '45051-075',
            '52051-020',
            '50070-455',
            '51030-300',
            '50710-901',
            '59152-110',
            '31080-255',
            '42850-970',
            '66635-894',
            '49010-000',
            '78030-210',
            '49097-510',
            '45400-000',
            '78455-000',
            '66040-170',
            '78055-428',
            '77020-024',
            '50070-010',
            '78005-370',
            '78125-100',
            '44700-000',
            '78110-400',
            '78008-000',
            '79062-200',
            '59080-900',
            '44900-000',
            '78450-000',
            '46880-000',
            '54450-015',
            '48700-000',
            '53401-435',
            '49160-000',
            '52010-140',
            '49020-550',
            '50670-000',
            '56912-440',
            '79002-351',
            '78088-010',
            '78043-305',
            '48601-260',
            '59025-500',
            '57045-660',
            '67130-120',
            '79080-105',
            '65010-500',
            '57020-220',
            '48970-000',
            '79644-900',
            '78068-360',
            '78043-172',
            '79060-070',
            '78075-850',
            '79950-000',
            '55750-000',
            '78010-200',
            '66120-000',
            '50950-030',
            '53130-150',
            '78360-000',
            '50010-000',
            '59078-600',
            '52031-000',
            '59140-001',
            '59066-180',
            '79010-470',
            '77500-000',
            '79750-000',
            '44190-000',
            '50740-050',
            '57057-450',
            '68552-248',
            '54510-480',
            '78048-135',
            '79092-060',
            '50020-390',
            '79009-095',
            '79103-050',
            '79081-650',
            '67113-970',
            '65110-000',
            '78117-440',
            '53610-000',
            '66033-770',
            '79051-560',
            '79290-000',
            '60135-238',
            '78520-000',
            '55700-000',
            '59054-500',
            '52070-070',
            '49025-100',
            '45810-000',
            '49085-410',
            '53610-605',
            '68005-100',
            '49035-190',
            '79740-000',
            '60811-341',
]

# Lê e exibi no terminal a quantidade de consultas na lista
quantidade_na_lista = len(lista)
print(f' ... A quantidade de itens para consulta é: {quantidade_na_lista} ... ')

# pasta onde estão os pdf para pesquisa
diretorio = 'C:/Users/dato/OneDrive/Documentos/Datoo/REPOSITORIOS/PYTHON/Pesquisa_PDF/salve os pdf aqui'

resultados = {}  # Dicionário para armazenar os resultados

for filename in os.listdir(diretorio):
    if filename.endswith('.pdf'):
        pdf_path = os.path.join(diretorio, filename)
        
        with open(pdf_path, 'rb') as file:
            pdf_reader = PyPDF2.PdfReader(file)
            
            for page_number in range(len(pdf_reader.pages)):
                page = pdf_reader.pages[page_number]
                content = page.extract_text()
                
                for item in lista:
                    if item.lower() in content.lower():
                        resultados[item] = filename

# exibi no terminal  o dicionario com chave e valor
print(resultados)

# Converte dictionario to data frame
tabela_df = pd.DataFrame(list(resultados.items()), columns=['CEP', 'CTE-AWB'])

# Exibi o dataframe no terminal
display(tabela_df)

# Salva o dataframe em um arquivo CSV, EXCEL (altere a extensão de saída)
tabela_df.to_excel('C:/Users/dato/OneDrive/Documentos/Datoo/REPOSITORIOS/PYTHON/Pesquisa_PDF/arquivo_combinado.xlsx', index=False)
