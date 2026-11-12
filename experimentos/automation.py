from subprocess import run
from string import Template
from time import sleep
import shutil
from enum import Enum




"""
    ❯ OMP_NUM_THREADS=4 OMP_DYNAMIC=FALSE perf stat -e task-clock,cycles,instructions,branches,branch-misses,cpu-migrations,context-switches,cache-references,cache-misses,major-faults,minor-faults,page-faults,dTLB-loads,dTLB-load-misses,dTLB-stores,dTLB-store-misses,iTLB-loads,iTLB-load-misses -o teste.txt taskset -c 0 solver-jacobi-mt-03.exec 1E-10 0 fontes/A1000.bin fontes/B1000.bin saida-teste.bin
testar isso daqui a pouco, e ver a porcentagem ao lado

"""

class TipoPC(Enum):
    NOVO=0
    ANTIGO=1



OTMIZATION_LEVELS = (
    ("../fontes/solver-jacobi-mt-O0.exec", "otimizacao-O0", "00"),
    ("../fontes/solver-jacobi-mt-O3.exec","otimizacao-03", "03"),
    ("../fontes/solver-jacobi-mt-O3-native.exec", "otimizacao-03-native","03-native"),
    )
 
PC_ATUAL:dict[str, TipoPC]={
    "novo":TipoPC.NOVO.value,
    "antigo":TipoPC.ANTIGO.value
}
    
MATRIXS = [ 
            ("../fontes/A1000.bin","../fontes/B1000.bin","1000"),
            ("../fontes/A2000.bin","../fontes/B2000.bin","2000"),
            ("../fontes/A3000.bin","../fontes/B3000.bin","3000"),
            ("../fontes/A4000.bin","../fontes/B4000.bin","4000"),
            ("../fontes/A5000.bin","../fontes/B5000.bin","5000")
        ]
    
command_template: Template = Template("OMP_NUM_THREADS=2 OMP_DYNAMIC=FALSE perf stat -e task-clock,cycles,instructions,"\
                        "branches,branch-misses,cpu-migrations,context-switches,cache-references,cache-misses,"\
                        "major-faults,minor-faults,page-faults -o ${destiny} "\
                        "taskset -c ${cores} ${executable} 1E-10 0 ${mat1} ${mat2} ${saida}")

for exec, folder, otimization_level in OTMIZATION_LEVELS:
    for matriz_A, matriz_B, sizes in MATRIXS:
        for i in range(1,11):
            command:str = command_template.substitute(
                                                        mat1=matriz_A,
                                                        mat2=matriz_B,
                                                        saida=f"{folder}/solution_{otimization_level}_{sizes}_{i}.bin",
                                                        destiny=f"{folder}/metrics_otimization{otimization_level}_{sizes}_{i}.txt",
                                                        cores="0,1",
                                                        executable=exec
                                                    )
            print(f"running: {command}")
            run(command, shell=True, check=True)
            sleep(4)
    
utilized_pc:str = input("Qual computador foi utilizado no experimento? ")

if PC_ATUAL[utilized_pc] == TipoPC.NOVO.value:
    shutil.move("otimizacao-00", "pc_novo")
    shutil.move("otimizacao-03","pc_novo")
    shutil.move("otimizacao-03-native","pc_novo")
else:
    shutil.move("otimizacao-00", "pc_antigo")
    shutil.move("otimizacao-03", "pc_antigo")
    shutil.move("otimizacao-03-native", "pc_antigo")