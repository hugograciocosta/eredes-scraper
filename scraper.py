import os
import time
from playwright.sync_api import sync_playwright

def run():
    user_email = os.environ.get("EREDES_EMAIL")
    user_password = os.environ.get("EREDES_PASSWORD")

    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True, args=["--disable-blink-features=AutomationControlled"])
        context = browser.new_context(viewport={'width': 1280, 'height': 800}, record_video_dir="videos/")
        page = context.new_page()

        try:
            print("1. A abrir portal...")
            page.goto("https://balcaodigital.e-redes.pt/login", wait_until="networkidle")
            
            # Cookies
            try:
                page.get_by_role("button", name="Aceitar todos os cookies").click(timeout=5000)
            except: pass

            print("2. A selecionar 'Empresarial'...")
            page.get_by_text("Empresarial").click()
            time.sleep(4) # Espera o formulário carregar

            print("3. A injetar credenciais em Shadow DOM...")
            # Esta função JS entra dentro de todos os Shadow Roots para encontrar os inputs reais
            script = f"""
            () => {{
                function fillDeep(root, email, pass) {{
                    const inputs = root.querySelectorAll('input');
                    inputs.forEach(i => {{
                        if (i.type === 'email' || i.getAttribute('type') === 'text' || i.id.includes('email')) {{
                            i.value = email;
                            i.dispatchEvent(new Event('input', {{ bubbles: true }}));
                            i.dispatchEvent(new Event('change', {{ bubbles: true }}));
                        }}
                        if (i.type === 'password') {{
                            i.value = pass;
                            i.dispatchEvent(new Event('input', {{ bubbles: true }}));
                            i.dispatchEvent(new Event('change', {{ bubbles: true }}));
                        }}
                    }});
                    
                    // Procura em Shadow Roots de outros elementos
                    const allElements = root.querySelectorAll('*');
                    allElements.forEach(el => {{
                        if (el.shadowRoot) {{
                            fillDeep(el.shadowRoot, email, pass);
                        }}
                    }});
                }}
                fillDeep(document, '{user_email}', '{user_password}');
            }}
            """
            page.evaluate(script)
            
            print("4. A tentar submeter...")
            time.sleep(2)
            # Tentar clicar no botão Entrar de várias formas
            try:
                # O botão também pode estar num Shadow DOM, vamos usar o teclado para garantir
                page.keyboard.press("Enter")
                print("Enter pressionado.")
            except:
                pass

            print("5. A aguardar resultado (20s)...")
            time.sleep(20)
            print(f"URL Final: {page.url}")
            page.screenshot(path="resultado_shadow.png")

        except Exception as e:
            print(f"Erro: {e}")
            page.screenshot(path="erro_fatal.png")

        context.close()
        browser.close()

if __name__ == "__main__":
    run()
