import os
import time
from playwright.sync_api import sync_playwright

def run():
    user_email = os.environ.get("EREDES_EMAIL")
    user_password = os.environ.get("EREDES_PASSWORD")

    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True, args=["--disable-blink-features=AutomationControlled"])
        context = browser.new_context(
            viewport={'width': 1280, 'height': 800},
            record_video_dir="videos/"
        )
        page = context.new_page()

        try:
            print("1. A carregar portal...")
            page.goto("https://balcaodigital.e-redes.pt/login", wait_until="networkidle")
            
            # Aceitar cookies para limpar a frente
            try:
                page.get_by_role("button", name="Aceitar todos os cookies").click(timeout=5000)
                time.sleep(1)
            except: pass

            print("2. A selecionar 'Empresarial'...")
            page.get_by_text("Empresarial").click()
            
            # Esperar o formulário aparecer visualmente
            page.wait_for_selector("input", timeout=15000)
            time.sleep(3)

            print("3. A forçar escrita das credenciais...")
            # Injetamos os valores diretamente na string JS para evitar erros de argumentos do Python
            script = f"""
                () => {{
                    const inputs = document.querySelectorAll('input');
                    inputs.forEach(el => {{
                        if (el.type === 'email' || el.placeholder.toLowerCase().includes('email')) {{
                            el.value = '{user_email}';
                            el.dispatchEvent(new Event('input', {{ bubbles: true }}));
                        }}
                        if (el.type === 'password' || el.placeholder.toLowerCase().includes('password')) {{
                            el.value = '{user_password}';
                            el.dispatchEvent(new Event('input', {{ bubbles: true }}));
                        }}
                    }});
                }}
            """
            page.evaluate(script)
            
            print("4. A tentar submeter login...")
            time.sleep(2)
            # Tentar clicar no botão amarelo 'Entrar'
            try:
                page.locator("button:has-text('Entrar')").click(timeout=5000)
            except:
                page.keyboard.press("Enter")

            print("5. A aguardar resultado final...")
            time.sleep(15)
            print(f"URL Final: {page.url}")
            page.screenshot(path="final_debug.png")

        except Exception as e:
            print(f"Erro detetado: {e}")
            page.screenshot(path="erro_fatal.png")

        context.close()
        browser.close()

if __name__ == "__main__":
    run()
