// ALU_regression.tst — Regression test for modified ALU
// Tests all 18 standard ops + MUL to verify no interference.

load ALU.hdl,
output-file ALUregression.out,
compare-to ALUregression.cmp,
output-list x%D1.6.1 y%D1.6.1 zx%B1.1.1 nx%B1.1.1 zy%B1.1.1 ny%B1.1.1 f%B1.1.1 no%B1.1.1 out%D1.6.1 zr%B1.1.1 ng%B1.1.1;

// ── 0  (101010) ──
set x 0, set y 0, set zx 1, set nx 0, set zy 1, set ny 0, set f 1, set no 0, eval, output;
set x 0, set y -1, set zx 1, set nx 0, set zy 1, set ny 0, set f 1, set no 0, eval, output;
set x 17, set y 3, set zx 1, set nx 0, set zy 1, set ny 0, set f 1, set no 0, eval, output;
set x -1, set y -1, set zx 1, set nx 0, set zy 1, set ny 0, set f 1, set no 0, eval, output;
set x 12345, set y 6789, set zx 1, set nx 0, set zy 1, set ny 0, set f 1, set no 0, eval, output;
set x -100, set y 50, set zx 1, set nx 0, set zy 1, set ny 0, set f 1, set no 0, eval, output;
set x 1, set y 1, set zx 1, set nx 0, set zy 1, set ny 0, set f 1, set no 0, eval, output;
set x 255, set y 4, set zx 1, set nx 0, set zy 1, set ny 0, set f 1, set no 0, eval, output;

// ── 1  (111111) ──
set x 0, set y 0, set zx 1, set nx 1, set zy 1, set ny 1, set f 1, set no 1, eval, output;
set x 0, set y -1, set zx 1, set nx 1, set zy 1, set ny 1, set f 1, set no 1, eval, output;
set x 17, set y 3, set zx 1, set nx 1, set zy 1, set ny 1, set f 1, set no 1, eval, output;
set x -1, set y -1, set zx 1, set nx 1, set zy 1, set ny 1, set f 1, set no 1, eval, output;
set x 12345, set y 6789, set zx 1, set nx 1, set zy 1, set ny 1, set f 1, set no 1, eval, output;
set x -100, set y 50, set zx 1, set nx 1, set zy 1, set ny 1, set f 1, set no 1, eval, output;
set x 1, set y 1, set zx 1, set nx 1, set zy 1, set ny 1, set f 1, set no 1, eval, output;
set x 255, set y 4, set zx 1, set nx 1, set zy 1, set ny 1, set f 1, set no 1, eval, output;

// ── -1  (111010) ──
set x 0, set y 0, set zx 1, set nx 1, set zy 1, set ny 0, set f 1, set no 0, eval, output;
set x 0, set y -1, set zx 1, set nx 1, set zy 1, set ny 0, set f 1, set no 0, eval, output;
set x 17, set y 3, set zx 1, set nx 1, set zy 1, set ny 0, set f 1, set no 0, eval, output;
set x -1, set y -1, set zx 1, set nx 1, set zy 1, set ny 0, set f 1, set no 0, eval, output;
set x 12345, set y 6789, set zx 1, set nx 1, set zy 1, set ny 0, set f 1, set no 0, eval, output;
set x -100, set y 50, set zx 1, set nx 1, set zy 1, set ny 0, set f 1, set no 0, eval, output;
set x 1, set y 1, set zx 1, set nx 1, set zy 1, set ny 0, set f 1, set no 0, eval, output;
set x 255, set y 4, set zx 1, set nx 1, set zy 1, set ny 0, set f 1, set no 0, eval, output;

