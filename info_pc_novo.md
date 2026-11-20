## Identificação 
Hostname: lab08013
Machine ID: e7b7f49ddd09b1c0198869df64348520
Arquitetura: x86-64

## CPU
Processador: AMD Ryzen 5 5600G with Radeon Graphics
Geração / arquitetura: Ryzen 5000 / Zen 3 (Cezanne)
Família: AMD Family 25
Modelo: 80
Núcleos fisicos: 6
CPUS Lógicas: 12
Processador híbrido:	Não
SMT (Simultaneous Multithreading): Sim
Frequência mínima informada	400 MHz
Frequência máxima informada	4464 MHz
Turbo / Boost	Suportado pelo processador

## Hierarquia de memória cache
Cache	Capacidade	Instâncias
L1d	     192 KiB	   6 (32 KiB cada)
L1i      192 KiB	   6 (32 KiB cada)
L2	      3 MiB	       6 
L3	      16 MiB	   1

## Memória RAM
Capacidade instalada	8 GB
Fabricante	Kingston
Serial Number: 7A1C4EA3
Tecnologia	DDR4
Velocidade configurada	2400 MT/s
Propriedade	Valor
Capacidade instalada	8 GB
Fabricante	Kingston
Tecnologia	DDR4
Velocidade configurada	2400 MT/s
Módulos identificados	1 × 8 GB
Largura de dados	64 bits
Swap	Aproximadamente 2 GiB

## Sistema operacional e ferramentas
Operating System: Ubuntu 22.04.1 LTS <!-- 2023.06.06 LTS (Cubic 2023-06-07 17:58) -->
Kernel: Linux 6.8.0-138-generic
GCC 11.4.0
OpenMP (_OPENMP)	201511 — OpenMP 4.5
Perf	6.8.12


	

edia/admin/SUB-MEMORY/trabalho-arq/experimentos on main !310 ?11 ·················· with admin@lab08013 at 18:08:43
❯ cpupower frequency-info                                                      
analyzing CPU 5:
  driver: amd-pstate-epp
  CPUs which run at the same hardware frequency: 5
  CPUs which need to have their frequency coordinated by software: 5
  maximum transition latency:  Cannot determine or is not supported.
  hardware limits: 400 MHz - 4.46 GHz
  available cpufreq governors: performance powersave
  current policy: frequency should be within 400 MHz and 4.46 GHz.
                  The governor "powersave" may decide which speed to use
                  within this range.
  current CPU frequency: Unable to call hardware
  current CPU frequency: 4.44 GHz (asserted by call to kernel)
  boost state support:
    Supported: yes
    Active: yes
    AMD PSTATE Highest Performance: 166. Maximum Frequency: 4.46 GHz.
    AMD PSTATE Nominal Performance: 145. Nominal Frequency: 3.90 GHz.
    AMD PSTATE Lowest Non-linear Performance: 88. Lowest Non-linear Frequency: 2.37 GHz.
    AMD PSTATE Lowest Performance: 15. Lowest Frequency: 400 MHz.

/media/admin/SUB-MEMORY/trabalho-arq/experimentos on main !310 ?11 ·················· with admin@lab08013 at 18:08:56
❯ 
 cat /sys/devices/system/cpu/cpu0/cpufreq/scaling_governor
powersave


 taskset -pc $$                                           
atual lista de afinidade do pid 4403: 0-11
❯ uptime  
 18:10:37 up 3 min,  1 user,  load average: 0,58, 0,50, 0,21

 ❯ vmstat 1 5 
procs -----------memória--------- ---swap-- ----e/s---- -sistema- ------cpu-----
 r  b   swpd  livre   buff  cache   si   so    bi    bo   in   cs us sy id wa st
 3  1      0 2311068 104736 2329072    0    0   585    97  527  631  3  1 95  1  0
 0  0      0 2291876 104756 2331372    0    0     0    84 2299 2994  1  0 99  0  0
 0  0      0 2295028 104756 2331372    0    0     0     0 2097 2528  1  0 99  0  0
 0  0      0 2297136 104756 2331372    0    0     0     0 2278 3099  1  0 99  0  0
 0  0      0 2296668 104756 2331372    0    0     0     0 3189 4226  1  0 99  0  0

ls /sys/bus/event_source/devices/ 
amd_iommu_0  breakpoint  cpu  ibs_fetch  ibs_op  kprobe  msr  power  software  tracepoint  uprobe


 ❯ lscpu -e=CPU,CORE,SOCKET,NODE
CPU CORE SOCKET NODE
  0    0      0    0
  1    1      0    0
  2    2      0    0
  3    3      0    0
  4    4      0    0
  5    5      0    0
  6    0      0    0
  7    1      0    0
  8    2      0    0
  9    3      0    0
 10    4      0    0
 11    5      0    0


 