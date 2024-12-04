# Project 3A

### Project 3
Scenario
A professor in your department is interested in tracking stock data trends and recently found the Alpha Vantage website. This site offers an api that returns historical stock data from the past 20 years. The data is returned in json and other formats. There is no way to visualize the data or choose a date range to view the data. The api, by default, returns 20 years of data for all but one of its functions.

Your team’s job is to create a python application that queries the [Alpha Vantage](https://www.alphavantage.co/) api, and allows the user to select a date range to view the data, and the type of chart they want to view the data in. Your team should use git and GitHub as a means of version control for the project.

The application should:
1. API
2. Ask the user to enter the stock symbol for the company they want data for.
3. Ask the user for the chart type they would like.
4. Ask the user for the time series function they want the api to use.
    - Type of graph: intraday (15 min), daily, weekly, monthly
5. Ask the user for the beginning date in YYYY-MM-DD format.
6. Ask the user for the end date in YYYY-MM-DD format. The end date should not be before the begin date.
7. Generate a graph and open in the user’s default browser.
