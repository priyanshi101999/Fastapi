class InsufficientFunds(Exception):
    pass

def add(num1: int,num2:int):
    return num1+num2

def substract(num1: int, num2:int):
    return num1-num2

def divide(num1: int, num2: int):
    return num1/num2

def multiply(num1: int, num2: int):
    return num1*num2

class BankAccount():
    def __init__(self, balance:int = 0):
        self.balance = balance

    def deposit(self, amount):
        self.balance+=amount
    
    def withdraw(self,amount):
        if amount > self.balance:
            print("Insufficient funds", self.balance, amount)
            raise InsufficientFunds("Insufficient funds")

        self.balance-=amount
    
    def get_balance(self):
        return self.balance
    
    def interest(self):
        self.balance*=1.1