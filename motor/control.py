from tkgpio import TkCircuit
from json import load

# Simulacao do circuito com os motores e botoes
with open("motor/simulation.json", "r") as file:
    config_analog = load(file)

analog = TkCircuit(config_analog)

@analog.run
def main():
    
    from gpiozero import Motor, Button, DistanceSensor, LED
    from time import sleep
    import encoder

    # Variaveis globais: gaps do encoder, angulo/velocidade/direcao do carrinho
    global gapsEncoder, angulo, velocidade, direcao
    gapsEncoder = 0       # entre 0 e 20
    angulo = 0.0          # entre 0 e 360 graus
    velocidade = 0.0      # entre 0 e 1
    direcao = ""          # fren, tras, esq, dir, para


    # Pinagem de entrada da ponte H (Esq: IN1,IN2 / Dir: IN3,IN4)
    HBRIDGE_IN1 = 22
    HBRIDGE_IN2 = 23
    HBRIDGE_IN3 = 24
    HBRIDGE_IN4 = 25

    # Inicializa componentes
    motorEsq = Motor(HBRIDGE_IN1, HBRIDGE_IN2)
    motorDir = Motor(HBRIDGE_IN3, HBRIDGE_IN4)

    bt_frente = Button(11)
    bt_tras = Button(12)
    bt_esq = Button(13)
    bt_dir = Button(14)
    bt_parar = Button(15)
    bt_encoder = Button(16)
    bt_start = Button(10)

    distance_sensor = DistanceSensor(trigger=17, echo=18)
    distance_sensor.threshold_distance = 0.1

    led1 = LED(21)


    # Funcoes de controle de direcao do carrinho
    def frente():
        motorEsq.forward(velocidade)
        motorDir.forward(velocidade)

    def tras():
        motorEsq.backward(velocidade)
        motorDir.backward(velocidade)

    def esquerda():
        motorEsq.backward(velocidade)
        motorDir.forward(velocidade)

    def direita():
        motorEsq.forward(velocidade)
        motorDir.backward(velocidade)

    def parar():
        motorEsq.stop()
        motorDir.stop()

    # Le o input do usuario com as intrucoes de movimento do carrinho
    def initialize():
        global angulo, velocidade, direcao

        direcao = input("Para qual direcao deseja andar?\n F - frente\n T - tras\n E - esquerda\n D - direita\n")
        angulo = float(input("Entre 0.0 e 360.0 graus, para qual angulo deseja ir?\n"))
        velocidade = float(input("Com quanto de velocidade, entre 0 e 100 porcento?\n"))/100

        print("Vc escolheu ir para %s com angulo %.2f graus e velocidade %.2f .\n"%(direcao, angulo, velocidade))
        start_car()

    # Faz a movimentacao do carrinho
    def start_car():
        global gapsEncoder, angulo, velocidade, direcao

        anguloAtual = encoder.calculaAnguloDoCarrinho(gapsEncoder)

        if anguloAtual < angulo:
        # Nao chegamos no angulo desejado ainda, continua girando o carrinho
            if direcao == "E":
                esquerda()
            elif direcao == "D":
                direita()
        # Terminou de girar ate o angulo desejado


    
    # Para simular o encoder
    # Incrementa o contador de gaps do encoder
    def count_gaps():
        global gapsEncoder
        gapsEncoder+=1

        print("Gaps: %d"%(gapsEncoder))

    # Callback quando contamos um gap do encoder (pressionando botao/alcance sensor distancia)
    def count_triggered():
        count_gaps()
        led1.on()


    while True:
        # Botoes de controle do motor
        bt_frente.when_pressed = frente
        bt_tras.when_pressed = tras
        bt_esq.when_pressed = esquerda
        bt_dir.when_pressed = direita
        bt_parar.when_pressed = parar

        # Gatilho do contador: botao ou distance sensor
        bt_encoder.when_pressed = count_triggered
        bt_encoder.when_released = led1.off
        distance_sensor.when_in_range = count_triggered
        distance_sensor.when_out_of_range = led1.off

        bt_start.when_pressed = initialize

        sleep(0.05)

