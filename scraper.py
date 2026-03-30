import os
import time
from playwright.sync_api import sync_playwright

def run():
    # Obtém as credenciais do ambiente (confirma que o EREDES_EMAIL é um email real no GitHub)
    user_email = os.environ.get("EREDES_EMAIL")
    user_password = os.environ.get("EREDES_PASSWORD")

    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True, args=["--disable-blink-features=AutomationControlled"])
        context = browser.new_context(viewport={'width': 1280, 'height': 800}, record_video_dir="videos/")
        page = context.new_page()

        try:
            print("1. A abrir portal...")
            page.goto("https://balcaodigital.e-redes.pt/login", wait_until="networkidle")
            
            # Aceitar cookies
            try:
                page.get_by_role("button", name="Aceitar todos os cookies").click(timeout=5000)
            except: pass

            print("2. A entrar na área Empresarial...")
            page.get_by_text("Empresarial").click()
            time.sleep(5) # Espera generosa para o formulário carregar

            print("3. A injetar credenciais (via Shadow Piercer v3.0)...")
            
            # Passamos os valores como ARGUMENTOS para o JS, e não via f-string
            script = """
            ([email, pw]) => {
                function fillShadowField(root) {
                    // Procura inputs no nível atual
                    const inputs = root.querySelectorAll('input');
                    inputs.forEach(i => {
                        // Seletor agressivo: type email ou ID/Name que contenha 'email'
                        if (i.type === 'email' || i.id.toLowerCase().includes('email') || i.getAttribute('name').toLowerCase().includes('email')) {
                            i.focus();
                            i.value = email; // Injeta o email exato recebido
                            // Avisa o Angular que o valor mudou
                            i.dispatchEvent(new Event('input', { bubbles: true }));
                            i.dispatchEvent(new Event('change', { bubbles: true }));
                            i.blur();
                        }
                        if (i.type === 'password') {
                            i.focus();
                            i.value = pw;
                            i.dispatchEvent(new Event('input', { bubbles: true }));
                            i.dispatchEvent(new Event('change', { bubbles: true }));
                            i.blur();
                        }
                    });
                    
                    // Procura em Shadow Roots de outros elementos (Web Components)
                    const allElements = root.querySelectorAll('*');
                    allElements.forEach(el => {
                        if (el.shadowRoot) {
                            fillShadowField(el.shadowRoot);
                        }
                    });
                }
                fillShadowField(document);
            }
            """
            
            # Injetamos os dados passando-os como uma lista de argumentos [email, pw]
            page.evaluate(script, [user_email, user_password])

            time.sleep(2)
            print("4. A submeter...")
            # Pressiona Enter para submeter o formulário validado
            page.keyboard.press("Enter")
            
            # Backup: clica no botão Entrar que vi nos teus prints
            try:
                page.locator("button.ant-btn-primary, button:has-text('Entrar')").click(timeout=3000)
            except: pass

            print("5. A verificar URL final...")
            time.sleep(20)
            print(f"URL Final: {page.url}")
            page.screenshot(path="final_login_result.png")

        except Exception as e:
            print(f"Erro: {e}")
            page.screenshot(path="erro_fatal.png")

        context.close()
        browser.close()

if __name__ == "__main__":
    run()
