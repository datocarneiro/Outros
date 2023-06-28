# Este programa une a informação de 2 planilhas

# Nesse exemplo foi vinculado 18 SKU para cada CNPJ 
        SKU	                Cód. Item
        7898994908722	62.702.238/0010-07
        7898994908739	62.702.238/0010-07
        7898994908746	62.702.238/0010-07
        7898994908753	62.702.238/0010-07
        7898994908715	62.702.238/0010-07
        7898994908739/AMOSTRA	62.702.238/0010-07
        7898994908746/AMOSTRA	62.702.238/0010-07
        7898994908753/AMOSTRA	62.702.238/0010-07
        8777	62.702.238/0010-07
        6065	62.702.238/0010-07
        5064	62.702.238/0010-07
        5071	62.702.238/0010-07
        5088	62.702.238/0010-07
        8760	62.702.238/0010-07
        TESTESHELFLIFE	62.702.238/0010-07
        7896579902028	62.702.238/0010-07
        5293	62.702.238/0010-07
        5286	62.702.238/0010-07
        7898994908722	37.972.472/0001-16
        7898994908739	37.972.472/0001-16
        7898994908746	37.972.472/0001-16
        7898994908753	37.972.472/0001-16
        7898994908715	37.972.472/0001-16
        7898994908739/AMOSTRA	37.972.472/0001-16
        7898994908746/AMOSTRA	37.972.472/0001-16
        7898994908753/AMOSTRA	37.972.472/0001-16
        8777	37.972.472/0001-16
        6065	37.972.472/0001-16
        5064	37.972.472/0001-16
        5071	37.972.472/0001-16
        5088	37.972.472/0001-16
        8760	37.972.472/0001-16
        TESTESHELFLIFE	37.972.472/0001-16
        7896579902028	37.972.472/0001-16
        5293	37.972.472/0001-16
        5286	37.972.472/0001-16

# Este programa faz a junção da listagem que há no arquivo que contém a listagem de SKU , com o arquivo que contém a listagem de cnpj

# As duas planilhas de SKU e CNPJ devem obrigatóriamente estar salva na mesma pasta do programa, a extensão do arquvo devem ser conforme o código, nesse caso foi xlsx.

# o cabeçalho do arquivo devem ser obrigatóriamente igual tanto no arquivo como no código, como no exemplo abaixo
# df_temp = pd.DataFrame({"SKU": df_sku["cod"], "CPF/CNPJ": cnpj}) 

# Após o processo será criado o arquivo_combinado com o resultado final.

