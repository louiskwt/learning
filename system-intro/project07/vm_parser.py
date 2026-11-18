from enum import Enum, auto
from pathlib import Path

class CommandType(Enum):
    C_ARITHMETIC = auto()
    C_PUSH = auto()
    C_POP = auto()
    C_LABEL = auto()
    C_GOTO = auto()
    C_IF = auto()
    C_FUNCTION = auto()
    C_RETURN = auto()
    C_CALL = auto()

C_POP = CommandType.C_POP
C_PUSH = CommandType.C_PUSH
C_ARITHMETIC = CommandType.C_ARITHMETIC

class Parser():
    input_lines = []
    input_index = 0
    current_command = ""
    current_cmd_type: CommandType | None = None

    def __init__(self, filename: Path | bytes) -> None:
        assert isinstance(filename, (Path, bytes)) 
        with open(filename, 'r') as f: 
            lines = f.readlines()
            for line in lines:
                if "//" not in line and line != "\n":
                    self.input_lines.append(line.strip())

    def has_more_commands(self) -> bool:
        return not self.input_index == len(self.input_lines)

    def advance(self) -> None:
        self.current_command = self.input_lines[self.input_index]
        self.current_cmd_type = self.command_type()
        self.input_index += 1

    def command_type(self) -> CommandType:
        command_parts = self.current_command.split(" ")
        if command_parts[0] in ["add", "sub", "lt", "eq", "gt", "neg", "and", "or", "not"]:
            if len(command_parts) > 1:
                raise ValueError("C_ARITHMETIC is incorrectly fromatted.")
            return CommandType.C_ARITHMETIC
        elif command_parts[0] == "push":
            return CommandType.C_PUSH
        elif command_parts[0] == "pop":
            return CommandType.C_POP
        else:
            return CommandType.C_RETURN

    def arg1(self) -> str:
        if self.current_cmd_type == CommandType.C_ARITHMETIC:
            return self.current_command
        else:
            command_parts = self.current_command.split(" ")
            return command_parts[1]

    def arg2(self) -> int:
        command_parts = self.current_command.split(" ")
        second_arg = command_parts[-1]
        if not second_arg.isnumeric():
            raise ValueError("Command is not formatted properly")
        return int(second_arg)
     