#!/usr/bin/env python
import sys
from hack_parser import Parser, C_COMMAND, A_COMMAND
from hack_code import Code

if len(sys.argv) != 2:
    print("Usage: hack_assembler.py <file_name>")
    sys.exit(1)

filename = sys.argv[1]
parser = Parser(filename)

def pre_load_symbol_table():
    while parser.has_more_commands():
        parser.advance()
        parser.load_symbol_table()
    parser.reset()

def assemble() -> None:
    code_generator = Code()
    output_list = []

    while parser.has_more_commands():
        parser.advance()
        parser.current_cmd_type = parser.command_type()
        output = ""

        if parser.current_cmd_type == C_COMMAND:
            dest_mnemonic, comp_mnemonic, jmp_mnemonic = parser.dest(), parser.comp(), parser.jump()
            output += f"{7:03b}" + code_generator.comp(comp_mnemonic) + code_generator.dest(dest_mnemonic) + code_generator.jmp(jmp_mnemonic)

        if parser.current_cmd_type == A_COMMAND:
            output += parser.symbol()

        if parser.current_cmd_type in (C_COMMAND, A_COMMAND):
            output_list.append(output)

    file_tag = filename.split(".")[0]
    target_ext = "hack"

    with open(f"{file_tag}.{target_ext}", "w", encoding="utf-8") as f:
        for i, line in enumerate(output_list):
            if i == len(output_list) - 1:
                f.write(line)
            else:
                f.write(f"{line}\n")

if __name__ == "__main__":
    pre_load_symbol_table()
    assemble()
    print(f"Completed! See {filename.split('.')[0]}.hack")





