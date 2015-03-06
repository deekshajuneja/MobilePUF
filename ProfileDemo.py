import math
import numpy
import os
#import SoundUtil
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
    
#Expands/Contracts lists of data samples to all be of length N, for profiling
def buildProfile(dataSets):
      avg = 0
      
      #find average number of samples in the data
      for dataSet in dataSets:
		avg += len(dataSet)
      avg = avg/len(dataSets)
	
	
      sample_period = 1/22050
      pre_profile = []
	#for each clip in raw profile
      for clip in range( len(dataSets) ):
             print 'Processing clip %d' % clip
             #calculate new sample period
             new_period = sample_period * ( avg / len(dataSets[clip]) )
             new_data = []
             #interpolate data
             for sample in range( len(dataSets[clip]) ):
                 if sample == 0:
                     new_data.append( dataSets[clip][sample] )
                 else:
                     #equation for linear interpolation
                     data = dataSets[clip][sample-1] + (dataSets[clip][sample] - dataSets[clip][sample-1]) * ( sample*sample_period - (sample-1)*new_period ) / ( sample*new_period - (sample-1)*new_period ) 
                     new_data.append(data)
             pre_profile.append(new_data)
	
      profile = []
      for i in range(len(pre_profile)):
          print 'Adding processed data to profile: Clip %d' % i
          count = 0
          stat = []
          for j in range(len(pre_profile[i])):
			if j == count:
				stat.append(pre_profile[i][j])
                       j += 2
                       count += 1
          mean = numpy.mean(stat)
          stdev = numpy.std(stat)
          print repr(mean)
          print repr(stdev)
          profile.append( (mean, stdev) )
  
      return profile


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
                print 'Trimming file %s' % fileName
                filePath = join(root, fileName)
                startEnd = findStartEnd(join(root, fileName), 2000)
                if (startEnd[0] != -1):
                    data = numpy.memmap(filePath, dtype='int16')
                    dataSets.append(data)
    print 'Done Trimming'
    
    print 'Building Profile'
    profile = buildProfile(dataSets)
    profile = bytes(profile)
    out_path = os.path.join(path, "profile.p")
    
    proFile = io.open(out_path, 'wb')
    
    print 'Writing Profile to %s' % out_path
    pickle.dump(profile, proFile)

    #return preBuildProfile(dataSets)
    return True                

# def graphTest(profile):
    # #Create figure to graph with
    # fig = figure(figsize=(16,12))
    # fig.suptitle("Jacob's Test")
    # #Setup plot of path traced
    # #subplot(1,2,1)
    # #xlim(0,800)
    # #ylim(1280,0)
    # #title("Challenge/Response Path")
    # #xlabel("X location (pixels)")
    # #ylabel("Y location (pixels)")
    # #CX = np.array(challengeX)
    # #CY = np.array(challengeY)
    # #plot(CX, CY, color='green', linewidth=2, linestyle="--", label="Generated Challenge")
    # #RX = np.array(respX)
    # #RY = np.array(respY)
    # #plot(RX, RY, color='blue', linewidth=2, label="User Response")
    # #annotate("Start", xy=(challengeX[0], challengeY[0]), bbox=dict(facecolor='white', edgecolor='None', alpha=0.65 ))
    # #annotate("End", xy=(challengeX[-1], challengeY[-1]), bbox=dict(facecolor='white', edgecolor='None', alpha=0.65 ))
    # #legend(loc='upper left')
    # #Setup plot of pressure data
    # subplot(1,2,1)
    # title("Overlay")
    # xlabel("Points")
    # ylabel("Magnitude")
    # maximum = 0
    # averages = [0 for i in range(len(profile))]
    # stddevs = [0 for i in range(len(profile))]
    # for point in profile:
        # if point.avg > maximum:
            # maximum = point.avg
    # i = 0
    # xlim(0, len(profile))
    # ylim(0, 1.0)
    # for point in profile:
        # averages[i] = point.avg
        # stddevs[i] = point.stddev
        # i = i + 1
    # posDevs = [averages[i] + (2 * stddevs[i]) for i in range(len(profile))]
    # negDevs = [averages[i] - (2 * stddevs[i]) for i in range(len(profile))]
    # PTS = np.linspace(1,len(profile), len(profile))
    # plot(PTS, averages, color='blue', linewidth=2, label="Averages")
    # plot(PTS, posDevs, color='red', linewidth=2, label="+2 devs")
    # plot(PTS, negDevs, color='green', linewidth=2, label="-2 devs")
    # legend(loc='lower right')
    # show()
