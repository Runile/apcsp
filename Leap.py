print("What year is it")
year = int(input())
is_leap = False

if (year%4 == 0) and (year%100 != 0 or year%400 == 0):
    is_leap = True

if is_leap:
    print("is a leap year")
else:
    print("not a leap year")