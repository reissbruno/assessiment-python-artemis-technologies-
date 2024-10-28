# Importar bibliotecas
import datetime
import csv

def processar_transacoes(transacoes):
    """
    Processa uma lista de transações para extrair e organizar os dados relevantes.

    Args:
        transacoes (list): Lista de listas, onde cada sub-lista representa uma transação.

    Returns:
        list: Lista de dicionários com os dados processados das transações.
    """
    transacoes_dados = []
    for linha in transacoes:
        t = {}
        t['linha'] = linha.copy()
        t['data_hora'] = linha[0]
        t['departamento'] = linha[1]
        t['valor_transacao'] = linha[2]
        t['beneficiario'] = linha[3]
        t['data_objeto'] = datetime.datetime.strptime(linha[0], '%Y-%m-%d').date()
        t['chave'] = (t['departamento'], t['valor_transacao'], t['beneficiario'])
        t['correspondido'] = False
        transacoes_dados.append(t)
    return transacoes_dados

def preparar_saida(transacoes_dados):
    """
    Prepara a lista de saída com o status de correspondência para cada transação.

    Args:
        transacoes_dados (list): Lista de dicionários contendo os dados das transações.

    Returns:
        list: Lista de listas contendo os dados originais da transação mais o status.
    """
    saida = []
    for t in transacoes_dados:
        status = 'FOUND' if t['correspondido'] else 'MISSING'
        linha_saida = t['linha'] + [status]
        saida.append(linha_saida)
    return saida

def conciliar_contas(transacoes1, transacoes2):
    """
    Compara duas listas de transações para identificar correspondências com base em critérios definidos.

    Args:
        transacoes1 (list): Primeira lista de transações.
        transacoes2 (list): Segunda lista de transações.

    Returns:
        tuple: Duas listas contendo as transações com o status de correspondência.
    """
    # Processar ambas as listas de transações usando a função
    transacoes1_dados = processar_transacoes(transacoes1)
    transacoes2_dados = processar_transacoes(transacoes2)

    # Criando um dicionário para armazenar as transações não correspondidas de transacoes2
    transacoes2_nao_correspondidas = {}
    for t2 in transacoes2_dados:
        chave = t2['chave']
        transacoes2_nao_correspondidas.setdefault(chave, []).append(t2)

    # Definindo diferença máxima entre as datas e suas prioridades
    prioridade_diferenca_data = {-1: 1, 0: 2, 1: 3}

    # Processando transacoes1 para encontrar correspondências em transacoes2
    for t1 in transacoes1_dados:
        chave = t1['chave']
        data1 = t1['data_objeto']
        encontrado = False
        if chave in transacoes2_nao_correspondidas:
            correspondencias_potenciais = []
            for t2 in transacoes2_nao_correspondidas[chave]:
                data2 = t2['data_objeto']
                diferenca_data = (data2 - data1).days
                if diferenca_data in prioridade_diferenca_data:
                    correspondencias_potenciais.append((prioridade_diferenca_data[diferenca_data], data2, t2))

            if correspondencias_potenciais:
                # Ordenar as correspondências potenciais por prioridade e data
                correspondencias_potenciais.sort(key=lambda x: (x[0], x[1]))
                t2_selecionado = correspondencias_potenciais[0][2]

                # Marcar ambas as transações como correspondidas
                t1['correspondido'] = True
                t2_selecionado['correspondido'] = True
                encontrado = True

                # Remover a transação correspondida de transacoes2_nao_correspondidas
                transacoes2_nao_correspondidas[chave].remove(t2_selecionado)
                if not transacoes2_nao_correspondidas[chave]:
                    del transacoes2_nao_correspondidas[chave]

        if not encontrado:
            t1['correspondido'] = False

    # Preparando o resultado usando a função preparar_saida
    saida_1 = preparar_saida(transacoes1_dados)
    saida_2 = preparar_saida(transacoes2_dados)

    # Escrita dos resultados em novos arquivos CSV
    with open('transacoes1_output.csv', 'w', newline='', encoding='utf-8') as arquivo1:
        escritor = csv.writer(arquivo1)
        escritor.writerows(saida_1)

    with open('transacoes2_output.csv', 'w', newline='', encoding='utf-8') as arquivo2:
        escritor = csv.writer(arquivo2)
        escritor.writerows(saida_2)

    return saida_1, saida_2
