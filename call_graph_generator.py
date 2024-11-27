#Call graph 
import ast
import networkx as nx
from matplotlib import pyplot as plt

class CallGraphBuilder(ast.NodeVisitor):
    def __init__(self):
        self.graph = nx.DiGraph()
        self.current_function = None

    def visit_FunctionDef(self, node):
        """Visiting function definitions to track the function name."""
        self.current_function = node.name
        self.graph.add_node(node.name)
        self.generic_visit(node)
        self.current_function = None  # Reset the current function after visiting it

    def visit_Call(self, node):
        """Visiting function calls to add an edge to the graph."""
        func_name = None
        
        if isinstance(node.func, ast.Name):
            # Simple function call like func()
            func_name = node.func.id
        elif isinstance(node.func, ast.Attribute):
            # Method call like obj.method() or module.function()
            # We use 'obj.method' for method calls
            if isinstance(node.func.value, ast.Name):
                func_name = f"{node.func.value.id}.{node.func.attr}"
            else:
                func_name = node.func.attr
        
        if func_name and self.current_function:
            # Only add the edge if both the current function and the called function name are valid
            self.graph.add_edge(self.current_function, func_name)
        
        self.generic_visit(node)

    def build_call_graph(self, source_code):
        """Build the call graph for a given source code."""
        tree = ast.parse(source_code)
        self.visit(tree)

def generate_call_graph(file_path):
    """Generate and visualize the call graph for a given Python file."""
    with open(file_path, 'r') as f:
        source_code = f.read()

    builder = CallGraphBuilder()
    builder.build_call_graph(source_code)

    # Visualize the graph with matplotlib
    nx.draw(builder.graph, with_labels=True, node_color='lightgreen', node_size=2000)
    plt.savefig(f'analysis_output/call_graph_{file_path.split("/")[-1]}.png')
    plt.show()

if __name__ == "__main__":
    file_to_analyze = "simple_library_management/main.py"
    generate_call_graph(file_to_analyze)
