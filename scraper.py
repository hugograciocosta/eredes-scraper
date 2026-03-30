import os
import time
from playwright.sync_api import sync_playwright

def run():
    user_email = os.environ.get("EREDES_EMAIL")
    user_password = os.environ.get("EREDES_PASSWORD")

    with sync_playwright() as p:
        # Modo non-headless para este teste pode ajudar, mas mantemos True para o GitHub
        browser = p.chromium.launch(headless=True)
        context = browser.new_context(viewport={'width': 1280, 'height': 800}, record_video_dir="videos/")
        page = context.new_page()

        try:
            print("1. A abrir portal...")
            page.goto("https://balcaodigital.e-redes.pt/login", wait_until="networkidle")
            
            # Aceitar cookies
            try:
                page.get_by_role("button", name="Aceitar todos os cookies").click(timeout=5000)
            except: pass

            print("2. A clicar em 'Empresarial'...")
            page.get_by_text("Empresarial").click()
            
            # Aguardar a estrutura do Angular carregar
            print("3. A aguardar carregamento do formulário Angular...")
            page.wait_for_selector("section.login-actions", timeout=20000)
            time.sleep(3) # Pausa técnica para o Angular estabilizar os bindings

            print("4. A preencher via seletores de posição...")
            
            # No Angular, selecionar pelo tipo de input dentro da seção é o mais seguro
            inputs = page.locator("section.login-actions input")
            
            # Primeiro input (E-mail)
            inputs.nth(0).click()
            inputs.nth(0).fill("") # Limpar
            inputs.nth(0).type(user_email, delay=100)
            
            # Segundo input (Password)
            inputs.nth(1).click()
            inputs.nth(1).fill("")
            inputs.nth(1).type(user_password, delay=100)

            print("5. A submeter...")
            # Clicar no botão 'Entrar' que está dentro da mesma seção
            page.locator("section.login-actions button.ant-btn-primary").click()
            
            # Backup: se não clicou, Enter
            page.keyboard.press("Enter")

            print("6. A verificar redirecionamento...")
            time.sleep(15)
            print(f"URL Final: {page.url}")
            page.screenshot(path="final_angular_test.png")

        except Exception as e:
            print(f"Erro: {e}")
            page.screenshot(path="erro_angular.png")

        context.close()
        browser.close()

if __name__ == "__main__":
    run()
