def convert(num, unit):
    if unit == "C":
        return (num * (9/5)) + 32
    else:
        return (num - 32) * (5/9)
    
print("what unit of temp is it (C or F in CAPS)")
unit = str(input())
print("what temp is it")
num = float(input())

if unit == "F" or unit == "C":
    print(unit + " converted is " + str(convert(num, unit)))
else:
    print("invalid unit")

