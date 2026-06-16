"""
CodeWriter module for the Hack VM Translator.
Translates parsed VM commands into Hack Assembly.
"""

SEGMENT_BASE = {
    "local": "LCL",
    "argument": "ARG",
    "this": "THIS",
    "that": "THAT",
}


class CodeWriter:
    def __init__(self, output_file: str):
        self.output = open(output_file, "w")
        self._label_counter = 0
        self._current_file = ""
        self._write_init()

    def _write_init(self):
        """Write bootstrap code: SP=256, call Sys.init"""
        self._write_lines([
            "// Bootstrap: SP=256",
            "@256",
            "D=A",
            "@SP",
            "M=D",
        ])
        self.write_call("Sys.init", 0)

    def set_file_name(self, filename: str):
        """Called when a new .vm file is being translated."""
        self._current_file = filename

    def _write_lines(self, lines):
        for line in lines:
            self.output.write(line + "\n")

    def _unique_label(self, prefix="LABEL"):
        self._label_counter += 1
        return f"{prefix}_{self._label_counter}"

    # ------------------------------------------------------------------ #
    # Stack helpers
    # ------------------------------------------------------------------ #
    def _push_D(self):
        """Push D register onto stack."""
        return [
            "@SP",
            "A=M",
            "M=D",
            "@SP",
            "M=M+1",
        ]

    def _pop_to_D(self):
        """Pop top of stack into D register."""
        return [
            "@SP",
            "AM=M-1",
            "D=M",
        ]

    # ------------------------------------------------------------------ #
    # Arithmetic / Logic
    # ------------------------------------------------------------------ #
    def write_arithmetic(self, command: str):
        self._write_lines([f"// {command}"])
        asm = []

        if command == "add":
            asm += self._pop_to_D()
            asm += ["A=A-1", "M=D+M"]
        elif command == "sub":
            asm += self._pop_to_D()
            asm += ["A=A-1", "M=M-D"]
        elif command == "neg":
            asm += ["@SP", "A=M-1", "M=-M"]
        elif command == "not":
            asm += ["@SP", "A=M-1", "M=!M"]
        elif command == "and":
            asm += self._pop_to_D()
            asm += ["A=A-1", "M=D&M"]
        elif command == "or":
            asm += self._pop_to_D()
            asm += ["A=A-1", "M=D|M"]
        elif command in ("eq", "gt", "lt"):
            true_label = self._unique_label(f"TRUE_{command.upper()}")
            end_label = self._unique_label("END_CMP")
            jump_map = {"eq": "JEQ", "gt": "JGT", "lt": "JLT"}
            jump = jump_map[command]
            asm += self._pop_to_D()
            asm += [
                "A=A-1",
                "D=M-D",
                f"@{true_label}",
                f"D;{jump}",
                "@SP", "A=M-1", "M=0",
                f"@{end_label}", "0;JMP",
                f"({true_label})",
                "@SP", "A=M-1", "M=-1",
                f"({end_label})",
            ]

        self._write_lines(asm)

    # ------------------------------------------------------------------ #
    # Push / Pop
    # ------------------------------------------------------------------ #
    def write_push_pop(self, command_type: str, segment: str, index: int):
        from parser import C_PUSH
        self._write_lines([f"// {'push' if command_type == C_PUSH else 'pop'} {segment} {index}"])
        asm = []

        if command_type == C_PUSH:
            if segment == "constant":
                asm += [f"@{index}", "D=A"]
                asm += self._push_D()

            elif segment in SEGMENT_BASE:
                asm += [
                    f"@{SEGMENT_BASE[segment]}",
                    "D=M",
                    f"@{index}",
                    "A=D+A",
                    "D=M",
                ]
                asm += self._push_D()

            elif segment == "static":
                asm += [f"@{self._current_file}.{index}", "D=M"]
                asm += self._push_D()

            elif segment == "temp":
                addr = 5 + index
                asm += [f"@{addr}", "D=M"]
                asm += self._push_D()

            elif segment == "pointer":
                reg = "THIS" if index == 0 else "THAT"
                asm += [f"@{reg}", "D=M"]
                asm += self._push_D()

        else:  # POP
            if segment in SEGMENT_BASE:
                # Store target addr in R13
                asm += [
                    f"@{SEGMENT_BASE[segment]}",
                    "D=M",
                    f"@{index}",
                    "D=D+A",
                    "@R13",
                    "M=D",
                ]
                asm += self._pop_to_D()
                asm += ["@R13", "A=M", "M=D"]

            elif segment == "static":
                asm += self._pop_to_D()
                asm += [f"@{self._current_file}.{index}", "M=D"]

            elif segment == "temp":
                addr = 5 + index
                asm += self._pop_to_D()
                asm += [f"@{addr}", "M=D"]

            elif segment == "pointer":
                reg = "THIS" if index == 0 else "THAT"
                asm += self._pop_to_D()
                asm += [f"@{reg}", "M=D"]

        self._write_lines(asm)

    # ------------------------------------------------------------------ #
    # Program Flow
    # ------------------------------------------------------------------ #
    def write_label(self, label: str):
        self._write_lines([f"// label {label}", f"({self._current_file}${label})"])

    def write_goto(self, label: str):
        self._write_lines([
            f"// goto {label}",
            f"@{self._current_file}${label}",
            "0;JMP",
        ])

    def write_if(self, label: str):
        self._write_lines([f"// if-goto {label}"])
        asm = self._pop_to_D()
        asm += [f"@{self._current_file}${label}", "D;JNE"]
        self._write_lines(asm)

    # ------------------------------------------------------------------ #
    # Function Calls
    # ------------------------------------------------------------------ #
    def write_function(self, function_name: str, num_locals: int):
        self._write_lines([f"// function {function_name} {num_locals}", f"({function_name})"])
        # Initialize local variables to 0
        for _ in range(num_locals):
            self._write_lines(["@SP", "A=M", "M=0", "@SP", "M=M+1"])

    def write_call(self, function_name: str, num_args: int):
        return_label = self._unique_label(f"{function_name}$ret")
        self._write_lines([f"// call {function_name} {num_args}"])
        asm = []

        # Push return address
        asm += [f"@{return_label}", "D=A"] + self._push_D()
        # Push LCL, ARG, THIS, THAT
        for seg in ["LCL", "ARG", "THIS", "THAT"]:
            asm += [f"@{seg}", "D=M"] + self._push_D()
        # ARG = SP - 5 - num_args
        asm += [
            "@SP", "D=M",
            f"@{5 + num_args}", "D=D-A",
            "@ARG", "M=D",
        ]
        # LCL = SP
        asm += ["@SP", "D=M", "@LCL", "M=D"]
        # goto function
        asm += [f"@{function_name}", "0;JMP"]
        # return label
        asm += [f"({return_label})"]

        self._write_lines(asm)

    def write_return(self):
        self._write_lines(["// return"])
        asm = [
            # FRAME = LCL (store in R14)
            "@LCL", "D=M", "@R14", "M=D",
            # RET = *(FRAME-5) (store in R15)
            "@5", "A=D-A", "D=M", "@R15", "M=D",
            # *ARG = pop()  (reposition return value)
        ]
        asm += self._pop_to_D()
        asm += [
            "@ARG", "A=M", "M=D",
            # SP = ARG+1
            "@ARG", "D=M+1", "@SP", "M=D",
        ]
        # Restore THAT, THIS, ARG, LCL from frame
        for i, seg in enumerate(["THAT", "THIS", "ARG", "LCL"], start=1):
            asm += [f"@R14", "D=M", f"@{i}", "A=D-A", "D=M", f"@{seg}", "M=D"]
        # goto RET
        asm += ["@R15", "A=M", "0;JMP"]

        self._write_lines(asm)

    def close(self):
        self.output.close()
