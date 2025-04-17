from SimpleNumbers import *
from FareyFunctions import *
import tkinter as ttk
from tkinter import *
import tkinter.filedialog as filedialog

from pylab import * #for powershell
import matplotlib.pyplot as plt #for large programs
import math

#Объявление переменных

# Значения частот
Fbix2 = 1.0  # Значение частоты на выходе
DF = 1.0  # Шаг частот
NF = 10  # Количество частот в диапазоне РРЛ связи
Fbx1 = 1.0  # Значение частоты на входе приемника
Fshbix2 = 1.0  # Значение частоты на выходе передатчика
Fsh1 = 1.0  # Значение частоты 1-го гетеродина передатчика
F1 = 1.0  # Значение частоты 1-го гетеродина приемника
F2 = 1.0  # Значение частоты 2-го гетеродина
Fbix1 = 1.0 # Ф"вх1????????????????
Fdig = 1  #  Целочисленное значение частоты, ранее было объявлено дважды
KP = 1 # Индекс ряда Фарея
KPP = 1  # Порядок допустимых комбинацилнных частот

# Дроби для аппроксимации соотношений смешиваемых частот
IrF2 = IqF2 = IrF2N= IqF2N = IrF1 = IqF1 = IrFsh1 = IqFsh1= 1

# Переменные для разложения частот на простые сомножители
# Подтягивается из библиотеки Simple Numbers
SF1 = Simple()
SFsh1 = Simple()
SF2 = Simple()
SDF = Simple()

# Переменные для вычисления частот на входах преобразователей
Q2 = Akoef2 = Akoef1 = Akoef1sh = 1.0

# Коэффициенты качества
Qk1 = Qk1sh = Qk2 = ii = jj = 1

# Промежуточные переменные для вычисления расстояний до ближайших
# комбинационных частот
IR1 = IQ1 = IR2 = IQ2 = nn = 1
RR1 = RR2 = RQk2 = RQk1 = RQk2sh = RQk1sh = 1.0

# Переменные для вычисления расстояний зон фильтрации
Rg2 = Rg1 = Rg2sh = Rg1sh = 1.0

# Переменные описывающие относительное качество
OQk1 = OQk1sh = OQk2 = ORk2 = ORk1 = ORk2sh = ORk1sh = 1.0
Okgs = 1.0  # суммарное качество # S поле
Okgm = 1.0  # мультипликативное качество # M поле


#Создание окна

root = Tk()
root.title("Оптимизация радиорелейны станций в жёстких ограничениях")
root.geometry("800x600")
root.resizable(width=False, height= False)

#задний фон
root.image = PhotoImage(file='Background.png')
backgr = Label(root, image= root.image)
backgr.place(x=0, y=0)

#верхняя панель
root.option_add("*tearOff", FALSE) #убирает ненужный пунктир в выплывающих пунктах
main_menu = Menu()
 
file_menu = Menu(tearoff=0)
file_menu.add_command(label="Calculate", command=lambda: cmdCalc_Click(txt_fbix2, txt_df, txt_nf, txt_fbx1, txt_fshbix2, txt_fsh1, txt_f1, txt_f2, txt_nfarey, txt_kpp, 
                  txt_irf2, txt_iqf2, txt_irf2sh, txt_iqf2sh, txt_q1, txt_qsh1, txt_q2, txt_rqk1, txt_rqk2,
                   txt_rqk1sh, txt_rqk2sh, txt_okgs, txt_okgm))
file_menu.add_command(label="Save", command=lambda: save_as())
file_menu.add_command(label="Graf", command=lambda: graf_of_quadratic_func())
file_menu.add_separator()
file_menu.add_command(label="Exit", command= lambda: exit())
 
main_menu.add_cascade(label="File", menu=file_menu)
main_menu.add_cascade(label="Edit")
main_menu.add_cascade(label="View")
 
root.config(menu=main_menu)


#настрoйка сетки
for c in range(200): root.columnconfigure(index=c, weight=1)
for r in range(200): root.rowconfigure(index=r, weight=1)

#кнопки
save_button = ttk.Button(text="Save", command= lambda: cmdSave_Click()).grid(row=190, column=85) #привязать функцию

calc_button = ttk.Button(text="Calc", command=lambda: cmdCalc_Click(txt_fbix2, txt_df, txt_nf, txt_fbx1, txt_fshbix2, txt_fsh1, txt_f1, txt_f2, txt_nfarey, txt_kpp, 
                  txt_irf2, txt_iqf2, txt_irf2sh, txt_iqf2sh, txt_q1, txt_qsh1, txt_q2, txt_rqk1, txt_rqk2,
                   txt_rqk1sh, txt_rqk2sh, txt_okgs, txt_okgm)).grid(row=190, column=95)

graf_button = ttk.Button(text="Graf", command=lambda: graf_of_quadratic_func()).grid(row=190, column=105) #привязать функцию

nn_down_btn = ttk.Button(text="<",height=1, command=lambda: cmdD_Click()).place(x=100, y=56) #привязать функцию
nn_up_btn = ttk.Button(text=">", height=1, command=lambda: cmdU_Click()).place(x=144, y=56) #привязать функцию

