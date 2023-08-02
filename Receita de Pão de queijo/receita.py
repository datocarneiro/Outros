class PaoDeQueijo:
    def _init_(self):
        self.polvilhoDoceGramas = 500
        self.mlDeLeite = 250
        self.mlDeOleo = 100
        self.ovos = 2
        self.gramasDeQueijoMeiaCuraRalado = 200
        self.colherDeCháDeSal = 1

    def reunir_ingredientes(self):
        print("Passo 1:Reunindo os ingredientes...")
        print(f"{self.polvilhoDoceGramas}g de polvilho doce")
        print(f"{self.mlDeLeite}ml de leite")
        print(f"{self.mlDeOleo}ml de óleo")
        print(f"{self.ovos} ovos")
        print(f"{self.gramasDeQueijoMeiaCuraRalado}g de queijo meia cura ralado")
        print(f"{self.colherDeCháDeSal} colher de chá de sal")

    def misturar_ingredientes(self):
        print("Passo 2: Misturando os ingredientes...")
        self.misturar_ingredientes_secos()
        self.adicionar_leite_e_oleo_fervidos()
        self.adicionar_ovos_e_queijo_ralado()

    def misturar_ingredientes_secos(self):
        print("Passo 3: Adicione o polvilho doce e o sal em uma tigela.")
        print("Passo 4: Misture bem o polvilho e o sal.")
        contador_tentativas = 0
        while not self.massa_homogenea() and contador_tentativas < 5:
            contador_tentativas += 1
            print(f"Tentativa {contador_tentativas}: Misturando a massa...")

    def massa_homogenea(self):
        return True

    def adicionar_leite_e_oleo_fervidos(self):
        print("Passo 5: Despeje o leite e o óleo fervidos sobre o polvilho misturado.")

    def adicionar_ovos_e_queijo_ralado(self):
        print("Passo 6: Acrescente os ovos e o queijo meia cura ralado.")

    def modelar_paes_de_queijo(self):
        print("Passo 7: Modele pequenas bolinhas de massa com as mãos.")
        for i in range(1, 16):
            print(f"Modelando pão de queijo {i}")

    def assar_paes_de_queijo(self):
        print("Passo 8: Disponha as bolinhas de massa em uma forma untada e asse no forno preaquecido a 180°C "
              "por 25-30 minutos ou até dourar.")

    def retirar_do_forno(self):
        print("Passo 9: Retire os pães de queijo do forno, deixe esfriar um pouco e sirva ainda quentinho!")
        for i in range(1, 16):
            print(f"Tirando da forma o pão de queijo {i}")        

    def aproveitar_sabor(self):
        print("Passo 10: Aproveite o sabor irresistível dos pães de queijo!")


pao_de_queijo = PaoDeQueijo()
pao_de_queijo.reunir_ingredientes()
pao_de_queijo.misturar_ingredientes()
pao_de_queijo.modelar_paes_de_queijo()
pao_de_queijo.assar_paes_de_queijo()
pao_de_queijo.retirar_do_forno()
pao_de_queijo.aproveitar_sabor()