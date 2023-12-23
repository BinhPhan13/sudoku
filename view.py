from board import Board, SETUP
from solver import Solver
import curses

class View:
    def __init__(self):
        curses.initscr()
        curses.curs_set(0)

        srow, scol = 10, 50
        height, width = 20, 30
        self.scr = curses.newwin(
            height, width,
            srow, scol
        )

    def update(self, index:int, value:int):
        r, c = index//9, index%9
        r += r//3
        c += c//3 * 4 + c%3

        color = curses.A_COLOR if value == 0 else curses.A_BOLD

        self.scr.addch(r, c, str(value), color)
        self.scr.refresh()

    def start(self):
        curses.noecho()
        curses.cbreak()
        self.scr.keypad(True)

    def exit(self):
        self.scr.keypad(False)
        curses.nocbreak()
        curses.echo()
        curses.endwin()

if __name__ == '__main__':
    v = View()
    b = Board()
    b.view = v

    try:
        v.start()
        b.config(SETUP)

        while True:
            key = v.scr.getch()
            if ord('q') == key: break

            if ord('s') == key:
                s = Solver(b, max_solutions=1, sleep_time=0.1)
                s.solve()

                solution = s.solutions[0]
                b.config(solution)

            elif ord('r') == key:
                b.config(SETUP)

    except Exception as e:
        print(f'{e!r}')
    finally:
        v.exit()