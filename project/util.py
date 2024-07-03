class AccountInformation:
    def __init__(self, name, available, current, limit):
        self.name = name
        self.available = available
        self.current = current
        self.limit = limit
        self.utilization = "N/A"
        self.institution_name = "Unpopulated"

        if self.limit != None:
            self.utilization = "{0:.2f}".format(100 * self.current / self.limit)

def get_account_info(account):
    return AccountInformation(account.name, 
                              account.balances.available, 
                              account.balances.current, 
                              account.balances.limit)
