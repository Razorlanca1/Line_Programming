mass = lambda: list(map(int, input().strip().split()))


def northwest_corner(a, b, c):
    base = []
    a = a[::]
    b = b[::]
    print("Решение допустимое")
    if sum(a) < sum(b):
        a.append(sum(b) - sum(a))
        c.append([0] * len(b))
    if sum(a) > sum(b):
        b.append(sum(b) - sum(a))
        [c[i].append(0) for i in range(len(a))]

    x = [[0] * len(b) for _ in range(len(a))]
    was = False

    i, j = 0, 0
    while i < len(a) and j < len(b):
        x[i][j] = min(a[i], b[j])
        base.append((i, j))
        if a[i] < b[j]:
            b[j] -= a[i]
            i += 1
        elif a[i] > b[j]:
            a[i] -= b[j]
            j += 1
        else:
            if not was:
                print("Решение вырожденное")
                print("Решение не базисное")
            was = True
            i += 1

    if not was:
        print("Решение не вырожденное")
        print("Решение базисное")
    return[x, sum([x[i][j] * c[i][j] for i in range(len(a)) for j in range(len(b))]), base]


"""a = [200, 350, 300]
b = [270, 130, 190, 150, 110]
c = [[24, 50, 45, 27, 15],
     [20, 32, 40, 35, 30],
     [22, 16, 18, 28, 20]]"""
if __name__ == "__main__":
    if 1:
        a = [100, 250, 200, 300]
        b = [200, 200, 100, 100, 250]
        c = [[10, 7, 4, 1, 4],
             [2, 7, 10, 6, 11],
             [8, 5, 3, 2, 2],
             [11, 8, 12, 16, 13]]
    else:
        a = mass()
        b = mass()
        c = [mass() for _ in range(len(a))]

    x, z, base = northwest_corner(a, b, c)
    for i in range(len(a)):
        tec = 0
        print(f"Поставщик {i + 1} поставил", end=" ")
        for j in range(len(b)):
            tec += x[i][j] * c[i][j]
            if x[i][j]:
                print(f"{x[i][j]} груза {j + 1}-ому потребителю,", end=" ")
        print(f"на общую сумму {tec}.")
    print(f"Начальное значение целевой функции - {z}")