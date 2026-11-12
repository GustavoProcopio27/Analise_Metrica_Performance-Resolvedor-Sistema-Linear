import pandas as pd
from sys import platform
from pathlib import Path
import re
from string import Template

"""
    Lembrança: rodar novamente as metricas que escolhermos com quantidades variadas de clock para notar a diferença e entender
    Aparentemente, certas metricas podem utilizar o mesmo registrador, oq pode atrabalhar a contagem, talvez seja recomendado ver quais interferem, e retirar da analise
"""
utilized_pc: str = input("Qual computador foi utilizado no experimento? ")
target_folder: str = "pc_novo" if utilized_pc == "novo"  else "pc_antigo"

    
SIZES: tuple[int] = (1000, 2000, 3000, 4000, 5000)
FOLDERS_OTIMIZATION_LEVEL: tuple[str] = (
    ("otimizacao-00", "00"),
    ("otimizacao-03", "03"),
    ("otimizacao-03-native", "03-native"),
)

metrics_data: dict[str, list] = {
    "task_clock": [],
    "cycles": [],
    "instructions": [],
    "branches": [],
    "branch_misses": [],
    "cpu_migrations": [],
    "context_switches": [],
    "cache_references": [],
    "cache_misses": [],
    "major_faults": [],
    "page_faults": [],
    "time_elapsed": [],
    "otimization": [],
    "matrix_size": [],
}

file_name: Template = Template( "${experimented_pc}/${folder}/metrics_otimization${otimization}_${size}_${run}.txt"
                                    if platform=="linux" else 
                                "${experimented_pc}\\${folder}\\metrics_otimization${otimization}_${size}_${run}.txt"
    )                       

for folder, otimization_lv in FOLDERS_OTIMIZATION_LEVEL:
    for size in SIZES:
        for idx in range(1, 11):
            file: Path = Path(file_name.substitute(experimented_pc=target_folder, folder=folder, otimization=otimization_lv, size=size, run=idx))

            with file.open(encoding="utf-8") as f:
                conteudo = f.read()

                metrics_data["task_clock"].append(float(
                    re.search(r"([\d.,]+) msec task-clock", conteudo).group(1).replace(".", "").replace(",", ".")))

                metrics_data["cycles"].append(int(
                    re.search(r"([\d.,]+)      cycles", conteudo).group(1).replace(".", "")))

                metrics_data["instructions"].append(int(
                    re.search(r"([\d.,]+)      instructions", conteudo).group(1).replace(".", "")))

                metrics_data["branches"].append(int(
                    re.search(r"([\d.,]+)      branches", conteudo).group(1).replace(".", "")))

                metrics_data["branch_misses"].append(int(
                    re.search(r"([\d.,]+)      branch-misses", conteudo).group(1).replace(".", "")))

                metrics_data["cpu_migrations"].append(int(
                    re.search(r"([\d.,]+)      cpu-migrations", conteudo).group(1).replace(".", "")))

                metrics_data["context_switches"].append(int(
                    re.search(r"([\d.,]+)      context-switches", conteudo).group(1).replace(".", "")))

                metrics_data["cache_references"].append(int(
                    re.search(r"([\d.,]+)      cache-references", conteudo).group(1).replace(".", "")))

                metrics_data["cache_misses"].append(int(
                    re.search(r"([\d.,]+)      cache-misses", conteudo).group(1).replace(".", "")))

                metrics_data["major_faults"].append(int( 
                    re.search(r"([\d.,]+)      major-faults", conteudo).group(1).replace(".", "")))

                metrics_data["page_faults"].append(int(
                    re.search(r"([\d.,]+)      page-faults", conteudo).group(1).replace(".", "")))

                metrics_data["time_elapsed"].append(float( 
                    re.search(r"([\d.,]+) seconds time elapsed", conteudo).group(1).replace(".", "").replace(",", ".")))

                metrics_data["otimization"].append(otimization_lv)

                metrics_data["matrix_size"].append(size)

metrics_df = pd.DataFrame(metrics_data)
metrics_df["IPC"] = metrics_df["instructions"] / metrics_df["cycles"]
metrics_df["CPI"] = metrics_df["cycles"] / metrics_df["instructions"]

metrics_df["Computer"] = "novo" if utilized_pc == "novo" else "antigo"

print(metrics_df)
metrics_df.to_csv( 
                "metricas_performance_PC_NOVO.csv" if utilized_pc == "novo" else "metricas_performance_PC_ANTIGO.csv",
                sep=";",
                index=False
                )