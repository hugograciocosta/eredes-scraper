import os
import time
from playwright.sync_api import sync_playwright

def run():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        context = browser.new_context(viewport={'width': 1280, 'height': 720})
        page = context.new_page()
        
        print("A navegar para a E-Redes...")
        page.goto("https://balcaodigital.e-redes.pt/login", wait_until="networkidle")
        
        # Lidar com Cookies
        try:
            # Tenta clicar no botão de aceitar (procurando por texto)
            page.get_by_role("button", name="Aceitar").click(timeout=5000)
            print("Cookies aceites!")
            # Dá 2 segundos para o site "limpar" o banner do ecrã
            time.sleep(2)
        except Exception:
            print("Sem botão de cookies visível.")

        # Agora procura o campo de email de forma mais flexível
        print("A procurar campo de login...")
        # Espera até 15 segundos e procura por qualquer campo que pareça um email
        page.wait_for_selector('input', timeout=15000)
        
        # Vamos imprimir quantos inputs existem na página para nos ajudar a depurar
        inputs = page.query_selector_all('input')
        print(f"Encontrei {len(inputs)} campos de texto na página.")
        
        if len(inputs) > 0:
            print("Sucesso! O formulário está visível.")
        
        browser.close()

if __name__ == "__main__":
    run()
