import requests
from bs4 import BeautifulSoup

def getSP500SymbolsFromWiki():
    # Wikipedia page URL
    url = 'https://en.wikipedia.org/wiki/List_of_S%26P_500_companies#S&P_500_component_stocks'

    # Send a GET request to URL
    response = requests.get(url)

    # create soup object that can find HTML content
    soup = BeautifulSoup(response.content, 'html.parser')

    # use soup object to find the table containing the list of S&P 500 companies (found element id using inspect on Wikipedia page) and assign it to a variable (the found element 'table' is a generic HTML element)
    table = soup.find('table', {'id': 'constituents'})

    # get symbols from from the table (generic HTML element)
    sp500_symbols = []
    for row in table.find_all('tr')[1:]: # find all rows after header
        column_data = row.find_all('td') # put company/row data into a list
        if len(column_data) >= 2: # if the list has at least 2 values
            symbol = column_data[0].text.strip() # grab the first value's text (no whitespace) and assign it as symbol
            sp500_symbols.append(symbol) # add it to the symbols list

    return sp500_symbols

def get_NYSE_NASDAQ_Symbols():
    # API request to fetch all stock symbols
    response = requests.get('https://www.alphavantage.co/query?function=LISTING_STATUS&apikey=QY73AL7RJZDQESXX')

    # read response csv text and split the data by lines
    lines = response.text.splitlines()
    # get list of column names from the data's first line
    column_names = lines[0].split(',')
    # create empty list of dictionaries
    data = []
    # loop through the rest of the lines
    for line in lines[1:]:
        # split line into values and put into list named values
        values = line.split(',')
        # create a dictionary with column_names as keys and values as values
        company_dict = {}
        for i in range(len(column_names)):
            company_dict[column_names[i]] = values[i]
        # append the dictionary to the list of data
        data.append(company_dict)

    # create empty list for S&P 500 symbols
    NYSE_NASDAQ_Symbols = []
    # loop through company dictionaries and add symbols from S&P 500 to the sp500_symbols list
    for company_dict in data:
        if (company_dict['exchange'] == 'NYSE' or company_dict['exchange'] == 'NASDAQ'):
            NYSE_NASDAQ_Symbols.append(company_dict['symbol'])
    return NYSE_NASDAQ_Symbols