F2_down_btn = ttk.Button(text="<",height=1, command=lambda: cmdDown_Click(txt_fbix2, txt_df, txt_nf, txt_fbx1, txt_fshbix2, txt_fsh1, txt_f1, txt_f2, txt_nfarey, txt_kpp, 
                  txt_irf2, txt_iqf2, txt_irf2sh, txt_iqf2sh, txt_q1, txt_qsh1, txt_q2, txt_rqk1, txt_rqk2, 
                  txt_rqk1sh, txt_rqk2sh, txt_okgs, txt_okgm)).place(x=488, y=306) #привязать функцию

F2_up_btn = ttk.Button(text=">", height=1, command=lambda: cmdUp_Click(txt_fbix2, txt_df, txt_nf, txt_fbx1, txt_fshbix2, txt_fsh1, txt_f1, txt_f2, txt_nfarey, txt_kpp, 
                  txt_irf2, txt_iqf2, txt_irf2sh, txt_iqf2sh, txt_q1, txt_qsh1, txt_q2, txt_rqk1, txt_rqk2, 
                  txt_rqk1sh, txt_rqk2sh, txt_okgs, txt_okgm)).place(x=538, y=306) #привязать функцию

#Добавление полей с начальными значениями
#Fвх1
ttk.Label(text="Fвх1:", font=("Arial", 10)).grid(row=10,column=1)
Fbx1 = 37072
txt_fbx1 = ttk.Entry(root, width=10)
txt_fbx1.place(x=51, y=25), txt_fbx1.insert(0, Fbx1)
    
#Df
ttk.Label(text="Df:", font=("Arial", 10)).grid(row=15,column=1)
DF = 28
txt_df = ttk.Entry(root, width=5)
txt_df.place(x=41, y=60), txt_df.insert(0, DF)

#Изменение значения частот Fbx1 и Fshbix2 на величину DF
nn = 0
txt_nn = ttk.Entry(root, width=3)
txt_nn.place(x=120, y=60), txt_nn.insert(0, nn)

#Индекс Фарея
ttk.Label(text="Индекс Фарея:", font=("Arial", 10)).place(x=600, y=300)
KP = 50
txt_nfarey = ttk.Entry(root, width=4)
txt_nfarey.place(x=698, y=301), txt_nfarey.insert(0, KP)

#Порядок допустимых комбинационных частот
ttk.Label(text="Допустимый порядок комб. частот:", font=("Arial", 10)).place(x=250, y=10)
KPP = 7
txt_kpp = ttk.Entry(root, width=4)
txt_kpp.place(x=468, y=11), txt_kpp.insert(0, KPP)

#F2
F2 = 2250
txt_f2 = ttk.Entry(root, width=4)
txt_f2.place(x=508, y=310), txt_f2.insert(0, F2)

#Fвых'2
ttk.Label(text="Fвых'2:", font=("Arial", 10)).grid(row=183,column=1)
Fshbix2 = 38332
txt_fshbix2 = ttk.Entry(root, width=8)
txt_fshbix2.place(x=55, y=515), txt_fshbix2.insert(0, Fshbix2)
    
#nf
ttk.Label(text="n:", font=("Arial", 10)).grid(row=16,column=1)
DF = 28
txt_nf = ttk.Entry(root, width=5)
txt_nf.place(x=41, y=81), txt_nf.insert(0, DF)


    
#Добавление полей для которых нужно рассчитать значения
    
#Q1
ttk.Label(text="Q1:", font=("Arial", 10)).grid(row=70,column=1)
txt_q1 = ttk.Entry(root, width=4)
txt_q1.grid(row=70,column=2), txt_q1.insert(0, Qk1)
#Q'1
ttk.Label(text="Q'1:", font=("Arial", 10)).grid(row=90,column=1)
txt_qsh1 = ttk.Entry(root, width=4)
txt_qsh1.grid(row=90,column=2), txt_qsh1.insert(0, Qk1sh)
#Q2
ttk.Label(text="Q2:", font=("Arial", 10)).place(x=600, y=275)
txt_q2 = ttk.Entry(root, width=4)
txt_q2.place(x=628, y=275), txt_q2.insert(0, Q2)
#RQk1
ttk.Label(text="RQk1:", font=("Arial", 10)).place(x=310, y=220)
txt_rqk1 = ttk.Entry(root, width=8)
txt_rqk1.place(x=355, y=221), txt_rqk1.insert(0, RQk1)
#RQk1'
ttk.Label(text="RQk1':", font=("Arial", 10)).place(x=310, y=317)
txt_rqk1sh = ttk.Entry(root, width=8)
txt_rqk1sh.place(x=356, y=318), txt_rqk1sh.insert(0, RQk1sh)
#RQk2
ttk.Label(text="RQk2:", font=("Arial", 10)).place(x=528, y=215)
txt_rqk2 = ttk.Entry(root, width=8)
txt_rqk2.place(x=573, y=216), txt_rqk2.insert(0, RQk2)
#RQk2'
ttk.Label(text="RQk2':", font=("Arial", 10)).place(x=528, y=360)
txt_rqk2sh = ttk.Entry(root, width=8)
txt_rqk2sh.place(x=575, y=361), txt_rqk2sh.insert(0, RQk2sh)
#Okgs
ttk.Label(text="Okgs:", font=("Arial", 10)).place(x=505, y=11)
txt_okgs = ttk.Entry(root, width=15)
txt_okgs.place(x=549, y=12), txt_okgs.insert(0, Okgs)
#Okgm
ttk.Label(text="Okgm:", font=("Arial", 10)).place(x=650, y=11)
txt_okgm = ttk.Entry(root, width=15)
txt_okgm.place(x=698, y=12), txt_okgm.insert(0, Okgm)

