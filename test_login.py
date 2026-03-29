from pathlib import Path
from eredesscraper.workflows import switchboard
from datetime import datetime

print("=== Teste de acesso ao Balcão Digital E-Redes ===")
print(f"Hora: {datetime.now()}")

try:
    print("A carregar config.yml e a tentar login...")

    # Executa o workflow "current" (mês atual) sem guardar em base de dados
    switchboard(
        config_path=Path("./config.yml"),
        name="current",
        db=[],          # não usa InfluxDB
        delta=False,
        keep=True       # mantém os dados na memória para vermos
    )

    print("✅ Login e obtenção de consumos bem sucedidos!")
    print("O scraper conseguiu aceder ao Balcão Digital da E-Redes.")

except Exception as e:
    print(f"❌ Erro: {str(e)}")
