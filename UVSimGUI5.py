# -*- coding: utf-8 -*-
"""
Created on Thu Jun 20 11:22:37 2024

@author: Jakob, Jarek, Ben, Michael
"""

import tkinter as tk
from tkinter import filedialog, messagebox, simpledialog, colorchooser
from tkinter.scrolledtext import ScrolledText
from tkinter import ttk
import os
from FL import FileLoader
from UVSIM import UVSim
from IH import InputHandler

CONFIG_FILE = "config.txt"

class UVSimGUI:
    def __init__(self, master):
        self.master = master
        self.master.title("UVSim GUI")
        self.uvsim = UVSim()
        
        self.programs = {}
        self.current_program = None
        self.program_frames = {}

        self.primary_color, self.off_color = self.load_color_scheme()

        self.create_widgets()

        self.clear_log()

    def load_color_scheme(self):
        if os.path.exists(CONFIG_FILE):
            with open(CONFIG_FILE, 'r') as file:
                lines = file.readlines()
                primary_color = lines[0].split('=')[1].strip()
                off_color = lines[1].split('=')[1].strip()
        else:
            primary_color = '#4C721D'
            off_color = '#FFFFFF'
        return primary_color, off_color

    def save_color_scheme(self):
        with open(CONFIG_FILE, 'w') as file:
            file.write(f"primary_color = {self.primary_color}\n")
            file.write(f"off_color = {self.off_color}\n")

    def create_widgets(self):
        self.master.configure(bg=self.primary_color)
        
        self.output_text = ScrolledText(self.master, width=60, height=10, bg=self.off_color)
        self.output_text.grid(row=0, column=0, columnspan=3, padx=10, pady=10)

        self.notebook = ttk.Notebook(self.master)
        self.notebook.grid(row=1, column=0, columnspan=3, padx=10, pady=10)
        self.notebook.bind("<<NotebookTabChanged>>", self.on_tab_change)

        self.program_frames = {}

        self.load_button = tk.Button(self.master, text="Load Program", command=self.load_program, bg=self.off_color)
        self.load_button.grid(row=2, column=0, padx=10, pady=5)

        self.run_button = tk.Button(self.master, text="Run", command=self.run_program, bg=self.off_color)
        self.run_button.grid(row=2, column=1, padx=10, pady=5)

        self.reset_button = tk.Button(self.master, text="Reset", command=self.reset_program, bg=self.off_color)
        self.reset_button.grid(row=2, column=2, padx=10, pady=5)

        self.save_button = tk.Button(self.master, text="Save Program", command=self.save_program, bg=self.off_color)
        self.save_button.grid(row=3, column=0, padx=10, pady=5)

        self.color_button = tk.Button(self.master, text="Change Color Scheme", command=self.change_color_scheme, bg=self.off_color)
        self.color_button.grid(row=3, column=1, padx=10, pady=5)

        self.quit_button = tk.Button(self.master, text="Quit", command=self.master.quit, bg=self.off_color)
        self.quit_button.grid(row=3, column=2, padx=10, pady=5)

        self.menu = tk.Menu(self.master)
        self.master.config(menu=self.menu)
        self.edit_menu = tk.Menu(self.menu, tearoff=0)
        self.menu.add_cascade(label="Edit", menu=self.edit_menu)
        self.edit_menu.add_command(label="Cut", command=lambda: self.get_current_text_widget().event_generate("<<Cut>>"))
        self.edit_menu.add_command(label="Copy", command=lambda: self.get_current_text_widget().event_generate("<<Copy>>"))
        self.edit_menu.add_command(label="Paste", command=lambda: self.get_current_text_widget().event_generate("<<Paste>>"))
        self.edit_menu.add_command(label="Add Line", command=self.add_line)
        self.edit_menu.add_command(label="Delete Line", command=self.delete_line)

    def on_tab_change(self, event):
        selected_tab = event.widget.select()
        tab_index = event.widget.index(selected_tab)
        self.current_program = tab_index

    def get_current_text_widget(self):
        return self.program_frames[self.current_program]['text_widget']

    def load_program(self):
        try:
            program_file = filedialog.askopenfilename(filetypes=[("Text files", "*.txt")])
            if program_file:
                with open(program_file, 'r') as file:
                    program = file.readlines()
                if len(program) > 250:
                    raise Exception("Programs must be no more than 250 lines long.")
                program = [line.strip() for line in program]
                tab_index = len(self.program_frames)

                frame = ttk.Frame(self.notebook)
                text_widget = ScrolledText(frame, width=60, height=10, bg=self.off_color)
                text_widget.pack(expand=True, fill='both')
                for line in program:
                    text_widget.insert(tk.END, line + '\n')

                self.notebook.add(frame, text=os.path.basename(program_file))
                self.program_frames[tab_index] = {'frame': frame, 'text_widget': text_widget, 'file_path': program_file}
                self.programs[tab_index] = program
                self.current_program = tab_index
                self.write_to_log(f"Program loaded successfully: {program_file}")
        except Exception as e:
            messagebox.showerror("Error", f"Error loading program: {str(e)}")

    def save_program(self):
        try:
            if self.current_program is not None:
                program_file = filedialog.asksaveasfilename(defaultextension=".txt", filetypes=[("Text files", "*.txt")])
                if program_file:
                    text_widget = self.get_current_text_widget()
                    program = text_widget.get(1.0, tk.END).strip().split('\n')
                    if len(program) > 250:
                        messagebox.showerror("Error", "Program exceeds the maximum of 250 instructions.")
                        return
                    with open(program_file, 'w') as file:
                        for line in program:
                            file.write(line + '\n')
                    self.programs[self.current_program] = program
                    self.program_frames[self.current_program]['file_path'] = program_file
                    self.notebook.tab(self.current_program, text=os.path.basename(program_file))
                    self.write_to_log(f"Program saved successfully: {program_file}")
        except Exception as e:
            messagebox.showerror("Error", f"Error saving program: {str(e)}")

    def run_program(self):
        try:
            if self.current_program is not None:
                text_widget = self.get_current_text_widget()
                program = text_widget.get(1.0, tk.END).strip().split('\n')
                if len(program) > 250:
                    messagebox.showerror("Error", "Program exceeds the maximum of 250 instructions.")
                    return
                self.uvsim.load_program(program)
                self.write_to_log("Starting program execution...")

                while self.uvsim.running:
                    instruction = self.uvsim.fetch()
                    operand = instruction[1]
                    length = instruction[2]
                    if instruction[0] == 10:
