import os
import time
import random
from playwright.sync_api import sync_playwright

def run():
    user_email = os.environ.get("EREDES_EMAIL")
    user_password = os.environ.get("EREDES_PASSWORD")

    with sync_playwright() as p:
        # Lançamos com argumentos para evitar deteção de bot
        browser = p.chromium.launch(headless=True, args=[
            "--disable-blink-features=AutomationControlled",
            "--user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36"
        ])
        context = browser.new_context(viewport={'width': 1280, 'height': 800}, record_video_dir="videos/")
        page = context.new_page()

        try:
            print("1. Acedendo ao portal...")
            page.goto("https://balcaodigital.e-redes.pt/login", wait_until="networkidle")
            
            # Seleção de área
            page.get_by_text("Empresarial").click()
            # Esta espera é crítica: aguarda que o seletor de email esteja REALMENTE pronto
            page.wait_for_selector("input[formcontrolname='email'], input[type='email']", state="visible")
            time.sleep(2)

            print("2. Preenchimento de E-mail (Método de Foco Real)...")
            # Em vez de injetar, vamos clicar e digitar como um humano
            email_input = page.locator("input[formcontrolname='email'], input[type='email']").first
            email_input.click()
            time.sleep(0.5)
            # Digitação com atraso variável para parecer humano
            page.keyboard.type(user_email, delay=random.randint(50, 150))

            print("3. Preenchimento de Password...")
            # Usar Tab é mais seguro para o Angular perceber a transição
            page.keyboard.press("Tab")
            time.sleep(0.5)
            page.keyboard.type(user_password, delay=random.randint(50, 150))

            print("4. Submissão Controlada...")
            # Em vez de Enter, clicamos no botão pelo texto exato para evitar erros de link
            submit_btn = page.locator("button").filter(has_text="Entrar").first
            submit_btn.click()

            print("5. Aguardando Dashboard...")
            # Esperamos por um elemento que só exista lá dentro, ou pelo URL
            time.sleep(20)
            print(f"URL Final: {page.url}")
            page.screenshot(path="final_result.png")

        except Exception as e:
            print(f"Erro detetado: {e}")
        finally:
            context.close()
            browser.close()

if __name__ == "__main__":
    run()
