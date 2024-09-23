package escalonador;

import java.io.BufferedReader;
import java.io.FileReader;
import java.io.IOException;
import java.util.ArrayList;
import java.util.Comparator;
import java.util.List;

public class Escalonador {
    private static final int ESPERA = 5; // Tempo de espera para processos bloqueados
    private static final int EXECUTADOS = 2; // Número de execuções antes de desbloquear
    private int quantum; // Tamanho do quantum
    private int totalInstrucoes = 0, qntQuantum = 0; // Contadores para estatísticas
    private LogWriter writer; // Escritor de logs
    private List<Integer> prioridades = new ArrayList<>(); // Lista de prioridades dos processos
    private List<BCP> prontos = new ArrayList<>(); // Processos prontos para execução
    private List<BCP> finalizados = new ArrayList<>(); // Processos finalizados
    private List<Bloqueado> bloqueados = new ArrayList<>(); // Processos bloqueados

    /**
     * Construtor do Escalonador. Carrega as prioridades, o quantum e os processos prontos a partir dos arquivos.
     *
     * @param caminhoArquivos Caminhos dos arquivos de processo.
     * @param caminhoQuantum Caminho do arquivo que contém o quantum.
     * @param caminhoLogs Caminho do arquivo de log.
     * @param caminhoPrioridades Caminho do arquivo que contém as prioridades.
     * @throws IOException Caso ocorra um erro na leitura dos arquivos.
     */
    public Escalonador(String[] caminhoArquivos, String caminhoQuantum, String caminhoLogs, String caminhoPrioridades) throws IOException {
        carregaPrioridades(caminhoPrioridades);
        carregaQuantum(caminhoQuantum);
        writer = new LogWriter(caminhoLogs, quantum);
        carregaProntos(caminhoArquivos);
        ordenarProntosPorCredito();
    }

    /**
     * Executa o escalonador, processando os processos prontos e bloqueados até que não haja mais.
     *
     * @throws IOException Caso ocorra um erro na escrita do log.
     */
    public void executaEscalonador() throws IOException {
        while (!prontos.isEmpty() || !bloqueados.isEmpty()) {
            executaQuantum();
        }
        writer.writeFile("MEDIA DE TROCAS: " + String.format("%.1f", ((double) qntQuantum / finalizados.size())));
        for (BCP processo : finalizados) totalInstrucoes += processo.getContadorPrograma();
        writer.writeFile("MEDIA DE INTRUCOES: " + String.format("%.1f", ((double) totalInstrucoes / qntQuantum)));
        writer.writeFile("QUANTUM: " + quantum);
    }

    /**
     * Executa um ciclo de quantum para o processo atual, realizando instruções até o quantum ser atingido.
     *
     * @throws IOException Caso ocorra um erro na escrita do log.
     */
    public void executaQuantum() throws IOException {
        boolean continua = true;
        BCP processoAtual = getProcessoAtual(); // Obtém o processo atual
        processoAtual.setEstado("Executando"); // Define o estado como "Executando"
        writer.writeFile("Executando " + processoAtual.getNome());
        qntQuantum++; // Incrementa o contador de quanta executados

        incrementaExecucoesBloqueados(); // Incrementa execuções dos processos bloqueados

        for (int i = 0; i < quantum; i++) {
            if (continua && processoAtual.getCreditos() != 0) {
                continua = executaInstrucao(i); // Executa instrução do processo
            }
            decrementaEsperaBloqueados(); // Decrementa o tempo de espera dos processos bloqueados
        }

        if (continua) {
            processoAtual.setEstado("Pronto"); // Retorna o processo ao estado "Pronto"
            ordenarProntosPorCredito(); // Reordena os prontos por créditos
        }

        if (processoAtual.getCreditos() == 0) { // Se os créditos acabaram
            if (bloqueados.isEmpty()) {
                redistribuiCreditos(); // Redistribui créditos se não há bloqueados
            } else {
                int menorTempo = bloqueados.get(0).getTempoEspera();
                for (Bloqueado bloqueado : bloqueados) {
                    bloqueado.setTempoEspera(bloqueado.getTempoEspera() - menorTempo); // Atualiza tempo de espera
                }
                desbloqueiaProcesso(bloqueados.get(0)); // Desbloqueia o primeiro processo na lista
            }
            ordenarProntosPorCredito(); // Reordena os prontos por créditos
        }
    }

