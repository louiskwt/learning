
import re
from symbol_table import SymbolTable
from enum import Enum, auto

class CommandType(Enum):
    A_COMMAND = auto()
    C_COMMAND = auto()
    L_COMMAND = auto()

A_COMMAND, C_COMMAND, L_COMMAND = CommandType.A_COMMAND, CommandType.C_COMMAND, CommandType.L_COMMAND

class Parser():
    input_lines = []
    input_index = 0
    current_line = 0
    current_command = ""
    current_cmd_type: CommandType | None = None
    symbol_table_loaded = False
    symbol_table = SymbolTable()

    def __init__(self, filename: str | bytes) -> None:
        assert isinstance(filename, (str, bytes)) 
        with open(filename, 'r') as f: 
            lines = f.readlines()
            for line in lines:
                if "//" not in line and line != "\n":
                    self.input_lines.append(line.strip())

    def has_more_commands(self) -> bool:
        return not self.input_index == len(self.input_lines)

    def advance(self) -> None:
        self.current_command = self.input_lines[self.input_index]
        self.input_index += 1

    def reset(self) -> None:
        self.current_line = 0
        self.input_index = 0
        self.symbol_table_loaded = True

    def command_type(self) -> CommandType | None:
        if self.current_command[0] == "@":
            return A_COMMAND
        if "=" in self.current_command or ";" in self.current_command:
            return C_COMMAND
        if self.current_command[0] == "(" and self.current_command[len(self.current_command) - 1] == ")":
            return L_COMMAND

    def load_symbol_table(self) -> None:
        if self.command_type() == L_COMMAND:
           label = re.findall(r'\((.*?)\)', self.current_command)[0] 
           self.symbol_table.add_entry(label, self.current_line)
        else:
            self.current_line += 1

    def symbol(self) -> str:
        symbol_key = self.current_command[1:]
        if self.symbol_table.contains(symbol_key):
            address = self.symbol_table.get_address(symbol_key)
        elif symbol_key.isnumeric():
            address = int(symbol_key)
        else:
            self.symbol_table.add_entry(symbol_key, self.symbol_table.next_address, True)
            address = self.symbol_table.get_address(symbol_key)
        formatted_symbol = f"{address:016b}" 
        return formatted_symbol

    def dest(self) -> str:
        dest_str = self.current_command.split("=")[0]
        if not dest_str:
            raise ValueError("Unknown DEST; Check command string.")
        return dest_str

    def comp(self) -> str:
        pattern = r'^(?:[AMD]+=)?([^;]+)'
        comp_str = ""
        command_groups = re.search(pattern, self.current_command)
        print(command_groups)
        if command_groups:
            comp_str = command_groups.group(1)
            print(comp_str)
        if not comp_str:
            raise ValueError("Unknown COMP; Check command string.")
        return comp_str

    def jump(self) -> str:
        if ";" in self.current_command:
            return self.current_command.split(";")[1]
        return ''
 