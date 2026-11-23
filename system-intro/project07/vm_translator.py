#!/usr/bin/env python
import sys
from pathlib import Path
from vm_parser import Parser, C_POP, C_PUSH, C_ARITHMETIC, C_LABEL, C_GOTO, C_IF, C_FUNCTION, C_RETURN, C_CALL
from vm_code_writer import CodeWriter, TARGET_EXT

def translate_vm_code(parser: Parser, writer: CodeWriter, filename: str):
        writer.set_file_name(filename)
        
        while parser.has_more_commands(filename):
            parser.advance(filename)

            if parser.current_cmd_type in [C_POP, C_PUSH]:
                writer.write_push_pop(parser.current_cmd_type, parser.arg1(), parser.arg2())

            if parser.current_cmd_type == C_ARITHMETIC:
                writer.write_arithmetic(parser.arg1())

            if parser.current_cmd_type == C_LABEL:
                writer.write_label(parser.arg1())

            if parser.current_cmd_type == C_GOTO:
                writer.write_goto(parser.arg1())

            if parser.current_cmd_type == C_IF:
                writer.write_if_goto(parser.arg1())

            if parser.current_cmd_type == C_FUNCTION:
                writer.write_function(parser.arg1(), parser.arg2())

            if parser.current_cmd_type == C_CALL:
                writer.write_call(parser.arg1(), parser.arg2())

            if parser.current_cmd_type == C_RETURN:
                writer.write_return()


if len(sys.argv) != 2:
    print("Usage: vm_translator.py <file_name | file_dir>")
    sys.exit(1)


if __name__ == "__main__":
    arg = sys.argv[1]
    target = Path(arg)

    if target.exists():
        is_folder = target.is_dir()
        file_stem = target.stem if is_folder else target.parent.stem
        output_file = f"{file_stem}{TARGET_EXT}"
        output_path = target / output_file if is_folder else target.parent / output_file
        
        if is_folder:
            vm_file_list = [f.name for f in target.glob("*.vm") if f.is_file()]
            sys_vm_file = "Sys.vm"
            parser = Parser(None)
            has_multiple_file = len(vm_file_list) > 1

            if sys_vm_file in vm_file_list:
                entry_file = target / sys_vm_file
                vm_file_list.remove(sys_vm_file)
                parser.load_file(entry_file)

            for file_name in vm_file_list:
                file_path = target / file_name
                parser.load_file(file_path)

            writer = CodeWriter(output_path)
            if has_multiple_file:
                writer.write_bootstrap_code()
            for file in parser.input_files.keys():
                translate_vm_code(parser, writer, file)
                parser.rest()

            writer.close()
        elif ".vm" in target.name:
            parser = Parser(target)
            writer = CodeWriter(output_path)
            translate_vm_code(parser, writer, target.stem)
            writer.close()
        else:
            raise ValueError("Target file must have .vm extenstion")
        
        print(f"Translation completed >> See {output_path}")
    else:
        raise FileNotFoundError(f"{target} does not exist. Please check your target file or directory.")
