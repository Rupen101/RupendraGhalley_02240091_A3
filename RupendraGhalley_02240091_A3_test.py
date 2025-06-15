
import unittest

class Account:
    def __init__(self, account_id, passcode, funds=0.0):
        self.account_id = account_id
        self.passcode = passcode
        self.funds = funds

    def deposit(self, amount):
        if amount <= 0:
            raise ValueError("Deposit amount must be positive.")
        self.funds += amount
        return self.funds

    def withdraw(self, amount):
        if amount <= 0:
            raise ValueError("Withdrawal amount must be positive.")
        if self.funds < amount:
            raise ValueError("Insufficient funds.")
        self.funds -= amount
        return self.funds

    def transfer(self, amount, recipient):
        if recipient is None:
            raise ValueError("Recipient not found.")
        if amount <= 0:
            raise ValueError("Transfer amount must be positive.")
        if self.funds < amount:
            raise ValueError("Insufficient funds.")
        self.funds -= amount
        recipient.funds += amount
        return True

    def recharge(self, amount, number):
        if len(number) != 8 or not number.startswith(('77', '17')):
            raise ValueError("Invalid phone number.")
        return self.withdraw(amount)

class TestBankingSystem(unittest.TestCase):

    def setUp(self):
        self.user = Account("12345", "0000", 1000.0)
        self.recipient = Account("54321", "1111", 500.0)

    # Test deposit
    def test_valid_deposit(self):
        self.assertEqual(self.user.deposit(200), 1200)

    def test_negative_deposit(self):
        with self.assertRaises(ValueError):
            self.user.deposit(-100)

    # Test withdrawal
    def test_valid_withdrawal(self):
        self.assertEqual(self.user.withdraw(300), 700)

    def test_insufficient_funds_withdrawal(self):
        with self.assertRaises(ValueError):
            self.user.withdraw(2000)

    def test_negative_withdrawal(self):
        with self.assertRaises(ValueError):
            self.user.withdraw(-50)

    # Test transfer
    def test_valid_transfer(self):
        result = self.user.transfer(200, self.recipient)
        self.assertTrue(result)
        self.assertEqual(self.user.funds, 800)
        self.assertEqual(self.recipient.funds, 700)

    def test_invalid_transfer_amount(self):
        with self.assertRaises(ValueError):
            self.user.transfer(-100, self.recipient)

    def test_transfer_to_none(self):
        with self.assertRaises(ValueError):
            self.user.transfer(100, None)

    def test_transfer_insufficient_funds(self):
        with self.assertRaises(ValueError):
            self.user.transfer(2000, self.recipient)

    # Test recharge
    def test_valid_recharge(self):
        self.assertEqual(self.user.recharge(100, "77123456"), 900)

    def test_invalid_phone_number_prefix(self):
        with self.assertRaises(ValueError):
            self.user.recharge(100, "66123456")

    def test_invalid_phone_number_length(self):
        with self.assertRaises(ValueError):
            self.user.recharge(100, "7712345")

if __name__ == '__main__':
    unittest.main()