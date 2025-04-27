import sys
from modules.utils import *
from modules.server import servidor
from modules.client import menu
import threading

def main(endereco_porta, vizinhos_txt, diretorio_compartilhado):
    # dicionario com dados do peer
    peer = {
        "endereco": "",
        "porta": 0,
        "vizinhos_file": "",
        "vizinhos": [],  
        "diretorio_compartilhado": "",
        "clock": 0
    }
    try:
        endereco, porta = validar_endereco_porta(endereco_porta)
        validar_arquivo(vizinhos_txt)
        validar_diretorio(diretorio_compartilhado)

        peer["endereco"] = endereco
        peer["porta"] = porta
        peer["vizinhos_file"] = vizinhos_txt
        peer["vizinhos"] = vizinhos_txt_to_list(vizinhos_txt)
        peer["diretorio_compartilhado"] = diretorio_compartilhado

        thread_servidor = threading.Thread(target=servidor, args=(peer,))
        thread_cliente = threading.Thread(target=menu,args =(peer,))

        thread_servidor.start()
        thread_cliente.start()

        thread_cliente.join()
        thread_servidor.join()

    except ValidacaoErro as e:
        return {"erro": str(e)}

if __name__ == "__main__":
    if len(sys.argv) != 4:
        print("Uso: ./eachare <endereço>:<porta> <vizinhos.txt> <diretório_compartilhado>")
        sys.exit(1)
    main(sys.argv[1], sys.argv[2], sys.argv[3])