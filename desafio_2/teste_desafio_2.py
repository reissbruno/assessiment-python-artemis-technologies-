# Import local
from desafio_2 import last_lines
import logging

def criar_arquivo_reverso():
    """Função que cria um novo arquivo com as linhas em ordem reversa."""
    arquivo_origem = r"o-senhor-dos-aneis.txt"
    arquivo_destino = r"o-senhor-dos-aneis-reverso.txt"
    try:
        # Especifique manualmente a codificação aqui, por exemplo:
        input_encoding = 'utf-8-sig'
        with open(arquivo_destino, 'w', encoding='utf-8') as f_destino:
            for linha in last_lines(arquivo_origem, input_encoding=input_encoding):
                f_destino.write(linha)
        logging.info(f"O arquivo reverso foi criado em: {arquivo_destino}")
    except FileNotFoundError:
        logging.error(f"O arquivo '{arquivo_origem}' não foi encontrado.")
        
if __name__ == "__main__":
    criar_arquivo_reverso()