import pandas as pd
import matplotlib.pyplot as plt
import os
import colorama
from colorama import Fore, Style

colorama.init()

df = pd.read_csv("C:/Users/zenet/OneDrive/Desktop/Sprint_4/prevdent-ia/data/dataset.csv")

df['Data_Consulta'] = df['Data_Consulta'].str.strip("[]").str.replace("'", "").astype(str)
df['Data_Consulta'] = pd.to_datetime(df['Data_Consulta'], format='%Y-%m-%d')

diagnostico_tratamento = df.groupby(['Diagnóstico', 'Tratamento']).size().unstack().fillna(0)
consultas_por_data = df.groupby('Data_Consulta').size()
medicamentos_comuns = df['Medicamentos'].value_counts()
seguimento_taxa = df['Seguimento'].value_counts()

print(Fore.GREEN + "Como você gostaria de visualizar os dados?" + Style.RESET_ALL)
print(Fore.CYAN + "(1) Visualizar gráficos na Web")
print(Fore.CYAN + "(2) Exibir informações no Terminal")
print(Fore.CYAN + "(3) Apenas salvar gráficos como PDFs" + Style.RESET_ALL)

opcao = input(Fore.YELLOW + "Escolha uma opção (1/2/3): " + Style.RESET_ALL)

try:
    if opcao == '1':
        
        plt.figure(figsize=(10, 6))
        diagnostico_tratamento.plot(kind='bar', stacked=True)
        plt.title('Contagem de Tratamentos por Diagnóstico')
        plt.xlabel('Diagnóstico')
        plt.ylabel('Contagem')
        plt.legend(title='Tratamento')
        plt.tight_layout()
        plt.show()

        plt.figure(figsize=(10, 6))
        consultas_por_data.plot()
        plt.title('Número de Consultas ao Longo do Tempo')
        plt.xlabel('Data')
        plt.ylabel('Contagem')
        plt.tight_layout()
        plt.show()

        plt.figure(figsize=(10, 6))
        medicamentos_comuns.plot(kind='bar')
        plt.title('Medicamentos Mais Comuns Prescritos')
        plt.xlabel('Medicamento')
        plt.ylabel('Contagem')
        plt.tight_layout()
        plt.show()

        plt.figure(figsize=(10, 6))
        seguimento_taxa.plot(kind='pie', autopct='%1.1f%%', startangle=90)
        plt.title('Taxa de Seguimento')
        plt.ylabel('')
        plt.tight_layout()
        plt.show()

    elif opcao == '2':
        
        print(Fore.GREEN + "Informações resumidas:" + Style.RESET_ALL)
        print(Fore.YELLOW + "\n1. Contagem de Tratamentos por Diagnóstico:" + Style.RESET_ALL)
        print(diagnostico_tratamento)
        print(Fore.YELLOW + "\n2. Número de Consultas ao Longo do Tempo:" + Style.RESET_ALL)
        print(consultas_por_data)
        print(Fore.YELLOW + "\n3. Medicamentos Mais Comuns Prescritos:" + Style.RESET_ALL)
        print(medicamentos_comuns)
        print(Fore.YELLOW + "\n4. Taxa de Seguimento:" + Style.RESET_ALL)
        print(seguimento_taxa)

    elif opcao == '3':
        
        caminho_pasta_especifica = "C:/Users/zenet/OneDrive/Desktop/Sprint_4/prevdent-ia/outputs/graficos"
        
        
        if not os.path.exists(caminho_pasta_especifica):
            os.makedirs(caminho_pasta_especifica)
        
        
        plt.figure(figsize=(10, 6))
        diagnostico_tratamento.plot(kind='bar', stacked=True)
        plt.title('Contagem de Tratamentos por Diagnóstico')
        plt.xlabel('Diagnóstico')
        plt.ylabel('Contagem')
        plt.legend(title='Tratamento')
        plt.tight_layout()
        plt.savefig(os.path.join(caminho_pasta_especifica, 'grafico_diagnostico_tratamento.pdf'))
        plt.close()

        plt.figure(figsize=(10, 6))
        consultas_por_data.plot()
        plt.title('Número de Consultas ao Longo do Tempo')
        plt.xlabel('Data')
        plt.ylabel('Contagem')
        plt.tight_layout()
        plt.savefig(os.path.join(caminho_pasta_especifica, 'grafico_consultas_por_data.pdf'))
        plt.close()

        plt.figure(figsize=(10, 6))
        medicamentos_comuns.plot(kind='bar')
        plt.title('Medicamentos Mais Comuns Prescritos')
        plt.xlabel('Medicamento')
        plt.ylabel('Contagem')
        plt.tight_layout()
        plt.savefig(os.path.join(caminho_pasta_especifica, 'grafico_medicamentos_comuns.pdf'))
        plt.close()

        plt.figure(figsize=(10, 6))
        seguimento_taxa.plot(kind='pie', autopct='%1.1f%%', startangle=90)
        plt.title('Taxa de Seguimento')
        plt.ylabel('')
        plt.tight_layout()
        plt.savefig(os.path.join(caminho_pasta_especifica, 'grafico_taxa_seguimento.pdf'))
        plt.close()

        print(Fore.GREEN + f"Gráficos salvos com sucesso na pasta '{caminho_pasta_especifica}'." + Style.RESET_ALL)

    else:
        print(Fore.RED + "Opção inválida." + Style.RESET_ALL)

    print(Fore.GREEN + "Finalizado." + Style.RESET_ALL)

except Exception as e:
    print(Fore.RED + f"Erro: {e}" + Style.RESET_ALL)