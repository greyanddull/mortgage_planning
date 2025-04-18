#!/bin/bash

# How we could afford the 450,000 house bought in June 2025 (i.e. now). - Comparison between purchase of 450,000 house in June compared to October
#
# Assuming we are able to put down a 70,000 deposit, we see that we can afford the rent and the mortgage at £1250 for the rent and £2275 for the mortgage. In the long term there is a marginal difference. The difference comes from having put down a smaller deposit and borrowing more money but whether this was good or bad depends on savings and mortgage interest rates.
#

python3 multi_model_time_step.py config.wall450.20yr.purchaseJune config.wall450.20yr.purchaseOct


# HOWEVER, we see from the following comparison that it is difficult to survive the change in income with the 450,000 house even at a 20-year mortgage. A comparison between the 20-year 450,000 house at ECMWF compared to switching to James switching to a 45,000 salary in October 2027.
#
# While it seems to be technically possible, we are losing £7.43 per day (still assuming that we're able to live on £100 per day)
# Especially if we have children, we are topping up daily expenses with savings accrued during time at ECMWF
#
# This plot really just highlights the need to maintain job at ECMWF

python3 multi_model_time_step.py config.wall450.20yr.purchaseJune config.wall450.20yr.purchaseJune.LoseJob.Trickle

# 
# Perhaps a better method is to dump all savings and pension into the mortgage in October 2027 so we compare that to the trickle method above
#

python3 multi_model_time_step.py config.wall450.20yr.purchaseJune.LoseJob.Dump config.wall450.20yr.purchaseJune.LoseJob.Trickle

