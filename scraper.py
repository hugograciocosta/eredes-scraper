import os
import time
from playwright.sync_api import sync_playwright

def run():
    user_email = os.environ.get("EREDES_EMAIL")
    user_password = os.environ.get("EREDES_PASSWORD")

    with sync_playwright() as p:
        # Firefox é a nossa melhor aposta para este redirecionamento
        browser = p.firefox.launch(headless=True)
        context = browser.new_context(viewport={'width': 1280, 'height': 800})
        page = context.new_page()
        
        print("1. A abrir login da E-Redes...")
        page.goto("https://balcaodigital.e-redes.pt/login", wait_until="networkidle")
        
        # Aceitar cookies para limpar o caminho
        try:
            page.get_by_role("button", name="Aceitar").click(timeout=5000)
        except:
            pass

        print("2. A procurar e clicar no botão 'Empresarial'...")
        try:
            # Localizamos a caixa específica do login empresarial
            btn = page.locator("app-login-option").filter(has_text="Empresarial")
            btn.wait_for(state="visible", timeout=10000)
            # click(force=True) garante que o clique acontece mesmo que algo esteja à frente
            btn.click(force=True)
            print("Clique no botão 'Empresarial' executado.")
        except Exception as e:
            print(f"Erro ao clicar: {e}. A tentar alternativa por texto...")
            page.get_by_text("Empresarial").click(force=True)

        print("3. A aguardar redirecionamento para o sistema EDP ID...")
        try:
            # Esperamos que o URL mude para o domínio de login da EDP
            page.wait_for_url("**/login.edp.pt/**", timeout=20000)
            print(f"Sucesso! Estamos agora em: {page.url}")
            
            # 4. Preencher Credenciais
            print("4. A preencher email e password...")
            page.wait_for_selector('input[type="email"]', timeout=15000)
            page.fill('input[type="email"]', user_email)
            page.fill('input[type="password"]', user_password)
            
            print("5. A submeter formulário...")
            # Clicar no botão 'Entrar' (submit)
            page.locator('button[type="submit"]').first.click()
            
            # Espera longa para o site processar o login e entrar no Dashboard
            print("A aguardar entrada no Balcão Digital...")
            time.sleep(15)
            
            print(f"URL Final Alcançado: {page.url}")
            
            if "login" not in page.url.lower():
                print("VITÓRIA: Login concluído!")
            else:
                print("AVISO: O URL ainda indica página de login.")
                page.screenshot(path="falha_final.png")

        except Exception as e:
            print(f"Ocorreu um erro no redirecionamento/login: {e}")
            page.screenshot(path="debug_erro.png")

        browser.close()

if __name__ == "__main__":
    run()
