import csv
import main



player1 = "SA"
player2 = "Heuristic3"


with open("final_"+player1+"_vs_"+player2+".csv", "a") as f:
    for i in range(200):

        win = main.main()
        winner = player1
        if win[0] == "player2":
            winner = player2
        record_str = "Kanchan,SA,Heuristic3," + winner + "," + str(win[1]) + "\n"
        f.write(record_str)
