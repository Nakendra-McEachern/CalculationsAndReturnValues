from datetime import datetime
import csv
import os

# Convert a Fahrenheit temperature to Celsius.
def convertData(data):
    convertedValue = (data - 32) * 5 / 9
    return convertedValue

# Append comma-separated data to the CSV file and handle writing errors.
def insertData(filePath, data):
    try:
        with open(filePath, "a", newline="") as file:
            file.write(data + "\n")
        return True
    except OSError as error:
        print("Error writing to file:", error)
        return False

# Display the CSV file path and contents using read-only permissions.
def viewData(filePath):
    try:
        print("\nReading file:", os.path.abspath(filePath))
        with open(filePath, "r", newline="") as file:
            reader = csv.reader(file)
            for row in reader:
                print(",".join(row))
    except OSError as error:
        print("Error reading file:", error)

# Ask for dates and temperatures, convert them, and save each entry.
def getInput():
    try:
        numberOfEntries = int(input("How many entries are you inputting? "))
    except ValueError:
        print("Please enter a valid whole number.")
        return

    # Repeat the input process for the requested number of entries.
    for entry in range(numberOfEntries):
        inputDate = input("Enter a date: ")
        try:
            temperature = int(input("Enter the highest temp for the inputted date: "))
        except ValueError:
            print("Invalid temperature. Entry not saved.")
            continue
        convertedTemperature = convertData(temperature)
        data = f"{inputDate},{temperature},{convertedTemperature}"
        try:
            if insertData("ZooData.csv", data):
                print("The following data was saved at", datetime.now(), ":", data)
        except OSError as error:
            print("Error saving data:", error)

# Create an Excel bar or line chart from the CSV temperature data.
# Arguments: filePath (str) is the CSV path; chartType (str) is "bar" or "line".
# Returns: None; saves final.xlsx when successful.
def createChart(filePath, chartType):
    from openpyxl import Workbook
    from openpyxl.chart import BarChart, LineChart, Reference
    from openpyxl.chart.data_source import AxDataSource, StrRef
    from openpyxl.styles import Font, PatternFill

    print("Choose the temperature data for your chart:")
    print("1 Fahrenheit (original)")
    print("2 Celsius (converted)")
    dataChoice = input("Enter 1 or 2: ").strip()
    if dataChoice not in ("1", "2"):
        print("Invalid data source selection.")
        return

    dataLabel = "Fahrenheit" if dataChoice == "1" else "Celsius"
    columnIndex = 1 if dataChoice == "1" else 2
    try:
        with open(filePath, "r", newline="") as file:
            csvRows = list(csv.reader(file))
    except OSError as error:
        print("Error reading CSV file:", error)
        return

    workbook = Workbook()
    worksheet = workbook.active
    worksheet.title = "Temperature Report"
    worksheet.append(["Date", dataLabel])
    for row in csvRows:
        if len(row) < 3:
            continue
        try:
            temperature = float(row[columnIndex])
        except ValueError:
            print("Skipping invalid temperature row:", row)
            continue
        worksheet.append([row[0], temperature])

    if worksheet.max_row < 2:
        print("No valid temperature data found in", filePath)
        return

    for cell in worksheet[1]:
        cell.font = Font(bold=True, color="FFFFFF")
        cell.fill = PatternFill("solid", fgColor="234B6C")
    worksheet.column_dimensions["A"].width = 20
    worksheet.column_dimensions["B"].width = 20
    for cell in worksheet["B"][1:]:
        cell.number_format = "0.00"

    chart = BarChart() if chartType == "bar" else LineChart()
    chart.title = "nakmce5302 " + datetime.now().strftime("%m/%d/%Y")
    chart.x_axis.title = "Date"
    chart.y_axis.title = "Temperature (°F)" if dataChoice == "1" else "Temperature (°C)"
    chart.add_data(Reference(worksheet, min_col=2, min_row=1, max_row=worksheet.max_row), titles_from_data=True)
    # Use the date strings explicitly as the horizontal-axis categories.
    date_range = f"'Temperature Report'!$A$2:$A${worksheet.max_row}"
    chart.series[0].cat = AxDataSource(strRef=StrRef(f=date_range))
    chart.legend = None  # Dates belong on the x-axis, not in a legend.
    chart.width = 19
    chart.height = 10
    worksheet.add_chart(chart, "D2")
    try:
        workbook.save("final.xlsx")
        print("Success!", chartType.title(), "chart saved in final.xlsx")
    except OSError as error:
        print("Error saving Excel file:", error)


# Ask for a graph type and generate an Excel report from the CSV data.
# Argument: filePath (str) is the CSV path.
# Returns: None; calls createChart for a valid chart selection.
def generateReport(filePath):
    print("Choose a graph type:")
    print("1 Bar chart")
    print("2 Line chart")
    chartChoice = input("Enter 1 or 2: ").strip()
    if chartChoice == "1":
        createChart(filePath, "bar")
    elif chartChoice == "2":
        createChart(filePath, "line")
    else:
        print("Invalid graph type selection.")


# Display the menu and run the selected option.
def main():
    print("NAKMCE5302's Spreadsheet Automation Menu")
    print("Choose a number from the following options")
    print("1 Input Data")
    print("2 View Current Data")
    print("3 Generate Report")
    menuChoice = input()
    print("You selected", menuChoice, "at", datetime.now())
    if menuChoice == "1":
        getInput()
    elif menuChoice == "2":
        viewData("ZooData.csv")
    elif menuChoice == "3":
        generateReport("ZooData.csv")
    else:
        print("Invalid menu option.")

main()

