from datetime import timedelta

def run_simulation(start_date, end_date, accounts, expenses, mortgage):
    from datetime import timedelta

    current_date = start_date
    print(f"\n🚀 Running simulation from {start_date} to {end_date}...\n")

    while current_date <= end_date:

        # Apply interest & record each day - this will increase the value of the house
        for account in accounts.values():
            account.apply_interest(days=1)
            account.record_day(current_date)

        # Calculate house equity based on mortgage just paid off
        if mortgage:
            if current_date == mortgage.start_date:
                accounts["house_value"].balance = mortgage.balance
            
            if current_date >= mortgage.start_date:
                accounts["house_equity"].balance = accounts["house_value"].balance - mortgage.balance

        # Apply expenses
        for exp in expenses:
            if not exp.is_due(current_date):
                continue

            # Special-case: handle 'house_and_mortgage' logic
            if exp.destination_account == "house_and_mortgage" or exp.name == "mortgage_payment":
                if mortgage:
                    interest, principal = mortgage.apply_payment(exp.amount, current_date)

                    # Handle cash leaving the source account
                    if exp.source_account:
                        accounts[exp.source_account].adjust_balance(-interest)
                        accounts[exp.source_account].adjust_balance(-principal)

                    # Interest goes to tracking (optional)
                    if "mortgage" in accounts:
                        accounts["mortgage"].adjust_balance(interest)

                continue  # Skip rest of loop for this expense

            # Normal expense handling
            amount = exp.amount

            if exp.source_account:
                source_acc = accounts[exp.source_account]
                source_acc.adjust_balance(-amount)

            if exp.destination_account:
                if exp.destination_account not in accounts:
                    raise KeyError(f"Unknown destination_account '{exp.destination_account}' in expense '{exp.name}'")
                dest_acc = accounts[exp.destination_account]
                dest_acc.adjust_balance(amount)

        # ✅ Record mortgage balance for this day
        if mortgage:
            mortgage.record_day(current_date)

        current_date += timedelta(days=1)

    print("✅ Simulation complete!\n")
