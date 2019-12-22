import os,sys,inspect
from multiprocessing.pool import ThreadPool

from excpetions.TimeWindowExceeded import TimeWindowExceeded
from services.NearestNeighborService import nearestNeighborService
from services.TravellingService import travellingService

currentdir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
parentdir = os.path.dirname(currentdir)
sys.path.insert(0,parentdir) 

from services.AStarService import aStarService
from services.EnvironmentService import environmentService
from Common import Common
from utils.SingletonMetaclass import SingletonMetaclass
from services.GraphService import graphService
import copy
import random
from modelObjects.FitnessObject import FitnessObject
import multiprocessing

import time
class GeneticAlgorithmService(metaclass=SingletonMetaclass):
    def __init__(self):
        self.thread = Common.thread
        self.len_population = Common.len_population
        self.crossRate = Common.crossRate
        self.mutationRate = Common.mutationRate
        self.initizalCount = 0

        self.max_generations = Common.max_generations
        self.len_max_keep = Common.len_max_keep

    def randomDeliveriesRoute(self, count=None):
        # print("randomDeliveriesRoute")
        driverVehiclesLength = len(environmentService.driverVehicles)
        existDepot = sum(p.orderId == 0 for p in self.sortedOrderList)
        depotLength = driverVehiclesLength - existDepot - 1
        # depotLength = driverVehiclesLength -1
        vaild = False
        cnt = 0
        while(vaild is False):
            # print(vaild)
            tempPath = self.sortedOrderList[:]
            cnt += 1
            if cnt >10000:
                print('err, cannot initialize suitable solutions')
            # print(cnt,flush=True)
            for i in range(depotLength):
                insertIndex = random.randint(0,len(tempPath)-1)
                tempPath.insert(insertIndex, environmentService.depot)
            vaild, mutliDeliveriesList = self.checkValidFromTempPath(tempPath)

            if vaild == True:
                break

        fitnessObject = FitnessObject(tempPath, mutliDeliveriesList)
        self.initizalCount += 1
        print('--Done Initial solution %s/%s' % (self.initizalCount, self.len_population))
        return fitnessObject

    def checkValidFromTempPath(self, tempPath):
        # print("checkValidFromTempPath")
        mutliDeliveriesList = environmentService.orderListToMutliDeliveriesList(tempPath)
        vaild = environmentService.isOrderStructureValid(mutliDeliveriesList)

        if vaild == False:
            return False, None

        newMutliDeliveriesList = []
        try:
            pool = random.sample(mutliDeliveriesList, len(mutliDeliveriesList))
            for singleDelivery in pool:
                newMutliDeliveriesList.append(travellingService.calucateTravelNodeFromDeliveryList(singleDelivery,singleDelivery[0].order.deliveryTimeStart,singleDelivery[-1].order.deliveryTimeEnd))
        except TimeWindowExceeded:
            return False,None

        vaild = environmentService.isTimeWindowsVaild(newMutliDeliveriesList)
        if vaild == False:
            return False,None
        return True, newMutliDeliveriesList


    def initialPopulation(self,popSize):
        print("Staring initial Population")
        startTime = time.time()
        self.nearestSolution = nearestNeighborService.nearestDriverVehilceList
        self.sortedOrderList = environmentService.mutliDeliveriesListToOrderList(
            nearestNeighborService.nearestDriverVehilceList)


        with ThreadPool(processes=Common.thread) as p:
            populations = p.map(self.randomDeliveriesRoute, range(popSize))


        crt_time = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
        print("\nEnd Initial solution: \ttime: %s\t%ds " % (crt_time, (time.time() - startTime)))


        return populations
    
    def calucateFitnessValue(self, fitnessObject):

        fitnessObject.routeFitness()
        return fitnessObject

    def rankRoutes(self,populations):
        
        fitnessResults =[]

        for population in populations:
            fitnessResults.append(self.calucateFitnessValue(population))

        fitnessResults.sort(key=lambda x: x.fitnessValue, reverse=True)

        return fitnessResults

    

    def run(self, num):
        tmpSolution = self.initialPopulation(self.len_population)
        start_time = time.time()
        len_tmp_keep = 0
        print("Starting Running GA")
        content = ""

        for i in range(0, self.max_generations):
            tmpSolution = self.nextGeneration(tmpSolution)
            if i == 0:
                bestResult = tmpSolution[0]
                crt_time = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
                text = "\ngeneration: %d\tResult: %ds \ttime: %s\t%ds " % (i, bestResult.totalDuration,crt_time, (time.time() - start_time))
                content+=text
                print(text)
                tmpBestResult = bestResult
            else:
                currentBestResult = tmpSolution[0]
                if currentBestResult.totalDuration < tmpBestResult.totalDuration:
                    tmpBestResult = currentBestResult
                    crt_time = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()) 
                    text = "\ngeneration: %d\tResult: %ds \ttime: %s\t%ds " % (i, tmpBestResult.totalDuration,crt_time, (time.time() - start_time))
                    print(text)
                    content += text
                    len_tmp_keep = 0
                    # print(text)

                else:
                    len_tmp_keep +=1

            if len_tmp_keep == self.len_max_keep:
                text = "\n\nThere are %s consective generations without changes.\n" % len_tmp_keep
                print(text)
                content+=text

                # print('Stop at generation ', i, '\t Result: %ds \n'%(tmpBestResult.totalDuration))
                text = 'Stop at generation %s \t Result: %ds \n'%(i,tmpBestResult.totalDuration)

                print(text)
                content += text

                crt_time = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
                # print("Time: %s\t%ds " % (crt_time, (time.time() - start_time)))

                text = "Time: %s\t%ds " % (crt_time, (time.time() - start_time))
                print(text)
                content += text

                # nCsv = open('./result/%s_ga.txt'%(num), 'a+', encoding='utf-8-sig')
                # nCsv.write(content)
                # nCsv.write("Total vehicle: %s\n" % tmpBestResult.vehicleNum)
                # nCsv.write("TotalDuration: %ss\n" % tmpBestResult.totalDuration)
                # nCsv.write("TotalTravelDuration: %ss\n" % (tmpBestResult.totalDurationWithoutNonUseVehicle - tmpBestResult.totalServiceTime))
                # nCsv.close()
                return tmpBestResult,content

            # nCsv = open('./result/%s_ga.txt'%(num), 'a+', encoding='utf-8-sig')
            # nCsv.write(content)
            # nCsv.write("Total vehicle: %s\n" % tmpBestResult.vehicleNum)
            # nCsv.write("TotalDuration: %ss\n" % tmpBestResult.totalDuration)
            # nCsv.write("TotalTravelDuration: %ss\n" % (tmpBestResult.totalDurationWithoutNonUseVehicle - tmpBestResult.totalServiceTime))
            # nCsv.close()
        return tmpBestResult,content
                
    def nextGeneration(self, currentGen):
        fitnessResults = self.rankRoutes(currentGen)
        len_population = len(currentGen)

        children_size = int(len_population * self.crossRate)  ##  len_pop 100, chidren_size 80
        eliteSize = len_population - children_size ## eliteSize = 20
        
        topPool = []
        topPool.append(fitnessResults[0])
        eliteParentPool = self.selection(fitnessResults, eliteSize - 1)

        nomralParentPool = self.selection(fitnessResults, children_size)

        childrenSelections = self.breedPopulation(nomralParentPool)




        childrenMutations= self.mutatePopulation(childrenSelections)



        if len(childrenMutations):
            nextGeneration = topPool + eliteParentPool + childrenMutations
        else:
            nextGeneration = topPool + eliteParentPool

        return nextGeneration


    def selection(self,fitnessResults, children_size):

        selectionResults = []
        fitness_sum = sum(fitness.fitnessValue for fitness in fitnessResults)

        for i in range(children_size):
            pick = random.uniform(0, 1) * fitness_sum
            for j in range(0, len(fitnessResults)): # usually, 
                pick -= fitnessResults[j].fitnessValue
                if pick < 0:
                    selectionResults.append(fitnessResults[j])
                    break

        return selectionResults # return the ids of selections

    def matingPool(self,population, selectionResults):
        matingpool = []
        for index in selectionResults:
            matingpool.append(population[index])
        return matingpool

    def breedPopulation(self, matingpool):

        childrens = []

        length = len(matingpool)

        pool = random.sample(matingpool, len(matingpool))
        poolForMulti = []
        for i in range(0, length-1):
            firstFitnessObject = pool[i]
            secondstFitnessObject = pool[i+1]
            poolForMulti.append([firstFitnessObject,secondstFitnessObject])
        firstFitnessObject = pool[0]
        secondstFitnessObject = pool[-1]
        poolForMulti.append([firstFitnessObject, secondstFitnessObject])

        with ThreadPool(processes=Common.thread) as p:
            breedResults = p.map(self.breed, poolForMulti)

        for breedResult in breedResults:
            if breedResult != 'err':
                children = breedResult
                childrens.append(children)
        #
        #
        #     res_corssover = self.breed(firstFitnessObject, secondstFitnessObject)
        #     if res_corssover != 'err':
        #         children = res_corssover
        #         childrens.append(children)
        # firstFitnessObject = pool[0]
        # secondstFitnessObject = pool[-1]
        # res_corssover = self.breed(firstFitnessObject, secondstFitnessObject)
        # if res_corssover != 'err':
        #     children = res_corssover
        #     childrens.append(children)
        return childrens


    def mutate(self,individual, mutationRate):

        for swapped in range(len(individual)):
            if(random.random() < mutationRate):
                tempArray =[]
                while(True):
                    # print("Doing mutate")
                    swapWith = int(random.random() * len(individual))
                    record = str(swapWith)
                    if len(tempArray) ==  (len(individual)-1):
                        break
                    if record in tempArray:
                        continue
                    tempArray.append(record)
                    city1 = individual[swapped]
                    city2 = individual[swapWith]
                    temp = individual
                    temp[swapped] = city2
                    temp[swapWith] = city1
                    if self.checkValid(temp) is True:
                        individual[swapped] = city2
                        individual[swapWith] = city1
                        break
        return individual

    def mutatePopulation(self, fitnessObjectsPool):
        mutatedPop = []
        with ThreadPool(processes=Common.thread) as p:
            mutatedResults = p.map(self.mutation, fitnessObjectsPool)

        for mutatedResult in mutatedResults:
            if mutatedResult != 'mutation_err':
                mutatedPop.append(mutatedResult)
        #
        # for ind in range(0, len(fitnessObjectsPool)):
        #         mutatedInd = self.mutation(fitnessObjectsPool[ind], mutationRate)
        #         if mutatedInd != 'mutation_err':
        #             mutatedPop.append(mutatedInd)
        return mutatedPop
    



    def breed(self, fitnessObjectArray,):
        fitnessObject1, fitnessObject2 = fitnessObjectArray[0], fitnessObjectArray[1]
        parent1 =fitnessObject1.fullPath
        parent2 = fitnessObject2.fullPath

        cnt = 0
        while(True):
            cnt +=1


            geneA = int(random.random() * len(parent1)) #ramdon length
            geneB = int(random.random() * len(parent1)) #ramdon length

            startGene = min(geneA, geneB)
            endGene = max(geneA, geneB)

            childP1 = parent1[startGene:endGene]

            childP2 = [item for item in parent2 if item not in childP1]
            child = childP1 + childP2
            tempPath = child
            vaild, mutliDeliveriesList = self.checkValidFromTempPath(tempPath)
            if vaild == True:
                return FitnessObject(tempPath,mutliDeliveriesList)

            if cnt > 10000:
                return 'err'


    # def crossover(self, parent1, parent2):

        # def process_gen_repeated(copy_child1,copy_child2):

        #     count1=0
        #     for gen1 in copy_child1[:pos]:
        #         repeat = 0
        #         repeat = copy_child1.count(gen1)
        #         if repeat > 1:#If need to fix repeated gen
        #             count2=0
        #             for gen2 in parent1[pos:]:#Choose next available gen
        #                 if gen2 not in copy_child1:
        #                     child1[count1] = parent1[pos:][count2]
        #                 count2+=1
        #         count1+=1

        #     count1=0
        #     for gen1 in copy_child2[:pos]:
        #         repeat = 0
        #         repeat = copy_child2.count(gen1)
        #         if repeat > 1:#If need to fix repeated gen
        #             count2=0
        #             for gen2 in parent2[pos:]:#Choose next available gen
        #                 if gen2 not in copy_child2:
        #                     child2[count1] = parent2[pos:][count2]
        #                 count2+=1
        #         count1+=1

        #     return [child1,child2]

        # cnt = 0
        # while(True):
        #     cnt += 1

        #     pos=random.randrange(1, self.len_each_solution-1)
        #     child1 = parent1[:pos] + parent2[pos:] 
        #     child2 = parent2[:pos] + parent1[pos:] 
        #     [child1,child2] = process_gen_repeated(child1, child2)
        #     if self.checkValid(child1) and  self.checkValid(child2):
        #         return  [child1,child2]

        #     if cnt > 10000:
        #         return 'err'



    def mutation(self, fitnessObject):
        prob = self.mutationRate

        def inversion_mutation(target):
   
            index1 = random.randrange(0,len(target))
            index2 = random.randrange(index1,len(target))                
            

            chromosome_mid = target[index1:index2]
            chromosome_mid.reverse()                
            
            chromosome_result = target[0:index1] + chromosome_mid + target[index2:]                
            return chromosome_result


        chromosome  = fitnessObject.fullPath 
        aux = []
        cnt = 0
        while(True):

            cnt += 1
            for _ in range(len(chromosome)):
                if random.random() < prob :
                    aux = inversion_mutation(chromosome)
            if len(aux) ==0:
                tempPath = fitnessObject.fullPath
            else:
                tempPath = aux
            vaild, mutliDeliveriesList = self.checkValidFromTempPath(tempPath)
            if vaild == True:
                return FitnessObject(tempPath,mutliDeliveriesList)
            if cnt > 10000:
                return 'mutation_err'

geneticAlgorithmService = GeneticAlgorithmService()
