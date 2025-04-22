print("what is ur balance")
balance = float(input())
def deposit(balance, amount):
    return balance + amount
def withdraw(balance, amount):
    return balance - amount
print("how much would you like to deposit??")
balance = deposit(balance, float(input()))
print('new balance is ' + str(balance))
print("how much would you like to withdraw??")
balance = withdraw(balance, float(input()))
print('new balance is ' + str(balance))