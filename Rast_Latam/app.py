from openpyxl import Workbook, load_workbook


# ler valor da celula no excel
#carregar planilha
planilha = load_workbook('Rastreamento.xlsx')
aba_ativa = planilha.active

lista1 = []

#if i != 'Entregue':
for i in aba_ativa["D"]: # "C" é a coluna da planilha que quero percorrer
    if i in aba_ativa != 'ENTREGUE':
        lista1.append(i.value)
    else:
        print('não adicionar')
print(lista1)