//1E-14
#include <stdio.h>
#include <stdlib.h>
#include <assert.h>
#include <sys/stat.h>
#include <string.h>
#include <omp.h>
#include <time.h>
#include <math.h>
#include <sys/time.h>
#include <stdint.h>
#define EPSILON 1E-30
#define STRING_LEN 1024*64
#define PROJECT_NAME "MPP-JACOBI-OPENMP.txt"


typedef struct {
    uint32_t n, m;
    double *vetor;
}tpMatrix;

 
uint64_t saveBinary(tpMatrix *A, char * filename);
uint64_t loadBinary(tpMatrix *A, char *filename);
void help(void);
double get_wall_time(void);
uint32_t md5_from_memory(uint8_t *md_value, const unsigned char *data, uint64_t len);
void save_anwser(const double elapsedtime, const uint8_t *md5, const uint32_t md_len);
void jacobiSolverMethod(double**  __restrict__ X,
                        tpMatrix* __restrict__ A,
                        tpMatrix* __restrict__ B,
                        const double error,
                        int show);
int main (int ac, char **av){
    tpMatrix A, B, X, X1;
   
 

    double error = atof(av[1]);
    int    showErr = atoi(av[2]);

    char  *filename_A = av[3],
          *filename_B = av[4],
          *filename_X = av[5];

    uint64_t            mem = 0;


    mem =  loadBinary(&A, filename_A);
    mem += loadBinary(&B, filename_B);

    printf("\nMétodo de Jacobi para solução de sistema linear\n");
    printf("\t     Error: %.3E \n", error);
    printf("\t  Matriz A: %s \n", filename_A);
    printf("\t   Vetor B: %s \n", filename_B);

    X1.m = B.n;
    X1.n = B.m;

    jacobiSolverMethod( &X1.vetor, &A, &B, error,  showErr);
    saveBinary(&X1, filename_X);



    free(A.vetor);
    free(B.vetor);
    free(X1.vetor);

    return EXIT_SUCCESS;
}

uint64_t saveBinary(tpMatrix *A, char * filename){
    FILE *ptr = fopen(filename, "wb");
    uint64_t bytes_written = 0, aux;
    assert(ptr != NULL);
    aux = fwrite(&A->m, sizeof(A->m), 1, ptr); bytes_written += aux * sizeof(A->m);
    aux = fwrite(&A->n, sizeof(A->n), 1, ptr); bytes_written += aux * sizeof(A->n);
    aux = fwrite(A->vetor, sizeof(double), A->m * A->n, ptr); bytes_written += aux * sizeof(double);

    fclose(ptr);

}

uint64_t loadBinary(tpMatrix *A, char *filename){
    FILE *ptr = fopen(filename, "rb");
    assert(ptr != NULL);
    double *a = NULL;
    uint64_t bytes_read = 0, aux;
    //numread = fread( list, sizeof( char ), 25, stream );

    aux = fread(&A->m, sizeof(A->m), 1, ptr); bytes_read += aux * sizeof(A->m);
    aux = fread(&A->n, sizeof(A->n), 1, ptr); bytes_read += aux * sizeof(A->n);

    a = (double *) malloc( A->m *  A->n * sizeof(double));
    assert(a != NULL);

    aux = fread(a, sizeof(double), A->m * A->n, ptr); bytes_read += aux * sizeof(double);

    A->vetor = a;
    fclose(ptr);
    return bytes_read;
    //print2Console(A);
}

void help(void){
    printf("\n\nExemplo de execução do programa:\n");
    printf("./solver-jacobi.exec 1E-10 1 A.bin B.bin Xout.bin\n");
    printf("                       |   |   |    |     |--------------> arquivo de saída \n");
    printf("                       |   |   |    |--------------------> arquivo com vetor B \n");
    printf("                       |   |   |-------------------------> arquivo com matriz A \n");
    printf("                       |   |-----------------------------> Exibe erro máximo a cada passo \n");
    printf("                       |---------------------------------> Critério de parada ER \n");
}



void jacobiSolverMethod(double**  __restrict__ X,
                        tpMatrix* __restrict__ A,
                        tpMatrix* __restrict__ B,
                        const double error,
                        int show){

   double aux,
         div,
         err = 0.0,
         *x0 = NULL,
         *x1 = NULL;
   unsigned int inter = 0;
   int flag = 0;

   x0 = (double *) malloc(B->m * sizeof(double));
   x1 = (double *) malloc(B->m * sizeof(double));

   bzero(x0, B->m * sizeof(double));
   bzero(x1, B->m * sizeof(double));

#pragma omp parallel private(aux, div) shared (x0, x1, A, B, error, err, show, flag)
{
    do{
            //Parte 1: resolve n equações
            #pragma omp for
            for (unsigned int j = 0; j < A->m; j++){ //M equações
                aux    = 0.0;
                div    = 0.0;

                for (unsigned int i = 0; i < A->n; i++){ // n incógnitas
                if (j != i)
                    aux += (A->vetor[A->n * j + i] * x0[i]);
                else
                    div =  A->vetor[A->n * j + i];
                }
                x1[j] = (B->vetor[j] - aux) / div ;
            }
            //Parte 2: Critério de parada do métodoi

            #pragma omp for reduction(max:err)
            for (unsigned int j = 0; j < A->n; j++){
                double b = fabs((x1[j] - x0[j]) / (x1[j] + EPSILON));
                if (b > err)
                    err = b;
                //err = max(err, b);
            }

            //#pragma omp barrier
            #pragma omp single
            {
                //Parte 3: Atualização/swap
                double *swap = x0;
                x0 = x1;
                x1 = swap;
                inter++;

                if (show){
                    printf("\t     Error: %.3E | step: %.5u | thread: %d\n", err, inter, omp_get_num_threads());
                    fflush(stdout);
                }

                //Parte 4: 'Aplica o critéio de parada
                flag = (err > error);
                err = 0.0f;
            }
            #pragma omp barrier
    }while (flag);
}
    *X = x0;
    printf("----------------------------------------------------------------\n");
    printf("\t     Error: %.3E | passos %u\n", error, inter);
    printf("----------------------------------------------------------------\n");
    free(x1);

}

