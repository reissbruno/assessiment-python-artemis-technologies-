# Imports
import io

def abrir_arquivo(filename):
    """
    Abre o arquivo em modo binário.

    Args:
        filename (str): Caminho para o arquivo.

    Returns:
        file object: Objeto do arquivo aberto em modo binário.
    """
    return open(filename, 'rb')

def obter_fim_do_arquivo(file_obj):
    """
    Obtém a posição do final do arquivo.

    Args:
        file_obj (file object): Objeto do arquivo.

    Returns:
        int: Posição do final do arquivo.
    """
    file_obj.seek(0, io.SEEK_END)
    return file_obj.tell()

def ler_bloco(file_obj, pos, tamanho_bloco):
    """
    Lê um bloco de bytes do arquivo a partir de uma posição específica.

    Args:
        file_obj (file object): Objeto do arquivo.
        pos (int): Posição a partir da qual ler.
        tamanho_bloco (int): Tamanho do bloco a ser lido.

    Returns:
        bytes: Bloco de bytes lido.
    """
    file_obj.seek(pos)
    return file_obj.read(tamanho_bloco)

def decodificar_buffer(buffer, input_encoding):
    """
    Decodifica o buffer de bytes em string, lidando com erros de decodificação.

    Args:
        buffer (bytes): Buffer de bytes a ser decodificado.
        input_encoding (str): Codificação do texto.

    Returns:
        tuple: (buffer decodificado, bytes restantes que não puderam ser decodificados)
    """
    try:
        buffer_str = buffer.decode(input_encoding)
        return buffer_str, b''
    except UnicodeDecodeError as e:
        bytes_validos = buffer[:e.start]
        bytes_incompletos = buffer[e.start:]
        buffer_str = bytes_validos.decode(input_encoding)
        return buffer_str, bytes_incompletos

def processar_linhas(buffer_str):
    """
    Processa a string decodificada em linhas.

    Args:
        buffer_str (str): String decodificada do buffer.

    Returns:
        list: Lista de linhas.
    """
    return buffer_str.split('\n')

def last_lines(filename, input_encoding='utf-8'):
    """
    Gera as linhas de um arquivo em ordem inversa.

    Args:
        filename (str): Caminho para o arquivo.
        input_encoding (str, optional): Codificação do arquivo. Padrão é 'utf-8'.

    Yields:
        str: Próxima linha do arquivo em ordem inversa.
    """
    with abrir_arquivo(filename) as f:
        fim_do_arquivo = obter_fim_do_arquivo(f)
        tamanho_do_bloco = io.DEFAULT_BUFFER_SIZE
        buffer = b''
        posicao = fim_do_arquivo

        # Lê o arquivo em blocos a partir do final
        while posicao > 0:
            tamanho_leitura = min(tamanho_do_bloco, posicao)
            posicao -= tamanho_leitura
            bytes_lidos = ler_bloco(f, posicao, tamanho_leitura)
            buffer = bytes_lidos + buffer

            buffer_str, buffer = decodificar_buffer(buffer, input_encoding)
            linhas = processar_linhas(buffer_str)

            if posicao > 0:
                # A primeira linha pode estar incompleta
                incompleta = linhas.pop(0)
                buffer = incompleta.encode(input_encoding) + buffer

            # Gera as linhas em ordem inversa
            for linha in reversed(linhas):
                yield linha + '\n'

        # Gera a primeira linha do arquivo
        if buffer:
            yield buffer.decode(input_encoding) + '\n'