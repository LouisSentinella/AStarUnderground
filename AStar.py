import math
import csv
import traceback
import copy
from tkinter import *
##TODO
#*Add cost for changing stations
#*Render Multiple train lines on one stations
#*Add ability to go via another station 


canvas_width = 1950
canvas_height = 900

master = Tk()
master.title("Points")
w = Canvas(master,
           width=canvas_width,
           height=canvas_height)
w.pack(expand=YES, fill=BOTH)
#
class pQueue(object):

    ### CONSTRUCTOR 
    def __init__(self, maxSize):

        #print("A pQueue has been created")

        ### Attributes
        self.__qList = []
        self.__maxSize = maxSize

    def __str__(self):
        report = ""
        #for i in self.__qList:
            #print(i)
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
        self.xCoords = 0
        self.yCoords = 0
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

    def __init__(self, name, length, color):

        self.name = name
        self.stationList = []
        self.color = color
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

    T.delete('1.0', END)

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
    #T.insert(END,"\n")
    for i in range(0, len(currentRoute.path)-1):
        stationOne = currentRoute.path[i].upper()
        stationOne = stationOne.replace(" ", "")
        stationOne = stationOne.replace("'", "")
        stationTwo = currentRoute.path[i+1].upper()
        stationTwo = stationTwo.replace(" ", "")
        stationTwo = stationTwo.replace("'", "")
        # print(startIn)
        # print(endIn)

        for i in stationList:
            if ((((i.name).upper()).replace(" ", "")).replace("'", "")) == stationOne:
                stationOneObj = i
                break
        for i in stationList:
            if ((((i.name).upper()).replace(" ", "")).replace("'", "")) == stationTwo:
                stationTwoObj = i
                break

        w.create_oval(stationOneObj.xCoords, stationOneObj.yCoords, stationOneObj.xCoords + 10, stationOneObj.yCoords + 10, fill="#ffa500")
        w.create_text(stationOneObj.xCoords, stationOneObj.yCoords - 9, fill="#ffa500", font="Times 10 italic bold",
                      text=stationOneObj.name)
        w.create_line(stationOneObj.xCoords + 5, stationOneObj.yCoords + 5, stationTwoObj.xCoords + 5, stationTwoObj.yCoords + 5,fill="#ffa500", width=5)
    w.create_oval(stationTwoObj.xCoords, stationTwoObj.yCoords, stationTwoObj.xCoords + 10, stationTwoObj.yCoords + 10,
                  fill="#ffa500")
    w.create_text(stationTwoObj.xCoords, stationTwoObj.yCoords - 9, fill="#ffa500", font="Times 10 italic bold",
                  text=stationTwoObj.name)




    #print(str(round(currentRoute.fval,2)))
    for i in currentRoute.path:
        T.insert(END,i + "\n")
    T.insert(END,"\nTotal Distance:\n" + str(round(currentRoute.fval,2)) + "km.")
    #print(endLoc.path)
  

lineBakerloo = trainLine("Bakerloo", 12,"#A45A2A" )
lineCentral = trainLine("Central", 12,"#da291c" )
lineCircle = trainLine("Circle", 28,"#F7D117" )
lineDistrict = trainLine("District", 20 , "#007a33")
lineHammersmithAndCity = trainLine("Hammersmith & City", 11,"#eb9ca8" )
lineJubilee = trainLine("Jubilee", 7,"#7c878e" )
lineMetropolitan = trainLine("Metropolitan", 9,"#8a004f")
lineNorthern = trainLine("Northern", 16 , "#000000")
linePiccadilly = trainLine("Piccadilly", 12, "#10069F")
lineVictoria = trainLine("Victoria", 8,"#00a3e0")
lineWaterlooAndCity = trainLine("Waterloo & City", 2,"#6ECEB2")
#print(nodeNottingHillGate)
trainLineList = [lineBakerloo, lineCentral,lineDistrict, lineHammersmithAndCity,lineJubilee, lineMetropolitan, linePiccadilly, lineVictoria, lineWaterlooAndCity,lineCircle, lineNorthern] 
with open("UndergroundStations.csv", 'rt') as text_file:
    reader = csv.reader(text_file)
    aList = list(reader)

#print(aList)
stationList = []
for i in aList:
    try:
        #reading in the file, and dynamically making objects for the stations.
        #print(i[1])
        globals()[i[0]] = Station(i[1], i[2], i[3], i[4], i[5])
        #print(i[5])
        for j in eval(i[5]):
        
            j[0].addStation(eval(i[0]), j[1])
        stationList.append(eval(i[0]))
    except:
        #traceback.print_exc()
        print("There is an error with your data – please correct it.")      

def mainLoopWhile(window):
        window.update_idletasks()
        window.update()
