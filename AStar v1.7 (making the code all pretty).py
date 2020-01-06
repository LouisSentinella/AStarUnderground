import math
import csv
import traceback
import copy

class pQueue(object):

    ### CONSTRUCTOR 
    def __init__(self, maxSize):

        #print("A pQueue has been created")

        ### Attributes
        self.__qList = []
        self.__maxSize = maxSize

    def __str__(self):
        report = ""
        for i in self.__qList:
            print(i)
        report += "\n"
        return report

    def __isFull(self):
        if len(self.__qList) >= self.__maxSize:
            return True
        else:
            return False
    
    def isEmpty(self):
        if len(self.__qList) == 0:
            return True
        else:
            return False
    def addItem(self, item):
        if self.__isFull():
            print("Sorry, the priority queue is already full.")
        else:
            if len(self.__qList) == 0 or item.val > self.__qList[len(self.__qList)-1].val: #This my method of sorting the pQueue
                self.__qList.append(item)    #Instead of sorting it after I add an item, I do an insertion sort with each item i add
            else:
                for i in range(0, len(self.__qList)):
                    if item.val <= self.__qList[i].val:
                        self.__qList.insert(i, item)
                        break
                    
                    
            ##self.__qList.append(item)        
            ##self.__qList = sorted(self.__qList, key=lambda x: x[1])

    def getItem(self, value):
        return self.__qList[value]

    def getQueueObject(self):
        return self.__qList.pop(0)

    def getLength(self):
        return len(self.__qList)
    def getList(self):
        return self.__qList
class Route(object):
    

    def __init__(self, fval, val, path, currentStation):
         
        self.fval = fval #Known distance
        self.val = val #Known distance plus heuristic
        self.currentStation = currentStation
        self.path = path
        
    def __str__(self):
        report = ""
        report += "Distance So Far:\n"
        report += str(self.val) 
        report += "\nRoute so far:\n"
        for i in self.path:
            report += i + "\n"
        return report
    
    def getItem(self):
        return(self.path[len(self.path)-1]) #returns the last item in the route

    def getSecondToLast(self):
        if len(self.path)>=2: #returns second to last item in the route
            return self.path[-2]
                
class Station(object):

    def __init__(self, name, val, lat, long, trainLines):

        self.name = name
        self.val = val
        self.lat = float(lat)
        self.long = float(long)  
        self.trainLines = []
        for i in eval(trainLines):
            #print(i)
            #print(i[0])
            self.trainLines.append(i[0]) 
        self.childAmount = 0
        self.intersection = False

        self.path = []
        self.fval = 0

    def __str__(self):

        report = "\n"

        report = report + self.name + ":"
        report += "\nChildren:"
        for i in self.childList:
            report += ("\n" + i.name )
        report = report + "\nNumber of children for " + self.name + ":" + str(self.childAmount)
        return report

    def connected(self):
        connectedList=[]
                        #this method returns all the stations adjacent to the current one. 
        for i in self.trainLines:

            for j in range(0, len(i.stationList)):

                if i.stationList[j] == self: #Finding the station inside the trainlines
                    if j != 0:
                        if i.stationList[j-1] != None: #adding adjacent stations in a list
                            connectedList.append(i.stationList[j-1])
                        if i.stationList[len(i.stationList)-1] == self:
                            break
                        else:
                            if i.stationList[j+1] != None:
                                connectedList.append(i.stationList[j+1])
                    else:
                        if i.stationList[j+1] != None:
                                connectedList.append(i.stationList[j+1])
        return connectedList #returning ye olde list

    def addToPath(self, i):
        
        self.path.append(i)
        

    def addChild(self, node):
        self.childList.append(node)

class trainLine(object):

    def __init__(self, name, length):

        self.name = name
        self.stationList = []
        for i in range(0,length):
            self.stationList.append(None)
        
    def __str__(self):
        report = ""
        report += self.name + ": \n"
        for i in self.stationList:
            if i == None:
                report +="None \n"
            else:
                report +=i.name + " \n"
        return report
    def addStation(self, station, val):
        self.stationList[val] = station
        
