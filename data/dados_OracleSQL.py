import oracledb
import pandas as pd

def criar_conexao():
    try:
        dsnStr = oracledb.makedsn("oracle.fiap.com.br", 1521, "ORCL")
        conn = oracledb.connect(
            user="rm553621",
            password="051102",
            dsn=dsnStr
        )
        print("✅ Conexão estabelecida com sucesso.")
        return conn
    except oracledb.DatabaseError as e:
        print("❌ Erro ao conectar ao banco:", e)
        return None

TABELAS_DESEJADAS = [
    "T_PD_CH_CONSULTAS",
    "T_PD_CH_DENTISTAS",
    "T_PD_CH_DENTISTAS_ESPECIALIDADES",
    "T_PD_CH_DIAGNOSTICOS",
    "T_PD_CH_DIAGNOSTICOS_SINISTROS",
    "T_PD_CH_ESPECIALIDADES",
    "T_PD_CH_PACIENTES",
    "T_PD_CH_PACIENTES_PLANOS",
    "T_PD_CH_PLANOS_SAUDE",
    "T_PD_CH_SINISTROS"
]

def obter_dados_tabela(conn, tabela):
    try:
        with conn.cursor() as cursor:
            cursor.execute(f"SELECT * FROM {tabela}")
            colunas = [desc[0] for desc in cursor.description]
            registros = cursor.fetchall()
            return colunas, registros
    except Exception as e:
        print(f"❌ Erro ao obter dados da tabela {tabela}: {e}")
        return [], []

def salvar_csv(tabela, colunas, registros):
    if not registros:
        print(f"⚠️ Nenhum dado encontrado para {tabela}, CSV não será gerado.")
        return

    df = pd.DataFrame(registros, columns=colunas)
    nome_arquivo = f"{tabela}.csv"
    df.to_csv(nome_arquivo, index=False, encoding="utf-8", sep=";")
    print(f"📁 CSV gerado: {nome_arquivo}")

def exportar_dados_para_csv():
    conn = criar_conexao()
    if not conn:
        return

    try:
        for tabela in TABELAS_DESEJADAS:
            colunas, registros = obter_dados_tabela(conn, tabela)
            salvar_csv(tabela, colunas, registros)
    except Exception as e:
        print(f"❌ Erro durante a exportação: {e}")
    finally:
        conn.close()

exportar_dados_para_csv()
