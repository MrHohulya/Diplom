
#Здесь вроде всё работает, в доработке не нуждается

import math

class Simple:
    def __init__(self):
        self.P = [0] * 20
        self.K = [0] * 20
        self.KN = 0

def razl(N, S):
    if N <= 0: return  # Handle non-positive numbers

    NP = N
    S.KN = 0
    L = False
    Lim = int(math.sqrt(NP))

    i = 2 # Start with 2, the first prime

    while i <= Lim:
        J = 0
        while NP % i == 0:
            NP //= i
            L = True
            J += 1

        if J:
            S.P[S.KN] = i # use S.KN as index and increase after usage
            S.K[S.KN] = J
            S.KN += 1

        i += 1 if i == 2 else 2 # Increment by 1 if i is 2, else by 2

    if NP > 1:
        S.P[S.KN] = NP
        S.K[S.KN] = 1
        S.KN += 1

    if not L:
        S.P[0] = N
        S.K[0] = 1
        S.KN = 1

#тестовый запуск
if __name__ == "__main__":
    N = 120
    S = Simple()
    razl(N, S)

    print(f"\nФакторизация {N}:\n")
    for i in range(S.KN):
        print(f"{S.P[i]}^{S.K[i]}", end="\n")
    print()