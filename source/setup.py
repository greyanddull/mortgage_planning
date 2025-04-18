import yaml
from datetime import datetime
from class_defs import Account, Expense, Mortgage  # <- import your Mortgage class too

def load_config(config_path: str):
    with open(config_path, 'r') as f:
        data = yaml.safe_load(f)

    global_start_date = data['start_date']
    global_end_date = data['end_date']

    # Create account objects
    accounts = {
        name: Account(name, **info)
        for name, info in data['accounts'].items()
    }

    # Create expense objects
    expenses = []
    for e in data['expenses']:
        freq = e.get('frequency', 'monthly')

        exp_start_date = e.get('start_date', global_start_date)
        exp_end_date = e.get('end_date', global_end_date)
        one_off_date = e.get('one_off_date')

        if freq == 'once':
            if not one_off_date:
                raise ValueError(f"One-off expense '{e['name']}' is missing 'one_off_date'")
            exp_start_date = one_off_date
            exp_end_date = one_off_date

        expenses.append(Expense(
            name=e['name'],
            start_date=exp_start_date,
            end_date=exp_end_date,
            amount=e['amount'],
            frequency=freq,
            day_of_month=e.get('day_of_month'),
            one_off_date=one_off_date,
            source_account=e.get('source_account'),
            destination_account=e.get('destination_account'),
            linked_to=e.get('linked_to')
        ))

    mortgage_data = data.get('mortgage')
    if mortgage_data:
        mortgage = Mortgage(
            principal=mortgage_data['principal'],
            annual_rate=mortgage_data['annual_rate'],
            start_date=mortgage_data['start_date']
        )
    else:
        mortgage = None

    return global_start_date, global_end_date, accounts, expenses, mortgage