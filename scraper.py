import os
import time
from playwright.sync_api import sync_playwright

def run():
    # Credenciais guardadas no GitHub Secrets
    user_email = os.environ.get("EREDES_EMAIL")
    user_password = os.environ.get("EREDES_PASSWORD")

    with sync_playwright() as p:
        # Lançar o browser
        browser = p.chromium.launch(headless=True)
        context = browser.new_context(viewport={'width': 1280, 'height': 800})
        page = context.new_page()
        
        print("1. A abrir a página de login da E-Redes...")
        page.goto("https://balcaodigital.e-redes.pt/login", wait_until="networkidle")
        
        # Aceitar cookies para limpar a visão do robô
        try:
            page.get_by_role("button", name="Aceitar").click(timeout=5000)
            time.sleep(1)
        except:
            pass

        print("2. A clicar no botão 'Empresarial'...")
        try:
            # Preparamos o contexto para detetar se uma nova janela se abre
            with context.expect_page(timeout=10000) as new_page_info:
                page.get_by_text("Empresarial").click()
            
            # Se abriu uma nova janela, trabalhamos nela. Se não, continuamos na atual.
            target_page = new_page_info.value if new_page_info else page
            print(f"Página de destino confirmada: {target_page.url}")
            
        except Exception:
            # Se não abriu nova janela, o 'Empresarial' pode ter carregado na mesma aba
            print("Nota: Não abriu nova janela, a continuar na página atual.")
            target_page = page

        # 3. Preencher o formulário de login (EDP ID)
        print("3. A aguardar campos de e-mail e password...")
        try:
            # Espera que o campo de email esteja visível e pronto
            target_page.wait_for_selector('input[type="email"]', timeout=20000, state="visible")
            
            print("4. A introduzir credenciais...")
            target_page.fill('input[type="email"]', user_email)
            time.sleep(1) # Pequena pausa para simular humano
            target_page.fill('input[type="password"]', user_password)
            
            print("5. A submeter login...")
            # Clica no botão 'Entrar' ou no botão de submit do formulário
            target_page.locator('button[type="submit"], button:has-text("Entrar")').first.click()
            
            # Espera 15 segundos para o Dashboard carregar totalmente
            print("A aguardar carregamento do Dashboard...")
            time.sleep(15)
            
            print(f"URL Final Alcançado: {target_page.url}")
            
            if "login" not in target_page.url.lower():
                print("SUCESSO: Login efetuado com êxito!")
            else:
                print("AVISO: O URL ainda indica página de login. Verifica as credenciais.")
                target_page.screenshot(path="falha_login.png")

        except Exception as e:
            print(f"Erro no processo de preenchimento: {e}")
            target_page.screenshot(path="erro_final.png")

        browser.close()

if __name__ == "__main__":
    run()
