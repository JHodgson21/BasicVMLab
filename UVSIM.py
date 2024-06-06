# -*- coding: utf-8 -*-
"""
Created on Wed May 22 17:37:33 2024

@author: Jakob
"""

import sys
import os
# changed 'memory' to instructions
# added 'memory' to hold values rather than instructions 
#   previously: instructions were overwritten by new written values (caused errors when branching)
class UVSim:
    def __init__(self):
        # changed to 20 for readability while debugging
        self.instructions = [0] * 20#100  # 100 instructions initialized to zero
        self.memory = [0] * 20#100 # stores written values; memory location 1: memory[1] 
        self.accumulator = 0  # Accumulator register
        self.instruction_counter = 0  #Instructions counter
        self.running = True  # Simulator running

    def load_program(self, program):
        """ Load the program into the instructions starting at location 0 """
        for i, instruction in enumerate(program):
            self.instructions[i] = instruction

    def fetch(self):
        """ Fetch the next instruction """
        instruction = self.instructions[self.instruction_counter]
        #print('memory', self.memory) # REMOVE LATER (DEBUG)
        #print('instructions', self.instructions) #REMOVE LATER (DEBUG)
        self.instruction_counter += 1 
        return instruction

    def decode_execute(self, instruction):
        """ Decode and execute the instruction """
        # Ignore first digit of program-loaded instructions as they are always positive.
        instruction = instruction[1:]
        opcode = instruction[:2] # First two digits
        operand = instruction[2:4] # Last two digits
        # checked as strs in following blocks (solves 01 vs 1 issue); cast to ints for indexing
        opcode = opcode
        operand = operand

        if opcode == '10':  # READ
            # Forces input to be an int.
            negative = False
            while(True):
                value = input("Enter an integer: ")
                # If negative, saves as negative int
                if (value[0] == "-"):
                    negative = True
                try:
                    if (negative):
                        value = -abs(int(value))
                    else:
                        value = int(value)
                    break
                except ValueError:
                    print("Not a valid integer.\n")
            self.memory[int(operand)] = value
        elif opcode == '11':  # WRITE
            print(self.memory[int(operand)])
        elif opcode == '20':  # LOAD
            self.accumulator = self.memory[int(operand)]
        elif opcode == '21':  # STORE
            self.memory[int(operand)] = self.accumulator
        elif opcode == '30':  # ADD
            self.accumulator += self.memory[int(operand)]
        elif opcode == '31':  # SUBTRACT
            self.accumulator -= self.memory[int(operand)]
        elif opcode == '32':  # DIVIDE
            if self.memory[int(operand)] == 0:
                raise ZeroDivisionError("Attempted division by zero")
            self.accumulator //= self.memory[int(operand)]
        elif opcode == '33':  # MULTIPLY
            self.accumulator *= self.memory[int(operand)]
        elif opcode == '40':  # BRANCH
            self.instruction_counter = int(operand)
        elif opcode == '41':  # BRANCHNEG
            if self.accumulator < 0:
                self.instruction_counter = int(operand)
        elif opcode == '42':  # BRANCHZERO
            if self.accumulator == 0:
                self.instruction_counter = int(operand)
        elif opcode == '43':  # HALT
            self.running = False
        else:
            raise ValueError(f"Unknown opcode {opcode}")

    def run(self):
        """ Run the simulation """
        while self.running:
            instruction = self.fetch()
            self.decode_execute(instruction)

# Example Run (we will need to use the file the prof gives us).
# program = [
#     1007,  # READ to instructions location 07
#     1008,  # READ to instructions location 08
#     2007,  # LOAD from instructions location 07
#     3008,  # ADD from instructions location 08
#     2109,  # STORE to instructions location 09
#     1109,  # WRITE from instructions location 09
#     4300   # HALT
# ]

def get_program():
    if len(sys.argv) < 2:
      print("Usage: python UVSIM.py <testFile.txt>")
      sys.exit()
    program_name = sys.argv[1]

    if not os.path.exists(program_name):
        print(f"The file {program_name} does not exist.")
        sys.exit()
    
    print('Testing: ', program_name)
    program_lines = []
    with open(program_name, "r") as file:
        for line in file:
            program_lines.append(line.rstrip())
    return program_lines

program = get_program()

# Create a uvsim instance
uvsim = UVSim()

# Loading the program into instructions
uvsim.load_program(program)

#Run it!
uvsim.run()
