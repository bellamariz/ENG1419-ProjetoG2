
import time
import argparse

parser = argparse.ArgumentParser( description = 'Test.' )
parser.add_argument( 'text', action = 'store', type = str, help = 'The text to parse.' )

args = parser.parse_args()

print(args.text)

codeObject = compile(args.text, '', 'exec')
exec(codeObject)


exit()