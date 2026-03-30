import os
import time
from playwright.sync_api import sync_playwright

def run():
    user_email = os.environ.get("EREDES_EMAIL")
    user_password = os.environ.get("EREDES_PASSWORD")

    with sync_playwright() as p:
        # Lançamos com slow_mo para garantir que o browser processa os scripts de injeção
        browser = p.chromium.launch(headless=True, args=["--disable-blink-features=AutomationControlled"])
        context = browser.new_context(viewport={'width': 1280, 'height': 800}, record_video_dir="videos/")
        page = context.new_page()

        try:
            print("1. Acedendo ao portal...")
            page.goto("https://balcaodigital.e-redes.pt/login", wait_until="networkidle")
            
            # Seleção de área
            page.get_by_text("Empresarial").click()
            page.wait_for_selector("input[type='password']", timeout=20000)
            time.sleep(3)

            print("2. Executando bypass de validação Angular...")
            # Esta função JavaScript emula um preenchimento humano completo a nível de memória
            page.evaluate(f"""
                (email, pw) => {{
                    function fillAngularField(selector, value) {{
                        const el = document.querySelector(selector);
                        if (!el) return;
                        
                        // 1. Dar foco e disparar eventos de início
                        el.focus();
                        el.dispatchEvent(new Event('focus', {{ bubbles: true }}));
                        
                        // 2. Injetar valor e disparar eventos de input (o que o Angular ouve)
                        el.value = value;
                        el.dispatchEvent(new Event('input', {{ bubbles: true }}));
                        el.dispatchEvent(new Event('change', {{ bubbles: true }}));
                        
                        // 3. Retirar foco para validar
                        el.blur();
                        el.dispatchEvent(new Event('blur', {{ bubbles: true }}));
                    }}

                    // O primeiro input é sempre o email nesta estrutura
                    const allInputs = document.querySelectorAll('input');
                    fillAngularField('input[type="password"]', pw); // Password primeiro para testar estabilidade
                    
                    // Encontrar o input de email (que às vezes não tem type='email')
                    const emailInput = Array.from(allInputs).find(i => i.getAttribute('formcontrolname') === 'email' || i.type !== 'password');
                    if (emailInput) {{
                        emailInput.focus();
                        emailInput.value = email;
                        emailInput.dispatchEvent(new Event('input', {{ bubbles: true }}));
                        emailInput.dispatchEvent(new Event('blur', {{ bubbles: true }}));
                    }}
                }}
            """, [user_email, user_password])

            time.sleep(2)

            print("3. Submetendo via clique forçado no botão de submissão...")
            # Usamos o seletor da classe primária que o Angular usa para o botão 'Entrar'
            # Isto evita clicar acidentalmente em 'Registe-se' ou 'Recuperar Password'
            submit_btn = page.locator("button.ant-btn-primary, button:has-text('Entrar')").first
            submit_btn.click(force=True)

            print("4. Aguardando processamento final...")
            time.sleep(20)
            print(f"URL de Destino: {page.url}")
            page.screenshot(path="resultado_final.png")

        except Exception as e:
            print(f"Erro Crítico: {e}")
            page.screenshot(path="debug_erro.png")
        finally:
            context.close()
            browser.close()

if __name__ == "__main__":
    run()
