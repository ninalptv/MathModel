import math
import tkinter as tk
from tkinter import *
from tkinter import ttk, messagebox


class Main(tk.Frame):
    def __init__(self, root):
        super().__init__(root)
        self.init_main()

    def init_main(self):
        toolbar = tk.Frame(bg="#f0f0f0", bd=7)
        toolbar.pack(side=tk.TOP, fill=tk.X)
        ttk.Label(toolbar, text="Кол-во опытов для случайных величин X, Y, Z").grid(row=1, column=1)
        self.edit1 = ttk.Entry(toolbar, width=10)
        btn_add = ttk.Button(toolbar, text="Добавить")
        btn_add.place(x=350, y=-2)
        btn_add.bind('<Button-1>', lambda event: self.edit_change(self.edit1.get()))
        self.edit1.place(x=270, y=0)
        self.edit1.bind("<KeyRelease>")
        tk.Label(self, font=("Arial", 12), text=f"").grid(row=2, column=1,columnspan=2, rowspan=5)
        self.tree = ttk.Treeview(self, columns=("№ Опыта X", "Значение"), show="headings")
        self.tree.column("#1", width=100)
        self.tree.column("#2", width=150)
        self.tree1 = ttk.Treeview(self, columns=("№ Опыта Y", "Значение"), show="headings")
        self.tree1.column("#1", width=100)
        self.tree1.column("#2", width=150)
        self.tree2 = ttk.Treeview(self, columns=("№ Опыта Z", "Значение"), show="headings")
        self.tree2.column("#1", width=100)
        self.tree2.column("#2", width=150)
        self.tree.heading("№ Опыта X", text="№ Опыта X")
        self.tree1.heading("№ Опыта Y", text="№ Опыта Y")
        self.tree2.heading("№ Опыта Z", text="№ Опыта Z")
        self.tree.heading("Значение", text="Значение")
        self.tree1.heading("Значение", text="Значение")
        self.tree2.heading("Значение", text="Значение")
        self.tree.grid(row=0, column=0)
        self.tree1.grid(row=0, column=1)
        self.tree2.grid(row=0, column=3)
        ttk.Button(self, text="Ввести X", command=self.open_dialog).place(x=170, y=228)
        ttk.Button(self, text="Ввести Y", command=self.open_dialog1).place(x=420, y=228)
        ttk.Button(self, text="Ввести Z", command=self.open_dialog2).place(x=660, y=228)
        tk.Button(text="ВЫЧИСЛИТЬ!!!", command=self.button1_click, ).place(x=380, y=300)

        self.moX = 0
        self.moY = 0
        self.moZ = 0
        self.dX = 0
        self.dY = 0
        self.dZ = 0
        self.deltaX = 0
        self.deltaY = 0
        self.deltaZ = 0
        self.rXY = 0
        self.rXZ = 0
        self.rYZ = 0

    def edit_change(self, event):
        """Заполнение таблиц"""
        try:
            n = int(event)
            if n > 1:
                for i in range(n):
                    self.tree.insert("", "end", values=(i + 1, '-'))
                    self.tree1.insert("", "end", values=(i + 1, '-'))
                    self.tree2.insert("", "end", values=(i + 1, '-'))
            else:
                messagebox.showwarning("Warning", "Введите количество опытов больше 1")
        except ValueError:
            pass

    def button1_click(self):
        # Оценка математического ожидания
        values1 = [float(self.tree.item(child)["values"][1]) for child in self.tree.get_children()]
        values2 = [float(self.tree1.item(child)["values"][1]) for child in self.tree1.get_children()]
        values3 = [float(self.tree2.item(child)["values"][1]) for child in self.tree2.get_children()]
        self.moX = sum(values1) / len(values1)
        self.moY = sum(values2) / len(values2)
        self.moZ = sum(values3) / len(values3)

        # Дисперсия
        self.dX = sum((x - self.moX) ** 2 for x in values1) / (len(values1) - 1)
        self.dY = sum((x - self.moY) ** 2 for x in values2) / (len(values2) - 1)
        self.dZ = sum((x - self.moZ) ** 2 for x in values3) / (len(values3) - 1)

        # Среднеквадратич отклонение
        self.deltaX = math.sqrt(self.dX)
        self.deltaY = math.sqrt(self.dY)
        self.deltaZ = math.sqrt(self.dZ)

        # коэффициенты парных корреляций
        self.rXY = sum((values1[i] - self.moX) * (values2[i] - self.moY) for i in range(len(values1))) / (
                (len(values1) - 1) * self.deltaX * self.deltaY)
        self.rXZ = sum((x - self.moX) * (z - self.moZ) for x, z in zip(values1, values3)) / (
                (len(values1) - 1) * self.deltaX * self.deltaZ)
        self.rYZ = sum((y - self.moY) * (z - self.moZ) for y, z in zip(values2, values3)) / (
                (len(values2) - 1) * self.deltaY * self.deltaZ)

        Child2()

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
            self.tree.set(self.tree.selection()[0], '#2', value=values)
        elif tree == "Y":
            self.tree1.set(self.tree1.selection()[0], '#2', value=values)
        elif tree == "Z":
            self.tree2.set(self.tree2.selection()[0], '#2', value=values)


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
        self.geometry("300x300")
        self.resizable(False, False)
        canvas = tk.Canvas(self, bg="white", width=250, height=250)
        canvas.pack(anchor=CENTER, expand=1)
        canvas.create_line(50, 80, 50, 100)
        canvas.create_line(48, 80, 48, 100)
        Label(self, font=("Arial", 12), text="Матрица коэфф-ов парных корреляций:").place(x=2, y=24)
        Label(self, font=("Arial", 12), text=f"r").place(x=75, y=100)
        canvas.create_line(65, 80, 65, 100)
        canvas.create_line(67, 80, 67, 100)
        Label(self, font=("Arial", 12), text="=").place(x=92, y=100)
        canvas.create_line(90, 40, 90, 140)
        canvas.create_line(94, 40, 94, 140)
        Label(self, font=("Arial", 12), text="1").place(x=120, y=64)
        Label(self, font=("Arial", 11), text=f"{str(app.rXY)[:4]}").place(x=152, y=64)
        Label(self, font=("Arial", 11), text=f"{str(app.rXZ)[:4]}").place(x=197, y=64)
        Label(self, font=("Arial", 12), text="1").place(x=170, y=100)
        Label(self, font=("Arial", 11), text=f"{str(app.rYZ)[:4]}").place(x=197, y=100)
        Label(self, font=("Arial", 12), text="1").place(x=220, y=140)
        canvas.create_line(218, 40, 218, 140)
        canvas.create_line(222, 40, 222, 140)
        Label(self, font=("Calibri", 9), text="Вывод о статистической зависимости с.в.:").place(x=0, y=190)
        if (app.rXY >= 0.7) or (app.rXY <= -0.7):
            Label(self, font=("Arial", 8), text="Между с.в. X и Y существует сильная линейная связь").place(x=5, y=220)
        elif ((app.rXY < 0.7) and (app.rXY >= 0.5)) or ((app.rXY > -0.7) and (app.rXY <= -0.5)):
            Label(self, font=("Arial", 8), text="Между с.в. X и Y существует средняя линейная связь").place(x=5, y=220)
        elif ((app.rXY < 0.5) and (app.rXY > 0)) or ((app.rXY > -0.5) and (app.rXY < 0)):
            Label(self, font=("Arial", 8), text="Между с.в. X и Y существует слабая линейная связь").place(x=5, y=220)
        elif (app.rXY <= 0.001) and (app.rXY >= -0.001):
            Label(self, font=("Arial", 8), text="Между с.в. X и Y не существует линейной связи").place(x=5, y=220)

        if (app.rXZ >= 0.7) or (app.rXZ <= -0.7):
            Label(self, font=("Arial", 8), text="Между с.в. X и Z существует сильная линейная связь").place(x=5, y=240)
        elif ((app.rXZ < 0.7) and (app.rXZ >= 0.5)) or ((app.rXZ > -0.7) and (app.rXZ <= -0.5)):
            Label(self, font=("Arial", 8), text="Между с.в. X и Z существует средняя линейная связь").place(x=5, y=240)
        elif ((app.rXZ < 0.5) and (app.rXZ > 0)) or ((app.rXZ > -0.5) and (app.rXZ < 0)):
            Label(self, font=("Arial", 8), text="Между с.в. X и Z существует слабая линейная связь").place(x=5, y=240)
        elif (app.rXZ <= 0.001) and (app.rXZ >= -0.001):
            Label(self, font=("Arial", 8), text="Между с.в. X и Z не существует линейной связи").place(x=5, y=240)

        if (app.rYZ >= 0.7) or (app.rYZ <= -0.7):
            Label(self, font=("Arial", 8), text="Между с.в. Y и Z существует сильная линейная связь").place(x=5, y=260)
        elif ((app.rYZ < 0.7) and (app.rYZ >= 0.5)) or ((app.rYZ > -0.7) and (app.rYZ <= -0.5)):
            Label(self, font=("Arial", 8), text="Между с.в. Y и Z существует средняя линейная связь").place(x=5, y=260)
        elif ((app.rYZ < 0.5) and (app.rYZ > 0)) or ((app.rYZ > -0.5) and (app.rYZ < 0)):
            Label(self, font=("Arial", 8), text="Между с.в. Y и Z существует слабая линейная связь").place(x=5, y=260)
        elif (app.rYZ <= 0.001) and (app.rYZ >= -0.001):
            Label(self, font=("Arial", 8), text="Между с.в. Y и Z не существует линейной связи").place(x=5, y=260)
        print(f"{app.rXY:.2f}")
        print(f"{app.rXZ:.2f}")
        print(f"{app.rYZ:.2f}")


if __name__ == "__main__":
    root = tk.Tk()
    app = Main(root)
    app.pack()
    root.title("Корреляционный анализ")
    root.geometry("820x360+300+200")
    root.resizable(False, False)
    root.mainloop()