    /**
     * Executa a instrução atual do processo.
     *
     * @param qtdInstrucoes Número de instruções executadas até o momento.
     * @return true se o processo deve continuar, false caso contrário.
     * @throws IOException Caso ocorra um erro na escrita do log.
     */
    public boolean executaInstrucao(int qtdInstrucoes) throws IOException {
        BCP processoAtual = getProcessoAtual();
        String instrucao = processoAtual.getInstrucaoAtual(); // Obtém a instrução atual
        processoAtual.avancarInstrucao(); // Avança o contador de programa
        processoAtual.decrementaCredito(); // Decrementa créditos

        switch (instrucao) {
            case "COM":
                return true; // Continua a execução
            case "E/S":
                if (processoAtual.getContadorPrograma() == 0) {
                    writer.writeFile("E/S iniciada em " + processoAtual.getNome());
                    return true; // Inicia operação de entrada/saída
                }
                writer.writeFile("Interrompendo " + processoAtual.getNome() + " apos " + (qtdInstrucoes + 1) + " instrucoes");
                bloqueiaProcesso(); // Bloqueia o processo atual
                return false;
            case "SAIDA":
                finalizaProcesso(); // Finaliza o processo
                writer.writeFile(processoAtual.getNome() + " terminado. " + processoAtual.valoresFinais());
                return false;
            default:
                // Atualiza registradores X e Y
                if (instrucao.startsWith("X=")) {
                    processoAtual.setRegistradorX(Integer.parseInt(instrucao.substring(2)));
                } else if (instrucao.startsWith("Y=")) {
                    processoAtual.setRegistradorY(Integer.parseInt(instrucao.substring(2)));
                }
                return true;
        }
    }

    /**
     * Redistribui os créditos para todos os processos prontos.
     */
    public void redistribuiCreditos() {
        prontos.forEach(BCP::resetCreditos); // Reseta créditos de todos os processos prontos
    }

    /**
     * Incrementa o contador de execuções dos processos bloqueados e desbloqueia se necessário.
     */
    public void incrementaExecucoesBloqueados() {
        List<Bloqueado> desbloquear = new ArrayList<>(); // Lista temporária para armazenar os bloqueados que serão desbloqueados
    
        for (Bloqueado bloqueado : bloqueados) {
            bloqueado.incrementaExecucoes();  // Incrementa o número de execuções no objeto original
    
            if (bloqueado.getExecucoes() == EXECUTADOS) {
                desbloquear.add(bloqueado);   // Adiciona à lista temporária se atingir o limite
            }
        }
    
        // Depois de iterar, desbloqueia os processos fora do loop original para evitar modificar a lista enquanto itera
        for (Bloqueado bloqueado : desbloquear) {
            desbloqueiaProcesso(bloqueado);  // Desbloqueia os processos que atingiram o limite de execuções
        }
    }

    /**
     * Decrementa o tempo de espera dos processos bloqueados.
     */
    public void decrementaEsperaBloqueados() {
        if (!bloqueados.isEmpty()) {
            for (Bloqueado bloqueado : bloqueados) {
                bloqueado.decrementaTempoEspera(); // Decrementa o tempo de espera
                if (bloqueado.getExecucoes() >= EXECUTADOS) {
                    desbloqueiaProcesso(bloqueado); // Desbloqueia se atingiu o número de execuções
                }
            }
        }
    }

