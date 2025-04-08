# Projeto P2P de Compartilhamento de Arquivos

Este projeto implementa um sistema P2P (peer-to-peer) para compartilhamento de arquivos, permitindo que os usuários compartilhem e baixem arquivos diretamente de outros peers na rede.

## Funcionalidades Principais

- **Listagem de Peers:** Permite visualizar a lista de peers conectados à rede, incluindo seus endereços, portas e status.
- **Obtenção de Peers:** Solicita a lista de peers de todos os vizinhos conhecidos, expandindo a rede.
- **Listagem de Arquivos Locais:** Exibe os arquivos disponíveis para compartilhamento no diretório local do peer.
- **Busca de Arquivos:** Permite buscar arquivos específicos na rede P2P.
- **Exibição de Estatísticas:** Mostra informações sobre o desempenho e o status da rede P2P.
- **Alteração do Tamanho do Chunk:** Permite ajustar o tamanho dos chunks usados para transferência de arquivos.
- **Conexão e Comunicação com Peers:** Estabelece conexões com outros peers para compartilhar e baixar arquivos.
- **Atualização de Status de Vizinhos:** Mantém o status dos vizinhos atualizado (online/offline).
- **Gerenciamento de Vizinhos:** Permite adicionar e remover vizinhos da lista de peers conhecidos.
- **Clock Lógico:** Implementa um clock lógico para ordenar eventos e garantir a consistência da rede.
- **Tratamento de Mensagens:** Processa mensagens recebidas de outros peers e executa ações apropriadas.
- **Validação de Dados:** Valida dados de entrada, como endereços, portas e caminhos de arquivos/diretórios.
- **Tratamento de Erros:** Implementa tratamento de erros robusto para lidar com exceções e garantir a estabilidade do sistema.
- **Inicialização do Peer:** Configura o peer com endereço, porta, lista de vizinhos e diretório compartilhado.
- **Threads para Servidor e Cliente:** Utiliza threads para executar o servidor e o cliente do peer simultaneamente.

## Arquivos Principais

- **`eachare.py`:** Contém a implementação principal do sistema P2P, incluindo as funções para inicialização do peer, comunicação com outros peers, gerenciamento de vizinhos e tratamento de mensagens.
- **`vizinhos.txt`:** Arquivo de texto contendo a lista inicial de vizinhos conhecidos pelo peer.
- **`arquivos`:** Diretório contendo arquivos que podem ser compartilhados entre os peers vizinhos
- **`Peer2Peer/tests/test_client.py`:** Contém testes unitários para o módulo do cliente.
- **`Peer2Peer/tests/test_server.py`:** Contém testes unitários para o módulo do servidor.
- **`Peer2Peer/tests/test_integration.py`:** Contém testes de integração para testar a interação entre o cliente e o servidor.
- **`Peer2Peer/tests/test_utils.py`:** Contém testes unitários para funções utilitárias.

## Como Executar

1.  Navegue até o diretório do projeto:

    ```bash
    cd <nome_do_diretório>
    ```

2.  Execute o script principal:

    ```bash
    python eachare.py <endereço>:<porta> <vizinhos.txt> <diretório_compartilhado>
    ```

    - `<endereço>`: Endereço IP do peer.
    - `<porta>`: Porta do peer.
    - `<vizinhos.txt>`: Caminho para o arquivo de texto com a lista de vizinhos.
    - `<diretório_compartilhado>`: Caminho para o diretório compartilhado do peer.

## Testes

Este projeto inclui testes unitários e de integração para garantir a qualidade e a estabilidade do sistema. Os testes são escritos usando o framework `unittest` do Python, com auxílio das bibliotecas `tempfile` e `unittest.mock`.

### Execução dos Testes

Para executar a suíte de testes completa, posicione-se no diretório raiz do projeto e execute o seguinte comando:

```bash
python -m unittest discover tests
```


Este comando instrui o `unittest` a descobrir e executar todos os testes presentes nos arquivos localizados no diretório `tests`.

### Execução de Testes Isolados

Para a execução de testes específicos, utilize o seguinte comando, substituindo `arquivo_teste_desejado.py` pelo nome do arquivo de teste desejado:

```bash
python -m unittest discover tests arquivo_teste_desejado.py
```

Este comando permite a execução de um subconjunto de testes, facilitando a depuração e o desenvolvimento iterativo.

### Estrutura dos Testes

- **`tests/test_client.py`:** Testa a funcionalidade do cliente, incluindo a conexão com outros peers e o envio de mensagens.
- **`tests/test_server.py`:** Testa a funcionalidade do servidor, incluindo o recebimento de conexões e o processamento de mensagens.
- **`tests/test_integration.py`:** Testa a interação entre o cliente e o servidor, simulando cenários de uso real.
- **`tests/test_utils.py`:** Testa funções utilitárias usadas em todo o projeto, como validação de dados e formatação de mensagens.

## Dependências

- `python` (versão 3.6 ou superior)
- `os` (módulo padrão do Python)
- `socket` (módulo padrão do Python)
- `threading` (módulo padrão do Python)
- `sys` (módulo padrão do Python)
- `tempfile` (módulo padrão do Python)
- `time` (módulo padrão do Python)
- `unittest` (módulo padrão do Python)
- `unittest.mock` (módulo padrão do Python)
````
