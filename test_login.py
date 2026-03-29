from eredesscraper import ERedesScraper
from datetime import datetime

print("=== Teste de acesso ao Balcão Digital E-Redes ===")
print(f"Hora: {datetime.now()}")

try:
    scraper = ERedesScraper(
        nif="${{ secrets.EREDES_NIF }}",
        password="${{ secrets.EREDES_PASSWORD }}",
        cpe="${{ secrets.EREDES_CPE }}"
    )
    
    print("✅ Login bem sucedido!")
    print("A tentar obter consumos...")
    
    # Tenta obter consumos (método mais simples)
    consumos = scraper.get_consumptions()
    print("✅ Consumos obtidos!")
    print(f"Total de registos: {len(consumos)}")
    
except Exception as e:
    print(f"❌ Erro durante a execução: {str(e)}")
