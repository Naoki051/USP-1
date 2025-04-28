import threading,server,client

data = {
    "ip": "127.0.0.1",
    "port": 9000,
    "clock": 0,
    "files_path":'./arquivos',
    'vizinhos': []
}


def teste_connexao():
    """ Servidor escuta e espera conexão se cliente enviar sair desconecta """
    thread_client = threading.Thread(target=client.cliente,args=(data,0,"SAIR"))
    thread_server = threading.Thread(target=server.servidor,args=(data,))

    thread_server.start()
    thread_client.start()
    
    thread_server.join()
    thread_client.join()

# teste_connexao()

def teste_dict_vizinhos():
    """ Armazena os dados do txt em um dict {ip, port, status} """
    vizinhos = client.dict_vizinhos()
    for vizinho in vizinhos:
        print(vizinho)

# teste_dict_vizinhos()

def teste_separar_msg():
    print(client.separar_msg("127.0.0.1:9000 1 HELLO")) 

# teste_separar_msg()

def teste_juntar_msg():
    print(client.juntar_msg(data,"HELLO","NONE"))

# teste_juntar_msg()

def teste_jutar_e_separar():
    mensagem = "127.0.0.1:9000 1 HELLO ARG1"
    mensagem = client.separar_msg(mensagem)
    print(mensagem)
    mensagem = client.juntar_msg(data,mensagem['tipo'],mensagem['args'])
    print(mensagem)
    mensagem = client.separar_msg(mensagem)
    print(mensagem)

# teste_jutar_e_separar()

def teste_incrementar_clk():
    client.incrementa_clock(data,"127.0.0.1:9000 5 HELLO ARG1")
    print(data["clock"])

# teste_incrementar_clk()

def teste_listar_vizinhos():
    data['vizinhos'] = client.dict_vizinhos()
    client.listar_vizinhos(data)

# teste_listar_vizinhos()

def teste_listar_arquivos():
    client.listar_arquivos(data)

# teste_listar_arquivos()

def teste_atualiza_status_vizinho():
    server.atualizar_status_vizinho(data,"127.0.0.1",9009,"ONLINE")

# teste_atualiza_status_vizinho()

def teste_adiciona_vizinho():
    data["vizinhos"] = client.dict_vizinhos()
    mensagem = "127.0.0.1:9001 8 PEER_LIST 4 127.0.0.1:9002:OFFLINE:0 127.0.0.1:9006:ONLINE:0 127.0.0.1:9043:ONLINE:0 127.0.0.1:9021:OFFLINE:0" 
    partes = client.separar_msg(mensagem)
    client.atualizar_vizinhos(data, partes['args'])

# teste_adiciona_vizinho()
