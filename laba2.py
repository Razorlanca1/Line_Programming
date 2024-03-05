import sys

#input = lambda: sys.stdin.readline()[:-1]
mass = lambda: list(map(int, input().strip().split()))


def get_normal_ints(table):
    for i in range(len(table)):
        for j in range(len(table[0])):
            table[i][j] = round(table[i][j], 5)
    return table


def get_table():
    print("Введите количество уравнений(не считай Z) и количество неизвестных через пробел")
    n, m = mass()
    table = []
    sings = []
    #print("Введите уравнения в формате: \"10x1 5x2 ... 9xn > 11\"")
    for j in range(n):
        table.append([0] * (m + 1))
        c = input().split()
        for i in range(len(c)):
            if i == len(c) - 2:
                sings.append(c[i])
            elif i == len(c) - 1:
                table[j][-1] = int(c[i])
            else:
                if "x" in c[i]:
                    k = c[i].split("x")
                    if k[0] == "":
                        k[0] = 1
                    elif k[0] == "-":
                        k[0] = -1
                    table[j][int(k[1]) - 1] = int(k[0])
                else:
                    table[j][i] = int(c[i])
    #print("Введите Z в формате: \"0 5 0 2 1 ... -10\"")
    table.append(list(map(lambda x: -x, mass())))
    while len(table[-1]) < m:
        table[-1].append(0)
    table[-1].append(0)
    #print("Введите неизвестные, которые ≥ 0 в формате: \"1 3 ... n\"")
    not_negative = []
    for i in input().split():
        not_negative.append(int(i) - 1)
    #print("Введите 1, если Z → MIN, 0 в противном случае")
    min = bool(int(input()))

    return [table, sings, not_negative, min]


def get_canon_view(table, signs, not_negative_x, min=False, dual=False):
    method = 0

    b = []
    for i in range(len(table)):
        b.append(table[i].pop())

    if min:
        for i in range(len(table[0])):
            table[-1][i] *= -1

    for x in range(len(table[0])):
        if x in not_negative_x:
            continue
        for i in range(len(table)):
            table[i].append(-table[i][x])

    for i in range(len(table) - 1):
        if signs[i] == "=":
            continue
        if signs[i] == ">":
            table[i] = list(map(lambda x: -x, table[i]))
            b[i] *= -1
        for j in range(len(table)):
            if i == j:
                table[j].append(1)
            else:
                table[j].append(0)

    for i in range(len(b)):
        table[i].append(b[i])
        if b[i] < 0:
            if dual:
                method = 2
                continue
            method = 1
            table[i] = list(map(lambda x: -x, table[i]))

    if method != 1:
        was = 0
        for i in range(len(table)):
            for j in range(len(table[0]) - 1):
                if table[i][j] == 1:
                    for h in range(len(table)):
                        if h == i:
                            continue
                        if table[h][j] != 0:
                            break
                    else:
                        was += 1
                        break

        if was != len(table) - 1:
            method = 1

    print()
    if method == 0:
        print("Simplex")
    elif method == 1:
        print("M-method")
    elif method == 2:
        print("Dual Simplex")
    print()

    return [table, method]


