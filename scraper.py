import os
import time
from playwright.sync_api import sync_playwright

def run():
    # Puxar credenciais das Secrets
    user_email = os.environ.get("EREDES_EMAIL")
    user_password = os.environ.get("EREDES_PASSWORD")

    with sync_playwright() as p:
        # Lançar browser (Headless para o GitHub)
        browser = p.chromium.launch(headless=True)
        context = browser.new_context(viewport={'width': 1280, 'height': 800})
        page = context.new_page()
        
        print("1. A abrir a página de login direto...")
        page.goto("https://balcaodigital.e-redes.pt/login", wait_until="networkidle")
        
        # Passo dos Cookies (para não tapar o botão Empresarial)
        try:
            page.get_by_role("button", name="Aceitar").click(timeout=5000)
            time.sleep(1)
        except:
            pass

        # 2. O Passo Crítico: Clicar em Empresarial
        print("2. A clicar no botão 'Empresarial'...")
        try:
            # Procuramos o botão pelo texto exato
            page.get_by_text("Empresarial").click(timeout=15000)
            print("Botão Empresarial clicado com sucesso.")
        except Exception as e:
            print(f"Erro ao encontrar botão Empresarial: {e}")
            page.screenshot(path="erro_botao.png")
            browser.close()
            return

        # 3. Esperar que o formulário de login carregue após o clique
        print("3. A aguardar o formulário de e-mail...")
        time.sleep(3) # Pausa técnica para a transição
        
        try:
            # Esperar pelo campo de email aparecer
            page.wait_for_selector('input[type="email"]', timeout=20000)
            
            print("4. A preencher credenciais...")
            page.fill('input[type="email"]', user_email)
            page.fill('input[type="password"]', user_password)
            
            print("5. A submeter...")
            page.get_by_role("button", name="Entrar").click()
            
            # Verificação final
            time.sleep(10)
            print(f"URL após login: {page.url}")
            
        except Exception as e:
            print(f"Erro no formulário: {e}")
            page.screenshot(path="erro_formulario.png")

        browser.close()

if __name__ == "__main__":
    run()
