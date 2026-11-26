# Análise de desempenho do método de Jacobi com Linux perf

## Integrantes do Grupo
* **[Gustavo Luiz da Silvs Procópio]** — Matrícula: `[20260002990]`
* **[Pablo Torres Santos da Silva]** — Matrícula: `[20260023176]`
* **[Pedro Lucas de Oliveira Alves]** — Matrícula: `[20260011184]`

## Estrutura do repositório
```sh
trabalho-arq
├── experimentos
│   ├── coleta_antigo/  # Resultados da coleta auxiliar com temperatura e carga (PC Antigo)
│   ├── coleta_novo/    # Resultados da coleta auxiliar com temperatura e carga (PC Novo)
│   ├── pc_antigo   # Contém ps logs brutos do perf (.txt) e saídas (.bin) da máquina antiga
│   │   ├── otimizacao-00/
│   │   ├── otimizacao-03/
│   │   └── otimizacao-03-native/
│   ├── pc_novo # Contém ps logs brutos do perf (.txt) e saídas (.bin) da máquina nova
│   │   ├── otimizacao-00/
│   │   ├── otimizacao-03/
│   │   └── otimizacao-03-native/
│   ├── graficos    # Contém Gráficos interativos (.html) e estáticos (.png)
│   │   ├── images
│   │   │   ├── box_branch_miss_rate_to_matrix_size.png
│   │   │   ├── box_cache_miss_rate_to_matrix_size.png
│   │   │   ├── box_CPI_to_matrix_size.png
│   │   │   ├── box_IPC_to_matrix_size.png
│   │   │   ├── box_time_to_matrix_size.png
│   │   │   ├── error_bars_branch_miss_rate.png
│   │   │   ├── error_bars_cache_miss_rate.png
│   │   │   ├── error_bars_IPC.png
│   │   │   ├── error_bars_time.png
│   │   │   ├── scatter_branch_miss_rate_to_matrix_size.png
│   │   │   ├── scatter_cache_miss_rate_to_matrix_size.png
│   │   │   ├── scatter_CPI_to_matrix_size.png
│   │   │   ├── scatter_IPC_to_matrix_size.png
│   │   │   └── scatter_time_to_matrix_size.png
│   │   ├── box_branch_miss_rate_to_matrix_size.html
│   │   ├── box_cache_miss_rate_to_matrix_size.html
│   │   ├── box_CPI_to_matrix_size.html
│   │   ├── box_IPC_to_matrix_size.html
│   │   ├── box_time_to_matrix_size.html
│   │   ├── error_bars_branch_miss_rate.html
│   │   ├── error_bars_cache_miss_rate.html
│   │   ├── error_bars_CPI.html
│   │   ├── error_bars_IPC.html
│   │   ├── error_bars_time.html
│   │   ├── scatter_branch_miss_rate_to_matrix_size.html
│   │   ├── scatter_cache_miss_rate_to_matrix_size.html
│   │   ├── scatter_CPI_to_matrix_size.html
│   │   ├── scatter_IPC_to_matrix_size.html
│   │   ├── scatter_time_to_matrix_size.html
│   │   └── README.md
│   ├── analise.ipynb   # Notebook de limpeza e separação de dados, e criação de gráficos
│   ├── calculos.ipynb  # Notebook com a validação númerica das 300 saídas contra Xn000,bin com erro de 1E-10 e agrupamento dos dados de carga e temperatura
│   ├── coleta_jacobi_simples_vibed.py  # Script auxiliar de monitoramento térmico e de carga
│   ├── metricas_performance.xlsx   # Planilha final (abas: tabela_completa e estatisticas)
│   ├── metricas_performance_PC_ANTIGO.csv  # Dados brutos consolidados (PC Antigo)
│   ├── metricas_performance_PC_NOVO.csv    # Dados brutos consolidados (PC Novo)
│   ├── process_data.py # Processamento dos logs do perf para CSVs consolidados
│   ├── automation.py   # Script de execução automatizada (10 repetições + perf stat)
│   ├── pyproject.toml
│   └── uv.lock
│
├── fontes  # Contém código-fonte original, Makefile, instâncias e validador (diff-mat)
│   ├── obj
│   │   ├── main-solver-jacobi-mt-O0.o
│   │   ├── main-solver-jacobi-mt-O3-native.o
│   │   └── main-solver-jacobi-mt-O3.o
│   ├── validacao
│   │   ├── obj
│   │   │   ├── main-diff-mat.o
│   │   │   └── rural-mat.o
│   │   ├── diff-mat.exec
│   │   ├── main-diff-mat.cpp
│   │   ├── main-gener-A-B-X.cpp
│   │   ├── rural-mat.cpp
│   │   ├── rural-mat.hpp
│   │   └── Makefile
│   ├── main-solver-jacobi-mt.c
│   ├── solver-jacobi-mt-O0.exec
│   ├── solver-jacobi-mt-O3-native.exec
│   ├── solver-jacobi-mt-O3.exec
│   └── Makefile
│
├── enunciado_trabalho_jacobi_perf-1.pdf
├── perf-1.pdf
├── README.md   # Documentação do projeto
├── relatorio.pdf   # Documentação do projeto
├── relatorio_mod_linux.odt
├── USO.md  # Declaração do uso de LLMs

```
# Súmario


