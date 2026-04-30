import tkinter as tk
from tkinter import ttk, messagebox
import json
from datetime import datetime

class TrainingPlanner:
    def __init__(self, root):
        self.root = root
        self.root.title("Training Planner")
        self.create_widgets()
        self.load_data()
        self.update_table()

    def create_widgets(self):
        # Поля ввода
        ttk.Label(self.root, text="Дата (YYYY-MM-DD):").grid(row=0, column=0, padx=5, pady=5)
        self.date_entry = ttk.Entry(self.root)
        self.date_entry.grid(row=0, column=1, padx=5, pady=5)

        ttk.Label(self.root, text="Тип:").grid(row=1, column=0, padx=5, pady=5)
        self.type_var = tk.StringVar()
        self.type_combo = ttk.Combobox(self.root, textvariable=self.type_var,
                                       values=["Кардио", "Силовая", "Растяжка"])
        self.type_combo.grid(row=1, column=1, padx=5, pady=5)

        ttk.Label(self.root, text="Длительность (мин):").grid(row=2, column=0, padx=5, pady=5)
        self.duration_entry = ttk.Entry(self.root)
        self.duration_entry.grid(row=2, column=1, padx=5, pady=5)

        # Кнопки
        ttk.Button(self.root, text="Добавить тренировку", command=self.add_training).grid(row=3, column=0, columnspan=2, pady=10)
        ttk.Button(self.root, text="Сохранить в JSON", command=self.save_data).grid(row=4, column=0, columnspan=2, pady=5)

        # Таблица
        self.tree = ttk.Treeview(self.root, columns=("Дата", "Тип", "Длительность"), show='headings')
        self.tree.heading("Дата", text="Дата")
        self.tree.heading("Тип", text="Тип")
        self.tree.heading("Длительность", text="Длительность")
        self.tree.grid(row=5, column=0, columnspan=2, padx=5, pady=5)

    def add_training(self):
        date = self.date_entry.get()
        type_ = self.type_var.get()
        duration = self.duration_entry.get()

        try:
            datetime.strptime(date, "%Y-%m-%d")
            duration = int(duration)
            if duration <= 0:
                raise ValueError("Длительность должна быть положительной")
            self.data.append({"date": date, "type": type_, "duration": duration})
            self.update_table()
            self.clear_entries()
        except Exception as e:
            messagebox.showerror("Ошибка", str(e))

    def update_table(self):
        for i in self.tree.get_children():
            self.tree.delete(i)
        for item in self.data:
            self.tree.insert("", "end", values=(item["date"], item["type"], item["duration"]))

    def clear_entries(self):
        self.date_entry.delete(0, tk.END)
        self.type_combo.set("")
        self.duration_entry.delete(0, tk.END)

    def save_data(self):
        with open("trainings.json", "w") as f:
            json.dump(self.data, f)

    def load_data(self):
        try:
            with open("trainings.json", "r") as f:
                self.data = json.load(f)
        except FileNotFoundError:
            self.data = []

if __name__ == "__main__":
    root = tk.Tk()
    app = TrainingPlanner(root)
    root.mainloop()
