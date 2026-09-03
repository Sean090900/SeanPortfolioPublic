import numpy as np
import pandas as pd

# Distance from last transaction
def calc_dist_from_last_transaction(df):
    # Sort once by cc_num and unix_time
    df = df.sort_values(['cc_num', 'unix_time'])

    # Previous transaction location per card
    merch_long_last_transaction = (
        df.groupby('cc_num')['merch_long'].shift(1)
    )
    merch_lat_last_transaction = (
        df.groupby('cc_num')['merch_lat'].shift(1)
    )

    # Calculate deltas in long and lat (NaN for first transaction per card)
    dlong = df['merch_long'] - merch_long_last_transaction
    dlat = df['merch_lat'] - merch_lat_last_transaction

    # Add values and return
    df['dist_last_transaction'] = np.sqrt(dlong**2 + dlat**2)
    return df

# Distance between Merchant and Customer
def calc_dist_between_merch_and_customer(df):
    # Calculate deltas in long and lat
    dlong = df['merch_long'] - df['long']
    dlat = df['merch_lat'] - df['lat']

    # Add values and return
    df['dist_between_merch_and_customer'] = np.sqrt(dlong**2 + dlat**2)
    return df

# Age at time of transaction
def calc_age_at_time_of_transaction(df):
    # Mapping month to coresponding numeric value
    month_map = {
        'January':1, 'February':2, 'March':3, 'April':4, 'May':5, 'June':6,
        'July':7, 'August':8, 'September':9, 'October':10, 'November':11, 'December':12
    }

    # Make 'dob' datetime
    df['dob'] = pd.to_datetime(df['dob'], format='mixed')

    # Make trans_date datetime field
    df['trans_date'] = pd.to_datetime(dict(
        year=df['year_date'].astype(int),
        month=df['month_date'].map(month_map),
        day=df['day_date'].astype(int)
    ))

    # Calculate age at time of transaction
    df['age_at_time_of_transaction'] = (df['trans_date'] - df['dob']).dt.days / 365.25

    # Remove temporary trans_date feature
    df = df.drop('trans_date', axis=1)
    return df

def calc_customer_specific_transaction_trends(df):
    # Group dataframe by customer
    df = df.copy()
    grp = df.groupby("cc_num")

    # Expanding mean/std of amount, using only past transactions
    cust_amt_exp_mean = grp["amt"].expanding().mean().shift(1)
    cust_amt_exp_std = grp["amt"].expanding().std(ddof=0).shift(1)

    df["cust_amt_mean_prev"] = cust_amt_exp_mean.values
    df["cust_amt_std_prev"] = cust_amt_exp_std.values

    # Fill NaNs for first transaction with global stats
    global_amt_mean = df["amt"].mean()
    global_amt_std = df["amt"].std(ddof=0)

    df["cust_amt_mean_prev"] = df["cust_amt_mean_prev"].fillna(global_amt_mean)
    df["cust_amt_std_prev"] = df["cust_amt_std_prev"].fillna(global_amt_std)

    # Z-score of current amount vs previous customer history
    df["cust_amt_zscore"] = (
        (df["amt"] - df["cust_amt_mean_prev"]) /
        df["cust_amt_std_prev"].replace(0, np.nan)
    ).fillna(0.0)

    return df

# Transaction Velocity
def calc_transaction_velocity(df, lookback_seconds=3600):
    # Sort to ensure proper temporal ordering
    df = df.sort_values(["cc_num", "unix_time"]).reset_index(drop=True)

    velocities = []
    current_customer = None
    customer_times = []

    col_name = f"txn_velocity_{lookback_seconds}s"

    for _, row in df.iterrows():
        cc = row["cc_num"]
        t = row["unix_time"]

        # When cc_num changes, start a new time list
        if cc != current_customer:
            current_customer = cc
            customer_times = []

        # Remove events outside the lookback window
        cutoff = t - lookback_seconds
        customer_times = [ts for ts in customer_times if ts >= cutoff]

        # Velocity = number of past transactions inside window
        velocities.append(len(customer_times))

        # Add current timestamp to the history AFTER computing velocity
        customer_times.append(t)

    df[col_name] = velocities
    return df