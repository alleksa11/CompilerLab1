import re
import tkinter as tk
from tkinter import filedialog, ttk, messagebox

TOKEN_TYPES = [
    ('KEYWORD', r'\b(var|if|else|while|for)\b'),
    ('IDENTIFIER', r'\b[a-zA-Z][a-zA-Z0-9]*\b'),
    ('NUMBER', r'\b\d+\b'),
    ('OPERATOR', r'==|!=|[+\-*/=]'),
    ('SEPARATOR', r'[;,()]')
]


class LexerApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Лексический анализатор")

        # Поле ввода
        self.text_input = tk.Text(root, height=10)
        self.text_input.pack(fill="x")

        # Кнопки
        frame = tk.Frame(root)
        frame.pack()

        tk.Button(frame, text="Анализ", command=self.analyze).pack(side="left")
        tk.Button(frame, text="Загрузить файл", command=self.load_file).pack(side="left")

        # Таблица
        self.tree = ttk.Treeview(root, columns=("Тип", "Позиция"), show="headings")
        self.tree.heading("Тип", text="Тип")
        self.tree.heading("Позиция", text="Позиция")
        self.tree.pack(fill="both", expand=True)

        # Ошибки
        self.error_label = tk.Label(root, text="", fg="red")
        self.error_label.pack()

    def load_file(self):
        file_path = filedialog.askopenfilename()
        if file_path:
            with open(file_path, "r") as f:
                self.text_input.delete(1.0, tk.END)
                self.text_input.insert(tk.END, f.read())

    def analyze(self):
        text = self.text_input.get("1.0", tk.END)

        self.tree.delete(*self.tree.get_children())
        self.error_label.config(text="")

        position = 0
        errors = []

        while position < len(text):
            if text[position].isspace():
                position += 1
                continue

            match = None

            for token_type, pattern in TOKEN_TYPES:
                regex = re.compile(pattern)
                match = regex.match(text, position)

                if match:
                    value = match.group(0)
                    self.tree.insert("", "end", values=(f"{value} ({token_type})", position))
                    position = match.end()
                    break

            if not match:
                errors.append(f"Ошибка: '{text[position]}' на позиции {position}")
                position += 1

        if errors:
            self.error_label.config(text="\n".join(errors))
        else:
            self.error_label.config(text="Ошибок нет")


# Запуск
root = tk.Tk()
app = LexerApp(root)
root.mainloop()