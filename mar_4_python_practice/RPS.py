def break_lines(it):
    if (it > 0):
        it = it - 1
        print("")
        break_lines(it)

print("player 1 choose [rock, paper, scissors]")
p1 = str(input())
break_lines(10)

print("player 2 choose [rock, paper, scissors]")
p2 = str(input())

status = "tie"

if (p1 == "rock"):
    if p2 == "paper":
        status = "lose"
    elif p2 == "scissors":
        status = "win"

if (p1 == "paper"):
    if p2 == "scissors":
        status = "lose"
    elif p2 == "rock":
        status = "win"

if (p1 == "scissors"):
    if p2 == "rock":
        status = "lose"
    elif p2 == "paper":
        status = "win"

if (status == "win"):
    print("player 1 wins with " + p1 + " beating " + p2)
elif (status == "lose"):
    print("player 1 loses with " + p2 + " beating " + p1)
elif (status == "tie"):
    print("its a tie!!")