def simplex(table, min=False, x=None, iter=0, M=False, message=False):
    if x is None:
        x = [i for i in range(len(table[0]) - len(table), len(table[0]) - 1)]
    while 1:
        get_normal_ints(table)
        if message:
            print("Iteration:", iter)
            for i in range(len(table)):
                if i == len(table) - 1:
                    print("Z", end=" ")
                else:
                    print(f"x{x[i] + 1}", end=" ")
                print(*table[i])
            print()
        m, ind = 0, -1
        for i in range(len(table[0]) - 1):
            if table[-1][i] < m:
                m = table[-1][i]
                ind = i
        if ind == -1:
            if message:
                print("Result: ")
                for i in range(len(x)):
                    print(f"x{x[i] + 1} = {table[i][-1]}")

                for i in range(len(table[0]) - 1):
                    if i not in x:
                        print(f"x{i + 1} = 0")
                if min:
                    print(f"Z = {-table[-1][-1]} - доход от реализации продукции")
                else:
                    print(f"Z = {table[-1][-1]} - доход от реализации продукции")

                if not M:
                    print()
                    for i in range(len(table[0]) - len(table)):
                        if i in x:
                            print(f"Оптимальное количество х{i + 1} - {table[x.index(i)][-1]}")
                        else:
                            print(f"Оптимальное количество х{i + 1} - 0")
                    print()
                    for i in range(len(table[0]) - len(table), len(table[0]) - 1):
                        if i not in x:
                            print(f"Ценность ресурса {i + 1 - len(table[0]) + len(table)} - {table[-1][i]}")
                        else:
                            print(f"Ресурс {i + 1 - len(table[0]) + len(table)} - не дефицитный")

            return [table, x]

        q = -1
        for i in range(len(table) - 1):
            if table[i][ind] > 0:
                if q == -1 or table[i][-1] / table[i][ind] < table[q][-1] / table[q][ind]:
                    q = i
        if q == -1:
            print("Z → ∞")
            return []
        x[q] = ind
        k = table[q][ind]
        for j in range(len(table[q])):
            table[q][j] /= k

        for i in range(len(table)):
            if i == q:
                continue
            k = -table[i][ind]
            for j in range(len(table[0])):
                table[i][j] += table[q][j] * k
        iter += 1


if __name__ == "__main__":
    table, sings, not_negative, min = get_table()
    table, method = get_canon_view(table, sings, not_negative, min)
    if method != 0:
        print("Not Simplex method")
    else:
        simplex(table, min)


"""
simplex([[2, -1, 1, 1, 0, 0, 1],
         [-4, 2, -1, 0, 1, 0, 2],
         [3, 0, 1, 0, 0, 1, 5],
         [1, -1, -3, 0, 0, 0, 0]])

3 6
2x1 -1x2 1x3 1x4 = 1
-4x1 2x2 -1x3 1x5 = 2
3x1 1x3 1x6 = 5
-1 1 3 0 0 0
1 2 3 4 5 6
0

3 3
2x1 -x2 x3 < 1
-4x1 +2x2 -x3 < 2
3x1 x3 < 5
-1 1 3
1 2 3
0

3 3
2x1 3x2 6x3 < 240
4x1 2x2 4x3 < 200
4x1 6x2 8x3 < 160
4 5 4
1 2 3
0

2 4
4x1 1x2 1x3 = 8
-1x1 1x2 1x4 = 3
3 4 0 0
1 2 3 4
0

2 2
4x1 1x2 < 8
1x1 -1x2 > -3
3 4
1 2
0

1x1 - 1x2 - 1x4 = -3
-1x1 + 1x2 + 1x4 = 3

3 3 
1x1 2x2 1x3 < 5
3x1 -4x2 0x3 > 6
1x1 2x2 7x3 > 10 
1 2 3 
1 2 3 
1


2 2
1x1 2x2 = 1
2x1 2x1 = 3
1 
1 2
0

2 4
1x1 3x2 2x3 2x4 = 3
2x1 2x2 1x3 x4 = 3
5 3 4 -1
1 2 3 4
0

3 4
3x1 5x2 -x3 -1x4 < 2
1x1 -5x2 -7x3 -3x4 < 5
-1x1 4x2 -5x3 -7x4 < 7
2 4 6 8
1 2 3 4
0

2 4
3x1 5x2 x3 x4 < 2
3x1 5x2 x3 x4 < 2
2 4 6 8
1 2 3 4
0

2 4
-x1 -3x2 -2x3 -2x4 = 3
-2x1 -2x2 -x3 -x4 = 3
-5 -3 -4 1
1 2 3 4
0

3 3
2 1 1 < 1
4 2 -1 < 2
3 0 1 < 5
-1 1 3
1 2 3
0
"""