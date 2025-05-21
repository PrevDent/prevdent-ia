import json
import os
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.neighbors import KNeighborsClassifier
from colorama import init, Fore, Style

init(autoreset=True)

CAMINHO_DADOS_JSON = '../outputs/MongoDB/base_unificada.json'
CAMINHO_SAIDA_PASTA = '../outputs/MongoDB/respostas_modelo/'

os.makedirs(CAMINHO_SAIDA_PASTA, exist_ok=True)

def carregar_dados_json(caminho):
    with open(caminho, 'r', encoding='utf-8') as f:
        return json.load(f)

def preprocessar_dados(dados):
    registros = []

    for consulta in dados:
        observacao = consulta.get("observacoes", "").strip()
        recomendacao = consulta.get("diagnostico", {}).get("recomendacao", "").strip()

        if observacao and recomendacao:
            registros.append({
                "entrada": observacao,
                "recomendacao": recomendacao
            })

    return pd.DataFrame(registros)

def treinar_modelo(df):
    vetorizador = TfidfVectorizer()
    X = vetorizador.fit_transform(df["entrada"])
    y = df["recomendacao"]
    modelo = KNeighborsClassifier(n_neighbors=3)
    modelo.fit(X, y)
    return modelo, vetorizador

def obter_dados_usuario():
    print(Fore.CYAN + "\nInforme os dados solicitados para recomendação:\n")
    nome = input(Fore.YELLOW + "1. Nome completo: ")
    idade = input(Fore.YELLOW + "2. Idade: ")

    print(Fore.BLUE + "\nExemplos do que você pode digitar:")
    print("- Dor de dente e inchaço na gengiva")
    print("- Sensibilidade ao frio e quente nos dentes")
    print("- Sangramento ao escovar")
    print("- Dente quebrado após queda")
    print("- Gengiva inflamada e vermelha\n")

    motivo = input(Fore.YELLOW + "3. Descreva o motivo da consulta ou sintomas: ")

    return {
        "nome": nome,
        "idade": idade,
        "entrada": motivo
    }

def gerar_nome_arquivo(nome_usuario):
    nome_limpo = nome_usuario.lower().replace(" ", "_")
    caminho_arquivo = os.path.join(CAMINHO_SAIDA_PASTA, f"{nome_limpo}.json")
    
    contador = 1
    while os.path.exists(caminho_arquivo):
        caminho_arquivo = os.path.join(CAMINHO_SAIDA_PASTA, f"{nome_limpo}_{contador}.json")
        contador += 1
    
    return caminho_arquivo

def salvar_resposta_usuario(dados_usuario, recomendacao):
    caminho_arquivo = gerar_nome_arquivo(dados_usuario["nome"])

    resposta = {
        "nome": dados_usuario["nome"],
        "idade": dados_usuario["idade"],
        "entrada": dados_usuario["entrada"],
        "recomendacao": recomendacao
    }

    try:
        with open(caminho_arquivo, 'w', encoding='utf-8') as f:
            json.dump([resposta], f, indent=4, ensure_ascii=False)

        print(Fore.CYAN + f"\nSeus dados foram salvos em '{caminho_arquivo}'.")
    except Exception as e:
        print(Fore.RED + f"Erro ao salvar os dados: {e}")

def main():
    try:
        print(Fore.GREEN + "Carregando dados...")
        dados = carregar_dados_json(CAMINHO_DADOS_JSON)
        print(Fore.GREEN + "✅Dados carregados com sucesso.")

        df = preprocessar_dados(dados)

        if df.empty:
            print(Fore.RED + "Nenhum dado válido encontrado para treinar o modelo.")
            return

        modelo, vetorizador = treinar_modelo(df)
        dados_usuario = obter_dados_usuario()

        entrada_vetorizada = vetorizador.transform([dados_usuario["entrada"]])
        recomendacao = modelo.predict(entrada_vetorizada)[0]

        print(Fore.MAGENTA + f"\nRecomendação para você: {Style.BRIGHT + recomendacao}")
        salvar_resposta_usuario(dados_usuario, recomendacao)

    except Exception as e:
        print(Fore.RED + f"Erro: {e}")

if __name__ == "__main__":
    main()
