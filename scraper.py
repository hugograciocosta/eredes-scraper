import os
from playwright.sync_api import sync_playwright

def run():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        context = browser.new_context(viewport={'width': 1280, 'height': 720})
        page = context.new_page()
        
        print("A navegar para a E-Redes...")
        page.goto("https://balcaodigital.e-redes.pt/login", wait_until="networkidle")
        
        # --- NOVO: Lidar com Cookies ---
        try:
            # Procura botões que contenham a palavra "Aceitar" ou "Concordar"
            # O 'timeout=5000' diz ao robô: "Procura durante 5 segundos, se não vires nada, segue caminho"
            botao_cookies = page.get_by_role("button", name="Aceitar")
            if botao_cookies.is_visible():
                botao_cookies.click()
                print("Cookies aceites com sucesso!")
        except Exception:
            print("Não vi nenhum aviso de cookies, a avançar...")
        # -------------------------------

        # Agora tentamos ver se o campo de email aparece
        page.wait_for_selector('input[type="email"]', timeout=10000)
        print(f"Sucesso! Cheguei ao formulário. Título: {page.title()}")
        
        browser.close()

if __name__ == "__main__":
    run()
