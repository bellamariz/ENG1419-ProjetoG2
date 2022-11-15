from tkgpio import TkCircuit
from json import load
import encoder

# Simulacao do circuito com os motores e botoes
with open("motor/simulation.json", "r") as file:
    config_analog = load(file)

analog = TkCircuit(config_analog)

@analog.run
def main():
    
    from gpiozero import Motor, Button, DistanceSensor, LED
    from time import sleep

    # Contador que simula o numero de gaps do encoder
    global gaps, anguloCarrinho
    gaps = 0
    anguloCarrinho = 0

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

    distance_sensor = DistanceSensor(trigger=17, echo=18)
    distance_sensor.threshold_distance = 0.1

    led1 = LED(21)


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

    # Incrementa o contador de gaps do encoder
    def count_gaps():
        global gaps, anguloCarrinho
        gaps+=1
        anguloCarrinho = encoder.calculaAnguloDoCarrinho(gaps)

        print("Gaps: %d - Angulo: %.2f"%(gaps, anguloCarrinho))

    # Callback quando contamos um gap do encoder (pressionando botao/alcance sensor distancia)
    def count_triggered():
        count_gaps()
        led1.on()


    while True:
        # Botoes de controle do motor
        bt_frente.when_pressed = forward
        bt_tras.when_pressed = backward
        bt_esq.when_pressed = left
        bt_dir.when_pressed = right
        bt_parar.when_pressed = stop

        # Gatilho do contador: botao ou distance sensor
        bt_encoder.when_pressed = count_triggered
        bt_encoder.when_released = led1.off
        distance_sensor.when_in_range = count_triggered
        distance_sensor.when_out_of_range = led1.off

        # Se o carrinho atingiu um certo angulo (ex: 80 graus), parar os motores
        if anguloCarrinho >= 80.0:
            stop()

        sleep(0.05)

