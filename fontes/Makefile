CPUCC       = gcc
DEFS        = -DALING=64
INCLUDES    = -I.
LIBDIR      =  #-L/opt/gnu-gcc/lib64
LIBS        = -lm
MKDIR_P     = mkdir -p
OUT_DIR     = obj

LINK        = $(LIBDIR) $(LIBS)  #-static #-static-libstdc++ -static-libgcc
COMPILECPU  = $(CPUCC) $(DEFS) $(INCLUDES) $(CPPFLAGS)

all: directories main-solve-jacobi-O3-native main-solve-jacobi-O3  main-solve-jacobi-O0


main-solve-jacobi-O3-native:
	$(COMPILECPU) -O3 -march=native -fopenmp -c main-solver-jacobi-mt.c -o ${OUT_DIR}/main-solver-jacobi-mt-O3-native.o
	$(COMPILECPU) -O3 -march=native -fopenmp ${OUT_DIR}/main-solver-jacobi-mt-O3-native.o $(LINK)  -o solver-jacobi-mt-O3-native.exec

main-solve-jacobi-O3:
	$(COMPILECPU) -O3  -fopenmp -c main-solver-jacobi-mt.c -o ${OUT_DIR}/main-solver-jacobi-mt-O3.o
	$(COMPILECPU) -O3  -fopenmp ${OUT_DIR}/main-solver-jacobi-mt-O3.o $(LINK)  -o solver-jacobi-mt-O3.exec


main-solve-jacobi-O0:
	$(COMPILECPU) -O0 -fopenmp -c main-solver-jacobi-mt.c -o ${OUT_DIR}/main-solver-jacobi-mt-O0.o
	$(COMPILECPU) -O0 -fopenmp ${OUT_DIR}/main-solver-jacobi-mt-O0.o $(LINK)  -o solver-jacobi-mt-O0.exec

directories:
	${MKDIR_P} ${OUT_DIR}

clean:
	rm ${OUT_DIR}/*.o; rm *.exec
