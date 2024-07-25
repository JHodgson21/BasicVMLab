# -*- coding: utf-8 -*-
"""
Created on Wed May 22 17:37:33 2024

@author: Jakob
"""

import sys

class UVSim:
    def __init__(self):
<<<<<<< Updated upstream
        self.memory = [0] * 100  # 100 memory initialized to zero
        self.accumulator = 0  # Accumulator register
        self.instruction_counter = 0  #Instructions counter
        self.running = True  # Simulator running
=======
        self.memory = ['+000000'] * 250  # Initialize memory with +0000
        self.accumulator = 0
        self.instruction_counter = 0
        self.running = True
        self.file = FileLoader()
>>>>>>> Stashed changes

    def load_program(self, program):
        """ Load the program into the memory starting at location 0 """
        for i, instruction in enumerate(program):
            self.memory[i] = instruction

    def fetch(self):
<<<<<<< Updated upstream
        """ Fetch the next instruction """
        instruction = self.memory[self.instruction_counter]
=======
        inst = self.memory[self.instruction_counter]
        print(inst)
        length = len(inst) - 1
        if (length == 4):
            instruction = InstructionHandler4(inst).parse()
        elif (length == 6):
            instruction = InstructionHandler6(inst).parse()
        else:
            raise Exception("Invalid instruction length")
>>>>>>> Stashed changes
        self.instruction_counter += 1
        return [instruction,length]

<<<<<<< Updated upstream
    def decode_execute(self, instruction):
        """ Decode and execute the instruction """
        # Ignore first digit of program-loaded instructions as they are always positive.
        instruction = instruction[1:]
        opcode = instruction[:2] # First two digits
        operand = instruction[2:4] # Last two digits
        opcode = int(opcode)
        operand = int(operand)
=======
    def decode_execute(self, instruction, inst_length):
        
        operation = instruction[0]
        operand = instruction[1]
        if instruction[0] == '-':
            operation = -operation
>>>>>>> Stashed changes

        if opcode == 10:  # READ
            # Forces input to be an int.
            negative = False
            while(True):
                value = input("Enter an integer: ")
                # If negative, saves as negative int
                if (value[0] == "-"):
                    negative = True
                try:
                    if (negative == True):
                        value = -abs(int(value))
                    else:
                        value = int(value)
                    break
                except ValueError:
                    print("Not a valid integer.\n")
            self.memory[operand] = value
        elif opcode == 11:  # WRITE
            print(self.memory[operand])
        elif opcode == 20:  # LOAD
            self.accumulator = self.memory[operand]
        elif opcode == 21:  # STORE
            self.memory[operand] = self.accumulator
        elif opcode == 30:  # ADD
            self.accumulator += self.memory[operand]
        elif opcode == 31:  # SUBTRACT
            self.accumulator -= self.memory[operand]
        elif opcode == 32:  # DIVIDE
            if self.memory[operand] == 0:
                raise ZeroDivisionError("Attempted division by zero")
            self.accumulator //= self.memory[operand]
        elif opcode == 33:  # MULTIPLY
            self.accumulator *= self.memory[operand]
        elif opcode == 40:  # BRANCH
            self.instruction_counter = operand
        elif opcode == 41:  # BRANCHNEG
            if self.accumulator < 0:
                self.instruction_counter = operand
        elif opcode == 42:  # BRANCHZERO
            if self.accumulator == 0:
                self.instruction_counter = operand
        elif opcode == 43:  # HALT
            self.running = False
<<<<<<< Updated upstream
        else:
            raise ValueError(f"Unknown opcode {opcode}")

    def run(self):
        """ Run the simulation """
        while self.running:
            instruction = self.fetch()
            self.decode_execute(instruction)
=======
        
        try:
            self.validate(self.accumulator, inst_length)
        except Exception as e:
            return e
        

    def output(self, operand):
        print(int(self.memory[operand]))
    
    def validate(self, acc, len):
        if (len == 4):
            if (acc > 9999):
                raise Exception("Overflow: Accumulator is greater than memory linit of 9999.")
            elif (acc > 999999):
                raise Exception("Overflow: Accumulator is greater than memory linit of 999999.")
            else:
                raise Exception("Instruction length invalid.")
>>>>>>> Stashed changes

# Example Run (we will need to use the file the prof gives us).
# program = [
#     1007,  # READ to memory location 07
#     1008,  # READ to memory location 08
#     2007,  # LOAD from memory location 07
#     3008,  # ADD from memory location 08
#     2109,  # STORE to memory location 09
#     1109,  # WRITE from memory location 09
#     4300   # HALT
# ]

def get_program():
    if len(sys.argv) < 2:
      print("Usage: python UVSIM.py <testFile.txt>")
      sys.exit()
    program_name = sys.argv[1]
    print('Testing: ', program_name)
    program_lines = []
    with open(program_name, "r") as file:
        for line in file:
            program_lines.append(line.rstrip())
    return program_lines

program = get_program()

# Create a uvsim instance
uvsim = UVSim()

# Loading the program into memory
uvsim.load_program(program)

#Run it!
uvsim.run()
