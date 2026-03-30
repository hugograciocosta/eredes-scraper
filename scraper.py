import os
import time
from playwright.sync_api import sync_playwright

def run():
    user_email = os.environ.get("EREDES_EMAIL")
    user_password = os.environ.get("EREDES_PASSWORD")

    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        context = browser.new_context(viewport={'width': 1280, 'height': 800}, record_video_dir="videos/")
        page = context.new_page()

        try:
            page.goto("https://balcaodigital.e-redes.pt/login", wait_until="networkidle")
            
            # 1. Chegar ao formulário
            page.get_by_text("Empresarial").click()
            page.wait_for_selector("input[type='password']", timeout=20000)
            time.sleep(2)

            # 2. Estratégia de Teclado (Ignora camadas de layout)
            # Clicamos na password (que já sabemos que funciona) para ganhar foco
            pw_field = page.locator("input[type='password']")
            pw_field.click(force=True)
            
            # Fazemos Shift+Tab para saltar para o campo de E-mail (o anterior)
            page.keyboard.press("Shift+Tab")
            time.sleep(0.5)
            
            # Escrevemos o email letra a letra (simulando humano)
            page.keyboard.type(user_email, delay=100)
            
            # Tab para voltar à password e escrever
            page.keyboard.press("Tab")
            page.keyboard.type(user_password, delay=100)

            # 3. Submeter
            page.keyboard.press("Enter")
            time.sleep(10)

        except Exception as e:
            print(f"Erro: {e}")
        finally:
            context.close()
            browser.close()

if __name__ == "__main__":
    run()
