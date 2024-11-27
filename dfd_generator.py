# import ast
# import networkx as nx
# from matplotlib import pyplot as plt

# class DFDBuilder(ast.NodeVisitor):
#     def __init__(self):
#         self.graph = nx.DiGraph()

#     def visit_FunctionDef(self, node):
#         function_name = f"Function: {node.name}"
#         self.graph.add_node(function_name)
        
#         # Add edges for function arguments
#         for arg in node.args.args:
#             arg_name = f"Arg: {arg.arg}"
#             self.graph.add_edge(arg_name, function_name)
        
#         # Visit function body
#         self.generic_visit(node)

#     def visit_Assign(self, node):
#         targets = [t.id for t in node.targets if isinstance(t, ast.Name)]
#         if hasattr(node.value, 'id'):
#             for target in targets:
#                 self.graph.add_edge(node.value.id, target)
#         self.generic_visit(node)

#     def build_dfd(self, source_code):
#         tree = ast.parse(source_code)
#         self.visit(tree)

# def generate_dfd(file_path):
#     with open(file_path, 'r') as f:
#         source_code = f.read()
    
#     builder = DFDBuilder()
#     builder.build_dfd(source_code)
    
#     # Improve layout for better clarity
#     pos = nx.spring_layout(builder.graph, seed=42)
    
#     # Draw the DFD graph
#     plt.figure(figsize=(10, 8))
#     nx.draw(builder.graph, pos, with_labels=True, node_color='orange', node_size=3000, font_size=10, font_weight='bold', edge_color='black')
    
#     # Save and display the graph
#     output_file = f'analysis_output/dfd_{file_path.split("/")[-1]}.png'
#     plt.savefig(output_file)
#     plt.show()

# if __name__ == "__main__":
#     file_to_analyze = "simple_library_management/main.py"
#     generate_dfd(file_to_analyze)

import os
import ast
from graphviz import Digraph

def parse_python_files_with_data(directory):
    """
    Parse Python files to extract functions, their parameters, return values,
    and interactions with files or logs.
    """
    functions = {}
    data_stores = set()

    for filename in os.listdir(directory):
        if filename.endswith(".py"):
            filepath = os.path.join(directory, filename)
            with open(filepath, "r") as file:
                try:
                    tree = ast.parse(file.read())
                    for node in ast.walk(tree):
                        if isinstance(node, ast.FunctionDef):
                            func_name = node.name
                            # Collect function parameters
                            params = [arg.arg for arg in node.args.args]
                            # Collect called functions and variables
                            calls = []
                            variables = []
                            for n in ast.walk(node):
                                if isinstance(n, ast.Call) and hasattr(n.func, "id"):
                                    calls.append(n.func.id)
                                if isinstance(n, ast.Name):
                                    variables.append(n.id)
                            # Identify file or log interactions
                            if any(v in ["open", "write", "read"] for v in variables):
                                data_stores.add("file_system")
                            if any("log" in v.lower() for v in variables):
                                data_stores.add("log")
                            functions[func_name] = {"params": params, "calls": calls}
                except SyntaxError as e:
                    print(f"Syntax error in file {filename}: {e}")

    return functions, data_stores

def generate_dfd_with_variables(functions, data_stores):
    """
    Generate a DFD incorporating variables and data stores.
    """
    dfd = Digraph("DFD", format="png")

    # Add external entity
    dfd.node("user", "User", shape="rectangle", style="filled", color="lightblue")

    # Add processes (functions)
    for func in functions:
        dfd.node(func, func.replace("_", " ").title(), shape="ellipse", style="filled", color="yellow")

    # Add data stores
    for store in data_stores:
        dfd.node(store, store.replace("_", " ").title(), shape="cylinder", style="filled", color="lightgreen")

    # Add data flows
    for func, details in functions.items():
        for param in details["params"]:
            dfd.edge("user", func, label=param)
        for call in details["calls"]:
            if call in functions:
                dfd.edge(func, call, label="Call")
        if "log" in data_stores:
            dfd.edge(func, "log", label="Log Entry")
        if "file_system" in data_stores:
            dfd.edge(func, "file_system", label="File Interaction")

    return dfd

# Modify this path to the location of your project directory
directory = "./simple_library_management"  # Absolute path

# Parse Python files and generate DFD
functions, data_stores = parse_python_files_with_data(directory)
dfd = generate_dfd_with_variables(functions, data_stores)

# Save and render the DFD
dfd.render("data_flow_diagram_with_variables", view=True)
