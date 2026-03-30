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
        
        # PASSO CRÍTICO: Matar os cookies
        print("2. A tentar eliminar a barra de cookies...")
        try:
            # Procuramos o botão amarelo de aceitar
            botao_cookies = page.get_by_role("button", name="Aceitar todos os cookies")
            botao_cookies.wait_for(state="visible", timeout=10000)
            botao_cookies.click()
            print("Cookies aceites com sucesso.")
            time.sleep(2) # Espera que a barra desapareça visualmente
        except Exception as e:
            print(f"Não vi a barra de cookies ou erro: {e}")

        print("3. A clicar no botão 'Empresarial'...")
        try:
            # Agora que o caminho está livre, clicamos no Empresarial
            # Usamos um seletor que foca no texto mas dentro da caixa correta
            page.locator("app-login-option").filter(has_text="Empresarial").click()
            print("Botão Empresarial clicado.")
        except Exception as e:
            print(f"Erro ao clicar no empresarial: {e}")
            # Se falhar, tentamos o clique por JavaScript (o nosso plano B)
            page.evaluate("document.querySelectorAll('app-login-option')[1].click()")

        print("4. A aguardar redirecionamento para EDP ID...")
        try:
            page.wait_for_url("**/login.edp.pt/**", timeout=20000)
            print(f"Sucesso! Página de login EDP alcançada: {page.url}")
            
            # Preencher login
            page.wait_for_selector('input[type="email"]')
            page.fill('input[type="email"]', user_email)
            page.fill('input[type="password"]', user_password)
            page.get_by_role("button", name="Entrar").click()
            
            print("5. A aguardar entrada no Balcão...")
            time.sleep(15)
            print(f"URL Final: {page.url}")
            
        except Exception as e:
            print(f"Falha após clique: {e}")
            page.screenshot(path="debug_pos_clique.png")

        browser.close()

if __name__ == "__main__":
    run()
