import random
import json
from datetime import datetime


class Bank:
    def __init__(self):
        self.Accounts = {}
        self.account_load()
        self.current_account = None

    def create_account(self):
        name = input("Enter your name: ")
        password = input("Enter your password: ")
        balance = float(input("Enter amount to deposit: "))
        account_no = str(random.randint(100000, 999999))
        self.Accounts[account_no] = {
            "name": name,
            "password": password,
            "balance": balance,
        }
        print("Account successfully created.")
        print("Your account number:", account_no)
        self.save_account()

    def account_load(self):
        try:
            with open("accounts.json", "r") as f:
                data = json.load(f)
                self.Accounts = data
        except FileNotFoundError:
            self.Accounts = {}
        except Exception as e:
            print(e)

    def save_account(self):
        with open("accounts.json", "w") as f:
            json.dump(self.Accounts, f, indent=4)

    def login(self):
        accountno = input("Enter the account number: ")
        if accountno in self.Accounts:
            password = input("Enter the password: ")
            if password == self.Accounts[accountno]["password"]:
                print("Login successful.")
                self.current_account = accountno
                return True
            else:
                print("Invalid password.")
                return False
        else:
            print("Account not found.")
            return False

    def deposit(self):
        amount = float(input("Enter the amount to deposit: "))
        if self.verify_password():
            self.Accounts[self.current_account]["balance"] += amount
            print("Deposit successful.")
            self.transaction_history(f"Deposited {amount}")
            self.save_account()

    def withdraw(self):
        amount = float(input("Enter the amount to withdraw: "))
        if self.verify_password():
            if self.Accounts[self.current_account]["balance"] >= amount:
                self.Accounts[self.current_account]["balance"] -= amount
                print("Withdraw successful.")
                self.transaction_history(f"Withdraw {amount}")
                self.save_account()
            else:
                print("Invalid amount entered.")

    def transaction_history(self, message):
        try:
            with open("History.txt", "a") as f:
                current_time = datetime.now().strftime("%d-%m-%Y %H:%M:%S")
                f.write(str(current_time) + "   " + message + "\n")
                print("Transaction history saved.")
        except Exception as e:
            print(e)

    def verify_password(self):
        entered = input("Enter the password: ")
        return entered == self.Accounts[self.current_account]["password"]
          

    def transfer_money(self):
        receiver_account = input("Enter receiver account number : ")
        if receiver_account == self.current_account:
            print("Cannot transfer to same account")
            return
        if receiver_account not in self.Accounts:
            print("Account not found")
            return
        amount = float(input("Enter amount : "))
        if self.verify_password():
         if amount <= 0:
            print("Invalid amount")
            return
        if self.Accounts[self.current_account]["balance"] < amount:
            print("Insufficient balance")
            return
        self.Accounts[self.current_account]["balance"] -= amount
        self.Accounts[receiver_account]["balance"] += amount
        self.transaction_history(f"Transferred {amount} to {receiver_account}")
        self.save_account()
        print("Transfer Successful")

    def change_password(self):
       current_password = str(input("Enter current paswword : "))
       if current_password == self.Accounts[self.current_account]["password"]:
          self.Accounts[self.current_account]["password"] = str(input("Enter new password :"))
          print("Password Updated...")
          self.save_account()
       else:
          print("password invalid")

    def check_balance(self):
       if self.verify_password():
          print(self.Accounts[self.current_account]["balance"])



bank = Bank()

while True:
    print("1. Create Account")
    print("2. Login")
    print("3. Exit")

    select = int(input("Enter your choice: "))

    if select == 1:
        bank.create_account()
    elif select == 2:
        if bank.login():
            while True:
                print("1. Deposit")
                print("2. Withdraw")
                print("3. Transaction History")
                print("4. Change Password")
                print("5. Check balance")
                print("6. Transfer Amount")
                print("7. Logout")

                choice = int(input("Enter your choice: "))

                if choice == 1:
                    bank.deposit()
                elif choice == 2:
                    bank.withdraw()
                elif choice == 3:
                    if bank.verify_password():
                        with open("History.txt", "r") as f:
                            data = f.read()
                            print(data)
                elif choice == 4:
                    bank.change_password()
                elif choice == 5:
                    bank.check_balance()
                elif choice == 6:
                    bank.transfer_money()
                elif choice == 7:
                    print("Logged out.")
                    break
                else:
                    print("Invalid choice.")
    elif select == 3:
        print("Goodbye.")
        break
    else:
        print("Invalid choice.")
    
