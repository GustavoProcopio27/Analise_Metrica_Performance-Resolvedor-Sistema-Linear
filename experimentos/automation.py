import os
import shutil
from enum import Enum
from string import Template
from subprocess import run
from time import sleep


class TipoPC(Enum):
    NOVO = 0
    ANTIGO = 1


os.mkdir("otimizacao-00")
os.mkdir("otimizacao-03")
os.mkdir("otimizacao-03-native")

OTMIZATION_LEVELS = (
    ("../fontes/solver-jacobi-mt-O0.exec", "otimizacao-00", "00"),
    ("../fontes/solver-jacobi-mt-O3.exec", "otimizacao-03", "03"),
    ("../fontes/solver-jacobi-mt-O3-native.exec", "otimizacao-03-native", "03-native"),
)

PC_ATUAL: dict[str, TipoPC] = {"novo": TipoPC.NOVO.value, "antigo": TipoPC.ANTIGO.value}

MATRIXS = [
    ("../fontes/A1000.bin", "../fontes/B1000.bin", "1000"),
    ("../fontes/A2000.bin", "../fontes/B2000.bin", "2000"),
    ("../fontes/A3000.bin", "../fontes/B3000.bin", "3000"),
    ("../fontes/A4000.bin", "../fontes/B4000.bin", "4000"),
    ("../fontes/A5000.bin", "../fontes/B5000.bin", "5000"),
]

command_template: Template = Template(
    "OMP_NUM_THREADS=2 OMP_DYNAMIC=FALSE perf stat -e cycles,instructions,"
    "branches,branch-misses,"
    "cache-references,cache-misses -o ${destiny} "
    "taskset -c ${cores} ${executable} 1E-10 0 ${mat1} ${mat2} ${saida}"
)

for exec, folder, otimization_level in OTMIZATION_LEVELS:
    for matriz_A, matriz_B, sizes in MATRIXS:
        for i in range(1, 11):
            command: str = command_template.substitute(
                mat1=matriz_A,
                mat2=matriz_B,
                saida=f"{folder}/solution_{otimization_level}_{sizes}_{i}.bin",
                destiny=f"{folder}/metrics_otimization{otimization_level}_{sizes}_{i}.txt",
                cores="0,1",
                executable=exec,
            )
            print(f"running: {command}")
            run(command, shell=True, check=True)
            sleep(4)

utilized_pc: str = input("Qual computador foi utilizado no experimento? ")

if PC_ATUAL[utilized_pc] == TipoPC.NOVO.value:
    shutil.move("otimizacao-00", "pc_novo")
    shutil.move("otimizacao-03","pc_novo")
    shutil.move("otimizacao-03-native","pc_novo")
else:
    shutil.move("otimizacao-00", "pc_antigo")
    shutil.move("otimizacao-03", "pc_antigo")
    shutil.move("otimizacao-03-native", "pc_antigo")
