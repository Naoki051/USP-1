def incrementa_clock(peer,msg_clock = 0):
    """
    Incrementa o clock lógico do peer e imprime o novo valor.
    """
    peer['clock'] = max(msg_clock,peer['clock']) +1
    print(f"=> Atualizando relogio para {peer['clock']}") 
    return

def separar_msg(mensagem):
    """
    Separa uma mensagem recebida em suas partes componentes que serão interpretadas.
    """
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

def adiciona_vizinho(peer,endereco,porta,status,clock):
    """
    Adiciona um novo vizinho à lista de vizinhos do peer e ao arquivo de vizinhos.
    """
    try:
        peer['vizinhos'].append((endereco, porta, status, clock))
        with open(peer['vizinhos_file'], 'a') as arquivo_vizinhos:
            arquivo_vizinhos.write(f"\n{endereco}:{porta}")
        print(f"Adicionando novo peer {endereco}:{porta} status {status}")
    except Exception as e:
        print(f"Erro ao adicionar vizinho: {e}")

def atualiza_status_vizinho(peer,endereco,porta,status,clock=0):
    """
    Atualiza o status de um vizinho existente na lista de vizinhos do peer.
    Se o vizinho não existir, ele é adicionado à lista.
    """
    try:
        for i, vizinho in enumerate(peer['vizinhos']):
            if endereco == vizinho[0] and porta == vizinho[1]:
                clock = max (vizinho[3],clock)
                peer['vizinhos'][i] = (endereco, porta, status, clock)
                if vizinho[2] != status:
                    print(f"Atualizando peer {endereco}:{porta} status {status}")
                return True
        adiciona_vizinho(peer,endereco,porta,status,clock)
        return True
    except IndexError:
        print("Erro: Vizinho mal formatado na lista de vizinhos.")
        return False
    except Exception as e:
        print(f"Erro inesperado ao atualizar status do vizinho: {e}")
        return False
    
def vizinhos_txt_to_list(vizinhos_file='vizinhos.txt'):
    """
    Lê um arquivo de texto contendo informações de vizinhos e retorna uma lista de tuplas.
    O arquivo deve ter uma linha por vizinho, no formato "endereco:porta".
    """
    vizinhos = []
    try:
        with open(vizinhos_file, 'r', encoding='utf-8') as arquivo:
            for linha in arquivo:
                linha = linha.strip()
                dados = linha.split(':')
                if len(dados) == 2:
                    endereco = dados[0].strip()
                    try:
                        porta = int(dados[1].strip())
                        vizinhos.append((endereco, porta,'OFFLINE',0))
                    except ValueError:
                        print(f"Erro: Porta inválida na linha: {linha}")
                else:
                    print(f"Erro: Linha mal formatada: {linha}")
    except FileNotFoundError:
        print(f"Erro: Arquivo {vizinhos_file} não encontrado.")
    return vizinhos