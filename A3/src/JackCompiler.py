import sys
import os
from JackTokenizer import JackTokenizer
from CompilationEngine import CompilationEngine


def compile_file(jack_path: str, output_dir: str):
    basename = os.path.splitext(os.path.basename(jack_path))[0]
    print(f"\n-- Compiling {basename}.jack")
    
    tokenizer = JackTokenizer(jack_path)
    tokens = tokenizer.tokenize()
    tokenizer.write_xml(output_dir)
    
    engine = CompilationEngine(tokens, basename, output_dir)
    engine.compile_class()
    
    print(f"  [vm]  {os.path.join(output_dir, basename + '.vm')}")


def main():
    if len(sys.argv) != 2:
        print("Usage: python JackCompiler.py <file.jack | directory>")
        sys.exit(1)

    path = sys.argv[1].rstrip("/\\")

    if os.path.isdir(path):
        jack_files = sorted([
            os.path.join(path, f)
            for f in os.listdir(path) if f.endswith(".jack")
        ])
        output_dir = os.path.join(os.path.dirname(path), "out")
    elif path.endswith(".jack") and os.path.isfile(path):
        jack_files = [path]
        output_dir = os.path.join(os.path.dirname(path) or ".", "out")
    else:
        print(f"Invalid input: {path}")
        sys.exit(1)

    os.makedirs(output_dir, exist_ok=True)

    for jf in jack_files:
        compile_file(jf, output_dir)

    print(f"\nAll done. Output in {output_dir}/")


if __name__ == "__main__":
    main()
