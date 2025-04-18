import matplotlib.pyplot as plt
import random
from datetime import date
import numpy as np

def summarize_config(start_date, end_date, accounts, expenses):
    print("\n📅 Simulation Period")
    print(f"  From {start_date} to {end_date}")

    print("\n🏦 Accounts")
    for name, acc in accounts.items():
        print(f"  - {name.capitalize()}:")
        print(f"      Starting amount : {acc.starting_amount:.2f}")
        print(f"      Interest rate   : {acc.interest_rate * 100:.2f}%")
        print(f"      Tax rate        : {acc.tax_rate * 100:.2f}%")

    print("\n💸 Expenses")
    for exp in expenses:

        # Frequency label
        if exp.frequency == 'once':
            freq_label = f"One-off ({exp.one_off_date})"
        elif exp.frequency == 'monthly':
            freq_label = f"Monthly (Day {exp.day_of_month})"
        else:
            freq_label = "Daily"

        direction = f"{exp.amount:+.2f}"
        src = exp.source_account or "N/A"
        dst = exp.destination_account or "N/A"
        linked = f" [Linked: {exp.linked_to}]" if exp.linked_to else ""
        print(f"  - {exp.name}{linked}")
        print(f"      Amount         : {direction}")
        print(f"      Frequency      : {freq_label}")
        print(f"      Active period  : {exp.start_date} → {exp.end_date}")
        print(f"      From           : {src}")
        print(f"      To             : {dst}")

    print("\n✅ Config loaded successfully.\n")

def plot_individual_accounts(ax, accounts, label_prefix="", mortgage=None):
    # Use history from the first account to define the date range
    dates = sorted(next(iter(accounts.values())).history.keys())

    for i, account in enumerate(accounts.values()):
        balances = [account.history[date] for date in dates]
        if i == 0 and label_prefix:
            label = f"{label_prefix} - {account.name.capitalize()}"
        else:
            label = None
        ax.plot(dates, balances, label=label)

    # ✅ Optionally plot mortgage debt as a separate line
    if mortgage:
        mortgage_balances = [mortgage.history.get(date, None) for date in dates]
        ax.plot(dates, mortgage_balances, label="Mortgage Debt", linestyle="--")

    ax.grid(True)

    return dates

def plot_total_balances(ax, accounts, expenses=None, label_prefix="", label_print=False):
    dates = sorted(next(iter(accounts.values())).history.keys())

    cash_accounts = ['current', 'savings']
    asset_accounts = ['current', 'savings', 'house']

    cash_balances = [
        sum(accounts[name].history[date] for name in cash_accounts if name in accounts)
        for date in dates
    ]
    total_balances = [
        sum(accounts[name].history[date] for name in asset_accounts if name in accounts)
        for date in dates
    ]

    ax.plot(dates, total_balances, linewidth=2, label=f"{label_prefix} Net Worth")
    ax.plot(dates, cash_balances, linestyle='--', label=f"{label_prefix} Cash (Current + Savings)")

    ax.grid(True)

    return dates, cash_balances

def add_linear_regression(ax, dates, values, fit_start_date: date, fit_end_date: date, label="Trend", color="orange"):
    # Filter dates and values within the fit window
    filtered = [(d, v) for d, v in zip(dates, values) if fit_start_date <= d <= fit_end_date]
    if len(filtered) < 2:
        print("❗ Not enough points for regression in given date range.")
        return

    fit_dates, fit_values = zip(*filtered)

    # Convert dates to numeric (e.g., days since start)
    x = np.array([(d - fit_dates[0]).days for d in fit_dates])
    y = np.array(fit_values)

    # Fit line
    coeffs = np.polyfit(x, y, 1)
    slope, intercept = coeffs

    # Create prediction line
    x_pred = np.array([(d - fit_dates[0]).days for d in dates if fit_start_date <= d <= fit_end_date])
    y_pred = slope * x_pred + intercept

    # Plot on same axis
    ax.plot(fit_dates, y_pred, linestyle='--', linewidth=2, color=color, label=label)

    # Show results
    print(f"📈 Fitted linear trend from {fit_start_date} to {fit_end_date}: slope = {slope:.2f}, intercept = {intercept:.2f}")

    return ax

    


