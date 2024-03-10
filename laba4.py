from laba3 import *


def dual_simplex(table, min=False, x=None, iter=0, M=False, message=False):
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
        m, q = 0, -1
        for i in range(len(table) - 1):
            if table[i][-1] < m:
                m = table[i][-1]
                q = i
        if q == -1:
            return simplex(table, min=min, x=x, iter=iter, M=M, message=message)

        ind = -1
        for i in range(len(table[0]) - 1):
            if table[q][i] < 0:
                if ind == -1 or abs(table[-1][i] / table[q][i]) < abs(table[-1][ind] / table[q][ind]):
                    ind = i
        if ind == -1:
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


def Gomori(table, min=False, x=None, iter=0, message=False):
    while 1:
        for i in range(len(table) - 1):
            if table[i][-1] < 0:
                print("Dual\n")
                table, x = dual_simplex(table, min, x, iter, True, message)
                break
        else:
            print("Simplex\n")
            table, x = simplex(table, min, x, iter, True, message)

        if message:
            print()

        drob, ind = -1, 0
        for i in range(len(table) - 1):
            if table[i][-1] % 1 and drob < table[i][-1] - int(table[i][-1]):
                ind, drob = i, table[i][-1] - int(table[i][-1])

        if drob == -1:
            return [table, x]

        for i in range(len(table)):
            table[i].insert(len(table[-1]) - 1, 0)

        x.append(len(table[0]) - 2)
        table.insert(len(table) - 1, list(map(lambda x: int(x) - x, table[ind])))
        table[-2][-2] = 1


if __name__ == "__main__":
    table, sings, not_negative, min = get_table()
    table, method = get_canon_view(table, sings, not_negative, min, dual=True)
    if input("Гомори?\n") != '0':
        Gomori(table, min, message=True)
    elif method == 1:
        table, x = M_method(table, min)
    elif method == 2:
        dual_simplex(table, min, message=True)
    else:
        simplex(table, min)

"""
3 3 
1x1 2x2 1x3 < 5
3x1 -4x2 0x3 > 6
1x1 2x2 7x3 > 10 
1 2 3 
1 2 3 
1

2 5
x1 x2 -x3 1x4  = 4
-x1 5x2 -x3 1x5 = -5
2 -1 -5
1 2 3 4 5
0

2 2
5x1 2x2 < 20
8x1 4x2 < 38
7 3
1 2
0


"""