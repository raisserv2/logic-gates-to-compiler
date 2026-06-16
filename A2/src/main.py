"""
main.py — Hack VM Translator
Usage:
    python main.py <input.vm>          # single file
    python main.py <directory/>        # all .vm files in directory
Output: <input>.asm or <directory>/<directory>.asm
"""

import sys
import os
from parser import (
    Parser,
    C_ARITHMETIC, C_PUSH, C_POP,
    C_LABEL, C_GOTO, C_IF,
    C_FUNCTION, C_CALL, C_RETURN,
)
from code_writer import CodeWriter


def translate(vm_files: list[str], output_path: str):
    writer = CodeWriter(output_path)

    for vm_file in vm_files:
        # Set current filename (stem, used for static labels)
        stem = os.path.splitext(os.path.basename(vm_file))[0]
        writer.set_file_name(stem)

        parser = Parser(vm_file)
        while parser.has_more_commands():
            parser.advance()
            ct = parser.command_type()

            if ct == C_ARITHMETIC:
                writer.write_arithmetic(parser.arg1())
            elif ct in (C_PUSH, C_POP):
                writer.write_push_pop(ct, parser.arg1(), parser.arg2())
            elif ct == C_LABEL:
                writer.write_label(parser.arg1())
            elif ct == C_GOTO:
                writer.write_goto(parser.arg1())
            elif ct == C_IF:
                writer.write_if(parser.arg1())
            elif ct == C_FUNCTION:
                writer.write_function(parser.arg1(), parser.arg2())
            elif ct == C_CALL:
                writer.write_call(parser.arg1(), parser.arg2())
            elif ct == C_RETURN:
                writer.write_return()

    writer.close()
    print(f"[✓] Translated → {output_path}")


def main():
    if len(sys.argv) != 2:
        print("Usage: python main.py <file.vm | directory>")
        sys.exit(1)

    path = sys.argv[1].rstrip("/\\")

    if os.path.isdir(path):
        vm_files = sorted([
            os.path.join(path, f)
            for f in os.listdir(path)
            if f.endswith(".vm")
        ])
        if not vm_files:
            print(f"No .vm files found in {path}")
            sys.exit(1)
        dir_name = os.path.basename(path)
        output_path = os.path.join(path, dir_name + ".asm")
    elif path.endswith(".vm") and os.path.isfile(path):
        vm_files = [path]
        output_path = path.replace(".vm", ".asm")
    else:
        print(f"Invalid input: {path}")
        sys.exit(1)

    translate(vm_files, output_path)


if __name__ == "__main__":
    main()
