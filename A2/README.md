# Hack VM Translator

## Structure

```
src/
  main.py         this is the entry point
  parser.py       this  tokenises & classifies VM commands
  code_writer.py  this emits Hack assembly

vm_programs/
  SimpleAdd.vm    this is a basic push/add test
  StackTest.vm    this provides full arithmetic & logical coverage
  MAC.vm          this is a Matrix Multiply-Accumulate 
```

## How to Run

```bash
#to translate a single .vm file
python src/main.py vm_programs/SimpleAdd.vm
#this will produce vm_programs/SimpleAdd.asm

#to translate an entire directory 
python src/main.py vm_programs/
#this will produce vm_programs/vm_programs.asm
```

Python 3.10+ required. No third-party dependencies.

## Supported VM Commands

| Category        | Commands                                      |
|-----------------|-----------------------------------------------|
| Arithmetic/Logic| add sub neg eq gt lt and or not               |
| Memory Access   | push/pop ; constant local argument this that static temp pointer |
| Program Flow    | label goto if-goto                            |
| Functions       | function call return                          |

## Memory Segment Mapping

| VM Segment | Hack RAM                        |
|------------|---------------------------------|
| constant   | literal (push only)             |
| local      | RAM[LCL + i]                    |
| argument   | RAM[ARG + i]                    |
| this       | RAM[THIS + i]                   |
| that       | RAM[THAT + i]                   |
| static     | RAM[filename.i]                 |
| temp       | RAM[5 + i]                      |
| pointer    | THIS (i=0) / THAT (i=1)         |

## On the design

- I have written `code_writer.py` to emit  a bootstrap block (SP=256, `call Sys.init`) at the
  top of every output for multi-file or directory translation.
- Comparison commands (`eq`, `gt`, `lt`) use unique auto-generated labels to
  avoid collisions across multiple translated files.
- R13 is used as a scratchpad register for `pop` target-address computation;
  R14/R15 for `return` frame or address storage.
