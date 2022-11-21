from tkgpio import TkCircuit
from json import load

# Simulacao do circuito com os motores e botoes
with open("motor/simulation.json", "r") as file:
    config_analog = load(file)

analog = TkCircuit(config_analog)

@analog.run
def main():
    
    from gpiozero import Motor, Button, LED
    from time import sleep
    import encoder

    # Variaveis globais: gaps do encoder, angulo/velocidade/direcao do carrinho
    global gapsEncoder, angulo, velocidade, direcao, modoManual
    gapsEncoder = 0       # entre 0 e 20
    angulo = 0.0          # entre -360 e 360 graus
    velocidade = 0.0      # entre 0 e 1
    direcao = ""          # frente ou tras
    modoManual = True     # True - botoes, False - input


    # Pinagem de entrada da ponte H (Esq: ENA,IN1,IN2 / Dir: ENB,IN3,IN4)
    HBRIDGE_IN1 = 3
    HBRIDGE_IN2 = 4
    HBRIDGE_IN3 = 27
    HBRIDGE_IN4 = 22
    HBRIDGE_ENA = 2
    HBRIDGE_ENB = 17

    # Inicializa componentes
    motorEsq = Motor(HBRIDGE_IN1, HBRIDGE_IN2)
    motorDir = Motor(HBRIDGE_IN3, HBRIDGE_IN4)

    bt_modo = Button(10)
    bt_frente = Button(11)
    bt_tras = Button(12)
    bt_esq = Button(13)
    bt_dir = Button(14)
    bt_parar = Button(15)
    bt_encoder = Button(16)

    ledEncoder = LED(23)
    ledManual = LED(24)
    ledAuto = LED(25)


    # Funcoes de controle de direcao do carrinho
    def frente():
        global velocidade
        
        motorEsq.forward(velocidade)
        motorDir.forward(velocidade)

    def tras():
        global velocidade

        motorEsq.backward(velocidade)
        motorDir.backward(velocidade)

    def esquerda():
        global velocidade

        motorEsq.backward(velocidade)
        motorDir.forward(velocidade)

    def direita():
        global velocidade

        motorEsq.forward(velocidade)
        motorDir.backward(velocidade)

    def parar():
        motorEsq.stop()
        motorDir.stop()

    # Le o input do usuario com as intrucoes de movimento do carrinho
    def initialize():
        global angulo, velocidade, direcao

        # direcao = input("Para qual direcao deseja andar, 'frente' ou 'tras'?\n")
        # angulo = float(input("Para qual angulo deseja girar (em graus)?\n"))
        # velocidade = float(input("Com quanto de velocidade, entre 0 e 100 porcento?\n"))/100
        direcao = "frente"
        angulo = 70.0
        velocidade = 0.2

        print("Vc escolheu ir para %s com angulo %.2f graus e velocidade %.2f .\n"%(direcao, angulo, velocidade))

    # Faz a movimentacao do carrinho (modo automatico)
    def start_car():
        global gapsEncoder, angulo, velocidade, direcao

        anguloAtual = encoder.calculaAnguloDoCarrinho(gapsEncoder)
        print("Angulo atual:", anguloAtual)

        # Movimenta o carrinho
        if angulo < 0:
            giro_esquerda(anguloAtual)
        elif angulo > 0:
            giro_direita(anguloAtual)
        else:
            andar()


    # Gira o carrinho pra esquerda quando o angulo desejado é negativo (modo automatico)
    def giro_esquerda(anguloAtual):
        global angulo

        if anguloAtual < abs(angulo):
            esquerda()
        else:
            parar()
            andar()

    # Gira o carrinho pra direita quando o angulo desejado é positivo (modo automatico)
    def giro_direita(anguloAtual):
        global angulo

        if anguloAtual < abs(angulo):
            direita()
        else:
            parar()
            andar()

    # Anda com o carrinho (modo automatico)
    def andar():
        global direcao

        if direcao == "frente":
            frente()
        elif direcao == "tras":
            tras()

    # Troca o modo de operacao do carrinho
    def trocaModo():
        global modoManual

        # Para os motores pra trocar o modo
        parar()

        # Troca o modo do carrinho
        modoManual = (not modoManual)

        if modoManual:
            print("Modo controle por botoes")
            ledManual.on()
            ledAuto.off()
        else:
            print("Modo controle automatico lido da entrada")
            ledManual.off()
            ledAuto.on()
    
    # Para simular o encoder
    # Incrementa o contador de gaps do encoder
    def count_gaps():
        global gapsEncoder
        gapsEncoder+=1

        print("Gaps: %d"%(gapsEncoder))

    # Callback quando contamos um gap do encoder (pressionando botao/alcance sensor distancia)
    def count_triggered():
        count_gaps()
        ledEncoder.on()

    initialize()

    while True:
        # Gatilho do contador: botao ou distance sensor
        bt_encoder.when_pressed = count_triggered
        bt_encoder.when_released = ledEncoder.off

        # Troca o modo de manual (botoes) pra automatico (lido do input)
        bt_modo.when_pressed = trocaModo

        # Verifica o modo de operacao do carrinho
        if modoManual:
            # Botoes de controle manual do motor
            bt_frente.when_pressed = frente
            bt_tras.when_pressed = tras
            bt_esq.when_pressed = esquerda
            bt_dir.when_pressed = direita
            bt_parar.when_pressed = parar
        else:
            start_car()

            # TODO: critério de parada do carrinho
            # Distancia de um giro completo da roda: 20.1cm --> 20 gaps do encoder

        sleep(0.05)

