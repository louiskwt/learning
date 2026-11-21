from vm_parser import CommandType

TARGET_EXT = ".asm"

POINTER_COMMAND = "D=M"
ADDRESS_COMMAND = "D=A"

HACK_MNEUNOMICS_COMMANDS = {
    "local": ["@LCL", POINTER_COMMAND],
    "argument": ["@ARG", POINTER_COMMAND],
    "this": ["@THIS", POINTER_COMMAND],
    "that": ["@THAT", POINTER_COMMAND],
    "temp": ["@5", ADDRESS_COMMAND],
    "static": ["@16", ADDRESS_COMMAND]
}

HACK_POINTER_OPS = "pointer"

HACK_POINTERS = {
    0: "THIS",
    1: "THAT"
}

HACK_ARITHMETICS = {
    "add": "D+M",
    "sub": "M-D"
}

HACK_LOGICAL_OPS = {
    "neg": "M=-M",
    "not": "M=!M",
    "and": "M=D&M",
    "or": "M=D|M"
}

HACK_COMP_OPS = {
    "eq": "JEQ",
    "gt": "JGT",
    "lt": "JLT"
}

class CodeWriter():
    def __init__(self, filename) -> None:
        self.output_file = open(filename, "w")
        self.stack_count = {}
        self.push_sequences = ["@SP", "A=M", "M=D", "@SP", "M=M+1"]
        self.pop_sequances = ["@R13", "M=D", "@SP", "AM=M-1", "D=M", "@R13", "A=M", "M=D"]


    def write_push_pop(self, cmd_type: CommandType, segment: str, index: int) -> None:
        commands_to_write = []
        sequences_to_attach = self.push_sequences if cmd_type == CommandType.C_PUSH else self.pop_sequances

        if cmd_type == CommandType.C_PUSH:
            if segment == HACK_POINTER_OPS:
                commands_to_write.extend([f"@{HACK_POINTERS[index]}", POINTER_COMMAND])

            if segment == "constant":
                commands_to_write.extend([f"@{index}", ADDRESS_COMMAND])

            if segment in HACK_MNEUNOMICS_COMMANDS.keys():
                commands_to_write.extend(HACK_MNEUNOMICS_COMMANDS[segment] + [f"@{index}", "A=D+A", POINTER_COMMAND])

            commands_to_write.extend(sequences_to_attach)

        if cmd_type == CommandType.C_POP:
            if segment in HACK_MNEUNOMICS_COMMANDS.keys():
                commands_to_write.extend(HACK_MNEUNOMICS_COMMANDS[segment] + [f"@{index}", "D=D+A"])

            if segment == HACK_POINTER_OPS:
                commands_to_write.extend(["@SP", "AM=M-1", "D=M", f"@{HACK_POINTERS[index]}", "M=D"])
            else:
                commands_to_write.extend(sequences_to_attach)
            
        for cmd in commands_to_write:
            self.output_file.write(f"{cmd}\n")


    def write_arithmetic(self, command: str) -> None:
        commands_to_write = []

        if command in HACK_ARITHMETICS.keys():
            commands_to_write.extend(["@SP", "AM=M-1", "D=M", "A=A-1", f"M={HACK_ARITHMETICS[command]}"])

        if command in HACK_LOGICAL_OPS.keys():
            n_ops_base_commands = ["@SP", "A=M-1"]
            and_or_base_commands = ["@SP", "AM=M-1", "D=M", "A=A-1"]
            if command in ["neg", "not"]:
                commands_to_write.extend(n_ops_base_commands + [f"{HACK_LOGICAL_OPS[command]}"])
            else:
                commands_to_write.extend(and_or_base_commands + [f"{HACK_LOGICAL_OPS[command]}"])

        if command in HACK_COMP_OPS.keys():
            label = command.upper()

            if label not in self.stack_count.keys():
                self.stack_count[label] = 1

            comp_steps = [
                "@SP", "AM=M-1", "D=M", "A=A-1", "D=M-D", f"@{label}_TRUE_{self.stack_count[label]}", f"D;{HACK_COMP_OPS[command]}", 
                "@SP", "A=M-1", "M=0", f"@{label}_END_{self.stack_count[label]}", "0;JMP", f"({label}_TRUE_{self.stack_count[label]})", "@SP", "A=M-1", "M=-1", 
                f"({label}_END_{self.stack_count[label]})"   
            ]

            self.stack_count[label] = self.stack_count[label] + 1
            commands_to_write.extend(comp_steps)

        for cmd in commands_to_write:
            self.output_file.write(f"{cmd}\n") 

    def _close_loop(self) -> None:
        self.output_file.write("(END_FILE_LOOP)\n")
        self.output_file.write("@END_FILE_LOOP\n")
        self.output_file.write("0;JMP")


    def close(self) -> None:
        self._close_loop()
        self.output_file.close()