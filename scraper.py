import os
import time
import random
from playwright.sync_api import sync_playwright

def run():
    user_email = os.environ.get("EREDES_EMAIL")
    user_password = os.environ.get("EREDES_PASSWORD")

    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        context = browser.new_context(viewport={'width': 1280, 'height': 800}, record_video_dir="videos/")
        page = context.new_page()

        try:
            print("1. A abrir portal...")
            page.goto("https://balcaodigital.e-redes.pt/login", wait_until="networkidle")
            
            # Clicar no botão 'Empresarial'
            page.get_by_text("Empresarial").click()
            
            # ESPERA HUMANA: Aguardar que o formulário "nasça" na página
            page.wait_for_selector("input[type='password']", timeout=20000)
            time.sleep(2)

            # --- ATAQUE AO EMAIL ---
            print("2. A focar no E-mail (com simulação de clique)...")
            # Em vez de preencher, vamos clicar no texto 'E-mail' para disparar a animação do Angular
            page.get_by_text("E-mail").first.click(force=True)
            time.sleep(1) # Tempo para a label subir
            
            # Escrever como um humano (atrasos aleatórios entre letras)
            for char in user_email:
                page.keyboard.type(char)
                time.sleep(random.uniform(0.05, 0.15))
            
            print("3. A saltar para Password...")
            page.keyboard.press("Tab")
            time.sleep(0.5)
            
            for char in user_password:
                page.keyboard.type(char)
                time.sleep(random.uniform(0.05, 0.15))

            print("4. Movimento de rato aleatório antes de Entrar...")
            page.mouse.move(random.randint(100, 500), random.randint(100, 500))
            time.sleep(1)
            
            print("5. A submeter...")
            page.keyboard.press("Enter")
            
            # Aguardar para ver se o URL muda (sucesso)
            time.sleep(15)
            print(f"URL Final: {page.url}")

        except Exception as e:
            print(f"Erro: {e}")
        finally:
            context.close()
            browser.close()

if __name__ == "__main__":
    run()
