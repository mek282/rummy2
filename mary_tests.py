import csv
import init_gui as ig

player1 = "Best_First"
player2 = "Control"

with open("final_"+player1+"_vs_"+player2+".csv", "a") as f:
    for i in range(100):

        win = ig.main()
        winner = player1
        if win[0] == "player2":
            winner = player2
        record_str = "Mary,"+player1+","+player2 +"," + winner + "," + str(win[1]) + "\n"
        f.write(record_str)
