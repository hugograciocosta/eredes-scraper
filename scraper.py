import os
import time
from playwright.sync_api import sync_playwright

def run():
    user_email = os.environ.get("EREDES_EMAIL")
    user_password = os.environ.get("EREDES_PASSWORD")

    with sync_playwright() as p:
        # Lançamos o browser
        browser = p.chromium.launch(headless=True)
        
        # Criamos o contexto COM GRAVAÇÃO DE VÍDEO
        context = browser.new_context(
            viewport={'width': 1280, 'height': 800},
            record_video_dir="videos/",
            user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36"
        )
        page = context.new_page()
        
        try:
            print("1. A abrir portal E-Redes...")
            page.goto("https://balcaodigital.e-redes.pt/login", wait_until="networkidle")
            
            # Passo dos Cookies (O vídeo vai mostrar isto a desaparecer)
            print("2. A limpar cookies...")
            try:
                page.get_by_role("button", name="Aceitar todos os cookies").click(timeout=8000)
                time.sleep(2)
            except:
                print("Barra de cookies não detectada.")

            print("3. A mover o rato para 'Empresarial'...")
            button = page.get_by_text("Empresarial")
            button.wait_for(state="visible", timeout=10000)
            
            # Cálculo de coordenadas para o vídeo mostrar o clique real
            box = button.bounding_box()
            if box:
                page.mouse.move(box['x'] + box['width'] / 2, box['y'] + box['height'] / 2)
                time.sleep(1) # Pausa para vermos o rato no vídeo
                page.mouse.click(box['x'] + box['width'] / 2, box['y'] + box['height'] / 2)
                print("Clique de rato real executado.")
            else:
                button.click(force=True)

            print("4. A aguardar 15s pelo redirecionamento...")
            # Esperamos para ver se o URL muda no vídeo
            time.sleep(15)
            print(f"URL após espera: {page.url}")

            if "login.edp.pt" in page.url:
                print("5. Sucesso! A preencher login...")
                page.fill('input[type="email"]', user_email)
                page.fill('input[type="password"]', user_password)
                page.get_by_role("button", name="Entrar").click()
                time.sleep(10)
            else:
                print("O redirecionamento não aconteceu. Verifica o vídeo.")
                page.screenshot(path="falha_final.png")

        except Exception as e:
            print(f"Erro durante a execução: {e}")
            page.screenshot(path="erro_fatal.png")

        # IMPORTANTE: Fechar o contexto para salvar o vídeo
        context.close()
        browser.close()

if __name__ == "__main__":
    run()
