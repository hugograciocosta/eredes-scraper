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
    print("A tentar obter consumos recentes...")
    
    # Tenta obter consumos do último mês
    consumos = scraper.get_monthly_consumption()
    consumo_total = consumos['energy'].sum() if 'energy' in consumos.columns else "Não foi possível calcular"
    
    print(f"✅ Consumos obtidos com sucesso!")
    print(f"Consumo total encontrado: {consumo_total} kWh")
    
except Exception as e:
    print(f"❌ Erro: {str(e)}")
