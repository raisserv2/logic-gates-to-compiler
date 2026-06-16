class Symbol:
    def __init__(self, name: str, stype: str, kind: str, index: int):
        self.name = name
        self.type = stype
        self.kind = kind
        self.index = index

    def segment(self) -> str:
        return {
            "static": "static",
            "field": "this",
            "argument": "argument",
            "var": "local",
        }[self.kind]
class SymbolTable:
    def __init__(self):
        self.class_scope = {}
        self.sub_scope = {}
        self._counts = {
            "static": 0, "field": 0, "argument": 0, "var": 0,
        }

    def start_subroutine(self):
        self.sub_scope = {}
        self._counts["argument"] = 0
        self._counts["var"] = 0

    def define(self, name: str, stype: str, kind: str):
        idx = self._counts[kind]
        sym = Symbol(name, stype, kind, idx)
        self._counts[kind] = idx + 1

        if kind in ("static", "field"):
            self.class_scope[name] = sym
        else:
            self.sub_scope[name] = sym

    def lookup(self, name: str):
        if name in self.sub_scope:
            return self.sub_scope[name]
        if name in self.class_scope:
            return self.class_scope[name]
        return None

    def var_count(self, kind: str) -> int:
        return self._counts.get(kind, 0)
