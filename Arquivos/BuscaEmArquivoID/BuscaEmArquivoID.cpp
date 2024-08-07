#include <stdio.h>
#include <stdlib.h>
#include <string.h>

#define MAX_LENGTH 50

typedef struct {
    int id;
    char nome[MAX_LENGTH];
    char cidade[MAX_LENGTH];
    int status;
} REGISTRO;

REGISTRO busca(FILE *arquivo, int id) {
    REGISTRO r;
    while (fread(&r, sizeof(REGISTRO), 1, arquivo)) {
        if (r.id == id) {
            return r;
        }
    }
    // Se o registro não for encontrado, retorna um registro com ID -1
    r.id = -1;
    return r;
}

int main() {
    FILE *arquivo;
    REGISTRO resultado;
    int id;

    // Abre o arquivo de entrada para leitura
    arquivo = fopen("entrada.txt", "rb");
    if (arquivo == NULL) {
        perror("Erro ao abrir arquivo de entrada");
        return 1;
    }

    // Lê o ID fornecido pelo usuário
    printf("Digite o ID a ser buscado: ");
    scanf("%d", &id);

    // Realiza a busca no arquivo de entrada
    resultado = busca(arquivo, id);

    // Verifica se o registro foi encontrado
    if (resultado.id != -1) {
        printf("Registro encontrado:\n");
        printf("ID: %d\n", resultado.id);
        printf("Nome: %s\n", resultado.nome);
        printf("Cidade: %s\n", resultado.cidade);
        printf("Status: %d\n", resultado.status);
    } else {
        printf("Registro com ID %d não encontrado.\n", id);
    }

    // Fecha o arquivo
    fclose(arquivo);

    return 0;
}
