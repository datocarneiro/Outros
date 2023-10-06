# app.py

import pandas as pd

def criar_dataframe():
    dados = [{'awb': 123, 'status': "entregue", 'data': "10/10/2023"},
             {'awb': 456, 'status': "rota", 'data': "2/2/2023"}]
    df = pd.DataFrame(dados)
    return df