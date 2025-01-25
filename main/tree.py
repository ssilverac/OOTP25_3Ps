import os

def display_tree(startpath, depth=2):
    for root, dirs, files in os.walk(startpath):
        # Calculate the current level
        level = root.replace(startpath, "").count(os.sep)
        if level >= depth:
            continue
        indent = " " * 4 * level
        print(f"{indent}{os.path.basename(root)}/")
        sub_indent = " " * 4 * (level + 1)
        for file in files:
            print(f"{sub_indent}{file}")

# Change '.' to your desired directory path
display_tree("..", depth=3)