#F1
txt_f1 = ttk.Entry(root, width=8)
txt_f1.place(x=235, y=276), txt_f1.insert(0, F1)
#Fsh1
txt_fsh1 = ttk.Entry(root, width=8)
txt_fsh1.place(x=235, y=372), txt_fsh1.insert(0, Fsh1)
    
#Дроби
#IRf1
txt_irf1 = ttk.Entry(root, width=4)
txt_irf1.place(x=285, y=80), txt_irf1.insert(0, 0)
ttk.Label(text="/", font=("Arial", 20), background="#c3c3c3").place(x=317, y=72)
#IQf1
txt_iqf1 = ttk.Entry(root, width=4)
txt_iqf1.place(x=335, y=80), txt_iqf1.insert(0, 0)

#IRf1sh
txt_irfsh1 = ttk.Entry(root, width=4)
txt_irfsh1.place(x=285, y=511), txt_irfsh1.insert(0, 0)
ttk.Label(text="/", font=("Arial", 20), background="#c3c3c3").place(x=317, y=503)
#IQf1sh
txt_iqfsh1 = ttk.Entry(root, width=4)
txt_iqfsh1.place(x=335, y=511), txt_iqfsh1.insert(0, 0)

#IRf2
txt_irf2 = ttk.Entry(root, width=4)
txt_irf2.place(x=545, y=80), txt_irf2.insert(0, 0)
ttk.Label(text="/", font=("Arial", 20), background="#c3c3c3").place(x=577, y=72)
#IQf2
txt_iqf2 = ttk.Entry(root, width=4)
txt_iqf2.place(x=595, y=80), txt_iqf2.insert(0, 0)

#IRf2sh
txt_irf2sh = ttk.Entry(root, width=4)
txt_irf2sh.place(x=545, y=511), txt_irf2sh.insert(0, 0)
ttk.Label(text="/", font=("Arial", 20), background="#c3c3c3").place(x=577, y=503)
#IQf2sh
txt_iqf2sh = ttk.Entry(root, width=4)
txt_iqf2sh.place(x=595, y=511), txt_iqf2sh.insert(0, 0)
    
#Fbix2 Значение частоты на выходе
txt_fbix2 = ttk.Entry(root, width=4)
txt_fbix2.place(x=700, y=110), txt_fbix2.insert(0, Fbix2)
#Fsh1 Значение частоты 1-го гетеродина передатчика
txt_fbix1 = ttk.Entry(root, width=4)
txt_fbix1.place(x=710, y=471), txt_fbix1.insert(0, Fbix1)


#Тестовый график для привязки к кнопке
def graf_of_quadratic_func():
    x_values = range(-10, 11)
    y_values = []
    for x in x_values:
        y = x**2 + 2*x + 1
        y_values.append(y)
    plt.plot(x_values,y_values,marker='*')
    xlabel("X"), ylabel("Y")
    title("y = x**2 + 2*x + 1")
    show()

#test def for call by button click
def draw_shell_way():
    try:
        u = float(input("Enter initial velocity(m/s): "))
        angle = float(input("Enter the angle of launch(degrees): "))
    except ValueError:
        print("Incorrect input.")

    theta = math.radians(angle)
    g = 9.8

    t_flight = 2*u*math.sin(theta)/g
    intervals = frange(0, t_flight, 0.1)
    #coordinates
    x = []
    y = []

    for t in intervals:
        x.append(u*math.cos(theta)*t)
        y.append(u*math.sin(theta)*t - 0.5*g*t*t)
    
    '''Draw traectory of shell'''
    plt.plot(x,y,marker="o")
    plt.xlabel("X")
    plt.ylabel("Y")
    plt.title("Traectory of shell")
    plt.show()
#test def test def for call by button click
def frange(start, final, increment):

    '''Generate anchor points'''
    numbers = []
    while start < final:
        numbers.append(start)
        start += increment
    return numbers   

