import tkinter as tk
from tkinter import filedialog

class DFA:
    def __init__(self):
        self.transitions = {}

    def add_transition(self, state, symbol, next_state):
        self.transitions[(state, symbol)] = next_state

    def get_next_state(self, state, symbol):
        return self.transitions.get((state, symbol), None)


dfa = DFA()


def load_transitions():
    file_path = filedialog.askopenfilename()

    if not file_path:
        return

    dfa.transitions.clear()

    with open(file_path, "r", encoding="utf-8") as f:
        for line in f:
            state, symbol, next_state = line.strip().split(",")
            dfa.add_transition(state, symbol, next_state)

    output.insert(tk.END, "Переходы загружены\n\n")


def run_dfa():
    output.delete("1.0", tk.END)

    state = start_state_entry.get()
    final_states = final_states_entry.get().split()
    input_string = input_entry.get()

    remaining = input_string

    output.insert(tk.END, "Последовательность конфигураций:\n\n")
    output.insert(tk.END, f"({state}, {remaining})\n")

    for symbol in input_string:

        next_state = dfa.get_next_state(state, symbol)

        if next_state is None:
            output.insert(tk.END, "Ошибка: переход не определён\n")
            return

        state = next_state
        remaining = remaining[1:]

        if remaining == "":
            remaining = "ε"

        output.insert(tk.END, f"({state}, {remaining})\n")

    if state in final_states:
        output.insert(tk.END, "\nРезультат: строка ПРИНЯТА")
    else:
        output.insert(tk.END, "\nРезультат: строка НЕ ПРИНЯТА")


root = tk.Tk()
root.title("Моделирование ДКА")
root.geometry("500x400")

tk.Label(root, text="Начальное состояние").pack()
start_state_entry = tk.Entry(root)
start_state_entry.pack()

tk.Label(root, text="Принимающие состояния").pack()
final_states_entry = tk.Entry(root)
final_states_entry.pack()

tk.Label(root, text="Строка для анализа").pack()
input_entry = tk.Entry(root)
input_entry.pack()

tk.Button(root, text="Загрузить переходы", command=load_transitions).pack(pady=5)
tk.Button(root, text="Запустить автомат", command=run_dfa).pack(pady=5)

output = tk.Text(root, height=15)
output.pack()

root.mainloop()