    /**
     * Bloqueia o processo atual e adiciona à lista de bloqueados.
     */
    public void bloqueiaProcesso() {
        BCP processoAtual = getProcessoAtual();
        processoAtual.setEstado("Bloqueado"); // Altera o estado do processo
        bloqueados.add(new Bloqueado(processoAtual, ESPERA, 0)); // Adiciona à lista de bloqueados
        prontos.remove(processoAtual); // Remove da lista de prontos
    }

    /**
     * Desbloqueia um processo bloqueado e o adiciona à lista de prontos.
     *
     * @param bloqueado O processo bloqueado a ser desbloqueado.
     */
    public void desbloqueiaProcesso(Bloqueado bloqueado) {
        BCP processo = bloqueado.getProcessoBCP(); // Obtém o processo do bloqueado
        processo.setEstado("Pronto"); // Altera o estado do processo
        prontos.add(processo); // Adiciona à lista de prontos
        bloqueados.remove(bloqueado); // Remove da lista de bloqueados
    }

    /**
     * Finaliza o processo atual e o move para a lista de finalizados.
     */
    public void finalizaProcesso() {
        BCP atual = getProcessoAtual();
        atual.setEstado("Finalizado"); // Altera o estado do processo
        finalizados.add(atual); // Adiciona à lista de finalizados
        prontos.remove(atual); // Remove da lista de prontos
    }

    /**
     * Ordena os processos prontos por seus créditos em ordem decrescente.
     */
    public void ordenarProntosPorCredito() {
        prontos.sort(Comparator.comparingInt(BCP::getCreditos).reversed()); // Ordena por créditos
    }

    /**
     * Carrega as prioridades a partir do arquivo especificado.
     *
     * @param caminho Caminho do arquivo de prioridades.
     * @throws IOException Caso ocorra um erro na leitura do arquivo.
     */
    public void carregaPrioridades(String caminho) throws IOException {
        BufferedReader br = new BufferedReader(new FileReader(caminho));
        String linha;
        while ((linha = br.readLine()) != null) {
            prioridades.add(Integer.parseInt(linha)); // Adiciona cada prioridade à lista
        }
        br.close(); // Fecha o BufferedReader
    }

    /**
     * Carrega o quantum a partir do arquivo especificado.
     *
     * @param caminho Caminho do arquivo que contém o quantum.
     * @throws IOException Caso ocorra um erro na leitura do arquivo.
     */
    public void carregaQuantum(String caminho) throws IOException {
        BufferedReader br = new BufferedReader(new FileReader(caminho));
        quantum = Integer.parseInt(br.readLine()); // Lê o quantum do arquivo
        br.close(); // Fecha o BufferedReader
    }

    /**
     * Carrega os processos prontos a partir dos arquivos especificados.
     *
     * @param caminhoArquivos Array com os caminhos dos arquivos de processo.
     * @throws IOException Caso ocorra um erro na leitura dos arquivos.
     */
    private void carregaProntos(String[] caminhoArquivos) throws IOException {
        for (int i = 0; i < caminhoArquivos.length; i++) {
            Processo processo = new Processo(caminhoArquivos[i]);
            BCP novoBCP = new BCP(processo, prioridades.get(i));
            prontos.add(novoBCP);
            writer.writeFile("Carregando " + processo.getNomeProcesso());
        }
    }

    /**
     * Obtém o primeiro processo na fila de prontos.
     *
     * @return O processo atual.
     */
    public BCP getProcessoAtual() {
        return prontos.get(0); // Retorna o primeiro processo da lista de prontos
    }
    
    // Getters para acessar as listas e propriedades
    public List<BCP> getProntos() {
        return prontos; // Retorna a lista de processos prontos
    }

    public List<BCP> getFinalizados() {
        return finalizados; // Retorna a lista de processos finalizados
    }

    public List<Bloqueado> getBloqueados() {
        return bloqueados; // Retorna a lista de processos bloqueados
    }

    public int getQuantum() {
        return quantum; // Retorna o quantum
    }

    public List<Integer> getPrioridades() {
        return prioridades; // Retorna a lista de prioridades
    }
}
