import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.preprocessing import LabelEncoder
import joblib
import os
import json
import colorama
from colorama import Fore, Style

colorama.init(autoreset=True)

def carregar_dados(caminho_arquivo):
    try:
        df = pd.read_csv(caminho_arquivo)
        print(Fore.GREEN + "Dataset carregado com sucesso.")
        return df
    except Exception as e:
        print(Fore.RED + f"Erro ao carregar o dataset: {str(e)}")
        return None


def preprocessar_dados(df):
    try:
        df['ID_Paciente'] = df['ID_Paciente'].astype(int)
        df['Idade'] = df['Idade'].astype(int)
        df['Data_Consulta'] = df['Data_Consulta'].astype(str).str.strip()
        
        df['Seguimento'] = df['Seguimento'].map({'Sim': 1, 'Não': 0})
        df.fillna({'Seguimento': 0}, inplace=True)

        le_motivo = LabelEncoder()
        le_diagnostico = LabelEncoder()
        le_tratamento = LabelEncoder()

        df['Motivo_Consulta'] = le_motivo.fit_transform(df['Motivo_Consulta'])
        df['Diagnóstico'] = le_diagnostico.fit_transform(df['Diagnóstico'])
        df['Tratamento'] = le_tratamento.fit_transform(df['Tratamento'])

        print(Fore.GREEN + "Pré-processamento concluído.")
        return df, le_motivo, le_diagnostico, le_tratamento
    except Exception as e:
        print(Fore.RED + f"Erro no pré-processamento: {str(e)}")
        return None, None, None, None


def treinar_modelo(df, modelo_path="modelo_recomendacao.pkl"):
    try:
        X = df[['Idade', 'Motivo_Consulta', 'Diagnóstico']]
        y = df['Tratamento']
        
        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

        model = RandomForestClassifier(n_estimators=100, random_state=42)
        model.fit(X_train, y_train)

        joblib.dump(model, modelo_path)
        print(Fore.GREEN + f"Modelo treinado e salvo em {modelo_path}")
        return model
    except Exception as e:
        print(Fore.RED + f"Erro ao treinar o modelo: {str(e)}")
        return None


def carregar_modelo(modelo_path="modelo_recomendacao.pkl"):
    if os.path.exists(modelo_path):
        try:
            model = joblib.load(modelo_path)
            print(Fore.GREEN + "Modelo carregado com sucesso.")
            return model
        except Exception as e:
            print(Fore.RED + f"Erro ao carregar o modelo: {str(e)}")
    return None


def coletar_informacoes(le_motivo, le_diagnostico, model, le_tratamento, nome_usuario):
    try:
        print(Fore.GREEN + "Bem-vindo ao sistema de recomendação de tratamentos!")

        idade = input(Fore.CYAN + "Digite a sua idade: ")
        if not idade.isdigit():
            print(Fore.RED + "Erro: A idade deve ser um número inteiro.")
            return
        
        idade = int(idade)
        print(Fore.YELLOW + f"Opções de Motivo: {list(le_motivo.classes_)}")
        motivo = input(Fore.CYAN + "Motivo da consulta: ").strip()

        if motivo not in le_motivo.classes_:
            print(Fore.RED + "Erro: Motivo não encontrado. Escolha entre as opções disponíveis.")
            return
        
        print(Fore.YELLOW + f"Opções de Diagnóstico: {list(le_diagnostico.classes_)}")
        diagnostico = input(Fore.CYAN + "Diagnóstico: ").strip()

        if diagnostico not in le_diagnostico.classes_:
            print(Fore.RED + "Erro: Diagnóstico não encontrado. Escolha entre as opções disponíveis.")
            return

        motivo_encoded = le_motivo.transform([motivo])[0]
        diagnostico_encoded = le_diagnostico.transform([diagnostico])[0]

        usuario_data = pd.DataFrame([[idade, motivo_encoded, diagnostico_encoded]], columns=['Idade', 'Motivo_Consulta', 'Diagnóstico'])
        tratamento_recomendado = model.predict(usuario_data)[0]
        tratamento = le_tratamento.inverse_transform([tratamento_recomendado])[0]

        print(Fore.YELLOW + f"Tratamento recomendado: {tratamento}")

        # Criar estrutura JSON
        resposta = {
            "nome": nome_usuario,
            "idade": idade,
            "motivo": motivo,
            "diagnostico": diagnostico,
            "tratamento_recomendado": tratamento
        }

        # Salvar como JSON
        pasta_respostas = "C:/Users/zenet/OneDrive/Desktop/Sprint_4/prevdent-ia/outputs/respostas_modelo"
        os.makedirs(pasta_respostas, exist_ok=True)
        caminho_arquivo_usuario = os.path.join(pasta_respostas, f"{nome_usuario}.json")

        with open(caminho_arquivo_usuario, "w", encoding="utf-8") as f:
            json.dump(resposta, f, indent=4, ensure_ascii=False)

        print(Fore.GREEN + f"Recomendação salva em: {caminho_arquivo_usuario}")

    except Exception as e:
        print(Fore.RED + f"Erro ao coletar informações: {str(e)}")


def main():
    caminho_arquivo = 'C:/Users/zenet/OneDrive/Desktop/Sprint_4/prevdent-ia/data/dataset.csv'
    modelo_path = "modelo_recomendacao.pkl"

    # Solicita nome do usuário
    nome_usuario = input(Fore.CYAN + "Digite seu nome: ").strip()
    if not nome_usuario:
        print(Fore.RED + "Nome inválido. Encerrando o programa.")
        return

    df = carregar_dados(caminho_arquivo)
    if df is None:
        return

    df, le_motivo, le_diagnostico, le_tratamento = preprocessar_dados(df)
    if df is None:
        return

    model = carregar_modelo(modelo_path)
    if model is None:
        model = treinar_modelo(df, modelo_path)
    
    if model is None:
        return

    coletar_informacoes(le_motivo, le_diagnostico, model, le_tratamento, nome_usuario)

if __name__ == "__main__":
    main()
