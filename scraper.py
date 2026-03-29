import os
import time
from playwright.sync_api import sync_playwright

def run():
    user_email = os.environ.get("EREDES_EMAIL")
    user_password = os.environ.get("EREDES_PASSWORD")

    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        context = browser.new_context(viewport={'width': 1280, 'height': 800})
        page = context.new_page()
        
        print("1. A abrir login...")
        page.goto("https://balcaodigital.e-redes.pt/login", wait_until="networkidle")
        
        try:
            page.get_by_role("button", name="Aceitar").click(timeout=5000)
        except:
            pass

        print("2. A clicar em Empresarial...")
        page.get_by_text("Empresarial").click()
        
        # Damos um tempo para o iframe carregar
        time.sleep(5)

        print("3. A procurar o quadro de login (iframe)...")
        # O segredo: Procurar todos os frames e ver qual tem o campo de email
        login_frame = None
        for frame in page.frames:
            if "login" in frame.url or "edp" in frame.url:
                login_frame = frame
                break
        
        # Se não encontramos pelo URL, tentamos o frame principal (fallback)
        target = login_frame if login_frame else page
        
        try:
            print("4. A tentar preencher credenciais...")
            # Usamos um seletor mais genérico que funciona em quase todos os logins EDP
            target.wait_for_selector('input[name="email"], input[type="email"]', timeout=20000)
            target.fill('input[name="email"], input[type="email"]', user_email)
            target.fill('input[name="password"], input[type="password"]', user_password)
            
            print("5. A submeter...")
            # Clica no botão que estiver disponível no frame
            target.locator('button[type="submit"]').click()
            
            time.sleep(10)
            print(f"Sucesso! URL final: {page.url}")
            
        except Exception as e:
            print(f"Erro no preenchimento: {e}")
            page.screenshot(path="debug_iframe.png")
            # Vamos listar os frames para eu analisar no próximo passo se falhar
            print(f"Frames encontrados: {[f.url for f in page.frames]}")

        browser.close()

if __name__ == "__main__":
    run()
