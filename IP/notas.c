#include <stdio.h>
#include "notas.h"

#define MAX_TAM 100
#define MAX_ALUNOS 60
#define MAX_NOTAS 2
static char* nomes[MAX_ALUNOS];
static float notas[MAX_ALUNOS][MAX_NOTAS];
static float medias[MAX_NOTAS];

static int notasRegistradas[MAX_ALUNOS];
static int totalAlunos = 0;

void adicionarAluno(char* nome){
	if (totalAlunos < MAX_ALUNOS) {
        nomes[totalAlunos++] = nome;
    } else {
        printf("Erro: Limite máximo de alunos atingido.\n");
    }
}

void adicionarNota(int index, float nota) {
    if (notasRegistradas[index] < MAX_NOTAS) {
        notas[index][notasRegistradas[index]++] = nota;
    } else {
        printf("Erro: Limite máximo de notas do aluno atingido.\n");
    }
}

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

void listarMedias(){
	printf("Medias---------------------\n");
	for(int i = 0; i < totalAlunos; i++){
		printf("%10s: %6.2f\n",nomes[i], medias[i]);
	}
	
}