# Reading data
#Отлажено и теперь рабоает как надо, вызывать так:
#ReadData(txt_fbix2.get(), txt_df.get(), txt_nf.get(), txt_fbx1.get(), txt_fshbix2.get(), txt_fsh1.get(), txt_f1.get(), txt_f2.get(), txt_nfarey.get(), txt_kpp.get())
def ReadData(txt_fbix2, txt_df, txt_nf, txt_fbx1, txt_fshbix2,
             txt_fsh1, txt_f1, txt_f2, txt_nfarey, txt_kpp):
    """
    Читает данные из текстовых полей и присваивает их переменным.
    """
    global Fbix2, DF, NF, Fbx1, Fshbix2, Fsh1, F1, F2, KP, KPP

    try:
        Fbix2 = float(txt_fbix2)
        DF = float(txt_df)
        NF = int(txt_nf)
        Fbx1 = float(txt_fbx1)
        Fshbix2 = float(txt_fshbix2)
        Fsh1 = float(txt_fsh1)
        F1 = float(txt_f1)
        F2 = float(txt_f2)
        KP = int(txt_nfarey)
        KPP = int(txt_kpp)

        print("Данные успешно прочитаны.")
        print(f"Fbix2: {Fbix2}, DF: {DF}, NF: {NF}, Fbx1: {Fbx1}, Fshbix2: {Fshbix2}, Fsh1: {Fsh1}, F1: {F1}, F2: {F2}, KP: {KP}, KPP: {KPP}")

    except ValueError:
        print("Ошибка: Не удалось преобразовать текст в число.")

# Write data
#Уточнить эту строку  txt_iqf2sh.insert(0, str(IrF2))
#Вызов: WriteData(txt_f1, txt_fsh1, txt_f2, txt_irf2, txt_iqf2, txt_irf2sh, txt_iqf2sh)
def WriteData(txt_f1, txt_fsh1, txt_f2, txt_irf2, txt_iqf2, txt_irf2sh, txt_iqf2sh):
    """Записывает значения переменных в текстовые поля GUI."""
    # необходимо создать эти текстовые поля под эти функции и запихать эту функцию в файл с параметарми окна, где будут объявлены поля

    global F1, Fsh1, F2, IqF2, IrF2

    txt_f1.delete(0, ttk.END)  
    txt_f1.insert(0, str(F1))  

    txt_fsh1.delete(0, ttk.END)
    txt_fsh1.insert(0, str(Fsh1))

    txt_f2.delete(0, ttk.END)
    txt_f2.insert(0, str(F2))

    txt_irf2.delete(0, ttk.END)
    txt_irf2.insert(0, str(IqF2))  # Обратите внимание на перестановку IrF2 и IqF2

    txt_iqf2.delete(0, ttk.END)
    txt_iqf2.insert(0, str(IrF2))  # Обратите внимание на перестановку IrF2 и IqF2

    txt_irf2sh.delete(0, ttk.END)
    txt_irf2sh.insert(0, str(IqF2 - IrF2))

    txt_iqf2sh.delete(0, ttk.END)
    txt_iqf2sh.insert(0, str(IrF2))

# Write Data Out
#Вроде всё работает без отклонений
#Вызов: WriteDataOut(txt_q1, txt_qsh1, txt_q2, txt_rqk1, txt_rqk2, txt_rqk1sh, txt_rqk2sh, txt_okgs, txt_okgm)
def WriteDataOut(txt_q1, txt_qsh1, txt_q2, txt_rqk1, txt_rqk2, txt_rqk1sh, txt_rqk2sh, txt_okgs, txt_okgm):
    """
    Записывает значения переменных в текстовые поля GUI.
    """
    global Qk1, Qk1sh, Qk2, RQk1, RQk1sh, RQk2, RQk2sh, Okgs, Okgm
    try:
        txt_q1.delete(0, ttk.END) 
        txt_q1.insert(0, str(Qk1))

        txt_qsh1.delete(0, ttk.END)
        txt_qsh1.insert(0, str(Qk1sh))

        txt_q2.delete(0, ttk.END)
        txt_q2.insert(0, str(Qk2))

        txt_rqk1.delete(0, ttk.END)
        txt_rqk1.insert(0, str(RQk1)) 

        txt_rqk2.delete(0, ttk.END)
        txt_rqk2.insert(0, str(RQk2))

        txt_rqk1sh.delete(0, ttk.END)
        txt_rqk1sh.insert(0, str(RQk1sh))

        txt_rqk2sh.delete(0, ttk.END)
        txt_rqk2sh.insert(0, str(RQk2sh))

        txt_okgs.delete(0, ttk.END)
        txt_okgs.insert(0, str(Okgs))

        txt_okgm.delete(0, ttk.END)
        txt_okgm.insert(0, str(Okgm))
    except:
       print("Непредвиденная ошибка. Функция WriteDataOut().")


# Calc Frequency
# Узнать все ли начальные значения перменных должны быть равны 0, в частности: IqF2, IrF2
#Вызов: CalcFrequency()
def CalcFrequency():
    """
    Вычисляет частоты F2, Fbix1, F1, Fsh1.
    """
    global Akoef2, Fbix2, IqF2, IrF2, F2, Fbix1, Fbx1, F1, Fsh1, Fshbix2
    try:
        Akoef2 = Fbix2 / (IqF2 - IrF2)
        F2 = IrF2 * Akoef2
        Fbix1 = IqF2 * Akoef2
        F1 = Fbx1 - Fbix1
        Fsh1 = Fshbix2 - Fbix1
        print("Частоты успешно расчитаны: ", Akoef2, F2, Fbix1, F1, Fsh1)
    except ZeroDivisionError:
        print("Ошибка деления на 0. Функция CalcFrequency().")

