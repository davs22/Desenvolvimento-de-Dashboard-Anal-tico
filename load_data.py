import os
from datetime import date

import yfinance as yf
from dotenv import load_dotenv
from sqlalchemy import create_engine, text

load_dotenv()

DATABASE_URL = (
    f"postgresql+psycopg://{os.getenv('DB_USER')}:"
    f"{os.getenv('DB_PASSWORD')}@{os.getenv('DB_HOST')}:"
    f"{os.getenv('DB_PORT')}/{os.getenv('DB_NAME')}"
)

engine = create_engine(DATABASE_URL)

EMPRESAS = {
    1: "VALE3.SA",
    2: "PETR4.SA",
    3: "WEGE3.SA",
    4: "ABEV3.SA",
    5: "RENT3.SA",
}


def obter_valor(df, coluna, nomes):
    for nome in nomes:
        if nome in df.index:
            valor = df.loc[nome, coluna]

            if hasattr(valor, "item"):
                try:
                    valor = valor.item()
                except Exception:
                    pass

            if valor is not None:
                try:
                    if valor != valor:
                        continue
                except Exception:
                    pass

                return float(valor)

    return None


with engine.begin() as conn:

    for empresa_id, ticker_nome in EMPRESAS.items():

        print(f"\nProcessando {ticker_nome}...")

        ticker = yf.Ticker(ticker_nome)

        # =====================================================
        # PREÇOS 2023-2025
        # =====================================================

        historico = ticker.history(
            start="2023-01-01",
            end="2026-01-01",
            auto_adjust=False
        )

        conn.execute(
            text("""
                DELETE FROM fato_preco
                WHERE empresa_id = :empresa_id
                AND data BETWEEN '2023-01-01' AND '2025-12-31'
            """),
            {"empresa_id": empresa_id}
        )

        for data_indice, linha in historico.iterrows():

            data_pregao = data_indice.date()

            conn.execute(
                text("""
                    INSERT INTO fato_preco (
                        data,
                        empresa_id,
                        abertura,
                        maxima,
                        minima,
                        fechamento,
                        preco_ajustado,
                        volume,
                        quantidade_negocios
                    )
                    VALUES (
                        :data,
                        :empresa_id,
                        :abertura,
                        :maxima,
                        :minima,
                        :fechamento,
                        :ajustado,
                        :volume,
                        NULL
                    )
                """),
                {
                    "data": data_pregao,
                    "empresa_id": empresa_id,
                    "abertura": float(linha["Open"]),
                    "maxima": float(linha["High"]),
                    "minima": float(linha["Low"]),
                    "fechamento": float(linha["Close"]),
                    "ajustado": float(linha["Adj Close"]),
                    "volume": float(linha["Volume"]),
                }
            )

        print(f"  Preços: {len(historico)} registros")

        # =====================================================
        # DADOS FINANCEIROS
        # =====================================================

        dre = ticker.income_stmt
        balanco = ticker.balance_sheet

        anos_inseridos = 0

        for coluna in dre.columns:

            ano = coluna.year

            if ano not in [2022, 2023, 2024, 2025]:
                continue

            receita = obter_valor(
                dre,
                coluna,
                [
                    "Total Revenue",
                    "Operating Revenue"
                ]
            )

            lucro = obter_valor(
                dre,
                coluna,
                [
                    "Net Income",
                    "Net Income Common Stockholders"
                ]
            )

            lucro_controlador = obter_valor(
                dre,
                coluna,
                [
                    "Net Income Common Stockholders",
                    "Net Income"
                ]
            )

            if coluna in balanco.columns:

                ativo = obter_valor(
                    balanco,
                    coluna,
                    ["Total Assets"]
                )

                patrimonio = obter_valor(
                    balanco,
                    coluna,
                    [
                        "Stockholders Equity",
                        "Common Stock Equity"
                    ]
                )

            else:
                ativo = None
                patrimonio = None

            data_referencia = date(ano, 12, 31)

            conn.execute(
                text("""
                    INSERT INTO fato_financeiro (
                        data_referencia,
                        ano,
                        empresa_id,
                        receita_liquida,
                        lucro_liquido,
                        lucro_atribuivel_controlador,
                        ativo_total,
                        patrimonio_liquido
                    )
                    VALUES (
                        :data_referencia,
                        :ano,
                        :empresa_id,
                        :receita,
                        :lucro,
                        :lucro_controlador,
                        :ativo,
                        :patrimonio
                    )
                    ON CONFLICT (data_referencia, empresa_id)
                    DO UPDATE SET
                        receita_liquida = EXCLUDED.receita_liquida,
                        lucro_liquido = EXCLUDED.lucro_liquido,
                        lucro_atribuivel_controlador =
                            EXCLUDED.lucro_atribuivel_controlador,
                        ativo_total = EXCLUDED.ativo_total,
                        patrimonio_liquido =
                            EXCLUDED.patrimonio_liquido
                """),
                {
                    "data_referencia": data_referencia,
                    "ano": ano,
                    "empresa_id": empresa_id,
                    "receita": receita,
                    "lucro": lucro,
                    "lucro_controlador": lucro_controlador,
                    "ativo": ativo,
                    "patrimonio": patrimonio,
                }
            )

            anos_inseridos += 1

        print(f"  Financeiro: {anos_inseridos} anos")

        # =====================================================
        # PROVENTOS
        # =====================================================

        dividendos = ticker.dividends

        conn.execute(
            text("""
                DELETE FROM fato_provento
                WHERE empresa_id = :empresa_id
                AND data_pagamento BETWEEN
                    '2023-01-01' AND '2025-12-31'
            """),
            {"empresa_id": empresa_id}
        )

        qtd_proventos = 0

        for data_indice, valor in dividendos.items():

            data_pagamento = data_indice.date()

            if not (
                date(2023, 1, 1)
                <= data_pagamento
                <= date(2025, 12, 31)
            ):
                continue

            conn.execute(
                text("""
                    INSERT INTO fato_provento (
                        data_pagamento,
                        empresa_id,
                        tipo_provento,
                        valor_por_acao,
                        valor_total
                    )
                    VALUES (
                        :data,
                        :empresa_id,
                        'Provento',
                        :valor,
                        NULL
                    )
                """),
                {
                    "data": data_pagamento,
                    "empresa_id": empresa_id,
                    "valor": float(valor)
                }
            )

            qtd_proventos += 1

        print(f"  Proventos: {qtd_proventos} registros")


print("\n====================================")
print("CARGA FINALIZADA COM SUCESSO")
print("====================================")