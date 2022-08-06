def printf(*args, sep: str = ' ', end: str = '\n', col: int = 197, bg: int = 0):
    str = ''

    for arg in args:
        str += f'{sep}{arg}'

    print(f"\033[38;5;{col}m\033[48;5;{bg}m{str}\033[0m", end=end)


def console_clear():
    print('\033[2J')

# https://dvmn.org/encyclopedia/terminal/ansi-codes/
