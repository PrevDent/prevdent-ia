import json

# Nomes dos arquivos das suas coleções
arquivos_json = [
    "C:/Users/zenet/OneDrive/Desktop/Sprint_4/prevdent-ia/outputs/MongoDB/consultas.json",
    "C:/Users/zenet/OneDrive/Desktop/Sprint_4/prevdent-ia/outputs/MongoDB/dentistas.json",
    "C:/Users/zenet/OneDrive/Desktop/Sprint_4/prevdent-ia/outputs/MongoDB/pacientes.json",
    "C:/Users/zenet/OneDrive/Desktop/Sprint_4/prevdent-ia/outputs/MongoDB/sinistros.json"
]

# Lista para armazenar todos os dados unificados
dados_unificados = []

# Ler e unir os dados
for arquivo in arquivos_json:
    with open(arquivo, "r", encoding="utf-8") as f:
        dados = json.load(f)
        if isinstance(dados, list):
            dados_unificados.extend(dados)
        else:
            dados_unificados.append(dados)

# Salvar tudo em um novo JSON unificado
with open("base_unificada.json", "w", encoding="utf-8") as f_out:
    json.dump(dados_unificados, f_out, ensure_ascii=False, indent=2)

print("Coleções unificadas com sucesso em 'base_unificada.json'")
