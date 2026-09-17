CREATE TABLE DimEmpresa (
    EmpresaID INT PRIMARY KEY,
    Ticker VARCHAR(10) NOT NULL UNIQUE,
    NomeEmpresa VARCHAR(100) NOT NULL,
    Setor VARCHAR(50) NOT NULL
);

CREATE TABLE DimData (
    Data DATE PRIMARY KEY,
    Ano INT NOT NULL,
    Trimestre INT NOT NULL,
    Mes INT NOT NULL,
    NomeMes VARCHAR(20) NOT NULL,
    Dia INT NOT NULL,
    DiaDaSemana VARCHAR(20) NOT NULL
);

CREATE TABLE FatoPreco (
    PrecoID SERIAL PRIMARY KEY,
    EmpresaID INT REFERENCES DimEmpresa(EmpresaID),
    Data DATE REFERENCES DimData(Data),
    PrecoFechamento NUMERIC(10,2) NOT NULL,
    Volume BIGINT
);

CREATE TABLE FatoFinanceiro (
    FinanceiroID SERIAL PRIMARY KEY,
    EmpresaID INT REFERENCES DimEmpresa(EmpresaID),
    Ano INT NOT NULL,
    ReceitaLiquida NUMERIC(15,2) NOT NULL,
    LucroLiquido NUMERIC(15,2) NOT NULL,
    PatrimonioLiquido NUMERIC(15,2) NOT NULL,
    AtivoTotal NUMERIC(15,2) NOT NULL,
    NumeroAcoes BIGINT NOT NULL
);
