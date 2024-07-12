# -*- coding: utf-8 -*-
"""
Created on Thu Jun 20 11:22:37 2024

@author: Jakob, Jarek, Ben, Michael
"""

import tkinter as tk
from tkinter import filedialog, messagebox, simpledialog
from tkinter.scrolledtext import ScrolledText
from FL import FileLoader

# need to import the UVSim class from UVSIM.py
from UVSIM import UVSim

class UVSimGUI:
    def __init__(self, master):
        self.master = master
        self.master.title("UVSim GUI")
        self.uvsim = UVSim()  # for creating an instance of UVSim
        self.program = []     # variable to hold the loaded program. 
        self.create_widgets()
        self.program_loaded = False
        self.file = FileLoader() # For loading files

    def create_widgets(self):
        # area to display output. we can make this bigger if we want. 
        self.output_text = ScrolledText(self.master, width=30, height=20)
        self.output_text.grid(row=0, column=0, columnspan=3, padx=10, pady=10)

        # area to display program readout. will likely want to make this the main display when finished.
        self.readout_text = ScrolledText(self.master, width=30, height=20)
        self.readout_text.grid(row=0, column=4, padx=10, pady=10)
        self.write_to_readout("Program output:")

        # Button that will let you search for a file. 
        self.load_button = tk.Button(self.master, text="Load Program", command=self.load_program)
        self.load_button.grid(row=1, column=0, padx=10, pady=5)

        # After loading in your file you need to 'run' it by hitting this button. 
        self.run_button = tk.Button(self.master, text="Run", command=self.run_program)
        self.run_button.grid(row=1, column=1, padx=10, pady=5)

        # Button to reset the GUI
        self.reset_button = tk.Button(self.master, text="Reset", command=self.reset_program)
        self.reset_button.grid(row=1, column=2, padx=10, pady=5)

        # Button to Quits the GUI
        self.quit_button = tk.Button(self.master, text="Quit", command=self.master.quit)
        self.quit_button.grid(row=2, column=1, padx=10, pady=5)

    def load_program(self):
        """ Load Program button callback function """
        try:
            program_file = filedialog.askopenfilename(filetypes=[("Text files", "*.txt")])
            if program_file:
                self.file.program_name = program_file
                self.program = self.file.get_program()
                self.uvsim.load_program(self.program)
                self.output_text.insert(tk.END, f"Program loaded successfully: {program_file}\n")
                self.program_loaded = True
        except Exception as e:
            messagebox.showerror("Error", f"Error loading program: {str(e)}")

    def run_program(self):
        """ Run button callback function """
        if(not self.program_loaded):
            messagebox.showerror("Error", "No program loaded.")
            return
        try:
            while self.uvsim.running:
                instruction = self.uvsim.fetch()
                if instruction[1:3] == '10':  # Handle READ opcode
                    self.handle_read(instruction)
                elif instruction[1:3] == '11': # Handle WRITE opcode
                    self.handle_write(instruction)
                else:
                    self.uvsim.decode_execute(instruction)

            self.output_text.insert(tk.END, f"Accumulator = {self.uvsim.accumulator}\n")
            self.output_text.insert(tk.END, "Program execution completed.\n")

        except Exception as e:
            messagebox.showerror("Error", f"Error running program: {str(e)}")

    def handle_read(self, instruction):
        """ Handle READ opcode """
        operand = int(instruction[3:5])  # gets the operand from instruction
        value = simpledialog.askinteger("Input", "Enter an integer:")
        if value is not None:
            if value < -9999 or value > 9999:
                messagebox.showerror("Error", "Input must be between -9999 and 9999.")
            elif value < 0:
                self.uvsim.memory[operand] = str(-abs(int(value))).zfill(4)
            else:
                self.uvsim.memory[operand] = f'+{str(value).zfill(4)}'
                self.output_text.insert(tk.END, f"Input added: {value}\n")
        else:
            messagebox.showwarning("Warning", "No input provided.")

    def handle_write(self, instruction):
        """ Handle WRITE opcode """
        operand = int(instruction[3:5]) # gets the operand from instruction
        self.write_to_readout(self.uvsim.memory[operand])

    def reset_program(self):
        """ Reset button callback function """
        self.uvsim = UVSim()  # reset the UVSim instance
        self.program = []     # reset the loaded program
        self.output_text.delete(1.0, tk.END)  # clears all the output text. 
        self.readout_text.delete(1.0, tk.END) # clears all the readout text.
        self.program_loaded = False # resets the flag
        self.output_text.insert(tk.END, "Program reset.\n")
        self.write_to_readout("Program output:")
    
    def write_to_readout(self, str):
        """ Writes a string to the readout display """
        self.readout_text.insert(tk.END, str + '\n')

if __name__ == "__main__":
    root = tk.Tk()
    app = UVSimGUI(root)
    root.mainloop()
