# -*- coding: utf-8 -*-
"""
Created on Wed May 22 17:37:33 2024

@author: Jakob, Jarek, Ben, Michael
"""

import sys
# import os
from FileLoader import FileLoader

# Name of unittest file
# TESTFILE = "UVSim Testing.py"

class UVSim:
    def __init__(self):
        self.memory = [0] * 100
        self.accumulator = 0
        self.instruction_counter = 0
        self.running = True

    def load_program(self, program):
        """ Load the program into memory starting at location 0 """
        for i, instruction in enumerate(program):
            self.memory[i] = instruction

    def fetch(self):
        """ Fetch the next instruction """
        instruction = self.memory[self.instruction_counter]
        self.instruction_counter += 1 
        return instruction

    def decode_execute(self, instruction):
        """ Decode and execute the instruction """
        opcode = instruction[1:3]
        operand = int(instruction[3:5])

        if opcode == '10':  # READ
            self.read_input(operand)

        elif opcode == '11':  # WRITE
            self.write_output(operand)

        elif opcode == '20':  # LOAD
            self.accumulator = int(self.memory[operand])

        elif opcode == '21':  # STORE
            self.memory[operand] = str(self.accumulator).zfill(4)

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
        """ Run the simulations """
        while self.running:
            instruction = self.fetch()
            self.decode_execute(instruction)

    def read_input(self, operand):
        """ Reads the input from user """
        value = input("Enter an integer: ")
        try:
            value = int(value)
        except ValueError:
            raise ValueError("Input must be an integer.")
        
        if value < 0:
            self.memory[operand] = str(value).zfill(5)
        else:
            self.memory[operand] = '+' + str(value).zfill(4)

    def write_output(self, operand):
        """ Write output to console """
        print(int(self.memory[operand]))

# def get_program(program_file):
#     """ Read program from file """
#     if sys.argv[0] == TESTFILE:
#         return ['+4300']  #termination for unittest
#     else:
#         if not os.path.exists(program_file):
#             raise FileNotFoundError(f"The file {program_file} does not exist.")
        
#         program_lines = []
#         with open(program_file, "r") as file:
#             for line in file:
#                 program_lines.append(line.strip())
#         return program_lines

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python UVSIM.py <program_file.txt>")
        sys.exit(1)

    program_file = sys.argv[1]
    file = FileLoader(program_file)
    program = file.get_program()

    uvsim = UVSim()
    uvsim.load_program(program)
    uvsim.run()

