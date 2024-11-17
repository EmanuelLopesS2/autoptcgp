import threading
import keyboard
import pyautogui
import time
from screeninfo import get_monitors
import os

# Ajuste este caminho para a pasta onde as suas imagens estão guardadas
IMAGE_FOLDER = "./img/"  
running = True

# Para o monitor principal (primeiro monitor)
MONITOR_X = 0
MONITOR_Y = 0

# Para o segundo monitor (exemplo, ajuste conforme necessário)
# MONITOR_X = -1360  # largura do monitor secundário (negativo pois está à esquerda)
# MONITOR_Y = 312   # diferença de altura para alinhar em baixo (1080 - 768)

# Adicione no início do programa para debug
print("Informação dos ecrãs:")
for i, monitor in enumerate(get_monitors()):
    print(f"Monitor {i+1}: {monitor}")

# Teste para verificar se o rato move para posições seguras
#print("A testar posições do rato...")
#time.sleep(2)
#pyautogui.moveTo(MONITOR_X + 10, MONITOR_Y + 10)  # Próximo ao canto superior esquerdo
#time.sleep(1)
#pyautogui.moveTo(MONITOR_X + 1910, MONITOR_Y + 1070)  # Próximo ao canto inferior direito

# Adicione no início para debug
print(f"Pasta atual: {os.getcwd()}")
print(f"A procurar imagens em: {os.path.abspath(IMAGE_FOLDER)}")
print(f"Ficheiros encontrados: {os.listdir(IMAGE_FOLDER)}\n")

def pause_script():
    print("Prima ESC para terminar o script...\n")
    global running
    while True:
        if keyboard.is_pressed('esc'):
            running = False
            print("\nScript terminado!")
            # Move o rato para o meio do ecrã principal
            pyautogui.moveTo(MONITOR_X + 960, MONITOR_Y + 540)  # 1920/2 = 960, 1080/2 = 540
            os.system('cls') # Limpa a consola
            os._exit(0)  # Força o encerramento completo do programa
        time.sleep(0.1)

def countdown_sleep(seconds, message):
    for i in range(seconds, 0, -1):
        print(f"\r{message} {i} segundos...", end="", flush=True)
        time.sleep(1)
    print()  # Nova linha no final

def check_sequence():
    global running
    i = 1
    try:
        while running:
            print(f"\n🔄 A iniciar sequência pela {i}ª vez...")
            
            # A procurar battle.png
            while running:
                print(f"\n🔍 A procurar battle.png...")
                print(f"📍 A procurar battle.png na região: x={MONITOR_X + 700}, y={MONITOR_Y + 700}, largura=400, altura=200")
                location = pyautogui.locateOnScreen(IMAGE_FOLDER + 'battle.png', confidence=0.8, region=(MONITOR_X + 700, MONITOR_Y + 700, 400, 200))
                if location:
                    print("✅ Battle encontrado! A clicar...")
                    countdown_sleep(2, "⏳ A aguardar")
                    pyautogui.click(pyautogui.center(location))
                    break
                countdown_sleep(1, "🔄 A tentar encontrar battle.png novamente em")
            
            countdown_sleep(30, "⏳ A esperar pelo draw das cartas")
            
            # A procurar 3tracos.png
            while running:
                print(f"\n🔍 A procurar 3tracos.png...")
                location = pyautogui.locateOnScreen(IMAGE_FOLDER + '3tracos.png', 
                    confidence=0.7,
                    region=(MONITOR_X + 600, MONITOR_Y + 750, 200, 200))
                if location:
                    print("✅ 3tracos.png encontrado! A clicar...")
                    pyautogui.click(pyautogui.center(location))
                    countdown_sleep(1, "⏳ A aguardar")
                    break
                countdown_sleep(1, "🔄 A tentar encontrar 3tracos.png novamente em")

            # A procurar e clicar concede
            tentativas_concede = 0
            max_tentativas = 3
            while running and tentativas_concede < max_tentativas:
                print(f"\n👆 A tentar clicar concede (tentativa {tentativas_concede + 1}/{max_tentativas})")
                pyautogui.click(920, 690)
                countdown_sleep(1, "⏳ A clicar concede novamente em")
                pyautogui.click(925, 620)
                tentativas_concede += 1
                if tentativas_concede < max_tentativas:
                    countdown_sleep(1, "🔄 Próxima tentativa em")
                else:
                    countdown_sleep(1, "⏳ A aguardar")
                break

            # Clicar para saltar
            print(f"\n⏭️ A saltar...")
            countdown_sleep(7, "⏳ A aguardar para saltar em")
            # Clica duas vezes na posição atual
            pyautogui.click(960, 980)
            countdown_sleep(1, "👆 Primeiro clique em")
            pyautogui.click(960, 980)
            countdown_sleep(1, "👆 Segundo clique em")
            # Clica uma vez na nova posição
            pyautogui.click(960, 840)
            countdown_sleep(1, "👆 Terceiro clique em")
            # Clique adicional após 5 segundos
            countdown_sleep(5, "⏳ A aguardar para clique final em")
            pyautogui.click(960, 980)
            countdown_sleep(1, "👆 Clique final em")

            print(f"\n🎉 Sequência concluída pela {i}ª vez!\n")
            i += 1
            countdown_sleep(6, "🔄 A iniciar próxima sequência em")

    except Exception as e:
        print(f"\n❌ Erro: {e}")
        print("⚠️ Tentando continuar a execução...")
        countdown_sleep(5, "🔄 Reiniciando em")
        check_sequence()

if __name__ == "__main__":

    # Inicia a thread de pausa
    pause_thread = threading.Thread(target=pause_script)
    pause_thread.daemon = True
    pause_thread.start()
    time.sleep(1)
    #aparecer um contador regressivo de 5 segundos que muda o texto a cada segundo na mesma linha
    for i in range(5, 0, -1):
        print(f"\rA iniciar sequência em {i} segundos...", end="", flush=True)
        time.sleep(1)

    # Inicia a verificação das imagens
    check_sequence()

