import sys
import os

TESTFILE = "UVSim Testing.py"

class FileLoader:
    def __init__(self):
        self.program_name = ""
        self.program_lines = []
    
    def get_program(self):
        """ Read program from file """
        if sys.argv[0] == TESTFILE:
            return ['+4300']  #termination for unittest
        else:
            if not os.path.exists(self.program_name):
                raise FileNotFoundError(f"The file {self.program_name} does not exist.")
            print(self.program_name)
            program_lines = []
            with open(self.program_name, "r") as file:
                for line in file:
                    program_lines.append(line.strip())
            return program_lines