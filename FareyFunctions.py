
#Нужно протестировать все функции и отладить их!!!!!

import math

# Глобальные переменные (старайтесь избегать в реальных проектах).
NFile = 0  # int
Str1 = ""  # str


def maxd(IR: int, IQ: int, NMH: int):
    """
    Находит ближайшую большую дробь (IRP/IQP) к заданной дроби (IR/IQ) Фарея индекса NMH.
    Оптимизированная версия.

    Args:
        IR: Числитель заданной дроби.
        IQ: Знаменатель заданной дроби.
        NMH: Индекс Фарея (максимальный знаменатель).

    Returns:
        Кортеж (IRP, IQP): Числитель и знаменатель ближайшей большей дроби Фарея.  Возвращает (1, NMH) если IR == 0.
    """
    global Str1  # Используем глобальную переменную Str1
    if IR == 0:
        return 1, NMH  

    # Вычисление границ. Избавляемся от дублирования вычислений.
    temp = NMH / IQ * IR + 1 / IQ
    MB = int(temp)
    MH = MB - IR + 1

    Str1 += f" п/п MAXDD: MH={MH} ,  MB={MB}\n"  # Отладочная информация

    # Оптимизированный поиск знаменателя J.  Используем range.
    for J in range(MH, MB + 1):
        if (IQ * J - 1) % IR == 0:
            Str1 += f" п/п MAXDD: J={J}\n"  # Отладочная информация (перенесено сюда)
            # Вычисление числителя и знаменателя. Избавляемся от дублирования.
            IQP = int((IQ / IR) * J - (1 / IR))
            B = (IQ / IR) * J - (1 / IR)  # Сохраняем значение, чтобы не вычислять снова.
            C = (IR / IQ) * IQP + (1 / IQ)
            IRP = int(C)

            Str1 += f" п/п MAXDD: IRP={C} ,  IQP={B}\n"  # Отладочная информация
            return IRP, IQP

    else:
        # Если не найдено.  Лучше бросать исключение, чем просто печатать.
        print("Внимание! Ошибка в п/п MAXD")
        print("Дробь Farey найдена неверно !")
        return None, None  # Или бросить исключение: raise ValueError("Дробь Фарея не найдена")  Возвращаем None, None чтобы обозначить ошибку.



def mind(IR: int, IQ: int, NMH: int):
    """
    Находит ближайшую меньшую дробь (IRP/IQP) к заданной дроби (IR/IQ) Фарея индекса NMH.

    Args:
        IR: Числитель заданной дроби.
        IQ: Знаменатель заданной дроби.
        NMH: Индекс Фарея (максимальный знаменатель).

    Returns:
        Кортеж (IRP, IQP): Числитель и знаменатель ближайшей меньшей дроби Фарея.
    """
    global Str1  # Используем глобальную переменную Str1
    if IR == 0:
        # Если числитель равен 0, ближайшая меньшая дробь - 0/1.
        IRP = 0
        IQP = 1
        return IRP, IQP
    else:
        # Вычисление верхней и нижней границ для знаменателя искомой дроби.
        MB = int((NMH / IQ) * IR - (1 / IQ))
        MH = MB - IR + 1

        Str1 += f" п/п MINDD: MH={MH} ,  MB={MB}\n"  # Добавляем отладочную информацию

        # Поиск подходящего знаменателя J в заданном диапазоне.
        for J in range(MH, MB + 1):
            # Проверяем, делится ли (IQ * J + 1) на IR без остатка.
            if (IQ * J + 1) % IR == 0:
                break  # Нашли подходящий знаменатель, прерываем цикл
        else:
            # Если цикл завершился без break, значит, подходящий знаменатель не был найден.
            print("Внимание! Ошибка в п/п MIND")
            print("Дробь Farey найдена неверно !")
            return None, None  # Или бросить исключение: raise ValueError("Дробь Фарея не найдена")

        Str1 += f" п/п MINDD: J={J}\n"  # Добавляем отладочную информацию

        # Вычисление знаменателя и числителя искомой дроби.
        IQP = int((IQ / IR) * J + (1 / IR))
        B = (IQ / IR) * J + (1 / IR)
        IRP = int((IR / IQ) * IQP - (1 / IQ))
        C = (IR / IQ) * IQP - (1 / IQ)

        Str1 += f" п/п MINDD: IRP={C} ,  IQP={B}\n"  # Добавляем отладочную информацию

        return IRP, IQP



def dcep(AL, IFAR, IPG, IQG):
    """
    Находит диофантово приближение дроби AL в классе дробей Фарея индекса IFAR.

    Args:
        AL: Дробь для приближения.
        IFAR: Индекс Фарея (максимальный знаменатель).

    Returns:
        Кортеж (IPG, IQG): Числитель и знаменатель дроби Фарея, аппроксимирующей AL.
    """
    global Str1  # Используем глобальную переменную Str1

    IPM = 1
    IQM = 0
    IQ0 = 1
    A = AL

    if A >= 0:
        IP0 = int(A)
        Str1 = ""  # Очищаем глобальную строку

        while True:  # Заменяем Do...Loop на while True
            if A == 0:
                break  # Завершаем цикл, если A равно 0

            Str1 += f" п/п DCEP:A={A}\n"  # Добавляем отладочную информацию

            A = 1 / A
            if A > 2147483647:  # Проверка на переполнение.
                break

            IC = int(A)
            A = A - IC

            if IC * IQ0 + IQM > IFAR:
                break  # Завершаем цикл, если знаменатель превышает IFAR

            IQ = IC * IQ0 + IQM
            IP = IC * IP0 + IPM

            if IQ < 0:
                break  # Завершаем цикл, если знаменатель отрицательный

            Str1 += (
                f" п/п DCEP:IP/IQ={IP}/{IQ} , IP0/IQ0={IP0}/{IQ0} ,  IPM/IQM={IPM}/{IQM}\n"
            )  # Добавляем отладочную информацию

            IPM = IP0
            IQM = IQ0
            IQ0 = IQ
            IP0 = IP

        IPG = IP0
        IQG = IQ0
        return IPG, IQG  # Возвращаем найденные значения
    else:
        return None, None 



