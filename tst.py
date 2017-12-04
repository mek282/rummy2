import csv
import init_gui as ig


player1 = "Best_First"
player2 = "Heuristic"

with open("heuristic_vs_bestfirst.csv", "a") as f:
    for i in range(10):
        win = ig.main()
        winner = player1
        if win[0] == "player2":
            winner = player2
        record_str = "Mary,Best_First,Heuristic," + winner + "," + str(win[1]) + "\n"
        f.write(record_str)
