package escalonador;

/**
 * Classe que representa um processo bloqueado no escalonador.
 * Contém informações sobre o processo, tempo de espera e contagem de execuções.
 */
public class Bloqueado {
    private BCP processoBCP;  // Controle do Processo em Bloqueio (BCP)
    private int tempoEspera;   // Tempo que o processo está bloqueado
    private int execucoes;     // Número de execuções do processo

    /**
     * Construtor da classe Bloqueado que inicializa os atributos do objeto.
     * 
     * @param processoBCP O BCP do processo bloqueado.
     * @param tempoEspera Tempo de espera inicial do processo.
     * @param execucoes Número de execuções do processo.
     */
    public Bloqueado(BCP processoBCP, int tempoEspera, int execucoes) {
        this.tempoEspera = tempoEspera;  // Define o tempo de espera
        this.processoBCP = processoBCP;  // Inicializa o BCP do processo
        this.execucoes = execucoes;       // Inicializa a contagem de execuções
    }

    /**
     * Atualiza o tempo de espera do processo.
     * 
     * @param t Novo valor do tempo de espera.
     */
    public void setTempoEspera(int t) {
        tempoEspera = t;  // Define um novo valor para o tempo de espera
    }

    /**
     * Decrementa o tempo de espera em um.
     */
    public void decrementaTempoEspera() {
        this.tempoEspera--;  // Reduz o tempo de espera em um
    }

    /**
     * Incrementa o número de execuções do processo.
     */
    public void incrementaExecucoes() {
        execucoes++;  // Aumenta a contagem de execuções em um
    }

    /**
     * Retorna o número de execuções do processo.
     * 
     * @return Número de execuções.
     */
    public int getExecucoes() {
        return execucoes;  // Retorna o total de execuções
    }

    /**
     * Retorna o BCP do processo bloqueado.
     * 
     * @return O BCP associado ao processo.
     */
    public BCP getProcessoBCP() {
        return processoBCP;  // Retorna o BCP do processo
    }

    /**
     * Retorna o tempo de espera do processo.
     * 
     * @return Tempo de espera atual.
     */
    public int getTempoEspera() {
        return tempoEspera;  // Retorna o tempo de espera do processo
    }
}
