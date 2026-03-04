# A_MAZE_ING

## Todo


1) Config parser — legge e valida il file di configurazione
2) Maze generator — genera il labirinto
3) Maze validator — verifica che il labirinto rispetti le regole
4) File writer — salva il labirinto in esadecimale + coordinate + soluzione
5) Solver — trova il percorso più breve
6) Visualizer — mostra il labirinto graficamente
WIDTH=15
HEIGHT=15
ENTRY=0,0
EXIT= 14,14
OUTPUT_FILE=maze.txt
PERFECT=true

START=7,7
ALGORITHM=backtrack
SEED=



# TODO:

# opzione play (extra flag player pos in Cell)

## Documentazione del Processo

    # @classmethod
    # def maze_menu(cls) -> None:

    #     msg = "\n"
    #     while True:
    #         cls.maze.print_maze()
    #         print(cls.maze.error_message)
    #         cls.display_maze_menu()
    #         print(msg)
    #         choice = input("Re-choose your path: ").strip().lower()
    #         match choice:
    #             case "1":
    #                 try:
    #                     cls.maze_generator()
    #                     msg = "\n"
    #                 except ValueError as e:
    #                     msg = e.args[0]
    #             case "2":
    #                 try:
    #                     cls.config_menu()
    #                     msg = "\n"
    #                 except ValidationError as e:
    #                     for err in e.errors():
    #                         msg += err['msg'] + "\n"
    #             case "3":
    #                 cls.color_menu()
    #                 clear_screen()
    #                 msg = "\n"
    #             case "4":
    #                 cls.maze.animation = not cls.maze.animation
    #                 msg = f"Maze animation changed to {cls.maze.animation}\n"
    #             case "5":
    #                 cls.maze.solution = not cls.maze.solution
    #                 state = "VISIBLE" if cls.maze.solution else "INVISIBLE"
    #                 msg = f"Maze solution changed to '{state}'\n"
    #             case "q":
    #                 cls.closure()
    #             case _:
    #                 msg = "error: invalid input\n"
    #                 clear_screen()
    #                 cls.maze.print_maze()