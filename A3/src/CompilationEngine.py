

import os
from JackTokenizer import Token
from SymbolTable import SymbolTable
from VMWriter import VMWriter

OP_MAP = {
    "+": "add", "-": "sub", "=": "eq", ">": "gt", "<": "lt",
    "&": "and", "|": "or",
}
UNARY_OP_MAP = {"-": "neg", "~": "not"}

KEYWORD_CONSTANTS = {"true", "false", "null", "this"}


class CompilationEngine:
    def __init__(self, tokens: list[Token], class_name: str, output_dir: str):
        self.tokens = tokens
        self.pos = 0
        self.class_name = class_name
        self.output_dir = output_dir

        self.sym = SymbolTable()
        self.vm = VMWriter(os.path.join(output_dir, f"{class_name}.vm"))

        self._xml_lines: list[str] = []
        self._indent = 0
        self._label_counter = 0

    def _current(self) -> Token:
        return self.tokens[self.pos]

    def _peek_value(self) -> str:
        return self.tokens[self.pos].value

    def _peek_type(self) -> str:
        return self.tokens[self.pos].type

    def _advance(self) -> Token:
        tok = self.tokens[self.pos]
        self.pos += 1
        return tok

    def _eat(self, expected_value: str) -> Token:
        
        tok = self._advance()
        assert tok.value == expected_value, \
            f"Expected '{expected_value}', got '{tok.value}' at token {self.pos}"
        return tok

    def _eat_type(self, expected_type: str) -> Token:
        
        tok = self._advance()
        assert tok.type == expected_type, \
            f"Expected type '{expected_type}', got '{tok.type}' ('{tok.value}') at token {self.pos}"
        return tok

    def _unique_label(self, tag: str) -> str:
        self._label_counter += 1
        return f"{tag}_{self._label_counter}"

    def _xml_open(self, tag: str):
        self._xml_lines.append("  " * self._indent + f"<{tag}>")
        self._indent += 1

    def _xml_close(self, tag: str):
        self._indent -= 1
        self._xml_lines.append("  " * self._indent + f"</{tag}>")

    def _xml_terminal(self, tok: Token):
        val = tok.xml_value()
        self._xml_lines.append("  " * self._indent + f"<{tok.type}> {val} </{tok.type}>")

    def _write_xml(self):
        path = os.path.join(self.output_dir, f"{self.class_name}.xml")
        with open(path, "w") as f:
            f.write("\n".join(self._xml_lines) + "\n")
        print(f"  [xml] {path}")

    def _process(self, expected_value: str = None):
        
        if expected_value:
            tok = self._eat(expected_value)
        else:
            tok = self._advance()
        self._xml_terminal(tok)
        return tok

    def _process_type(self, expected_type: str = None):
        if expected_type:
            tok = self._eat_type(expected_type)
        else:
            tok = self._advance()
        self._xml_terminal(tok)
        return tok


    def compile_class(self):
        
        self._xml_open("class")

        self._process("class")
        self._process()           # className
        self._process("{")

        while self._peek_value() in ("static", "field"):
            self.compile_class_var_dec()

        while self._peek_value() in ("constructor", "function", "method"):
            self.compile_subroutine_dec()

        self._process("}")
        self._xml_close("class")

        self.vm.close()
        self._write_xml()

    def compile_class_var_dec(self):
        
        self._xml_open("classVarDec")

        kind = self._process().value        # static | field
        var_type = self._process().value     # type
        name = self._process().value         # varName
        self.sym.define(name, var_type, kind)

        while self._peek_value() == ",":
            self._process(",")
            name = self._process().value
            self.sym.define(name, var_type, kind)

        self._process(";")
        self._xml_close("classVarDec")

    def compile_subroutine_dec(self):
        
        self._xml_open("subroutineDec")

        self.sym.start_subroutine()

        sub_kind = self._process().value   # constructor | function | method
        self._process()                     # return type
        sub_name = self._process().value    # subroutine name

        if sub_kind == "method":
            self.sym.define("this", self.class_name, "argument")

        self._process("(")
        self.compile_parameter_list()
        self._process(")")

        self._xml_open("subroutineBody")
        self._process("{")

        while self._peek_value() == "var":
            self.compile_var_dec()

        n_locals = self.sym.var_count("var")
        self.vm.write_function(f"{self.class_name}.{sub_name}", n_locals)

        if sub_kind == "constructor":
            n_fields = self.sym.var_count("field")
            self.vm.write_push("constant", n_fields)
            self.vm.write_call("Memory.alloc", 1)
            self.vm.write_pop("pointer", 0)  # anchor THIS

        if sub_kind == "method":
            self.vm.write_push("argument", 0)
            self.vm.write_pop("pointer", 0)

        self.compile_statements()
        self._process("}")
        self._xml_close("subroutineBody")
        self._xml_close("subroutineDec")

    def compile_parameter_list(self):
        
        self._xml_open("parameterList")

        if self._peek_value() != ")":
            var_type = self._process().value
            name = self._process().value
            self.sym.define(name, var_type, "argument")

            while self._peek_value() == ",":
                self._process(",")
                var_type = self._process().value
                name = self._process().value
                self.sym.define(name, var_type, "argument")

        self._xml_close("parameterList")

    def compile_var_dec(self):
        
        self._xml_open("varDec")

        self._process("var")
        var_type = self._process().value
        name = self._process().value
        self.sym.define(name, var_type, "var")

        while self._peek_value() == ",":
            self._process(",")
            name = self._process().value
            self.sym.define(name, var_type, "var")

        self._process(";")
        self._xml_close("varDec")


    def compile_statements(self):
        self._xml_open("statements")
        while self._peek_value() in ("let", "if", "while", "do", "return"):
            if self._peek_value() == "let":
                self.compile_let()
            elif self._peek_value() == "if":
                self.compile_if()
            elif self._peek_value() == "while":
                self.compile_while()
            elif self._peek_value() == "do":
                self.compile_do()
            elif self._peek_value() == "return":
                self.compile_return()
        self._xml_close("statements")

    def compile_let(self):
        
        self._xml_open("letStatement")
        self._process("let")

        var_name = self._process().value
        sym = self.sym.lookup(var_name)
        is_array = False

        if self._peek_value() == "[":
            is_array = True
            self._process("[")
            self.vm.write_push(sym.segment(), sym.index)
            self.compile_expression()   # push index
            self.vm.write_arithmetic("add")  # base + index
            self._process("]")

        self._process("=")
        self.compile_expression()   # push RHS value

        if is_array:
            self.vm.write_pop("temp", 0)
            self.vm.write_pop("pointer", 1)
            self.vm.write_push("temp", 0)
            self.vm.write_pop("that", 0)
        else:
            self.vm.write_pop(sym.segment(), sym.index)

        self._process(";")
        self._xml_close("letStatement")

    def compile_if(self):
        
        self._xml_open("ifStatement")

        label_else = self._unique_label("IF_ELSE")
        label_end = self._unique_label("IF_END")

        self._process("if")
        self._process("(")
        self.compile_expression()
        self._process(")")

        self.vm.write_arithmetic("not")
        self.vm.write_if(label_else)

        self._process("{")
        self.compile_statements()
        self._process("}")

        self.vm.write_goto(label_end)
        self.vm.write_label(label_else)

        if self._peek_value() == "else":
            self._process("else")
            self._process("{")
            self.compile_statements()
            self._process("}")

        self.vm.write_label(label_end)
        self._xml_close("ifStatement")

    def compile_while(self):
        
        self._xml_open("whileStatement")

        label_loop = self._unique_label("WHILE_LOOP")
        label_end = self._unique_label("WHILE_END")

        self.vm.write_label(label_loop)

        self._process("while")
        self._process("(")
        self.compile_expression()
        self._process(")")

        self.vm.write_arithmetic("not")
        self.vm.write_if(label_end)

        self._process("{")
        self.compile_statements()
        self._process("}")

        self.vm.write_goto(label_loop)
        self.vm.write_label(label_end)

        self._xml_close("whileStatement")

    def compile_do(self):
        
        self._xml_open("doStatement")
        self._process("do")

        name = self._process().value
        self._compile_subroutine_call(name)

        self.vm.write_pop("temp", 0)

        self._process(";")
        self._xml_close("doStatement")

    def compile_return(self):
        
        self._xml_open("returnStatement")
        self._process("return")

        if self._peek_value() != ";":
            self.compile_expression()
        else:
            self.vm.write_push("constant", 0)  # void returns push 0

        self.vm.write_return()
        self._process(";")
        self._xml_close("returnStatement")


    def compile_expression(self):
        
        self._xml_open("expression")

        self.compile_term()

        while self._peek_value() in "+-*/&|<>=":
            op = self._process().value
            self.compile_term()

            if op == "*":
                self.vm.write_call("Math.multiply", 2)
            elif op == "/":
                self.vm.write_call("Math.divide", 2)
            else:
                self.vm.write_arithmetic(OP_MAP[op])

        self._xml_close("expression")

    def compile_term(self):
        
        self._xml_open("term")

        if self._peek_value() == "(":
            self._process("(")
            self.compile_expression()
            self._process(")")

        elif self._peek_value() in ("-", "~"):
            op = self._process().value
            self.compile_term()
            self.vm.write_arithmetic(UNARY_OP_MAP[op])

        elif self._peek_type() == "integerConstant":
            val = int(self._process().value)
            self.vm.write_push("constant", val)

        elif self._peek_type() == "stringConstant":
            s = self._process().value
            self.vm.write_push("constant", len(s))
            self.vm.write_call("String.new", 1)
            for ch in s:
                self.vm.write_push("constant", ord(ch))
                self.vm.write_call("String.appendChar", 2)

        elif self._peek_value() in KEYWORD_CONSTANTS:
            kw = self._process().value
            if kw == "true":
                self.vm.write_push("constant", 0)
                self.vm.write_arithmetic("not")  # -1
            elif kw in ("false", "null"):
                self.vm.write_push("constant", 0)
            elif kw == "this":
                self.vm.write_push("pointer", 0)

        elif self._peek_type() == "identifier":
            name = self._process().value

            if self._peek_value() == "[":
                sym = self.sym.lookup(name)
                self.vm.write_push(sym.segment(), sym.index)
                self._process("[")
                self.compile_expression()
                self._process("]")
                self.vm.write_arithmetic("add")
                self.vm.write_pop("pointer", 1)
                self.vm.write_push("that", 0)

            elif self._peek_value() in ("(", "."):
                self._compile_subroutine_call(name)

            else:
                sym = self.sym.lookup(name)
                self.vm.write_push(sym.segment(), sym.index)

        self._xml_close("term")

    def _compile_subroutine_call(self, name: str):
        
        n_args = 0

        if self._peek_value() == ".":
            self._process(".")
            sub_name = self._process().value

            sym = self.sym.lookup(name)
            if sym is not None:
                self.vm.write_push(sym.segment(), sym.index)
                n_args = 1
                full_name = f"{sym.type}.{sub_name}"
            else:
                full_name = f"{name}.{sub_name}"
        else:
            self.vm.write_push("pointer", 0)
            n_args = 1
            full_name = f"{self.class_name}.{name}"

        self._process("(")
        n_args += self.compile_expression_list()
        self._process(")")

        self.vm.write_call(full_name, n_args)

    def compile_expression_list(self) -> int:
        
        self._xml_open("expressionList")
        n = 0

        if self._peek_value() != ")":
            self.compile_expression()
            n = 1
            while self._peek_value() == ",":
                self._process(",")
                self.compile_expression()
                n += 1

        self._xml_close("expressionList")
        return n

