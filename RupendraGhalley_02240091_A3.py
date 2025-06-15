import tkinter as tk
from tkinter import messagebox
from tkinter import simpledialog
import random


class BankError(Exception):
    pass
class InvalidAmountError(BankError):
    pass
class BalanceTooLowError(BankError):
    pass
class InvalidLoginError(BankError):
    pass
class InvalidPhoneNumberError(BankError):
    pass

class User:
    def __init__(self, user_id, password):
        self.user_id = user_id
        self.password = password
        self.balance = 0.00

    def deposit(self, amount):
        if amount <= 0:
            raise InvalidAmountError("Enter a valid amount.")
        self.balance += amount
        return f"Deposited Nu.{amount:.2f}"

    def withdraw(self, amount):
        if amount <= 0:
            raise InvalidAmountError("Enter a valid amount.")
        if self.balance < amount:
            raise BalanceTooLowError("Not enough balance.")
        self.balance -= amount
        return f"Withdrew Nu.{amount:.2f}"

    def transfer_to(self, other_user, amount):
        if self == other_user:
            raise BankError("Cannot transfer to self.")
        self.withdraw(amount)
        other_user.deposit(amount)
        return f"Transferred Nu.{amount:.2f} to {other_user.user_id}"

    def recharge_phone(self, phone, amount):
        if not phone.startswith(('77', '17')) or len(phone) != 8:
            raise InvalidPhoneNumberError("Bhutanese phone numbers start with 77 or 17.")
        self.withdraw(amount)
        return f"Recharged Nu.{amount:.2f} to {phone}"

class Bank:

    def __init__(self):
        self.users = {}

    def create_user(self):
        while True:
            uid = str(random.randint(10000, 99999))
            if uid not in self.users:
                break
        pwd = str(random.randint(1000, 9999))
        user = User(uid, pwd)
        self.users[uid] = user
        return user

    def authenticate(self, user_id, password):
        user = self.users.get(user_id)
        if not user or user.password != password:
            raise InvalidLoginError("Wrong ID or password.")
        return user

    def delete_user(self, user):
        del self.users[user.user_id]

class BankApp:

    def __init__(self, master):
        self.master = master
        self.master.title("Bank App")
        self.bank = Bank()
        self.logged_user = None
        self.setup_login_ui()
        self.setup_action_ui()

    def setup_login_ui(self):
        login_frame = tk.Frame(self.master)
        login_frame.pack()

        tk.Label(login_frame, text="Account ID").grid(row=0, column=0)
        self.id_entry = tk.Entry(login_frame)
        self.id_entry.grid(row=0, column=1)

        tk.Label(login_frame, text="Password").grid(row=1, column=0)
        self.pass_entry = tk.Entry(login_frame, show="*")
        self.pass_entry.grid(row=1, column=1)

        tk.Button(login_frame, text="Login", command=self.login).grid(row=2, column=0, pady=5)
        tk.Button(login_frame, text="Create Account", command=self.create_account).grid(row=2, column=1)

        self.status = tk.Label(login_frame, text="Not logged in.")
        self.status.grid(row=3, column=0, columnspan=2)

    def setup_action_ui(self):
        self.action_frame = tk.Frame(self.master)
        self.action_frame.pack(pady=10)

        buttons = [
            ("Check Balance", self.check_balance),
            ("Deposit", self.do_deposit),
            ("Withdraw", self.do_withdraw),
            ("Transfer", self.do_transfer),
            ("Recharge", self.do_recharge),
            ("Delete Account", self.do_delete),
        ]

        for text, cmd in buttons:
            tk.Button(self.action_frame, text=text, command=cmd, width=20).pack(pady=2)

    def login(self):
        uid = self.id_entry.get()
        pwd = self.pass_entry.get()
        try:
            user = self.bank.authenticate(uid, pwd)
            self.logged_user = user
            self.status.config(text=f"Logged in: {uid}")
        except BankError as e:
            messagebox.showerror("Login Failed", str(e))

    def create_account(self):
        user = self.bank.create_user()
        messagebox.showinfo("Account Created", f"ID: {user.user_id}\nPassword: {user.password}")

    def check_logged_in(self):
        if not self.logged_user:
            raise BankError("Please log in first.")

    def check_balance(self):
        try:
            self.check_logged_in()
            balance = self.logged_user.balance
            messagebox.showinfo("Balance", f"Nu.{balance:.2f}")
        except BankError as e:
            messagebox.showerror("Error", str(e))

    def do_deposit(self):
        try:
            self.check_logged_in()
            amt = float(simpledialog.askstring("Deposit", "Amount to deposit:"))
            msg = self.logged_user.deposit(amt)
            messagebox.showinfo("Success", msg)
        except BankError as e:
            messagebox.showerror("Error", str(e))
        except:
            messagebox.showerror("Error", "Invalid input.")

    def do_withdraw(self):
        try:
            self.check_logged_in()
            amt = float(simpledialog.askstring("Withdraw", "Amount to withdraw:"))
            msg = self.logged_user.withdraw(amt)
            messagebox.showinfo("Success", msg)
        except BankError as e:
            messagebox.showerror("Error", str(e))

    def do_transfer(self):
        try:
            self.check_logged_in()
            rid = simpledialog.askstring("Transfer", "Recipient ID:")
            amt = float(simpledialog.askstring("Transfer", "Amount to transfer:"))
            recipient = self.bank.users.get(rid)
            if not recipient:
                raise BankError("Recipient not found.")
            msg = self.logged_user.transfer_to(recipient, amt)
            messagebox.showinfo("Success", msg)
        except BankError as e:
            messagebox.showerror("Error", str(e))

    def do_recharge(self):
        try:
            self.check_logged_in()
            number = simpledialog.askstring("Recharge", "Phone number:")
            amt = float(simpledialog.askstring("Recharge", "Amount:"))
            msg = self.logged_user.recharge_phone(number, amt)
            messagebox.showinfo("Success", msg)
        except BankError as e:
            messagebox.showerror("Error", str(e))

    def do_delete(self):
        try:
            self.check_logged_in()
            confirm = messagebox.askyesno("Confirm", "Are you sure?")
            if confirm:
                self.bank.delete_user(self.logged_user)
                self.logged_user = None
                self.status.config(text="Account deleted.")
        except BankError as e:
            messagebox.showerror("Error", str(e))

if __name__ == "__main__":
    root = tk.Tk()
    app = BankApp(root)
    root.mainloop()
