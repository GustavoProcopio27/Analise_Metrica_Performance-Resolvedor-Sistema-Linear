## Identificação 
Hostname: lab280867
Machine ID: e7b7f49ddd09b1c0198869df64348520
Arquitetura: x86-64

## CPU
Processador: Intel Core i3-2120
Geração / arquitetura: 2ª geração Intel Core / Sandy Bridge
Família: 6
Modelo: 42
Núcleos fisicos: 2
CPUS Lógicas: 4
Processador híbrido:	Não
Hyper-Threading	Sim
Frequência mínima informada	1600 MHz
Frequência máxima informada	3300 MHz
Turbo Boost	Não suportado

Topologia: 
????
????
????



## Hierarquia de memória cache
Cache	Capacidade	Instâncias
L1d	      64 KiB	   2
L1i	      64 KiB	   2
L2	      512 KiB	   2
L3	       3 MiB	   1

## Memória RAM
Capacidade instalada	4 GB
Módulos	2 × 2 GB ([Bank Locator: BANK 1 ChannelA-DIMM1] - [Bank Locator: BANK 3 Locator: ChannelB-DIMM1] )
Fabricante	8502 (campo manufacturer no dmidecode -t memory)
Serial Number: 00000000
Tecnologia	DDR3
Velocidade configurada	1333 MT/s
Largura de dados	64 bits por módulo
Swap	Aproximadamente 2 GiB

## Sistema operacional e ferramentas
Operating System: Ubuntu 22.04.3 LTS <!-- 2023.06.06 LTS (Cubic 2023-06-07 17:58) -->
Kernel: Linux 6.2.0-26-generic
GCC 11.4.0
OpenMP (_OPENMP)	201511 — OpenMP 4.5
Perf	6.8.13


	

cpupower frequency-info
analyzing CPU 0:
  driver: intel_cpufreq
  CPUs which run at the same hardware frequency: 0
  CPUs which need to have their frequency coordinated by software: 0
  maximum transition latency: 20.0 us
  hardware limits: 1.60 GHz - 3.30 GHz
  available cpufreq governors: conservative ondemand userspace powersave performance schedutil
  current policy: frequency should be within 1.60 GHz and 3.30 GHz.
                  The governor "schedutil" may decide which speed to use
                  within this range.
  current CPU frequency: Unable to call hardware
  current CPU frequency: 1.60 GHz (asserted by call to kernel)
  boost state support:
    Supported: no
    Active: no
    25500 MHz max turbo 4 active cores
    25500 MHz max turbo 3 active cores
    25500 MHz max turbo 2 active cores
    25500 MHz max turbo 1 active cores

    cat /sys/devices/system/cpu/cpu0/cpufreq/scaling_governor
schedutil


cat /sys/devices/system/cpu/intel_pstate/no_turbo
1

Em repouso:
 taskset -pc $$
atual lista de afinidade do pid 3960: 0-3

uptime
 14:29:55 up 23 min,  1 user,  load average: 0,56, 1,39, 1,73

 vmstat 1 5
procs -----------memória--------- ---swap-- ----e/s---- -sistema- ------cpu-----
 r  b   swpd  livre   buff  cache   si   so    bi    bo   in   cs us sy id wa st
 1  1 780112 728248  33892 1045100    5  142   332   296 5343 2892 15  7 63 15  0
 1  0 780112 726372  33900 1047272    0    0     0   880 4610 9478  4  3 92  1  0
 0  0 780112 730224  33908 1045096    0    0     0    36 2663 6161  7  3 89  1  0
 1  0 780112 728696  33908 1045096    0    0     0     0 1561 3231  8  3 90  0  0
 0  0 780112 727976  33908 1045100   32    0    32     0 3582 5802 13  2 84  1  0

  ls /sys/bus/event_source/devices/
breakpoint  cstate_core  kprobe  power     tracepoint  uncore_cbox_0  uncore_imc
cpu         cstate_pkg   msr     software  uncore_arb  uncore_cbox_1  uprobe

 lscpu -e=CPU,CORE,SOCKET,NODE
CPU CORE SOCKET NODE
  0    0      0    0
  1    1      0    0
  2    0      0    0
  3    1      0    0
