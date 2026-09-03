# SecureBank Assignment


## Prerequisites

Before starting, make sure you have completed the following:

1. **Review**:
   - *Machine Learning Systems Fundamentals Module*
   - *Tutorials*
   - *SecureBank Case Study Background*

2. **Dataset**: The SecureBank case study includes three raw data sources provided by different gatekeepers:
   - `customer_release.csv`
   - `transactions_release.parquet`
   - `fraud_release.json`  
     *(The dictionary structure is recorded using the same order as `transactions_release.parquet`, with the corresponding value as `is_fraud`).*

3. **File Organization**: Place these files in a directory named `securebank/data_sources/`. For example:
   ```
   <BASE_DIRECTORY>/securebank/data_sources/customer_release.csv
   ```

**Important:** Do **NOT** check these data files (or any data files) into GitHub. Instead, add them to a `.gitignore` file.



## Objectives

- **Task 1**:  
  Familiarize yourself with the SecureBank dataset and create a Python class `RawDataHandler` to handle **data extraction, transformation, and descriptive analysis** of raw data for machine learning tasks.  
  - You may only use the Python packages listed in the Tutorial section.  
  - The [Pandas documentation](https://pandas.pydata.org/docs/) may be helpful.

- **Tasks 2–4**:  
  The current `Model` class (`securebank/modules/model.py`) returns a random binary integer.  
  You will:
  1. Implement a **Dockerized Flask server**.  
  2. Build a **Dockerfile** to run the system.  
  3. Write a **README** with quick start instructions and a test `curl` command.

> **NOTE: Do NOT develop a model for this assignment. You will do this throughout the semester as part of your final case submission.**


## Instructions

Use (your provisioned repository)[TODO: Insert link here] to fork the SecureBank base repository for this assignment into your personal GitHub account. Please update your current repository as there may be updates to the repository. Make your changes as directed by the instructions and push your changes into your repository. *Unit test automatically runs when you push new commits to your repository.*


## Task 1: Implement the `RawDataHandler` Class

Save your implementation in:  
```
securebank/modules/data/raw_data_handler.py
```

Your class should avoid **hardcoded paths** and **unnecessary imports**.

### A. Class Definition

```python
class RawDataHandler:
    """
    Handles extraction, transformation, and description 
    of raw data for machine learning preprocessing.
    """
```

### B. Initialization

```python
def __init__(self, storage_path: str, save_path: str):
    self.storage_path = storage_path
    self.save_path = save_path
```

Parameters:
- `storage_path`: Path where the raw data files are stored.  
- `save_path`: Path where cleaned data will be saved.  



### C. Class Methods

#### 1. `extract()`
**Purpose:** Reads raw data files and returns them as DataFrames.  
**Parameters:**
- `customer_information_filename` (CSV)  
- `transaction_filename` (Parquet)  
- `fraud_information_filename` (JSON)  

**Output:**  
- `customer_information` (DataFrame)  
- `transaction_information` (DataFrame)  
- `fraud_information` (DataFrame)



#### 2. `convert_dates()`
**Purpose:** Converts `trans_date_trans_time` into seven distinct columns:  
- `day_of_week` (string, e.g. Monday)  
- `hour` (int 0–23)  
- `minute` (int 0–59)  
- `seconds` (int 0–59)  
- `day_date` (int 1–31)  
- `month_date` (string, e.g. January)  
- `year_date` (int, e.g. 2025)

**Input:** DataFrame with `trans_date_trans_time`.  
**Output:** Modified DataFrame with these new columns appended (and `trans_date_trans_time` removed).



#### 3. `transform()`
**Purpose:** Prepares and cleans data by:  
- Merging the three data sources  
- Imputing/dropping missing values  
- Dropping duplicate rows  

**Input:**  
- `customer_information`  
- `transaction_information`  
- `fraud_information`  

**Output:** A cleaned and merged DataFrame where each row is a **unique transaction** with all relevant information.



#### 4. `describe()`
**Purpose:** Produces a summary of quality metrics.  
**Input:** `raw_data` (cleaned DataFrame)  
**Output:** Dictionary with:
- `"number_of_records"` (int)  
- `"number_of_columns"` (int)  
- `"feature_names"` (list of str)  
- `"number_missing_values"` (int)  
- `"column_data_types"` (list of str)  



### Example Runner

```python
# Initialize handler
handler = RawDataHandler(storage_path="path/to/data_sources", save_path="path/to/output")

# Extract raw data
customer_info, transaction_info, fraud_info = handler.extract(
    "customers.csv", "transactions.parquet", "fraud.json"
)

# Transform the data
cleaned_data = handler.transform(customer_info, transaction_info, fraud_info)
cleaned_data = handler.convert_dates(cleaned_data)

# Describe the cleaned data
description = handler.describe(cleaned_data)
print(description)
```


## Task 2: Flask Server

Create a Flask app in `securebank/app.py` with an endpoint:

**Endpoint:**  
```
predict/
```

**Functionality:** Calls `Model.predict(input_data)` to classify a transaction as *legitimate* or *fraudulent*.  

**Input Format (JSON):**
```json
{
  "trans_date_trans_time": "...",
  "cc_num": "...",
  "unix_time": "...",
  "merchant": "...",
  "category": "...",
  "amt": "...",
  "merch_lat": "...",
  "merch_long": "..."
}
```

> *For the final case study, additional endpoints will be required. You do **not** need to train a model for this task.*



## Task 3: Dockerfile

Write `securebank/Dockerfile` to:
- Build a Docker image  
- Run a container for interaction with the system  



## Task 4: README

In `securebank/README.md`, include:
- **Quick start instructions** for starting the server with Docker  
- The **curl command** you used to test predictions  



## Submission & Evaluation

Check in (i.e., git push) all implementation files into your provisioned GitHub repository. Provide the **repository URL** before the deadline to receive credit. After checking this in, GitHub Classroom with automatically run the autograder. 

1. **Push your work**  
   Check in (i.e., `git push`) all implementation files into your provisioned GitHub repository.  

2. **Submit your repository URL**  
Provide the **repository URL** before the deadline to receive credit. 

3. **Autograder execution**  
Once you push to GitHub, **GitHub Classroom** will automatically run the autograder on your submission.  
- You can view the results under the **Actions** tab of your repository.  
- Each push to your repository will re-trigger the autograder.  
- The autograder runs unit tests to check correctness of your code and may also check for:
  - File naming conventions  
  - Method signatures  
  - Correctness of outputs  
  - Presence of required files

4. **Checking your grade**  
- Go to your repository on GitHub.  
- Click the **Actions** tab.  
- Select the latest workflow run (triggered by your most recent commit).  
- Expand the **Autograder job** to see detailed test results.  
- A ✅ indicates a passed test; a ❌ indicates a failed test.  

5. **Resubmissions**  
- If you fail tests, you can fix your code and push again.  
- Each new commit will re-run the autograder.  
- Only the **latest successful run before the deadline** counts toward your grade.  


