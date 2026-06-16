

import re
import os

KEYWORDS = {
    "class", "constructor", "function", "method", "field", "static",
    "var", "int", "char", "boolean", "void", "true", "false", "null",
    "this", "let", "do", "if", "else", "while", "return",
}

SYMBOLS = set("{}()[].,;+-*/&|<>=~")

XML_ESC = {"<": "&lt;", ">": "&gt;", "&": "&amp;", '"': "&quot;"}


class Token:
    
    def __init__(self, ttype: str, value: str):
        self.type = ttype    # keyword | symbol | integerConstant | stringConstant | identifier
        self.value = value

    def __repr__(self):
        return f"Token({self.type}, {self.value!r})"

    def xml_value(self) -> str:
        
        if self.type == "symbol":
            return XML_ESC.get(self.value, self.value)
        if self.type == "stringConstant":
            return self.value  # already stripped of quotes
        return self.value


class JackTokenizer:
    def __init__(self, filepath: str):
        self.filepath = filepath
        with open(filepath, "r") as f:
            self.source = f.read()
        self.tokens: list[Token] = []

    def _strip_comments(self, src: str) -> str:
        
        result = []
        i = 0
        n = len(src)
        in_string = False

        while i < n:
            if in_string:
                result.append(src[i])
                if src[i] == '"':
                    in_string = False
                i += 1
                continue

            if src[i] == '"':
                in_string = True
                result.append(src[i])
                i += 1
                continue

            if i + 1 < n and src[i] == '/' and src[i + 1] == '/':
                while i < n and src[i] != '\n':
                    i += 1
                continue

            if i + 1 < n and src[i] == '/' and src[i + 1] == '*':
                i += 2
                while i + 1 < n and not (src[i] == '*' and src[i + 1] == '/'):
                    i += 1
                i += 2  # skip closing */
                result.append(' ')  # replace comment with space
                continue

            result.append(src[i])
            i += 1

        return ''.join(result)

    def tokenize(self) -> list[Token]:
        clean = self._strip_comments(self.source)
        i = 0
        n = len(clean)
        self.tokens = []

        while i < n:
            ch = clean[i]

            if ch in ' \t\n\r':
                i += 1
                continue

            if ch in SYMBOLS:
                self.tokens.append(Token("symbol", ch))
                i += 1
                continue

            if ch.isdigit():
                j = i
                while j < n and clean[j].isdigit():
                    j += 1
                self.tokens.append(Token("integerConstant", clean[i:j]))
                i = j
                continue

            if ch == '"':
                j = i + 1
                while j < n and clean[j] != '"':
                    j += 1
                self.tokens.append(Token("stringConstant", clean[i + 1:j]))
                i = j + 1
                continue

            if ch.isalpha() or ch == '_':
                j = i
                while j < n and (clean[j].isalnum() or clean[j] == '_'):
                    j += 1
                word = clean[i:j]
                if word in KEYWORDS:
                    self.tokens.append(Token("keyword", word))
                else:
                    self.tokens.append(Token("identifier", word))
                i = j
                continue

            i += 1

        return self.tokens

    def write_xml(self, output_dir: str):
        
        basename = os.path.splitext(os.path.basename(self.filepath))[0]
        outpath = os.path.join(output_dir, f"{basename}T.xml")

        lines = ["<tokens>"]
        for tok in self.tokens:
            lines.append(f"<{tok.type}> {tok.xml_value()} </{tok.type}>")
        lines.append("</tokens>")

        with open(outpath, "w") as f:
            f.write("\n".join(lines) + "\n")

        print(f"  [tok] {outpath}")
        return outpath

