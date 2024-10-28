# Importar bibliotecas
import datetime
import csv

def conciliar_contas(transacoes1, transacoes2):
    # Analisar transacoes1
    transacoes1_dados = []

    for linha in transacoes1:
        t = {}
        t['linha'] = linha.copy()
        t['data_hora'] = linha[0]
        t['departamento'] = linha[1]
        t['valor_transacao'] = linha[2]
        t['beneficiario'] = linha[3]
        t['data_objeto'] = datetime.datetime.strptime(linha[0], '%Y-%m-%d').date()
        t['chave'] = (t['departamento'], t['valor_transacao'], t['beneficiario'])
        t['correspondido'] = False
        transacoes1_dados.append(t)

    # Analisar transacoes2
    transacoes2_dados = []

    for linha in transacoes2:
        t = {}
        t['linha'] = linha.copy()
        t['data_hora'] = linha[0]
        t['departamento'] = linha[1]
        t['valor_transacao'] = linha[2]
        t['beneficiario'] = linha[3]
        t['data_objeto'] = datetime.datetime.strptime(linha[0], '%Y-%m-%d').date()
        t['chave'] = (t['departamento'], t['valor_transacao'], t['beneficiario'])
        t['correspondido'] = False
        transacoes2_dados.append(t)

    # Criando um dicionário para armazenar as transações não correspondidas
    transacoes2_nao_correspondidas = {}
    for t2 in transacoes2_dados:
        chave = t2['chave']
        transacoes2_nao_correspondidas.setdefault(chave, []).append(t2)

    # Definindo diferença máxima entre as datas
    prioridade_diferenca_data = {-1: 1, 0: 2, 1: 3}

    # Processando transacoes1
    for t1 in transacoes1_dados:
        chave = t1['chave']
        data1 = t1['data_objeto']
        encontrado = False
        if chave in transacoes2_nao_correspondidas:
            correspondencias_potenciais = []
            for t2 in transacoes2_nao_correspondidas[chave]:
                data2 = t2['data_objeto']
                diferenca_data = (data2 - data1).days
                if diferenca_data in (-1, 0, 1):
                    correspondencias_potenciais.append((prioridade_diferenca_data[diferenca_data], data2, t2))

            if correspondencias_potenciais:
                # Ordenar as correspondências potenciais
                correspondencias_potenciais.sort(key=lambda x: (x[0], x[1]))
                t2_selecionado = correspondencias_potenciais[0][2]

                t1['correspondido'] = True
                t2_selecionado['correspondido'] = True
                encontrado = True

                # Remover a transação correspondida
                transacoes2_nao_correspondidas[chave].remove(t2_selecionado)
                if not transacoes2_nao_correspondidas[chave]:
                    del transacoes2_nao_correspondidas[chave]

        if not encontrado:
            t1['correspondido'] = False

    # Preparando o resultado
    saida_1 = []
    for t1 in transacoes1_dados:
        status = 'FOUND' if t1['correspondido'] else 'MISSING'
        linha_saida = t1['linha'] + [status]
        saida_1.append(linha_saida)

    saida_2 = []
    for t2 in transacoes2_dados:
        status = 'FOUND' if t2['correspondido'] else 'MISSING'
        linha_saida = t2['linha'] + [status]
        saida_2.append(linha_saida)
                
    # Escrita dos resultados em novos arquivos CSV
    with open('transacoes1_output.csv', 'w', newline='', encoding='utf-8') as arquivo1:
        escritor = csv.writer(arquivo1)
        escritor.writerows(saida_1)

    with open('transacoes2_output.csv', 'w', newline='', encoding='utf-8') as arquivo2:
        escritor = csv.writer(arquivo2)
        escritor.writerows(saida_2)

    return saida_1, saida_2
