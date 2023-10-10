from datetime import datetime
import pandas as pd
import matplotlib.pyplot as plt
import statsmodels.api as sm
import numpy as np
import seaborn as sns
from datetime import datetime
sns.set()
import warnings
warnings.filterwarnings('ignore')

df = pd.read_csv(r"C:\Users\arjd2\OneDrive\Documents\GitHub\JPMC_Quant_Research\task1\code\output.csv")
df['date'] = pd.to_datetime(df['date'])
df.set_index('date', inplace=True)
df.drop(columns='price_pred', inplace=True)

def calculate_contract_value(injection_dates, withdrawal_dates, purchase_prices, sale_prices, injection_rate, withdrawal_rate, max_volume, storage_costs):
    """
    Calculate the value of a gas storage contract.

    Args:
        injection_dates (list of datetime): List of injection dates.
        withdrawal_dates (list of datetime): List of withdrawal dates.
        purchase_prices (list of float): List of purchase prices on injection dates.
        sale_prices (list of float): List of sale prices on withdrawal dates.
        injection_rate (float): Rate at which gas can be injected (monthly).
        withdrawal_rate (float): Rate at which gas can be withdrawn (monthly).
        max_volume (float): Maximum volume that can be stored.
        storage_costs (float): Monthly storage costs.

    Returns:
        float: The value of the gas storage contract.
    """
    # Initialize the contract value
    contract_value = 0.0

    # Iterate through injection and withdrawal dates
    for i in range(len(injection_dates)):
        
        # Calculate the gas volume injected and withdrawn for this period
        injected_volume = max_volume * injection_rate
        withdrawn_volume = max_volume * withdrawal_rate

        # Calculate the cash flows for this period
        cash_inflow = injected_volume * purchase_prices[i]
        cash_outflow = withdrawn_volume * sale_prices[i]
        storage_cost = max_volume * storage_costs
        
        print(f"Buy value: ${round(cash_inflow,2)}")
        print(f"Sale value: ${round(cash_outflow, 2)}")
        print(f"Storage cost: ${round(storage_cost,2)}")

        # Update the contract value by adding the net cash flow and deducting storage costs
        contract_value = contract_value + (cash_outflow - cash_inflow - storage_cost)
        # print(f"contract value: ", contract_value)

    return contract_value

def run_test_cases():
    # Test case 1: Basic contract with single injection and withdrawal
    injection_dates_1 = [datetime(2023, 1, 1)]
    withdrawal_dates_1 = [datetime(2023, 2, 1)]
    purchase_prices_1 = [2.0]
    sale_prices_1 = [3.0]
    injection_rate_1 = 0.02  # 2% per month
    withdrawal_rate_1 = 0.03  # 3% per month
    max_volume_1 = 10000.0  # Maximum volume in cubic meters
    storage_costs_1 = 0.1  # Monthly storage costs

    contract_value_1 = calculate_contract_value(injection_dates_1, withdrawal_dates_1, purchase_prices_1, sale_prices_1, injection_rate_1, withdrawal_rate_1, max_volume_1, storage_costs_1)
    print(f"Test Case 1: The value of the contract is ${contract_value_1:.2f}")

    # Test case 2: Multiple injections and withdrawals with different prices
    injection_dates_2 = [datetime(2023, 1, 1), datetime(2023, 2, 1)]
    withdrawal_dates_2 = [datetime(2023, 4, 1), datetime(2023, 5, 1)]
    purchase_prices_2 = [2.0, 2.5]
    sale_prices_2 = [3.5, 3.0]
    injection_rate_2 = 0.02  # 2% per month
    withdrawal_rate_2 = 0.03  # 3% per month
    max_volume_2 = 10000.0  # Maximum volume in cubic meters
    storage_costs_2 = 0.1  # Monthly storage costs

    contract_value_2 = calculate_contract_value(injection_dates_2, withdrawal_dates_2, purchase_prices_2, sale_prices_2, injection_rate_2, withdrawal_rate_2, max_volume_2, storage_costs_2)
    print(f"Test Case 2: The value of the contract is ${contract_value_2:.2f}")

    # Test case 3: High storage costs, which affect contract value
    injection_dates_3 = [datetime(2023, 1, 1), datetime(2023, 2, 1)]
    withdrawal_dates_3 = [datetime(2023, 3, 1), datetime(2023, 4, 1)]
    purchase_prices_3 = [2.0, 2.5]
    sale_prices_3 = [3.5, 3.0]
    injection_rate_3 = 0.02  # 2% per month
    withdrawal_rate_3 = 0.03  # 3% per month
    max_volume_3 = 10000.0  # Maximum volume in cubic meters
    storage_costs_3 = 0.5  # High monthly storage costs

    contract_value_3 = calculate_contract_value(injection_dates_3, withdrawal_dates_3, purchase_prices_3, sale_prices_3, injection_rate_3, withdrawal_rate_3, max_volume_3, storage_costs_3)
    print(f"Test Case 3: The value of the contract is ${contract_value_3:.2f}")

# Function to find the nearest value in the DataFrame
def find_nearest_value(df, dates, purchase=False, sell=False):
    
    if purchase == True:
        nearest_values_purchase = []
        for date in dates:
            nearest_date = min(df.index, key=lambda x: abs(x - date))
            nearest_value = df.loc[nearest_date]['price']
            nearest_values_purchase.append(nearest_value)
        return nearest_values_purchase
    
    if sell == True:
        nearest_values_sell = []
        for date in dates:
            nearest_date = min(df.index, key=lambda x: abs(x - date))
            nearest_value = df.loc[nearest_date]['price']
            nearest_values_sell.append(nearest_value)
        return nearest_values_sell



if __name__ == "__main__":
    # List of injection and withdrawal dates
    injection_dates = [datetime(2023, 10, 30), datetime(2024, 3, 30)]
    withdrawal_dates = [datetime(2025, 11, 29), datetime(2025, 11, 29)]

    # Find nearest values for injection dates
    nearest_injection_values = find_nearest_value(df, injection_dates, purchase=True)
    # Find nearest values for withdrawal dates
    nearest_withdrawal_values = find_nearest_value(df, withdrawal_dates, sell=True)

    injection_rate = 0.02  # 2% per month
    withdrawal_rate = 0.03  # 3% per month
    max_volume = 10000.0  # Maximum volume in cubic meters
    storage_costs = 0.1  # High monthly storage costs

    contract_value = calculate_contract_value(injection_dates, withdrawal_dates, nearest_injection_values, nearest_withdrawal_values, injection_rate, withdrawal_rate, max_volume, storage_costs)
    print(f"The value of the contract is : ${contract_value:.2f}")

    