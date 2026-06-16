# Logic Gates to Compiler — nand2tetris

A bottom-up build of a computer, from individual logic gates to a working compiler for a
high-level language. Completed as the three assignments for **DA2304 — Introduction to
Computer Systems** (IIT Madras, Dept. of Data Science & AI).

The repo traces the full nand2tetris arc: **logic gates → arithmetic & memory hardware →
VM translator → Jack compiler.** Each layer's output is the next layer's input, so the
whole stack composes into one machine.

```
Jack source ──(compiler: A3)──▶ VM code ──(translator: A2)──▶ Hack assembly ──▶ runs on hardware (A1)
```

> ⚠️ **Academic-integrity note.** These are graded coursework solutions. If you are a
> current DA2304 student, do not copy this — it is shared as a portfolio reference only.

---

## Repository layout

```
.
├── A1-hardware/        # HDL: arithmetic + memory units
│   ├── *.hdl           # Bit, Register, RAM8…RAM16K, CLA chips, multiplier
│   └── report/         # theoretical report
├── A2-vm-translator/   # Python: stack-VM → Hack assembly
│   └── src/
└── A3-jack-compiler/   # Python: Jack → VM code
    ├── src/
    └── jack/           # sample Jack programs (incl. 2D convolution)
```

---

## A1 — Hardware in HDL

Built the arithmetic and memory components of the Hack computer from 2-input gates up.

**Arithmetic**
- **Carry-lookahead adder hierarchy** — `CLA2 → CLA4 → CLA16`. The same 4-gate
  group-lookahead pattern (`C = G | (P·Cin)`, group-generate, group-propagate) recurses
  at every level, giving O(log n) carry propagation instead of the O(n) ripple of a naïve
  adder.
- **Multiplier** — a Wallace-tree design: 16 partial products (each a single bit of `b`
  broadcast across `a`, pre-shifted to its bit position via `ShiftLeft1`), reduced with
  **carry-save adders (`CSA16`)** and a final `Add16`. Lower 16 bits kept; two's-complement
  correct.

**Memory**
- `Bit` (DFF + load mux) → `Register` (16 Bits) → **`RAM8 → RAM64 → RAM512 → RAM4K → RAM16K`**.
  Each tier is 8× the one below (4× at the top), addressed by splitting the address bus into
  a block-select field (DMux/Mux tree) and a within-block field.

**Report** — covers the design trade-offs: ripple vs. lookahead carry, Wallace-tree
reduction, and why large memory blocks (RAM4K) beat many tiny ones (RAM8) on gate count,
hierarchy depth, and critical-path delay.

### Run
Open the chips in the nand2tetris **Hardware Simulator**, loading bottom-up
(`Bit` first, `RAM16K`/`Multiplier` last), and run the supplied `.tst` scripts.

---

## A2 — VM Translator (Python)

Translates stack-based **VM code** into **Hack assembly**, following the standard
two-module design:

- **`Parser`** — reads a `.vm` file, strips comments/whitespace, and classifies each line
  (arithmetic, push/pop, label, goto, function, call, return).
- **`CodeWriter`** — emits the corresponding Hack assembly: stack arithmetic/logic,
  the eight memory segments (`local`, `argument`, `this`, `that`, `temp`, `pointer`,
  `static`, `constant`), and the function-calling protocol (frames, `call`, `return`).

### Run
```bash
cd A2-vm-translator/src
python VMTranslator.py path/to/input.vm      # or a directory of .vm files
# produces path/to/input.asm
```
Feed the `.asm` into the CPU Emulator to execute.

---

## A3 — Jack Compiler (Python)

A full front-end compiler for **Jack** (an object-oriented, Java-flavoured language),
emitting VM code that A2 can consume.

- **`JackTokenizer`** — lexes source into a token stream (keywords, symbols, integer/string
  constants, identifiers); also emits the token XML.
- **`CompilationEngine`** — recursive-descent parser over Jack's grammar; drives parse-tree
  XML output and code generation in one pass.
- **`SymbolTable`** — tracks the four variable kinds (`static`, `field`, `arg`, `var`) across
  class and subroutine scopes, resolving each identifier to its segment and index.
- **`VMWriter`** — emits VM commands (push/pop, arithmetic, `call`, `function`, `return`),
  handling constructors, methods (with `this`/`pointer`), arrays, and strings.

Includes a sample **2D-convolution** program (`Conv.jack`, `Main.jack`) exercised end-to-end.

### Run
```bash
cd A3-jack-compiler/src
python JackCompiler.py ../jack/                # compiles every .jack in the folder
# emits, per source file:  *T.xml (tokens), *.xml (parse tree), *.vm (VM code)
```
Pipe the `.vm` output through the A2 translator to get assembly.

---

## Tech

- **HDL** (nand2tetris Hardware Description Language) — A1
- **Python 3.10+** — A2, A3 (no external dependencies)
- nand2tetris **Hardware Simulator** / **CPU Emulator** for testing

## What this demonstrates

Designing and verifying digital logic, mapping carry-propagation and partial-product
algorithms onto gates, and building a clean two/four-module translator and compiler with a
recursive-descent parser and scoped symbol resolution — i.e. the full path from a NAND gate
to a running high-level program.