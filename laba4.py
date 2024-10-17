import math
import tkinter as tk
from tkinter import ttk

import matplotlib.pyplot as plt
import scipy
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg


class Main(tk.Frame):
    def __init__(self, root):
        super().__init__(root)
        self.init_main()

    def init_main(self):
        toolbar = tk.Frame(bg="#f0f0f0", bd=2)
        toolbar.pack(side=tk.TOP, fill=tk.X)

        self.tree = ttk.Treeview(self, columns=("№ Опыта", "Значение"), show="headings")
        self.tree.heading("№ Опыта", text="№ Опыта")
        self.tree.heading("Значение", text="Значение")
        self.tree.grid(row=0, column=0, columnspan=4)

        self.values = []
        with open('values.txt', ) as f:
            for item in f:
                self.values.append(float(item))
        for i in range(len(self.values)):
            self.tree.insert("", "end", values=(i + 1, self.values[i]))

        ttk.Button(self, text="Вычислить", command=self.button1_click).grid(row=2, column=1, columnspan=1)

        self.labels = {}
        self.edits = {}
        for i, text in enumerate(["Оценка математического ожидания", "Среднее квадратичное отклонение", "Дисперсия",
                                  "Варьирование X", "Формула Стерджесса"]):
            self.labels[text] = ttk.Label(self, text=text)
            self.labels[text].grid(row=3 + i, column=0)
            self.edits[text] = ttk.Entry(self)
            self.edits[text].grid(row=3 + i, column=1)
        self.mo = 0
        self.d = 0
        self.koef_as_a = 0
        self.ekscess_e = 0
        self.xi = []
        self.ni = []
        self.p = []  # вероятность попадания
        self.f = []
        self.g = []
        self.x_min = 0
        self.x_max = 0
        self.chart = plt.Figure(figsize=(6, 4))
        self.chart_canvas = FigureCanvasTkAgg(self.chart, self)
        self.chart_canvas.get_tk_widget().grid(row=0, column=4, rowspan=10)

    def button1_click(self):
        # Оценка математического ожидания
        self.mo = sum(self.values) / len(self.values)
        self.edits["Оценка математического ожидания"].delete(0, tk.END)
        self.edits["Оценка математического ожидания"].insert(0, str(self.mo))

        # Среднее квадратичное отклонение, Дисперсия
        self.d = sum((x - self.mo) ** 2 for x in self.values) / (len(self.values) - 1)
        self.edits["Среднее квадратичное отклонение"].delete(0, tk.END)
        self.edits["Среднее квадратичное отклонение"].insert(0, str(math.sqrt(self.d)))
        self.edits["Дисперсия"].delete(0, tk.END)
        self.edits["Дисперсия"].insert(0, str(self.d))

        # Варьирование X
        self.values.sort()
        self.x_min, self.x_max = self.values[0], self.values[-1]
        self.edits["Варьирование X"].delete(0, tk.END)
        self.edits["Варьирование X"].insert(0, str(self.x_max - self.x_min))

        # Формула Стерджесса
        dx = (self.x_max - self.x_min) / (1 + 3.22 * math.log(len(self.values)))
        self.edits["Формула Стерджесса"].delete(0, tk.END)
        self.edits["Формула Стерджесса"].insert(0, str(dx))

        # Вычисление xi, ni, f, и g
        self.xi = [self.x_min + i * 0.08 for i in range(len(self.values) + 1)]
        self.ni = [sum(1 for v in self.values if (v < x and v >= (x - dx))) for x in self.xi[1:]]
        self.g = [n / len(self.values) for n in self.ni]
        self.f = [0] + [sum(self.ni[:i + 1]) / len(self.values) for i in range(len(self.ni))]

        # Графики
        self.chart.clear()
        ax = self.chart.add_subplot(111)
        ax.plot(self.xi, self.f, color='red', label='Статистическая функция')
        ax.bar(self.xi[:-1], self.g, width=dx, alpha=0.5, color='blue', label='Гистограмма')
        ax.legend()
        self.chart_canvas.draw()
        self.open_dialog()

    def open_dialog(self):
        Child()


class Child(tk.Toplevel):
    def __init__(self):
        super().__init__(root)
        self.init_child()
        self.view = app

    def init_child(self):
        self.title("ЧАСТОТЫ ПОПАДАНИЯ СЛУЧАЙНОЙ ВЕЛИЧИНЫ")
        self.geometry("600x200+300+200")
        self.resizable(False, False)
        self.tree1 = ttk.Treeview(self, columns=("Интервал", "Эмпирическая частота", "Теоретическая частота"),
                                  show="headings")
        self.tree1.heading("Интервал", text="Интервал")
        self.tree1.heading("Эмпирическая частота", text="Эмпирическая частота")
        self.tree1.heading("Теоретическая частота", text="Теоретическая частота")
        self.tree1.grid(row=0, column=0, columnspan=4)
        self.values1 = []
        ksi_sqrt = 0
        with open('values.txt', ) as f:
            for item in f:
                self.values1.append(float(item))
        n = len(self.values1)
        for i in range(n):
            p = (scipy.stats.norm.cdf(app.xi[i + 1]) - 0.5) - (
                    scipy.stats.norm.cdf(app.xi[i]) - 0.5)  # теоритическая частота
            app.p.append(p)
            self.tree1.insert("", "end", values=(f"{app.xi[i]}-{app.xi[i + 1]}", app.g[i], p))
            ksi_sqrt += (app.ni[i] - n * p) ** 2 / (len(self.values1) * p)
        critical_distrib_points = [6.6, 9.2, 11.3, 13.3, 15.1, 16.8, 18.5, 20.1, 21.7, 23.2, 24.7, 26.2, 27.7]
        ksi = math.sqrt(ksi_sqrt)
        ksi_k = critical_distrib_points[n - 1]
        if ksi < ksi_k:
            tk.Label(self, text=f"Получаем {ksi}<{ksi_k}, закон распределения нормальный ").place(x=10, y=160)
        elif ksi > ksi_k:
            tk.Label(self, text=f"Получаем {ksi}>{ksi_k}, закон распределения не нормальный ").place(x=10, y=160)


if __name__ == "__main__":
    root = tk.Tk()
    app = Main(root)
    app.pack()
    root.title("ОЦЕНКА ЧИСЛОВЫХ ХАРАКТЕРИСТИК СЛУЧАЙНЫХ ВЕЛИЧИН")
    root.geometry("1000x450+300+200")
    root.resizable(False, False)
    root.mainloop()