# Calc Frac
#Работает, не ругается. Но надо уточнить все ли значения используемых переменных равны 0
#Вызов: CalcFrac()
#проверить после того как уберу функцию create_window()
def CalcFrac():
    """
    Вычисляет и отображает дроби для частот.
    """
    global Fbx1, F1, Fbix1, Fsh1, txt_irf1, txt_iqf1, txt_irfsh1, txt_iqfsh1
    try:
        if Fbx1 - int(Fbx1) == 0 and F1 - int(F1) == 0:
            IP = int(Fbx1)
            IQ = int(F1)
            SIp = Simple()  # Создаем экземпляры Simple
            SIq = Simple()
            razl(IP, SIp) #from Simple Numbers
            razl(IQ, SIq) #from Simple Numbers
            Ipr = 1
            for ii in range(1, SIp.KN + 1):
                for jj in range(1, SIq.KN + 1):
                    if SIp.P[ii-1] == SIq.P[jj-1]:
                        m = min(SIp.K[ii-1], SIq.K[jj-1])
                        for mm in range(1, m + 1):
                            Ipr *= SIp.P[ii-1]
            IP = IP // Ipr  # Целочисленное деление
            IQ = IQ // Ipr  # Целочисленное деление
            txt_irf1.delete(0, ttk.END)
            txt_irf1.insert(0, str(IP))
            txt_iqf1.delete(0, ttk.END)
            txt_iqf1.insert(0, str(IQ))
        else:
            txt_irf1.delete(0, ttk.END)
            txt_iqf1.delete(0, ttk.END)

        if Fbix1 - int(Fbix1) == 0 and Fsh1 - int(Fsh1) == 0:
            IP = int(Fbix1)
            IQ = int(Fsh1)
            SIp = Simple()  # Создаем экземпляры Simple
            SIq = Simple()
            razl(IP, SIp)
            razl(IQ, SIq)
            Ipr = 1
            for ii in range(1, SIp.KN + 1):
                for jj in range(1, SIq.KN + 1):
                    if SIp.P[ii-1] == SIq.P[jj-1]:
                        m = min(SIp.K[ii-1], SIq.K[jj-1])
                        for mm in range(1, m + 1):
                            Ipr *= SIp.P[ii-1]
            IP = IP // Ipr  # Целочисленное деление
            IQ = IQ // Ipr  # Целочисленное деление
            txt_irfsh1.delete(0, ttk.END)
            txt_irfsh1.insert(0, str(IP))
            txt_iqfsh1.delete(0, ttk.END)
            txt_iqfsh1.insert(0, str(IQ))
        else:
            txt_irfsh1.delete(0, ttk.END)
            txt_iqfsh1.delete(0, ttk.END)
    except:
        print("Непредвиденная ошибка.")

