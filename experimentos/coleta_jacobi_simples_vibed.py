import csv
import json
import os
import subprocess
import threading
import time
from datetime import datetime
from pathlib import Path

# Ajuste se necessário: o script espera ser executado na pasta de otimização.
OTIMIZACOES = {
    "O0": "../fontes/solver-jacobi-mt-O0.exec",
    "O3": "../fontes/solver-jacobi-mt-O3.exec",
    "O3-native": "../fontes/solver-jacobi-mt-O3-native.exec",
}

MATRIZES = [1000, 3000, 5000]
CORES = "0,1"
THREADS = 2
INTERVALO = 1  # segundos entre amostras
REPOUSO = 4    # segundos entre execuções

EVENTOS = (
    "task-clock,cycles,instructions,branches,branch-misses,"
    "cache-references,cache-misses,context-switches,cpu-migrations"
)


def ler_arquivo(caminho):
    try:
        return Path(caminho).read_text().strip()
    except (OSError, PermissionError):
        return "indisponível"


def comando(cmd):
    try:
        return subprocess.check_output(
            cmd, shell=True, text=True, stderr=subprocess.STDOUT
        ).strip()
    except subprocess.CalledProcessError as erro:
        return erro.output.strip()


def frequencias():
    resultado = {}
    for arquivo in Path("/sys/devices/system/cpu").glob("cpu*/cpufreq/scaling_cur_freq"):
        cpu = arquivo.parts[-3]
        valor = ler_arquivo(arquivo)
        if valor != "indisponível":
            resultado[cpu] = round(int(valor) / 1000, 1)
    return resultado


def temperaturas():
    resultado = {}
    for arquivo in Path("/sys/class/hwmon").glob("hwmon*/temp*_input"):
        valor = ler_arquivo(arquivo)
        if valor != "indisponível":
            nome = arquivo.parent / "name"
            sensor = ler_arquivo(nome)
            resultado[f"{sensor}_{arquivo.stem}"] = round(int(valor) / 1000, 1)
    return resultado


def monitorar(arquivo_csv, processo):
    amostras = []
    while processo.poll() is None:
        amostra = {
            "horario": datetime.now().isoformat(timespec="seconds"),
            "frequencia_MHz": json.dumps(frequencias()),
            "temperatura_C": json.dumps(temperaturas()),
            "loadavg": ler_arquivo("/proc/loadavg").split()[:3],
            "memoria": comando("free -m | grep Mem"),
        }
        amostras.append(amostra)
        time.sleep(INTERVALO)

    with open(arquivo_csv, "w", newline="") as arquivo:
        campos = ["horario", "frequencia_MHz", "temperatura_C", "loadavg", "memoria"]
        escritor = csv.DictWriter(arquivo, fieldnames=campos)
        escritor.writeheader()
        escritor.writerows(amostras)


def main():
    computador = input("Computador utilizado (novo/antigo): ").strip().lower()
    if computador not in ("novo", "antigo"):
        raise SystemExit("Informe 'novo' ou 'antigo'.")

    pasta = Path(f"coleta_{computador}_{datetime.now():%Y%m%d_%H%M%S}")
    pasta.mkdir()

    # Informações gerais da máquina e configurações de frequência.
    inventario = {
        "hostname": comando("hostname"),
        "data": datetime.now().astimezone().isoformat(),
        "cpu": comando("lscpu"),
        "memoria": comando("free -h"),
        "kernel": comando("uname -a"),
        "gcc": comando("gcc --version | head -1"),
        "perf": comando("perf --version"),
        "governador": ler_arquivo(
            "/sys/devices/system/cpu/cpu0/cpufreq/scaling_governor"
        ),
        "driver": ler_arquivo(
            "/sys/devices/system/cpu/cpu0/cpufreq/scaling_driver"
        ),
        "amd_boost": ler_arquivo("/sys/devices/system/cpu/cpufreq/boost"),
        "intel_no_turbo": ler_arquivo("/sys/devices/system/cpu/intel_pstate/no_turbo"),
        "afinidade_solicitada": CORES,
        "OMP_NUM_THREADS": THREADS,
        "OMP_DYNAMIC": "FALSE",
    }

    (pasta / "maquina.json").write_text(
        json.dumps(inventario, indent=4, ensure_ascii=False)
    )

    resumo = []

    for nome, executavel in OTIMIZACOES.items():
        for tamanho in MATRIZES:
            for repeticao in range(1, 4):  # altere para range(1, 4) se quiser 3 repetições
                identificador = f"{nome}_{tamanho}_rep{repeticao}"
                arquivo_perf = pasta / f"{identificador}_perf.txt"
                arquivo_monitoramento = pasta / f"{identificador}_monitoramento.csv"
                saida = pasta / f"{identificador}_saida.bin"

                matriz_a = f"../fontes/A{tamanho}.bin"
                matriz_b = f"../fontes/B{tamanho}.bin"

                cmd = (
                    f"OMP_NUM_THREADS={THREADS} OMP_DYNAMIC=FALSE "
                    f"perf stat -e {EVENTOS} -o {arquivo_perf} "
                    f"taskset -c {CORES} {executavel} "
                    f"1E-10 0 {matriz_a} {matriz_b} {saida}"
                )

                print(f"\nExecutando {identificador}...")
                inicio = time.time()
                processo = subprocess.Popen(cmd, shell=True)
                monitor = threading.Thread(
                    target=monitorar, args=(arquivo_monitoramento, processo)
                )
                monitor.start()
                codigo = processo.wait()
                monitor.join()
                duracao = round(time.time() - inicio, 2)

                resumo.append({
                    "execucao": identificador,
                    "duracao_segundos": duracao,
                    "codigo_saida": codigo,
                })

                print(f"Concluído: {duracao}s (código {codigo})")
                time.sleep(REPOUSO)

    with open(pasta / "resumo.csv", "w", newline="") as arquivo:
        escritor = csv.DictWriter(
            arquivo, fieldnames=["execucao", "duracao_segundos", "codigo_saida"]
        )
        escritor.writeheader()
        escritor.writerows(resumo)

    print(f"\nColeta concluída. Arquivos salvos em: {pasta}")


if __name__ == "__main__":
    main()
