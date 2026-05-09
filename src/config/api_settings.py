# BCB SERIES (API Banco Central)
SERIES = {
    4390:  "selic_mensal",
    433:   "ipca",
    1636:  "ipca_habitacao",
    192:   "incc_di",
    27576: "ic_br_metal",
    29040: "ic_br_metal_usd",
}

# SINAPI CONFIG (API SIDRA/IBGE)
SINAPI_CONFIG = {
    "tabela": "2296",
    "variaveis": "48, 2119, 2120", # custo geral, custo materiais, custo mo
    "nivel": "n1",
    "territorio": "all",
    "descricao": "SINAPI — Custo médio m² construção residencial",
}