# Calc Quality
# Узнать все ли начальные значения перменных должны быть равны 0, поскольку это влияет на работу функции prom()
# Проверить корректность работы функции prom() из библиотеки rFareyFunctions()
#Вызов: CalcQuality()
def CalcQuality():
    """
    Вычисляет показатели качества.
    """
    global DF, F1, Fsh1, F2, Qk1, OQk1, Qk1sh, OQk1sh, Qk2, OQk2, \
           IR1, IQ1, IR2, IQ2, RR1, RR2, Rg2, RQk2, ORk2, Rg1, RQk1, \
           ORk1, Rg2sh, RQk2sh, ORk2sh, Rg1sh, RQk1sh, ORk1sh, Okgs, Okgm, \
           Fdig, SDF, SF1, SFsh1, SF2, Fbix1, Fbix2, RR1, RR2, Fbx1, Fsh1, F2, Fbix1, RR1, RR2

    if int(DF) - DF != 0:
        # Оптимизация невозможна т.к. DF не целое
        print("Оптимизация невозможна т.к. DF не целое")
        return  # Выходим из функции, если DF не целое

    Fdig = int(DF)
    razl(Fdig, SDF)

    if int(F1) - F1 != 0:
        Qk1 = 0
    else:
        Fdig = int(F1)
        razl(Fdig, SF1)
        Qk1 = 1
        for ii in range(1, SDF.KN + 1):  # Индексация с 1
            for jj in range(1, SF1.KN + 1):  # Индексация с 1
                if SDF.P[ii-1] == SF1.P[jj-1]:  # Индексы в Python начинаются с 0
                    Qk1 *= SDF.P[ii-1] # Индексы в Python начинаются с 0
    OQk1 = Qk1 / DF

    if int(Fsh1) - Fsh1 != 0:
        Qk1sh = 0
    else:
        Fdig = int(Fsh1)
        razl(Fdig, SFsh1)
        Qk1sh = 1
        for ii in range(1, SDF.KN + 1):  # Индексация с 1
            for jj in range(1, SFsh1.KN + 1):  # Индексация с 1
                if SDF.P[ii-1] == SFsh1.P[jj-1]:  # Индексы в Python начинаются с 0
                    Qk1sh *= SDF.P[ii-1] # Индексы в Python начинаются с 0
    OQk1sh = Qk1sh / DF

    if int(F2) - F2 != 0:
        Qk2 = 0
    else:
        Fdig = int(F2)
        razl(Fdig, SF2)
        Qk2 = 1
        for ii in range(1, SDF.KN + 1):  # Индексация с 1
            for jj in range(1, SF2.KN + 1):  # Индексация с 1
                if SDF.P[ii-1] == SF2.P[jj-1]:  # Индексы в Python начинаются с 0
                    Qk2 *= SDF.P[ii-1] # Индексы в Python начинаются с 0
    OQk2 = Qk2 / DF

    # Вычисление расстояний до ближайших комбинационных частот
    try:
        prom(F2 / Fbix1, KPP, IR1, IQ1, IR2, IQ2)
        RR1 = abs(IR1 / IQ1 - F2 / Fbix1)
        RR2 = abs(F2 / Fbix1 - IR2 / IQ2)
        Rg2 = RR1 + RR2
        RQk2 = RR1 if RR1 < RR2 else RR2 # Альтернативный синтаксис if/else
        ORk2 = RQk2 / Rg2

        prom(F1 / Fbx1, KPP, IR1, IQ1, IR2, IQ2)
        RR1 = abs(IR1 / IQ1 - F1 / Fbx1)
        RR2 = abs(F1 / Fbx1 - IR2 / IQ2)
        Rg1 = RR1 + RR2
        RQk1 = RR1 if RR1 < RR2 else RR2
        ORk1 = RQk1 / Rg1

        prom(Fbix2 / F2, KPP, IR1, IQ1, IR2, IQ2)
        RR1 = abs(IR1 / IQ1 - Fbix2 / F2)
        RR2 = abs(Fbix2 / F2 - IR2 / IQ2)
        Rg2sh = RR1 + RR2
        RQk2sh = RR1 if RR1 < RR2 else RR2
        ORk2sh = RQk2sh / Rg2sh

        prom(Fbix1 / Fsh1, KPP, IR1, IQ1, IR2, IQ2)
        RR1 = abs(IR1 / IQ1 - Fbix1 / Fsh1)
        RR2 = abs(Fbix1 / Fsh1 - IR2 / Fsh1) # Ошибка в оригинальном коде: RR2 = Abs(Fbix1 / Fsh1 - IR2 / IQ2)
        Rg1sh = RR1 + RR2
        RQk1sh = RR1 if RR1 < RR2 else RR2
        ORk1sh = RQk1sh / Rg1sh
    except Exception as e: print("\nОшибка в функции CalcQuality:", e)

    Okgs = round(ORk1sh + ORk2sh + ORk1 + ORk2 + OQk1 + OQk2 + OQk1sh, 8)
    Okgm = round(ORk1sh * ORk2sh * ORk1 * ORk2 * OQk1 * OQk2 * OQk1sh, 8)


# cmdD_Click
# Работает без отклонений, но нужно уточниить начальное значение NF, т.к. это ключевой момент для работы этой функции
#Вызов: cmdD_Click()
def cmdD_Click():
    """Уменьшает значения частот Fbx1 и Fshbix2 на величину DF, если nn > 0. """
    #функция левой верхней кнопки со стрелкой, 
    global nn, Fbx1, Fshbix2, DF, txt_nn, txt_fbx1, txt_fshbix2

    try:
        nn = int(txt_nn.get())
        
    except ValueError:
        print("Ошибка: Не удалось преобразовать txt_nn в число.")
        return  # Выходим из функции, если произошла ошибка

    if nn > 0:
        nn -= 1
        txt_nn.delete(0, ttk.END)
        txt_nn.insert(0, str(nn))

        Fbx1 -= int(txt_df.get())
        Fshbix2 -= int(txt_df.get())

        txt_fbx1.delete(0, ttk.END)
        txt_fbx1.insert(0, str(Fbx1))  # Val() не нужен

        txt_fshbix2.delete(0, ttk.END)
        txt_fshbix2.insert(0, str(Fshbix2))  # Val() не нужен

        #cmdCalc_Click()  # Вызываем cmdCalc_Click


# cmdU_Click
# Работает без отклонений, но нужно уточниить начальное значение NF, т.к. это ключевой момент для работы этой функции
#Вызов: cmdU_Click()
def cmdU_Click():
    """Увеличивает значения частот Fbx1 и Fshbix2 на величину DF, если nn < NF - 1."""
    #правая верхняя кнопка
    global nn, NF, Fbx1, Fshbix2, DF, txt_nn, txt_fbx1, txt_fshbix2, txt_df

    try:
        nn = int(txt_nn.get())
        
    except ValueError:
        print("Ошибка: Не удалось преобразовать txtNn в число.")
        return

    if nn < NF - 1:
        nn += 1
        txt_nn.delete(0, ttk.END)
        txt_nn.insert(0, str(nn))

        Fbx1 += int(txt_df.get())
        Fshbix2 += int(txt_df.get())

        txt_fbx1.delete(0, ttk.END)
        txt_fbx1.insert(0, str(Fbx1))

        txt_fshbix2.delete(0, ttk.END)
        txt_fshbix2.insert(0, str(Fshbix2))

        #cmdCalc_Click()


