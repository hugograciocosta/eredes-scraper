import os
from datetime import datetime

print("=== Teste de acesso ao Balcão Digital E-Redes ===")
print(f"Hora: {datetime.now()}")

nif = os.getenv("EREDES_NIF")
password = os.getenv("EREDES_PASSWORD")
cpe = os.getenv("EREDES_CPE")

print(f"NIF: {nif[:3]}... (9 dígitos)")
print(f"CPE: {cpe[:8]}...")

# Vamos apenas importar e ver o que o pacote tem
import eredesscraper

print("\nFunções e classes disponíveis no pacote:")
print([item for item in dir(eredesscraper) if not item.startswith('_')])

print("\nTentando ajuda da função principal...")
help(eredesscraper)

print("\nTeste terminado.")
