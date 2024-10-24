import csv
from pathlib import Path
from pprint import pprint
from desafio_1 import reconcile_accounts

# Leitura dos arquivos CSV
transactions1 = list(csv.reader(Path('C:/Users/Bruno Reis/Documents/assessiment-python-artemis-technologies-/desafio_1/transactions1.csv').open(encoding='utf-8')))
transactions2 = list(csv.reader(Path('C:/Users/Bruno Reis/Documents/assessiment-python-artemis-technologies-/desafio_1/transactions2.csv').open(encoding='utf-8')))


# Chamada da função de conciliação
out1, out2 = reconcile_accounts(transactions1, transactions2)

# Exibição dos resultados
print("Resultado para transactions1:")
pprint(out1)
print("\nResultado para transactions2:")
pprint(out2)
