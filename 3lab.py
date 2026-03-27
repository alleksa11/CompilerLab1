import tkinter as tk
from tkinter import filedialog

# Приоритет операторов
priority = {
    '+': 1, '-': 1,
    '*': 2, '/': 2
}


# ===== Инфикс → Постфикс =====
def infix_to_postfix(expression):
    stack = []
    output = []

    tokens = expression.split()

    for token in tokens:
        if token.isalnum():
            output.append(token)

        elif token == '(':
            stack.append(token)

        elif token == ')':
            while stack and stack[-1] != '(':
                output.append(stack.pop())
            stack.pop()

        else:
            while (stack and stack[-1] != '(' and
                   priority.get(stack[-1], 0) >= priority.get(token, 0)):
                output.append(stack.pop())
            stack.append(token)

    while stack:
        output.append(stack.pop())

    return ' '.join(output)


# ===== Инфикс → Префикс =====
def infix_to_prefix(expression):
    tokens = expression.split()[::-1]

    for i in range(len(tokens)):
        if tokens[i] == '(':
            tokens[i] = ')'
        elif tokens[i] == ')':
            tokens[i] = '('

    postfix = infix_to_postfix(' '.join(tokens))
    return ' '.join(postfix.split()[::-1])


# ===== Узел дерева =====
class Node:
    def __init__(self, value):
        self.value = value
        self.left = None
        self.right = None


# ===== Постфикс → Дерево =====
def build_tree(postfix):
    stack = []
    tokens = postfix.split()

    for token in tokens:
        node = Node(token)

        if token not in '+-*/':
            stack.append(node)
        else:
            node.right = stack.pop()
            node.left = stack.pop()
            stack.append(node)

    return stack[0]


# ===== Печать дерева =====
def print_tree(node, level=0):
    if node is not None:
        print_tree(node.right, level + 1)
        tree_output.insert(tk.END, '   ' * level + node.value + '\n')
        print_tree(node.left, level + 1)


# ===== GUI =====
def analyze():
    expr = entry.get()

    postfix = infix_to_postfix(expr)
    prefix = infix_to_prefix(expr)

    result.delete(1.0, tk.END)
    tree_output.delete(1.0, tk.END)

    result.insert(tk.END, f"Постфикс: {postfix}\n")
    result.insert(tk.END, f"Префикс: {prefix}\n")

    tree = build_tree(postfix)
    print_tree(tree)


def load_file():
    file_path = filedialog.askopenfilename()
    if file_path:
        with open(file_path, 'r') as f:
            entry.delete(0, tk.END)
            entry.insert(0, f.read())


root = tk.Tk()
root.title("Генератор синтаксического дерева")

entry = tk.Entry(root, width=50)
entry.pack()

tk.Button(root, text="Загрузить файл", command=load_file).pack()
tk.Button(root, text="Анализ", command=analyze).pack()

result = tk.Text(root, height=5)
result.pack()

tree_output = tk.Text(root, height=15)
tree_output.pack()

root.mainloop()