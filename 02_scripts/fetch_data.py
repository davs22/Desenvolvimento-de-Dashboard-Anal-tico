import os
import pandas as pd
import yfinance as yf


os.makedirs('data', exist_ok=True)

tickers = {
    'VALE3.SA': 1,
    'PETR4.SA': 2,
    'WEGE3.SA': 3,
    'ABEV3.SA': 4,
    'RENT3.SA': 5
}

print("Coletando preços históricos do Yahoo Finance...")
df_precos_list = []

for ticker_symbol, emp_id in tickers.items():
    stock = yf.Ticker(ticker_symbol)
    hist = stock.history(start="2023-01-01", end="2026-01-01").reset_index()
    hist['EmpresaID'] = emp_id
    hist['Data'] = hist['Date'].dt.date
    hist['PrecoFechamento'] = hist['Close']
    hist['Volume'] = hist['Volume']
    df_precos_list.append(hist[['EmpresaID', 'Data', 'PrecoFechamento', 'Volume']])

df_precos = pd.concat(df_precos_list)
df_precos.to_csv('data/fato_preco.csv', index=False)


dados_financeiros = [
    # Vale (VALE3)
    {'EmpresaID': 1, 'Ano': 2023, 'ReceitaLiquida': 207800, 'LucroLiquido': 39800, 'PatrimonioLiquido': 188000, 'AtivoTotal': 420000, 'NumeroAcoes': 4539000000},
    {'EmpresaID': 1, 'Ano': 2024, 'ReceitaLiquida': 212000, 'LucroLiquido': 35000, 'PatrimonioLiquido': 192000, 'AtivoTotal': 430000, 'NumeroAcoes': 4539000000},
    {'EmpresaID': 1, 'Ano': 2025, 'ReceitaLiquida': 205000, 'LucroLiquido': 32000, 'PatrimonioLiquido': 190000, 'AtivoTotal': 425000, 'NumeroAcoes': 4539000000},
    # Petrobras (PETR4)
    {'EmpresaID': 2, 'Ano': 2023, 'ReceitaLiquida': 511900, 'LucroLiquido': 124600, 'PatrimonioLiquido': 382000, 'AtivoTotal': 1060000, 'NumeroAcoes': 13044000000},
    {'EmpresaID': 2, 'Ano': 2024, 'ReceitaLiquida': 490000, 'LucroLiquido': 105000, 'PatrimonioLiquido': 390000, 'AtivoTotal': 1080000, 'NumeroAcoes': 13044000000},
    {'EmpresaID': 2, 'Ano': 2025, 'ReceitaLiquida': 480000, 'LucroLiquido': 98000,  'PatrimonioLiquido': 395000, 'AtivoTotal': 1090000, 'NumeroAcoes': 13044000000},
    # WEG (WEGE3)
    {'EmpresaID': 3, 'Ano': 2023, 'ReceitaLiquida': 32500,  'LucroLiquido': 5700,   'PatrimonioLiquido': 17500,  'AtivoTotal': 35000,  'NumeroAcoes': 4197000000},
    {'EmpresaID': 3, 'Ano': 2024, 'ReceitaLiquida': 38000,  'LucroLiquido': 6800,   'PatrimonioLiquido': 20500,  'AtivoTotal': 41000,  'NumeroAcoes': 4197000000},
    {'EmpresaID': 3, 'Ano': 2025, 'ReceitaLiquida': 43500,  'LucroLiquido': 7900,   'PatrimonioLiquido': 24000,  'AtivoTotal': 47000,  'NumeroAcoes': 4197000000},
    # Ambev (ABEV3)
    {'EmpresaID': 4, 'Ano': 2023, 'ReceitaLiquida': 79700,  'LucroLiquido': 14800,  'PatrimonioLiquido': 92000,  'AtivoTotal': 140000, 'NumeroAcoes': 15730000000},
    {'EmpresaID': 4, 'Ano': 2024, 'ReceitaLiquida': 82500,  'LucroLiquido': 15200,  'PatrimonioLiquido': 95000,  'AtivoTotal': 143000, 'NumeroAcoes': 15730000000},
    {'EmpresaID': 4, 'Ano': 2025, 'ReceitaLiquida': 85000,  'LucroLiquido': 15800,  'PatrimonioLiquido': 98000,  'AtivoTotal': 146000, 'NumeroAcoes': 15730000000},
    # Localiza (RENT3)
    {'EmpresaID': 5, 'Ano': 2023, 'ReceitaLiquida': 28900,  'LucroLiquido': 1800,   'PatrimonioLiquido': 25800,  'AtivoTotal': 68000,  'NumeroAcoes': 1060000000},
    {'EmpresaID': 5, 'Ano': 2024, 'ReceitaLiquida': 34500,  'LucroLiquido': 2100,   'PatrimonioLiquido': 27500,  'AtivoTotal': 75000,  'NumeroAcoes': 1060000000},
    {'EmpresaID': 5, 'Ano': 2025, 'ReceitaLiquida': 39000,  'LucroLiquido': 2500,   'PatrimonioLiquido': 29500,  'AtivoTotal': 82000,  'NumeroAcoes': 1060000000}
]

df_fin = pd.DataFrame(dados_financeiros)
df_fin.to_csv('data/fato_financeiro.csv', index=False)

print("Tabelas geradas com sucesso na pasta /data!")
