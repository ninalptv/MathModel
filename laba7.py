import math
import random
import tkinter as tk
from tkinter import *
from tkinter import ttk, messagebox
from scipy.stats import f
import matplotlib.pyplot as plt
import numpy as np
from sympy import symbols


class Main(tk.Frame):
    def __init__(self, root):
        super().__init__(root)
        self.init_main()

    def init_main(self):
        toolbar = tk.Frame(bg="#f0f0f0", bd=7)
        toolbar.pack(side=tk.TOP, fill=tk.X)
        ttk.Label(toolbar, text="Кол-во опытов для случайных величин ").grid(row=1, column=1)
        self.edit1 = ttk.Entry(toolbar, width=10)
        btn_add = ttk.Button(toolbar, text="Добавить")
        btn_add.place(x=350, y=-2)
        btn_add.bind('<Button-1>', lambda event: self.edit_change(self.edit1.get()))
        self.edit1.place(x=270, y=0)
        self.edit1.bind("<KeyRelease>")
        tk.Label(self, font=("Arial", 12), text=f"").grid(row=2, column=1, columnspan=2, rowspan=5)
        self.tree0 = ttk.Treeview(self, columns="Значение", show="headings")
        self.tree = ttk.Treeview(self, columns="Значение", show="headings")
        self.tree0.column("#1", width=70)
        self.tree.column("#1", width=150)
        self.tree1 = ttk.Treeview(self, columns="Значение", show="headings")

        self.tree1.column("#1", width=150)
        self.tree2 = ttk.Treeview(self, columns="Значение", show="headings")
        self.tree2.column("#1", width=150)
        self.tree0.heading("Значение", text="№ Опыта ")

        self.tree.heading("Значение", text="X1:")
        self.tree1.heading("Значение", text="X2:")
        self.tree2.heading("Значение", text="Y:")
        self.tree0.grid(row=0, column=0)
        self.tree.grid(row=0, column=1)

        self.tree1.grid(row=0, column=2)
        self.tree2.grid(row=0, column=3)
        ttk.Button(self, text="Ввести X1", command=self.open_dialog).place(x=130, y=228)
        ttk.Button(self, text="Ввести X2", command=self.open_dialog1).place(x=290, y=228)
        ttk.Button(self, text="Ввести Y", command=self.open_dialog2).place(x=450, y=228)
        tk.Button(text="ВЫЧИСЛИТЬ!!!", command=self.button1_click, ).place(x=280, y=300)
        self.X1 = []
        self.X2 = []
        self.Y = []
        self.Y_r=[]
        self.moX1 = 0
        self.moX2 = 0
        self.moY = 0
        self.dX1 = 0
        self.dX2 = 0
        self.deltaX1 = 0
        self.deltaX2 = 0
        self.rX1_X2 = 0
        self.numerical_solution = []
        self.s_ad=0
        self.s_y=0
        self.f = 0
        self.F_critical_value = 0

    def edit_change(self, event):
        """Заполнение таблиц"""
        try:
            n = int(event)
            if n > 1:
                for i in range(n):
                    self.tree0.insert("", "end", values=(i + 1))
                    self.tree.insert("", "end", values=random.uniform(1.1, 3.0))
                    self.tree1.insert("", "end", values=random.uniform(2.5, 4.0))
                    self.tree2.insert("", "end", values=random.randint(2, 6))
            else:
                messagebox.showwarning("Warning", "Введите количество опытов больше 1")
        except ValueError:
            pass

    def button1_click(self):
        # Оценка математического ожидания
        self.X1 = [float(self.tree.item(child)["values"][0]) for child in self.tree.get_children()]
        self.X2 = [float(self.tree1.item(child)["values"][0]) for child in self.tree1.get_children()]
        self.Y = [float(self.tree2.item(child)["values"][0]) for child in self.tree2.get_children()]
        self.moX1 = sum(self.X1) / len(self.X1)
        self.moX2 = sum(self.X2) / len(self.X2)
        self.moY = sum(self.Y) / len(self.Y)

        # Дисперсия
        self.dX1 = sum((x - self.moX1) ** 2 for x in self.X1) / (len(self.X1) - 1)
        self.dX2 = sum((x - self.moX2) ** 2 for x in self.X2) / (len(self.X2) - 1)

        # Среднеквадратич отклонение
        self.deltaX1 = math.sqrt(self.dX1)
        self.deltaX2 = math.sqrt(self.dX2)

        # коэффициенты парных корреляций
        self.rX1_X2 = sum((self.X1[i] - self.moX1) * (self.X2[i] - self.moX2) for i in range(len(self.X1))) / (
                (len(self.X1) - 1) * self.deltaX1 * self.deltaX2)

        Child2()

    def func(self, X1, X2, Y):
        self.X1 = X1
        self.X2 = X2
        self.Y = Y
        self.sum_X1 = sum(self.X1)
        self.sum_X2 = sum(self.X2)
        self.sum_Y = sum(self.Y)
        self.sum_X1_X2 = sum(x1 * x2 for x1, x2 in zip(self.X1, self.X2))
        self.sum_X1_Y = sum(x1 * y for x1, y in zip(self.X1, self.Y))
        self.sum_X2_Y = sum(x2 * y for x2, y in zip(self.X2, self.Y))
        self.sum_X1_sqr = sum(x ** 2 for x in self.X1)
        self.sum_X2_sqr = sum(x ** 2 for x in self.X2)
        m1 = np.array([[len(self.X1), self.sum_X1, self.sum_X2], [self.sum_X1, self.sum_X1_sqr, self.sum_X1_X2],
                       [self.sum_X2, self.sum_X1_X2, self.sum_X2_sqr]])
        v1 = np.array([self.sum_Y, self.sum_X1_Y, self.sum_X2_Y])
        # equations = [
        #     Eq(len(self.X1) * self.b0 + self.sum_X1 * self.b1 + self.sum_X2 * self.b2, self.sum_Y),
        #     Eq(self.sum_X1 * self.b0 + self.sum_X1_sqr * self.b1 + self.sum_X1_X2 * self.b2, self.sum_X1_Y),
        #     Eq(self.sum_X2 * self.b0 + self.sum_X1_X2 * self.b1 + self.sum_X2_sqr, self.sum_X2_Y)
        # ]
        # initial_guess = [0, 0, 0]
        # #self.numerical_solution = nsolve(equations, (self.b0, self.b1, self.b2), initial_guess)
        self.numerical_solution = np.linalg.solve(m1, v1)
        self.Y_r = [self.func1(x1, x2) for x1, x2 in zip(self.X1, self.X2)]
        self.s_ad=sum((self.Y[i] - self.Y_r[i]) **2 for i in range(len(self.X1))) / len(self.X1)
        self.s_y=sum((self.Y[i] - self.moY) **2 for i in range(len(self.X1))) / len(self.X1)
        if self.s_ad <= self.s_y:
            self.f = self.s_y / self.s_ad
            k1 = len(self.X1) - 1
            k2 = len(self.X1)- 1
        else:
            self.f = self.s_ad / self.s_y
            k1 = len(self.X1)- 1
            k2 =  len(self.X1)- 1
        # Критические  точки  распределения  F  Фишера — Снедекора
        self.F_critical_value = f.ppf(q=1 - .01, dfn=k1, dfd=k2)



    def func1(self,x1,x2):
        return self.numerical_solution[0]+x1*self.numerical_solution[1]+x2*self.numerical_solution[2]

    def open_dialog(self):
        child = Child()
        child.bottonX()

    def open_dialog1(self):
        child = Child()
        child.bottonY()

    def open_dialog2(self):
        child = Child()
        child.bottonZ()

    def records(self, values, tree):
        if tree == "X":
            self.tree.set(self.tree.selection()[0], '#1', value=values)
        elif tree == "Y":
            self.tree1.set(self.tree1.selection()[0], '#1', value=values)
        elif tree == "Z":
            self.tree2.set(self.tree2.selection()[0], '#1', value=values)


