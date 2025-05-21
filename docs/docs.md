
# 🦷 PrevDent IA — Sistema de Recomendação com IA para Clínicas Odontológicas

## 📌 Descrição do Projeto

Este projeto implementa um sistema inteligente de recomendação de tratamentos odontológicos com base em dados históricos de pacientes. A solução foi construída em Python, utilizando dados previamente exportados do MongoDB, tratados localmente e processados por um modelo de Machine Learning.

---

## 🎯 Objetivos

- Utilizar dados clínicos para treinar um modelo que auxilie na recomendação de tratamentos.
- Oferecer uma interface via terminal para o usuário final (paciente ou atendente).
- Salvar as respostas e interações para fins de auditoria e evolução do modelo.

---

## 🧠 Tecnologias Utilizadas

| Tecnologia       | Finalidade                                 |
|------------------|---------------------------------------------|
| Python 3.11      | Linguagem principal                         |
| pandas           | Manipulação e análise de dados              |
| scikit-learn     | Modelo de Machine Learning (KNN)            |
| TfidfVectorizer  | Transformação de texto em vetores numéricos |
| colorama         | Cores no terminal (experiência do usuário)  |
| MongoDB (export) | Fonte original dos dados                    |

---

## 📁 Estrutura de Pastas

```
prevdent-ia/
├── outputs/
│   ├── MongoDB/
│   │   └── base_unificada.json      # Base de dados exportada do Mongo
│   └── respostas/                   # Respostas dos usuários salvas aqui
│       └── Neymar.json              # Exemplo de resposta individual
├── src/
│   └── recomendacao_mongo.py        # Código principal do sistema
└── README.md                        # Este arquivo de documentação
```

---

## ⚙️ Como Funciona

1. **Carga dos dados**: Os dados são lidos do arquivo `base_unificada.json`, unificados e pré-processados.
2. **Treinamento do modelo**: Um modelo KNN é treinado com base nas observações e recomendações históricas.
3. **Interação com o usuário**: O terminal solicita:
   - Nome completo
   - Idade
   - Sintomas ou motivo da consulta
4. **Predição**: O modelo retorna uma recomendação de tratamento com base na entrada.
5. **Armazenamento**: A resposta é salva como um arquivo `.json` no diretório `outputs/respostas/`, nomeado com o nome completo do usuário.

---

## 📝 Exemplos de Entrada (Campo: Sintomas)

- "Dor de dente"
- "Sangramento na gengiva"
- "Dente quebrado"
- "Mau hálito persistente"
- "Sensibilidade ao frio"
- "Retirada de siso"
- "Gengiva inflamada"
- "Cárie visível"
- "Dor ao mastigar"
- "Consulta preventiva"

---

## 🛠️ Execução

Execute no terminal:

```bash
python src/recomendacao_mongo.py
```

---

## 💾 Exemplo de Resposta Salva

Arquivo: `outputs/respostas/Neymar.json`

```json
[
    {
        "nome": "Neymar",
        "idade": "33",
        "entrada": "Dor de dente",
        "recomendacao": "Drenagem e antibióticos"
    }
]
```

---

## 📌 Observações

- O modelo pode ser facilmente substituído por outros algoritmos com melhor desempenho no futuro.
- A base de dados é carregada de forma local, dispensando conexão ativa com o MongoDB.
- O histórico das respostas pode ser utilizado para aprimoramento contínuo do modelo.

---

## 📧 Contato

Caso deseje contribuir ou tenha dúvidas, entre em contato com o responsável pelo projeto.

---

## Link Vídeo:
https://www.youtube.com/watch?v=xe6j4f32Ky0