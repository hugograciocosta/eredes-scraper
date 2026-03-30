import os
import time
from playwright.sync_api import sync_playwright

def run():
    user_email = os.environ.get("EREDES_EMAIL")
    user_password = os.environ.get("EREDES_PASSWORD")

    with sync_playwright() as p:
        # Importante: viewport fixo para as coordenadas baterem certo
        browser = p.chromium.launch(headless=True)
        context = browser.new_context(viewport={'width': 1280, 'height': 800}, record_video_dir="videos/")
        page = context.new_page()

        try:
            print("1. A abrir portal...")
            page.goto("https://balcaodigital.e-redes.pt/login", wait_until="networkidle")
            
            # Limpar cookies (essencial para o layout estar correto)
            try:
                page.get_by_role("button", name="Aceitar todos os cookies").click(timeout=5000)
                time.sleep(1)
            except: pass

            print("2. A clicar em 'Empresarial'...")
            page.get_by_text("Empresarial").click()
            time.sleep(5) # Espera o formulário estabilizar

            print("3. A atacar o campo de E-mail por coordenadas...")
            # Na tua imagem (1280x800), o campo de email está sensivelmente no centro direito
            # Vamos clicar no centro do ecrã ligeiramente para a direita e para cima
            page.mouse.click(850, 480) # Coordenada aproximada do campo E-mail
            time.sleep(0.5)
            
            # Limpar possível lixo e escrever
            page.keyboard.press("Control+A")
            page.keyboard.press("Backspace")
            page.keyboard.type(user_email, delay=150)
            print("E-mail escrito via teclado físico.")

            # Tab para a password (mais seguro que clicar)
            page.keyboard.press("Tab")
            time.sleep(0.5)
            page.keyboard.type(user_password, delay=150)
            print("Password escrita via Tab.")

            print("4. A tentar submeter...")
            page.keyboard.press("Enter")
            
            # Se o Enter não funcionar, tentamos o clique no botão Entrar
            time.sleep(2)
            try:
                page.mouse.click(850, 640) # Coordenada aproximada do botão Entrar
            except: pass

            print("5. A aguardar resultado final...")
            time.sleep(20)
            print(f"URL Final: {page.url}")
            page.screenshot(path="resultado_coordenadas.png")

        except Exception as e:
            print(f"Erro: {e}")
            page.screenshot(path="erro_coordenadas.png")

        context.close()
        browser.close()

if __name__ == "__main__":
    run()