class Child(tk.Toplevel):
    def __init__(self):
        super().__init__(root)
        self.init_child()
        self.view = app

    def init_child(self):
        self.title("Добавить значение")
        self.geometry("300x120+300+200")
        self.resizable(False, False)
        label_values = tk.Label(self, text='Значение:')
        label_values.place(x=50, y=40)
        self.entry_values = ttk.Entry(self)
        self.entry_values.place(x=120, y=40)
        self.grab_set()
        self.focus_set()
        self.btn_ok = ttk.Button(self, text='Добавить', command=self.destroy)
        self.btn_ok.place(x=180, y=80)

    def bottonX(self):
        self.btn_ok.bind('<Button-1>', lambda event: self.view.records(self.entry_values.get(), "X"))

    def bottonY(self):
        self.btn_ok.bind('<Button-1>', lambda event: self.view.records(self.entry_values.get(), "Y"))

    def bottonZ(self):
        self.btn_ok.bind('<Button-1>', lambda event: self.view.records(self.entry_values.get(), "Z"))


class Child2(tk.Toplevel):
    def __init__(self):
        super().__init__(root)
        self.init_child()
        self.view = app

    def init_child(self):
        self.title("Вывод")
        self.geometry("600x300")
        self.resizable(False, False)
        Button(self, text="Оценка адеватности", command=self.btn_click, ).place(x=450, y=250)
        Label(self, font=("Arial", 11), text=f"Коэф. корреляции rX1_X2={app.rX1_X2}").place(x=0, y=10)
        if (app.rX1_X2 >= 0.7) or (app.rX1_X2 <= -0.7):
            Label(self, font=("Arial", 11), text="Между  X1 и X2 существует сильная линейная связь").place(x=0, y=30)
            app.func(app.X1, app.X2, app.Y)
            self.draw_sys()
        elif ((app.rX1_X2 < 0.7) and (app.rX1_X2 >= 0.5)) or ((app.rX1_X2 > -0.7) and (app.rX1_X2 <= -0.5)):
            Label(self, font=("Arial", 11), text="Между X1 и X2 существует средняя линейная связь").place(x=0, y=30)
            app.func(app.X1, app.X2, app.Y)
            self.draw_sys()
        elif ((app.rX1_X2 < 0.5) and (app.rX1_X2 > 0)) or ((app.rX1_X2 > -0.5) and (app.rX1_X2 < 0)):
            Label(self, font=("Arial", 11), text="Между X1 и X2 существует слабая линейная связь").place(x=0, y=30)
            Label(self, font=("Arial", 11), text=f"Заменим ~X2=1/X2").place(x=0, y=50)
            x2_ = [1 / x for x in app.X2]
            app.func(app.X1, x2_, app.Y)
            self.draw_sys()
        elif (app.rX1_X2 <= 0.001) and (app.rX1_X2 >= -0.001):
            Label(self, font=("Arial", 11), text="Между X1 и X2 не существует линейной связи").place(x=0, y=30)
            x2_ = [1 / x for x in app.X2]
            app.func(app.X1, x2_, app.Y)
            self.draw_sys()

    def draw_sys(self):
        Label(self, font=("Arial", 11), text=f"Система уравнений:").place(x=0, y=80)
        Label(self, font=("Arial", 10),
              text=f"{len(app.X1)}*b0 + {app.sum_X1}*b1 + {app.sum_X2}*b2 = {app.sum_Y}").place(x=0, y=100)
        Label(self, font=("Arial", 10),
              text=f"{app.sum_X1}*b0 + {app.sum_X1_sqr}*b1 + {app.sum_X1_X2}*b2 = {app.sum_X1_Y}").place(x=0, y=120)
        Label(self, font=("Arial", 10),
              text=f"{app.sum_X2}*b0 + {app.sum_X1_X2}*b1 + {app.sum_X2_sqr}*b2 = {app.sum_X2_Y}").place(x=0, y=140)
        Label(self, font=("Arial", 10), text="Коэффициенты линейной модели").place(x=0, y=170)
        Label(self, font=("Arial", 10), text=f"b0={app.numerical_solution[0]}").place(x=0, y=190)
        Label(self, font=("Arial", 10), text=f"b1={app.numerical_solution[1]}").place(x=0, y=210)
        Label(self, font=("Arial", 10), text=f"b2={app.numerical_solution[2]}").place(x=0, y=230)

        # Создание данных для графиков
        x1 = np.array(app.X1)
        x2 = np.array(app.X2)
        y = np.array(app.Y)
        # y_x1 = app.numerical_solution[0] + app.numerical_solution[1] * x1
        # y_x2 = app.numerical_solution[0] + app.numerical_solution[2] * x2

        # Создание первого графика
        plt.subplot(2, 1, 1)  # указываем 2 строки, 1 столбец, выбираем первое место
        plt.scatter(x1, y, c="magenta")
        plt.plot(np.unique(x1),
                 np.poly1d(np.polyfit(x1, y, 1))
                 (np.unique(x1)), color='red')

        plt.xlabel('X1')
        plt.ylabel('Y')

        # Создание второго графика
        plt.subplot(2, 1, 2)  # указываем 2 строки, 1 столбец, выбираем второе место
        plt.scatter(x2, y, c="magenta")
        plt.plot(np.unique(x2),
                 np.poly1d(np.polyfit(x2, y, 1))
                 (np.unique(x2)), color='red')

        plt.xlabel('X2')
        plt.ylabel('Y')
        plt.show()

    def btn_click(self):
        Child3()

