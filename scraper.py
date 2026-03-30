import os
import time
from playwright.sync_api import sync_playwright

def run():
    user_email = os.environ.get("EREDES_EMAIL")
    user_password = os.environ.get("EREDES_PASSWORD")

    with sync_playwright() as p:
        # Usamos uma identidade de browser muito comum para evitar bloqueios
        browser = p.chromium.launch(headless=True)
        context = browser.new_context(
            user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
        )
        page = context.new_page()
        
        print("1. A abrir portal e aceitar cookies...")
        page.goto("https://balcaodigital.e-redes.pt/login", wait_until="networkidle")
        
        try:
            page.get_by_role("button", name="Aceitar todos os cookies").click(timeout=5000)
            time.sleep(1)
        except:
            pass

        print("2. A forçar entrada no sistema EDP ID...")
        # Em vez de clicar, vamos navegar diretamente para o "túnel" de login empresarial
        # Este URL é o que o botão ativa por trás das cenas
        page.goto("https://balcaodigital.e-redes.pt/login-return?type=business", wait_until="networkidle")
        
        # Damos tempo para o redirecionamento múltiplo (E-redes -> EDP ID)
        time.sleep(10)
        
        print(f"URL atual: {page.url}")

        try:
            # Se o salto funcionou, o campo de email TEM de estar aqui
            print("3. A procurar campos de login...")
            page.wait_for_selector('input[type="email"]', timeout=30000)
            
            print("4. A preencher dados...")
            page.fill('input[type="email"]', user_email)
            page.fill('input[type="password"]', user_password)
            
            # Submeter
            page.get_by_role("button", name="Entrar").click()
            
            print("5. Aguardando Dashboard final...")
            time.sleep(15)
            print(f"URL Final Alcançado: {page.url}")
            
            if "login" not in page.url.lower():
                print("ESTAMOS DENTRO!")
            else:
                print("O login parou no meio do caminho.")
                page.screenshot(path="parado_no_login.png")

        except Exception as e:
            print(f"O salto direto falhou ou o site bloqueou: {e}")
            page.screenshot(path="erro_salto.png")

        browser.close()

if __name__ == "__main__":
    run()
