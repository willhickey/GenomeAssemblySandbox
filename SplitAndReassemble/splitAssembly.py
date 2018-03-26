#	2018-03-25
#	Will Hickey
#
#	This script chops up an assembled genome. The resulting "reads" can then be 
#	reassembled as an in silico test of various read lengths and coverages.
#	Since genomes have repeating sequences there is a minimum read length
#	required to assemble any specific genome (intutively a read length of 1
#	is never sufficient). Randomly chopping and re-assembling genomes provides
#	a very fast way to compare the assemblies with different read lengths
#	while sacrificing some external validity.

import random
import sys

def getInsertLength():
	return 1000		#This should be replaced with a distribution

def getReadLength():
	return 250		#This should also be replaced with a distribution

fastaFile = open("data/MAB.ATCC19977.fasta", "r")
fastqFile1 = open("data/output1.fastq", "w")
fastqFile2 = open("data/output2.fastq", "w")
line = fastaFile.readline()	#header line gets thrown away
assembly = ""
#read the assembly and store it as a single string
while line:
	line = fastaFile.readline()
	assembly = assembly + line
fastaFile.close()
assembly = assembly.replace("\n", "")
assemblyLength = len(assembly)

#add the first 1000 characters to the end so we don't read off the end
#the genome is circular so a read that wraps around to the start is fine
assembly = assembly + assembly[0:1000]

#print(assembly)
#print(assemblyLength)

headerSequence = 0
coverage = 100
meanReadLength = 250
numberOfReadPairs = coverage * assemblyLength / (2*meanReadLength)
print(numberOfReadPairs)
for i in range(0,int(numberOfReadPairs)):
	#startOfRead = random.randrange(0, assemblyLength, 1)
	startOfRead = random.randrange(0, assemblyLength, 1)
	insertLength = getInsertLength()
	readLength1 = getReadLength()
	readLength2 = getReadLength()
	read1 = assembly[startOfRead:startOfRead+readLength1]
	#read2 = assembly[startOfRead+insertLength:startOfRead+insertLength+readLength2:-1]
	read2 = assembly[startOfRead+insertLength-1:startOfRead+insertLength-readLength2-1:-1]
	myRand = random.random()

	#fastq format is a repeating sequence of 4 lines that look like this
	#@id		id can be anything but should be unique and perfectly paired between paired reads
	#read		GATC
	#+
	#phred		series of phred scores, same length as the read. hardcoding "I" here for now
	output1 = "@" + str(headerSequence) + "\n" + read1 + "\n+\n" + "I"*readLength1
	output2 = "@" + str(headerSequence) + "\n" + read2 + "\n+\n" + "I"*readLength2

	#In normal fastq data there's no way to tell which read is forwards and which is backwards.
	#Here read1 is forward and read2 is backward, so we randomize which gets printed to each file
	#to simulate the normal uncertainty.
	if myRand < .5:
		fastqFile1.write(output1 + "\n")
		fastqFile2.write(output2 + "\n")
	else:
		fastqFile1.write(output2 + "\n")
		fastqFile2.write(output1 + "\n")
	headerSequence = headerSequence + 1
	#print("Forward from " + str(startOfRead) + ": " + read1)
	#print("Backward from " + str(startOfRead + insertLength) + ": " + read2)

fastqFile1.close()
fastqFile2.close()