# cmdDown_Click
#
#Вызов: 
def cmdDown_Click(txt_fbix2, txt_df, txt_nf, txt_fbx1, txt_fshbix2, txt_fsh1, txt_f1, txt_f2, txt_nfarey, txt_kpp, 
                  txt_irf2, txt_iqf2, txt_irf2sh, txt_iqf2sh, txt_q1, txt_qsh1, txt_q2, txt_rqk1, txt_rqk2, 
                  txt_rqk1sh, txt_rqk2sh, txt_okgs, txt_okgm):
    """
    Вычисляет и присваивает новые значения IrF2 и IqF2, если не выполняется условие IrF2 = 1 и IqF2 = KP.
    """
    global IrF2, IqF2, IrF2N, IqF2N, KP, KPP

    ReadData(txt_fbix2.get(), txt_df.get(), txt_nf.get(), txt_fbx1.get(),
             txt_fshbix2.get(), txt_fsh1.get(), txt_f1.get(), txt_f2.get(),
             txt_nfarey.get(), txt_kpp.get())  # Обновляем данные из GUI

    if not (IrF2 == 1 and IqF2 == KP):
       
        IrF2, IqF2 = mind_kp(IrF2, IqF2, KP, KPP) # Вызываем функцию mind_kp.  Убедитесь, что IrF2N, IqF2N передаются правильно
      
        CalcFrequency()
        CalcFrac()
        WriteData(txt_f1.get(), txt_fsh1.get(), txt_f2.get(), txt_irf2.get(), txt_iqf2.get(), txt_irf2sh.get(), txt_iqf2sh.get())
        CalcQuality()
        WriteDataOut(txt_q1.get(), txt_qsh1.get(), txt_q2.get(), txt_rqk1.get(), txt_rqk2.get(), txt_rqk1sh.get(), txt_rqk2sh.get(), txt_okgs.get(), txt_okgm.get())


# cmdUp_Click
#
#Вызов:
def cmdUp_Click(txt_fbix2, txt_df, txt_nf, txt_fbx1, txt_fshbix2, txt_fsh1, txt_f1, txt_f2, txt_nfarey, txt_kpp, 
                  txt_irf2, txt_iqf2, txt_irf2sh, txt_iqf2sh, txt_q1, txt_qsh1, txt_q2, txt_rqk1, txt_rqk2, 
                  txt_rqk1sh, txt_rqk2sh, txt_okgs, txt_okgm):
    """
    Вычисляет и присваивает новые значения IrF2 и IqF2, если IrF2N < IqF2N.
    """
    global IrF2, IqF2, IrF2N, IqF2N, KP, KPP

    ReadData(txt_fbix2.get(), txt_df.get(), txt_nf.get(), txt_fbx1.get(),
             txt_fshbix2.get(), txt_fsh1.get(), txt_f1.get(), txt_f2.get(),
             txt_nfarey.get(), txt_kpp.get())  # Обновляем данные из GUI

    IrF2N, IqF2N = maxd_kp(IrF2, IqF2, KP, KPP)  # Вызываем функцию maxd_kp

    if IrF2N < IqF2N:
        IrF2 = IrF2N
        IqF2 = IqF2N

        CalcFrequency()
        CalcFrac()
        WriteData(txt_f1.get(), txt_fsh1.get(), txt_f2.get(), txt_irf2.get(), txt_iqf2.get(), txt_irf2sh.get(), txt_iqf2sh.get())
        CalcQuality()
        WriteDataOut(txt_q1.get(), txt_qsh1.get(), txt_q2.get(), txt_rqk1.get(), txt_rqk2.get(), txt_rqk1sh.get(), txt_rqk2sh.get(), txt_okgs.get(), txt_okgm.get())


#cmdCalc_Click
#Ошибки в CalcFrequency и CalcQuality из-за кривы значений переменных начальных, надо узнавать с какие ставить данные, 1 не прокатывают
#
def cmdCalc_Click(txt_fbix, txt_df, txt_nf, txt_fbx1, txt_fshbix2, txt_fsh1, txt_f1, txt_f2, txt_nfarey, txt_kpp, 
                  txt_irf2, txt_iqf2, txt_irf2sh, txt_iqf2sh, txt_q1, txt_qsh1, txt_q2, txt_rqk1, txt_rqk2,
                   txt_rqk1sh, txt_rqk2sh, txt_okgs, txt_okgm):
    """
    Основная функция, выполняющая расчеты и запись данных.
    """
    global Q2, IrF2, IqF2, F2, Fbix2, KP # Объявляем глобальные переменные, которые будем изменять

    ReadData(txt_fbix.get(), txt_df.get(), txt_nf.get(), txt_fbx1.get(),
             txt_fshbix2.get(), txt_fsh1.get(), txt_f1.get(), txt_f2.get(),
             txt_nfarey.get(), txt_kpp.get())  # Вызываем функцию ReadData, передавая значения из GUI

    Q2 = F2 / (F2 + Fbix2)  # Вычисляем Q2

    dcep(Q2, KP, IrF2, IqF2) # Вызываем функцию DCEP, передавая Q2, KP, IrF2, IqF2 в Функциях Фарея лежит

    CalcFrequency()  # Вызываем функцию CalcFrequency

    CalcFrac()  # Вызываем функцию CalcFrac

    WriteData(txt_f1, txt_fsh1, txt_f2, txt_irf2, txt_iqf2, txt_irf2sh, txt_iqf2sh)  # Вызываем функцию WriteData

    CalcQuality()  # Вызываем функцию CalcQuality

    WriteDataOut(txt_q1, txt_qsh1, txt_q2, txt_rqk1, txt_rqk2, txt_rqk1sh, txt_rqk2sh, txt_okgs, txt_okgm)  # Вызываем функцию WriteDataOut


