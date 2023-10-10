import ast
import os

def find_imports(directory):
    imports = set()
    for root, dirs, files in os.walk(directory):
        for file in files:
            if file.endswith(".py"):
                filepath = os.path.join(root, file)
                with open(filepath, "r", encoding="utf-8") as f:
                    try:
                        tree = ast.parse(f.read())
                        for node in ast.walk(tree):
                            if isinstance(node, ast.Import):
                                for alias in node.names:
                                    imports.add(alias.name)
                            elif isinstance(node, ast.ImportFrom):
                                module = node.module
                                for alias in node.names:
                                    imports.add(f"{module}.{alias.name}")
                    except Exception as e:
                        print(f"Error parsing {filepath}: {e}")
    return imports

if __name__ == "__main__":
    project_directory = "."  # 修改为你的项目目录
    all_imports = find_imports(project_directory)
    
    with open("requirements.txt", "w") as req_file:
        for package in all_imports:
            req_file.write(f"{package}\n")
    
    print("requirements.txt 文件已创建。")