- [Análise de desempenho do método de Jacobi com Linux perf](#análise-de-desempenho-do-método-de-jacobi-com-linux-perf)
  - [Integrantes do Grupo](#integrantes-do-grupo)
  - [Estrutura do repositório](#estrutura-do-repositório)
- [Súmario](#súmario)
- [1. Ambiente:](#1-ambiente)
  - [1.1 Especificações dos Computadores:](#11-especificações-dos-computadores)
  - [1.2 Condição nos Computadores:](#12-condição-nos-computadores)
    - [1.2.1 Temperatura:](#121-temperatura)
    - [1.2.2 Carga Média](#122-carga-média)
    - [1.2.3. Processos em Execução:](#123-processos-em-execução)
- [2. Escopo do Experimento:](#2-escopo-do-experimento)
  - [2.1 Níveis de Otimização](#21-níveis-de-otimização)
  - [2.2 Matrizes e Dimensões](#22-matrizes-e-dimensões)
  - [2.3 Métricas](#23-métricas)
    - [2.3.1 Comando de Coleta:](#231-comando-de-coleta)
    - [2.3.2. IPC (Instructions per Cycles)](#232-ipc-instructions-per-cycles)
    - [2.3.3. Taxa de Erros de Predição de Desvio (Branch Miss Rate)](#233-taxa-de-erros-de-predição-de-desvio-branch-miss-rate)
    - [2.3.3. Taxa de Erros de Acesso a Cache(Cache Miss Rate)](#233-taxa-de-erros-de-acesso-a-cachecache-miss-rate)
    - [2.4. Limitações das amostras:](#24-limitações-das-amostras)
# 1. Ambiente:


## 1.1 Especificações dos Computadores: 

|   Campo               |            Máquina Nova                   | Máquina Antiga                                    |
| --------------------- | ----------------------------------------- | ------------------------------------------------- |
| Id Maquina            | e7b7f49ddd09b1c0198869df64348520          | e7b7f49ddd09b1c0198869df64348520                  |
| Hostname              | lab08013                                  | lab280867                                         |
| Arquitetura           | x86-64                                    | x86-64                                            | 
| Processador           | AMD Ryzen 5 5600G with Radeon Graphics    | Intel Core i3-2120                                |
| Geração da CPU        | Ryzen 5000 / Zen 3 (Cezanne)              | 2ª geração Intel Core / Sandy Bridge              |
| Modelo da CPU         | 80                                        | 42                                                |
| Núcleos Fisicos       | 6                                         | 2                                                 |
| CPUs Lógicas          | 12                                        | 4                                                 |
| Tamanho Cache L1      | L1d:192 KiB-L1i:192 KiB                   | L1d:64 KiB-L1i:64 KiB                             | 
| Tamanho Cache L2      | 3 MiB                                     | 512 KiB                                           |
| Tamanho Chache L3     | 16 MiB                                    | 3 MiB                                             |
| Memória Instalada     | 8 GB DDR4-2400 MT/s, 1x8                  | 4 GB DDR3-1333, 2 × 2 GB 1333 MT/s (Dual-Channel) |
| Sistema Operacional   | Ubuntu 22.04.1 LTS                        | Ubuntu 22.04.3 LTS                                |
| Kernel                | Linux 6.8.0-138-generic                   | 6.2.0-26-generic                                  |
| Versão GCC            | 11.4.0                                    | 11.4.0                                            |
| Versão runtime OpenMP | 201511 — OpenMP 4.5                       | 201511 — OpenMP 4.5                               | 
| Versão Perf           | 6.8.12                                    | 6.8.13                                            |
| Processador Hibrido   | Não                                       | Não                                               |
| Hyper-Threading/SMT   | Sim                                       | Sim                                               | 
| Afinidade de CPU      | CPUs lógicas 0 e 1: núcleos fisicos 0 e 1 | CPUs lógicas 0 e 1: núcleos fisicos 0 e 1         |
| Turbo/Boost           | Suportado e Ativo                         | Não Suportado                                     |
| Mapeamento dos cores  | **CPU lógica → Núcleo físico**<br>`0 → 0` · `1 → 1` · `2 → 2`<br>`3 → 3` · `4 → 4` · `5 → 5`<br>`6 → 0` · `7 → 1` · `8 → 2`<br>`9 → 3` · `10 → 4` · `11 → 5`  | **CPU lógica → Núcleo físico**<br>`0 → 0` · `1 → 1`<br>`2 → 0` · `3 → 1`|


## 1.2 Condição nos Computadores: 
    O registro das temperaturas e cargas foi feito posteriormente nas mesmas máquinas matrizes 1000x1000, 3000x3000 e 5000x5000, reduzindo o numero de dados para monitorar, e possibilitando ainda assim uma noção geral da carga e temperatura das máquinas durante a execução.
    Os aplicativos abertos se mantiveram inalterados. Diferentemente dos arquivos para a execução primária, análise e geração de gráficos, o código coleta dessas métricas foi gerado via inteligencia artifical ao invés de escrito manualmente.

### 1.2.1 Temperatura: 




* PC Novo
  
| Otimização | Tamanho da matriz | Temperatura média (°C) | Desvio padrão (°C) | 
|------------| ----------------- | ---------------------- | ------------------ |
| O0         | 1000 × 1000       | 40,40                  | 0,40               | 
| O0         | 3000 × 3000       | 45,43                  | 3,93               |
| O0         | 5000 × 5000       | 52,03                  | 1,82               |
| O3         | 1000 × 1000       | 50,87                  | 3,01               | 
| O3         | 3000 × 3000       | 45,17                  | 0,67               | 
| O3         | 5000 × 5000       | 45,07                  | 0,81               |
| O3-native  | 1000 × 1000       | 44,77                  | 1,36               | 
| O3-native  | 3000 × 3000       | 42,80                  | 0,36               | 
| O3-native  | 5000 × 5000       | 44,50                  | 0,89               |

`O0`: Nesse nível de otimização observa-se um aumento da temperatura média conforme o tamanho da matriz aumenta.

`O3`: Neste nível de otimização, a temperatura permaneceu mais próxima de 45ºC. O pico de 50.87º na temperatura média, também é acompanhado de um alto desvio padrão, podendo sinalizar um pico atipico de temperatura nesse nível de otimização no momento de execução. Nesse nível de otimização, o aumento do tamanho da matriz não causou impacto significativo na temperatura.

`O3-native`: Neste nível de otimização, as temperaturas médias foram de 44,77 °C, 42,80 °C e 44,50 °C para as matrizes de 1000 × 1000, 3000 × 3000 e 5000 × 5000, respectivamente. O menor desvio padrão foi observado na matriz de 3000 × 3000, com apenas 0,36 °C, indicando maior estabilidade nas medições dessa configuração. A temperatura semelhante ao nível O3, e até menor talvez possa ser atribuido ao uso de instruções especificas de hardware, facilitando execução na CPU

De modo geral, no PC novo, a otimização O0 apresentou o maior aquecimento à medida que o tamanho da matriz aumentou. Já O3 e O3-native mantiveram temperaturas médias relativamente estáveis para os maiores tamanhos de matriz.

* PC Velho
  
| Otimização | Tamanho da matriz | Temp. C1 média (°C) | Desvio Padrão C1 | Temp. C2 média (°C) | Desvio Padrão C2 |
|----------- | ----------------- | ------------------- | ---------------- | ------------------- | ---------------- |
| O0         | 1000 × 1000       | 38,33               | 0,58             | 38,33               | 0,58             |
| O0         | 3000 × 3000       | 41,33               | 2,52             | 40,67               | 2,08             | 
| O0         | 5000 × 5000       | 45,67               | 4,04             | 45,67               | 4,04             |
| O3         | 1000 × 1000       | 47,00               | 3,61             | 45,67               | 3,06             |
| O3         | 3000 × 3000       | 47,33               | 3,21             | 46,33               | 2,52             | 
| O3         | 5000 × 5000       | 44,00               | 0,00             | 43,00               | 0,00             |
| O3-native  | 1000 × 1000       | 47,33               | 2,52             | 47,33               | 2,52             |
| O3-native  | 3000 × 3000       | 45,00               | 1,00             | 43,67               | 1,15             | 
| O3-native  | 5000 × 5000       | 45,00               | 1,73             | 44,00               | 1,73             | 

`O0`: Nesse nível de otimização observa-se um aumento da temperatura média conforme o tamanho da matriz aumenta, e uma menor estabilidade da temperatura, expresso pelo desvio padrão mais elevado.

`O3`: Nesse nível de otimização se observou uma maior média de temperaturas, acompanhada de maior estabilidade nas matrizes de maior tamanho. 

`O3-native`:  Nesse nível de otimização se observou temperaturas semelhantes ao nível O3 sem otimização para execucação de instruções nativas e maior estabilidade.

De modo geral, o PC antigo apresentou temperaturas médias mais elevadas nas configurações O3 e O3-native em comparação com O0. Entretanto, diferentemente do comportamento observado em O0, as otimizações O3 e O3-native não apresentaram aumento progressivo da temperatura conforme o tamanho da matriz aumentou.

Ademais, deve-se ressaltar que a condição de resfriamento no ambiente também pode ter afetado nas medições. Atitudes como abertura de porta ou redução ou aumento dinamica na temperatura do ar condicionado para se conformar ao gasto de energia e temperatura podem ter afetado as medidas. Assim como também picos de carga na execução de processos no computador.

### 1.2.2 Carga Média
A carga média do processador foi obtida por meio do arquivo /proc/loadavg, considerando o valor referente ao último minuto durante as execuções. Essa métrica permite observar a demanda de processamento imposta por cada configuração experimental.

* PC novo — AMD Ryzen 5 5600G
  
| Otimização | Media 1000  | DP 1000 | Media 3000 | DP 3000 | Media 5000 | DP 5000 |
| ---------- | ----------  | ------- | ---------- | ------- | ---------- | ------- |
| O0	       |   0,79	   | 0,18	     |   0,75     | 0,03    | 0,91       | 0,05    |  
| O3	       |   1,97	   | 0,31	     | 1,91       | 0,12    | 1,72       | 0,09    |
| O3-native	 |   1,44	   | 0,12      | 1,12       | 0,09    | 0,87       | 0,07    |

`O0`: Apresentou os menores valores de carga média entre as três configurações de otimização, variando de 0,75 a 0,91. Observa-se uma pequena variação entre os diferentes tamanhos de matriz, indicando uma demanda relativamente baixa e estável do processador.

`O3`: Apresentou os maiores valores de carga média, variando de 1,72 a 1,97. Apesar de registrar uma carga superior às demais configurações, observa-se uma pequena redução conforme o tamanho da matriz aumenta.

`O3`-native: Apresentou uma redução progressiva da carga média, passando de 1,44 nas matrizes de 1000 × 1000 para 0,87 nas matrizes de 5000 × 5000. Esse comportamento indica uma diminuição da carga média registrada nas execuções com matrizes maiores

* PC antigo — Intel Core i3-2120
  
| Otimização | Media 1000  | DP 1000 | Media 3000 | DP 3000 | Media 5000 | DP 5000 |
| ---------- | ----------  | ------- | ---------- | ------- | ---------- | ------- |
| O0	       |   1,90	     | 0,16	   | 1,51       | 0,09    | 2,29       | 0,50    |  
| O3	       |   2,17	     | 0,14	   | 2,32       | 0,28    | 2,20       | 0,11    |
| O3-native	 |   2,07	     | 0,11    | 1,82       | 0,02    | 1,84       | 0,37    |



`O0`: Apresentou carga média de 1,90 para matrizes de 1000 × 1000, reduzindo para 1,51 nas matrizes de 3000 × 3000. Para matrizes de 5000 × 5000, houve um aumento para 2,29, representando o maior valor registrado nessa configuração de otimização.

`O3`: Apresentou valores relativamente estáveis de carga média, variando entre 2,17 e 2,32. A maior carga foi registrada nas matrizes de 3000 × 3000, com valor de 2,32.

`O3-native`: Apresentou carga média de 2,07 para matrizes de 1000 × 1000, reduzindo para 1,82 nas matrizes de 3000 × 3000 e apresentando uma pequena elevação para 1,84 nas matrizes de 5000 × 5000. Entre as três configurações, apresentou o comportamento mais estável para os dois maiores tamanhos de matriz.

### 1.2.3. Processos em Execução:
Durante a execução dos experimentos, os seguintes programas permaneciam abertos:
1. Visual Studio Code (VS Code);
2. Mozilla Firefox.
Além desses programas, outros processos e serviços do sistema operacional permaneciam ativos, podendo contribuir para a carga geral das máquinas.


# 2. Escopo do Experimento:

## 2.1 Níveis de Otimização
Foram utilizadas três configurações de compilação:
* `O0`: Na qual as otimizações do compilador são desativadas, e as instruções do código-fonte são traduzidas de forma direta. Útil para servir como baseline para medir o ganho bruto das otimizações. Também acelera o processo de compilação.
  
* `O3`: Otimização de nivel 3, no qual ativa otimizações do nivel `O2` como reordenação de instrução(instruction scheduling),function inlining(substituição da chamada da função pelo próprio corpo), eliminação de código morto(dead code elimination)  além de adicionar transformações   agressivas que melhoram o paralelismo e localidade de dados, entre elas: loop unroling(desenrolamento de laços), loop distribution(divisão de laços), IPA-CP (Interprocedural Constant Propagation) e vetorização automática.
  
* `O3-native`: Nível `O3` junto a flag `-march=native`, o compilador detecta a CPU da máquina e libera instruções de hardware especificas e registradores mais largos. Exemplos são as extensões vetoriais AVX2, AVX-512 — além de ajustar o escalonamento de instruções às latências e unidades

## 2.2 Matrizes e Dimensões
Foram utilizadas matrizes de dimensões 1000×1000, 2000×2000, 3000×3000, 4000×4000 e 5000×5000.

Para cada combinação de máquina, otimização e tamanho de matriz, foram realizadas dez execuções, totalizando:
- 2 computadores;
- 3 configurações de compilação;
- 5 tamanhos de matriz;
- 10 repetições por combinação;
- 300 execuções no total.
Foram utilizados dois threads OpenMP, com OMP_NUM_THREADS=2 e OMP_DYNAMIC=FALSE, restringindo a execução às CPUs lógicas 0 e 1 por meio de taskset -c 0,1.


## 2.3 Métricas
### 2.3.1 Comando de Coleta: 
O comando padronizado para a instrumentação e execução do algoritmo foi:
```sh

OMP_NUM_THREADS=2 OMP_DYNAMIC=FALSE perf stat -e cycles,instructions,branches,branch-misses,cache-references,cache-misses -o ${destiny} taskset -c ${cores} ${executable} 1E-10 0 ${mat1} ${mat2} ${saida}
```


* **`OMP_NUM_THREADS=2` e `OMP_DYNAMIC=FALSE`:** Fixa a execução em exatamente duas threads de trabalho, desabilitando o ajuste dinâmico do runtime OpenMP.
* **`taskset -c 0,1`:** Impõe a afinidade de CPU (*CPU affinity*), vinculando os processos estritamente aos processadores lógicos 0 e 1 do sistema operacional.

* `${executable}`: Solucionador do método de Jacobi.
* `1E-10`: Critério de tolerância ($\varepsilon = 10^{-10}$) para convergência.
* `0`: Desabilita a exibição do erro máximo a cada passo
* `${mat1}` e `${mat2}`: Matrizes de coeficientes $A$ e vetor/matriz de termos independentes $B$ armazenados em formato binário (`Ax000.bin`, `Bx000.bin`).
* `${saida}`: Arquivo de persistência da solução calculada ($X$).
* `${destiny}`: Arquivo de texto que recebe a saída bruta dos contadores da PMU capturados pelo utilitário `perf stat`.

Para reproduzir o experimento: 
1. Habilitar acesso aos contadores do perf (Linux)
```sh
sudo sh -c "echo 2 > /proc/sys/kernel/perf_event_paranoid"
```

2. Compilar os executáveis na máquina alvo
Na pasta `fontes/` e na pasta `fontes/validacao` respectivamente:
```sh
make clean && make
make clean && make diff-mat
```

3. Executar os experimentos
```sh 
python3 automation.py
```

4. Processar os dados e gerar estatísticas/gráficos
```sh
python3 process_data.py
python3 -m jupyter nbconvert --to notebook --execute analise.ipynb # ou execute as celulas diretamente, pois esse metódo foi testado
python3 -m jupyter nbconvert --to notebook --execute calculos.ipynb # ou execute as celulas diretamente, pois esse metódo foi testado
```


---

### 2.3.2. IPC (Instructions per Cycles)
**Eventos da PMU/sintaxe no *perf***: `cycles`, `instructions`

**Unidade:** Adimensional (instruções/ciclo para IPC; ciclos/instrução para CPI).

**Significado Arquitetural**:
As arquiteturas x86-64 modernas são superescalares e podem buscar, decodificar, executar e aposentar várias instruções por ciclo, assim, é possível que o computador execute mais de uma instrução por ciclo. Nesse contexto, a métrica de IPC nos permite ver quantas instruções estão sendo executadas por ciclo no computador, analisando assim sua vazão(throughtput) de instruções e ajudando a analisar seu desempenho.

**IPC Alto (> 1.5 a 2.5):** Indica alta ocupação das unidades de execução (ALUs, FPUs, registradores vetoriais) e pipeline desobstruído.

**IPC Baixo(≤1.0 ou ≤0.5)** Revela a ocorrência de bolhas no pipeline (*pipeline stalls*). O clock do processador avança, mas as instruções não são confirmadas porque as portas de despacho estão bloqueadas aguardando a chegada de dados da hierarquia de memória (*memory-bound stalls*) ou a resolução de dependências de dados. <!--melhorar esse texto daqui porque não está muito natural, em relação aos termos-->

**Hipótese**: 
Espera-se que o **IPC** caia drasticamente nas execuções com otimização O3 e O3-native em comparação ao IPC nas execuções com otimização O0, uma vez que estas otimizações incluem a presença de vetorização automática de suas instruções, permitindo que uma única instrução opere sob múltiplos dados simultaneamente (SIMD — Single Instruction, Multiple Data). 
Espera-se que essa queda seja ainda mais acentuada na otimização O3-native, devido a presença de extensões do conjunto vetoriais como AVX2 e FMA  que permitem a execução operações sobre 4 (256 bits) números de precisão dupla de uma vez só e multiplicação e soma em passo único, com apenas um arredondamento. 
Também se espera que essa queda no IPC na CPU Intel(computador antigo) seja menor, uma vez que não há suporte a conjunto de instruções modernas de vetorização como os conjuntos AVX2 citados, mantendo suporte a conjuntos de instruções vetoriais mais antigas como SSE4.1 e AVX 



**Justificativa de relevância**:

* A análise do IPC é fundamental porque o tempo de execução é regido pela relação clássica:
  $$Tempo = \frac{\text{Instruções}}{\text{IPC} \times \text{Frequência}} = \text{Instruções} \times \text{CPI} \times \text{Período de Clock}$$
* Quando a vetorização atua em `O3` e `O3-native`, o número absoluto de instruções despenca (ex.: queda de $\approx 3,5$ bilhões para $\approx 900$ milhões em $N=1000$). Como instruções vetoriais demandam mais estágios e realizam o trabalho equivalente a múltiplas instruções escalares, o IPC pode se manter estável ou até cair ligeiramente. A métrica comprova que a aceleração decorre da redução do total de instruções úteis executadas, e não de um mero aumento na frequência de despacho de instruções escalares.


**Disponibilidade e Comparatividade entre máquinas**:
Disponibilidade: Os eventos `cycles` e `instructions` estão disponíveis nas duas máquinas utilizadas.

* Disponibilidade: Os eventos cycles e instructions são universais e contidos nos contadores arquiteturais básicos em arquiteturas Intel e AMD.
* Diferenças semânticas na PMU:
    *instructions*: O evento monitora instruções confirmadas/aposentadas (retired), descartando instruções executadas sob ramos especulativos incorretos. Entretanto, o compilador emite instruções distintas para a AMD Zen 3 (suporte a AVX2/FMA3 de 256 bits) e para a Intel Sandy Bridge (limitada a instruções escalares ou AVX de 1ª geração sem FMA). Adicionalmente, técnicas de macro-fusion diferem entre as gerações.
    *cycles*: Mede ciclos não parados (CPU_CLK_UNHALTED). No Core i3-2120, a frequência é nominalmente estática (3,30 GHz, sem Turbo Boost). No Ryzen 5 5600G, a frequência é dinâmica (Precision Boost ativo, variando entre 3,9 e 4,4 GHz). Assim, comparações absolutas de ciclos entre as duas máquinas são desprovidas de base isomórfica, devendo-se comparar o speedup e ganhos relativos.

* Limitações da PMU: Devido à requisição de 6 eventos simultâneos para uma PMU de 4 contadores de propósito geral, o perf operou com multiplexação temporal (≈83% do tempo ativo para instructions, e 66% do tempo para cycles), estimando os totais por extrapolação linear. O uso do sufixo :u (cycles:u, instructions:u) filtrou o ruído de chamadas ao kernel, isolando a computação do espaço de usuário.
  
> **Fórmula: **IPC** = $\frac{Instructions}{Cycles}$**

---

### 2.3.3. Taxa de Erros de Predição de Desvio (Branch Miss Rate)
**Eventos da PMU/sintaxe no *perf***:  `branches` e `branch-misses`.

**Unidade:** Porcentagem (%).

**Significado Arquitetural**: Para evitar que o pipeline congele a cada instrução de controle de fluxo condicional (`j`, `bne`, `beq`, `jal` etc.), o processador utiliza uma unidade de hardware especializada — o **Preditor de Desvios (*Branch Predictor*)** — composta por tabelas de histórico (*Branch History Table* - BHT, *Branch Target Buffer* - BTB e preditores baseados em perceptrons/TAGE). Ele infere o desfecho do salto antes de sua resolução lógica.
* **Acerto (*Branch Hit*):** O processador alimenta o pipeline com as instruções especulativas do fluxo correto sem perda de tempo.
* **Erro (*Branch Miss*):** O processador detecta que seguiu o caminho errado, descartas as instruções especuladas e o pipeline começa de novo da branch correta, o tempo gasto por um erro de predição de branch tende a ser proporcional ao número de estágios na pipeline entre busca e execução. Microprocessadores modernos tendem a ter pipelines mais longas, o que resulta em perdas gerais de 10 a 20 ciclos de clock

**Hipótese**: Espera-se que o experimento tenha baixa taxa de erros de predição, uma vez que o metódo de resolução jacobi utiliza de loops aninhados, como é possível visualizar no código:
```c
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
```



**Justificativa de relevância**: Como em um laço `for (int j = 0; j < N; j++)`, a condição de retorno do salto é verdadeira centenas ou milhares de vezes consecutivas e falsa apenas na última iteração. O histórico de saltos aprende esse comportamento rapidamente e realiza um grande número de predições acuradas, com minuscúla taxa de erro.

Como o critério de parada ($err < 10^{-10}$) é avaliado apenas uma vez a cada iteração externa completa sobre as matrizes, erros de predição de desvio nesse critério geram pouco impacto na métrica agregada.

**Disponibilidade e Comparatividade entre máquinas**:
* **Disponibilidade:** Os contadores `branches` e `branch-misses` estão presentes nas PMUs de ambas as máquinas.
  
* **Composição do evento:** O contador genérico agrega todos os ramos arquiteturais validados (saltos condicionais, incondicionais, chamadas e retornos). Compiladores diferentes (ou níveis distintos de otimização como `O2` e `O3`) podem converter laços em estruturas de desvio diferentes ou realizar loop unroling, reduzindo o número de desvios.
  
* **Diferenças na PMU e preditores:** O Ryzen 5 5600G (Zen 3) implementa um preditor TAGE complexo com suporte a histórico longo e buffers consideravelmente maiores do que o preditor de 2 níveis da Sandy Bridge (2011). Isso faz com que taxas residuais de miss ligeiramente menores no PC Novo reflitam o avanço da microarquitetura, e não propriedades algorítmicas.
  
* **Afinidade (`taskset -c 0,1`):** Como as CPUs lógicas 0 e 1 foram mapeadas para núcleos físicos distintos (núcleos 0 e 1) em ambas as máquinas, as threads não concorreram pelos buffers físicos de histórico de salto (BTB), operando sem interferência mútua de predição.


> **Fórmula: Branch Miss Rate = $\frac{Branch Misses}{Branch}$ x 100**
  * `branches`: Total de instruções de desvio executadas e validadas.
  * `branch-misses`: Total de instruções de desvio cujo alvo foi incorretamente previsto pelo hardware.
  
---

### 2.3.3. Taxa de Erros de Acesso a Cache(Cache Miss Rate)
**Eventos da PMU/sintaxe no *perf***:  `cache-references` e `cache-misses`.
**Unidade:** Porcentagem (%).
**Significado Arquitetural**: A hierarquia de memória existe para reduzir o impacto da diferença de velocidade entre a memória principal (DRAM) e o processador, utilizando níveis intermediários de memória cache (L1, L2 e L3). Quanto mais próximo do núcleo, menor é a capacidade e menor é a latência (Velocidade: L1 > L2 > L3; Capacidade: L3 > L2 > L1).

Os eventos `cache-references` e `cache-misses` geralmente medem o comportamento no último nível de cache(L3), de modo que o `cache-misses` permite analisar quantas vezes ocorreu um *miss* na cache processador foi forçado a acessar a memória RAM. Um acesso a memória RAM costuma impor uma perda de 50 a 80 nanosegundos, o que equivale a centenas de ciclos nos quais a CPU fica ociosa.

**Hipótese**: O algoritmo de Jacobi é tipicamente uma aplicação **limitada por memória (*memory-bound*)**. Para matrizes que excedem a capacidade física do cache L3, a taxa de cache-misses cresce acentuadamente, tornando o subsistema de memória o gargalo dominante do tempo de execução.

Para resolver um sistema linear com matrizes de ordem $N$, são necessários vetores e matrizes que consomem $O(N^2)$ elementos de 8 bytes (`double`). Para resolver um sistema linear de ordem N, o algoritmo utiliza uma matriz de coeficientes A com N^{2} elementos do tipo double (8 bytes cada). Conforme detalhado na tabela da seção anterior, apenas a matriz A já ocupa 7,62 MiB para N=1000, chegando a 190,73 MiB para N=5000.
Assim, espera-se que a memória aparece como um gargalo no desempenho do método.

**Justificativa de relevância**: A  cada iteração do laço principal (do...while), o programa precisa percorrer novamente todas as NxN posições da matriz. De acordo com o levantamento de tamanho das entradas:
• Em N=1000 (7,62 MiB): A matriz já excede a cache L3 da máquina antiga 3 MiB, mas ainda cabe na cache L3 da máquina nova 16 MiB
• A partir de N=2000 30,51 MiB até N=5000 190,73\ MiB: A matriz ultrapassa com folga a capacidade de cache L3 de ambos os processadores, forçando o descarte constante de dados e recarregamentos contínuos a partir da DRAM. Medir a taxa de falhas de cache é, portanto, essencial para comprovar a transição do comportamento da aplicação: de um cenário com bom aproveitamento da hierarquia de cache em matrizes menores para um regime severamente limitado pela largura de banda da memória (memory-bound) nas dimensões maiores, além de permitir avaliar o impacto prático de otimizações de localidade espacial e temporal no código.



**Disponibilidade e Comparatividade entre máquinas**:
* **Disponibilidade:** Os eventos genéricos `cache-references` e `cache-misses` são disponibilizados pelo `perf` para ambas as plataformas x86.
  
* **Diferenças semânticas na PMU:**

Apesar de compartilharem a mesma nomenclatura na interface do perf (que envia ao kernel os identificadores genéricos `PERF_COUNT_HW_CACHE_REFERENCES = 0x2` e `PERF_COUNT_HW_CACHE_MISSES = 0x3` observados abaixo na saida de `perf stat -vv`)
```sh
perf_event_attr:
  type                             0 (PERF_TYPE_HARDWARE)
  size                             136
  config                           0x2 (PERF_COUNT_HW_CACHE_REFERENCES)
  sample_type                      IDENTIFIER
  read_format                      TOTAL_TIME_ENABLED|TOTAL_TIME_RUNNING
  disabled                         1
  inherit                          1
  enable_on_exec                   1
  exclude_guest                    1

perf_event_attr:
  type                             0 (PERF_TYPE_HARDWARE)
  size                             136
  config                           0x3 (PERF_COUNT_HW_CACHE_MISSES)
  sample_type                      IDENTIFIER
  read_format                      TOTAL_TIME_ENABLED|TOTAL_TIME_RUNNING
  disabled                         1
  inherit                          1
  exclude_kernel                   1
  exclude_hv                       1
  enable_on_exec                   1
  exclude_guest                    1

```

o driver da PMU no kernel Linux mapeia esses eventos para níveis distintos da hierarquia de memória em cada microarquitetura:
	• Intel Core i3-2120 (Sandy Bridge): Mapeia diretamente para os contadores do cache L3 (LLC) — eventos `LONGEST_LAT_CACHE.REFERENCE (0x4f2e)` e `LONGEST_LAT_CACHE.MISS (0x412e)`.

	• AMD Ryzen 5 5600G (Zen 3): O kernel Linux mapeia os eventos genéricos para os contadores internos do cache L2 — eventos L2_REQUEST_G1 (`event=0x60, umask=0xff`, que combina outras sub-requisições como `0x01 (group2)`, `0x02 (l2_hw_pf)`, `0x04 (prefetch_l2_cmd)`, `0x08 (change_to_x)`, etc.)  e L2_CACHE_REQ_STAT.IC_DC_MISS_IN_L2  (event=0x64, umask=0x9, código 0x0964).
  


* **Disparidade de capacidade física:** O PC Antigo possui apenas **3 MiB de cache L3 e 512KiB de cache L3**, enquanto o PC Novo dispõe de **16 MiB de cache L3 e 3MiB de cache L2**. Uma matriz de $1000 \times 1000$ ($\approx 8\text{ MB}$) cabe confortavelmente na L3 do Ryzen (junto aos vetores auxiliares), mas transborda inteiramente a L3 do Core i3. Logo, o menor número de misses no PC Novo reflete primordialmente a especificação do silício, e não mérito algorítmico.
  
* **Prefetchers e Barramento:** O PC Novo utiliza barramento DDR4-2400 (maior taxa de transferência) e circuitos de pré-busca (*hardware prefetchers*) muito mais agressivos da arquitetura Zen 3, que identificam com eficiência a varredura contínua de linhas em C (*row-major*). O PC Antigo opera com DDR3-1333 e pré-buscadores de geração anterior.
  
* **Afinidade (`taskset -c 0,1`):** A execução vinculada a dois núcleos físicos distintos garantiu que cada thread operasse com suas próprias caches L1 e L2 privativas, dividindo apenas o pool compartilhado da L3.

> **Fórmula: Cache Miss Rate = $\frac{cache-misses}{cache-loads}$ x 100**
  * `cache-references`: Total de requisições enviadas ao cache de último nível (L3).
  * `cache-misses`: Falhas no L3 que exigiram leitura/escrita na DRAM.







---



### 2.4. Limitações das amostras:
1. **Separação de Medições de Temperatura e Carga:** O registro de temperatura e carga de CPU foi conduzido posteriormente ao experimento principal nas mesmas máquinas e sob condições controladas, cobrindo as dimensões $1000 \times 1000$, $3000 \times 3000$ e $5000 \times 5000$. Portanto, expressam o comportamento térmico sob carga, mas não refletem com exatidão instantânea cada uma das execuções do conjunto de dados principal.
   
2. **Semântica da Métrica de Carga:** A carga obtida via `/proc/loadavg` quantifica o número médio de tarefas executáveis ou aguardando CPU no último minuto, não correspondendo linearmente à porcentagem instantânea de utilização de CPU.
   
3. **Diferenças Semanticas nas metricas de cache**: A diferença de qual acesso a nível de cache é medido no processador Intel e no processador AMD tornam as métricas não diretamente comparáveis.
   
4. **Multiplexação de Contadores:** Pela requisição simultânea de 6 eventos em PMUs com 4 contadores de propósito geral, o `perf` operou com amostragem ponderada no tempo ($\approx 83\%$), extrapolando linearmente as contagens brutas.