##def main():
##
##    #print(stationList)
##    for i in stationList:
##        print(i.name)
##        
##    print("\n")#taking inputs and checking whether they are actual stations. 
##    startIn = str(input("Where would you like to navigate from?"))
##    endIn = str(input("Where would you like to navigate to?"))
##    endIn = endIn.upper()
##    endIn = endIn.replace(" ", "")
##    endIn = endIn.replace("'", "")
##    startIn = startIn.upper()
##    startIn = startIn.replace(" ", "")
##    startIn = startIn.replace("'", "")
##    #print(startIn)
##    #print(endIn)
##    
##    
##    for i in stationList:
##        if ((((i.name).upper()).replace(" ", "")).replace("'", "")) == startIn:
##            startStation = i
##            break
##    for i in stationList:
##        if ((((i.name).upper()).replace(" ", "")).replace("'", "")) == endIn:
##            endStation=i
##            break
##    if (startIn == "CABBAGE") or (endIn=="CABBAGE"):
##        for i in range(0,1000):
##            globals()["window" + str(i)] = Tk()
##            globals()["canvas" + str(i)] = Canvas(eval("window" + str(i)), width=1000, height=1000)
##            eval("canvas" + str(i)).pack()
##            photo = PhotoImage(file="ING-green-cabbage-2-main.gif")
##            eval("canvas" + str(i)).create_image(0,0,image=photo, anchor=tkinter.NW)
##            eval("window" + str(i)).mainloop()
##            
##    aStarAlgorithm(startStation, endStation)

def main():

    #print(stationList)
    #for i in stationList:
        #print(i.name)
        
    #print("\n")#taking inputs and checking whether they are actual stations. 
    startIn = e1.get()
    endIn = e2.get()
    endIn = endIn.upper()
    endIn = endIn.replace(" ", "")
    endIn = endIn.replace("'", "")
    startIn = startIn.upper()
    startIn = startIn.replace(" ", "")
    startIn = startIn.replace("'", "")
    #print(startIn)
    #print(endIn)
    
    
    for i in stationList:
        if ((((i.name).upper()).replace(" ", "")).replace("'", "")) == startIn:
            startStation = i
            break
    for i in stationList:
        if ((((i.name).upper()).replace(" ", "")).replace("'", "")) == endIn:
            endStation=i
            break
    if (startIn == "CABBAGE") or (endIn=="CABBAGE"):
        for i in range(0,1000):
            globals()["window" + str(i)] = Tk()
            globals()["canvas" + str(i)] = Canvas(eval("window" + str(i)), width=1000, height=1000)
            eval("canvas" + str(i)).pack()
            photo = PhotoImage(file="ING-green-cabbage-2-main.gif")
            eval("canvas" + str(i)).create_image(0,0,image=photo, anchor=NW)
            eval("window" + str(i)).mainloop()
            
    aStarAlgorithm(startStation, endStation)
def startUp():
    try:
        w.delete("all")
        drawCanvas()
        main()
    except:
        T.delete('1.0', END)
        T.insert(END, "Invalid Input, try again!")
        #traceback.print_exc()
        main()
def clearRoute():
    w.delete("all")
    drawCanvas()
    T.delete('1.0', END)
    
for i in stationList:
    coordsY= i.lat
    coordsX = i.long
    coordsY = coordsY - 51
    coordsY = coordsY*13000
    coordsX = 1 + coordsX
    coordsX = coordsX*13000
    coordsX -= 10385
    coordsY -= 6200
    #coordsY = 500-coordsY
    coordsY = 900-coordsY
    i.xCoords = coordsX
    i.yCoords = coordsY
def drawCanvas():
    for i in trainLineList:
        newStationList = i.stationList[:]
        #print(str(len(newStationList) % 2))
        #print(str(len(newStationList)))
        #print(newStationList)
        if (len(newStationList)%2)== 0:
            for j in range(0, int(len(newStationList))-1):
                PointOne = copy.deepcopy(newStationList[0])
                newStationList.pop(0)
                PointTwo = copy.deepcopy(newStationList[0])
                if (PointOne == None) or (PointTwo== None):
                    #print("Yikers")
                    pass
                else:
                    w.create_line(PointOne.xCoords+5, PointOne.yCoords+5, PointTwo.xCoords+5, PointTwo.yCoords+5, fill=i.color, width=5)
        else:
            for j in range(0, int(math.ceil(len(newStationList)))-1):
                PointOne = newStationList.pop(0)
                PointTwo = newStationList[0]
                if (PointOne == None) or (PointTwo== None):
                    #print("Yikers")
                    pass
                else:
                    w.create_line(PointOne.xCoords+5, PointOne.yCoords+5, PointTwo.xCoords+5, PointTwo.yCoords+5, fill=i.color, width=5)
    for i in stationList:
        #print("(" +str(i.xCoords) + ", " + str(i.yCoords) + ")")
        #print("\n")
        w.create_oval(i.xCoords, i.yCoords, i.xCoords  + 10, i.yCoords + 10, fill="#476042")
        w.create_text(i.xCoords,i.yCoords-9,fill="#000000",font="Times 10 italic bold",
                            text=i.name)

drawCanvas()
b1 = Button(master, text="Find Route", command = startUp)
b2 = Button(master, text="Clear Route", command = clearRoute)
e1 = Entry(master)
e2 = Entry(master)
b1.place(x=1750, y=150)
e1.place(x=1750, y=180)
e2.place(x=1750, y=200)
b2.place(x=1750, y=560)
T = Text(master, height = 20, width = 25)
T.place(x=1750, y= 230)

mainloop()



