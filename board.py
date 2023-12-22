class Board:
    def __init__(self, setup=None):
        self._data = [0] * 81
        if setup:
            for i in range(81): self[i] = setup[i]

    def possible_values(self, index):
        assert 0 <= index < 81
        possible_values = set(range(1,10))
        row, col = index//9, index%9

        for r in range(9):
            v = self[r*9+col]
            if v: possible_values.discard(v)

        for c in range(9):
            v = self[row*9+c]
            if v: possible_values.discard(v)

        # 3x3 box
        sr, sc = row//3 * 3, col//3 * 3
        for r in range(sr, sr+3):
            for c in range(sc, sc+3):
                v = self[r*9+c]
                if v: possible_values.discard(v)

        return possible_values

    def holes(self, flip=False):
        if flip:
            return [i for i in range(81) if self[i] > 0]
        else:
            return [i for i in range(81) if self[i] == 0]

    def __getitem__(self, i):
        return self._data[i]

    def __setitem__(self, i, v):
        assert isinstance(v, int)
        assert 0 <= v <= 9
        if v > 0: assert v in self.possible_values(i)
        self._data[i] = v

    def __repr__(self):
        WS, BR = ' ', '\n'
        s = ''
        for r in range(9):
            for c in range(9):
                sep = WS*4 if c in [2,5] else WS*2
                s += f'{self._data[r*9+c]}{sep}'
            s += BR
            if r in [2,5]: s += BR

        return s

    def __copy__(self):
        return Board([x for x in self._data])

SETUP = [
    0, 0, 0,  9, 6, 0,  2, 0, 0,
    0, 0, 0,  0, 0, 0,  0, 6, 0,
    0, 8, 0,  1, 0, 0,  0, 9, 0,

    0, 0, 8,  0, 0, 0,  0, 3, 2,
    6, 1, 9,  0, 0, 0,  0, 0, 0,
    0, 0, 2,  0, 0, 0,  0, 0, 4,

    0, 0, 0,  0, 0, 3,  5, 0, 7,
    1, 0, 0,  0, 0, 8,  0, 0, 0,
    0, 5, 0,  0, 2, 0,  0, 0, 0,
]
if __name__ == '__main__':
    b = Board(SETUP)
    print(b)