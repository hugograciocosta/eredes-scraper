import os
from pathlib import Path
from eredesscraper.workflows import switchboard
from datetime import datetime

print("=== Teste de acesso ao Balcão Digital E-Redes ===")
print(f"Hora: {datetime.now()}")

nif = os.getenv("EREDES_NIF")
password = os.getenv("EREDES_PASSWORD")
cpe = os.getenv("EREDES_CPE")

print(f"NIF encontrado: {len(nif) if nif else 0} caracteres")
print(f"CPE encontrado: {len(cpe) if cpe else 0} caracteres")

try:
    print("A tentar login diretamente...")

    switchboard(
        config_path=None,           # não usa config.yml
        nif=int(nif),
        pwd=password,
        cpe=cpe,
        name="current",
        db=[],                      # sem base de dados
        delta=False
    )

    print("✅ Login e obtenção de consumos bem sucedidos!")
    print("O scraper conseguiu aceder ao Balcão Digital da E-Redes.")

except Exception as e:
    print(f"❌ Erro: {str(e)}")
