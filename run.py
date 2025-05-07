import gspread
from google.oauth2.service_account import Credentials
from pprint import pprint

SCOPE = [
    "https://www.googleapis.com/auth/spreadsheets",
    "https://www.googleapis.com/auth/drive.file",
    "https://www.googleapis.com/auth/drive"
    ]

CREDS = Credentials.from_service_account_file('creds.json')
SCOPED_CREDS = CREDS.with_scopes(SCOPE)
GSPREAD_CLIENT = gspread.authorize(SCOPED_CREDS)
SHEET = GSPREAD_CLIENT.open('love_sandwiches')


def get_sales_data():
    """
    Get sales figures input from the user
    """
    while True:
        print("Please enter sales data.")
        print("Data should be 6 numbers, separated by commas.")
        print("eg: 56,2,34,22,67,9\n")

        data_str= input("Enter your data here: ")
        sales_data = data_str.split(",")
        if validate_data(sales_data):
            print("Data is valid")
            return [int(value) for value in sales_data]

def validate_data(values):
    """
    Converts all strong values to intergers.
    Raises ValueError if string cannot be converted
    or if there aren't 6 values.
    """
    try:
        values =[int(value) for value in values]
        print(values)
        if len(values) != 6:
            raise ValueError(
                f"Numbers of values must equal 6. You provided {len(values)}"
            )
    except ValueError as e:
        print(f"Invalid data: {e}, please try again.\n")
        return False
    
    return True

def update_sales_worksheet(data):
    """
    Updates sales worksheet, add new row with the list data provided
    """
    print("updating sales worksheet...\n")
    sales_worksheet = SHEET.worksheet("sales")
    sales_worksheet.append_row(data)
    print("sales worksheet updated successfully\n")

def calculate_surplus_data(sales_row):
    """
    Compare sales with stock and calculate the surplus for each item
    """
    print("calculating surplus data...\n")
    stock = SHEET.worksheet("stock").get_all_values()
    stock_row = stock[-1]
    print(stock_row)

def main():
    data = get_sales_data()
    update_sales_worksheet(data)
    calculate_surplus_data(data)

print("WElcome to love sandwiches data automation")
main()
