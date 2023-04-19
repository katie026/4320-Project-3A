from flask import Flask, render_template, request, flash
import pygal, lxml, requests
from datetime import datetime

def getData(timeSeries, symbol):
    # populate the query parameters
    queryData = {'function': '', 'symbol': '', 'interval': '', 'apikey': ''}
    queryData['function'] = timeSeries
    queryData['symbol'] = symbol
    queryData['apikey'] = "QY73AL7RJZDQESXX"
    if (timeSeries == "TIME_SERIES_INTRADAY"):
        queryData['interval'] = "15min"

    # request the data from alpha vantage
    alphavantageRequest = requests.get('https://www.alphavantage.co/query', params=queryData)

    # check if request successfull
    if alphavantageRequest.status_code == 200:
        # turn Response object into a python dictionary
        stocksDictionary = alphavantageRequest.json()
        return stocksDictionary
    else:
        flash("Error: Request failed")

def generateGraph(symbol, timeSeries, chart, stocksDictionary, startDate, endDate):
    # get the name of the data for that time series ex. 'Monthly Time Series'
    timeSeriesKeys = list(stocksDictionary.keys())
    if len(timeSeriesKeys) > 1:
        # timeSeriesName = timeSeriesKeys[1]
        timeSeriesName = list(stocksDictionary)[1]

        # create a reference to the time series data
        timeSeriesData = stocksDictionary[timeSeriesName]

        # name graph
        displayStartDate = startDate.strftime("%Y/%m/%d")
        displayEndDate = endDate.strftime("%Y/%m/%d")
        graphTitle = f"Stock Data for {symbol}: {displayStartDate} to {displayEndDate}"

        # create graph based on selected chart
        if (chart == "Line"):
            finalGraph = generateLineGraph(timeSeries, timeSeriesData, startDate, endDate, graphTitle)
            return finalGraph
        if (chart == "Bar"):
            finalGraph = generateBarChart(timeSeries, timeSeriesData, startDate, endDate, graphTitle)
            return finalGraph
    else:
        flash("Error: No data in the stocksDictionary")

def generateLineGraph(timeSeries, timeSeriesData, startDate, endDate, graphTitle):
    # list the graph lines
    graphLines = ["1. open", "2. high", "3. low", "4. close"]

    # creating line graph
    lineGraph = pygal.Line(title=graphTitle, x_label_rotation=45, x_value_formatter=lambda dt: dt.strftime('%Y-%m-%d %H:%M:%S'))

    # loop through each line
    for line in graphLines:
        # create list of data points for the line
        dataPoints = list()
        x_labels = list()
        # loop through the timeSeriesData (objects) to populate dataPoints list
        for date, values in timeSeriesData.items():
            # turn the date string into a datetime object
            if (timeSeries == "TIME_SERIES_INTRADAY"):
                date = datetime.strptime(date, "%Y-%m-%d %H:%M:%S")
            else:
                date = datetime.strptime(date, "%Y-%m-%d")
            # find objects based on date range
            if date > startDate and date < endDate:
                # add date to x-axis label list (assign x-coordinate the date)
                if (timeSeries == "TIME_SERIES_INTRADAY"):
                    x_labels.insert(0, date.strftime("%Y/%m/%d %H:%M:%S"))
                else:
                    x_labels.insert(0, date.strftime("%Y/%m/%d"))
                # assign y-coordinate it's value based on the current key (line name)
                y = float(values[line])
                # add the y-coordinate to the list of data points
                dataPoints.append(y)
        # add the line with all of the data points
        lineGraph.add(line, dataPoints)
    
    # set x-axis labels
    lineGraph.x_labels = x_labels

    return lineGraph

def generateBarChart(timeSeries, timeSeriesData, startDate, endDate, graphTitle):
    # list the chart labels
    chartLabels = ["1. open", "2. high", "3. low", "4. close"]

    # creating bar chart
    barChart = pygal.Bar(title=graphTitle, x_label_rotation=45)

    # loop through each label
    for label in chartLabels:
        x_labels = list() # dates in the range
        dataPoints = list() # values per label (date is determined by x-labels)
        # loop through the timeSeriesData (objects) to popoulate dataPoints list
        for date, values in timeSeriesData.items():
            # turn the date string into a datetime object
            if (timeSeries == "TIME_SERIES_INTRADAY"):
                date = datetime.strptime(date, "%Y-%m-%d %H:%M:%S")
            else:
                date = datetime.strptime(date, "%Y-%m-%d")
            # find objects based on date range
            if date > startDate and date < endDate:
                # add date to x-axis label list
                if (timeSeries == "TIME_SERIES_INTRADAY"):
                    x_labels.insert(0, date.strftime("%Y/%m/%d %H:%M:%S"))
                else:
                    x_labels.insert(0, date.strftime("%Y/%m/%d"))
                # add value to data point list
                y = float(values[label])
                dataPoints.append(y)
        # add data to chart
        barChart.add(label, dataPoints)
    
    # set x-axis labels
    barChart.x_labels = x_labels
    
    return barChart