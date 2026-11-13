
class Code():
    def __init__(self) -> None:
        bit_length_3, bit_length_7 = 3, 7

        self.comp_code = {
            # a = 0
            "0": f"{42:0{bit_length_7}b}",
            "1": f"{63:0{bit_length_7}b}",
            "-1": f"{58:0{bit_length_7}b}",
            "D": f"{12:0{bit_length_7}b}",
            "A": f"{48:0{bit_length_7}b}",
            "!D": f"{13:0{bit_length_7}b}",
            "!A": f"{49:0{bit_length_7}b}",
            "-D": f"{15:0{bit_length_7}b}",
            "-A": f"{51:0{bit_length_7}b}",
            "D+1": f"{31:0{bit_length_7}b}", 
            "A+1": f"{55:0{bit_length_7}b}", 
            "D-1": f"{14:0{bit_length_7}b}", 
            "A-1": f"{50:0{bit_length_7}b}", 
            "D+A": f"{2:0{bit_length_7}b}",
            "D-A": f"{19:0{bit_length_7}b}",
            "A-D": f"{7:0{bit_length_7}b}",
            "D&A": f"{0:0{bit_length_7}b}",
            "D|A": f"{21:0{bit_length_7}b}",
            # a = 1
            "M": f"{112:0{bit_length_7}b}",
            "!M": f"{113:0{bit_length_7}b}",
            "-M": f"{115:0{bit_length_7}b}",
            "M+1": f"{119:0{bit_length_7}b}",
            "M-1": f"{114:0{bit_length_7}b}",
            "D+M": f"{66:0{bit_length_7}b}",
            "D-M": f"{83:0{bit_length_7}b}",
            "M-D": f"{71:0{bit_length_7}b}",
            "D&M": f"{64:0{bit_length_7}b}",
            "D|M": f"{85:0{bit_length_7}b}",
        }

        self.dest_code = {
            "null": f"{0:0{bit_length_3}b}",
            "M": f"{1:0{bit_length_3}b}",
            "D": f"{2:0{bit_length_3}b}",
            "MD": f"{3:0{bit_length_3}b}",
            "DM": f"{3:0{bit_length_3}b}",
            "A": f"{4:0{bit_length_3}b}",
            "AM": f"{5:0{bit_length_3}b}",
            "AD": f"{6:0{bit_length_3}b}",
            "AMD": f"{7:0{bit_length_3}b}",
        }

        self.jmp_code = {
            "null": f"{0:0{bit_length_3}b}",
            "JGT": f"{1:0{bit_length_3}b}",
            "JEQ": f"{2:0{bit_length_3}b}",
            "JGE": f"{3:0{bit_length_3}b}",
            "JLT": f"{4:0{bit_length_3}b}",
            "JNE": f"{5:0{bit_length_3}b}",
            "JLE": f"{6:0{bit_length_3}b}",
            "JMP": f"{7:0{bit_length_3}b}",
        }

    def dest(self, mnemonic: str) -> str:
        return self.dest_code.get(mnemonic, self.dest_code["null"])

    def jmp(self, mnemonic: str) -> str:
        return self.jmp_code.get(mnemonic, self.dest_code["null"])

    def comp(self, mnemonic: str) -> str:
        return self.comp_code.get(mnemonic, "")