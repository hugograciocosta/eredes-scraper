import os
import time
import random
from playwright.sync_api import sync_playwright

def human_type(element, text):
    """Escreve texto com atrasos aleatórios entre cada letra."""
    for char in text:
        element.type(char, delay=random.randint(100, 250))
        time.sleep(random.uniform(0.01, 0.05))

def run():
    user_email = os.environ.get("EREDES_EMAIL")
    user_password = os.environ.get("EREDES_PASSWORD")

    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        context = browser.new_context(viewport={'width': 1280, 'height': 800}, record_video_dir="videos/")
        page = context.new_page()

        try:
            print("1. A carregar portal...")
            page.goto("https://balcaodigital.e-redes.pt/login", wait_until="networkidle")
            
            # Clicar em Empresarial e aguardar a transição
            page.get_by_text("Empresarial").click()
            time.sleep(4) # Pausa generosa para o Angular renderizar

            # --- CAMPO E-MAIL ---
            print("2. A focar no E-mail...")
            email_field = page.locator("input").nth(0)
            email_field.click(force=True)
            time.sleep(1.5) # Esperar a animação da etiqueta subir
            
            print("A escrever e-mail calmamente...")
            human_type(email_field, user_email)
            time.sleep(1) # Pausa após escrever

            # --- CAMPO PASSWORD ---
            print("3. A saltar para Password...")
            page.keyboard.press("Tab")
            time.sleep(1.5) # Esperar o foco estabilizar
            
            pw_field = page.locator("input[type='password']")
            print("A escrever password...")
            human_type(pw_field, user_password)
            time.sleep(1)

            # --- SUBMISSÃO ---
            print("4. A navegar até ao botão 'Entrar'...")
            # Em vez de Enter, vamos usar o Tab para chegar ao botão amarelo
            page.keyboard.press("Tab") # Salta o "Esqueceu-se..."
            time.sleep(0.5)
            page.keyboard.press("Tab") # Foca no botão Entrar
            time.sleep(1.5)

            print("5. A clicar...")
            page.keyboard.press("Enter")
            
            print("A aguardar dashboard (30s)...")
            time.sleep(30)
            print(f"URL Final: {page.url}")
            page.screenshot(path="final_result.png")

        except Exception as e:
            print(f"Erro: {e}")
        finally:
            context.close()
            browser.close()

if __name__ == "__main__":
    run()
