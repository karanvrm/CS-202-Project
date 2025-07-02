import os
import re
import google.generativeai as genai
from pycparser import parse_file, c_ast
from pycparser.c_generator import CGenerator

# Step 1: Setup Gemini
genai.configure(api_key=os.environ["GEMINI_API_KEY"])  # Ensure you set your API key in the environment
model = genai.GenerativeModel("gemini-2.0-flash")

# Step 2: Function Extractor
class FunctionExtractor(c_ast.NodeVisitor):
    def __init__(self):
        self.generator = CGenerator()
        self.functions = []

    def visit_FuncDef(self, node):
        func_code = self.generator.visit(node)
        self.functions.append(func_code)

def extract_functions_from_c_file(filename):
    import pycparser
    fake_libc = os.path.join(os.path.dirname(pycparser.__file__), 'utils', 'fake_libc_include')
    ast = parse_file(filename, use_cpp=True, cpp_path='gcc', cpp_args=['-E', f'-I{fake_libc}'])
    extractor = FunctionExtractor()
    extractor.visit(ast)
    return extractor.functions

def gemini(prompt):
    try:
        response = model.generate_content(prompt)
        return response.text
    except Exception as e:
        return f"[Error during translation]: {str(e)}"

def preprocess_c_code(c_code):
    #removing "//" and "/*...*/"
    c_code = re.sub(r'//.*$', '', c_code, flags=re.MULTILINE)
    c_code = re.sub(r'/\*.*?\*/', '', c_code, flags=re.DOTALL)
    #removing #include 
    c_code = re.sub(r'#include\s*<.*?>', '', c_code)


def save_to_file(content, filename="output.pml"):
    try:
        with open(filename, "w") as file:
            file.write(content)
        print(f"Output successfully saved to {filename}")
    except Exception as e:
        print(f"Error while saving the output: {str(e)}")

if __name__ == "__main__":
    file_path = "input.c"  # Replace with your C source file path

    with open(file_path, "r") as file:
        c_code = file.read()

    prompt = (
        "If the following code is recursive, convert it into an iterative version. "
        "Only provide the iterative code without any explanation, context, or additional code. "
        "Remove all comments and #include statements. Replace any pseudo commands like min, max, etc., with their basic implementations.\n"
        f"Code: {c_code}\n"
    )

    c_code_iterative= gemini(prompt)
    c_code_iterative= c_code_iterative[4:len(c_code_iterative)-3]
    with open("simpleCode.c", "w") as file:
        file.write(c_code_iterative)

    functions = extract_functions_from_c_file("simpleCode.c")

    # Store the complete output in the file
    context = ""
    for i, func in enumerate(functions):
        context+= f"\n----- Function {i+1} (C) -----\n"
        prompt = f"Find the context of this function:\n{func}\n And Give Context Straight and Short.\n"
        context+= gemini(prompt)
        context= context.strip()


    #Full C code
    with open("input.c", "r") as file:
        c_code = file.read()
    
    #examples for conversion
    with open("DataBase_Examples.txt", "r") as file:
        Examples = file.read()

    #Syntax for conversion
    with open("DataBase_Syntax.txt", "r") as file:
        Syntax = file.read()
    
    #limitations of promela
    with open("DataBase_Limitations.txt", "r") as file:
        Limitations = file.read()


    #prompt for conversion

    prompt = (
    f"Convert the following C function to Promela, respecting Promela’s feature limitations and only use inline i.e. don't use prototype.\n"
    f"This the full C code That is To be converted:\n"
    f"```c\n"
    f"{c_code}\n"
    f"```"
    f"Don't Provide any explanation. Just return the Promela code.Don't include Provided snippets in Response.\n"
    f"Here is Extra information to help you with the conversion:\n"
    f"{Limitations}"
    f"keep in Mind these limitations while converting.\n"
    f"{Syntax}"
    f"Use this syntax for conversion.\n"
    # f"{Examples}"
    # f"Here are some examples of C code and their Promela equivalents:\n"
    f"Context of the functions(numbered):\n"
    f"{context}\n"
    f"If Code is Recursive then convert into iterative Promela version.\n"
    )
    # #prompt for conversion
    print("Prompt for conversion:")
    print(prompt)
    complete_output =gemini(prompt)
    complete_output= complete_output.strip()
    complete_output= complete_output[10:len(complete_output)-3]
    # Save the complete output to a file
    save_to_file(complete_output, "output.pml")
