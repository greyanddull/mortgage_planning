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

def plot_individual_accounts(ax, accounts, label_prefix="", mortgage=None, label_print=False):
    # Use history from the first account to define the date range
    dates = sorted(next(iter(accounts.values())).history.keys())

    for account in accounts.values():
        balances = [account.history[date] for date in dates]
        label = f"{label_prefix} - {account.name.capitalize()}" if label_print else None
        ax.plot(dates, balances, label=label)

    # ✅ Optionally plot mortgage debt as a separate line
    if mortgage:
        mortgage_balances = [mortgage.history.get(date, None) for date in dates]
        label = "Mortgage Debt" if label_print else None
        ax.plot(dates, mortgage_balances, linestyle="--", label=label)

    ax.grid(True)
    ax.set_ylabel("Value (currency)")

    return dates

def plot_total_balances(ax, accounts, expenses=None, label_prefix="", label_print=False, mortgage=None):
    dates = sorted(next(iter(accounts.values())).history.keys())

    plot_dream_home_reference_lines(ax, dates, start_values=None, growth_rate=0.05)

    # Get the next color in the cycle
    color = next(ax._get_lines.prop_cycler)['color']

    cash_accounts = ['current', 'savings']
    asset_accounts = ['current', 'savings', 'house_equity']

    cash_balances = [
        sum(accounts[name].history[date] for name in cash_accounts if name in accounts)
        for date in dates
    ]
    total_assets = [
        sum(accounts[name].history[date] for name in asset_accounts if name in accounts)
        for date in dates
    ]

    if mortgage:
        debt = [mortgage.history.get(date, 0) for date in dates]
        net_worth = [asset - d for asset, d in zip(total_assets, debt)]
    else:
        net_worth = total_assets

    # Plot each line with or without label depending on label_print
    if 'house_equity' in accounts:
        house_balances = [accounts['house_equity'].history[date] for date in dates]
        ax.plot(
            dates, house_balances,
            linestyle=':', color=color,
            label=f"{label_prefix} House Equity" if label_print else None
        )

    ax.plot(
        dates, total_assets,
        linestyle='-.', color=color,
        label=f"{label_prefix} Total Positive Assets" if label_print else None
    )

    ax.plot(
        dates, cash_balances,
        linestyle='--', color=color,
        label=f"{label_prefix} Cash (Current + Savings)" if label_print else None
    )

    ax.plot(
        dates, net_worth,
        linestyle='-', color=color,
        label=f"{label_prefix} Net Worth" if label_print else None
    )

    ax.grid(True)

    return dates, cash_balances

def plot_dream_home_reference_lines(ax, dates, start_values=None, growth_rate=0.03):
    """
    Plots reference lines for dream home prices increasing over time,
    with end-of-line labels showing the final price.

    Parameters:
        ax: Matplotlib axis to draw on.
        dates: List of datetime objects.
        start_values: List of starting home prices (e.g. [300000, 400000, 500000]).
        growth_rate: Annual percentage increase as a decimal (e.g. 0.03 for 3%).
    """
    if start_values is None:
        start_values = [100000, 200000, 250000, 300000, 350000, 400000, 450000, 500000, 600000, 700000]

    num_days = [(date - dates[0]).days for date in dates]
    ref_color = 'grey'
    ref_alpha = 1

    for base in start_values:
        line = [base * (1 + growth_rate) ** (days / 365.25) for days in num_days]
        ax.plot(dates, line, color=ref_color, linewidth=1, linestyle='--', alpha=ref_alpha)

        # Add label at the last date
        end_date = dates[-1]
        end_value = line[0]
        end_position = line[-1]
        ax.text(
            end_date, end_position,
            f"£{int(end_value//1000):,}K",
            fontsize=8,
            color=ref_color,
            alpha=ref_alpha,
            ha='left',
            va='center'
        )

        # Add label at the last date
        end_date = dates[0]
        end_value = line[0]
        end_position = line[0]
        ax.text(
            end_date, end_position,
            f"£{int(end_value//1000):,}K",
            fontsize=8,
            color=ref_color,
            alpha=ref_alpha,
            ha='right',
            va='center'
        )


def add_linear_regression(ax, dates, values, fit_start_date: date, fit_end_date: date, label=None, color="orange", config_name=None):
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
    ax.plot(fit_dates, y_pred, linestyle='--', linewidth=2, color=color, label=label+f" {config_name}")

    # Show results
    print(f"📈 Cash accrument for {config_name} from {fit_start_date} to {fit_end_date} = {30*slope:.2f} per 30 days")

    return ax

    


