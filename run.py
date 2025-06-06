import gspread
from google.oauth2.service_account import Credentials

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

        data_str= input("Enter your data here: \n")
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
        if len(values) != 6:
            raise ValueError(
                f"Numbers of values must equal 6. You provided {len(values)}"
            )
    except ValueError as e:
        print(f"Invalid data: {e}, please try again.\n")
        return False
    
    return True

def calculate_surplus_data(sales_row):
    """
    Compare sales with stock and calculate the surplus for each item
    """
    print("calculating surplus data...\n")
    stock = SHEET.worksheet("stock").get_all_values()
    stock_row = stock[-1]
    stock_row_int =[int(stock_item) for stock_item in stock_row]

    surplus_data = []
    for stock, sales in zip(stock_row_int, sales_row):
        surplus = stock - sales
        surplus_data.append(surplus)

    return(surplus_data)

def update_worksheet(data,worksheet):
    """
    Receives data to be insterted into a worksheet.
    Updates the relevant worksheet.
    """
    print(f"updating {worksheet} worksheet...\n")
    worksheet_to_update = SHEET.worksheet(worksheet)
    worksheet_to_update.append_row(data)
    print(f"{worksheet} worksheet updated successfully\n")

def get_last_five_entries_sales():
    """
    Get the last 5 entries of sales data
    """
    sales = SHEET.worksheet("sales")
    columns = []
    for ind in range(1,7):
        column = sales.col_values(ind)[-5:]
        columns.append(column)
    return columns

def calculate_stock_data(data):
    """
    Funtion to calculate how muh stock to make for the next day of sandwiches
    """
    print('calculating stock data')
    new_stock_data = []
    for column in data:
        int_column = [int(num) for num in column]
        average = sum(int_column) / len(int_column)
        stock_num = average * 1.1
        new_stock_data.append(round(stock_num))
    return new_stock_data



def main():
    data = get_sales_data()
    update_worksheet(data, "sales")
    new_surplus_data = calculate_surplus_data(data)
    update_worksheet(new_surplus_data, "surplus")
    sales_columns = get_last_five_entries_sales()
    stock_data = calculate_stock_data(sales_columns)
    update_worksheet(stock_data, "stock")

print("Welcome to love sandwiches data automation")


main()
