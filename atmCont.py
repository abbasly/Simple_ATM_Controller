import random

class Woori:
    def __init__(self):
        self.data_dict = {}


    def new_acc(self, card_no, account, amt):
        if card_no in self.data_dict:
            self.data_dict[card_no]["account"][account] = amt

    def new_card(self, card_no, paswd, account, amt):
        self.data_dict[card_no] = { "account": {account: amt},"pin": paswd}

    def passwd_check(self, card_num, entered_pin):
        if card_num in self.data_dict and self.data_dict[card_num]["pin"] == entered_pin:
            return self.data_dict[card_num]["account"]
        else:
            return None

    def update_account(self, card_num, account, amt):
        if self.data_dict[card_num]["account"][account] in self.data_dict[card_num]["account"]:
            self.data_dict[card_num]["account"][account] = amt
            return True
        else:
            return False


class Controller:
    def __init__(self, bank, cash):
        self.accounts = None
        self.Woori = bank
        self.cash_bin = cash

    def insert_card(self, card_num, pin):
        self.accounts = self.Woori.passwd_check(card_num, pin)
        if self.accounts != None:
            return 1, "Welcome!"     
        else:
            return 0, "Invalid card or wrong password"

    def acc_selection(self, acc):
        if acc in self.accounts:
            return True
        else:
            return False

    def account_actions(self, card_num, acc, action, amt=0):
        if action == "See Balance":
            return self.accounts[acc], 1,0
        elif action == "Withdraw":
            if self.cash_bin >= amt and self.accounts[acc] >= amt:
                updated_balance = self.accounts[acc] - amt
                self.cash_bin = self.cash_bin - amt
                self.accounts[acc] = updated_balance
                self.Woori.update_account(card_num, acc, updated_balance)
                return self.accounts[acc], 1, 0
            elif self.cash_bin < amt:
                return self.accounts[acc], 0 , 1
            elif self.accounts[acc] < amt:
                return self.accounts[acc], 0 , 2
        elif action == "Deposit":
            updated_balance = self.accounts[acc] + amt
            self.cash_bin = self.cash_bin + amt
            self.accounts[acc] = updated_balance
            self.Woori.update_account(card_num, acc, updated_balance)
            return self.accounts[acc], 1,0
        else:
            return self.accounts[acc], 2,0

    def __call__(self, card_num, pin, acc, action_list):
        a, b = self.insert_card(card_num, pin)
        if a == 0:
            return "Invalid card or wrong password"
        check = self.acc_selection(acc)
        if check is False:
            return "Invalid Account!"
        for action in action_list:
            if action[0] == "Leave":
                return "Left successfully"
            balance, bit, bit1 = self.account_actions(card_num, acc, action[0], action[1])
            if bit == 0:
                continue
            elif bit == 2:
                return "Invalid operation"
            else:
                continue
        return "Operations completed"


