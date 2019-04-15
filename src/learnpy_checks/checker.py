import ast


class ScriptVisitor(ast.NodeVisitor):
    def __init__(self):
        self.names = []
        self.assigns = []
        self.calls = []

    def visit_Name(self, node):
        self.generic_visit(node)
        self.set_names(node)

    def set_names(self, node):
        self.names.append(node)

    def get_names(self):
        return self.names

    def visit_Assign(self, node):
        self.generic_visit(node)
        self.set_assigns(node)

    def set_assigns(self, node):
        self.assigns.append(node)

    def get_assigns(self):
        return self.assigns

    def visit_Call(self, node):
        self.generic_visit(node)
        self.set_calls(node)

    def set_calls(self, node):
        self.calls.append(node)

    def get_calls(self):
        return self.calls
