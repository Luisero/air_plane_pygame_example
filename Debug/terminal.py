def clear_terminal():
    from os import system, name
    system('cls' if name == 'nt' else 'clear')