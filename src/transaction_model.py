class TransactionModel:
    def __init__(self, date, description, amount, balance):
        self.date = date
        self.description = description
        self.amount = amount
        self.balance = balance

    def __str__(self):
        return f"Transaction(date={self.date}, description={self.description}, amount={self.amount}, balance={self.balance})"