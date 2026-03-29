import eredesscraper
from datetime import datetime

print("=== Teste de acesso ao Balcão Digital E-Redes ===")
print(f"Hora: {datetime.now()}")

# Mostrar o que o pacote tem
print("Pacote importado com sucesso.")
print("Conteúdo disponível:", [x for x in dir(eredesscraper) if not x.startswith('_')])

try:
    # Forma mais comum usada no repositório
    scraper = eredesscraper.ERedes(
        username="${{ secrets.EREDES_NIF }}",
        password="${{ secrets.EREDES_PASSWORD }}",
        cpe="${{ secrets.EREDES_CPE }}"
    )
    
    print("✅ Objeto scraper criado com sucesso!")
    print("A tentar fazer login...")

    # Tenta obter consumos (método simples)
    df = scraper.get_consumptions()
    print(f"✅ Sucesso! Obtidos {len(df)} registos de consumo.")
    print(f"Consumo total aproximado: {df['energy'].sum() if 'energy' in df.columns else 'N/A'} kWh")

except AttributeError as e:
    print(f"❌ Erro de atributo: {str(e)}")
    print("Tentando método alternativo...")

except Exception as e:
    print(f"❌ Erro: {str(e)}")
