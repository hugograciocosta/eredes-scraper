import os
import time
import random
from playwright.sync_api import sync_playwright

def run():
    user_email = os.environ.get("EREDES_EMAIL")
    user_password = os.environ.get("EREDES_PASSWORD")

    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True, args=["--disable-blink-features=AutomationControlled"])
        context = browser.new_context(viewport={'width': 1280, 'height': 800}, record_video_dir="videos/")
        page = context.new_page()

        try:
            print("1. Acedendo ao portal...")
            page.goto("https://balcaodigital.e-redes.pt/login", wait_until="networkidle")
            
            # --- RESOLUÇÃO DO PROBLEMA DOS COOKIES ---
            print("2. A limpar banner de cookies...")
            try:
                # Tentamos clicar no botão 'Aceitar todos os cookies' que aparece nos teus prints
                cookie_btn = page.locator("button#onetrust-accept-btn-handler, button:has-text('Aceitar todos os cookies')").first
                if cookie_btn.is_visible():
                    cookie_btn.click()
                    print("Cookies aceites.")
                else:
                    # Se não for o OneTrust, tentamos o botão genérico amarelo do banner cinzento
                    page.locator(".cookie-banner button, button:has-text('Aceitar')").first.click()
            except Exception as e:
                print(f"Nota: Banner de cookies não encontrado ou já fechado. {e}")

            time.sleep(2)

            print("3. A selecionar 'Empresarial'...")
            # Clicamos e aguardamos que o banner desapareça realmente da frente dos campos
            page.get_by_text("Empresarial").click()
            time.sleep(3)

            # Diagnóstico de Inputs: O que é que o Angular realmente injetou?
            inputs_info = page.evaluate("""() => {
                return Array.from(document.querySelectorAll('input')).map(i => ({
                    type: i.type, placeholder: i.placeholder, visible: i.getBoundingClientRect().width > 0
                }));
            }""")
            print(f"Inputs visíveis: {inputs_info}")

            print("4. A preencher credenciais (com foco forçado)...")
            # Foco no email (o primeiro input visível que não é password)
            email_field = page.locator("input:not([type='password']):visible").first
            email_field.click(force=True)
            page.keyboard.type(user_email, delay=random.randint(50, 100))
            
            time.sleep(1)
            
            # Foco na password
            pw_field = page.locator("input[type='password']:visible").first
            pw_field.click(force=True)
            page.keyboard.type(user_password, delay=random.randint(50, 100))

            print("5. Submetendo...")
            # O botão 'Entrar' deve estar agora clicável sem o banner por cima
            submit_btn = page.locator("button.ant-btn-primary, button:has-text('Entrar')").first
            submit_btn.click()

            print("6. Aguardando processamento...")
            time.sleep(20)
            print(f"URL de Destino: {page.url}")
            page.screenshot(path="final_result_sem_cookies.png")

        except Exception as e:
            print(f"Erro: {e}")
            page.screenshot(path="erro_cookies.png")
        finally:
            context.close()
            browser.close()

if __name__ == "__main__":
    run()
