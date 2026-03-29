import os
import time
from playwright.sync_api import sync_playwright

def run():
    # Puxar as credenciais
    user_email = os.environ.get("EREDES_EMAIL")
    user_password = os.environ.get("EREDES_PASSWORD")

    with sync_playwright() as p:
        # Lançar o browser
        browser = p.chromium.launch(headless=True)
        context = browser.new_context(viewport={'width': 1280, 'height': 800})
        page = context.new_page()
        
        print("1. A abrir a página inicial...")
        page.goto("https://balcaodigital.e-redes.pt/home", wait_until="networkidle")
        time.sleep(3) # Pausa para carregar tudo

        # 2. Cookies (Essencial para libertar o ecrã)
        try:
            page.get_by_role("button", name="Aceitar").click(timeout=5000)
            print("Cookies aceites.")
            time.sleep(1)
        except:
            print("Banner de cookies não apareceu.")

        # 3. Clicar no botão 'Login' do topo (visto na tua foto)
        print("2. A clicar no link de Login no topo...")
        # Usamos o 'header' para garantir que clicamos no sítio certo
        page.locator("header").get_by_text("Login").click()
        
        # 4. Esperar que a página de formulário carregue
        print("3. A aguardar que o formulário apareça...")
        # Esperamos 10 segundos pelo campo de email
        page.wait_for_selector('input[type="email"]', timeout=15000)
        
        # 5. Preencher com calma
        print("4. A introduzir as credenciais...")
        page.locator('input[type="email"]').fill(user_email)
        time.sleep(1)
        page.locator('input[type="password"]').fill(user_password)
        time.sleep(1)
        
        # 6. Clicar no botão 'Entrar'
        print("5. A submeter o formulário...")
        page.get_by_role("button", name="Entrar").click()
        
        # 7. Verificação final
        time.sleep(8)
        print(f"Página após tentativa: {page.url}")
        
        if "login" not in page.url.lower():
            print("VITÓRIA: Saímos da zona de login!")
        else:
            print("ERRO: O login falhou ou o site pediu um segundo passo.")
            page.screenshot(path="falha_final.png")

        browser.close()

if __name__ == "__main__":
    run()
