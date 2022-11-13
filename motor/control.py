from tkgpio import TkCircuit
from json import load
import encoder

# Simulacao do circuito com os motores e botoes
with open("motor/simulation.json", "r") as file:
    config_analog = load(file)

analog = TkCircuit(config_analog)

@analog.run
def main():
    
    from gpiozero import Motor, Button
    from time import sleep

    # Contador que simula o numero de gaps do encoder
    global gaps
    gaps = 0

    # Velocidade padrao do motor (sempre entre 0 e 1)
    MOTOR_SPEED = 0.5

    # Inicializa componentes
    motorEsq = Motor(22, 23)
    motorDir = Motor(24, 25)

    bt_frente = Button(11)
    bt_tras = Button(12)
    bt_esq = Button(13)
    bt_dir = Button(14)
    bt_parar = Button(15)
    bt_encoder = Button(16)


    # Funcoes de controle de direcao do carrinho
    def forward():
        motorEsq.forward(MOTOR_SPEED)
        motorDir.forward(MOTOR_SPEED)

    def backward():
        motorEsq.backward(MOTOR_SPEED)
        motorDir.backward(MOTOR_SPEED)

    def left():
        motorEsq.backward(MOTOR_SPEED)
        motorDir.forward(MOTOR_SPEED)

    def right():
        motorEsq.forward(MOTOR_SPEED)
        motorDir.backward(MOTOR_SPEED)

    def stop():
        motorEsq.stop()
        motorDir.stop()


    # Incrementa o contador de gaps do encoder (simulado pelo pressionar de um botao)
    def count_gaps():
        global gaps
        gaps+=1

        print("Gaps: ", gaps)


    while True:
        bt_frente.when_pressed = forward
        bt_tras.when_pressed = backward
        bt_esq.when_pressed = left
        bt_dir.when_pressed = right
        bt_parar.when_pressed = stop

        bt_encoder.when_pressed = count_gaps

        sleep(0.05)