// ── x  (001100) ──
set x 0, set y 0, set zx 0, set nx 0, set zy 1, set ny 1, set f 0, set no 0, eval, output;
set x 0, set y -1, set zx 0, set nx 0, set zy 1, set ny 1, set f 0, set no 0, eval, output;
set x 17, set y 3, set zx 0, set nx 0, set zy 1, set ny 1, set f 0, set no 0, eval, output;
set x -1, set y -1, set zx 0, set nx 0, set zy 1, set ny 1, set f 0, set no 0, eval, output;
set x 12345, set y 6789, set zx 0, set nx 0, set zy 1, set ny 1, set f 0, set no 0, eval, output;
set x -100, set y 50, set zx 0, set nx 0, set zy 1, set ny 1, set f 0, set no 0, eval, output;
set x 1, set y 1, set zx 0, set nx 0, set zy 1, set ny 1, set f 0, set no 0, eval, output;
set x 255, set y 4, set zx 0, set nx 0, set zy 1, set ny 1, set f 0, set no 0, eval, output;

// ── y  (110000) ──
set x 0, set y 0, set zx 1, set nx 1, set zy 0, set ny 0, set f 0, set no 0, eval, output;
set x 0, set y -1, set zx 1, set nx 1, set zy 0, set ny 0, set f 0, set no 0, eval, output;
set x 17, set y 3, set zx 1, set nx 1, set zy 0, set ny 0, set f 0, set no 0, eval, output;
set x -1, set y -1, set zx 1, set nx 1, set zy 0, set ny 0, set f 0, set no 0, eval, output;
set x 12345, set y 6789, set zx 1, set nx 1, set zy 0, set ny 0, set f 0, set no 0, eval, output;
set x -100, set y 50, set zx 1, set nx 1, set zy 0, set ny 0, set f 0, set no 0, eval, output;
set x 1, set y 1, set zx 1, set nx 1, set zy 0, set ny 0, set f 0, set no 0, eval, output;
set x 255, set y 4, set zx 1, set nx 1, set zy 0, set ny 0, set f 0, set no 0, eval, output;

// ── !x  (001101) ──
set x 0, set y 0, set zx 0, set nx 0, set zy 1, set ny 1, set f 0, set no 1, eval, output;
set x 0, set y -1, set zx 0, set nx 0, set zy 1, set ny 1, set f 0, set no 1, eval, output;
set x 17, set y 3, set zx 0, set nx 0, set zy 1, set ny 1, set f 0, set no 1, eval, output;
set x -1, set y -1, set zx 0, set nx 0, set zy 1, set ny 1, set f 0, set no 1, eval, output;
set x 12345, set y 6789, set zx 0, set nx 0, set zy 1, set ny 1, set f 0, set no 1, eval, output;
set x -100, set y 50, set zx 0, set nx 0, set zy 1, set ny 1, set f 0, set no 1, eval, output;
set x 1, set y 1, set zx 0, set nx 0, set zy 1, set ny 1, set f 0, set no 1, eval, output;
set x 255, set y 4, set zx 0, set nx 0, set zy 1, set ny 1, set f 0, set no 1, eval, output;

// ── !y  (110001) ──
set x 0, set y 0, set zx 1, set nx 1, set zy 0, set ny 0, set f 0, set no 1, eval, output;
set x 0, set y -1, set zx 1, set nx 1, set zy 0, set ny 0, set f 0, set no 1, eval, output;
set x 17, set y 3, set zx 1, set nx 1, set zy 0, set ny 0, set f 0, set no 1, eval, output;
set x -1, set y -1, set zx 1, set nx 1, set zy 0, set ny 0, set f 0, set no 1, eval, output;
set x 12345, set y 6789, set zx 1, set nx 1, set zy 0, set ny 0, set f 0, set no 1, eval, output;
set x -100, set y 50, set zx 1, set nx 1, set zy 0, set ny 0, set f 0, set no 1, eval, output;
set x 1, set y 1, set zx 1, set nx 1, set zy 0, set ny 0, set f 0, set no 1, eval, output;
set x 255, set y 4, set zx 1, set nx 1, set zy 0, set ny 0, set f 0, set no 1, eval, output;

