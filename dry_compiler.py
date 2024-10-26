# this is the current src code

import sys
import os

mainFile = "T.cpp"

# Initial C++ setup, so we can append lines without repeating headers each time
with open(mainFile, "w") as f:
    f.write("#include <iostream>\n")
    f.write("using namespace std;\n")
    f.write("int main(){\n")

# Function to handle parsing each line
def parse(line: str):
    with open(mainFile, "a") as f:
        if "->" in line:
            # Parsing variable declaration
            parts = line.split("->")
            nameVal = parts[0].split()
            data_type = nameVal[0]
            
            # Map Dry++ types to C++ types
            if data_type == "num":
                data_type = "int"
            elif data_type == "str":
                data_type = "string"
                
            f.write(f"\t{data_type} {nameVal[1]} = {parts[1].strip()};\n")

        elif line.startswith("\tout("):
            # Parsing output
            val = line[5:-2]  # Strip out the "out(" and ");"
            if "<<" in val:
                val = val.replace("+", "<<")  # Replace concatenation syntax
            f.write(f"\tcout << {val} << endl;\n")
        
        elif "in(" in line:
            # Parsing input
            var_name = line[3:-2].strip()  # Strip "in(" and ");"
            f.write(f"\tcin >> {var_name};\n")

# Reads each character from the input file to find complete lines
def readFileContents():
    line = ""
    with open(sys.argv[1], 'r') as file:
        for char in file.read():
            if char == ";":
                line += ";"
                parse(line.strip())  # Clean whitespace before parsing
                line = ""
            else:
                line += char

    # Finalize main function in the C++ file
    with open(mainFile, "a") as f:
        f.write("\n}\n")

if len(sys.argv) < 2:
    print("Usage:\n\tspecify a file to parse!")
else:
    try:
        readFileContents()
    except FileNotFoundError:
        print(f"Could not open file {sys.argv[1]}.")

# Compile and execute
os.system("g++ T.cpp -o dry.exe && cmd /c dry.exe")
