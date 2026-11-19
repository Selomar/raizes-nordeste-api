import subprocess
import sys

scripts = [
    "criar_unidades.py",
    "criar_produtos.py",
    "criar_clientes.py"
]

for script in scripts:
    print(f"\nExecutando {script}...")

    resultado = subprocess.run(
        [sys.executable, script],
        check=False
    )

    if resultado.returncode != 0:
        print(f"Erro ao executar {script}.")
        sys.exit(1)

print("\nDados iniciais cadastrados com sucesso!")