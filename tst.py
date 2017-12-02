import csv
import init_gui as ig

player1 = "Heuristic"
player2 = "Heuristic2"

with open("heuristic_tests.csv", "a") as f:
    for i in range(50):
        win = ig.main()
        winner = player1
        if win[0] == "player2":
            winner = player2
        record_str = "Mary,Heuristic,Heuristic2," + winner + "," + str(win[1]) + "\n"
        f.write(record_str)
