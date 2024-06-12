import sys
import os

'''
Creates a readable version of a UVSim program file
Syntax: python convert.py [file]
Writes to a new file called [file]_READABLE.txt
'''

def convert(program: str)->None:
    '''Reads the input program file and writes each line to a new file with English instructions appended'''
    with open (program[:-4] + '_READABLE.txt', 'w') as wfile:
        with open (program, 'r') as rfile:
            for line in rfile:
                char_check = 0
                if line[0] == '+' or line[0] == '-': # Start char check at 1
                    char_check = 1
                else:
                    char_check = 0

                match line[char_check:char_check+2]:
                    case '10': newline = ' READ to ' #READ
                    case '11': newline = ' WRITE to screen ' #WRITE
                    case '20': newline = ' LOAD from ' #LOAD
                    case '21': newline = ' STORE to ' #STORE
                    case '30': newline = ' ADD from ' #ADD
                    case '31': newline = ' SUBTRACT from ' #SUBTRACT
                    case '32': newline = ' DIVIDE from ' #DIVIDE
                    case '33': newline = ' MULTIPLY from ' #MULTIPLY
                    case '40': newline = ' BRANCH to ' #BRANCH
                    case '41': newline = ' BRANCHNEG to ' #BRANCHNEG
                    case '42': newline = ' BRANCHZERO to ' #BRANCHZERO
                    case '43': newline = ' HALT' #HALT
                    case _: newline = ' (VALUE)' #VALUE
                if newline[-1] != ' ':
                    wfile.write(line.strip() + newline + '\n')
                else:
                    wfile.write(line.strip() + newline + line[char_check+2:char_check+4] + '\n')
                
def main():
    if len(sys.argv) > 2 or len(sys.argv) < 2:
        raise IndexError('Usage: python convert.py [file]')

    file = sys.argv[1]

    if not os.path.exists(file):
        raise FileNotFoundError(f'The file "{file}" does not exist')

    convert(file)

if __name__ == '__main__':
    main()