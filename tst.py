import csv
import init_gui as ig



player1 = "Heuristic3"
player2 = "Adversarial"

with open("heuristic3_adv_tests.csv", "a") as f:
    for i in range(50):

        win = ig.main()
        winner = player1
        if win[0] == "player2":
            winner = player2
        record_str = "Kanchan,Heuristic3,Adversarial," + winner + "," + str(win[1]) + "\n"
        f.write(record_str)
