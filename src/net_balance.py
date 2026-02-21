import re

def net_balance_monthly(opening_balance, closing_balance):
    # extract float value from string "$34,897.60"
    opening_balance = float(re.sub(r'[^\d.]', '', opening_balance))
    closing_balance = float(re.sub(r'[^\d.]', '', closing_balance))
    # net balance round to 2 decimal places    
    net_balance = round(closing_balance - opening_balance, 2)

    return net_balance