class Child3(tk.Toplevel):
    def __init__(self):
        super().__init__(root)
        self.init_child()
        self.view = app

    def init_child(self):
        self.title("Вывод")
        self.geometry("500x220+300+200")
        self.resizable(False, False)
        tk.Label(self, font=("Arial", 12), text=f"Дисперсии адекватности равна {app.s_ad}").place(x=50, y=10)
        tk.Label(self, font=("Arial", 12), text=f"Дисперсия опытных данных равна {app.s_y}").place(x=50, y=40)
        tk.Label(self, font=("Arial", 10),
                 text=f"Случайная величина с распределением Фишера-Снедекора F={app.f}").place(x=5, y=70)
        tk.Label(self, font=("Arial", 12), text=f"F(a,k1,k2)={app.F_critical_value}").place(x=50, y=100)
        if app.f > app.F_critical_value:
            tk.Label(self, font=("Arial", 14), text=f"Так как F > F(a,k1,k2), гипотеза отвергается").place(
                x=25, y=130)
        else:
            tk.Label(self, font=("Arial", 14), text=f"Так как F <= F(a,k1,k2), гипотеза  верна").place(
                x=25, y=130)
        print(app.Y_r)


if __name__ == "__main__":
    root = tk.Tk()
    app = Main(root)
    app.pack()
    root.title("Линейная и не линейная регрессия")
    root.geometry("620x360+300+200")
    root.resizable(False, False)
    root.mainloop()
