import ast
import os
import sys

MAX_LINES = 100


def check_docstrings(filename):
    with open(filename, "r", encoding="utf-8") as f:
        tree = ast.parse(f.read())

    missing = []

    for node in ast.walk(tree):
        if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)):
            if ast.get_docstring(node) is None:
                missing.append(node.name)

    return missing

S
def count_lines(filename):
    with open(filename, "r", encoding="utf-8") as f:
        return len(f.readlines())


errors = []

for root, dirs, files in os.walk("."):
    if ".git" in root:
        continue

    for file in files:
        if file.endswith(".py"):

            path = os.path.join(root, file)

            line_count = count_lines(path)

            if line_count > MAX_LINES:
                errors.append(
                    f"{path}: exceeds {MAX_LINES} lines ({line_count})"
                )

            missing_docs = check_docstrings(path)

            for func in missing_docs:
                errors.append(
                    f"{path}: function '{func}' missing docstring"
                )

if errors:
    print("\n".join(errors))
    sys.exit(1)

print("All quality checks passed.")
