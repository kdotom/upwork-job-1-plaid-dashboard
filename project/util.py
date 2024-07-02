class AccountInformation:
    def __init__(self, name, available, current, limit):
        self.name = name
        self.available = available
        self.current = current
        self.limit = limit

def get_account_info(account):
    return AccountInformation(account.name, 
                              account.balances.available, 
                              account.balances.current, 
                              account.balances.limit)
