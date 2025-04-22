bugs = ["ant", "cockroach", "fly", "dragonfly", "beetle"]
print("Give me a random bug name!!! singular - lowercase")
bug_input = str(input())

found_bug = False

for x in bugs:
    if x == bug_input:
        found_bug = True
        print("We have your bug!!")

if found_bug == False:
    print("Sorry, your bug is not in our database.")