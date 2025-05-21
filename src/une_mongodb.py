import json

arquivos_json = [
    "../outputs/MongoDB/consultas.json",
    "../outputs/MongoDB/dentistas.json",
    "../outputs/MongoDB/pacientes.json",
    "../outputs/MongoDB/sinistros.json"
]


dados_unificados = []

for arquivo in arquivos_json:
    with open(arquivo, "r", encoding="utf-8") as f:
        dados = json.load(f)
        if isinstance(dados, list):
            dados_unificados.extend(dados)
        else:
            dados_unificados.append(dados)

with open("base_unificada.json", "w", encoding="utf-8") as f_out:
    json.dump(dados_unificados, f_out, ensure_ascii=False, indent=2)

print("Coleções unificadas com sucesso em 'base_unificada.json'")
