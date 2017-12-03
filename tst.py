import csv
import init_gui as ig

player1 = "Best_First_1"
player2 = "Best_First_2"

with open("BFtree_vs_BFtree.csv", "a") as f:
    for i in range(10):
        win = ig.main()
        winner = player1
        if win[0] == "player2":
            winner = player2
        record_str = "Mary,Best_First_1,Best_First_2," + winner + "," + str(win[1]) + "\n"
        f.write(record_str)
