import tkinter as tk

receita = {
    "ingredientes": [
        "Ingredientes:",
        "- 250g de carne moída",
        "- 1 cebola picada",
        "- 2 dentes de alho picados",
        "- 1 tomate picado",
        "- 1/2 colher de chá de sal",
        "- 1/4 colher de chá de pimenta",
        "- 2 ovos",
        "- 200 ml de leite",
        "- 150g de farinha de trigo",
        "- 2 colheres de sopa de óleo vegetal",
    ],
    "preparo": [
        "Modo de Preparo:",
        "1. Refogue a cebola e o alho até dourar.",
        "2. Adicione a carne moída e cozinhe até que esteja completamente cozida.",
        "3. Acrescente o tomate, o sal e a pimenta, e cozinhe por mais alguns minutos.",
        "4. Em uma liquidificador ou batedeira, bata os ovos e o leite.",
        "5. Adicione a farinha de trigo aos poucos, mexendo até obter uma massa homogênea.",
        "6. Aqueça uma frigideira antiaderente e untá-la com óleo vegetal.",
        "7. Despeje uma concha pequena de massa na frigideira e espalhe uniformemente.",
        "8. Cozinhe cada lado da panqueca até que esteja dourado.",
        "9. Coloque uma porção do recheio de carne moída no centro de cada panqueca.",
        "10. Enrole a panqueca, cobrindo o recheio.",        
        "11. Opcional: cubra com uma fatia de queijo e leve ao forno por 5 minutos a 180°.",
        "12. Sirva quente com molho de sua escolha.",
    ]
}

def exibir_conteudo(secao):
    receita_text.config(state=tk.NORMAL)
    receita_text.delete(1.0, tk.END) 
    for linha in receita[secao]:
        receita_text.insert(tk.END, linha + "\n")
    receita_text.config(state=tk.DISABLED)  

janela = tk.Tk()

janela.title("Receita de Panqueca")

botao_ingredientes = tk.Button(janela, text="Ingredientes", command=lambda: exibir_conteudo("ingredientes"))
botao_preparo = tk.Button(janela, text="Modo de Preparo", command=lambda: exibir_conteudo("preparo"))

botao_ingredientes.pack()
botao_preparo.pack()

receita_text = tk.Text(janela, wrap=tk.WORD, height=20, width=50)
receita_text.pack()
receita_text.config(state=tk.DISABLED)  

janela.mainloop() 