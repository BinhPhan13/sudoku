from board import Board
import random

class Solver:
    def __init__(self,
        board:Board, *,
        max_solutions=2,
    ):
        self._board = board
        self._holes = board.holes()

        self._solutions = []
        self._max_solutions = max_solutions

        self._n = 0

    def solve(self):
        if self.num_solutions >= self._max_solutions:
            return

        if not self._holes:
            solution = self._board.export()
            self._solutions.append(solution)
            return

        self._n += 1
        # choose the branch with least branches
        self._holes.sort(key=lambda x: len(
            self._board.possible_values(x)
        ), reverse=True)
        idx = self._holes.pop()
        assert self._board[idx] == 0

        values = list(self._board.possible_values(idx))
        random.shuffle(values)
        for v in values:
            self._board[idx] = v
            self.solve()

        # backtrack
        self._board[idx] = 0
        self._holes.append(idx)

    @property
    def num_solutions(self):
        return len(self._solutions)

    @property
    def solutions(self):
        return self._solutions.copy()

    @property
    def num_trials(self):
        return self._n

if __name__ == '__main__':
    from board import SETUP
    b = Board(SETUP)
    print(f'{len(b.holes())} holes')

    s = Solver(b, max_solutions=2)
    s.solve()

    print(f'{s.num_trials=}')
    print(f'{s.num_solutions=}')