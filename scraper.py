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
            page.wait_for_selector("input[type='password']", timeout=20000)
            time.sleep(2)

            # --- PREENCHIMENTO ---
            print("2. A focar e preencher E-mail...")
            # Clicamos na label para ativar o campo
            page.get_by_text("E-mail").first.click(force=True)
            time.sleep(1) 
            
            # Escrevemos o email
            page.keyboard.type(user_email, delay=50)
            
            print("3. A preencher Password...")
            page.keyboard.press("Tab")
            time.sleep(0.5)
            page.keyboard.type(user_password, delay=50)

            # --- CORREÇÃO CRÍTICA DO ERRO ---
            print("4. A mover foco para o botão 'Entrar' (para evitar recuperação de pw)...")
            # Fazemos TAB mais duas vezes para saltar o link "Esqueceu-se..." e focar no botão
            page.keyboard.press("Tab")
            time.sleep(0.2)
            page.keyboard.press("Tab")
            time.sleep(0.5) # Tempo para o foco visual assentar no botão amarelo

            print("5. A submeter (agora sim, no botão certo)...")
            page.keyboard.press("Enter")
            
            # Aguardar redirecionamento
            print("6. A aguardar Dashboard...")
            time.sleep(15)
            print(f"URL Final: {page.url}")
            page.screenshot(path="final_login_attempt.png")

        except Exception as e:
            print(f"Erro: {e}")
        finally:
            context.close()
            browser.close()

if __name__ == "__main__":
    run()
