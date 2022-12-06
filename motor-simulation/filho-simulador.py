import time
import argparse

parser = argparse.ArgumentParser( description = 'Test.' )
parser.add_argument( 'text', action = 'store', type = str, help = 'The text to parse.' )

args = parser.parse_args()

print(args.text)

with open("motor-simulation\simulation-control.py", 'r') as f:
    stringComandos = f.read()
    stringComandos = stringComandos.replace("pass", args.text)
    
    with open("output.txt", 'w') as file:
        file.write(stringComandos)

    codeObject = compile(stringComandos, '', 'exec')
    exec(codeObject)
    



exit()