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
C_LABEL = CommandType.C_LABEL
C_IF = CommandType.C_IF
C_GOTO = CommandType.C_GOTO
C_FUNCTION = CommandType.C_FUNCTION
C_RETURN = CommandType.C_RETURN
C_CALL = CommandType.C_CALL

class Parser():
    input_index = 0
    input_files = {}
    current_command = ""
    current_cmd_type: CommandType | None = None

    def __init__(self, file: Path | None) -> None:
        if file:
            self.load_file(file)

    def load_file(self, file: Path) -> None:
        file_stem = file.stem
        self.input_files[file_stem] = []
        with open(file, 'r') as f: 
            lines = f.readlines()
            for line in lines:
                line = line.split("//")[0].strip()
                if not line:
                    continue
                self.input_files[file_stem].append(line) 

    def has_more_commands(self, filename) -> bool:
        return not self.input_index == len(self.input_files[filename])

    def rest(self) -> None:
        self.input_index = 0

    def advance(self, filename: str) -> None:
        self.current_command = self.input_files[filename][self.input_index]
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
        elif command_parts[0] == "label":
            return CommandType.C_LABEL
        elif command_parts[0] == "if-goto":
            return CommandType.C_IF
        elif command_parts[0] == "goto":
            return CommandType.C_GOTO
        elif command_parts[0] == "function":
            return CommandType.C_FUNCTION
        elif command_parts[0] == "call":
            return CommandType.C_CALL
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
     