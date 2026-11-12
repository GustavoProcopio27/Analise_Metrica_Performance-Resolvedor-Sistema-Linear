### task-clock: Representa o tempo durante o qual a tarefa (processo) esteve efetivamente utilizando a CPU
    É importante observar que esse valor não necessariamente corresponde ao tempo de relógio. Se o processo ficar esperando I/O, for interrompido pelo sistema operacional ou ficar aguardando escalonamento, esse tempo não será contabilizado como execução efetiva na CPU.

### time elapsed: Tempo total decorrido (Wall-clock time)
Representa o tempo real entre o início e o término da execução. Diferentemente do task-clock, ele inclui todo o tempo decorrido, inclusive períodos em que o processo ficou aguardando ou sem executar na CPU.
É a métrica mais próxima do tempo que você perceberia utilizando um cronômetro para medir a execução do programa.

### seconds user — Tempo de CPU em modo usuário
Representa o tempo que o processo passou executando código em modo usuário (user mode).
É o tempo gasto executando as instruções do próprio programa, como:
- Operações matemáticas.
- Laços de repetição.
- Acessos a variáveis.
- Chamadas de funções executadas em espaço de usuário.


### seconds sys — Tempo de CPU em modo kernel
Representa o tempo que o processo passou executando código do sistema operacional em modo kernel (kernel mode). Pode incluir atividades como:
- Chamadas de sistema (syscalls).
- Operações de leitura e escrita em arquivos.
- Gerenciamento de memória.
- Operações relacionadas a threads e processos.



# Metricas escolhidas: 
Metricas são uma contagem de evento, ou uma medida derivada de eventos do perf


1. ##  IPC/CPI

2. ## (Branch Miss Rate) Taxa de Erro de Predição de Desvio    ->Erros de Predição de desvio branch-misses e branches

3. ## (Cache Miss Rate) Taxa de Falta de Cache                -> Referências e faltas de cache: `cache-references` e `cache-misses`