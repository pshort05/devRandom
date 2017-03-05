#!/usr/bin/python
# -*- coding: utf-8 -*-
# ----------------------------------------------------------------------------------------------------------------------
#
#                               devRandom.py    by Paul Short
#                                               paul@jpkweb.com
#                                               using Python v3.6
#
# ----------------------------------------------------------------------------------------------------------------------
import time
import random
import psutil

# Class for the Random Pool
class randomPool():

    # create an empty array to use as the ongoing random pool - use only printable characters so numbers will be in
    #   the range of 1 to 255 but we will print them as unicode characters
    randomList=[]

    # Initialize the random pool using net counters
    def __init__(self):
        netCounters = psutil.net_io_counters()
        random.seed(netCounters[0] % 1000000)
        self.randomSeed()
        for i in range (100):
            self.randomList.append(random.randint(32, 126))

# Randomness methods to grab information from the environment to add to the random pool and keep it current
    def addRandomness(self):
        # generate the random characters
        for i in range (100):
            self.randomList[i]=(random.randint(1, 255))

        # randomly decide when to reseed and mix
        if random.randint(0,100) == 0 :
            self.randomSeed()
        if random.randint(0,200) == 0 :
            self.mixRandomness()
        return

    # Mixing Randomness will be used to swap data within the list - grab a number between 1 to 100 to determine the number
    #   of items to mix
    def mixRandomness(self):
        for i in range(100):
            p1 = random.randint(0, 99)
            p2 = random.randint(0, 99)
            if p1!=p2:
                n1 = self.randomList[p1]
                n2 = self.randomList[p2]
                self.randomList[p1] = n2
                self.randomList[p2] = n1

    # Print and remove items from the list
    def printRandomness(self):
        for item in self.randomList:
            print(chr(item), "", end="")
            pass
        print()

    def randomSeed(self):
        ioCounters = 0
        t = random.randint(0,3)
        # I tried to use disk IO, network IO and others but did not get enough variation in the pool
        # Grab the CPU times
        ioCounters = psutil.cpu_times()
        if t == 0:
            random.seed(int(ioCounters[0]*100) % 1000 )
        elif t == 1:
            # Note - skipping nice time - was always 0 during tests
            random.seed(int(ioCounters[2]*100) % 1000 )
        elif t == 2:
            random.seed(int(ioCounters[3]*100) % 1000 )
        # this item will force a "random mixing" of data
        elif t == 3:
            random.seed(int(round(time.time() * 1000)) % 10000 )
        else:
            # - exception case - will use milliseconds like above
            random.seed(int(round(time.time() * 1000)) % 10000 )


# main execution
random.seed()
pool1 = randomPool()
while True:
    pool1.addRandomness()
    pool1.printRandomness()
