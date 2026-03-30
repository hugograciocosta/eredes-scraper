import os
import time
from playwright.sync_api import sync_playwright

def run():
    user_email = os.environ.get("EREDES_EMAIL")
    user_password = os.environ.get("EREDES_PASSWORD")

    with sync_playwright() as p:
        # Usamos Chromium mas com uma identidade de browser real
        browser = p.chromium.launch(headless=True)
        
        # Simulamos um utilizador real num ecrã normal
        context = browser.new_context(
            user_agent="Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36",
            viewport={'width': 1920, 'height': 1080}
        )
        page = context.new_page()
        
        print("1. A carregar o portal E-Redes (com identidade real)...")
        page.goto("https://balcaodigital.e-redes.pt/login", wait_until="networkidle")
        
        # Pausa para o JavaScript do site assentar
        time.sleep(5)

        print("2. A tentar forçar o clique no 'Empresarial' via JavaScript...")
        try:
            # Este comando procura o elemento que contém "Empresarial" e clica via JS puro
            # Ignora proteções visuais ou sobreposições
            page.evaluate("""
                const elements = document.querySelectorAll('app-login-option');
                for (let el of elements) {
                    if (el.innerText.includes('Empresarial')) {
                        el.click();
                        break;
                    }
                }
            """)
            print("Comando de clique enviado.")
        except Exception as e:
            print(f"Erro no clique JS: {e}")

        print("3. A aguardar a transição para a EDP ID...")
        # Esperamos que o URL mude. Se o clique funcionou, o URL TEM de mudar.
        try:
            page.wait_for_url("**/login.edp.pt/**", timeout=30000)
            print(f"Sucesso! Entrámos na página da EDP: {page.url}")
            
            # 4. Preencher o Login
            print("4. A preencher credenciais...")
            page.wait_for_selector('input[type="email"]', state="visible")
            page.fill('input[type="email"]', user_email)
            page.fill('input[type="password"]', user_password)
            
            # Clicar no Entrar
            page.get_by_role("button", name="Entrar").click()
            
            print("5. A aguardar o Dashboard final...")
            time.sleep(15)
            print(f"Página Final: {page.url}")

        except Exception:
            print(f"O site não reagiu ao clique. URL atual: {page.url}")
            # Se falhar, vamos tirar um print para ver o que o robô está a ver
            page.screenshot(path="visao_do_robo.png")

        browser.close()

if __name__ == "__main__":
    run()
