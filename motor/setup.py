from tkgpio import TkCircuit
from json import load

# initialize the circuit inside the GUI
with open("motor/analog.json", "r") as file:
    config_analog = load(file)

# with open("setup/circuit.json", "r") as file:
#     config_circuit = load(file)
    
# circuit = TkCircuit(config_circuit)
analog = TkCircuit(config_analog)

@analog.run
def main():
    
    from gpiozero import Motor, MCP3008, Button
    from time import sleep


    motor1 = Motor(22, 23)
    motor2 = Motor(24, 25)

    potenciometer1 = MCP3008(0)
    potenciometer2 = MCP3008(1)
    switch1 = Button(15)
    switch2 = Button(16)


    while True:

        if switch1.is_pressed:
            motor1.forward(potenciometer1.value)
        else:
            motor1.backward(potenciometer1.value)

        if switch2.is_pressed:
            motor2.forward(potenciometer2.value)
        else:
            motor2.backward(potenciometer2.value)

        sleep(0.05)