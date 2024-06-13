# -*- coding: utf-8 -*-
"""
Created on Wed May 22 17:37:33 2024

@authors: Jakob, Ben, Michael, Jarek
"""

import sys
import os

# Name of unittest file
TESTFILE = "UVSim Testing.py"

# merged memory and instructions into just "memory". ability to overwrite instructions is intended
class UVSim:
    def __init__(self):
        # changed to 20 for readability while debugging
        self.memory = [0] * 100 # stores written values; memory location 1: memory[1] 
        self.accumulator = 0  # Accumulator register
        self.instruction_counter = 0  #Instructions counter
        self.running = True  # Simulator running

    def load_program(self, program):
        """ Load the program into the instructions starting at location 0 """
        for i, instruction in enumerate(program):
            self.memory[i] = instruction

    def fetch(self):
        """ Fetch the next instruction """
        instruction = self.memory[self.instruction_counter]
        #print('memory', self.memory) # REMOVE LATER (DEBUG)
        #print('instructions', self.instructions) #REMOVE LATER (DEBUG)
        self.instruction_counter += 1 
        return instruction

    def decode_execute(self, instruction):
        """ Decode and execute the instruction """
        # Ignore first digit of program-loaded instructions as they are always positive.
        #instruction = str(instruction)
        if instruction[:1] in '+-': # Checks if the current instruction begins with a sign. If it does, ignore it
            instruction = instruction[1:]
        opcode = instruction[:2] # First two digits
        operand = instruction[2:4] # Last two digits
        # checked as strs in following blocks (solves 01 vs 1 issue); cast to ints for indexing
        #opcode = opcode
        operand = int(operand) # Operand references point in memory
    
        if opcode == '10':  # READ
            # Forces input to be an int.
            while(True):
                value = input("Enter an integer: ")
                try:
                    int(value) # Checks to make sure the input can be converted to an input NOT SURE IF THIS IS REQUIRED
                    break
                except ValueError:
                    print("Not a valid integer.\n")
            if int(value) < 0:
                self.memory[operand] = value.zfill(5)
            else:
                self.memory[operand] = '+' + value.zfill(4)

        elif opcode == '11':  # WRITE
            print(int(self.memory[operand]))

        elif opcode == '20':  # LOAD
            self.accumulator = int(self.memory[operand])

        elif opcode == '21':  # STORE
            if int(self.accumulator) < 0: # If negative, fill with an extra digit because "-" counts as a character
                self.memory[operand] = str(self.accumulator).zfill(5)
            else:
                self.memory[operand] = '+' + str(self.accumulator).zfill(4)

        elif opcode == '30':  # ADD
            self.accumulator += int(self.memory[operand])

        elif opcode == '31':  # SUBTRACT
            self.accumulator -= int(self.memory[operand])

        elif opcode == '32':  # DIVIDE
            if int(self.memory[operand]) == 0:
                raise ZeroDivisionError("Attempted division by zero")
            self.accumulator //= int(self.memory[operand])

        elif opcode == '33':  # MULTIPLY
            self.accumulator *= int(self.memory[operand])

        elif opcode == '40':  # BRANCH
            self.instruction_counter = operand

        elif opcode == '41':  # BRANCHNEG
            if self.accumulator < 0:
                self.instruction_counter = operand

        elif opcode == '42':  # BRANCHZERO
            if self.accumulator == 0:
                self.instruction_counter = operand

        elif opcode == '43':  # HALT
            self.running = False
        else:
            raise ValueError(f"Unknown opcode {opcode}")

    def run(self):
        """ Run the simulation """
        # Loading the program into instructions
        while self.running:
            instruction = self.fetch()
            self.decode_execute(instruction)

def get_program():
    # If the current file is the unittest, load an empty program without needing a file as an argument
    if sys.argv[0] == TESTFILE:
        program_lines = [
            '+4300' # IMMEDIATELY TERMINATE PROGRAM
        ]
        return program_lines
    
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
uvsim.load_program(program)
uvsim.run()
