# 🏦 Cash-Flow Analysis

This program models income, expenses, savings, mortgage payments, and house equity over time to support personal financial planning.

---

## 🚀 Getting Started

Install required packages using:

```bash
pip install -r requirements.txt
```

Or just run the helper script:

```bash
bash runme.sh
```

> 🔧 If any packages are missing, install them manually based on the error messages.

---

## ⚡ Quick Run

1. The `runme.sh` script runs two example scenarios:
   - Renting full-time
   - Purchasing a home

   This will generate comparative plots. Highly recommended!

2. Alternatively, run the program manually from the `source/` directory:

```bash
cd source/
python3 main_model.py examples/rent examples/300K_purchase
```

You can also run a single scenario if preferred.

---

## 🧠 How It Works

### Running a Model

Each scenario is defined by a YAML file stored in the `configs/` directory.

Run two scenarios side-by-side like this:

```bash
python3 main_model.py <config_sub_folder>/scenario_1 <config_sub_folder>/scenario_2
```

> 🔍 Do **not** include the `configs/` path or the `.yaml` extension in your arguments — the program handles that for you.

---

## 🗂️ Scenario Configuration

Each scenario file defines:
- Accounts
- Expenses
- Mortgage (if applicable)

These are represented as Python class instances via structured YAML.

### 💰 Account

Represents a financial account with daily interest accrual (e.g. savings).

Key points:
- Named freely (e.g. `current`, `savings`)
- Two special accounts:
  - `house`: Tracks home equity
  - `mortgage`: Tracks interest payments (see below)

When an expense is paid to the special `house_and_mortgage` destination:
- Interest goes to `mortgage`
- Principal goes to `house`

### 📉 Expense

Defines money moving between accounts. Could be income, bills, or transfers.

Each expense has:
- `amount`: How much is moved
- `frequency`: `daily`, `monthly`, or `once`
- `source_account`: Where the money comes from (`null` for income)
- `destination_account`: Where it goes (`null` for outflows)
- `day_of_month`: Used for monthly recurring payments

### 🏠 Mortgage

A special object tracking the mortgage loan balance.

- Uses its own `Mortgage` class (not a regular account)
- Tracks principal reduction over time
- Interest payments are routed to the `mortgage` account
- Principal payments increase the `house` account (equity)
