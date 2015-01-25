import os
import numpy
from os.path import join, dirname, basename

from util import simpleMovingAverage, cumulativeMovingAverage, distBetweenPts, calcNextPt

def findStartEnd(pcmFile, amp_limit):
    #Opens the file into an array
    data = numpy.memmap(pcmFile, dtype='int16')
    startPos = -1
    endPos = len(data)
    
    for i in range(1000, len(data) - 10):
        if abs(data[i]) > amp_limit:
            #Once an appropriate peak is found
            #Checks how many of the 20 surrounding points are also high
            pointsPassed = 0
            for j in range(i-10, i+10):
                if abs(data[j]) > amp_limit:
                    pointsPassed += 1
            if pointsPassed > 12:
                startPos = i
                break

    for i in range(len(data) - 10, 1000, -1):
        if abs(data[i]) > amp_limit:
            #Once an appropriate peak is found
            #Checks how many of the 20 surrounding points are also high
            pointsPassed = 0
            for j in range(i-10, i+10):
                if abs(data[j]) > amp_limit:
                    pointsPassed += 1
            if pointsPassed > 12:
                endPos = i
                break
    return (startPos, endPos)

def arbiter(val1, val2):
    return 0 if val1 > val2 else 1 #ternary operation

#Creates the bitstring based on the global average of the raw data samples
def Strat1(path, start, end, destPath, fileName):
    data = numpy.memmap(path, dtype='int16')
    globalAverage = 0
    for i in range(start, end):
        globalAverage = globalAverage + data[i]
    globalAverage = float(globalAverage) / len(data)

    #Build the bitstring as per Ryan's approach
    bitString = ""
    for i in range(start, end):
        bitString += str(arbiter(data[i], globalAverage))
    byteArr = convBitStrToByteArr(bitString)

    #Writes it to a file in the correct strat folder
    destPath = join(destPath, "Strat1", fileName[0:len(fileName)-4])
    if not os.path.exists(os.path.dirname(destPath)):
        os.makedirs(os.path.dirname(destPath))
    with open(destPath, "wb") as outputFile:
        outputFile.write(byteArr)

#Creates the bitstring based on the global average of the magnitude data samples
def Strat1Abs(path, start, end, destPath, fileName):
    data = numpy.memmap(path, dtype='int16')
    globalAverage = 0
    for i in range(start, end):
        globalAverage = globalAverage + abs(data[i])
    globalAverage = float(globalAverage) / len(data)

    #Build the bitstring as per Ryan's approach
    bitString = ""
    for i in range(start, end):
        bitString += str(arbiter(abs(data[i]), globalAverage))
    byteArr = convBitStrToByteArr(bitString)

    #Writes it to a file in the correct strat folder
    destPath = join(destPath, "Strat1Abs", fileName[0:len(fileName)-4])
    if not os.path.exists(os.path.dirname(destPath)):
        os.makedirs(os.path.dirname(destPath))
    with open(destPath, "wb") as outputFile:
        outputFile.write(byteArr)

#Uses a moving average of 5 based on the raw data
def Strat2(path, start, end, destPath, fileName):
    data = numpy.memmap(path, dtype='int16')
    
    movingAvg5 = simpleMovingAverage(data, 5)

    #Build the bitstring as per Ryan's approach
    bitString = ""
    for i in range(start, end):
        bitString += str(arbiter(data[i], movingAvg5[i]))
    byteArr = convBitStrToByteArr(bitString)

    #Writes it to a file in the correct strat folder
    destPath = join(destPath, "Strat2", fileName[0:len(fileName)-4])
    if not os.path.exists(os.path.dirname(destPath)):
        os.makedirs(os.path.dirname(destPath))
    with open(destPath, "wb") as outputFile:
        outputFile.write(byteArr)

#Uses a moving average of 5 based on the magnitude data
def Strat2Abs(path, start, end, destPath, fileName):
    data = numpy.memmap(path, dtype='int16')

    absData = []
    for i in range(0, len(data)):
        absData.append(abs(data[i]))
    movingAvg5 = simpleMovingAverage(absData, 5)

    #Build the bitstring as per Ryan's approach
    bitString = ""
    for i in range(start, end):
        bitString += str(arbiter(abs(data[i]), movingAvg5[i]))
    byteArr = convBitStrToByteArr(bitString)

    #Writes it to a file in the correct strat folder
    destPath = join(destPath, "Strat2Abs", fileName[0:len(fileName)-4])
    if not os.path.exists(os.path.dirname(destPath)):
        os.makedirs(os.path.dirname(destPath))
    with open(destPath, "wb") as outputFile:
        outputFile.write(byteArr)

