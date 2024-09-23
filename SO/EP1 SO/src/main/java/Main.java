import escalonador.Escalonador;

import java.io.IOException; 

public class Main {
    public static void main(String[] args) {
        try {
            // Caminho absoluto para os arquivos em 'resources/programas'
            String basePath = System.getProperty("user.dir")+"/resources/";
    
            // Caminhos completos para os arquivos usando basePath
            String[] caminhoArquivos = {
                basePath + "programas/01.txt",
                basePath + "programas/02.txt",
                basePath + "programas/04.txt",
                basePath + "programas/05.txt",
                basePath + "programas/06.txt",
                basePath + "programas/07.txt",
                basePath + "programas/08.txt",
                basePath + "programas/09.txt",
                basePath + "programas/10.txt"
            };
            String caminhoQuantum = basePath + "programas/quantum.txt";
            String caminhoLogs = basePath + "logs/";
            String caminhoPrioridades = basePath + "programas/prioridades.txt";
    
            // Instanciando o escalonador com os caminhos absolutos
            Escalonador escalonador = new Escalonador(caminhoArquivos, caminhoQuantum, caminhoLogs, caminhoPrioridades);
            escalonador.executaEscalonador();
        } catch (IOException e) {
            System.err.println("Erro ao carregar o escalonador: " + e.getMessage());
        }
    }
    
}