def prom(AL: float, IFAR: int, IPG: int, IQG: int, IPN: int, IQN: int):
    """
    Находит двойное диофантово приближение дроби AL<=0 в классе дробей Фарея
    индекса IFAR с помощью алгоритма Евклида и алгоритма поиска
    промежуточных дробей.

    Args:
        AL: Любое действительное число (<= 0).
        IFAR: Индекс промежуточной дроби.
    """
    IPM = 1
    IQM = 0
    IQ0 = 1
    A = AL

    if A >= 0:
        IP0 = math.floor(A)
        while True:
            if A == 0:
                break
            A = 1 / A
            if A > 2147483647:
                break
            IC = math.floor(A)
            A = A - IC
            if IC * IQ0 + IQM > IFAR:
                break
            IQ = IC * IQ0 + IQM
            IP = IC * IP0 + IPM
            if IQ < 0:
                break
            IPM = IP0
            IQM = IQ0
            IQ0 = IQ
            IP0 = IP

        IPG = IP0
        IQG = IQ0
        IP1 = IPM
        IQ1 = IQM
        I = 0

        while True:
            I = I + 1
            IPN = IP1
            IQN = IQ1
            IP1 = IPM + I * IPG
            IQ1 = IQM + I * IQG
            if IQ1 == IFAR:
                IPN = IP1
                IQN = IQ1
                break
            if IQ1 < 0 or IQ1 > IFAR:
                # Заменяем GoTo Vixod на break, так как переменные уже установлены
                break

    return IPG, IQG, IPN, IQN



def maxd_kp(IRR: int, IQQ: int, KP: int, NMH: int):
    """
    Находит ближайшую большую дробь (IRP/IQP) к заданной дроби (IR/IQ) Фарея индекса NMH,
    исключая дроби индекса KP и меньше.

    Args:
        IRR: Числитель заданной дроби.
        IQQ: Знаменатель заданной дроби.
        NMH: Индекс Фарея (максимальный знаменатель).
        KP: Индекс, дроби которого нужно исключить (IQP > KP)."""

    IR = IRR
    IQ = IQQ

    if IR == 0:
        return 1, NMH
    else:
        while True:  # Заменяем GoTo на цикл while True

            MB = int((NMH / IQ) * IR + (1 / IQ))
            MH = MB - IR + 1

            for J in range(MH, MB + 1):
                if (IQ * J - 1) % IR == 0:
                    break
            else:
                print("Внимание! Ошибка в п/п MAXD_KP")
                print("Дробь Farey найдена неверно !")
                return None, None  # Возвращаем None, None, чтобы обозначить ошибку

            IQP = int((IQ / IR) * J - (1 / IR))
            IRP = int((IR / IQ) * IQP + (1 / IQ))

            if IQP <= KP:
                IR = IRP
                IQ = IQP
                continue  # Продолжаем цикл (эквивалентно GoTo 40)
            else:
                return IRP, IQP



def mind_kp(IRR: int, IQQ: int, KP: int, NMH: int):
    """
    Находит ближайшую меньшую дробь (IRP/IQP) к заданной дроби (IRR/IQQ) Фарея индекса NMH,
    исключая дроби индекса KP и меньше.

    Args:
        IRR: Числитель заданной дроби.
        IQQ: Знаменатель заданной дроби.
        NMH: Индекс Фарея (максимальный знаменатель).
        KP: Индекс, дроби которого нужно исключить (IQP > KP). Ограничение KP <= NMH
    """

    IR = IRR
    IQ = IQQ

    if IR == 0:
        return 0, 1
    else:
        while True:  # Заменяем GoTo на цикл while True

            MB = int((NMH / IQ) * IR - (1 / IQ))
            MH = MB - IR + 1

            for J in range(MH, MB + 1):
                if (IQ * J + 1) % IR == 0:
                    break
            else:
                print("Внимание! Ошибка в п/п MIND_KP")
                print("Дробь Farey найдена неверно !")
                return None, None  # Возвращаем None, None, чтобы обозначить ошибку

            IQP = int((IQ / IR) * J + (1 / IR))
            IRP = int((IR / IQ) * IQP - (1 / IQ))

            if IQP <= KP:
                IR = IRP
                IQ = IQP
                continue  # Продолжаем цикл (эквивалентно GoTo 40)
            else:
                return IRP, IQP
            
if __name__ == "__main__":
    
    IrF2 = 1
    IqF2 = 1
    KP = 1
    KPP = 10
    IRP = 0
    IQP = 0

    print(maxd_kp(IrF2, IqF2, KP, KPP))
    print(IRP, IQP)