#cmdSave_Click
#Пишет данные в файл Calcuated_Data, при каждом вызове добавляет новые данные в файл. Если файла нет в папке программы, он автоматически создаётся.
#Работает исправно
def cmdSave_Click():
    """
    Записывает данные в файл с номером NFile.
    """
    global NFile, txt_nn, KP, KPP, Okgs, Okgm, Fbx1, F1, Fbix1, F2, Fbix2, txt_q1, txt_q2, txt_rqk1, txt_rqk2 
    global txt_irf1, txt_iqf1, IrF2, IqF2, Fbix2, Fsh1, Fshbix2, txt_qsh1, txt_rqk1sh, txt_rqk2sh, txt_irfsh1, txt_iqfsh1, txt_irf2sh, txt_iqf2sh 
    try:
        with open("Calcuated_Data", "a", encoding="utf-8") as f:  # Открываем файл для добавления данных ("a" - append)
            f.write(f"Вариант структуры  Nt={txt_nn.get()}  Kp={KP}  Kpp={KPP}\n")
            f.write(f"  Показатели качества: Ks={Okgs} Km={Okgm}\n")
            f.write("   Частоты приемника:\n")
            f.write(f"   Fbx1={Fbx1} F1={F1} Fbix1={Fbix1} F2={F2} Fbix2={Fbix2}\n")
            f.write("      Качественные параметры приемника:\n")
            f.write(f"   Q1:={txt_q1.get()} Q2={txt_q2.get()} R1={txt_rqk1.get()} R2={txt_rqk2.get()}\n")
            f.write("      Дроби Фарея:\n")
            f.write(f"      Ir(1)/Iq(1)={txt_irf1.get()}/{txt_iqf1.get()}    Ir(2)/Iq(2)={IrF2}/{IqF2}\n")
            f.write("\n")
            f.write("   Частоты передатчика:\n")
            f.write(f"   F'bx1={Fbix2} F2={F2} Fbix1={Fbix1} F'1={Fsh1} F'bix2={Fshbix2}\n")
            f.write("      Качественные параметры передатчика:\n")
            f.write(f"   Q'1:={txt_qsh1.get()} Q2={txt_q2.get()} R'1={txt_rqk1sh.get()} R'2={txt_rqk2sh.get()}\n")
            f.write("      Дроби Фарея:\n")
            f.write(f"      Ir'(1)/Iq'(1)={txt_irfsh1.get()}/{txt_iqfsh1.get()}    Ir(2)/Iq(2)={txt_irf2sh.get()}/{txt_iqf2sh.get()}\n")
            f.write("\n")
            f.close()

    except Exception as e:
        print(f"Ошибка при записи в файл: {e}")

#Save_as
#
#
def save_as():
    file_path = filedialog.asksaveasfilename(initialfile = 'Calculated_Data.txt', defaultextension=".txt",filetypes=[("All Files","*.*"),("Text Documents","*.txt")])
    if file_path:
        with open(file_path, "w", encoding="utf-8") as f:
            f.write(f"Вариант структуры  Nt={txt_nn.get()}  Kp={KP}  Kpp={KPP}\n")
            f.write(f"  Показатели качества: Ks={Okgs} Km={Okgm}\n")
            f.write("   Частоты приемника:\n")
            f.write(f"   Fbx1={Fbx1} F1={F1} Fbix1={Fbix1} F2={F2} Fbix2={Fbix2}\n")
            f.write("      Качественные параметры приемника:\n")
            f.write(f"   Q1:={txt_q1.get()} Q2={txt_q2.get()} R1={txt_rqk1.get()} R2={txt_rqk2.get()}\n")
            f.write("      Дроби Фарея:\n")
            f.write(f"      Ir(1)/Iq(1)={txt_irf1.get()}/{txt_iqf1.get()}    Ir(2)/Iq(2)={IrF2}/{IqF2}\n")
            f.write("\n")
            f.write("   Частоты передатчика:\n")
            f.write(f"   F'bx1={Fbix2} F2={F2} Fbix1={Fbix1} F'1={Fsh1} F'bix2={Fshbix2}\n")
            f.write("      Качественные параметры передатчика:\n")
            f.write(f"   Q'1:={txt_qsh1.get()} Q2={txt_q2.get()} R'1={txt_rqk1sh.get()} R'2={txt_rqk2sh.get()}\n")
            f.write("      Дроби Фарея:\n")
            f.write(f"      Ir'(1)/Iq'(1)={txt_irfsh1.get()}/{txt_iqfsh1.get()}    Ir(2)/Iq(2)={txt_irf2sh.get()}/{txt_iqf2sh.get()}\n")
            f.write("\n")
            f.close()
    
    #Запуск окна



root.mainloop()