// ── -x  (001111) ──
set x 0, set y 0, set zx 0, set nx 0, set zy 1, set ny 1, set f 1, set no 1, eval, output;
set x 0, set y -1, set zx 0, set nx 0, set zy 1, set ny 1, set f 1, set no 1, eval, output;
set x 17, set y 3, set zx 0, set nx 0, set zy 1, set ny 1, set f 1, set no 1, eval, output;
set x -1, set y -1, set zx 0, set nx 0, set zy 1, set ny 1, set f 1, set no 1, eval, output;
set x 12345, set y 6789, set zx 0, set nx 0, set zy 1, set ny 1, set f 1, set no 1, eval, output;
set x -100, set y 50, set zx 0, set nx 0, set zy 1, set ny 1, set f 1, set no 1, eval, output;
set x 1, set y 1, set zx 0, set nx 0, set zy 1, set ny 1, set f 1, set no 1, eval, output;
set x 255, set y 4, set zx 0, set nx 0, set zy 1, set ny 1, set f 1, set no 1, eval, output;

// ── -y  (110011) ──
set x 0, set y 0, set zx 1, set nx 1, set zy 0, set ny 0, set f 1, set no 1, eval, output;
set x 0, set y -1, set zx 1, set nx 1, set zy 0, set ny 0, set f 1, set no 1, eval, output;
set x 17, set y 3, set zx 1, set nx 1, set zy 0, set ny 0, set f 1, set no 1, eval, output;
set x -1, set y -1, set zx 1, set nx 1, set zy 0, set ny 0, set f 1, set no 1, eval, output;
set x 12345, set y 6789, set zx 1, set nx 1, set zy 0, set ny 0, set f 1, set no 1, eval, output;
set x -100, set y 50, set zx 1, set nx 1, set zy 0, set ny 0, set f 1, set no 1, eval, output;
set x 1, set y 1, set zx 1, set nx 1, set zy 0, set ny 0, set f 1, set no 1, eval, output;
set x 255, set y 4, set zx 1, set nx 1, set zy 0, set ny 0, set f 1, set no 1, eval, output;

// ── x+1  (011111) ──
set x 0, set y 0, set zx 0, set nx 1, set zy 1, set ny 1, set f 1, set no 1, eval, output;
set x 0, set y -1, set zx 0, set nx 1, set zy 1, set ny 1, set f 1, set no 1, eval, output;
set x 17, set y 3, set zx 0, set nx 1, set zy 1, set ny 1, set f 1, set no 1, eval, output;
set x -1, set y -1, set zx 0, set nx 1, set zy 1, set ny 1, set f 1, set no 1, eval, output;
set x 12345, set y 6789, set zx 0, set nx 1, set zy 1, set ny 1, set f 1, set no 1, eval, output;
set x -100, set y 50, set zx 0, set nx 1, set zy 1, set ny 1, set f 1, set no 1, eval, output;
set x 1, set y 1, set zx 0, set nx 1, set zy 1, set ny 1, set f 1, set no 1, eval, output;
set x 255, set y 4, set zx 0, set nx 1, set zy 1, set ny 1, set f 1, set no 1, eval, output;

// ── y+1  (110111) ──
set x 0, set y 0, set zx 1, set nx 1, set zy 0, set ny 1, set f 1, set no 1, eval, output;
set x 0, set y -1, set zx 1, set nx 1, set zy 0, set ny 1, set f 1, set no 1, eval, output;
set x 17, set y 3, set zx 1, set nx 1, set zy 0, set ny 1, set f 1, set no 1, eval, output;
set x -1, set y -1, set zx 1, set nx 1, set zy 0, set ny 1, set f 1, set no 1, eval, output;
set x 12345, set y 6789, set zx 1, set nx 1, set zy 0, set ny 1, set f 1, set no 1, eval, output;
set x -100, set y 50, set zx 1, set nx 1, set zy 0, set ny 1, set f 1, set no 1, eval, output;
set x 1, set y 1, set zx 1, set nx 1, set zy 0, set ny 1, set f 1, set no 1, eval, output;
set x 255, set y 4, set zx 1, set nx 1, set zy 0, set ny 1, set f 1, set no 1, eval, output;

