package escalonador;

/**
 * Classe BCP (Bloco de Controle de Processos).
 * Contém todas as informações necessárias para controlar a execução de um processo.
 */
public class BCP {
    private Processo processo;  // Processo associado ao BCP
    private int contadorPrograma; // Contador de programa, indica a próxima instrução a ser executada
    private String estado; // Estado do processo (Pronto, Executando, Bloqueado)
    private int prioridade; // Prioridade do processo
    private int creditos; // Número de créditos do processo
    private int registradorX; // Valor do registrador X
    private int registradorY; // Valor do registrador Y

    /**
     * Construtor do BCP. Inicializa o bloco de controle de processo com as informações fornecidas.
     * 
     * @param processo O processo que será armazenado.
     * @param prioridade A prioridade do processo e quantidade de créditos inicial.
     */
    public BCP(Processo processo, int prioridade) {
        this.processo = processo; // Define o processo (nome e instruções)
        this.prioridade = prioridade; // Define a prioridade do processo
        this.creditos = prioridade; // Define o número inicial de créditos do processo
        this.contadorPrograma = 0; // Inicializa o contador de programa no início (0)
        this.estado = "Pronto"; // O processo começa no estado "Pronto"
        this.registradorX = 0; // Inicializa o registrador X com valor 0
        this.registradorY = 0; // Inicializa o registrador Y com valor 0
    }

    /**
     * Retorna o processo associado ao BCP.
     * 
     * @return O processo.
     */
    public Processo getProcesso() {
        return processo; // Retorna o processo associado
    }

    /**
     * Retorna o nome do processo.
     * 
     * @return O nome do processo.
     */
    public String getNome() {
        return processo.getNomeProcesso(); // Retorna o nome do processo
    }

    /**
     * Retorna o estado atual do processo.
     * 
     * @return O estado do processo.
     */
    public String getEstado() {
        return estado; // Retorna o estado do processo
    }

    /**
     * Define o estado atual do processo.
     * 
     * @param estado O novo estado do processo.
     */
    public void setEstado(String estado) {
        this.estado = estado; // Atualiza o estado do processo
    }

    /**
     * Retorna o contador de programa (próxima instrução a ser executada).
     * 
     * @return O valor do contador de programa.
     */
    public int getContadorPrograma() {
        return contadorPrograma; // Retorna o contador de programa
    }

    /**
     * Atualiza o valor do contador de programa.
     * 
     * @param contador O novo valor do contador de programa.
     */
    // Método ausente, por favor insira aqui o método de atualização do contador de programa

    /**
     * Retorna o valor do registrador X.
     * 
     * @return O valor do registrador X.
     */
    public int getRegistradorX() {
        return registradorX; // Retorna o valor do registrador X
    }

    /**
     * Define o valor do registrador X.
     * 
     * @param valor O valor a ser atribuído ao registrador X.
     */
    public void setRegistradorX(int valor) {
        this.registradorX = valor; // Atualiza o valor do registrador X
    }

    /**
     * Retorna o valor do registrador Y.
     * 
     * @return O valor do registrador Y.
     */
    public int getRegistradorY() {
        return registradorY; // Retorna o valor do registrador Y
    }

    /**
     * Define o valor do registrador Y.
     * 
     * @param valor O valor a ser atribuído ao registrador Y.
     */
    public void setRegistradorY(int valor) {
        this.registradorY = valor; // Atualiza o valor do registrador Y
    }

    /**
     * Retorna a prioridade do processo.
     * 
     * @return A prioridade do processo.
     */
    public int getPrioridade() {
        return prioridade; // Retorna a prioridade do processo
    }

    /**
     * Retorna o número de créditos do processo.
     * 
     * @return O número de créditos do processo.
     */
    public int getCreditos() {
        return creditos; // Retorna o número de créditos do processo
    }

    /**
     * Atualiza o número de créditos do processo para o valor inicial.
     */
    public void resetCreditos() {
        this.creditos = this.prioridade; // Reinicia os créditos para o valor da prioridade
    }

    /**
     * Retorna a instrução atual a ser executada pelo processo.
     * 
     * @return A instrução atual, baseada no contador de programa.
     */
    public String getInstrucaoAtual() {
        if (contadorPrograma < processo.getInstrucoes().length) {
            return processo.getInstrucoes()[contadorPrograma]; // Retorna a próxima instrução
        } else {
            return "SAIDA"; // Retorna "SAIDA" se todas as instruções tiverem sido executadas
        }
    }

    /**
     * Avança o contador de programa para a próxima instrução.
     */
    public void avancarInstrucao() {
        contadorPrograma++; // Incrementa o contador de programa
    }

    /**
     * Decrementa o número de créditos do processo em um.
     */
    public void decrementaCredito() {
        creditos--; // Reduz o número de créditos
    }

    /**
     * Retorna uma representação em string dos valores finais do processo (usada na saída de log).
     * 
     * @return Uma string com os valores finais de X e Y.
     */
    public String valoresFinais() {
        return "X=" + registradorX + ". Y=" + registradorY; // Retorna os valores finais dos registradores
    }

    /**
     * Retorna uma representação em string do processo, com nome e estado.
     * 
     * @return Uma string contendo o nome e o estado do processo.
     */
    @Override
    public String toString() {
        return "Processo: " + processo.getNomeProcesso() + " | Estado: " + estado + " | Créditos: " + creditos; // Retorna representação do processo
    }
}
