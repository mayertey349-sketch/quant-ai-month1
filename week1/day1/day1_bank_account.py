"""
Day 1 Exercise: BankAccount Class
File: day1_bank_account.py
Author: Michael Tetteh (mayertey349-sketch)
Date: [Today's date]

Description: 
A simple bank account class to practice OOP fundamentals.
"""
class BankAccount:
    """
    Represents a bank account with basic operations.
    """
    
    def __init__(self, owner, balance=0):
        """
        Initialize a new bank account.
        
        Parameters:
        owner (str): Name of account owner
        balance (float): Initial balance (default 0)
        """
        self.owner = owner
        self.balance = balance
        self.transaction_history = []
    
    def deposit(self, amount):
        """Add money to account."""
        if amount <= 0:
            print("Deposit amount must be positive!")
            return
        
        self.balance += amount
        self.transaction_history.append(f"Deposit: +${amount}")
        print(f"Deposited ${amount}. New balance: ${self.balance}")
    
    def withdraw(self, amount):
        """Remove money from account."""
        if amount <= 0:
            print("Withdrawal amount must be positive!")
            return
        
        if amount > self.balance:
            print(f"Insufficient funds! Balance: ${self.balance}")
            return
        
        self.balance -= amount
        self.transaction_history.append(f"Withdrawal: -${amount}")
        print(f"Withdrew ${amount}. New balance: ${self.balance}")
    
    def get_balance(self):
        """Return current balance."""
        return self.balance
    
    def show_history(self):
        """Display all transactions."""
        print(f"\n=== Transaction History for {self.owner} ===")
        if not self.transaction_history:
            print("No transactions yet.")
        else:
            for transaction in self.transaction_history:
                print(transaction)
        print(f"Current Balance: ${self.balance}")
        print("=" * 40)

# Test your class (write these tests yourself)
if __name__ == "__main__":
    # Create account
    account = BankAccount("Michael Tetteh", 1000)
    
    # Test deposit
    account.deposit(500)
    
    # Test withdrawal
    account.withdraw(200)
    
    # Test insufficient funds
    account.withdraw(2000)
    
    # Show history
    account.show_history()
    
    # Check balance
    print(f"\nFinal balance: ${account.get_balance()}")