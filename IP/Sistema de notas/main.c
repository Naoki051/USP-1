#include <stdio.h>
#include "notas.h"

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