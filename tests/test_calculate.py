from app.calculate import InsufficientFunds, add, multiply, divide, substract, BankAccount
import pytest


@pytest.fixture
def bank_Account_1():
    return BankAccount(50)
@pytest.fixture
def zero_bank_Account():
    return BankAccount()



@pytest.mark.parametrize(
        "num1, num2, expected",
        [
            (2, 3, 5),
            (3, 4, 7),
            (2, 2, 4)
        ]
)
def test_add(num1, num2, expected):
    print("1st test")
    assert add(num1,num2) == expected

def test_substact():
    assert substract(3,1) == 2

def test_divide():
    assert divide(6,3) == 2

def test_multiply():
    assert multiply(2,3) == 6

def test_initial_bank_account(bank_Account_1):
    assert bank_Account_1.balance == 50


def test_default_balace(zero_bank_Account):
    assert zero_bank_Account.balance==0

def test_deposit():
    account=BankAccount(50)
    account.deposit(20)
    assert account.balance==70

def test_withdraw():
    account=BankAccount(50)
    account.withdraw(20)
    assert account.balance==30

def test_rate():
    account=BankAccount(50)
    account.interest()
    assert round(account.balance,6)==55


@pytest.mark.parametrize("deposit, withdrew, expected",
                         [(200, 100, 100),
                          (300, 200, 100), (20, 10, 10)])
def test_transaction(zero_bank_Account, deposit, withdrew, expected):
    zero_bank_Account.deposit(deposit)
    zero_bank_Account.withdraw(withdrew)
    assert zero_bank_Account.balance==expected


def test_insufficien_balance(bank_Account_1):
    with pytest.raises(InsufficientFunds):
        print("2nd test", bank_Account_1.balance)
        bank_Account_1.withdraw(70)