<<<<<<< Updated upstream
                        self.handle_read(instruction[1])
=======
                        self.handle_read(operand, length)
>>>>>>> Stashed changes
                    elif instruction[0] == 11:
                        self.handle_write(operand)
                    else:
                        self.uvsim.decode_execute(instruction)

                self.write_to_log(f"Accumulator = {self.uvsim.accumulator}")
                self.write_to_log("Program execution completed.")
        except Exception as e:
            messagebox.showerror("Error", f"Error running program: {str(e)}")

<<<<<<< Updated upstream
    def handle_read(self, val):
        operand = int(val)
        value = simpledialog.askinteger("Input", "Enter an integer:")
        if value is not None:
            if value < -9999 or value > 9999:
                messagebox.showerror("Error", "Input must be between -9999 and 9999.")
            else:
                self.uvsim.memory[operand] = f'+{str(value).zfill(4)}'
                self.write_to_log(f"Input added: {value}")
=======
    def handle_read(self, val, length):
        operand = int(val)
        value = simpledialog.askinteger("Input", "Enter an integer:")
        if value is not None:
            InputHandler(value, length).validate()
            if length == 4:
                self.uvsim.memory[operand] = f'+{str(value).zfill(4)}'
                self.write_to_log(f"Input added: {value}")
            elif length == 6:
                self.uvsim.memory[operand] = f'+{str(value).zfill(6)}'
                self.write_to_log(f"Input added: {value}")
>>>>>>> Stashed changes
        else:
            messagebox.showwarning("Warning", "No input provided.")

    def handle_write(self, instruction):
        operand = instruction
        value = self.uvsim.memory[operand]
        self.write_to_output(value)

    def reset_program(self):
        self.uvsim = UVSim()
        self.programs = {}
        self.current_program = None
        self.output_text.delete(1.0, tk.END)
        for frame in self.program_frames.values():
            frame['text_widget'].delete(1.0, tk.END)
        self.write_to_output("Program reset.")

    def change_color_scheme(self):
        primary_color = colorchooser.askcolor(title="Choose Primary Color")[1]
        off_color = colorchooser.askcolor(title="Choose Off Color")[1]
        if primary_color and off_color:
            self.primary_color = primary_color
            self.off_color = off_color
            self.save_color_scheme()
            self.apply_color_scheme()

    def apply_color_scheme(self):
        self.master.configure(bg=self.primary_color)
        self.output_text.configure(bg=self.off_color)
        for frame in self.program_frames.values():
            frame['text_widget'].configure(bg=self.off_color)
        self.load_button.configure(bg=self.off_color)
        self.run_button.configure(bg=self.off_color)
        self.reset_button.configure(bg=self.off_color)
        self.save_button.configure(bg=self.off_color)
        self.color_button.configure(bg=self.off_color)
        self.quit_button.configure(bg=self.off_color)

    def write_to_log(self, message):
        self.output_text.insert(tk.END, message + "\n")
        self.output_text.yview(tk.END)

    def write_to_output(self, message):
        self.output_text.insert(tk.END, message + "\n")
        self.output_text.yview(tk.END)

    def clear_log(self):
        self.output_text.delete(1.0, tk.END)

    def add_line(self):
        line = simpledialog.askstring("Input", "Enter the line to add:")
        if line is not None:
            self.get_current_text_widget().insert(tk.END, line + '\n')

    def delete_line(self):
        index = simpledialog.askinteger("Input", "Enter the line number to delete (1-based):")
        if index is not None:
            text_widget = self.get_current_text_widget()
            lines = text_widget.get(1.0, tk.END).strip().split('\n')
            if 1 <= index <= len(lines):
                del lines[index - 1]
                text_widget.delete(1.0, tk.END)
                for line in lines:
                    text_widget.insert(tk.END, line + '\n')

if __name__ == "__main__":
    root = tk.Tk()
    app = UVSimGUI(root)
    root.mainloop()

