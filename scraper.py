import os
import time
import random
from playwright.sync_api import sync_playwright

def run():
    user_email = os.environ.get("EREDES_EMAIL")
    user_password = os.environ.get("EREDES_PASSWORD")

    with sync_playwright() as p:
        # Lançamos o browser com argumentos para evitar deteção de bot
        browser = p.chromium.launch(headless=True, args=[
            "--disable-blink-features=AutomationControlled",
        ])
        
        context = browser.new_context(
            viewport={'width': 1280, 'height': 800},
            record_video_dir="videos/",
            user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36"
        )
        
        page = context.new_page()
        
        # SCRIPT MÁGICO: Remove a marca de "bot" do browser antes de carregar a página
        page.add_init_script("""
            Object.defineProperty(navigator, 'webdriver', {
                get: () => undefined
            });
        """)

        try:
            print("1. A abrir portal...")
            page.goto("https://balcaodigital.e-redes.pt/login", wait_until="networkidle")
            
            # Matar cookies
            try:
                page.get_by_role("button", name="Aceitar todos os cookies").click(timeout=5000)
                time.sleep(1)
            except: pass

            print("2. A entrar na área Empresarial...")
            page.get_by_text("Empresarial").click()
            
            # Aguardar a página carregar bem
            time.sleep(5)
            print(f"Página atual: {page.url}")

            print("3. A injetar credenciais via JavaScript (Força Bruta)...")
            # Em vez de 'escrever', vamos 'setar' o valor diretamente no elemento DOM
            # Isto ignora bloqueios de teclado do Captcha
            page.evaluate(f"""
                (email, pw) => {{
                    const inputs = document.querySelectorAll('input');
                    inputs.forEach(i => {{
                        if (i.type === 'email' || i.placeholder.includes('E-mail')) {{
                            i.value = email;
                            i.dispatchEvent(new Event('input', {{ bubbles: true }}));
                            i.dispatchEvent(new Event('blur', {{ bubbles: true }}));
                        }}
                        if (i.type === 'password' || i.placeholder.includes('Password')) {{
                            i.value = pw;
                            i.dispatchEvent(new Event('input', {{ bubbles: true }}));
                            i.dispatchEvent(new Event('blur', {{ bubbles: true }}));
                        }}
                    }});
                }}
            """, user_email, user_password)

            time.sleep(2)
            print("4. A tentar submeter...")
            
            # Clicar no botão 'Entrar'
            try:
                page.get_by_role("button", name="Entrar").click(timeout=5000)
            except:
                page.keyboard.press("Enter")

            print("5. A aguardar resposta final...")
            time.sleep(15)
            
            print(f"URL Final: {page.url}")
            page.screenshot(path="resultado_final.png")

        except Exception as e:
            print(f"Erro: {e}")
            page.screenshot(path="erro_detalhado.png")

        context.close()
        browser.close()

if __name__ == "__main__":
    run()
