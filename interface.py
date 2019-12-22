import datetime

from flask import Flask

from flask import request
from DataInitializer import dataInitializer
from services.ResultService import resultService
from services.TravellingService import travellingService

app = Flask(__name__)
app.config["CACHE_TYPE"] = "null"
@app.route('/generate', methods=['GET', 'POST'])
def generatePath():
    content = request.values
    # return content
    startTimeWindow = content['startTimeWindow']
    endTimeWindow = content['endTimeWindow']
    startDate = datetime.datetime.strptime(startTimeWindow, '%Y-%m-%d %H:%M:%S')
    endDate = datetime.datetime.strptime(endTimeWindow, '%Y-%m-%d %H:%M:%S')
    dataInitializer.setStartDate(startDate)
    dataInitializer.setTimeEndWindows(endDate)
    travellingService.method = 0
    dynamicPickup = int(content['dynamicPickup'])
    if dynamicPickup == 1:
        dataInitializer.dynamicPickupGenerate()
        from services.DynamicPickupService import dynamicPickUpService
        fitnessResult = dynamicPickUpService.run()
        print(fitnessResult.dynamicDriverList)
        resultService.sendDynamicResultToDB(fitnessResult)
    else:
        dataInitializer.normalGenerate()
        from services.GeneticAlgorithmService import geneticAlgorithmService
        fitnessResult = geneticAlgorithmService.run()
        resultService.sendResultToDB(fitnessResult)

    return "DONE"

if __name__ == "__main__":
    app.run()
