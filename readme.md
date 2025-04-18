# Cash-Flow Analysis

This program aims to model income, outgoing, savings, mortgage, and house value to help in deciding personal financial decisions. 

## Getting Started

The requirements.txt contains the name and version of packages required to run the program.

### Examples

The `runme` file will run two examples which generate plots comparing two scenarios - a scenario in which one rents fulltime and a house purchase scenario. It's highly recommended to run the bash script `runme.sh`.

## Overview

### Running a Model

Run a model by defining a Scenario (see below) and then running,
```
python3 main_model.py config_sub_folder/scenario_1 config_sub_folder/scenario_2
```
Note that the program will look for the scenario config files from `/configs`, so no need to include that directory when running and no need to include the `*.yaml` extension.

### Scenarios

Scenarios are defined by the *.yaml config files found in the `configs` folder. Scenarios contain the definitions for various `account`, `expense` and `mortgage` classes of objects.

#### Account

The account class contains a value which is incremented on a daily basis by the account's interest rate - this is supposed to emulate a savings account which accrues daily interest. Accounts can be called anything, but the `mortgage` and `house` accounts are special cases because expenses sent to `house_and_mortgage` will be split by the interest payment and the capital and sent to those two accounts individually. 

#### Expense

The expense class contains objects which represent incomings or outgoings. Expenses have
- `value` (the amount moving between accounts)
- `frequency` (can be monthly, once, or daily)
- `source_account` (the account from which this expense comes from - for salary, the source account is `null`)
- `destination_account` (the account to which expenses go to - for bills, this is `null` i.e. money disappears and for mortgage payments, the destination account is house_and_mortgage)
- `day_of_month` in the case of monthly frequency payments

#### Mortgage

Mortgage is a special type of account which has become its own class. It tracks the debt owed while the interest paid is managed by - specifically - an object called "mortgage" which is actually an `account` object.
