Overview: 
The UVSim is a simple virtual machine desgined to execture programs written in BasicML machine language. This README file will provide the reader with all the instructions needed to use the UVSim from the command line. 

 

Prerequisites: 
Before running the UVSim, make sure that you have Python Installed on your system. The UVSim that we created was created using Python Version 3.8.10 

 

Installation: 
1. Clone the UVSim repository from GitHub 
2. Open your computer's command line interface
3. Type in the following: git clone https://github.com/JHodgson21/CS-2450-Group-Project.git 
4. This link is important because here you will be able to obtain the UVSim codebase from our GitHub. By cloning the repository you’ll be able to access the source code and run the program on your own computer.  
5. Navigate to the project directory if needed (cd CS-2450-Group-Project) 

 

Usage: 
To run the UVSim follow these steps: 
1. Open a “Command Prompt” on Windows or a “Terminal” on macOS/Linux. 
2. Once the command prompt is open, go to the directory where you saved the UVSim repository using the ‘cd’ command.  
Example:  
cd  \Users\Jakob\Desktop\2024 Software Engineering Project\CS-2450-Group-Project 

3. Make a txt file for commands to be used in the UVSIM. If you are on Windows search for notepad. If you are on macOS you will be using TextEdit, or you can use any other text editor you like.  
4. Writing to your program (to the UVSIM): In the text editor write your program using the commands supported by the UVSIM. Each command should be written on a separate line.  
5. Save the file in the same location where the UVSIM is saved. (also make sure its a .txt file).  

Example of a .txt file 

+010007
+010008
+020007
+030008
+021009
+011009 
+043000 


This txt file explained
‘+010007’: This is a READ operation. It prompts the user to input an integer and stores it in memory to location 07 
‘+010008’: This is a READ operation. It prompts the user to input an integer and stores it in memory to location 08 
‘+020007’: This is a LOAD operation. It loads the value stored in memory location 07 into the accumulator 
‘+030008’: This instruction is an ADD operation. It adds the value stored in memory location 08 to the value currently in the accumulator 
‘+021009’: This instruction is a STORE operation. It stores the value currently in the accumulator into memory location 09. 
‘+011009’: This instruction is a WRITE operation. It will write or output the value stored in memory location 09. 
‘+043000’: This instruction is a HALT operation. It will halt the program, indicating to the computer that the program has finished running.  


Run the UVSim application using Python, providing the name of the python file (UVSimGUI.py), example below. 
python UVSimGUI.py

After inputting the line above the GUI will pop up on your screen. 
Follow the instructions below to use the GUI

Loading the program:
1. Click the "Load Program" button.
2. A file dialog will appear. Navigate to your '.txt' file that contains the program instructions and select it.
3. The program will be loaded, and you will see a confirmation message appear in the output text area.
4. On the second half of the screen you will also see the contents or 'instructions' in your .txt file. 

Editing the program:
1. You can edit the program instructions directly within the GUI on the lower half of the screen.
2. You can add, modify, delete, cut, copy, and paste within the GUI. 
3. After you've finished editing you can either hit 'Run' or 'Save Program'.

Saving Edited Programs:
1. After editing, you can click "Save Program" to save it as a new file. 
2. Choose a directory and enter a filename to save the edited program as a '.txt' file.

Running the program:
1. After loading the program, click the "Run" button.
2. If the program requires any input, a prompt will appear in the GUI for you to enter the required values.
3. The output of the program, including any WRITE operations and the final accumulator value, will be displayed in the output text area. 

Resetting the program:
1. Click the "Reset" button to clear the current program and reset the UVSim instance.
2. This will clear the output text area and reset the internal state of the UVSim.

Configuring the Color Scheme:
1. The color sceheme is set to a default UVU Green.
2. To change the color scheme hit the button 'Change Color Scheme'.
3. The GUI will show some default colors as well as allowing the user to choose any color they'd like.
4. The first color you pick will be for the outline of the GUI and the second color will be for the button color as well as the background color. 
5. Once you find the first color you like select the color or type in the RGB values of it on the right hand side of the screen and click 'ok'.
    - If you'd like to save that specific color hit 'Add To Custom Colors'.
6. After clicking 'ok' you'll choose your second color by selecting it or manually typing in the RGB values of it on the right hand side of the screen. Then once you're finished click 'ok'.
7. The color you chose will carry over throughout your sessions!

Quitting the application:
1. Click the "Quit" button to close the UVSim GUI.

How the BasicML vocabulary works within the UVSim.  

BasicML vocabulary defined as follows: 

I/O operation: 
READ = 10 Read a word from the keyboard into a specific location in memory. 
WRITE = 11 Write a word from a specific location in memory to screen. 

Load/store operations: 
LOAD = 20 Load a word from a specific location in memory into the accumulator. 
STORE = 21 Store a word from the accumulator into a specific location in memory. 

Arithmetic operation: 
ADD = 30 Add a word from a specific location in memory to the word in the accumulator (leave the result in the accumulator) 
SUBTRACT = 31 Subtract a word from a specific location in memory from the word in the accumulator (leave the result in the accumulator) 
DIVIDE = 32 Divide the word in the accumulator by a word from a specific location in memory (leave the result in the accumulator). 
MULTIPLY = 33 multiply a word from a specific location in memory to the word in the accumulator (leave the result in the accumulator). 

Control operation: 
BRANCH = 40 Branch to a specific location in memory 
BRANCHNEG = 41 Branch to a specific location in memory if the accumulator is negative. 
BRANCHZERO = 42 Branch to a specific location in memory if the accumulator is zero. 
HALT = 43 Stop the program 

New Features:

UVSim Supports 250 Lines and Three-Digit Memory Addresses:
The UVSim supports data files containing up to 250 lines, with internal memory registers going from 000 to 249.
Commands trying to reference a number outside the range of 000-249 will result in an error.

Handling Six-Digit Math Operations:
The UVSim can handle six-digit math operations with proper overflow handling.

Supporting Old and New File Formats:
The UVSim supports both old (four-digit) and new (six-digit) file formats.

Conversion From Four-Digit to Six-Digit Format:
THe UVSim includes a new conversion feature to convert four-digit files to six-digit form.

Multiple Files Open Simultaneously:
The UVSim GUI now allows multiple files to be opened, edited, and saved within the application.
Only one file can be executed at a time.

Other txt files (ideas) 

Subtracting two numbers: 

+010007
+010008 
+020007 
+031008 
+021009 
+011009 
+043000 

 
Multiplying two numbers: 

+010007  
+010008 
+020007 
+033008 
+021009 
+011009 
+043000 

Other Files That Are Needed to Run the Software:

Configuration File (config.txt)
The config.txt file is used to store the default color scheme for the UVSIM. It contains two lines, the first is the primary color and the second line is for the off color. 
The default colors are set to be UVU's colors which is a darkish green and white. 
You don't need to mess with this config.txt file. If you'd like to change the color you can do it through the GUI. ( SEE Configuring The Color Scheme ABOVE ).

FL.py
The FL.py file contains the 'FileLoader' class which is responsible for loading programs from text files into the UVSIM.
