from tkgpio import TkCircuit
from json import load

# initialize the circuit inside the GUI
with open("motor/simulation.json", "r") as file:
    config_analog = load(file)

analog = TkCircuit(config_analog)

@analog.run
def main():
    
    from gpiozero import Motor, Button
    from time import sleep

    MOTOR_SPEED = 0.5

    motorEsq = Motor(22, 23)
    motorDir = Motor(24, 25)

    frente = Button(11)
    tras = Button(12)
    esq = Button(13)
    dir = Button(14)
    parar = Button(15)


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


    while True:
        frente.when_pressed = forward
        tras.when_pressed = backward
        esq.when_pressed = left
        dir.when_pressed = right
        parar.when_pressed = stop

        sleep(0.05)

