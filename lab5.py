import tkinter as tk
from tkinter import ttk, messagebox

from scipy.stats import f


class Main(tk.Frame):
    def __init__(self, root):
        super().__init__(root)
        self.init_main()

    def init_main(self):
        toolbar = tk.Frame(bg="#f0f0f0", bd=2)
        toolbar.pack(side=tk.TOP, fill=tk.X)
        ttk.Label(toolbar, text="Количество опытов X").grid(row=1, column=1)
        ttk.Label(toolbar, text="Количество опытов Y").place(x=420, y=0)
        self.edit1 = ttk.Entry(toolbar)
        self.edit2 = ttk.Entry(toolbar)
        btn_add = ttk.Button(toolbar, text="Добавить в таблицу")
        btn_add1 = ttk.Button(toolbar, text="Добавить в таблицу")
        btn_add.place(x=260, y=0)
        btn_add1.place(x=680, y=0)
        btn_add.bind('<Button-1>', lambda event: self.edit1_change(self.edit1.get()))
        btn_add1.bind('<Button-1>', lambda event: self.edit2_change(self.edit2.get()))
        self.edit1.place(x=133, y=0)
        self.edit2.place(x=550, y=0)
        self.edit1.bind("<KeyRelease>")
        self.edit2.bind("<KeyRelease>")
        tk.Label(self, font=("Arial", 12), text=f"").grid(row=2, column=1,
                                                          columnspan=2, rowspan=5)
        self.tree = ttk.Treeview(self, columns=("№ Опыта X", "Значение"), show="headings")
        self.tree1 = ttk.Treeview(self, columns=("№ Опыта Y", "Значение"), show="headings")
        self.tree.heading("№ Опыта X", text="№ Опыта X")
        self.tree1.heading("№ Опыта Y", text="№ Опыта Y")
        self.tree.heading("Значение", text="Значение")
        self.tree1.heading("Значение", text="Значение")
        self.tree.grid(row=0, column=0)
        self.tree1.grid(row=0, column=1)
        ttk.Button(self, text="Ввести значение X", command=self.open_dialog).place(x=104, y=228)
        ttk.Button(self, text="Ввести значение Y", command=self.open_dialog1).place(x=570, y=228)

        ttk.Button(self, text="Вычислить", command=self.button1_click).place(x=360, y=228)

        self.moX = 0
        self.moY = 0
        self.dX = 0
        self.dY = 0
        self.f = 0
        self.F_critical_value = 0

    def edit1_change(self, event):
        try:
            n = int(self.edit1.get())
            if n > 1:
                for i in range(n):
                    self.tree.insert("", "end", values=(i + 1, '-'))

            else:
                messagebox.showwarning("Warning", "Введите количество опытов больше нуля")
        except ValueError:
            pass

    def edit2_change(self, event):
        try:
            n = int(self.edit2.get())
            if n > 1:
                for i in range(n):
                    self.tree1.insert("", "end", values=(i + 1, '-'))

            else:
                messagebox.showwarning("Warning", "Введите количество опытов больше 1")
        except ValueError:
            pass

    def button1_click(self):
        # Оценка математического ожидания
        values1 = [float(self.tree.item(child)["values"][1]) for child in self.tree.get_children()]
        values2 = [float(self.tree1.item(child)["values"][1]) for child in self.tree1.get_children()]
        self.moX = sum(values1) / len(values1)
        self.moY = sum(values2) / len(values2)

        # Дисперсия
        self.dX = sum((x - self.moX) ** 2 for x in values1) / (len(values1) - 1)
        self.dY = sum((x - self.moY) ** 2 for x in values2) / (len(values2) - 1)
        # Отношение F
        if self.dX <= self.dY:
            self.f = self.dY / self.dX
            k1 = len(values2) - 1
            k2 = len(values1) - 1
        else:
            self.f = self.dX / self.dY
            k1 = len(values1) - 1
            k2 = len(values2) - 1
        # Критические  точки  распределения  F  Фишера — Снедекора
        self.F_critical_value = f.ppf(q=1 - .01, dfn=k1, dfd=k2)
        print(self.F_critical_value)
        Child2()

    def open_dialog(self):
        child = Child()
        child.bottonX()

    def open_dialog1(self):
        child = Child()
        child.bottonY()

    def records(self, values):
        self.tree.set(self.tree.selection()[0], '#2', value=values)

    def records1(self, values):
        self.tree1.set(self.tree1.selection()[0], '#2', value=values)


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

    def bottonX(self):
        btn_ok = ttk.Button(self, text='Добавить', command=self.destroy)
        btn_ok.place(x=180, y=80)
        btn_ok.bind('<Button-1>', lambda event: self.view.records(self.entry_values.get()))

    def bottonY(self):
        btn_ok = ttk.Button(self, text='Добавить', command=self.destroy)
        btn_ok.place(x=180, y=80)
        btn_ok.bind('<Button-1>', lambda event: self.view.records1(self.entry_values.get()))


class Child2(tk.Toplevel):
    def __init__(self):
        super().__init__(root)
        self.init_child()
        self.view = app

    def init_child(self):
        self.title("Вывод")
        self.geometry("500x220+300+200")
        self.resizable(False, False)
        tk.Label(self, font=("Arial", 12), text=f"Дисперсия с.в. X: D(X)=S**2(X)={app.dX}").place(x=50, y=10)
        tk.Label(self, font=("Arial", 12), text=f"Дисперсия с.в. Y: D(Y)=S**2(Y)={app.dY}").place(x=50, y=40)
        tk.Label(self, font=("Arial", 10),
                 text=f"Случайная величина с распределением Фишера-Снедекора F={app.f}").place(x=5, y=70)
        tk.Label(self, font=("Arial", 12), text=f"F(a,k1,k2)={app.F_critical_value}").place(x=50, y=100)
        if app.f > app.F_critical_value:
            tk.Label(self, font=("Arial", 14), text=f"Так как F > F(a,k1,k2), гипотеза D(X)=D(Y) отвергается").place(
                x=25, y=130)
        else:
            tk.Label(self, font=("Arial", 14), text=f"Так как F <= F(a,k1,k2), гипотеза D(X)=D(Y) верна").place(
                x=25, y=130)


if __name__ == "__main__":
    root = tk.Tk()
    app = Main(root)
    app.pack()
    root.title("ОЦЕНКА ЧИСЛОВЫХ ХАРАКТЕРИСТИК СЛУЧАЙНЫХ ВЕЛИЧИН")
    root.geometry("820x300+300+200")
    root.resizable(False, False)
    root.mainloop()
