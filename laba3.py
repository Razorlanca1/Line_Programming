from laba2 import *


def M_method(table, min=False, message=False):
    ret = []
    for i in range(len(table)):
        ret.append(table[i].pop())

    ret.append(-sum(ret))

    for i in range(len(table)):
        table[i] += [0] * (len(table) - 1)
        if i != len(table) - 1:
            table[i][len(table[i]) - len(table) + i + 1] = 1

    table.append([0] * len(table[0]))
    for i in range(len(table) - 2):
        for j in range(len(table[i]) - len(table) + 2):
            table[-1][j] -= table[i][j]

    for i in range(len(table)):
        table[i].append(ret[i])

    x = [i for i in range(len(table[0]) - len(table) + 1, len(table[0]) - 1)]
    y = set([i for i in range(len(table) - 2)])
    removed = set()

    iter = 0
    while 1:
        get_normal_ints(table)
        m, ind = 0, -1
        zero = True
        for i in range(len(table[0]) - 1):
            if i not in removed and abs(table[-1][i]) > 1e-9:
                zero = False
            if table[-1][i] < m and abs(table[-1][i]) > 1e-9:
                m = table[-1][i]
                ind = i
        if ind == -1:
            if zero:
                table.pop()
                for i in range(len(table)):
                    table[i] = table[i][:-len(table)] + [table[i][-1]]
                table = simplex(table, min, x, iter, M=True, message=message)
            else:
                print("Cистема ограничений исходной задачи несовместна в области допустимых решений")
                table = []
            return table

        if message:
            print("Iteration:", iter)
            for i in range(len(table)):
                if i > len(table) - 3:
                    print("Z", end=" ")
                else:
                    print(f"x{x[i] + 1}", end=" ")
                for j in range(len(table[i])):
                    if j not in removed:
                        print(table[i][j], end=" ")
                print()
            print()

        q = -1
        for i in range(len(table) - 2):
            if table[i][ind] > 0:
                if q == -1 or table[i][-1] / table[i][ind] < table[q][-1] / table[q][ind]:
                    q = i
        if q == -1:
            print("Z → ∞")
            return []
        if q in y:
            y.remove(q)
            removed.add(x[q])
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
    if method == 1:
        M_method(table, min, message=True)
    else:
        simplex(table, min, message=True)


"""
3 3 
1x1 2x2 1x3 < 5
3x1 -4x2 0x3 > 6
1x1 2x2 7x3 > 10 
1 2 3 
1 2 3 
1

"""