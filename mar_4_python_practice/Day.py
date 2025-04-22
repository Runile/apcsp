print("day of the week 1-7")
num = int(input())
day = None

if num == 1:
    day = "Monday"
elif num == 2:
    day = "Tuesday"
elif num == 3:
    day = "Wednesday"
elif num == 4:
    day = "Thursday"
elif num == 5:
    day = "Friday"
elif num == 6:
    day = "Saturday"
elif num == 7:
    day = "Sunday"

if day:
    print("The day is " + day)
else:
    print("It is not found on the list!!")