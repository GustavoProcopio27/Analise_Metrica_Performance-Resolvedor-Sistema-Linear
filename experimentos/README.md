# Análise de desempenho do método de Jacobi com Linux perf

## Súmario

## Ambiente:


### 1. Especificações dos Computadores: 
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

### 2. Condição nos Computadores: 
    O registro das temperaturas e cargas foi feito posteriormente nas mesmas máquinas matrizes 1000x1000, 3000x3000 e 5000x5000, reduzindo o numero de dados para monitorar, e possibilitando ainda assim uma noção geral da carga e temperatura das máquinas durante a execução.
    Os aplicativos abertos se mantiveram inalterados. Diferentemente dos arquivos para a execução primária, análise e geração de gráficos, o código coleta dessas métricas foi gerado via inteligencia artifical ao invés de escrito manualmente.

#### 1. Temperatura: 




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

#### 2. Carga Média
A carga média do processador foi obtida por meio do arquivo /proc/loadavg, considerando o valor referente ao último minuto durante as execuções. Essa métrica permite observar a demanda de processamento imposta por cada configuração experimental.

* PC novo — AMD Ryzen 5 5600G
| Otimização | Media 1000  | DP 1000 | Media 3000 | DP 3000 | Media 5000 | DP 5000 |
| ---------- | ----------  | ------- | ---------- | ------- | ---------- | ------- |
| O0	     |   0,79	   | 0,18	 | 0,75       | 0,03    | 0,91       | 0,05    |  
| O3	     |   1,97	   | 0,31	 | 1,91       | 0,12    | 1,72       | 0,09    |
| O3-native	 |   1,44	   | 0,12    | 1,12       | 0,09    | 0,87       | 0,07    |

`O0`: Apresentou os menores valores de carga média entre as três configurações de otimização, variando de 0,75 a 0,91. Observa-se uma pequena variação entre os diferentes tamanhos de matriz, indicando uma demanda relativamente baixa e estável do processador.

`O3`: Apresentou os maiores valores de carga média, variando de 1,72 a 1,97. Apesar de registrar uma carga superior às demais configurações, observa-se uma pequena redução conforme o tamanho da matriz aumenta.

`O3`-native: Apresentou uma redução progressiva da carga média, passando de 1,44 nas matrizes de 1000 × 1000 para 0,87 nas matrizes de 5000 × 5000. Esse comportamento indica uma diminuição da carga média registrada nas execuções com matrizes maiores

* PC antigo — Intel Core i3-2120
| Otimização | Media 1000  | DP 1000 | Media 3000 | DP 3000 | Media 5000 | DP 5000 |
| ---------- | ----------  | ------- | ---------- | ------- | ---------- | ------- |
| O0	     |   1,90	   | 0,16	 | 1,51       | 0,09    | 2,29       | 0,50    |  
| O3	     |   2,17	   | 0,14	 | 2,32       | 0,28    | 2,20       | 0,11    |
| O3-native	 |   2,07	   | 0,11    | 1,82       | 0,02    | 1,84       | 0,37    |



`O0`: Apresentou carga média de 1,90 para matrizes de 1000 × 1000, reduzindo para 1,51 nas matrizes de 3000 × 3000. Para matrizes de 5000 × 5000, houve um aumento para 2,29, representando o maior valor registrado nessa configuração de otimização.

`O3`: Apresentou valores relativamente estáveis de carga média, variando entre 2,17 e 2,32. A maior carga foi registrada nas matrizes de 3000 × 3000, com valor de 2,32.

`O3-native`: Apresentou carga média de 2,07 para matrizes de 1000 × 1000, reduzindo para 1,82 nas matrizes de 3000 × 3000 e apresentando uma pequena elevação para 1,84 nas matrizes de 5000 × 5000. Entre as três configurações, apresentou o comportamento mais estável para os dois maiores tamanhos de matriz.

### 3. Processos em Execução:
Durante a execução dos experimentos, os seguintes programas permaneciam abertos:
1. Visual Studio Code (VS Code);
2. Mozilla Firefox.
Além desses programas, outros processos e serviços do sistema operacional permaneciam ativos, podendo contribuir para a carga geral das máquinas.


### 3. Escopo do Experimento:

#### 3.1 Níveis de Otimização
Foram utilizadas três configurações de compilação:
* `O0`: Na qual as otimizações do compilador são desativadas, e as instruções do código-fonte são traduzidas de forma direta. Útil para servir como baseline para medir o ganho bruto das otimizações. Também acelera o processo de compilação.
  
* `O3`: Otimização de nivel 3, no qual ativa otimizações do nivel `O2` como reordenação de instrução(instruction scheduling),function inlining(substituição da chamada da função pelo próprio corpo), eliminação de código morto(dead code elimination)  além de adicionar transformações   agressivas que melhoram o paralelismo e localidade de dados, entre elas: loop unroling(desenrolamento de laços), loop distribution(divisão de laços), IPA-CP (Interprocedural Constant Propagation) e vetorização automática.
  
* `O3-native`: Nível `O3` junto a flag `-march=native`, o compilador detecta a CPU da máquina e libera instruções de hardware especificas e registradores mais largos. Exemplos são as extensões vetoriais AVX2, AVX-512 — além de ajustar o escalonamento de instruções às latências e unidades

#### 3.2 Matrizes e Dimensões
Foram utilizadas matrizes de dimensões 1000×1000, 2000×2000, 3000×3000, 4000×4000 e 5000×5000.

Para cada combinação de máquina, otimização e tamanho de matriz, foram realizadas dez execuções, totalizando:
- 2 computadores;
- 3 configurações de compilação;
- 5 tamanhos de matriz;
- 10 repetições por combinação;
- 300 execuções no total.
Foram utilizados dois threads OpenMP, com OMP_NUM_THREADS=2 e OMP_DYNAMIC=FALSE, restringindo a execução às CPUs lógicas 0 e 1 por meio de taskset -c 0,1.


#### 3.3 Métricas


# Fazer aqui pfvr


### Instruções de Reprodução
```sh
python automation.py    # Necessidade de responder input se foi utilizado no computador novo ou antigo
python process_data.py  # Necessidade de responder input se foi utilizado no computador novo ou antigo


# Executar blocos de código em analise.ipynb ce em calculos.ipynb onforme necessidade. Os gráficos também podem ser vistos separadamente nos arquivos .hmtl, mantendo responsividade, possibilidade de zoom e filtragem não existente no pdf

```

### Limitações das amostras:
1. A temperatura e carga foram medidos separadamente ao experimento principal no mesmo computador e condições, possuindo menos amostras e não havendo testes com as matrizes de tamanho 2000x2000 e 4000x4000, e logo não refletem com exatidão as condições durante cada execução do experimento principal
   
2. A carga medida não reflete a porcentagem de uso de CPU, mas a média de tarefas executáveis/esperando CPU ao longo do tempo no último minuto;
   