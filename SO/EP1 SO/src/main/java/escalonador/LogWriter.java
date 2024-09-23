package escalonador;

import java.io.BufferedWriter;
import java.io.FileWriter;
import java.io.IOException;

/**
 * Classe responsável por escrever logs em arquivos de texto. 
 * Cada instância da classe cria ou edita um arquivo de log específico para o quantum fornecido.
 */
public class LogWriter {

	private String caminhoArquivo;  // Caminho completo do arquivo de log

	/**
	 * Construtor que recebe o caminho do diretório e o número do quantum para nomear o arquivo.
	 * 
	 * @param caminhoArquivo Caminho do diretório onde o arquivo será criado/editado.
	 * @param quantum Número do quantum que será usado para nomear o arquivo de log.
	 */
	public LogWriter(String caminhoArquivo, int quantum) {
		String s_quantum = "/log" + String.format("%02d", quantum) + ".txt";  // Formata o nome do arquivo com base no quantum
		this.caminhoArquivo = caminhoArquivo + s_quantum;  // Define o caminho completo do arquivo
	}

	/**
	 * Escreve uma String no arquivo de log correspondente ao objeto. 
	 * Se o arquivo já existir, o conteúdo é adicionado ao final.
	 * 
	 * @param inputString Texto que será escrito no arquivo.
	 * @throws IOException Caso ocorra algum erro durante a escrita do arquivo.
	 */
	public void writeFile(String inputString) throws IOException {
		FileWriter fileWriter = new FileWriter(caminhoArquivo, true);  // Abre o arquivo em modo de adição
		BufferedWriter writer = new BufferedWriter(fileWriter);  // Usa BufferedWriter para escrita eficiente

		writer.write(inputString);  // Escreve a string no arquivo
		writer.newLine();  // Adiciona uma nova linha após o conteúdo

		writer.close();  // Fecha o writer após a escrita
	}

	/**
	 * Retorna o caminho completo do arquivo de log.
	 * 
	 * @return String representando o caminho do arquivo.
	 */
	@Override
	public String toString() {
		return this.caminhoArquivo;  // Retorna o caminho do arquivo de log
	}
}
