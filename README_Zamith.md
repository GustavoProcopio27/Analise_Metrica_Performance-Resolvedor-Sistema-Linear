# Análise de Desempenho do Método de Jacobi com Linux perf

## Sumário
- [Análise de Desempenho do Método de Jacobi com Linux perf](#análise-de-desempenho-do-método-de-jacobi-com-linux-perf)
  - [Sumário](#sumário)
  - [1. Ambiente Experimental](#1-ambiente-experimental)
    - [1.1 Especificações dos Computadores](#11-especificações-dos-computadores)
    - [1.2 Condições Experimentais: Temperatura](#12-condições-experimentais-temperatura)
      - [PC Novo — AMD Ryzen 5 5600G](#pc-novo--amd-ryzen-5-5600g)
      - [PC Antigo — Intel Core i3-2120](#pc-antigo--intel-core-i3-2120)
    - [1.3 Condições Experimentais: Carga Média](#13-condições-experimentais-carga-média)
      - [PC Novo — AMD Ryzen 5 5600G](#pc-novo--amd-ryzen-5-5600g-1)
      - [PC Antigo — Intel Core i3-2120](#pc-antigo--intel-core-i3-2120-1)
    - [1.4 Processos em Execução](#14-processos-em-execução)
  - [2. Escopo do Experimento](#2-escopo-do-experimento)
    - [2.1 Níveis de Otimização](#21-níveis-de-otimização)
    - [2.2 Matrizes e Dimensões](#22-matrizes-e-dimensões)
    - [2.3 Protocolo e Comando de Coleta](#23-protocolo-e-comando-de-coleta)
  - [3. Documentação das Métricas de Desempenho](#3-documentação-das-métricas-de-desempenho)
    - [3.1 Eficiência do Pipeline — IPC e CPI](#31-eficiência-do-pipeline--ipc-e-cpi)
      - [1. Nome conceitual, eventos da PMU, unidade e significado arquitetural](#1-nome-conceitual-eventos-da-pmu-unidade-e-significado-arquitetural)
      - [2. Hipótese investigada](#2-hipótese-investigada)
      - [3. Justificativa de relevância para Jacobi e otimizações](#3-justificativa-de-relevância-para-jacobi-e-otimizações)
      - [4. Disponibilidade e comparabilidade entre máquinas (PMU)](#4-disponibilidade-e-comparabilidade-entre-máquinas-pmu)
      - [5. Fórmula de derivação](#5-fórmula-de-derivação)
    - [3.2 Taxa de Erros de Predição de Desvio — Branch Miss Rate](#32-taxa-de-erros-de-predição-de-desvio--branch-miss-rate)
      - [1. Nome conceitual, eventos da PMU, unidade e significado arquitetural](#1-nome-conceitual-eventos-da-pmu-unidade-e-significado-arquitetural-1)
      - [2. Hipótese investigada](#2-hipótese-investigada-1)
      - [3. Justificativa de relevância para Jacobi e otimizações](#3-justificativa-de-relevância-para-jacobi-e-otimizações-1)
      - [4. Disponibilidade e comparabilidade entre máquinas (PMU)](#4-disponibilidade-e-comparabilidade-entre-máquinas-pmu-1)
      - [5. Fórmula de derivação](#5-fórmula-de-derivação-1)
    - [3.3 Taxa de Erros de Acesso a Cache L3 — Cache Miss Rate](#33-taxa-de-erros-de-acesso-a-cache-l3--cache-miss-rate)
      - [1. Nome conceitual, eventos da PMU, unidade e significado arquitetural](#1-nome-conceitual-eventos-da-pmu-unidade-e-significado-arquitetural-2)
      - [2. Hipótese investigada](#2-hipótese-investigada-2)
      - [3. Justificativa de relevância para Jacobi e otimizações](#3-justificativa-de-relevância-para-jacobi-e-otimizações-2)
      - [4. Disponibilidade e comparabilidade entre máquinas (PMU)](#4-disponibilidade-e-comparabilidade-entre-máquinas-pmu-2)
      - [5. Fórmula de derivação](#5-fórmula-de-derivação-2)
    - [3.4 Tabela Síntese das Métricas](#34-tabela-síntese-das-métricas)
  - [4. Limitações Amostrais e Metodológicas](#4-limitações-amostrais-e-metodológicas)

---

## 1. Ambiente Experimental

### 1.1 Especificações dos Computadores

| Campo | Máquina Nova | Máquina Antiga |
| :--- | :--- | :--- |
| **Id Máquina** | `e7b7f49ddd09b1c0198869df64348520` | `e7b7f49ddd09b1c0198869df64348520` |
| **Hostname** | `lab08013` | `lab280867` |
| **Arquitetura** | x86-64 | x86-64 |
| **Processador** | AMD Ryzen 5 5600G with Radeon Graphics | Intel Core i3-2120 |
| **Geração da CPU** | Ryzen 5000 / Zen 3 (Cezanne) | 2ª geração Intel Core / Sandy Bridge |
| **Modelo da CPU** | Família 25, Modelo 80 | Família 6, Modelo 42 |
| **Núcleos Físicos** | 6 | 2 |
| **CPUs Lógicas (Threads)** | 12 | 4 |
| **Tamanho Cache L1** | L1d: 192 KiB (6×32 KiB) / L1i: 192 KiB (6×32 KiB) | L1d: 64 KiB (2×32 KiB) / L1i: 64 KiB (2×32 KiB) |
| **Tamanho Cache L2** | 3 MiB (6×512 KiB) | 512 KiB (2×256 KiB) |
| **Tamanho Cache L3** | 16 MiB (Compartilhado) | 3 MiB (Compartilhado) |
| **Memória Instalada** | 8 GB DDR4-2400 MT/s, 1×8 GB (Single-Channel) | 4 GB DDR3-1333, 2×2 GB 1333 MT/s (Dual-Channel) |
| **Sistema Operacional** | Ubuntu 22.04.1 LTS | Ubuntu 22.04.3 LTS |
| **Kernel** | Linux 6.8.0-138-generic | Linux 6.2.0-26-generic |
| **Versão GCC** | 11.4.0 | 11.4.0 |
| **Versão OpenMP** | 201511 (OpenMP 4.5) | 201511 (OpenMP 4.5) |
| **Versão Perf** | 6.8.12 | 6.8.13 |
| **Processador Híbrido** | Não | Não |
| **Hyper-Threading / SMT**| Suportado e Ativo | Suportado e Ativo |
| **Afinidade de CPU** | CPUs lógicas 0 e 1: núcleos físicos 0 e 1 | CPUs lógicas 0 e 1: núcleos físicos 0 e 1 |
| **Turbo / Boost** | Suportado e Ativo (Precision Boost) | Não Suportado (Clock fixo de 3.30 GHz) |

---

### 1.2 Condições Experimentais: Temperatura

O registro térmico e de carga foi conduzido nas mesmas máquinas sob matrizes $1000 \times 1000$, $3000 \times 3000$ e $5000 \times 5000$, viabilizando a caracterização do comportamento térmico sob estresse contínuo.

#### PC Novo — AMD Ryzen 5 5600G
| Otimização | Tamanho da Matriz | Temperatura Média (°C) | Desvio Padrão (°C) |
| :--- | :--- | :--- | :--- |
| **O0** | 1000 × 1000 | 40,40 | 0,40 |
| **O0** | 3000 × 3000 | 45,43 | 3,93 |
| **O0** | 5000 × 5000 | 52,03 | 1,82 |
| **O3** | 1000 × 1000 | 50,87 | 3,01 |
| **O3** | 3000 × 3000 | 45,17 | 0,67 |
| **O3** | 5000 × 5000 | 45,07 | 0,81 |
| **O3-native** | 1000 × 1000 | 44,77 | 1,36 |
| **O3-native** | 3000 × 3000 | 42,80 | 0,36 |
| **O3-native** | 5000 × 5000 | 44,50 | 0,89 |

* **O0:** Observa-se aquecimento progressivo com o aumento do volume de dados, culminando em 52,03 °C na matriz $5000 \times 5000$.
* **O3:** Apresentou temperatura média equilibrada em torno de 45 °C para matrizes grandes, com pico atípico no início dos testes ($1000 \times 1000$).
* **O3-native:** Manteve temperaturas estáveis entre 42,80 °C e 44,77 °C, com desvio padrão reduzido (0,36 °C para $3000 \times 3000$). O melhor agendamento e o uso de instruções nativas proporcionaram menor tempo sob pico de carga, mitigando o acúmulo térmico.

#### PC Antigo — Intel Core i3-2120
| Otimização | Tamanho da Matriz | Temp. Núcleo 1 Média (°C) | DP Núcleo 1 | Temp. Núcleo 2 Média (°C) | DP Núcleo 2 |
| :--- | :--- | :--- | :--- | :--- | :--- |
| **O0** | 1000 × 1000 | 38,33 | 0,58 | 38,33 | 0,58 |
| **O0** | 3000 × 3000 | 41,33 | 2,52 | 40,67 | 2,08 |
| **O0** | 5000 × 5000 | 45,67 | 4,04 | 45,67 | 4,04 |
| **O3** | 1000 × 1000 | 47,00 | 3,61 | 45,67 | 3,06 |
| **O3** | 3000 × 3000 | 47,33 | 3,21 | 46,33 | 2,52 |
| **O3** | 5000 × 5000 | 44,00 | 0,00 | 43,00 | 0,00 |
| **O3-native** | 1000 × 1000 | 47,33 | 2,52 | 47,33 | 2,52 |
| **O3-native** | 3000 × 3000 | 45,00 | 1,00 | 43,67 | 1,15 |
| **O3-native** | 5000 × 5000 | 45,00 | 1,73 | 44,00 | 1,73 |

* O PC Antigo apresentou temperaturas médias mais altas em `O3` e `O3-native` devido à maior ocupação das unidades funcionais por ciclo em relação ao `O0`.
* Ressalta-se que variações climáticas locais no laboratório (ex.: atuação do ar condicionado, fluxo de ar e abertura de portas) podem induzir pequenas flutuações experimentais.

---

### 1.3 Condições Experimentais: Carga Média

A carga média do sistema foi extraída via `/proc/loadavg` (janela móvel do último minuto), monitorando o número de tarefas ativas e concorrentes na fila do escalonador.

#### PC Novo — AMD Ryzen 5 5600G
| Otimização | Média 1000 | DP 1000 | Média 3000 | DP 3000 | Média 5000 | DP 5000 |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| **O0** | 0,79 | 0,18 | 0,75 | 0,03 | 0,91 | 0,05 |
| **O3** | 1,97 | 0,31 | 1,91 | 0,12 | 1,72 | 0,09 |
| **O3-native** | 1,44 | 0,12 | 1,12 | 0,09 | 0,87 | 0,07 |

#### PC Antigo — Intel Core i3-2120
| Otimização | Média 1000 | DP 1000 | Média 3000 | DP 3000 | Média 5000 | DP 5000 |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| **O0** | 1,90 | 0,16 | 1,51 | 0,09 | 2,29 | 0,50 |
| **O3** | 2,17 | 0,14 | 2,32 | 0,28 | 2,20 | 0,11 |
| **O3-native** | 2,07 | 0,11 | 1,82 | 0,02 | 1,84 | 0,37 |

---

### 1.4 Processos em Execução
Durante a execução de todos os testes, o ambiente manteve-se padronizado com os seguintes processos de usuário ativos:
1. Visual Studio Code (VS Code);
2. Mozilla Firefox;
3. Serviços padrão em background do sistema operacional Ubuntu.

---

## 2. Escopo do Experimento

### 2.1 Níveis de Otimização
* **`O0`:** Otimizações do compilador desativadas. O código em C é traduzido diretamente em instruções escalares com frequentes acessos redundantes à pilha, servindo como linha de base (*baseline*).
* **`O3`:** Otimização agressiva com fusão de funções (*inlining*), eliminação de código morto, escalonamento avançado de instruções, propagação de constantes, desenrolamento de laços (*loop unrolling*) e auto-vetorização genérica.
* **`O3-native`:** Agrega ao nível `O3` a flag `-march=native`, instruindo o compilador a emitir instruções e registradores vetoriais específicos suportados pela microarquitetura do hospedeiro (ex.: extensões AVX2 e FMA no Ryzen 5 5600G).

### 2.2 Matrizes e Dimensões
* **Dimensões analisadas:** $1000 \times 1000$, $2000 \times 2000$, $3000 \times 3000$, $4000 \times 4000$ e $5000 \times 5000$.
* **Amostragem:** 10 repetições por configuração experimental:
  $$\text{Total} = 2 \text{ máquinas} \times 3 \text{ níveis de otimização} \times 5 \text{ tamanhos de matriz} \times 10 \text{ repetições} = 300 \text{ execuções}$$
* **Paralelismo:** Restrito a 2 threads OpenMP vinculadas às CPUs lógicas 0 e 1 via `taskset -c 0,1`.

### 2.3 Protocolo e Comando de Coleta
```bash
OMP_NUM_THREADS=2 OMP_DYNAMIC=FALSE perf stat -e cycles,instructions,\
branches,branch-misses,\
cache-references,cache-misses -o ${destiny} \
taskset -c 0,1 ${executable} 1E-10 0 ${mat1} ${mat2} ${saida}
```

* **`OMP_NUM_THREADS=2` e `OMP_DYNAMIC=FALSE`:** Impede que o runtime OpenMP crie mais threads ou reduza a quantidade dinamicamente.
* **`taskset -c 0,1`:** Garante afinidade de CPU (*CPU affinity*), vinculando as threads aos núcleos lógicos 0 e 1 e eliminando o overhead de migração de contexto pelo escalonador.
* **`${executable}`:** Binário correspondente (`solver-jacobi-mt-O0.exec`, `solver-jacobi-mt-O3.exec`, `solver-jacobi-mt-O3-native.exec`).
* **`1E-10`:** Critério de tolerância residual ($\varepsilon = 10^{-10}$) para validação da convergência numérica.
* **`0`:** Desabilita a impressão detalhada do erro a cada passo na saída padrão.
* **`${mat1}` e `${mat2}`:** Arquivos binários contendo a matriz de coeficientes $A$ e o vetor independente $B$.
* **`${saida}`:** Arquivo binário de saída onde é gravado o vetor solução $X$.
* **`-o ${destiny}`:** Arquivo de texto que armazena as saídas brutas do `perf stat`.

---

## 3. Documentação das Métricas de Desempenho

---

### 3.1 Eficiência do Pipeline — IPC e CPI

#### 1. Nome conceitual, eventos da PMU, unidade e significado arquitetural
* **Nome conceitual:** Eficiência de Processamento do Pipeline — Instruções por Ciclo (*Instructions Per Cycle* - IPC) e Ciclos por Instrução (*Cycles Per Instruction* - CPI).
* **Eventos da PMU / Sintaxe `perf`:** `cycles` e `instructions` (ou métrica derivada `-M ipc` / `-M cpi`).
* **Unidade:** Adimensional (instruções/ciclo para IPC; ciclos/instrução para CPI).
* **Significado arquitetural:** Processadores x86-64 modernos são superescalares e operam fora de ordem (*out-of-order*). Possuem múltiplas portas de execução capazes de decodificar e aposentar entre 4 e 8 instruções por ciclo de clock.
  * O **IPC** mede a vazão efetiva (*throughput*): valores elevados (> 1.5 a 2.5) indicam que as unidades funcionais (ALUs, FPUs, registradores vetoriais) estão operando continuamente desobstruídas.
  * O **CPI** é o inverso direto do IPC ($CPI = 1 / IPC$) e representa o custo médio em ciclos para aposentar cada instrução.
  * IPC baixo (≤ 1.0 ou ≤ 0.5) revela a ocorrência de bolhas no pipeline (*pipeline stalls*), onde os ciclos de clock avançam enquanto as portas de despacho permanecem bloqueadas aguardando a chegada de dados da hierarquia de memória (*memory-bound stalls*) ou a resolução de dependências lógicas.

#### 2. Hipótese investigada
Espera-se que o IPC nominal sofra alterações expressivas entre as otimizações `O0`, `O3` e `O3-native`. Em `O3` e `O3-native`, a presença de vetorização automática (SIMD — *Single Instruction, Multiple Data*) permite que uma única instrução opere sobre múltiplos dados simultaneamente. Na máquina AMD Zen 3, extensões como AVX2 e FMA permitem processar 4 números de precisão dupla (`double`, 256 bits) em uma única instrução vetorial, reduzindo drasticamente o volume bruto de instruções necessárias para resolver o sistema.

#### 3. Justificativa de relevância para Jacobi e otimizações
No método de Jacobi, a atualização de cada incógnita $x_i$ depende do produto interno da linha correspondente da matriz $A$ pelo vetor de estimativas anteriores $x_0$:
$$x_i^{(k+1)} = \frac{1}{A[i][i]} \left( B[i] - \sum_{j \ne i} A[i][j] x_j^{(k)} \right)$$
* Na versão `O0`, o compilador gera acessos escalares repetidos à pilha e à memória para carregar valores intermediários, resultando em um alto volume de instruções redundantes.
* A análise do IPC é fundamental porque o tempo de execução é regido pela relação clássica:
  $$Tempo = \frac{\text{Instruções}}{\text{IPC} \times \text{Frequência}} = \text{Instruções} \times \text{CPI} \times \text{Período de Clock}$$
* Quando a vetorização atua em `O3` e `O3-native`, o número absoluto de instruções despenca (ex.: queda de $\approx 3,5$ bilhões para $\approx 900$ milhões em $N=1000$). Como instruções vetoriais demandam mais estágios e realizam o trabalho equivalente a múltiplas instruções escalares, o IPC pode se manter estável ou até cair ligeiramente. A métrica comprova que a aceleração decorre da redução do total de instruções úteis executadas, e não de um mero aumento na frequência de despacho de instruções escalares.

#### 4. Disponibilidade e comparabilidade entre máquinas (PMU)
* **Disponibilidade:** Os eventos `cycles` e `instructions` são universais e contidos nos contadores arquiteturais básicos em arquiteturas Intel e AMD.
* **Diferenças semânticas na PMU:**
  * `instructions`: O evento monitora instruções confirmadas/aposentadas (*retired*), descartando instruções executadas sob ramos especulativos incorretos. Entretanto, o compilador emite instruções distintas para a AMD Zen 3 (suporte a AVX2/FMA3 de 256 bits) e para a Intel Sandy Bridge (limitada a instruções escalares ou AVX de 1ª geração sem FMA). Adicionalmente, técnicas de *macro-fusion* diferem entre as gerações.
  * `cycles`: Mede ciclos não parados (`CPU_CLK_UNHALTED`). No Core i3-2120, a frequência é nominalmente estática (3,30 GHz, sem Turbo Boost). No Ryzen 5 5600G, a frequência é dinâmica (Precision Boost ativo, variando entre 3,9 e 4,4 GHz). Assim, comparações absolutas de ciclos entre as duas máquinas são desprovidas de base isomórfica, devendo-se comparar o *speedup* e ganhos relativos.
* **Limitações da PMU:** Devido à requisição de 6 eventos simultâneos para uma PMU de 4 contadores de propósito geral, o `perf` operou com **multiplexação temporal** ($\approx 83\%$ do tempo ativo por evento), estimando os totais por extrapolação linear. O uso do sufixo `:u` (`cycles:u`, `instructions:u`) filtrou o ruído de chamadas ao kernel, isolando a computação do espaço de usuário.

#### 5. Fórmula de derivação
$$\text{IPC} = \frac{\text{instructions}}{\text{cycles}} \quad \Longleftrightarrow \quad \text{CPI} = \frac{\text{cycles}}{\text{instructions}}$$

---

### 3.2 Taxa de Erros de Predição de Desvio — Branch Miss Rate

#### 1. Nome conceitual, eventos da PMU, unidade e significado arquitetural
* **Nome conceitual:** Taxa de Erro de Predição de Desvios (*Branch Misprediction Rate*).
* **Eventos da PMU / Sintaxe `perf`:** `branches` e `branch-misses` (ou `-M branch-miss-rate`).
* **Unidade:** Porcentagem (%) ou taxa fracionária.
* **Significado arquitetural:** Para evitar que o pipeline congele a cada instrução de controle de fluxo condicional (`jcc`, `jmp`, `call`, `ret`), processadores utilizam uma unidade especializada de hardware — o **Preditor de Desvios (*Branch Predictor*)** — composta por tabelas de histórico (*Branch History Table* - BHT, *Branch Target Buffer* - BTB e preditores neurais/TAGE).
  * **Acerto (*Branch Hit*):** O processador alimenta o pipeline com as instruções especulativas do fluxo correto sem descontinuidade.
  * **Erro (*Branch Miss*):** O processador detecta o erro de salto, descarta todas as instruções calculadas especulativamente (*pipeline flush*) e reinicia a busca a partir do endereço correto, impondo uma penalidade de **10 a 20+ ciclos de clock** por erro.

#### 2. Hipótese investigada
Espera-se que o experimento registre baixa taxa de erros de predição de desvios (< 1%), uma vez que o método de Jacobi é composto essencialmente por laços aninhados regulares de contagem fixa ($N \times N$), conforme demonstrado no trecho central do código:

```c
#pragma omp parallel private(aux, div) shared (x0, x1, A, B, error, err, show, flag)
{
    do {
        // Parte 1: Resolve equações
        #pragma omp for
        for (unsigned int j = 0; j < A->m; j++) {
            aux = 0.0;
            div = 0.0;
            for (unsigned int i = 0; i < A->n; i++) {
                if (j != i)
                    aux += (A->vetor[A->n * j + i] * x0[i]);
                else
                    div = A->vetor[A->n * j + i];
            }
            x1[j] = (B->vetor[j] - aux) / div;
        }

        // Parte 2: Critério de parada do método
        #pragma omp for reduction(max:err)
        for (unsigned int j = 0; j < A->n; j++) {
            double b = fabs((x1[j] - x0[j]) / (x1[j] + EPSILON));
            if (b > err)
                err = b;
        }

        // Parte 3: Atualização e swap de ponteiros
        #pragma omp single
        {
            double *swap = x0;
            x0 = x1;
            x1 = swap;
            inter++;
            flag = (err > error);
            err = 0.0f;
        }
        #pragma omp barrier
    } while (flag);
}
```

#### 3. Justificativa de relevância para Jacobi e otimizações
* No laço `for (unsigned int i = 0; i < A->n; i++)`, a condição de repetição é verdadeira centenas ou milhares de vezes consecutivas e falsa em apenas uma ocorrência por linha. As tabelas de histórico aprendem esse padrão quase imediatamente, assegurando altíssima precisão de predição.
* A condição de convergência do laço externo (`while (flag)`) é avaliada apenas uma vez por iteração global da matriz, de forma que eventuais falhas nesse desfecho exercem impacto estatístico desprezível sobre a métrica global.
* Em `O3` e `O3-native`, o desenrolamento de laço (*unrolling*) reduz a frequência física de saltos no código binário, cortando a contagem de `branches` praticamente pela metade em relação ao `O0` e aliviando as consultas às tabelas do preditor.

#### 4. Disponibilidade e comparabilidade entre máquinas (PMU)
* **Disponibilidade:** Os contadores `branches` e `branch-misses` estão presentes nas PMUs de ambas as máquinas.
* **Composição do evento:** O contador genérico agrega todos os ramos arquiteturais validados (saltos condicionais, incondicionais, chamadas e retornos).
* **Diferenças na PMU e preditores:** O Ryzen 5 5600G (Zen 3) implementa um preditor TAGE complexo com suporte a histórico longo e buffers consideravelmente maiores do que o preditor de 2 níveis da Sandy Bridge (2011). Isso faz com que taxas residuais de miss ligeiramente menores no PC Novo reflitam o avanço da microarquitetura, e não propriedades algorítmicas.
* **Afinidade (`taskset -c 0,1`):** Como as CPUs lógicas 0 e 1 foram mapeadas para núcleos físicos distintos (núcleos 0 e 1) em ambas as máquinas, as threads não concorreram pelos buffers físicos de histórico de salto (BTB), operando sem interferência mútua de predição.

#### 5. Fórmula de derivação
$$\text{Branch Miss Rate} = \left( \frac{\text{branch-misses}}{\text{branches}} \right) \times 100\$$

---

### 3.3 Taxa de Erros de Acesso a Cache L3 — Cache Miss Rate

#### 1. Nome conceitual, eventos da PMU, unidade e significado arquitetural
* **Nome conceitual:** Taxa de Perdas de Cache de Último Nível (*Last Level Cache Miss Rate* / LLC Miss Rate).
* **Eventos da PMU / Sintaxe `perf`:** `cache-references` e `cache-misses` (ou `-M cache-miss-rate`).
* **Unidade:** Porcentagem (%) ou razão fracionária.
* **Significado arquitetural:** A hierarquia de memória atenua a disparidade de velocidade entre o processador e a memória RAM intermediando dados em múltiplos níveis de cache (L1, L2 e L3/LLC).
  * No Linux `perf`, `cache-references` e `cache-misses` monitoram o **cache de último nível (L3)**.
  * O evento `cache-references` contabiliza as requisições que falharam nas caches privativas L1 e L2 e foram encaminhadas à L3.
  * O evento `cache-misses` indica requisições que falharam também na L3, forçando o acesso direto à memória principal (DRAM).
  * Um acesso à DRAM impõe uma penalidade massiva de latência (**50 a 80+ nanosegundos**, equivalendo a centenas de ciclos de CPU ociosos), além de saturar a largura de banda do barramento de dados.

#### 2. Hipótese investigada
O método de Jacobi é tipicamente uma aplicação **limitada por memória (*memory-bound*)**, apresentando baixa intensidade aritmética (poucas operações de ponto flutuante por elemento trafegado).
* Para matrizes de ordem $N$, a matriz de coeficientes $A$ requer $N^2 \times 8$ bytes em precisão dupla (`double`).
* Conforme $N$ cresce de $1000$ para $5000$, o tamanho da matriz varia de $\approx 8\text{ MB}$ até $\approx 200\text{ MB}$. Como as capacidades de cache L3 típicas são de 3 MiB (PC Antigo) e 16 MiB (PC Novo), **a matriz de dados excede a capacidade física de armazenamento da L3**, forçando contínuos recarregamentos da DRAM a cada iteração do método e estabelecendo a memória como principal gargalo.

#### 3. Justificativa de relevância para Jacobi e otimizações
* A intensidade aritmética do Jacobi é extremamente reduzida: para cada elemento de 8 bytes de $A[n \times j + i]$ carregado da memória, executa-se apenas uma multiplicação e uma adição ($aux += A \times x_0$).
* No laço `do...while (flag)`, cada iteração completa revisita todas as $N \times N$ posições da matriz:
  * Em $N=1000$: $A$ consome $\approx 8\text{ MB}$;
  * Em $N=3000$: $A$ consome $\approx 72\text{ MB}$;
  * Em $N=5000$: $A$ consome $\approx 200\text{ MB}$.
* Quando a matriz ultrapassa a capacidade de armazenamento da L3, os dados são sistematicamente expulsos para a DRAM. A medição da taxa de perdas de cache L3 é, portanto, indispensável para identificar a transição da aplicação: de um regime com bom aproveitamento de cache nas matrizes pequenas para um regime estritamente limitado pela largura de banda de memória (*memory-bound*) nas matrizes maiores.

#### 4. Disponibilidade e comparabilidade entre máquinas (PMU)
* **Disponibilidade:** Os eventos genéricos `cache-references` e `cache-misses` são disponibilizados pelo `perf` para ambas as plataformas x86.
* **Diferenças semânticas na PMU:**
  * Na Intel Sandy Bridge, mapeia-se `LONGEST_LAT_CACHE.REFERENCE` e `LONGEST_LAT_CACHE.MISS`.
  * Na AMD Zen 3, monitora-se requisições no Core Complex (L3) e no Data Fabric. As camadas físicas e regras de filtragem diferem entre os fabricantes.
* **Disparidade de capacidade física:** O PC Antigo possui apenas **3 MiB de cache L3**, enquanto o PC Novo dispõe de **16 MiB de cache L3** (capacidade 5,3 vezes superior). Uma matriz de $1000 \times 1000$ ($\approx 8\text{ MB}$) cabe confortavelmente na L3 do Ryzen (junto aos vetores auxiliares), mas transborda inteiramente a L3 do Core i3. Logo, o menor número de misses no PC Novo reflete primordialmente a especificação do silício, e não mérito algorítmico.
* **Prefetchers e Barramento:** O PC Novo utiliza barramento DDR4-2400 (maior taxa de transferência) e circuitos de pré-busca (*hardware prefetchers*) muito mais agressivos da arquitetura Zen 3, que identificam com eficiência a varredura contínua de linhas em C (*row-major*). O PC Antigo opera com DDR3-1333 e pré-buscadores de geração anterior.
* **Afinidade (`taskset -c 0,1`):** A execução vinculada a dois núcleos físicos distintos garantiu que cada thread operasse com suas próprias caches L1 e L2 privativas, dividindo apenas o pool compartilhado da L3.

#### 5. Fórmula de derivação
$$\text{Cache Miss Rate} = \left( \frac{\text{cache-misses}}{\text{cache-references}} \right) \times 100\$$

---

### 3.4 Tabela Síntese das Métricas

| Métrica | Eventos Base (`perf`) | Expressão Derivada | Dimensão Avaliada no `solver-jacobi-mt` | Limitação Metodológica / PMU |
| :--- | :--- | :--- | :--- | :--- |
| **Eficiência do Pipeline (IPC / CPI)** | `cycles:u`, `instructions:u` | $\text{IPC} = \frac{\text{instructions}}{\text{cycles}}$ | A vetorização (`O3`/`native`) reduz instruções totais em até 74%, encurtando o tempo mesmo com IPC nominal similar. | Multiplexação temporal de contadores ($\approx 83\%$) e variação dinâmica de frequência de clock. |
| **Branch Miss Rate** | `branches`, `branch-misses:u` | $\frac{\text{branch-misses}}{\text{branches}} \times 100\$ | Laços regulares apresentam erro $< 0,3\%$; o desenrolamento em `O3` reduz saltos totais. | Diferença de sofisticação dos preditores (Zen 3 TAGE vs. Sandy Bridge); mitigação de concorrência com núcleos físicos dedicados. |
| **Cache Miss Rate** | `cache-references`, `cache-misses` | $\frac{\text{cache-misses}}{\text{cache-references}} \times 100\$ | Matrizes com $N \ge 2000$ extrapolam a L3 ($> 16\text{ MB}$), tornando Jacobi estritamente *memory-bound*. | Grande disparidade na capacidade física da L3 (16 MiB vs. 3 MiB) e agressividade dos *hardware prefetchers*. |

---

## 4. Limitações Amostrais e Metodológicas

1. **Separação de Medições de Temperatura e Carga:** O registro de temperatura e carga de CPU foi conduzido posteriormente ao experimento principal nas mesmas máquinas e sob condições controladas, cobrindo as dimensões $1000 \times 1000$, $3000 \times 3000$ e $5000 \times 5000$. Portanto, expressam o comportamento térmico sob carga, mas não refletem com exatidão instantânea cada uma das execuções do conjunto de dados principal.
2. **Semântica da Métrica de Carga:** A carga obtida via `/proc/loadavg` quantifica o número médio de tarefas executáveis ou aguardando CPU no último minuto, não correspondendo linearmente à porcentagem instantânea de utilização de CPU.
3. **Escopo do Monitoramento (`perf stat`):** O utilitário monitorou todo o ciclo de vida do processo, englobando a fase de E/S de leitura e escrita das matrizes binárias em disco.
4. **Multiplexação de Contadores:** Pela requisição simultânea de 6 eventos em PMUs com 4 contadores de propósito geral, o `perf` operou com amostragem ponderada no tempo ($\approx 83\%$), extrapolando linearmente as contagens brutas.
