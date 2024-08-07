#include <stdio.h>
#include <stdlib.h>
#include <string.h>

#define MAX_REG 100
#define MAX_CHAR 255

typedef struct registro {
    int id;
    char nome[MAX_CHAR];
    char local[MAX_CHAR];
    int status;
} REGISTRO;

// Função de comparação usada pelo qsort
int compare(const void *a, const void *b) {
    REGISTRO *regA = (REGISTRO *)a;
    REGISTRO *regB = (REGISTRO *)b;
    return regA->id - regB->id;
}

int main() {
    REGISTRO tabela[MAX_REG];
    int count = 0;
    FILE *arquivo = fopen("entrada.txt", "r");
    if (arquivo == NULL) {
        perror("Falha ao abrir o arquivo de entrada");
        return 1;
    }

    FILE *arquivoSaida = fopen("saida.txt", "w");
    if (arquivoSaida == NULL) {
        fclose(arquivo);
        perror("Falha ao criar o arquivo de saída");
        return 2;
    }

    // Lendo os dados do arquivo
    while (fscanf(arquivo, "%d %254s %254s %d", &tabela[count].id, tabela[count].nome, tabela[count].local, &tabela[count].status) == 4) {
        if (++count >= MAX_REG) break;
    }

    // Ordenando os registros por id
    qsort(tabela, count, sizeof(REGISTRO), compare);

    // Escrevendo os registros ordenados no arquivo de saída
    for (int i = 0; i < count; i++) {
        fprintf(arquivoSaida, "%d %s %s %d\n", tabela[i].id, tabela[i].nome, tabela[i].local, tabela[i].status);
    }

    fclose(arquivo);
    fclose(arquivoSaida);

    return 0;
}
