# StaticAnalysisYolov5

This static analysis tool uses the following tools to analyze linear operations in yolov5

Tools: 
1. AST
2. Tokenize
3. Scalpel 

# How to run the code
1. activate the environment: conda activate myenv
2. required files: 
2.1 nncp.py: python code contains the static analysis  
2.2 specification file: contains the expected order of operation
2.3 input python file to analyze. 

# example: 
python nncp.py spec_nonfunc.txt example_nonfunc.py 