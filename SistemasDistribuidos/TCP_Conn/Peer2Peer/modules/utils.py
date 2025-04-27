import os

class ValidacaoErro(Exception):
    pass

def validar_endereco_porta(endereco_porta):
    try:
        endereco, porta = endereco_porta.split(":")
        porta = int(porta)
        return endereco, porta
    except ValueError:
        raise ValidacaoErro("Endereço e porta devem estar no formato <endereço>:<porta>")

def validar_arquivo(caminho_arquivo):
    if not os.path.isfile(caminho_arquivo):
        raise ValidacaoErro(f"Arquivo {caminho_arquivo} não encontrado.")

def validar_diretorio(caminho_diretorio):
    if not os.path.isdir(caminho_diretorio):
        raise ValidacaoErro(f"Diretório {caminho_diretorio} não encontrado.")

def incrementa_clock(peer):
    peer['clock'] = peer['clock']+1
    print(f"=> Atualizando relogio para {peer['clock']}") 
    return

def vizinhos_txt_to_list(vizinhos_file='vizinhos.txt'):
    # lista de tuplas
    vizinhos = []
    try:
        with open(vizinhos_file, 'r', encoding='utf-8') as arquivo:
            status = 'OFFLINE'
            for linha in arquivo:
                linha = linha.strip()
                dados = linha.split(':')
                if len(dados) == 2:
                    endereco = dados[0].strip()
                    try:
                        porta = int(dados[1].strip())
                        vizinhos.append((endereco, porta,status))
                    except ValueError:
                        print(f"Erro: Porta inválida na linha: {linha}")
                else:
                    print(f"Erro: Linha mal formatada: {linha}")
    except FileNotFoundError:
        print(f"Erro: Arquivo {vizinhos_file} não encontrado.")
    return vizinhos

def separar_msg(mensagem):
    try:
        partes = mensagem.split(" ")
        if len(partes) < 3:
            raise ValueError("Mensagem mal formatada: faltam partes essenciais.")
        origem = partes[0].split(":")
        if len(origem) != 2:
            raise ValueError("Endereço de origem mal formatado.")
        endereco_origem = origem[0]
        porta_origem = int(origem[1])
        clock_origem = int(partes[1])
        mensagem_tipo = partes[2]
        args = partes[3:] if len(partes) > 3 else []  # args como lista vazia se ausentes
        mensagem_separada = {
            "endereco_origem": endereco_origem,
            "porta_origem": porta_origem,
            "clock_origem": clock_origem,
            "tipo": mensagem_tipo,
            "args": args
        }
        return mensagem_separada
    except ValueError as e:
        print(f"Erro ao separar mensagem: {e}")
        return None  # Retorna None em caso de erro
    except IndexError:
        print("Erro: Mensagem mal formatada.")
        return None
    except Exception as e:
        print(f"Erro inesperado ao separar mensagem: {e}")
        return None

def adiciona_vizinho(peer,endereco,porta,status):
    try:
        peer['vizinhos'].append((endereco, porta, status))
        with open('vizinhos.txt', 'a') as arquivo_vizinhos:
            arquivo_vizinhos.write(f"\n{endereco}:{porta}")
        print(f"Adicionando novo peer {endereco}:{porta} status {status}")
    except Exception as e:
        print(f"Erro ao adicionar vizinho: {e}")

def atualiza_status_vizinho(peer,endereco,porta,status):
    try:
        for i, vizinho in enumerate(peer['vizinhos']):
            if endereco == vizinho[0] and porta == vizinho[1]:
                peer['vizinhos'][i] = (endereco, porta, status)
                print(f"Atualizando peer {endereco}:{porta} status {status}")
                return True
        adiciona_vizinho(peer,endereco,porta,status)
        return True
    except IndexError:
        print("Erro: Vizinho mal formatado na lista de vizinhos.")
        return False
    except Exception as e:
        print(f"Erro inesperado ao atualizar status do vizinho: {e}")
        return False