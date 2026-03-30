import os
import time
from playwright.sync_api import sync_playwright

def run():
    user_email = os.environ.get("EREDES_EMAIL")
    user_password = os.environ.get("EREDES_PASSWORD")

    with sync_playwright() as p:
        # Mantemos o Firefox que é mais robusto aqui
        browser = p.firefox.launch(headless=True)
        context = browser.new_context(viewport={'width': 1280, 'height': 800})
        page = context.new_page()
        
        print("1. A abrir a página principal...")
        page.goto("https://balcaodigital.e-redes.pt/login", wait_until="networkidle")
        
        # Limpar cookies se aparecerem
        try:
            page.get_by_role("button", name="Aceitar").click(timeout=5000)
        except:
            pass

        print("2. A clicar no botão 'Empresarial'...")
        # Clicamos e esperamos que a página mude de URL (o redirecionamento)
        page.get_by_text("Empresarial").click()
        
        print("3. A aguardar que o site redirecione para a EDP...")
        # Esperamos até que o URL contenha 'login.edp.pt' ou mude da home
        time.sleep(8) 
        
        print(f"URL atual: {page.url}")

        try:
            print("4. A procurar campos de login no novo URL...")
            # Agora que mudou, o campo de email TEM de aparecer
            page.wait_for_selector('input[type="email"]', timeout=20000)
            
            print("5. A preencher dados...")
            page.fill('input[type="email"]', user_email)
            page.fill('input[type="password"]', user_password)
            
            print("6. A submeter...")
            page.locator('button[type="submit"]').first.click()
            
            time.sleep(15)
            print(f"Final: {page.url}")

        except Exception as e:
            print(f"Falha ao encontrar formulário. URL atual era: {page.url}")
            page.screenshot(path="debug_final.png")

        browser.close()

if __name__ == "__main__":
    run()
