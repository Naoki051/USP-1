Sistema de notas
1. Descrição do Projeto
Apresentar conceitos básicos da programação em C, declaração e atribuição de valor para variáveis, condicionais, funções e laço de repetição.
2. Objetivos
* Armazenar Notas: Permitir a inserção e armazenamento de alunos e notas de alunos. 
* Gerenciamento de Notas: Facilitar a listagem dos alunos e das notas armazenadas. 
* Cálculos: Calcular e exibir a média de todos os alunos.
3. Requisitos do Sistema
Detalhamento do software e hardware utilizado, exemplo Compilador de C e sistemas operacionais compatíveis (Windows, Linux e macOS).
4. Estrutura do Projeto
/NomeProjeto 
main.c         // Arquivo principal contendo o fluxo do programa. 
notas.c         // Implementação das funções de gerenciamento.
notas.h         // Declarações de funções e estruturas de dados. 
README.md        // Documentação do projeto.
Compilação:
gcc -o sistema main.c notas.c
Execução:
./sistema
ou
sistema
5. Funcionalidades Principais
5.1 Adicionar aluno
Descrição: Adiciona um novo aluno ao sistema.
Assinatura: void adicionarAluno(char* nome);
Parâmetros: 
nome: nome do aluno. 
5.2 Adiciona nota
Descrição: Adiciona a nota do aluno ao sistema.
Assinatura: void adicionarNota(int index, float nota);
Parâmetros: 
index: índice do aluno correspondente a nota a ser adicionada.
nota: valor da nota a ser adicionada.
5.3 Listar notas
Descrição: Exibe os nomes e as notas dos alunos.
Assinatura: void listarNotas();
5.4 Calcular média
Descrição: Calcula a média de todos os alunos.
Assinatura: void calcularMedias();
5.5 Listar médias
Descrição: Exibe os nomes e as médias dos alunos.
Assinatura: void listarMedias();
6. Detalhamento das Funções
6.1 Adicionar aluno
Descrição: Insere um novo aluno no vetor de nomes respeitando o limite máximo de alunos.
Implementação:
void adicionarAluno(char* nome){
    if (totalAlunos < MAX_ALUNOS) {
        nomes[totalAlunos++] = nome;
    } else {
        printf("Erro: Limite máximo de alunos atingido.\n");
    }
}


6.2 Adiciona nota
Descrição: Insere a nota de um aluno na matriz de notas utilizando o índice do aluno na matriz de nomes e respeitando o limite máximo de notas.
Implementação: 
void adicionarNota(int index, float nota) {
    if (notasRegistradas[index] < MAX_NOTAS) {
        notas[index][notasRegistradas[index]++] = nota;
    } else {
        printf("Erro: Limite máximo de notas do aluno atingido.\n");
    }
}
6.3 Listar notas
Descrição: Exibe os nomes dos alunos, percorrendo o vetor de nomes, e as respectivas notas, percorrendo a matriz de notas.
Implementação:
void listarNotas() {
    printf("Notas----------------------\n");
    for (int i = 0; i < totalAlunos; i++) {
        printf("%-10s:",nomes[i]);
        for(int j = 0;j < notasRegistradas[i];j++){
            printf(" %6.2f",notas[i][j]);
        }
        printf("\n");
    }
}
6.4 Calcular média
Descrição: Percorre a matriz de notas, considerando o total de alunos inseridos e a quantidade de notas registradas para evitar dados inválidos, e calcula a média das notas considerando MAX_NOTAS como o total de provas aplicadas.
Implementação: 
void calcularMedias() {
    float soma = 0.0;
    for(int i = 0; i < totalAlunos; i++){
        for (int j = 0; j < notasRegistradas[i]; j++) {
            soma += notas[i][j];
        }
        medias[i] = soma/MAX_NOTAS;
        soma = 0;
    }
}
6.5 Listar médias
Descrição: Exibe os nomes e as médias dos alunos a partir dos vetores de nomes e de médias.
Implementação:
void listarMedias(){
    printf("Medias---------------------\n");
    for(int i = 0; i < totalAlunos; i++){
        printf("%10s: %6.2f\n",nomes[i], medias[i]);
    }
   
}
7. Exemplos de Uso
int main() {
    adicionarAluno("Alan");
    adicionarAluno("Darlan");
    adicionarAluno("Bruno");
    adicionarNota(0,9.0);
    adicionarNota(0,8.3);
    adicionarNota(1,9.3);

    listarNotas();

    calcularMedias();
   
    listarMedias();

    return 0;
}
8. Considerações Finais
Este projeto serve como uma introdução prática à linguagem C, abordando conceitos como manipulação de arrays, matrizes, funções e controle de fluxo. Futuras melhorias podem incluir persistência de dados em arquivos, interface gráfica e suporte a múltiplas turmas de alunos.