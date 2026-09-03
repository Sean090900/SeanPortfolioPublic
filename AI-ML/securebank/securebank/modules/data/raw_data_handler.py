from datetime import datetime
import pandas as pd

class RawDataHandler:
    """
    Handles extraction, transformation, and description 
    of raw data for machine learning preprocessing.
    """

    def __init__(self, storage_path: str, save_path: str):
        self.storage_path = storage_path
        self.save_path = save_path

    def extract(self, customer_information_filename, transaction_filename, fraud_information_filename):
        """
        Reads raw data files and returns them as DataFrames.  
        Parameters:
            `customer_information_filename` (CSV)  
            `transaction_filename` (Parquet)  
            `fraud_information_filename` (JSON)  
        Output: 
            `customer_information` (DataFrame)  
            `transaction_information` (DataFrame)  
            `fraud_information` (DataFrame)
        """
        # Convert `customer_information_filename` to DataFrame
        customer_info = pd.read_csv(self.storage_path + '/' + customer_information_filename)

        # Convert `transaction_filename` to DataFrame
        transaction_info = pd.read_parquet(self.storage_path + '/' + transaction_filename).reset_index()

        # Convert `fraud_information_filename` to DataFrame
        fraud_info = pd.read_json(self.storage_path + '/' + fraud_information_filename, orient='index').reset_index()
        fraud_info.columns = ['trans_num', 'is_fraud']

        # Return tuple of DataFrames
        return (customer_info, transaction_info, fraud_info)

    def convert_dates(self, df):
        """
        Converts `trans_date_trans_time` into seven distinct columns:  
            `day_of_week` (string, e.g. Monday)  
            `hour` (int 0–23)  
            `minute` (int 0–59)  
            `seconds` (int 0–59)  
            `day_date` (int 1–31)  
            `month_date` (string, e.g. January)  
            `year_date` (int, e.g. 2025)
        Input: DataFrame with `trans_date_trans_time`.  
        Output: Modified DataFrame with these new columns appended (and `trans_date_trans_time` removed).
        """
        # Initialize `month to num` dictionary
        month_to_num = {
            1: 'January',
            2: 'February',
            3: 'March',
            4: 'April',
            5: 'May',
            6: 'June',
            7: 'July',
            8: 'August',
            9: 'September',
            10: 'October',
            11: 'November',
            12: 'December',
        }

        # For each row in df, add parsed data to new columns
        for index, row in df.iterrows():

            # Parse date and time
            date_str = row['trans_date_trans_time']
            date = datetime.strptime(date_str, '%Y-%m-%d %H:%M:%S')

            # Assign values to new df columns
            df.at[index, 'day_of_week'] = date.strftime('%A')
            df.at[index, 'hour'] = date.hour
            df.at[index, 'minute'] = date.minute
            df.at[index, 'seconds'] = date.second
            df.at[index, 'day_date'] = date.day
            df.at[index, 'month_date'] = month_to_num[date.month]
            df.at[index, 'year_date'] = date.year

        # Drop `trans_date_trans_time` columns from df
        df = df.drop('trans_date_trans_time', axis=1)

        # Return df
        return df
        
    def transform(self, customer_information, transaction_information, fraud_information):
        """
        Prepares and cleans data by:  
            Merging the three data sources  
            Inputing/dropping missing values  
            Dropping duplicate rows
        Input:
            `customer_information`
            `transaction_information`
            `fraud_information`
        Output: A cleaned and merged DataFrame where each row is a **unique transaction** with all relevant information.
        """
        # Merge `customer_info` and `transaction_info` on column: `cc_num`
        first = customer_information.merge(transaction_information, on='cc_num', how='outer')
        first = first.drop(['index_x', 'index_y'], axis=1)

        # Merge the first df with `fraud_info` on column: `trans_num`
        second = first.merge(fraud_information, on='trans_num', how='outer')

        # Return second dataframe
        return second

    def describe(self, raw_data):
        """
        Produces a summary of quality metrics.  
        Input: `raw_data` (cleaned DataFrame)
        Output: Dictionary with:
            `"number_of_records"` (int)  
            `"number_of_columns"` (int)  
            `"feature_names"` (list of str)  
            `"number_missing_values"` (int)  
            `"column_data_types"` (list of str)  
        """
        # Initialize output dict
        output = {}

        # Gather quailty metrics from raw_data
        output['number_of_records'] = len(raw_data)
        output['number_of_columns'] = len(raw_data.columns)
        output['feature_names'] = raw_data.columns
        output['number_missing_values'] = int(raw_data.isna().sum().sum())
        output['column_data_types'] = [type(item) for item in list(raw_data.loc[0])]

        # Return quailty metrics
        return output


if __name__ == '__main__':

    # Initialize handler
    handler = RawDataHandler(storage_path="../../data_sources", save_path="../../storage/temp")

    # Extract raw data
    customer_info, transaction_info, fraud_info = handler.extract(
        "customer_release.csv", "transactions_release.parquet", "fraud_release.json"
    )

    # Transform the data
    cleaned_data = handler.transform(customer_info, transaction_info, fraud_info)
    cleaned_data = handler.convert_dates(cleaned_data)

    # Describe the cleaned data
    description = handler.describe(cleaned_data)
    print(description)