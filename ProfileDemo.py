import math, random
import numpy
import os
import SoundUtil
from os.path import join, dirname, basename
import io
#from pylab import *
import cPickle as pickle

# What % longer or shorter a sample can be before being summarily rejected.
TIME_THRESHOLD = 0.15
# How many standard deviations away a point can be without failing
DEVS = 1
# What % of points need to pass for verification
PASS_LIMIT = 0.8

class profilePoint:
    def __init__(self, mu = 0, sigma = 0, samples = 0):
        self.avg = mu
        self.stddev = sigma
        self.n = samples

    def addSample(self, newSample):
        self.avg = ((self.avg * self.n) / (self.n+1.0)) + (newSample/(self.n+1.0))
        self.stddev = math.sqrt((((self.stddev * self.stddev) * (self.n)) + ((self.avg - newSample) * (self.avg - newSample)))/(self.n+1))
        self.n = self.n + 1

    def fits(self, newSample):
        if (newSample < (self.avg + (self.stddev * DEVS))):
            if (newSample > (self.avg - (self.stddev * DEVS))):
                return True
        return False

#Expands/Contracts lists of data samples to all be of length N, for profiling
def preBuildProfile(dataSets):
    avg = 0
    #Per Jacob's algorithm, finds the average sample length
    #If a given sample is too long, randomly combine two adjacent samples
    #into a single point of their mean value, repeat until length

    #If a given sample is too short, randomly insert a point between two
    #adjacent samples using the mean value of those samples, repeat
    for dataSet in dataSets:
        avg += len(dataSet)
    avg = avg/len(dataSets)
    for i in range(len(dataSets)):
        if len(dataSets[i]) > avg:
            dataSets[i] = contract(dataSets[i], avg)
        elif len(dataSets[i]) < avg:
            dataSets[i] = expand(dataSets[i], avg)
    return buildProfile(dataSets)

#Contracts the given dataSet to length N
def contract(dataSet, N):
    while len(dataSet) > N:
        index = random.randint(0,len(dataSet)-2)
        dataSet[index] = dataSet[index]/2 + dataSet[index+1]/2
        dataSet = numpy.delete(dataSet, index+1)
    return dataSet

#Expands the given dataSet to length N
def expand(dataSet, N):
    while len(dataSet) < N:
        index = random.randint(0,len(dataSet)-2)
        newPoint = dataSet[index]/2 + dataSet[index+1]/2
        dataSet = numpy.insert(dataSet, index+1, newPoint)
    return dataSet

#Takes a list of lists of data samples, all of length N
def buildProfile(dataSets):
    #indices 0, 1, and 2 hold mu, sigma, and N respectively
    #N is the number of samples used to build the average and stdDev
    #This allows the potential for later addition of samples to the set
    profile = [profilePoint() for i in range(len(dataSets[0]))]
    for dataSet in dataSets:
        for i in range(len(dataSet)):
            profile[i].addSample(dataSet[i])
    return profile

#Takes a sample and sizes it to the same length as profile, for verification
def preVerifyUser(profile, sample):
    if (len(profile) * (1 + TIME_THRESHOLD)) < len(sample):
        return false
    if (len(profile) * (1 - TIME_THRESHOLD)) > len(sample):
        return false
    if len(sample) > len(profile):
        sample = contract(sample, len(profile))
    elif len(sample) < len(profile):
        sample = expand(sample, len(profile))
    return verifyUser(profile, sample)

#Takes a profile and a new set of adjusted length and determines if it passes
#Could also add the sample to the profile if it passes, to allow learning
def verifyUser(profile, sample):
    passedPoints = 0
    for i in range(len(profile)):
        if (profile[i].fits(sample[i])):
            passedPoints += 1
    if passedPoints > (len(sample) * PASS_LIMIT):
        return True
    return False

#Reads in all PCM files in the given directory and attempts to build a profile out of them
def pcmProfile(path):
    for root, dirs, files in os.walk(path):
        if(len(files) != 0):
            files.sort()
            dataSets = []
            for fileName in files:
                filePath = join(root, fileName)
                startEnd = SoundUtil.findStartEnd(join(root, fileName), 2000)
                if (startEnd[0] != -1):
                    data = numpy.memmap(filePath, dtype='int16')
                    dataSets.append(data)
    #profile = preBuildProfile(dataSets)
    #out_path = os.path.join(path, "profile.p")
    #if not os.path.exists(out_path):
        #os.makedirs(out_path)
    #proFile = io.open(out_path, 'w+')
    #pickle.dump(profile, proFile)
    return preBuildProfile(dataSets)
                    

def graphTest(profile):
    #Create figure to graph with
    fig = figure(figsize=(16,12))
    fig.suptitle("Jacob's Test")
    #Setup plot of path traced
    #subplot(1,2,1)
    #xlim(0,800)
    #ylim(1280,0)
    #title("Challenge/Response Path")
    #xlabel("X location (pixels)")
    #ylabel("Y location (pixels)")
    #CX = np.array(challengeX)
    #CY = np.array(challengeY)
    #plot(CX, CY, color='green', linewidth=2, linestyle="--", label="Generated Challenge")
    #RX = np.array(respX)
    #RY = np.array(respY)
    #plot(RX, RY, color='blue', linewidth=2, label="User Response")
    #annotate("Start", xy=(challengeX[0], challengeY[0]), bbox=dict(facecolor='white', edgecolor='None', alpha=0.65 ))
    #annotate("End", xy=(challengeX[-1], challengeY[-1]), bbox=dict(facecolor='white', edgecolor='None', alpha=0.65 ))
    #legend(loc='upper left')
    #Setup plot of pressure data
    subplot(1,2,1)
    title("Overlay")
    xlabel("Points")
    ylabel("Magnitude")
    maximum = 0
    averages = [0 for i in range(len(profile))]
    stddevs = [0 for i in range(len(profile))]
    for point in profile:
        if point.avg > maximum:
            maximum = point.avg
    i = 0
    xlim(0, len(profile))
    ylim(0, 1.0)
    for point in profile:
        averages[i] = point.avg
        stddevs[i] = point.stddev
        i = i + 1
    posDevs = [averages[i] + (2 * stddevs[i]) for i in range(len(profile))]
    negDevs = [averages[i] - (2 * stddevs[i]) for i in range(len(profile))]
    PTS = np.linspace(1,len(profile), len(profile))
    plot(PTS, averages, color='blue', linewidth=2, label="Averages")
    plot(PTS, posDevs, color='red', linewidth=2, label="+2 devs")
    plot(PTS, negDevs, color='green', linewidth=2, label="-2 devs")
    legend(loc='lower right')
    show()
