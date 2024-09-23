package escalonador;

import java.io.BufferedReader;
import java.io.FileReader;
import java.io.IOException;
import java.util.ArrayList;
import java.util.List;

/**
 * Classe que representa um processo a ser executado no escalonador.
 * Um processo é carregado de um arquivo de texto que contém o nome e as instruções.
 */
public class Processo {
    private String nomeProcesso;  // Nome do processo (primeira linha do arquivo)
    private String[] instrucoes;  // Instruções do processo (linhas restantes do arquivo)

    /**
     * Construtor da classe Processo. 
     * Ele carrega o processo a partir do caminho de um arquivo de texto especificado.
     * 
     * @param caminhoArquivo Caminho do arquivo de texto que contém o processo.
     * @throws IOException Caso ocorra um erro de leitura do arquivo.
     */
    public Processo(String caminhoArquivo) throws IOException {
        carregarProcesso(caminhoArquivo);  // Inicializa o processo carregando suas instruções a partir do arquivo
    }

    /**
     * Método privado que carrega o nome do processo (a primeira linha do arquivo)
     * e suas instruções (o restante das linhas) de um arquivo de texto para o Objeto Processo.
     * 
     * @param caminhoArquivo Caminho do arquivo de texto que contém o processo.
     * @throws IOException Caso ocorra um erro de leitura do arquivo.
     */
    private void carregarProcesso(String caminhoArquivo) throws IOException {
        BufferedReader leitor = new BufferedReader(new FileReader(caminhoArquivo));  // Abre o arquivo para leitura
        List<String> linhas = new ArrayList<>();  // Armazena temporariamente todas as linhas do arquivo
        String linha;  // Variável temporária para armazenar cada linha do arquivo

        // Lê todas as linhas do arquivo e as adiciona à lista
        while ((linha = leitor.readLine()) != null) {
            linhas.add(linha);  
        }
        leitor.close();  // Fecha o leitor de arquivos após a leitura

        nomeProcesso = linhas.get(0);  // Define a primeira linha como o nome do processo
        instrucoes = linhas.subList(1, linhas.size()).toArray(new String[0]);  // As demais linhas são as instruções
    }

    /**
     * Método que retorna o nome do processo.
     * 
     * @return Nome do processo (primeira linha do arquivo).
     */
    public String getNomeProcesso() {
        return nomeProcesso;  // Retorna o nome do processo
    }

    /**
     * Método que retorna as instruções do processo.
     * 
     * @return Array de strings contendo as instruções do processo.
     */
    public String[] getInstrucoes() {
        return instrucoes;  // Retorna as instruções do processo
    }
}