// ── x-1  (001110) ──
set x 0, set y 0, set zx 0, set nx 0, set zy 1, set ny 1, set f 1, set no 0, eval, output;
set x 0, set y -1, set zx 0, set nx 0, set zy 1, set ny 1, set f 1, set no 0, eval, output;
set x 17, set y 3, set zx 0, set nx 0, set zy 1, set ny 1, set f 1, set no 0, eval, output;
set x -1, set y -1, set zx 0, set nx 0, set zy 1, set ny 1, set f 1, set no 0, eval, output;
set x 12345, set y 6789, set zx 0, set nx 0, set zy 1, set ny 1, set f 1, set no 0, eval, output;
set x -100, set y 50, set zx 0, set nx 0, set zy 1, set ny 1, set f 1, set no 0, eval, output;
set x 1, set y 1, set zx 0, set nx 0, set zy 1, set ny 1, set f 1, set no 0, eval, output;
set x 255, set y 4, set zx 0, set nx 0, set zy 1, set ny 1, set f 1, set no 0, eval, output;

// ── y-1  (110010) ──
set x 0, set y 0, set zx 1, set nx 1, set zy 0, set ny 0, set f 1, set no 0, eval, output;
set x 0, set y -1, set zx 1, set nx 1, set zy 0, set ny 0, set f 1, set no 0, eval, output;
set x 17, set y 3, set zx 1, set nx 1, set zy 0, set ny 0, set f 1, set no 0, eval, output;
set x -1, set y -1, set zx 1, set nx 1, set zy 0, set ny 0, set f 1, set no 0, eval, output;
set x 12345, set y 6789, set zx 1, set nx 1, set zy 0, set ny 0, set f 1, set no 0, eval, output;
set x -100, set y 50, set zx 1, set nx 1, set zy 0, set ny 0, set f 1, set no 0, eval, output;
set x 1, set y 1, set zx 1, set nx 1, set zy 0, set ny 0, set f 1, set no 0, eval, output;
set x 255, set y 4, set zx 1, set nx 1, set zy 0, set ny 0, set f 1, set no 0, eval, output;

// ── x+y  (000010) ──
set x 0, set y 0, set zx 0, set nx 0, set zy 0, set ny 0, set f 1, set no 0, eval, output;
set x 0, set y -1, set zx 0, set nx 0, set zy 0, set ny 0, set f 1, set no 0, eval, output;
set x 17, set y 3, set zx 0, set nx 0, set zy 0, set ny 0, set f 1, set no 0, eval, output;
set x -1, set y -1, set zx 0, set nx 0, set zy 0, set ny 0, set f 1, set no 0, eval, output;
set x 12345, set y 6789, set zx 0, set nx 0, set zy 0, set ny 0, set f 1, set no 0, eval, output;
set x -100, set y 50, set zx 0, set nx 0, set zy 0, set ny 0, set f 1, set no 0, eval, output;
set x 1, set y 1, set zx 0, set nx 0, set zy 0, set ny 0, set f 1, set no 0, eval, output;
set x 255, set y 4, set zx 0, set nx 0, set zy 0, set ny 0, set f 1, set no 0, eval, output;

// ── x-y  (010011) ──
set x 0, set y 0, set zx 0, set nx 1, set zy 0, set ny 0, set f 1, set no 1, eval, output;
set x 0, set y -1, set zx 0, set nx 1, set zy 0, set ny 0, set f 1, set no 1, eval, output;
set x 17, set y 3, set zx 0, set nx 1, set zy 0, set ny 0, set f 1, set no 1, eval, output;
set x -1, set y -1, set zx 0, set nx 1, set zy 0, set ny 0, set f 1, set no 1, eval, output;
set x 12345, set y 6789, set zx 0, set nx 1, set zy 0, set ny 0, set f 1, set no 1, eval, output;
set x -100, set y 50, set zx 0, set nx 1, set zy 0, set ny 0, set f 1, set no 1, eval, output;
set x 1, set y 1, set zx 0, set nx 1, set zy 0, set ny 0, set f 1, set no 1, eval, output;
set x 255, set y 4, set zx 0, set nx 1, set zy 0, set ny 0, set f 1, set no 1, eval, output;

