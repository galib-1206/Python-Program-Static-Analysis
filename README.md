# Python-Program-Static-Analysis
This repository provides a collection of tools for static analysis of Python programs. The tools include the generation of Control Flow Graphs (CFG), Call Graphs, and Data Flow Diagrams (DFD).. These tools help visualize the structure, behavior, and data interactions in Python applications, aiding in debugging, optimization, and system documentation.

### Features
- Control Flow Graph (CFG) Generation:
Visualize the control flow of Python programs by analyzing how the execution of statements flows.

- Call Graph Generation:
Generate a graph that maps the relationships between functions, showing which functions call others.

- Data Flow Diagram (DFD) Generation:
Visualize the interaction between processes, data stores, and external entities, incorporating variables and file or log interactions.

### Project Directory
.
├── analysis_output/             
├── simple library management/  
│   ├── main.py                  
│   └── (other files...)         
├── cfg_generator.py             
├── call_graph_generator.py      
├── dfd_generator.py            
└── README.md                    


### Prerequisites
Libraries:
- networkx
- matplotlib
- graphviz

### Example Application: Library Management System
The repository includes an example Python project (simple library management/) that implements a basic library management system with features like:
- Listing available books
- Borrowing books
- Returning books
