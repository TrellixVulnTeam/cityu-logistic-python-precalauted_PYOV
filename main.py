

import datetime


from DataInitializer import dataInitializer
import multiprocessing
import argparse



parser = argparse.ArgumentParser()
parser.add_argument("-s","--startTimeWindow", type=str, default="2019-11-25 9:30:00", help="The start time of delivery date")
parser.add_argument("-e","--endTimeWindow", type=str, default="2019-11-25 22:00:00", help="The end time of delivery date")
parser.add_argument("-m","--method", type=int, default=0, help="0 = AStar, 1 = CPD ")
parser.add_argument("-o","--orderIndex", type=int, default=2, help="0 = AStar, 1 = CPD ")
args = parser.parse_args()



def writeDownRoutes(fileName, fitnessResult1):
    nCsv = open('./result/%s.csv' % (fileName), 'w+', encoding='utf-8-sig')
    for vehilce in fitnessResult1.multiDeliveriesList:
        if len(vehilce) > 2:
            for index in range(len(vehilce) - 1):
                startDelivery = vehilce[index]
                endDelivery = vehilce[index + 1]
                nCsv.write("%s=>%s,%s\n" % (
                startDelivery.order.orderId, endDelivery.order.orderId, endDelivery.deliveryTime.strftime("%H:%M:%S")))

if __name__ == '__main__':
    multiprocessing.freeze_support()
    startDate = datetime.datetime.strptime(args.startTimeWindow, '%Y-%m-%d %H:%M:%S')
    endDate = datetime.datetime.strptime(args.endTimeWindow, '%Y-%m-%d %H:%M:%S')
    dataInitializer.setStartDate(startDate)
    dataInitializer.setTimeEndWindows(endDate)
    dataInitializer.normalGenerate(args.orderIndex)

    from services.TravellingService import travellingService
    travellingService.method = args.method


    # from services.NetworkService import networkService
    #
    # networkService.buildDynamicNetorkXNpz(args.orderIndex)
    # resultService.sendResultToDB(fitnessResult)
    from services.NearestNeighborService import nearestNeighborService
    fitnessResult1 = nearestNeighborService.run(args.orderIndex)
    writeDownRoutes("%s_nn_route" %(args.orderIndex),fitnessResult1)

    # print(fitnessResult.multiDeliveriesList)

    for index in range(10):
        from services.GeneticAlgorithmService import geneticAlgorithmService
        fitnessResult,content = geneticAlgorithmService.run(args.orderIndex)
        print('Done GA loop %s' %index)
        nCsv = open('./result/%s_ga.txt'%(args.orderIndex), 'a+', encoding='utf-8-sig')
        nCsv.write("Done Loop: %s\n" % index)
        nCsv.write("%s\n" % content)
        nCsv.write("Total vehicle: %s\n" % fitnessResult.vehicleNum)
        nCsv.write("TotalDuration: %ss\n" % fitnessResult.totalDuration)
        nCsv.write("TotalTravelDuration: %ss\n" % (fitnessResult.totalDurationWithoutNonUseVehicle - fitnessResult.totalServiceTime))

        nCsv.write("%s\n\n" % (
                    fitnessResult.multiDeliveriesList))
        nCsv.close()
        writeDownRoutes("%s_ga_%s_route" % (args.orderIndex,index), fitnessResult)


    from services.DriverRecordService import driverRecordService
    fitnessResult = driverRecordService.checkDriverRecord(args.orderIndex)
    writeDownRoutes("%s_o_route" % (args.orderIndex), fitnessResult)
    #
    # print(fitnessResult3.multiDeliveriesList)
    #
    # resultService.sendResultToDB(fitnessResult)

