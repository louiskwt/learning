from vm_parser import CommandType

TARGET_EXT = ".asm"

POINTER_COMMAND = "D=M"
ADDRESS_COMMAND = "D=A"
GOTO_COMMAND = "0;JMP"
POINTER_SYMBOL = "@SP"

HACK_MNEUNOMICS_COMMANDS = {
    "local": ["@LCL", POINTER_COMMAND],
    "argument": ["@ARG", POINTER_COMMAND],
    "this": ["@THIS", POINTER_COMMAND],
    "that": ["@THAT", POINTER_COMMAND],
    "temp": ["@5", ADDRESS_COMMAND],
    "static": [ADDRESS_COMMAND]
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
        self.static_count = {}
        self.current_file_name = ""
        self.address_count = {}
        self.push_sequences = ["@SP", "A=M", "M=D", "@SP", "M=M+1"]
        self.pop_sequances = ["@R13", "M=D", "@SP", "AM=M-1", "D=M", "@R13", "A=M", "M=D"]
        self.branching_sequences = ["@SP", "AM=M-1", "D=M"]
        self.return_sequences = [
                                    "@LCL", POINTER_COMMAND, "@R13", "M=D", "@5", "A=D-A",
                                    POINTER_COMMAND, "@R14", "M=D", POINTER_SYMBOL, "AM=M-1", POINTER_COMMAND,
                                    "@ARG", "A=M", "M=D", "@ARG", "D=M+1", POINTER_SYMBOL, "M=D", "@R13", "AM=M-1",
                                    POINTER_COMMAND, "@THAT", "M=D", "@R13", "AM=M-1", "D=M", "@THIS", "M=D", "@R13",
                                    "AM=M-1", "D=M", "@ARG", "M=D", "@R13", "AM=M-1", "D=M", "@LCL", "M=D", "@R14",
                                    "A=M", GOTO_COMMAND
                                 ]


    def set_file_name(self, filename: str) -> None:
        self.current_file_name = filename


    def generate_bootstrap_code(self) -> None:
        boot_strap_code = ["@256", "D=A", "@SP", "M=D"]
        self._output_command(boot_strap_code)


    def write_push_pop(self, cmd_type: CommandType, segment: str, index: int) -> None:
        commands_to_write = []
        sequences_to_attach = self.push_sequences if cmd_type == CommandType.C_PUSH else self.pop_sequances

        if cmd_type == CommandType.C_PUSH:
            if segment == HACK_POINTER_OPS:
                commands_to_write.extend([f"@{HACK_POINTERS[index]}", POINTER_COMMAND])

            if segment == "constant":
                commands_to_write.extend([f"@{index}", ADDRESS_COMMAND])

            if segment in HACK_MNEUNOMICS_COMMANDS.keys():
                if segment == "static":
                    current_stat = self.static_count.get(self.current_file_name, 0)
                    self.static_count[self.current_file_name] = current_stat + 1
                    commands_to_write.extend([f"@{self.current_file_name}.{index}", POINTER_COMMAND])
                else:
                    commands_to_write.extend(HACK_MNEUNOMICS_COMMANDS[segment] + [f"@{index}", "A=D+A", POINTER_COMMAND])

            commands_to_write.extend(sequences_to_attach)

        if cmd_type == CommandType.C_POP:
            if segment in HACK_MNEUNOMICS_COMMANDS.keys():
                if segment == "static":
                    current_stat = self.static_count.get(self.current_file_name, 0)
                    self.static_count[self.current_file_name] = current_stat + 1
                    commands_to_write.extend([f"@{self.current_file_name}.{index}", "D=A"])
                else:
                    commands_to_write.extend(HACK_MNEUNOMICS_COMMANDS[segment] + [f"@{index}", "D=D+A"])

            if segment == HACK_POINTER_OPS:
                commands_to_write.extend(["@SP", "AM=M-1", "D=M", f"@{HACK_POINTERS[index]}", "M=D"])
            else:
                commands_to_write.extend(sequences_to_attach)
            
        self._output_command(commands_to_write) 


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

        self._output_command(commands_to_write)


    def write_label(self, label: str) -> None:
        label_command = f"({label})\n"
        self.output_file.write(label_command)


    def write_goto(self, label:str) -> None:
        commands_to_write = [f"@{label}", GOTO_COMMAND]
        self._output_command(commands_to_write)


    def write_if_goto(self, label) -> None:
        commands_to_write = self.branching_sequences + [f"@{label}", "D;JNE"]
        self._output_command(commands_to_write)


    def write_function(self, function_name: str, n_vars: int) -> None:
        self.output_file.write(f"({function_name})\n")
        commands_to_write = ["@0", "D=A"] + self.push_sequences
        for _ in range(n_vars):
            for cmd in commands_to_write:
                self.output_file.write(f"{cmd}\n")

    def write_call(self, function_name: str, n_args: int) -> None:
        ret_addr = f"{function_name}$ret"
        next_addr = self.address_count.get(function_name, 1)

        self.address_count[function_name] = next_addr + 1

        ret_address_commands = [f"@{ret_addr}.{next_addr}", "D=A"] + self.push_sequences
        self._output_command(ret_address_commands)

        lcl_commands = HACK_MNEUNOMICS_COMMANDS["local"] + self.push_sequences
        self._output_command(lcl_commands)
        
        arg_commands = HACK_MNEUNOMICS_COMMANDS["argument"] + self.push_sequences
        self._output_command(arg_commands)

        this_commands = HACK_MNEUNOMICS_COMMANDS["this"] + self.push_sequences
        self._output_command(this_commands)

        that_commands = HACK_MNEUNOMICS_COMMANDS["that"] + self.push_sequences
        self._output_command(that_commands)

        nArgs_commands = ["@SP", "D=M", "@5", "D=D-A", f"@{n_args}", "D=D-A", "@ARG", "M=D"]
        self._output_command(nArgs_commands)
        
        lcl_sp_commands = ["@SP", "D=M", "@LCL", "M=D"]
        self._output_command(lcl_sp_commands)

        goto_func_and_label_commands = [f"@{function_name}", GOTO_COMMAND, f"({ret_addr}.{next_addr})"] 
        self._output_command(goto_func_and_label_commands)


    def write_bootstrap_code(self) -> None:
        bootstrap_code = ["@256", "D=A", "@SP", "M=D"]
        self._output_command(bootstrap_code)

        ret_address_commands = [f"@RET_BOOTSTRAP", "D=A"] + self.push_sequences
        self._output_command(ret_address_commands)

        lcl_commands = HACK_MNEUNOMICS_COMMANDS["local"] + self.push_sequences
        self._output_command(lcl_commands)
        
        arg_commands = HACK_MNEUNOMICS_COMMANDS["argument"] + self.push_sequences
        self._output_command(arg_commands)

        this_commands = HACK_MNEUNOMICS_COMMANDS["this"] + self.push_sequences
        self._output_command(this_commands)

        that_commands = HACK_MNEUNOMICS_COMMANDS["that"] + self.push_sequences
        self._output_command(that_commands)

        nArgs_commands = ["@SP", "D=M", "@5", "D=D-A", "@ARG", "M=D"]
        self._output_command(nArgs_commands)
        
        lcl_sp_commands = ["@SP", "D=M", "@LCL", "M=D"]
        self._output_command(lcl_sp_commands)

        goto_func_and_label_commands = [f"@Sys.init", GOTO_COMMAND, "(RET_BOOTSTRAP)"] 
        self._output_command(goto_func_and_label_commands)

    def write_return(self) -> None:
        for cmd in self.return_sequences:
            self.output_file.write(f"{cmd}\n")


    def _output_command(self, commands: list[str]) -> None:
        for cmd in commands:
            self.output_file.write(f"{cmd}\n")

        
    def _close_loop(self) -> None:
        self.output_file.write("(END_FILE_LOOP)\n")
        self.output_file.write("@END_FILE_LOOP\n")
        self.output_file.write("0;JMP")


    def close(self) -> None:
        self._close_loop()
        self.output_file.close()