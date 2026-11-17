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
        if cmd_type == CommandType.C_PUSH:
            if segment == HACK_POINTER_OPS:
                steps = [f"@{HACK_POINTERS[index]}", "D=M"]
                for s in steps:
                    self.output_file.write(f"{s}\n")

            if segment == "constant":
                self.output_file.write(f"@{index}\n")
                self.output_file.write("D=A\n")

            if segment in HACK_MNEUNOMICS_COMMANDS.keys():
                steps = HACK_MNEUNOMICS_COMMANDS[segment] + [f"@{index}", "A=D+A", "D=M"]
                for s in steps:
                    self.output_file.write(f"{s}\n")

            for seq in self.push_sequences:
                self.output_file.write(f"{seq}\n")

        if cmd_type == CommandType.C_POP:
            if segment in HACK_MNEUNOMICS_COMMANDS.keys():
                steps = HACK_MNEUNOMICS_COMMANDS[segment] + [f"@{index}", "D=D+A"]
                for s in steps:
                    self.output_file.write(f"{s}\n")

            if segment == HACK_POINTER_OPS:
                pointer_pop_sequences = ["@SP", "AM=M-1", "D=M", f"@{HACK_POINTERS[index]}", "M=D"]
                for seq in pointer_pop_sequences:
                    self.output_file.write(f"{seq}\n")
            else:
                for seq in self.pop_sequances:
                    self.output_file.write(f"{seq}\n")


    def write_arithmetic(self, command: str) -> None:
        if command in HACK_ARITHMETICS.keys():
            add_sub_steps = ["@SP", "AM=M-1", "D=M", "A=A-1", f"M={HACK_ARITHMETICS[command]}"]
            for step in add_sub_steps:
                self.output_file.write(f"{step}\n")

        if command in HACK_LOGICAL_OPS.keys():
            n_ops_base_steps = ["@SP", "A=M-1"]
            and_or_base_steps = ["@SP", "AM=M-1", "D=M", "A=A-1"]
            if command in ["neg", "not"]:
                ng_not_steps = n_ops_base_steps + [f"{HACK_LOGICAL_OPS[command]}"]
                for step in ng_not_steps:
                    self.output_file.write(f"{step}\n")
            else:
                and_or_steps = and_or_base_steps + [f"{HACK_LOGICAL_OPS[command]}"]
                for step in and_or_steps:
                    self.output_file.write(f"{step}\n")

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

            for step in comp_steps:
                self.output_file.write(f"{step}\n")
        

    def _close_loop(self) -> None:
        self.output_file.write("(END)\n")
        self.output_file.write("@END\n")
        self.output_file.write("0;JMP")

    def close(self):
        self._close_loop()
        self.output_file.close()