// ── y-x  (000111) ──
set x 0, set y 0, set zx 0, set nx 0, set zy 0, set ny 1, set f 1, set no 1, eval, output;
set x 0, set y -1, set zx 0, set nx 0, set zy 0, set ny 1, set f 1, set no 1, eval, output;
set x 17, set y 3, set zx 0, set nx 0, set zy 0, set ny 1, set f 1, set no 1, eval, output;
set x -1, set y -1, set zx 0, set nx 0, set zy 0, set ny 1, set f 1, set no 1, eval, output;
set x 12345, set y 6789, set zx 0, set nx 0, set zy 0, set ny 1, set f 1, set no 1, eval, output;
set x -100, set y 50, set zx 0, set nx 0, set zy 0, set ny 1, set f 1, set no 1, eval, output;
set x 1, set y 1, set zx 0, set nx 0, set zy 0, set ny 1, set f 1, set no 1, eval, output;
set x 255, set y 4, set zx 0, set nx 0, set zy 0, set ny 1, set f 1, set no 1, eval, output;

// ── x&y  (000000) ──
set x 0, set y 0, set zx 0, set nx 0, set zy 0, set ny 0, set f 0, set no 0, eval, output;
set x 0, set y -1, set zx 0, set nx 0, set zy 0, set ny 0, set f 0, set no 0, eval, output;
set x 17, set y 3, set zx 0, set nx 0, set zy 0, set ny 0, set f 0, set no 0, eval, output;
set x -1, set y -1, set zx 0, set nx 0, set zy 0, set ny 0, set f 0, set no 0, eval, output;
set x 12345, set y 6789, set zx 0, set nx 0, set zy 0, set ny 0, set f 0, set no 0, eval, output;
set x -100, set y 50, set zx 0, set nx 0, set zy 0, set ny 0, set f 0, set no 0, eval, output;
set x 1, set y 1, set zx 0, set nx 0, set zy 0, set ny 0, set f 0, set no 0, eval, output;
set x 255, set y 4, set zx 0, set nx 0, set zy 0, set ny 0, set f 0, set no 0, eval, output;

// ── x|y  (010101) ──
set x 0, set y 0, set zx 0, set nx 1, set zy 0, set ny 1, set f 0, set no 1, eval, output;
set x 0, set y -1, set zx 0, set nx 1, set zy 0, set ny 1, set f 0, set no 1, eval, output;
set x 17, set y 3, set zx 0, set nx 1, set zy 0, set ny 1, set f 0, set no 1, eval, output;
set x -1, set y -1, set zx 0, set nx 1, set zy 0, set ny 1, set f 0, set no 1, eval, output;
set x 12345, set y 6789, set zx 0, set nx 1, set zy 0, set ny 1, set f 0, set no 1, eval, output;
set x -100, set y 50, set zx 0, set nx 1, set zy 0, set ny 1, set f 0, set no 1, eval, output;
set x 1, set y 1, set zx 0, set nx 1, set zy 0, set ny 1, set f 0, set no 1, eval, output;
set x 255, set y 4, set zx 0, set nx 1, set zy 0, set ny 1, set f 0, set no 1, eval, output;

// ── x*y  (000001) ──
set x 0, set y 0, set zx 0, set nx 0, set zy 0, set ny 0, set f 0, set no 1, eval, output;
set x 0, set y -1, set zx 0, set nx 0, set zy 0, set ny 0, set f 0, set no 1, eval, output;
set x 17, set y 3, set zx 0, set nx 0, set zy 0, set ny 0, set f 0, set no 1, eval, output;
set x -1, set y -1, set zx 0, set nx 0, set zy 0, set ny 0, set f 0, set no 1, eval, output;
set x 12345, set y 6789, set zx 0, set nx 0, set zy 0, set ny 0, set f 0, set no 1, eval, output;
set x -100, set y 50, set zx 0, set nx 0, set zy 0, set ny 0, set f 0, set no 1, eval, output;
set x 1, set y 1, set zx 0, set nx 0, set zy 0, set ny 0, set f 0, set no 1, eval, output;
set x 255, set y 4, set zx 0, set nx 0, set zy 0, set ny 0, set f 0, set no 1, eval, output;

