#include <stdio.h>
#include <stdlib.h>

typedef struct estr {
  int adj; // elemento do caminho
  struct estr *prox;
} NO;

NO *insereInicio(NO *lista, int valor);
void liberaLista(NO *lista);
void dfs(int atual, int fim, int *visitado, int dinheiroAtual, int *melhorSaldo, NO **resp, NO *caminhoAtual, int **grafo, int *ganhos, int N);
NO *caminho(int N, int A, int ijpeso[], int ganhos[], int inicio, int fim, int* dinheiro);

NO *insereInicio(NO *lista, int valor) {
  NO *novo = (NO *)malloc(sizeof(NO));
  if (!novo)
    return NULL;
  novo->adj = valor;
  novo->prox = lista;
  return novo;
}

void liberaLista(NO *lista) {
  NO *aux;
  while (lista) {
    aux = lista;
    lista = lista->prox;
    free(aux);
  }
}

void imprimirLista(NO *lista) {
  if (!lista)
    printf("null");
  while (lista) {
    printf("%d ", lista->adj);
    lista = lista->prox;
  }
  printf("\n");
}

void dfs(int atual, int fim, int *visitado, int dinheiroAtual, int *melhorSaldo, NO **resp, NO *caminhoAtual, int **grafo, int *ganhos, int N) {
  if (visitado[atual]) return;
  visitado[atual] = 1;
  dinheiroAtual += ganhos[atual-1];
  caminhoAtual = insereInicio(caminhoAtual, atual);
  if (atual == fim) {
    if (dinheiroAtual > *melhorSaldo) {
      *melhorSaldo = dinheiroAtual;
      //Reescreve o melhor caminho
      liberaLista(*resp);
      *resp = NULL;
      NO *tmp = caminhoAtual;
      while (tmp) {
        *resp = insereInicio(*resp, tmp->adj);
        tmp = tmp->prox;
      }
    }
  } else {
    for (int i = 1; i <= N; ++i) {
      if (grafo[atual][i] && dinheiroAtual - grafo[atual][i] >= 0) {
        dfs(i, fim, visitado, dinheiroAtual - grafo[atual][i], melhorSaldo,
            resp, caminhoAtual, grafo, ganhos, N);
      }
    }
  }
  visitado[atual] = 0;
  NO *temp = caminhoAtual;
  caminhoAtual = caminhoAtual->prox;
  free(temp);
}

NO *caminho(int N, int A, int ijpeso[], int ganhos[], int inicio, int fim, int* dinheiro){
  int **grafo = (int **)calloc(N + 1, sizeof(int *));
  
  for (int i = 0; i <= N; i++) {
    grafo[i] = (int *)calloc(N + 1, sizeof(int));
  }
  
  for (int i = 0; i < A; i++) {
    int u = ijpeso[3 * i];
    int v = ijpeso[3 * i + 1];
    int peso = ijpeso[3 * i + 2];
    grafo[u][v] = peso;
  }
  
  NO *resp = NULL;
  int *visitado = (int *)calloc(N + 1, sizeof(int));
  int melhorSaldo = -1;

  dfs(inicio, fim, visitado, *dinheiro, &melhorSaldo, &resp, NULL, grafo, ganhos, N);
  for (int i = 0; i <= N; i++) free(grafo[i]);
  free(grafo);
  free(visitado);
  return resp;
}

int main() {
  int N = 4;
  int ganhos[] = {10, 400, 5, 10};
  int A = 6;
  int ijpeso[] = {1, 3, 15, 1, 2, 10, 
                  1, 4,  5, 2, 3, 10, 
                  4, 2,  5, 4, 3,  5};
  int inicio = 1;
  int fim = 3;
  int dinheiroInicial = 20;
  NO *resultado = caminho(N, A, ijpeso, ganhos, inicio, fim, &dinheiroInicial);

  printf("Caminho com o melhor saldo:\n");
  imprimirLista(resultado);
  liberaLista(resultado);

  return 0;
}
