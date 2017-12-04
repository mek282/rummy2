import csv
import init_gui as ig

player1 = "Heuristic3"
player2 = "Heuristic"

with open("heuristic3_tests.csv", "a") as f:
    for i in range(100):
        win = ig.main()
        winner = player1
        if win[0] == "player2":
            winner = player2
        record_str = "Kanchan,Heuristic3,Heuristic," + winner + "," + str(win[1]) + "\n"
        f.write(record_str)
