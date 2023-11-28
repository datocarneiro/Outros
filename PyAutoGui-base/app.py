# pip install pyautogui
import pyautogui


# Aqui está um exemplo simples de como você pode capturar a posição do mouse:
# Este código cria um loop infinito que imprime continuamente a posição do mouse 
# até que seja interrompido pelo usuário pressionando Ctrl+C.
try:
    while True:
        x, y = pyautogui.position()
        print(f'Posição do mouse: x={x} y={y}')
except KeyboardInterrupt:
    print('\nCaptura de posição do mouse encerrada.')

# escala do mause mouse apenas quando ocorrerem eventos, como cliques do mouse
# Este código permanecerá em execução até que você o interrompa manualmente

#  pip install pyautogui pynput
import pyautogui
from pynput import mouse
def on_click(x, y, button, pressed):
    if pressed:
        print(f'Clique do mouse! Posição: x={x} y={y}, button={button}')
# Configura o listener para capturar eventos de clique do mouse
with mouse.Listener(on_click=on_click) as listener:
    listener.join()

# Obtém as dimensões do monitor primário.
screenWidth, screenHeight = pyautogui.size()

# Obtém as coordenadas X e Y atuais do mouse.
currentMouseX, currentMouseY = pyautogui.position()

# Move o cursor do mouse para as coordenadas (100, 150).
pyautogui.moveTo(100, 150)

# Para clicar com o botão esquerdo do mouse, você pode usar o método click() sem especificar o botão, pois o botão esquerdo é o padrão.#
pyautogui.click() # OU pyautogui.click(button='right')

# Para clicar com o botão DIREITO do mouse Se você quiser ser explícito, também pode usar
pyautogui.click(button='left')

# Move o cursor para as coordenadas (100, 200) e clica.
pyautogui.click(100, 200)

# Localiza a posição da imagem 'button.png' e clica nela.
pyautogui.click('button.png')

# Move o cursor do mouse 400 pixels para a direita.
pyautogui.move(400, 0)

# Realiza um duplo clique do mouse.
pyautogui.doubleClick()

# Move o cursor do mouse para (500, 500) em 2 segundos, usando interpolação suave.
pyautogui.moveTo(500, 500, duration=2, tween=pyautogui.easeInOutQuad)

# Simula a digitação da frase 'Hello world!' com pausas de 0.25 segundos entre cada caractere.
pyautogui.write('Hello world!', interval=0.25)

# Simula a pressão da tecla 'Esc'.
pyautogui.press('esc')

# Pressiona e mantém a tecla Shift pressionada, em seguida, pressiona a tecla de seta para a esquerda quatro vezes.
with pyautogui.hold('shift'):
    pyautogui.press(['left', 'left', 'left', 'left'])

# Simula a combinação de teclas Ctrl + C.
pyautogui.hotkey('ctrl', 'c')

# Exibe uma caixa de alerta com a mensagem 'This is the message to display.' e pausa a execução até clicar em OK.
pyautogui.alert('This is the message to display.')

