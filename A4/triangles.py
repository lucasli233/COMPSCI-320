import sys
from math import *


def read():
    rows_str = sys.stdin.readline()
    rows_num = int(rows_str)
    triangles = []
    for i in range(rows_num):
        line = sys.stdin.readline().strip("\n")
        line1 = line.split(' ')
        sideA = int(line1[0])
        sideB = int(line1[1])
        sideC = int(line1[2])
        shade = float(line1[3])
        # list.append((int(sideA), int(sideB), int(sideC), float(shade)))
        triangles.append(Triangle(sideA, sideB, sideC, shade))
        triangles.sort()
    return triangles

# let m(i) be max possible chain with ith triangle at the end
# m(i)= m(j) + 1, if j.shade < i.shade, one side matches
# if no such j then m(i) = 1


class Triangle:
    def __init__(self, sideA, sideB, sideC, shade):
        self.sides = (sideA, sideB, sideC)
        self.shade = shade

    def __lt__(self, other):
        return self.shade < other.shade

    def __repr__(self):
        return f"({self.sides} {self.shade})"


def _matrix(triangles):
    n = len(triangles)
    # print(n)
    matrix = [[1 for i in range(3)] for j in range(n)]

    for i in range(1, n):
        for j in range(3):
            maxx = 1
            for k in range(i):
                if triangles[i].shade <= triangles[k].shade:
                    continue
                for l in range(3):
                    if triangles[k].sides[(l+1) % 3] == triangles[i].sides[j] or\
                            triangles[k].sides[(l+2) % 3] == triangles[i].sides[j]:
                        maxx = max(maxx, matrix[k][l] + 1)
            matrix[i][j] = maxx
    # print(matrix)

    maxx = -1
    for i in range(n):
        for j in range(3):
            maxx = max(maxx, matrix[i][j])
    print(maxx)


if __name__ == "__main__":
    triangles = read()
    _matrix(triangles)