if __name__ == "__main__":


    empty_bank = Woori()
    # Test Controller on Empty Woori
    empty_atm = Controller(empty_bank, 0)
    valid, message = empty_atm.insert_card(0, 0)
    if valid == 0:
        print("Test Invalid Message on Empty ATM \t SUCCESS")
    else:
        print("Test Invalid Message on Empty ATM \t FAILURE")

    # New bank for teting

    test_bank = Woori()
    test_bank.new_card(20202021, 1234, "checking", 1000)
    test_bank.new_acc(20202021, "savings", 1000)
    test_bank.new_card(20192020, 4860, "checking", 5000)
    test_atm = Controller(test_bank, 10000)
    operations = [ ("Withdraw", 40),("See Balance", 0), ("Deposit", 100), ("Withdraw", 1000) ]

    # Testing the ATM with valid sequence of operations
    if test_atm(20192020, 4860, "checking", operations) == "Operations completed":
        print("Test Valid ATM Check \t SUCCESS")
    else:
        print("Test Valid ATM Check \t FAILURE")

    # Testing if overdraft is handled correclty
    if test_atm(20202021, 1234, "checking", operations) == "Operations completed":
        print("Test Overdraft handling \t SUCCESS")
    else:
        print("Test Overdraft handling \t FAILURE")

    # Test invalid PIN number
    if test_atm(20192020, 9878, "checking", operations) == "Invalid card or wrong password":
        print("Test Incorrect password \t SUCCESS")
    else:
        print("Test Incorrect password \t FAILURE")

    # Test invalid Account no
    if test_atm(876504321, 1234, "checking", operations) == "Invalid card or wrong password":
        print("Test Invalid Account Number \t SUCCESS")
    else:
        print("Test Invalid Account Number \t FAILURE")

    test_bank2 = Woori()
    test_bank2.new_card(20202021, 1234, "checking", 1000)
    test_bank2.new_acc(20202021, "savings", 1000)
    test_bank2.new_card(20192020, 4860, "checking", 5000)
    test_atm2 = Controller(test_bank2, 10000)
    cash_bin_over_action = [("See Balance", 0), ("Withdraw", 30000)]

    # Tests cash bin excess handling on account balance
    if test_atm(20192020, 4860, "checking", cash_bin_over_action) == "Operations completed":
        print("Test Exceeding Cash Bin \t SUCCESS")
    else:
        print("Test Exceeding Cash Bin \t FAILURE")

    exit_action = [("See Balance", 0), ("Leave", 0)]
    if test_atm(20192020, 4860, "checking", exit_action) == "Left successfully":
        print("Test exiting \t SUCCESS")
    else:
        print("Test exiting \t FAILURE")

    test_bank = Woori()
    card_num = 20180821
    test_bank.new_card(card_num, 1234, "stipend", 20000)
    test_bank.new_acc(card_num, "savings", 15000)
    test_atm = Controller(test_bank, 10000)

    #while True:
    pin = int(input("\n Please Enter Your account pin: "))
    a, b = test_atm.insert_card(card_num, pin)
    while a == 0:
        pin = int(input("\nInvalid Pin.. Re-enter your Pin please: "))
        a, b = test_atm.insert_card(card_num, pin)
    print("\nSelect Account:")
    print("\n1 - Savings \t 2 - Stipend")
    temp = int(input("\nEnter your selection: "))
    account= "none"
    if temp == 1:
        account = "savings"
    if temp == 2:
        account = "stipend"

    while True:
        print("\n1 - Balance \t 2 - Withdraw \t 3 - Deposit \t 4 - Quit ")
        selection = int(input("\nEnter your selection: "))
        if selection == 1:
            balance, void, void1 = test_atm.account_actions(card_num, account, "See Balance")
            print("Your Balance is: " + str(balance) +" KRW")
        if selection==2:
            balance, void, void1 = test_atm.account_actions(card_num, account, "See Balance")
            print("Your Balance is: " + str(balance)+" KRW")
            amt = int(input("\nPlease Enter amount to withdraw: "))
            balance, void, void1 = test_atm.account_actions(card_num, account, "Withdraw",amt)
            if void==0 and void1==2:
                print("Please enter a valid amount")
            if void==0 and void1==1:
                print("There is not enough cash in the ATM")
            balance, void, void1 = test_atm.account_actions(card_num, account, "See Balance")
            print("Your Balance is: " + str(balance)+" KRW")
        if selection==3:
            amt = int(input("\nEnter an amount to deposit: "))
            test_atm.account_actions(card_num, account, "Deposit", amt)
            balance, void, void1 = test_atm.account_actions(card_num, account, "See Balance")
            print("Your Balance is: " + str(balance)+" KRW")
        if selection == 4:
            flag = input("Are you sure you want to quit?, Yes, or No:")
            if flag.lower() == "yes":
                print("\nYour Transaction is complete")
                print("Transaction number: ", random.randint
                (10000, 1000000))
                print("Thanks for choosing us as your bank")
                break
