import csv
from pathlib import Path
from pprint import pprint
from desafio_1 import conciliar_contas

# Leitura dos arquivos CSV
transactions1 = list(csv.reader(Path('transactions1.csv').open(encoding='utf-8')))
transactions2 = list(csv.reader(Path('transactions2.csv').open(encoding='utf-8')))


# Chamada da função de conciliação
out1, out2 = conciliar_contas(transactions1, transactions2)

# Exibição dos resultados
print("Resultado para transactions1:")
pprint(out1)
print("\nResultado para transactions2:")
pprint(out2)
