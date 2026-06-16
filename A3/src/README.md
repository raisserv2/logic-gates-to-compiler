# Jack Compiler

## How to Use

```bash
python JackCompiler.py ../jack/
```

Output files in `out/`:
- ConvT.xml, MainT.xml - tokenized source
- Conv.xml, Main.xml - parse trees  
- Conv.vm, Main.vm - VM code

## Modules

- JackTokenizer.py - lexical analysis
- CompilationEngine.py - parser and code gen
- SymbolTable.py - symbol table management
- VMWriter.py - VM code output
- JackCompiler.py - entry point

Requirements: Python 3.10+
