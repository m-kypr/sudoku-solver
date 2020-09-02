import math


class Solver():

    example = [[8, 0, 2, 0, 5, 0, 7, 0, 1], [0, 0, 7, 0, 8, 2, 4, 6, 0], [0, 1, 0, 9, 0, 0, 0, 0, 0], [6, 0, 0, 0, 0, 1, 8, 3, 2], [5, 0, 0, 0, 0, 0, 0, 0, 9], [1, 8, 4, 3, 0, 0, 0, 0, 6], [0, 0, 0, 0, 0,
                                                                                                                                                                                              4, 0, 2, 0], [0, 9, 5, 6, 1, 0, 3, 0, 0], [3, 0, 8, 0, 9, 0, 6, 0, 7]]

    def __init__(self, sudoku=None):
        if sudoku:
            self.sudoku = sudoku
        else:
            self.sudoku = example
        self.n = int(math.sqrt(len(self.sudoku)))

    def can(self, y, x, v):
        for i in range(len(self.sudoku)):
            if self.sudoku[y][i] == v:
                return False
        for i in range(len(self.sudoku)):
            if self.sudoku[i][x] == v:
                return False
        dx = (x//self.n)*3
        dy = (y//self.n)*3
        for i in range(self.n):
            for j in range(self.n):
                if self.sudoku[dy+i][dx+j] == v:
                    return False
        return True

    def solve(self):
        for y in range(9):
            for x in range(9):
                if self.sudoku[y][x] == 0:
                    for n in range(1, 10):
                        if self.can(y, x, n):
                            self.sudoku[y][x] = n
                            yield from self.solve()
                        self.sudoku[y][x] = 0
                    return
        yield self.sudoku


if __name__ == "__main__":
    block_size = int(input("block size (default=3): ") or 3)
    sudoku = []
    for _ in range(block_size*block_size):
        sudoku.append([int(x) for x in input().split(" ") if x])
    solver = Solver(sudoku)
    solver.solve()
