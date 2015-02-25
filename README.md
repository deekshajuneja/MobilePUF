# PUFProject
The path drawn on the screen but the android device is generated by a simple program
that just uses Java libaries to randomly generate 4 x,y pairs on the screen and draw them.
The algorithm makes sure that all the x,y pairs are atleast a minimum distance from eachother.
The paths are seeded with an incrementing count before each use to ensure easy reproducability
of each individual path.

# Folder Breakdown
1. /581Project/
  * This folder contains all the code for the android project used to record the data
2. /scripts/
  * Has all the python scripts I've created to generate output and figures
3. /Figures/
  * Contains all the generated figures created by genFigures.py
4. /OutputCSVs/
  * This folder has all of the CSVs with the raw location/pressure data collected from the android project
5. /OutputGenerated/
  * Contains all the generated binary files using different strategies. Each strategy has it's own sub folder and are detailed below.
6. /Results/
  * Contains the results from automated tests like the PRG testing and hamming distance tests.
7. /Screenshots/
  * Screenshots of the android app used to record the pressure data.

# Strategy Breakdown
These are the strategies used to generate the random 1's or 0's.

1. Simple Average
  * This is the simplest strategy, averages all the pressure values and then outputs a 0 or 1 depending on if it is above or below the average.
2. Moving average n=5
  * This strategy uses a moving average with an n of 5 to compare the pressure value against
3. Moving average n=10
  * Same as above but n=10
4. Cumulative moving average
  * This strategy uses a cumulative running average for the pressure comparison.