def haversineFunction(stationOne, stationTwo):
    lat1 = math.radians(stationOne.lat)
    long1 = math.radians(stationOne.long)
    lat2 = math.radians(stationTwo.lat)
    long2 = math.radians(stationTwo.long)
    R = 6371#this is all the math for calculating the distance between stations
    dlat = lat2 -lat1
    dlong = long2- long1
    a = (math.sin(dlat/2)**2) + (math.cos(lat1) * math.cos(lat2) * (math.sin(dlong/2)**2))
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1-a))

    d = R * c

    return d
def lineTravelled(nodeOne, nodeTwo):
    if nodeOne == None:
        return(nodeTwo.trainLines)
    else:
        #print("NodeOne",nodeOne)
        #print("nodeTwo",nodeTwo)
        a = nodeOne.trainLines
        b = nodeTwo.trainLines
        return(set(a).intersection(b))
    
def aStarAlgorithm(startLoc, endLoc):

    

    routeQueue = pQueue(1000)

    currentRoute = Route(0,0, [startLoc.name], startLoc)
    routeQueue.addItem(currentRoute)
    closedList = []
    counter = 0
    while currentRoute.currentStation != endLoc or routeQueue.isEmpty():
        
        currentRoute = routeQueue.getQueueObject()
        closedList.append(currentRoute.currentStation.name)
        #print("Expanding", currentRoute.currentStation)

        connectedList = []
        
        connectedList = currentRoute.currentStation.connected()
        for i in connectedList:

            #print(i.path)
            #print(i.name)
            #print(closedList)
            if i.name not in closedList:
                globals()["Route" + str(counter)] = copy.deepcopy(currentRoute)
                editRoute = eval("Route" + str(counter))

                editRoute.path.append(i.name)

                #This calculated the distances between the stations
                #to figure out the value for the pQueue                
                fval = haversineFunction(currentRoute.currentStation, i)
                gval = haversineFunction(i, endLoc)              
    
                editRoute.fval += fval#this changes the new route to add the new distance
                editRoute.val = editRoute.fval + gval

                editRoute.currentStation = i
                routeQueue.addItem(editRoute)
                counter += 1#increasing counter used to make route objects
        currentRoute = routeQueue.getItem(0)


        #print(routeQueue)
        #input("")
    print("\n")    
    for i in currentRoute.path:

        print(i)
    print("\nTotal Distance:", str(round(currentRoute.fval,2)), "km.")
    #print(endLoc.path)
  

lineBakerloo = trainLine("Bakerloo", 12)
lineCentral = trainLine("Central", 12)
lineCircle = trainLine("Circle", 26)
lineDistrict = trainLine("District", 20)
lineHammersmithAndCity = trainLine("Hammersmith & City", 11)
lineJubilee = trainLine("Jubilee", 7)
lineMetropolitan = trainLine("Metropolitan", 9)
lineNorthern = trainLine("Northern", 16)
linePiccadilly = trainLine("Piccadilly", 12)
lineVictoria = trainLine("Victoria", 8)
lineWaterlooAndCity = trainLine("Waterloo & City", 2)
#print(nodeNottingHillGate)

with open("UndergroundStations.csv", 'rt') as text_file:
    reader = csv.reader(text_file)
    aList = list(reader)

#print(aList)
stationList = []
for i in aList:
    try:
        #reading in the file, and dynamically making objects for the stations. 
        globals()[i[0]] = Station(i[1], i[2], i[3], i[4], i[5])
        #print(i[5])
        for j in eval(i[5]):
        
            j[0].addStation(eval(i[0]), j[1])
        stationList.append(eval(i[0]))
    except:
        traceback.print_exc()
        print("There is an error with your data – please correct it.")      


def main():

    #print(stationList)
    for i in stationList:
        print(i.name)
        
    print("\n")#taking inputs and checking whether they are actual stations. 
    startIn = str(input("Where would you like to navigate from?"))
    endIn = str(input("Where would you like to navigate to?"))
    endIn = ((endIn.upper).replace(" ", "")).replace("'", "")
    startIn = ((startIn.upper).replace(" ", "")).replace("'", "")
    print(endIn)
    print(startIn)
    input()
    for i in stationList:
        if ((((i.name).upper).replace(" ", "")).replace("'", "")) == startIn:
            startStation = i
            break
    for i in stationList:
        if ((((i.name).upper).replace(" ", "")).replace("'", "")) == endIn:
            endStation=i
            break
    aStarAlgorithm(startStation, endStation)
    
try:
    main()
except:
    print("Invalid Input, try again!")
    traceback.print_exc()
    main()

