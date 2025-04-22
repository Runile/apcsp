print('input your current grade')
grade = int(input())
current_grade = "F"
if grade < 0 or grade > 100:
    if grade < 0:
        print("how bro...")
    else:
        print("oooo smarty")
else:
    if grade > 60:
        current_grade = "D"
    if grade > 70:
        current_grade = "C"
    if grade > 80:
        current_grade = "B"
    if grade > 90:
        current_grade = "A"

    print('You have a(n) ' + current_grade)

