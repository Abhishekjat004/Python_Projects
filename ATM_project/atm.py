class ATM:
    def __init__(self):
        self.user_data = {
            '12345': {'pin': '5678', 'balance': 1000, 'transactions': []},
            '67890': {'pin': '1234', 'balance': 500, 'transactions': []}
        }
        self.current_user = 0

    def authenticate_user(self):
        account_number = input("Enter your account number: ")
        pin = input("Enter your PIN: ")

        if account_number in self.user_data and self.user_data[account_number]['pin'] == pin:
            self.current_user = account_number
            return True
        else:
            print("Invalid account number or PIN. Please try again.")
            return False

    def check_balance(self):
        print("Balance:", self.user_data[self.current_user]['balance'])

    def withdraw_amount(self):
        amount = int(input("Enter Withdraw Amount: "))
        if amount <= self.user_data[self.current_user]['balance']:
            self.user_data[self.current_user]['balance'] -= amount
            self.user_data[self.current_user]['transactions'].append(-amount)  # Negative amount for withdrawals
            print("Withdraw Successful....")
            print("Remaining Balance: ", self.user_data[self.current_user]['balance'])
        else:
            print("Insufficient Balance")

    def generate_pin(self):
        attempt = 3
        while attempt:
            old_pin = input("Enter your Old Pin: ")
            if old_pin == self.user_data[self.current_user]['pin']:
                new_pin1 = input("Enter New Pin: ")
                new_pin2 = input("Re-enter Pin for Confirmation: ")
                if new_pin1 == new_pin2:
                    self.user_data[self.current_user]['pin'] = new_pin2
                    print("Successfully Pin Change...")
                    break
                else:
                    print("PINs do not match. Please try again.")
            else:
                if attempt > 1:
                    print("Please Enter Correct Pin.")
                    attempt -= 1
                else:
                    print("All Attempt are Failed!")
                    break

    def display_transactions(self):
        print("Transactions:", self.user_data[self.current_user]['transactions'])

    def main_menu(self):
        if self.authenticate_user():
            print("1. Check Balance")
            print("2. Withdraw Amount")
            print("3. Pin Generate")
            print("4. Transactions")
            choice = int(input("Enter your choice: "))

            if choice == 1:
                self.check_balance()
            elif choice == 2:
                self.withdraw_amount()
            elif choice == 3:
                self.generate_pin()
            elif choice == 4:
                self.display_transactions()


# object creation
Abhi = ATM()
print()
print("                                                    Please Insert Your ATM Card                                                    ")
print()
Abhi.main_menu()
print("                                                    Please Remove Your ATM Card                                                    ")
