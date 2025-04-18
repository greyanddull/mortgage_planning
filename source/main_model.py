import sys
from pathlib import Path
from setup import load_config
from model_engine import run_simulation
from print_and_plot import *
from datetime import date
import matplotlib.pyplot as plt

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python3 compare_models.py config1 [config2 ...]")
        sys.exit(1)

    config_names = sys.argv[1:]
    all_cash_lines = []
    all_dates = []
    all_labels = []
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 6), sharex=True)

    for config_name in config_names:
        # Full path to the config file
        config_path = Path("../configs") / f"{config_name}.yaml"

        # Extract readable label: just the part between 'config.' and '.yaml'
        readable_label = config_name
        if "config." in config_name:
            readable_label = config_name.split("config.")[1]
        readable_label = readable_label.replace(".yaml", "")  # Extra safety

        # Load config
        start_date, end_date, accounts, expenses, mortgage = load_config(config_path)

        # Run sim
        run_simulation(start_date, end_date, accounts, expenses, mortgage)

        # Plot individual accounts on left
        plot_individual_accounts(ax1, accounts, label_prefix=readable_label, mortgage=mortgage)

        # Plot total + cash on right (stack them)
        dates, cash_balances = plot_total_balances(
            ax2, accounts, expenses,
            label_prefix=readable_label,
            label_print=(config_name == config_names[0])  # only once
        )

        all_cash_lines.append(cash_balances)
        all_dates.append(dates)

        # Find daily disposable income
        ax2 = add_linear_regression(
        ax=ax2,
        dates=dates,
        values=cash_balances,
        fit_start_date=date(2031, 1, 1),
        fit_end_date=date(2035, 10, 1),
        label="Cash accrument rate 1",
        color="purple",
        config_name = config_name
        )

        # Find daily disposable income
        ax2 = add_linear_regression(
        ax=ax2,
        dates=dates,
        values=cash_balances,
        fit_start_date=date(2026, 10, 1),
        fit_end_date=date(2027, 10, 1),
        label="Cash accrument rate 2",
        color="green",
        config_name = config_name
        )

    # Final layout + show
    ax1.legend()
    ax2.legend()
    fig.tight_layout()
    plt.show()
