import os
from playwright.sync_api import sync_playwright

def run():
    with sync_playwright() as p:
        # Abre o navegador em modo "escondido" (headless)
        browser = p.chromium.launch()
        page = browser.new_page()
        
        print("A tentar abrir o site da E-Redes...")
        page.goto("https://balcaodigital.e-redes.pt/login")
        
        # Espera que o campo de email apareça para confirmar que o site carregou
        page.wait_for_selector('input[type="email"]', timeout=30000)
        
        titulo = page.title()
        print(f"Sucesso! Entrei na página: {titulo}")
        
        browser.close()

if __name__ == "__main__":
    run()
