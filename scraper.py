import os
import time
from playwright.sync_api import sync_playwright

def run():
    # Vai buscar as credenciais aos Secrets do GitHub
    user_email = os.environ.get("EREDES_EMAIL")
    user_password = os.environ.get("EREDES_PASSWORD")

    with sync_playwright() as p:
        # Lançamos o Chromium
        browser = p.chromium.launch(headless=True)
        
        # Criamos o contexto com gravação de vídeo ativada
        context = browser.new_context(
            viewport={'width': 1280, 'height': 800},
            record_video_dir="videos/",
            user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36"
        )
        page = context.new_page()
        
        try:
            print("1. A abrir portal E-Redes...")
            page.goto("https://balcaodigital.e-redes.pt/login", wait_until="networkidle")
            
            # 2. Limpar Cookies
            print("2. A aceitar cookies para limpar o ecrã...")
            try:
                page.get_by_role("button", name="Aceitar todos os cookies").click(timeout=8000)
                time.sleep(2)
            except:
                print("Aviso: Barra de cookies não encontrada (pode já estar limpa).")

            # 3. Clicar no botão Empresarial
            print("3. A mover o rato e clicar em 'Empresarial'...")
            button = page.get_by_text("Empresarial")
            button.wait_for(state="visible", timeout=10000)
            
            # Usamos o bounding_box para um clique físico simulado
            box = button.bounding_box()
            if box:
                page.mouse.move(box['x'] + box['width'] / 2, box['y'] + box['height'] / 2)
                time.sleep(1) # Pausa para o vídeo registar o movimento
                page.mouse.click(box['x'] + box['width'] / 2, box['y'] + box['height'] / 2)
                print("Clique físico executado.")
            else:
                button.click(force=True)

            # 4. Aguardar a página da EDP carregar (onde o vídeo parava antes)
            print("4. A aguardar carregamento da página de login da EDP...")
            # Esperamos até 30 segundos pelo campo de email
            page.wait_for_selector('input[type="email"]', timeout=30000)
            print(f"Página de login detectada: {page.url}")

            # 5. Preenchimento "Humano" (Letra a letra)
            print("5. A preencher credenciais devagar...")
            
            # Focar e escrever o Email
            email_field = page.locator('input[type="email"]')
            email_field.click() # Clica primeiro para garantir foco
            time.sleep(0.5)
            email_field.type(user_email, delay=120) # Escreve com atraso entre teclas
            print("Email inserido.")

            # Focar e escrever a Password
            pass_field = page.locator('input[type="password"]')
            pass_field.click()
            time.sleep(0.5)
            pass_field.type(user_password, delay=120)
            print("Password inserida.")

            # Clicar no botão Entrar
            print("6. A submeter formulário...")
            page.get_by_role("button", name="Entrar").click()
            
            # Espera final para ver se entramos no Dashboard
            print("A aguardar redirecionamento final para o Balcão...")
            time.sleep(15)
            
            print(f"URL Final Alcançado: {page.url}")
            if "login" not in page.url.lower():
                print("VITÓRIA: Login concluído com sucesso!")
            else:
                print("ALERTA: O site ainda parece estar na página de login. Verifica o vídeo.")
                page.screenshot(path="resultado_final.png")

        except Exception as e:
            print(f"Erro detetado: {e}")
            page.screenshot(path="erro_fatal.png")

        # Fechar o contexto guarda o ficheiro de vídeo
        context.close()
        browser.close()

if __name__ == "__main__":
    run()
