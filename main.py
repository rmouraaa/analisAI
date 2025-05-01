import pandas as pd
from tabulate import tabulate

from modules.seo_functions import (
    dispersao_baixo_custo,
    dominio_de_marca,
    oportunidade_crescimento,
    demanda_qualificada,
    aposta_nicho,
    apoio_conversao,
    reconhecimento_com_midia
)

OBJECTIVES = {
    "1": ("Dispersão com Baixo Custo", dispersao_baixo_custo),
    "2": ("Domínio de Marca", dominio_de_marca),
    "3": ("Oportunidade de Crescimento", oportunidade_crescimento),
    "4": ("Geração de Demanda Qualificada", demanda_qualificada),
    "5": ("Aposta em Nichos Emergentes", aposta_nicho),
    "6": ("Apoio à Conversão", apoio_conversao),
    "7": ("Reconhecimento com Mídia Rica", reconhecimento_com_midia),
}


def main():
    print("\n👋 Bem-vindo ao AnalisAI")
    empresa = input("Qual a empresa que você gostaria de pesquisar? ").strip()

    print("\nAgora me conta, qual o seu objetivo estratégico:")
    for key, (name, _) in OBJECTIVES.items():
        print(f"{key}. {name}")

    escolha = input("\nDigite o número da sua escolha: ").strip()
    escolha_tuple = OBJECTIVES.get(escolha)

    if not escolha_tuple:
        print("❌ Objetivo inválido. Tente novamente.")
        return

    nome_objetivo, funcao_objetivo = escolha_tuple

    try:
        df = pd.read_excel("db/DataBase-Fini.xlsx", sheet_name="Sheet 1")
    except FileNotFoundError:
        print("❌ Base de dados não encontrada.")
        return

    df_resultado = funcao_objetivo(df)

    if df_resultado.empty:
        print("\n⚠️ Nenhum resultado encontrado com os critérios escolhidos.")
    else:
        print(f"\n🔍 Top resultados para '{nome_objetivo}' em '{empresa}':\n")
        print(tabulate(
            df_resultado[["Keyword", "Search Volume",
                          "CPC", "Number of Results"]],
            headers="keys",
            tablefmt="fancy_grid"
        ))


if __name__ == "__main__":
    main()
