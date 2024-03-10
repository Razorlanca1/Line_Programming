from laba5 import *


def get_potential(a, b, c, base):
    u = [-1e9] * len(a)
    v = [-1e9] * len(b)
    u[0] = 0
    was = set()
    while -1e9 in u or -1e9 in v:
        for i, j in base:
            if (i, j) in was:
                continue
            if u[i] != -1e9:
                v[j] = c[i][j] - u[i]
            elif v[j] != -1e9:
                u[i] = c[i][j] - v[j]
            else:
                continue
            was.add((i, j))
    return [u, v]


def potential_method(a, b, c):
    x, z, base = northwest_corner(a, b, c)
    iter = 0
    while 1:
        print("Iteration:", iter)
        row_format = "{:>15}" * (len(b) + 1)
        u, v = get_potential(a, b, c, base)
        print(row_format.format("", *list(map(lambda x: f"b{x}", b))))
        print(row_format.format("", *v))
        for team, row in zip(list(map(lambda x: f"a{x[0]} {x[1]}", zip(a, u))), x):
            print(row_format.format(team, *row))

        print("U:", *u)
        print("V:", *v)
        sbase = set(base)
        ci, cj, mdc = -1, -1, -1e9
        for i in range(len(c)):
            for j in range(len(c[0])):
                dc = u[i] + v[j] - c[i][j]
                if (i, j) not in sbase and dc > 0 and (ci == -1 or (mdc < dc or mdc == dc and c[i][j] < c[ci][cj])):
                    ci, cj, mdc = i, j, dc
        if ci == -1:
            return [x, z, base]

        ac = [[] for _ in range(len(a))]
        bc = [[] for _ in range(len(b))]
        for i, j in base:
            ac[i].append((i, j))
            bc[j].append((i, j))
        ac[ci].append((ci, cj))
        bc[cj].append((ci, cj))

        ty = 0
        q = [((ci, cj), 0)]
        new_base = []
        was = set()
        fin = False
        tec_dfs = 0
        while q:
            t, dfs = q.pop()
            while dfs != tec_dfs:
                new_base.pop()
                tec_dfs -= 1
                ty = (ty + 1) % 2
            was.add(t)
            new_base.append(t)
            add = False
            if ty:
                for i in bc[t[1]]:
                    if i == (ci, cj) != t:
                        fin = True
                        break
                    if i in was or len(new_base) > 2 and new_base[-2][1] == i[1]:
                        continue
                    q.append((i, tec_dfs + 1))
                    add = True
            else:
                for i in ac[t[0]]:
                    if i == (ci, cj) != t:
                        fin = True
                        break
                    if i in was or len(new_base) > 2 and new_base[-2][0] == i[0]:
                        continue
                    q.append((i, tec_dfs + 1))
                    add = True
            if fin:
                break
            if not add:
                new_base.pop()
            else:
                tec_dfs += 1
                ty = (ty + 1) % 2
        m = min(new_base[1::2], key=lambda y: x[y[0]][y[1]])
        mz = x[m[0]][m[1]]
        for t in range(len(new_base)):
            i, j = new_base[t]
            if t % 2:
                x[i][j] -= mz
            else:
                x[i][j] += mz
        base[base.index(m)] = (ci, cj)
        iter += 1


if __name__ == "__main__":
    """a = [100, 250, 200, 300]
    b = [200, 200, 100, 100, 250]
    c = [[10, 7, 4, 1, 4],
         [2, 7, 10, 6, 11],
         [8, 5, 3, 2, 2],
         [11, 8, 12, 16, 13]]
    """
    a = [200, 350, 300]
    b = [270, 130, 190, 150, 110]
    c = [[24, 50, 45, 27, 15],
         [20, 32, 40, 35, 30],
         [22, 16, 18, 28, 20]]
    x, z, base = potential_method(a, b, c)
