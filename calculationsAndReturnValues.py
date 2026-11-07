
from datetime import datetime
import csv
import os

# Convert a Fahrenheit temperature to Celsius.
def convertData(data):
    convertedValue = (data - 32) * 5 / 9
    return convertedValue


# Append comma-separated data to the CSV file.
# Handle errors that may occur while writing.
def insertData(filePath, data):
    try:
        with open(filePath, "a", newline="") as file:
            file.write(data + "\n")
        return True
    except OSError as error:
        print("Error writing to file:", error)
        return False


# Display the CSV file path and its contents.
# Open the file with read-only permissions.
def viewData(filePath):
    try:
        print("\nReading file:", os.path.abspath(filePath))
        with open(filePath, "r", newline="") as file:
            reader = csv.reader(file)
            for row in reader:
                print(",".join(row))
    except OSError as error:
        print("Error reading file:", error)


# Ask the user for dates and temperatures.
# Convert the temperatures and save each entry.
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
            temperature = int(input(
                "Enter the highest temp for the inputted date: "
            ))
        except ValueError:
            print("Invalid temperature. Entry not saved.")
            continue

        # Convert Fahrenheit to Celsius.
        convertedTemperature = convertData(temperature)

        # Prepare comma-separated data for the CSV file.
        data = f"{inputDate},{temperature},{convertedTemperature}"

        # Save the data and display the date/time on success.
        try:
            if insertData("ZooData.csv", data):
                print(
                    "The following data was saved at",
                    datetime.now(),
                    ":",
                    data
                )
        except OSError as error:
            print("Error saving data:", error)


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
    else:
        print("Error: The chosen functionality is not implemented yet")


main()

