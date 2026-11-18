#!/usr/bin/env python
import sys
from pathlib import Path
from vm_parser import Parser, C_POP, C_PUSH, C_ARITHMETIC
from vm_code_writer import CodeWriter, TARGET_EXT

if len(sys.argv) != 2:
    print("Usage: vm_translator.py <file_name>")
    sys.exit(1)


if __name__ == "__main__":
    arg = sys.argv[1]
    target = Path(arg)

    if target.exists():
        output_file = f"{target.stem}{TARGET_EXT}"
        parser = Parser(target)
        writer = CodeWriter(output_file)
        while parser.has_more_commands():
            parser.advance()

            if parser.current_cmd_type in [C_POP, C_PUSH]:
                writer.write_push_pop(parser.current_cmd_type, parser.arg1(), parser.arg2())

            if parser.current_cmd_type == C_ARITHMETIC:
                writer.write_arithmetic(parser.arg1())

        writer.close()
        print(f"Translation completed >> See {output_file}")