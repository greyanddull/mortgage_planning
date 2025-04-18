from datetime import date
from typing import Optional

class Expense:
    def __init__(self, name: str, start_date: date, end_date: date, amount: float,
                 frequency: str = 'monthly', day_of_month: Optional[int] = None,
                 one_off_date: Optional[date] = None,
                 source_account: Optional[str] = None, destination_account: Optional[str] = None,
                 linked_to: Optional[str] = None):
        """
        frequency: 'daily', 'monthly', or 'once'
        day_of_month: Required for 'monthly'
        one_off_date: Required for 'once'
        """
        self.name = name
        self.start_date = start_date
        self.end_date = end_date
        self.amount = amount
        self.frequency = frequency
        self.day_of_month = day_of_month
        self.one_off_date = one_off_date
        self.source_account = source_account
        self.destination_account = destination_account
        self.linked_to = linked_to

    def is_due(self, current_date: date) -> bool:
        if self.frequency == 'once':
            return current_date == self.one_off_date

        if not (self.start_date <= current_date <= self.end_date):
            return False

        if self.frequency == 'daily':
            return True
        elif self.frequency == 'monthly':
            return current_date.day == self.day_of_month

        return False

class Account:
    def __init__(self, name: str, starting_amount: float, interest_rate: float = 0.0, tax_rate: float = 0.0):
        """
        Represents a financial account with interest, tax, and time history.
        
        :param name: Name of the account
        :param starting_amount: Initial balance
        :param interest_rate: Annual interest rate (decimal), e.g. 0.03 for 3%
        :param tax_rate: Tax rate on interest earned (decimal)
        """
        self.name = name
        self.starting_amount = starting_amount
        self.balance = starting_amount
        self.interest_rate = interest_rate
        self.tax_rate = tax_rate
        self.history: Dict[date, float] = {}

    def apply_interest(self, days: int):
        daily_rate = self.interest_rate / 365
        interest = self.balance * daily_rate * days
        taxed_interest = interest * (1 - self.tax_rate)
        self.balance += taxed_interest

    def adjust_balance(self, amount: float):
        self.balance += amount

    def record_day(self, current_date: date):
        self.history[current_date] = self.balance

    def reset(self):
        self.balance = self.starting_amount
        self.history.clear()

class Mortgage:
    def __init__(self, principal: float, annual_rate: float, start_date: date):
        self.balance = principal
        self.annual_rate = annual_rate
        self.start_date = start_date
        self.history = {}

    def is_active(self, current_date: date):
        return self.balance > 0 and current_date >= self.start_date

    def calculate_monthly_interest(self):
        monthly_rate = self.annual_rate / 12
        return self.balance * monthly_rate

    def apply_payment(self, payment_amount: float, current_date: date):
        if not self.is_active(current_date):
            return 0.0, 0.0  # No interest or principal change

        interest = self.calculate_monthly_interest()
        principal = min(payment_amount - interest, self.balance)  # Prevent overpay

        self.balance -= principal
        self.history[current_date] = self.balance

        return interest, principal

    def record_day(self, current_date: date):
        self.history[current_date] = self.balance
