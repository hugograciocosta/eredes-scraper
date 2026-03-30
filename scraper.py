import os
import time
from playwright.sync_api import sync_playwright

def run():
    user_email = os.environ.get("EREDES_EMAIL")
    user_password = os.environ.get("EREDES_PASSWORD")

    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        context = browser.new_context(viewport={'width': 1280, 'height': 800})
        page = context.new_page()
        
        print("1. A abrir E-Redes...")
        page.goto("https://balcaodigital.e-redes.pt/login", wait_until="networkidle")
        
        # 2. Matar Cookies
        try:
            print("2. A aceitar cookies...")
            page.get_by_role("button", name="Aceitar todos os cookies").click(timeout=10000)
            time.sleep(2)
        except:
            print("Barra de cookies não apareceu ou já foi aceite.")

        # 3. Clicar no Empresarial
        print("3. A clicar em 'Empresarial'...")
        try:
            # Esperamos que o texto esteja visível e clicamos
            botao = page.get_by_text("Empresarial")
            botao.wait_for(state="visible", timeout=10000)
            botao.click()
            print("Clique efetuado.")
        except Exception:
            print("Falha no clique normal, a tentar via JavaScript forçado...")
            # Esta linha procura qualquer elemento que diga Empresarial e clica
            page.evaluate("Array.from(document.querySelectorAll('*')).find(el => el.innerText === 'Empresarial').click()")

        # 4. Login EDP
        print("4. A aguardar página da EDP...")
        try:
            page.wait_for_url("**/login.edp.pt/**", timeout=20000)
            print("Sucesso! A preencher dados...")
            
            # Usamos IDs e tipos genéricos que a EDP não muda
            page.wait_for_selector('input[type="email"]')
            page.fill('input[type="email"]', user_email)
            page.fill('input[type="password"]', user_password)
            
            # Clicar no botão 'Entrar'
            page.get_by_role("button", name="Entrar").click()
            
            print("5. Login submetido. A aguardar Dashboard...")
            time.sleep(15)
            
            print(f"URL Final: {page.url}")
            if "home" in page.url.lower() or "dashboard" in page.url.lower():
                print("ESTAMOS DENTRO!")
            else:
                page.screenshot(path="pos_login.png")
                
        except Exception as e:
            print(f"Erro final: {e}")
            page.screenshot(path="erro_edp.png")

        browser.close()

if __name__ == "__main__":
    run()
