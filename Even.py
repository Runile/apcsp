def check(n):
    if n % 2 == 0:
        return True
    else:
        return False
    
print('give me a number')
num = int(input())
if check(num):
    print(str(num) + " is even")
else:
    print(str(num) + " is odd")