# -*- coding: utf-8 -*-
"""
Created on Thu Jul 11 14:37:02 2024

@author: Jakob, Jarek, Ben, Michael
"""
import sys
from FL import FileLoader

# Name of unittest file
TESTFILE = "UVSim Testing.py"

class UVSim:
    def __init__(self):
        self.memory = ['+0000'] * 100  # Initialize memory with +0000
        self.accumulator = 0
        self.instruction_counter = 0
        self.running = True

    def load_program(self, program):
        for i, instruction in enumerate(program):
            self.memory[i] = instruction
        self.instruction_counter = 0
        self.running = True

    def fetch(self):
        instruction = self.memory[self.instruction_counter]
        self.instruction_counter += 1
        return instruction

    def decode_execute(self, instruction):
        operation = int(instruction[1:3])
        operand = int(instruction[3:5])
        if instruction[0] == '-':
            operation = -operation

        if operation == 10:  # READ
            pass  # READ is handled separately
        elif operation == 11:  # WRITE
            self.output(operand)
        elif operation == 20:  # LOAD
            self.accumulator = int(self.memory[operand])
        elif operation == 21:  # STORE
            self.memory[operand] = f'+{str(self.accumulator).zfill(4)}'
        elif operation == 30:  # ADD
            self.accumulator += int(self.memory[operand])
        elif operation == 31:  # SUBTRACT
            self.accumulator -= int(self.memory[operand])
        elif operation == 32:  # DIVIDE
            self.accumulator //= int(self.memory[operand])
        elif operation == 33:  # MULTIPLY
            self.accumulator *= int(self.memory[operand])
        elif operation == 40:  # BRANCH
            self.instruction_counter = operand
        elif operation == 41:  # BRANCHNEG
            if self.accumulator < 0:
                self.instruction_counter = operand
        elif operation == 42:  # BRANCHZERO
            if self.accumulator == 0:
                self.instruction_counter = operand
        elif operation == 43:  # HALT
            self.running = False

    def output(self, operand):
        print(int(self.memory[operand]))

# def get_program(filename):
#     with open(filename, 'r') as file:
#         program = [line.strip() for line in file.readlines()]
#     return program

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python UVSIM.py <program_file.txt>")
        sys.exit(1)

    program_file = sys.argv[1]
    file = FileLoader()
    file.program_name = program_file
    program = file.get_program()

    uvsim = UVSim()
    uvsim.load_program(program)
    uvsim.run()
