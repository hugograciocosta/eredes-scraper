import os
import time
from playwright.sync_api import sync_playwright

def run():
    user_email = os.environ.get("EREDES_EMAIL")
    user_password = os.environ.get("EREDES_PASSWORD")

    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        # O vídeo só é gravado se o contexto for fechado corretamente
        context = browser.new_context(
            viewport={'width': 1280, 'height': 800},
            record_video_dir="videos/"
        )
        page = context.new_page()

        try:
            print("1. A abrir portal...")
            page.goto("https://balcaodigital.e-redes.pt/login", wait_until="networkidle")
            
            try:
                page.get_by_role("button", name="Aceitar todos os cookies").click(timeout=5000)
            except: pass

            print("2. A entrar na área Empresarial...")
            page.get_by_text("Empresarial").click()
            
            print("3. A aguardar formulário...")
            page.wait_for_selector("section.login-actions", timeout=20000)
            time.sleep(3) 

            print("4. A preencher com FORÇA (ignora sobreposições)...")
            inputs = page.locator("section.login-actions input")
            
            # Email - Usamos force=True para ignorar a label que está à frente
            inputs.nth(0).click(force=True)
            inputs.nth(0).fill(user_email)
            
            # Password - Usamos force=True para ignorar a label que está à frente
            inputs.nth(1).click(force=True)
            inputs.nth(1).fill(user_password)

            print("5. A submeter...")
            page.keyboard.press("Enter")
            time.sleep(15)

        except Exception as e:
            print(f"Erro detetado: {e}")
        
        finally:
            # ESTA PARTE É CRUCIAL: Fecha sempre para garantir que o vídeo é guardado
            print("A fechar contexto e guardar vídeo...")
            context.close()
            browser.close()

if __name__ == "__main__":
    run()
