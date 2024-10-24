# Import libs
import datetime
import csv

def reconcile_accounts(transactions1, transactions2):
    # Parse transactions1
    transactions1_data = []

    # Criando um dicionário para armazenar as transações não correspondidas
    for row in transactions1:
        t = {}
        t['data'] = row.copy()
        t['data_hora'] = row[0]
        t['departamento'] = row[1]
        t['valor_transacao'] = row[2]
        t['beneficiario'] = row[3]
        t['date'] = datetime.datetime.strptime(row[0], '%Y-%m-%d').date()
        t['key'] = (t['departamento'], t['valor_transacao'], t['beneficiario'])
        t['matched'] = False
        transactions1_data.append(t)

    # Parse transactions2
    transactions2_data = []

    # Criando um dicionário para armazenar as transações não correspondidas
    for row in transactions2:
        t = {}
        t['data'] = row.copy()
        t['data_hora'] = row[0]
        t['departamento'] = row[1]
        t['valor_transacao'] = row[2]
        t['beneficiario'] = row[3]
        t['date'] = datetime.datetime.strptime(row[0], '%Y-%m-%d').date()
        t['key'] = (t['departamento'], t['valor_transacao'], t['beneficiario'])
        t['matched'] = False
        transactions2_data.append(t)

    # Criando um dicionário para armazenar as transações não correspondidas
    unmatched_transactions2 = {}
    for t2 in transactions2_data:
        key = t2['key']
        unmatched_transactions2.setdefault(key, []).append(t2)

    # Definindo diferença máxima entre as datas
    date_diff_priority = {-1: 1, 0: 2, 1: 3}

    # Processando transactions1
    for t1 in transactions1_data:
        key = t1['key']
        date1 = t1['date']
        found = False
        if key in unmatched_transactions2:
            potential_matches = []
            for t2 in unmatched_transactions2[key]:
                date2 = t2['date']
                date_diff = (date2 - date1).days
                if date_diff in (-1, 0, 1):
                    potential_matches.append((date_diff_priority[date_diff], date2, t2))

            if potential_matches:
                # Ordenar as correspondências potenciais
                potential_matches.sort(key=lambda x: (x[0], x[1]))
                selected_t2 = potential_matches[0][2]

                t1['matched'] = True
                selected_t2['matched'] = True
                found = True

                # Remover a transação correspondida
                unmatched_transactions2[key].remove(selected_t2)
                if not unmatched_transactions2[key]:
                    del unmatched_transactions2[key]

        if not found:
            t1['matched'] = False

    # Preparando o resultado
    out_1 = []
    for t1 in transactions1_data:
        status = 'FOUND' if t1['matched'] else 'MISSING'
        out_row = t1['data'] + [status]
        out_1.append(out_row)

    out_2 = []
    for t2 in transactions2_data:
        status = 'FOUND' if t2['matched'] else 'MISSING'
        out_row = t2['data'] + [status]
        out_2.append(out_row)
            
    # Escrita dos resultados em novos arquivos CSV
    with open('transactions1_output.csv', 'w', newline='', encoding='utf-8') as file1:
        writer = csv.writer(file1)
        writer.writerows(out_1)

    with open('transactions2_output.csv', 'w', newline='', encoding='utf-8') as file2:
        writer = csv.writer(file2)
        writer.writerows(out_2)

    return out_1, out_2


