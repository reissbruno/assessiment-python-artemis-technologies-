# Imports
import io


# Função que lê as últimas linhas de um arquivo
def last_lines(filename, input_encoding='utf-8'):
    """Gerador que produz as linhas de um arquivo em ordem inversa."""
    with open(filename, 'rb') as f:
        f.seek(0, io.SEEK_END)
        fim_do_arquivo = f.tell()
        tamanho_do_bloco = io.DEFAULT_BUFFER_SIZE
        buffer = b''
        posicao = fim_do_arquivo

        # Lê o arquivo em blocos a partir do final
        while posicao > 0:
            tamanho_leitura = min(tamanho_do_bloco, posicao)
            posicao -= tamanho_leitura
            f.seek(posicao)
            bytes_lidos = f.read(tamanho_leitura)
            buffer = bytes_lidos + buffer
            try:
                buffer_str = buffer.decode(input_encoding)
                buffer = b''
            except UnicodeDecodeError as e:
                # Move os bytes incompletos para a próxima iteração
                bytes_validos = buffer[:e.start]
                bytes_incompletos = buffer[e.start:]
                buffer_str = bytes_validos.decode(input_encoding)
                buffer = bytes_incompletos
            linhas = buffer_str.split('\n')
            if posicao > 0:
                incompleta = linhas.pop(0)
                buffer = incompleta.encode(input_encoding) + buffer
            for linha in reversed(linhas):
                yield linha + '\n'
        # Processa quaisquer bytes restantes no buffer
        if buffer:
            yield buffer.decode(input_encoding) + '\n'