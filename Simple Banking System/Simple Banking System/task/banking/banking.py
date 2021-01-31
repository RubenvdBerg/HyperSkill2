import random
import sqlite3


class Banksystem:
    def __init__(self):
        self.con = sqlite3.connect('card.s3db')
        self.con.execute((
            'CREATE TABLE IF NOT EXISTS card('   
            'id INTEGER PRIMARY KEY AUTOINCREMENT,'
            'number TEXT,'
            'pin TEXT,'
            'balance INTEGER DEFAULT 0);'
        ))
        self.start()
        self.con.close()

    def start(self):
        inp = int(input('''
            1. Create an account
            2. Log into account
            0. Exit
            '''))
        if inp == 1:
            self.create_account()
        elif inp == 2:
            self.log_in()
        elif inp == 0:
            print('Bye!')
            exit()
        else:
            print('Not a valid number')

    def create_account(self):
        number = self.generate_card()
        pin = Banksystem.randintn(4)
        self.con.execute('INSERT INTO card(number, pin) VALUES (?, ?);', (number, pin))
        self.con.commit()
        print('Your card has been created')
        print('Your card number:')
        print(number)
        print('Your pin number:')
        print(pin)
        self.start()

    def generate_card(self):
        iin = '400000'
        while True:
            precard = iin + Banksystem.randintn(9)
            checksum = Banksystem.luhncalc(precard)
            cardnr = precard + checksum
            rows = self.con.execute('SELECT number FROM card WHERE number=?', (cardnr,))
            row = rows.fetchone()
            if not row:
                break
        return cardnr

    @staticmethod
    def luhncalc(number: str) -> str:
        num = [int(x) for x in number]
        num[0::2] = (x * 2 for x in num[0::2])
        check = sum(x - 9 if x > 9 else x for x in num)
        return str((10 - check % 10) % 10)

    @staticmethod
    def randintn(n):
        x = ''
        for _ in range(n):
            x += str(random.randint(0, 9))
        return x

    def log_in(self):
        account = str(input('Enter your card number:'))
        pin = str(input('Enter your PIN:'))
        row = self.con.execute('SELECT pin FROM card WHERE number=?;', (account,))
        try:
            if row.fetchone()[0] == pin:
                print('You have successfully logged in!')
                self.logged_in(account)
            else:
                print('Wrong card number or PIN!')
                self.start()

        except (TypeError, KeyError):
            print('Wrong card number or PIN!')
            self.start()

    def logged_in(self, account):
        choice = int(input('''
        1. Balance
        2. Add income
        3. Do transfer
        4. Close account
        5. Log out
        0. Exit
        '''))
        if choice == 1:
            self.balance(account)
        elif choice == 2:
            self.add_income(account)
        elif choice == 3:
            self.transfer(account)
        elif choice == 4:
            self.close_acc(account)
        elif choice == 5:
            self.start()
        elif choice == 0:
            print('Bye!')
            exit()
        else:
            print('Not a valid number')

    def balance(self, account):
        balance = self.con.execute('SELECT balance FROM card WHERE number=?', (account,))
        print(f'Balance: {balance}')
        self.logged_in(account)

    def add_income(self, account):
        income = int(input('Enter income:'))
        self.con.execute('UPDATE card SET balance = balance + ? WHERE number = ?;', (income, account))
        self.con.commit()
        print('Income was added!')
        self.logged_in(account)

    def transfer(self, account):
        to_acc = int(input('Enter card number:'))
        if to_acc == int(account):
            print("You can't transfer money to the same account!")
            self.logged_in(account)
        elif Banksystem.luhncalc(str(to_acc)[0:-1]) != str(to_acc)[-1]:
            print('Probably you made a mistake in the card number. Please try again!')
            self.logged_in(account)
        else:
            acc_check = self.con.execute('SELECT * FROM card WHERE number=?;', (to_acc,)).fetchone()
            if acc_check:
                amount = int(input('Enter how much money you want to transfer:'))
                balance1 = self.con.execute('SELECT balance FROM card WHERE number=?;', (account,)).fetchone()
                if amount > balance1[0]:
                    print('Not enough money!')
                    self.logged_in(account)
                else:
                    self.con.execute('UPDATE card SET balance = balance - ? WHERE number=?;', (amount, account))
                    self.con.execute('UPDATE card SET balance = balance + ? WHERE number=?;', (amount, to_acc))
                    self.con.commit()
                    print('Success!')
                    self.logged_in(account)
            else:
                print('Such a card does not exist.')
                self.logged_in(account)
            self.logged_in(account)

    def close_acc(self, account):
        self.con.execute('DELETE FROM card WHERE number = ?;', (account,))
        self.con.commit()
        print('The account has been closed!')
        self.start()


bank = Banksystem()
