import os
import time
from playwright.sync_api import sync_playwright

def run():
    # Puxamos as tuas credenciais guardadas no GitHub
    user_email = os.environ.get("EREDES_EMAIL")
    user_password = os.environ.get("EREDES_PASSWORD")

    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        context = browser.new_context(viewport={'width': 1280, 'height': 720})
        page = context.new_page()
        
        print("A abrir página de login...")
        page.goto("https://balcaodigital.e-redes.pt/login", wait_until="networkidle")
        
        # Aceitar cookies se aparecerem
        try:
            page.get_by_role("button", name="Aceitar").click(timeout=5000)
            time.sleep(1)
        except:
            pass

        print("A introduzir credenciais...")
        # Preenche o email
        page.locator('input[type="email"]').fill(user_email)
        # Preenche a password
        page.locator('input[type="password"]').fill(user_password)
        
        # Clica no botão de entrar (geralmente é o botão primário ou do tipo submit)
        print("A clicar no botão de entrar...")
        page.click('button[type="submit"]')
        
        # Espera para ver se mudamos de página (sucesso)
        time.sleep(10) 
        
        print(f"Página após login: {page.url}")
        
        if "dashboard" in page.url or "home" in page.url:
            print("LOGIN EFETUADO COM SUCESSO! Estamos dentro.")
        else:
            print("Ainda não chegámos ao dashboard. Pode haver um segundo passo ou erro de login.")
            page.screenshot(path="resultado_login.png")

        browser.close()

if __name__ == "__main__":
    run()
