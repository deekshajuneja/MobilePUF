import os
import binascii
from util import hammingDistance
from os.path import join, dirname, basename

def testHamming(folder):
    byteArrList = []
    fileCount = 0
    for root, dirs, files in os.walk(folder):
        if(len(files) != 0):
            files.sort()
            for fileName in files:
                byteArrList.append(convBinFileToByteArr(join(root, fileName)))
                print "Binary File %i = %s" % (fileCount, join(root, fileName))
                fileCount += 1

    for i in range(0, len(byteArrList)):
        for j in range(i, len(byteArrList)):
            shortLen = len(byteArrList[i]) if len(byteArrList[i]) < len(byteArrList[j]) else len(byteArrList[j])
            avgHamDist = 0
            for k in range(0, shortLen, 16):
                if ((len(byteArrList[i][k:k+16]) == 16) and (len(byteArrList[j][k:k+16]) == 16)):
                    avgHamDist += hammingDistance(byteArrList[i][k:k+16], byteArrList[j][k:k+16])
            avgHamDist /= (shortLen/16)
            print "%i -> %i = %i" % (i, j, avgHamDist)

def convBinFileToByteArr(binFile):
    byteArr = bytearray()
    #print binFile

    with open(binFile, "rb") as f:
        byte = f.read(1)
        while(byte != ""):
            #print binascii.hexlify(byte)
            byteArr.append(byte)
            byte = f.read(1)

    return byteArr
