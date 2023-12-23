class Board:
    def __init__(self, setup=None):
        self._data = [0] * 81
        if setup: self.config(setup)

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

    def config(self, setup:str):
        assert isinstance(setup, str)
        if not setup.isdigit():
            raise ValueError("Setup should only contains 0-9")

        self.clear()
        for i in range(len(self._data)):
            v = int(setup[i])
            self[i] = v

    def clear(self):
        for i in range(81): self[i] = 0

    def export(self) -> str:
        return ''.join(str(v) for v in self._data)

    def __getitem__(self, i):
        return self._data[i]

    def __setitem__(self, i, v):
        assert isinstance(v, int)
        assert 0 <= v <= 9
        if v > 0: assert v in self.possible_values(i)
        self._data[i] = v

        try:
            self.view.update(i,v)
        except AttributeError: pass

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

SETUP = ''.join([
    '000960200',
    '000000060',
    '080100090',
    '008000032',
    '619000000',
    '002000004',
    '000003507',
    '100008000',
    '050020000',
])
if __name__ == '__main__':
    b = Board(SETUP)
    print(b)