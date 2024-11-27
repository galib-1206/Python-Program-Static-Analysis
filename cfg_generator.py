#CFG
import ast
import networkx as nx
from matplotlib import pyplot as plt

class CFGBuilder(ast.NodeVisitor):
    def __init__(self):
        self.graph = nx.DiGraph()
        self.node_counter = 0

    def visit_FunctionDef(self, node):
        self.node_counter += 1
        function_name = f"Function: {node.name}"
        self.graph.add_node(self.node_counter, label=function_name)
        self.generic_visit(node)

    def visit_If(self, node):
        self.node_counter += 1
        condition = f"If: {ast.dump(node.test)}"
        self.graph.add_node(self.node_counter, label=condition)
        self.generic_visit(node)

    def build_cfg(self, source_code):
        tree = ast.parse(source_code)
        self.visit(tree)

def generate_cfg(file_path):
    with open(file_path, 'r') as f:
        source_code = f.read()
    builder = CFGBuilder()
    builder.build_cfg(source_code)
    nx.draw(builder.graph, with_labels=True, node_color='skyblue', node_size=2000)
    plt.savefig(f'analysis_output/cfg_{file_path.split("/")[-1]}.png')
    plt.show()

if __name__ == "__main__":
    file_to_analyze = "simple_library_management/main.py"
    generate_cfg(file_to_analyze)
