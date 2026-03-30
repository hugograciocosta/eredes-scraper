import os
import time
from playwright.sync_api import sync_playwright

def run():
    user_email = os.environ.get("EREDES_EMAIL")
    user_password = os.environ.get("EREDES_PASSWORD")

    with sync_playwright() as p:
        # Usamos Chromium com identidade real
        browser = p.chromium.launch(headless=True)
        context = browser.new_context(
            user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36"
        )
        page = context.new_page()
        
        print("1. A carregar E-Redes...")
        page.goto("https://balcaodigital.e-redes.pt/login", wait_until="networkidle")
        
        # Aceitar cookies via teclado (mais seguro que clique)
        time.sleep(3)
        page.keyboard.press("Escape") # Tenta fechar overlays

        print("2. A selecionar 'Empresarial' via TAB (Acessibilidade)...")
        # Este método simula um humano a saltar entre botões com o teclado
        # É quase impossível de bloquear
        found = False
        for _ in range(15): # Tentamos 15 vezes o TAB até focar no Empresarial
            page.keyboard.press("Tab")
            focused_text = page.evaluate("document.activeElement.innerText")
            if focused_text and "Empresarial" in focused_text:
                page.keyboard.press("Enter")
                print("Botão acionado via Teclado!")
                found = True
                break
        
        if not found:
            print("Teclado falhou, a tentar clique forçado por coordenadas...")
            box = page.get_by_text("Empresarial").bounding_box()
            if box:
                page.mouse.click(box['x'] + box['width'] / 2, box['y'] + box['height'] / 2)

        # Esperar a transição
        try:
            print("3. A aguardar EDP ID...")
            page.wait_for_url("**/login.edp.pt/**", timeout=20000)
            
            print("4. A preencher login...")
            page.wait_for_selector('input[type="email"]', state="visible")
            page.fill('input[type="email"]', user_email)
            page.fill('input[type="password"]', user_password)
            page.keyboard.press("Enter")
            
            time.sleep(10)
            print(f"URL Final: {page.url}")
            
        except Exception as e:
            print(f"Erro: {e}")
            page.screenshot(path="debug.png")

        browser.close()

if __name__ == "__main__":
    run()
