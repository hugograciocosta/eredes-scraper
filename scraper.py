import os
import time
from playwright.sync_api import sync_playwright

def run():
    # Vai buscar o email e pass que guardaste nos Secrets
    user_email = os.environ.get("EREDES_EMAIL")
    user_password = os.environ.get("EREDES_PASSWORD")

    with sync_playwright() as p:
        # AGORA USAMOS FIREFOX
        browser = p.firefox.launch(headless=True)
        context = browser.new_context(viewport={'width': 1280, 'height': 800})
        page = context.new_page()
        
        print("1. A saltar direto para o login Empresarial...")
        # Este link ignora o botão inicial e vai direto ao que interessa
        page.goto("https://balcaodigital.e-redes.pt/login-return?type=business", wait_until="networkidle")
        
        # Espera 5 segundos para o site da EDP ID carregar
        time.sleep(5)

        print(f"2. Estamos em: {page.url}")

        try:
            print("3. A procurar campos de email...")
            # Espera até o campo de email aparecer no ecrã
            page.wait_for_selector('input[type="email"]', timeout=20000)
            
            print("4. A preencher dados...")
            page.fill('input[type="email"]', user_email)
            page.fill('input[type="password"]', user_password)
            
            print("5. A clicar em Entrar...")
            # Clica no botão de submeter o formulário
            page.locator('button[type="submit"]').first.click()
            
            # Espera 15 segundos para ver se o Dashboard aparece
            print("A aguardar login final...")
            time.sleep(15)
            
            print(f"6. URL final: {page.url}")
            
            if "login" not in page.url.lower():
                print("CONSEGUIMOS! Estamos dentro do balcão.")
            else:
                print("Algo falhou no login. A tirar print...")
                page.screenshot(path="falha_login.png")

        except Exception as e:
            print(f"Erro no processo: {e}")
            page.screenshot(path="erro_total.png")

        browser.close()

if __name__ == "__main__":
    run()
