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
            print("--- INÍCIO DO DIAGNÓSTICO ---")
            page.goto("https://balcaodigital.e-redes.pt/login", wait_until="networkidle")
            
            # 1. Ver que botões existem na página inicial
            buttons = page.locator("button, .ant-tabs-tab").all_inner_texts()
            print(f"Botões/Tabs encontrados: {buttons}")

            print("2. A selecionar 'Empresarial'...")
            page.get_by_text("Empresarial").click()
            time.sleep(5) 

            # 2. Diagnóstico de Inputs: O que é que o Angular realmente injetou?
            inputs_info = page.evaluate("""() => {
                return Array.from(document.querySelectorAll('input')).map(i => ({
                    type: i.type,
                    placeholder: i.placeholder,
                    id: i.id,
                    name: i.name,
                    visible: i.getBoundingClientRect().width > 0
                }));
            }""")
            print(f"Inputs detetados após clique: {inputs_info}")

            # 3. Ação de Escrita com Foco Forçado
            print("3. A preencher E-mail...")
            # Procuramos o primeiro input que não seja password e esteja visível
            email_field = page.locator("input:not([type='password']):visible").first
            email_field.click(force=True)
            time.sleep(1)
            # Limpar e escrever como humano
            page.keyboard.press("Control+A")
            page.keyboard.press("Backspace")
            page.keyboard.type(user_email, delay=random.randint(50, 100))

            print("4. A preencher Password...")
            pw_field = page.locator("input[type='password']").first
            pw_field.click(force=True)
            time.sleep(0.5)
            page.keyboard.type(user_password, delay=random.randint(50, 100))

            print("5. Submeter...")
            # Procurar o botão amarelo/primário de entrar
            submit_btn = page.locator("button.ant-btn-primary, button:has-text('Entrar')").first
            submit_btn.click()

            print("6. Aguardando resultado (30s)...")
            time.sleep(30)
            print(f"URL Final: {page.url}")
            page.screenshot(path="final_diag.png")

        except Exception as e:
            print(f"ERRO CRÍTICO: {e}")
            page.screenshot(path="erro_diag.png")
        finally:
            context.close()
            browser.close()

if __name__ == "__main__":
    run()
