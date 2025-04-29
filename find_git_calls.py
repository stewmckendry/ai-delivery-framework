import ast

def find_repo_calls(filename):
    with open(filename, "r", encoding="utf-8") as f:
        tree = ast.parse(f.read(), filename=filename)

    results = []

    class RepoCallVisitor(ast.NodeVisitor):
        def __init__(self):
            self.current_function = None

        def visit_FunctionDef(self, node):
            prev_function = self.current_function
            self.current_function = node.name
            self.generic_visit(node)
            self.current_function = prev_function

        def visit_AsyncFunctionDef(self, node):
            self.visit_FunctionDef(node)  # Same handling for async defs

        def visit_Call(self, node):
            if isinstance(node.func, ast.Attribute):
                if node.func.attr in ("create_file", "update_file"):
                    if isinstance(node.func.value, ast.Name) and node.func.value.id == "repo":
                        results.append((self.current_function, node.lineno, node.func.attr))
            self.generic_visit(node)

    RepoCallVisitor().visit(tree)

    return results

# --- Usage ---
if __name__ == "__main__":
    matches = find_repo_calls("main.py")
    for func_name, lineno, method in matches:
        print(f"Function: {func_name} | Line: {lineno} | Call: repo.{method}()")
