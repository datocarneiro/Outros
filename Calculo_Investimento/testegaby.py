investimentos_gaby = float(input("valor"))
meses = int(input("mes"))

taxa_rendimento = 0.01
taxa_imposto = 0.15

rendimento_total = 0
saldo = investimentos_gaby

for gaby in range(meses):
    rendimento_mensal = saldo * taxa_rendimento
    imposto = rendimento_mensal  * taxa_imposto
    rendimento_total += rendimento_mensal
    saldo += rendimento_mensal - imposto
    print(f'saldo mensal {saldo}')
    print('------------------------------------------')

print(rendimento_total)
print(rendimento_total * taxa_imposto)
print(saldo)