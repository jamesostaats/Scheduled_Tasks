import base64
import io
import pandas as pd


# Read user's .csv or Excel input and establishes usable dataset
def parse_contents(contents, filename):
    content_type, content_string = contents.split(',')
    decoded = base64.b64decode(content_string)
    if 'csv' in filename:
        df = pd.read_csv(io.StringIO(decoded.decode('utf-8')))
    elif 'xls' in filename:
        df = pd.read_excel(io.BytesIO(decoded))
    # if it is unable to read anything, it returns a blank dataframe
    else:
        df = pd.DataFrame()
    return df
    
    
# Intakes a user-provided dataset and validates it
def validate_data(data):
    # Add validation steps here
    # Should check if all required fields are there and filled out
    # For now, just checks if there are any rows in the table
    if len(data) == 0:
        msg = 'No Data Present'
    else:
        msg = 'Data Valid'
    return msg
    

# This is your main test function
# Right now it just adds a column, but you'd want your main operation to be here
# I would suggest splitting your function into several smaller ones and aggregating them here    
def main_function(data):
    data['NewColumn'] = 'Successful'
    return data