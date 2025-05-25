#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Script para compactar e descompactar arquivos e pastas.

IMPORTANTE:
- A descompactação é feita EXCLUSIVAMENTE pela biblioteca 'stream-unzip'.
- Não é permitido usar nenhuma outra biblioteca para descompactação, nem como fallback.
- A compactação é feita usando a biblioteca padrão 'zipfile'.
"""

import os
import sys
import zipfile
from pathlib import Path
from stream_unzip import stream_unzip

def compactar(caminho_origem, caminho_destino=None):
    """
    Compacta um arquivo ou pasta em um arquivo ZIP.

    Args:
        caminho_origem (str): Caminho do arquivo ou pasta a ser compactado.
        caminho_destino (str, opcional): Caminho do arquivo ZIP de destino.
            Se não for fornecido, será criado um arquivo ZIP com o mesmo nome
            no mesmo diretório.

    Returns:
        str: Caminho do arquivo ZIP criado.
    """
    caminho_origem = Path(caminho_origem)

    if not caminho_origem.exists():
        print(f"Erro: O caminho '{caminho_origem}' não existe.")
        return None

    if caminho_destino is None:
        caminho_destino = f"{caminho_origem}.zip"

    caminho_destino = Path(caminho_destino)

    # Garantir que a extensão seja .zip
    if not str(caminho_destino).lower().endswith('.zip'):
        caminho_destino = Path(f"{caminho_destino}.zip")

    try:
        with zipfile.ZipFile(caminho_destino, 'w', zipfile.ZIP_DEFLATED) as arquivo_zip:
            if caminho_origem.is_file():
                # Compactar um único arquivo
                arquivo_zip.write(caminho_origem, arcname=caminho_origem.name)
                print(f"Arquivo '{caminho_origem}' compactado com sucesso em '{caminho_destino}'.")
            else:
                # Compactar uma pasta e seu conteúdo
                for pasta_atual, _, arquivos in os.walk(caminho_origem):
                    pasta_atual = Path(pasta_atual)
                    # Adicionar arquivos na pasta atual
                    for arquivo in arquivos:
                        caminho_arquivo = pasta_atual / arquivo
                        # Calcular o nome relativo dentro do ZIP
                        nome_relativo = caminho_arquivo.relative_to(caminho_origem.parent)
                        arquivo_zip.write(caminho_arquivo, arcname=str(nome_relativo))
                print(f"Pasta '{caminho_origem}' compactada com sucesso em '{caminho_destino}'.")

        return str(caminho_destino)

    except Exception as e:
        print(f"Erro ao compactar: {e}")
        return None

def descompactar(caminho_zip, pasta_destino=None):
    """
    Descompacta um arquivo ZIP usando EXCLUSIVAMENTE a biblioteca stream-unzip.

    IMPORTANTE: Esta função deve usar APENAS a biblioteca stream-unzip para
    descompactação, nunca use outras bibliotecas como alternativa ou fallback.

    Args:
        caminho_zip (str): Caminho do arquivo ZIP a ser descompactado.
        pasta_destino (str, opcional): Pasta onde os arquivos serão extraídos.
            Se não for fornecida, será criada uma pasta com o mesmo nome do
            arquivo ZIP (sem a extensão) no mesmo diretório.

    Returns:
        str: Caminho da pasta onde os arquivos foram extraídos.
    """
    caminho_zip = Path(caminho_zip)

    if not caminho_zip.exists():
        print(f"Erro: O arquivo ZIP '{caminho_zip}' não existe.")
        return None

    if not str(caminho_zip).lower().endswith('.zip'):
        print(f"Erro: O arquivo '{caminho_zip}' não parece ser um arquivo ZIP.")
        return None

    if pasta_destino is None:
        # Usar o nome do arquivo ZIP sem a extensão como pasta de destino
        pasta_destino = caminho_zip.with_suffix('')

    pasta_destino = Path(pasta_destino)

    # Criar a pasta de destino se não existir
    os.makedirs(pasta_destino, exist_ok=True)

    try:
        # Função que lê o arquivo ZIP em chunks
        def ler_zip_chunks():
            with open(caminho_zip, 'rb') as f:
                while True:
                    chunk = f.read(65536)  # Ler 64KB por vez
                    if not chunk:
                        break
                    yield chunk

        # Descompactar usando stream-unzip (EXCLUSIVAMENTE)
        for nome_arquivo, _, chunks_descompactados in stream_unzip(ler_zip_chunks()):
            # Usamos _ para ignorar o tamanho_arquivo, já que não o utilizamos

            # Converter o nome do arquivo para o formato do sistema operacional
            # O nome_arquivo vem como bytes, precisamos decodificá-lo para string
            nome_arquivo_str = nome_arquivo.decode('utf-8').replace('/', os.sep)
            caminho_arquivo = pasta_destino / nome_arquivo_str

            # Criar diretórios intermediários se necessário
            os.makedirs(caminho_arquivo.parent, exist_ok=True)

            # Verificar se é um diretório (termina com separador)
            if nome_arquivo_str.endswith('/') or nome_arquivo_str.endswith('\\'):
                os.makedirs(caminho_arquivo, exist_ok=True)
                continue

            # Escrever o arquivo descompactado
            with open(caminho_arquivo, 'wb') as f:
                for chunk in chunks_descompactados:
                    f.write(chunk)

            print(f"Extraído: {nome_arquivo_str}")

        print(f"Arquivo ZIP '{caminho_zip}' descompactado com sucesso em '{pasta_destino}'.")
        return str(pasta_destino)

    except Exception as e:
        print(f"Erro ao descompactar: {e}")
        return None

def mostrar_ajuda():
    """Exibe instruções de uso do script."""
    print("Uso:")
    print("  python compactador.py compactar <caminho_origem> [caminho_destino]")
    print("  python compactador.py descompactar <caminho_zip> [pasta_destino]")
    print()
    print("Exemplos:")
    print("  python compactador.py compactar C:\\Users\\Antonio\\Desktop\\Testes_Fotix")
    print("  python compactador.py descompactar C:\\Users\\Antonio\\Desktop\\Testes_Fotix.zip")

if __name__ == "__main__":
    if len(sys.argv) < 3:
        mostrar_ajuda()
        sys.exit(1)

    comando = sys.argv[1].lower()

    if comando == "compactar":
        caminho_origem = sys.argv[2]
        caminho_destino = sys.argv[3] if len(sys.argv) > 3 else None
        compactar(caminho_origem, caminho_destino)

    elif comando == "descompactar":
        caminho_zip = sys.argv[2]
        pasta_destino = sys.argv[3] if len(sys.argv) > 3 else None
        descompactar(caminho_zip, pasta_destino)

    else:
        print(f"Comando desconhecido: {comando}")
        mostrar_ajuda()
        sys.exit(1)
