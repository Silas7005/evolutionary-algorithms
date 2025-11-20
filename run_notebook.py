"""Run a Jupyter notebook programmatically using nbclient.

Usage:
  python run_notebook.py --input nsga2_load_balancing.ipynb --output nsga2_run.ipynb [--timeout 600] [--fast]

Options:
  --fast    Inject a small cell at the top to reduce POP_SIZE and NGEN for quick test runs.

This script executes the notebook with the current Python environment (the .venv when you run it from there).
"""
import argparse
import nbformat
from nbclient import NotebookClient
from nbformat import v4
from pathlib import Path
import sys


def run_notebook(input_path: Path, output_path: Path, timeout: int = 600, fast: bool = False):
    nb = nbformat.read(str(input_path), as_version=4)

    if fast:
        # Inject a small parameter cell at the top to speed up execution for tests.
        param_code = "# Injected by run_notebook.py for fast testing\nPOP_SIZE = 20\nNGEN = 5\nprint('Running in FAST mode: POP_SIZE=', POP_SIZE, 'NGEN=', NGEN)\n"
        param_cell = v4.new_code_cell(source=param_code)
        nb.cells.insert(0, param_cell)

    # Use a concrete kernel name so nbclient can start the correct kernel in the venv.
    # 'python3' usually maps to the active Python environment; running this script
    # from the project's .venv will use that interpreter.
    client = NotebookClient(nb, timeout=timeout, kernel_name='python3')
    print(f"Executing notebook {input_path} (timeout={timeout}s)...")
    try:
        client.execute()
    except Exception as e:
        print("Notebook execution failed:", e)
        # Still write the partially executed notebook for debugging
        nbformat.write(nb, str(output_path))
        raise

    nbformat.write(nb, str(output_path))
    print(f"Execution finished. Saved executed notebook to: {output_path}")

    # Report common output files if present
    proj_dir = input_path.parent
    for name in ("pareto_plot.html", "pareto_plot.png", "pareto_vals.csv"):
        p = proj_dir / name
        if p.exists():
            print(f"Found output: {p}")


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--input', '-i', required=True, help='Input notebook file')
    parser.add_argument('--output', '-o', required=False, help='Output executed notebook file')
    parser.add_argument('--timeout', type=int, default=600)
    parser.add_argument('--fast', action='store_true', help='Run a faster test by injecting smaller POP_SIZE/NGEN')

    args = parser.parse_args()
    input_path = Path(args.input)
    if not input_path.exists():
        print('Input notebook not found:', input_path)
        sys.exit(2)
    output_path = Path(args.output) if args.output else input_path.with_name(input_path.stem + '_executed.ipynb')

    try:
        run_notebook(input_path, output_path, timeout=args.timeout, fast=args.fast)
    except Exception as exc:
        print('Error running notebook:', exc)
        sys.exit(1)
    sys.exit(0)
