from datetime import datetime

def convertData(data):
    convertedValue = (data - 32) * 5 / 9
    return convertedValue


def getInput():
    numberOfEntries = int(input("How many entries are you inputting? "))

    for entry in range(numberOfEntries):
        inputDate = input("Enter a date: ")
        temperature = int(input("Enter the highest temp for the inputted date: "))

        # Calls convertData with the Fahrenheit temperature and returns the Celsius value.
        convertedTemperature = convertData(temperature)

        print("The following was saved at", datetime.now(), ":")
        print(inputDate, temperature, convertedTemperature, sep=",")


print("NAKMCE5302's Spreadsheet Automation Menu")
print("Choose a number from the following options")
print("1 Input Data")
print("2 View Current Data")
print("3 Generate Report")

menuChoice = input()

print("You selected", menuChoice, "at", datetime.now())

if menuChoice == "1":
    getInput()
else:
    print("Error: The chosen functionality is not implemented yet")
