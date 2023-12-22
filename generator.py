from board import Board
from solver import Solver
import random

class Generator:
    def __init__(self,
        num_holes=50, *,
        num_trials=20,
        num_picks=10,
    ):
        '''Create a generator
        num_holes: number of holes required
        num_trials: number of trials
        num_picks: number of positions consider to drop
        '''
        self._num_holes = num_holes
        self._num_trials = num_trials
        self._num_picks = num_picks

    def generate(self):
        self._board = Board()
        # not always satisfy num_holes
        # -> get the board with maximum number of holes
        best, min_k = None, 81
        for t in range(self._num_trials):
            print(f"Trial no.{t+1}")
            self._fill()
            k = self._drop()
            if k == 0: return self._board.export()
            if k < min_k:
                best, min_k = self._board.export(), k

        return best

    def _fill(self):
        s = Solver(self._board, max_solutions=1)
        s.solve()

        solution = s.solutions[0]
        self._board.config(solution)

    def _drop(self):
        b = self._board
        k = self._num_holes
        fulls = random.sample(range(81), 81)

        while k > 0:
            x = len(fulls)
            picks = random.sample(range(x),
                min(self._num_picks, x))

            for j in picks:
                idx = fulls[j]
                v = b[idx]
                b[idx] = 0

                s = Solver(b)
                s.solve()

                if s.num_solutions != 1:
                    b[idx] = v
                else:
                    fulls.pop(j)
                    k -= 1
                    break
            else: break # ?

        return k

if __name__ == '__main__':
    g = Generator(58)
    with open('test.txt', 'w') as f:
        for i in range(10):
            setup = g.generate()
            b = Board(setup)
            if len(b.holes()) < 58: continue
            print(setup, file=f, flush=True)

    with open('test.txt') as f:
        for line in f:
            setup = line.strip()
            b = Board(setup)

            s = Solver(b)
            s.solve()
            assert len(s.solutions) == 1