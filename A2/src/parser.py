"""
Parser module for the Hack VM Translator.
Handles reading and parsing of .vm files.
"""

C_ARITHMETIC = "C_ARITHMETIC"
C_PUSH = "C_PUSH"
C_POP = "C_POP"
C_LABEL = "C_LABEL"
C_GOTO = "C_GOTO"
C_IF = "C_IF"
C_FUNCTION = "C_FUNCTION"
C_CALL = "C_CALL"
C_RETURN = "C_RETURN"

ARITHMETIC_CMDS = {"add", "sub", "neg", "eq", "gt", "lt", "and", "or", "not"}


class Parser:
    def __init__(self, vm_file: str):
        with open(vm_file, "r") as f:
            raw_lines = f.readlines()

        self.commands = []
        for line in raw_lines:
            line = line.split("//")[0].strip()
            if line:
                self.commands.append(line)

        self.current_index = -1
        self.current_command = None

    def has_more_commands(self) -> bool:
        return self.current_index < len(self.commands) - 1

    def advance(self):
        self.current_index += 1
        self.current_command = self.commands[self.current_index]

    def command_type(self) -> str:
        first = self.current_command.split()[0]
        if first in ARITHMETIC_CMDS:
            return C_ARITHMETIC
        elif first == "push":
            return C_PUSH
        elif first == "pop":
            return C_POP
        elif first == "label":
            return C_LABEL
        elif first == "goto":
            return C_GOTO
        elif first == "if-goto":
            return C_IF
        elif first == "function":
            return C_FUNCTION
        elif first == "call":
            return C_CALL
        elif first == "return":
            return C_RETURN
        else:
            raise ValueError(f"Unknown command: {self.current_command}")

    def arg1(self) -> str:
        """Returns arg1. For C_ARITHMETIC, returns the command itself."""
        parts = self.current_command.split()
        if self.command_type() == C_ARITHMETIC:
            return parts[0]
        return parts[1]

    def arg2(self) -> int:
        """Returns arg2 (only for push, pop, function, call)."""
        return int(self.current_command.split()[2])
