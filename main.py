import pandas as pd
from tabulate import tabulate
from modules import data_filter

# Dicionário de objetivos estratégicos com funções vinculadas
OBJECTIVES = {
    "1": ("Dispersão com Baixo Custo", data_filter.dispersao_baixo_custo),
    "2": ("Domínio de Marca", data_filter.dominio_de_marca),
    "3": ("Oportunidade de Crescimento", data_filter.oportunidade_crescimento),
    "4": ("Geração de Demanda Qualificada", data_filter.demanda_qualificada),
    "5": ("Aposta em Nichos Emergentes", data_filter.aposta_nicho),
    "6": ("Apoio à Conversão", data_filter.apoio_conversao),
    "7": ("Reconhecimento com Mídia Rica", data_filter.reconhecimento_com_midia),
}

# Boas-vindas
print("\n👋 Bem-vindo ao AnalisAI")
empresa = input("Qual a empresa que você gostaria de pesquisar? ").strip()

# Seleção de objetivo estratégico
print("\nAgora me conta, qual o seu objetivo estratégico:")
for key, (name, _) in OBJECTIVES.items():
    print(f"{key}. {name}")

escolha = input("\nDigite o número da sua escolha: ").strip()
objetivo = OBJECTIVES.get(escolha)

if not objetivo:
    print("❌ Objetivo inválido. Tente novamente.")
    exit()

nome_objetivo, funcao_objetivo = objetivo

# Carrega a base de dados
try:
    df = pd.read_excel("db/DataBase-Fini.xlsx", sheet_name="Sheet 1")
except FileNotFoundError:
    print("❌ Base de dados não encontrada.")
    exit()

# Aplica a função de estratégia
df_resultado = funcao_objetivo(df)

# Exibe o resultado
if df_resultado.empty:
    print("\n⚠️ Nenhum resultado encontrado com os critérios escolhidos.")
else:
    print(f"\n🔍 Top resultados para '{nome_objetivo}' em '{empresa}':\n")
    print(tabulate(
        df_resultado[["Keyword", "Search Volume", "CPC", "Number of Results"]],
        headers="keys",
        tablefmt="fancy_grid"
    ))