#Uses a moving average of 10 based on the raw data
def Strat3(path, start, end, destPath, fileName):
    data = numpy.memmap(path, dtype='int16')
    
    movingAvg10 = simpleMovingAverage(data, 10)

    #Build the bitstring as per Ryan's approach
    bitString = ""
    for i in range(start, end):
        bitString += str(arbiter(data[i], movingAvg10[i]))
    byteArr = convBitStrToByteArr(bitString)

    #Writes it to a file in the correct strat folder
    destPath = join(destPath, "Strat3", fileName[0:len(fileName)-4])
    if not os.path.exists(os.path.dirname(destPath)):
        os.makedirs(os.path.dirname(destPath))
    with open(destPath, "wb") as outputFile:
        outputFile.write(byteArr)

#Uses a moving average of 10 based on the magnitude data
def Strat3Abs(path, start, end, destPath, fileName):
    data = numpy.memmap(path, dtype='int16')

    absData = []
    for i in range(0, len(data)):
        absData.append(abs(data[i]))
    movingAvg10 = simpleMovingAverage(absData, 10)

    #Build the bitstring as per Ryan's approach
    bitString = ""
    for i in range(start, end):
        bitString += str(arbiter(abs(data[i]), movingAvg10[i]))
    byteArr = convBitStrToByteArr(bitString)

    #Writes it to a file in the correct strat folder
    destPath = join(destPath, "Strat3Abs", fileName[0:len(fileName)-4])
    if not os.path.exists(os.path.dirname(destPath)):
        os.makedirs(os.path.dirname(destPath))
    with open(destPath, "wb") as outputFile:
        outputFile.write(byteArr)
        
#Uses a cumulative moving average based on the raw data
def Strat4(path, start, end, destPath, fileName):
    data = numpy.memmap(path, dtype='int16')
    
    cumulativeMovAvg = []
    prevSum = 0
    count = 0

    for i in range(0, len(data)):
        prevSum += data[i]
        count += 1
        cumulativeMovAvg.append(prevSum/count)

    #Build the bitstring as per Ryan's approach
    bitString = ""
    for i in range(start, end):
        bitString += str(arbiter(data[i], cumulativeMovAvg[i]))
    byteArr = convBitStrToByteArr(bitString)

    #Writes it to a file in the correct strat folder
    destPath = join(destPath, "Strat4", fileName[0:len(fileName)-4])
    if not os.path.exists(os.path.dirname(destPath)):
        os.makedirs(os.path.dirname(destPath))
    with open(destPath, "wb") as outputFile:
        outputFile.write(byteArr)

#Uses a cumulative moving average based on the magnitude data
def Strat4Abs(path, start, end, destPath, fileName):
    data = numpy.memmap(path, dtype='int16')
    
    cumulativeMovAvg = []
    prevSum = 0
    count = 0

    for i in range(0, len(data)):
        prevSum += abs(data[i])
        count += 1
        cumulativeMovAvg.append(prevSum/count)

    #Build the bitstring as per Ryan's approach
    bitString = ""
    for i in range(start, end):
        bitString += str(arbiter(abs(data[i]), cumulativeMovAvg[i]))
    byteArr = convBitStrToByteArr(bitString)

    #Writes it to a file in the correct strat folder
    destPath = join(destPath, "Strat4Abs", fileName[0:len(fileName)-4])
    if not os.path.exists(os.path.dirname(destPath)):
        os.makedirs(os.path.dirname(destPath))
    with open(destPath, "wb") as outputFile:
        outputFile.write(byteArr)

def TestSuite(folder = "C:\\Users\\eliil_000\\Downloads\\SoundFiles", destPath = "C:\\Users\\eliil_000\\Downloads\\Results"):
    #Attempts to read each file in the given folder as raw PCM data and create all bitstreams
    for root, dirs, files in os.walk(folder):
        if(len(files) != 0):
           files.sort()
           for fileName in files:
               path = join(root, fileName)
               startEnd = findStartEnd(join(root, fileName), 2000)
               if (startEnd[0] != -1):
                   Strat1(path, startEnd[0], startEnd[1], destPath, fileName)
                   Strat1Abs(path, startEnd[0], startEnd[1], destPath, fileName)
                   Strat2(path, startEnd[0], startEnd[1], destPath, fileName)
                   Strat2Abs(path, startEnd[0], startEnd[1], destPath, fileName)
                   Strat3(path, startEnd[0], startEnd[1], destPath, fileName)
                   Strat3Abs(path, startEnd[0], startEnd[1], destPath, fileName)
                   Strat4(path, startEnd[0], startEnd[1], destPath, fileName)
                   Strat4Abs(path, startEnd[0], startEnd[1], destPath, fileName)

def convBitStrToByteArr(bitString):

    byteToBuild = 0

    #Chop up the bitstring into a list of 8-length strings
    byteList = [bitString[i:i+8] for i in range(0, len(bitString), 8)]

    byteArr = bytearray()
    for byteStr in byteList:
        for i in range(0,8):
            if i < len(byteStr):
                byteToBuild = byteToBuild | (int(byteStr[i]) << (7-i))
        byteArr.append(byteToBuild)
        byteToBuild = 0

    return byteArr

