import os
from datetime import date, timedelta

from dotenv import load_dotenv
from sqlalchemy import create_engine, text


load_dotenv()


def get_database_url() -> str:
    database_url = os.getenv("DATABASE_URL")
    if database_url:
        return database_url

    db_user = os.getenv("DB_USER", "seu_usuario")
    db_password = os.getenv("DB_PASSWORD", "senha12345")
    db_host = os.getenv("DB_HOST", "127.0.0.1")
    db_port = os.getenv("DB_PORT", "5432")
    db_name = os.getenv("DB_NAME", "dashboard_financeiro")

    return (
        f"postgresql+psycopg://{db_user}:{db_password}"
        f"@{db_host}:{db_port}/{db_name}"
    )


engine = create_engine(get_database_url())

with engine.begin() as conn:
    conn.execute(text("""
        CREATE TABLE IF NOT EXISTS dim_empresa (
            empresa_id INTEGER PRIMARY KEY,
            ticker VARCHAR(10) UNIQUE NOT NULL,
            empresa VARCHAR(100) NOT NULL,
            setor VARCHAR(100) NOT NULL,
            classe_acao VARCHAR(5) NOT NULL
        );
    """))

    conn.execute(text("""
        CREATE TABLE IF NOT EXISTS dim_data (
            data DATE PRIMARY KEY,
            ano INTEGER NOT NULL,
            trimestre INTEGER NOT NULL,
            mes_numero INTEGER NOT NULL,
            mes VARCHAR(20) NOT NULL,
            ano_mes VARCHAR(7) NOT NULL,
            dia INTEGER NOT NULL,
            dia_semana VARCHAR(20) NOT NULL
        );
    """))

    conn.execute(text("""
        CREATE TABLE IF NOT EXISTS fato_preco (
            data DATE NOT NULL,
            empresa_id INTEGER NOT NULL,
            abertura NUMERIC(18,4),
            maxima NUMERIC(18,4),
            minima NUMERIC(18,4),
            fechamento NUMERIC(18,4),
            preco_ajustado NUMERIC(18,4),
            volume NUMERIC(20,2),
            quantidade_negocios BIGINT,

            PRIMARY KEY (data, empresa_id),

            FOREIGN KEY (data)
                REFERENCES dim_data(data),

            FOREIGN KEY (empresa_id)
                REFERENCES dim_empresa(empresa_id)
        );
    """))

    conn.execute(text("""
        CREATE TABLE IF NOT EXISTS fato_financeiro (
            data_referencia DATE NOT NULL,
            ano INTEGER NOT NULL,
            empresa_id INTEGER NOT NULL,

            receita_liquida NUMERIC(22,2),
            lucro_liquido NUMERIC(22,2),
            lucro_atribuivel_controlador NUMERIC(22,2),
            ativo_total NUMERIC(22,2),
            patrimonio_liquido NUMERIC(22,2),

            lpa NUMERIC(18,6),
            qtd_acoes_vpa NUMERIC(22,2),
            vpa NUMERIC(18,6),

            PRIMARY KEY (data_referencia, empresa_id),

            FOREIGN KEY (data_referencia)
                REFERENCES dim_data(data),

            FOREIGN KEY (empresa_id)
                REFERENCES dim_empresa(empresa_id)
        );
    """))

    conn.execute(text("""
        CREATE TABLE IF NOT EXISTS fato_provento (
            provento_id BIGSERIAL PRIMARY KEY,
            data_pagamento DATE NOT NULL,
            empresa_id INTEGER NOT NULL,
            tipo_provento VARCHAR(30) NOT NULL,
            valor_por_acao NUMERIC(18,8) NOT NULL,
            valor_total NUMERIC(22,2),

            FOREIGN KEY (data_pagamento)
                REFERENCES dim_data(data),

            FOREIGN KEY (empresa_id)
                REFERENCES dim_empresa(empresa_id)
        );
    """))

    conn.execute(text("""
        INSERT INTO dim_empresa
            (empresa_id, ticker, empresa, setor, classe_acao)
        VALUES
            (1, 'VALE3', 'Vale', 'Mineração', 'ON'),
            (2, 'PETR4', 'Petrobras', 'Petróleo e Gás', 'PN'),
            (3, 'WEGE3', 'WEG', 'Bens Industriais', 'ON'),
            (4, 'ABEV3', 'Ambev', 'Bebidas', 'ON'),
            (5, 'RENT3', 'Localiza', 'Locação de Veículos', 'ON')
        ON CONFLICT (empresa_id) DO NOTHING;
    """))

    meses = [
        "Janeiro", "Fevereiro", "Março", "Abril",
        "Maio", "Junho", "Julho", "Agosto",
        "Setembro", "Outubro", "Novembro", "Dezembro",
    ]

    dias = [
        "Segunda-feira", "Terça-feira", "Quarta-feira",
        "Quinta-feira", "Sexta-feira", "Sábado", "Domingo",
    ]

    atual = date(2022, 1, 1)
    fim = date(2025, 12, 31)

    while atual <= fim:
        trimestre = ((atual.month - 1) // 3) + 1

        conn.execute(text("""
            INSERT INTO dim_data (
                data,
                ano,
                trimestre,
                mes_numero,
                mes,
                ano_mes,
                dia,
                dia_semana
            )
            VALUES (
                :data,
                :ano,
                :trimestre,
                :mes_numero,
                :mes,
                :ano_mes,
                :dia,
                :dia_semana
            )
            ON CONFLICT (data) DO NOTHING;
        """), {
            "data": atual,
            "ano": atual.year,
            "trimestre": trimestre,
            "mes_numero": atual.month,
            "mes": meses[atual.month - 1],
            "ano_mes": atual.strftime("%Y-%m"),
            "dia": atual.day,
            "dia_semana": dias[atual.weekday()],
        })

        atual += timedelta(days=1)

print("BANCO CRIADO COM SUCESSO.")
print("Tabelas:")
print("- dim_empresa")
print("- dim_data")
print("- fato_preco")
print("- fato_financeiro")
print("- fato_provento")
