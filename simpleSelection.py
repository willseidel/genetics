#!/Users/agray/anaconda/bin/python

import random
import os

#dynamic path  
directoryname = os.path.dirname(os.path.abspath('population.txt'))
filename = os.path.join(directoryname,'population.txt')
#print filename
#print directoryname

#this function reads in a text file to create an initial population dictionary
def readPopulation(delineator, input_file_path):

	input_dict = {} 						#making new dictionary for input file
	input_file = open(input_file_path)		#reading input file
	lines = input_file.readlines() 			#reading input file lines

	for line in lines:
		details = line.split("=")
		name = details[0]
		name = name.strip() 				#stripping white space
		genSeq = details[1] 				#reading genetic sequence
		genSeq = genSeq.strip() 			#stripping genetic sequence whitespace
		subjectInfo = [details[1],float(genSeq.count(fitnessPreference))/len(genSeq)]#\
		#calculating % of desired trait and assigning to subject data
		input_dict[name] = subjectInfo 		#assigning subject data to dictionary entry

	return input_dict

#This function takes as input a population dictionary and a member of that population \
#along with that member's generation and fecundity values. It adds copies of the member \
#with the name modified to reflect the generation and fecundity of the copy.
def asexual(dictionary,target,generation,fecundity):
	speciesnumber=1
	while speciesnumber<fecundity+1:
		newspecies=target+str(generation)+str(speciesnumber)
		speciesnumber=speciesnumber+1
		dictionary[newspecies] = dictionary[target]
	return dictionary

#This function calculates the product of each entry in the dictionary's % of desired traits \
#multiplied by a random value between 0 and 1. That value is then mapped to fecundity based\
#on user-specified floors.
def selectionTimestep(population,gen,oneFloor,twoFloor):
	
	for key, subjectInfo in population.items():
		subjectInfo = population[key] 				#getting subject info
		fitness = subjectInfo[1]*random.random() 	#assigning fitness with random
		if fitness > twoFloor:
			population = asexual(population,key,gen,2)
		if fitness > oneFloor and fitness < twoFloor:
			population = asexual(population,key,gen,1)
		del population[key] 						#killing last generation's people

	return population

#This function calls selectionTimestep to simulate a user-specified number of generations.
def runGenerations(nGenerations,population,fitnessPreference,oneOffSpringFloor,twoOffSpringFloor):
	generation = 0 									#generation counter
	genList = [] 									#list of generations for plotting
	fitnessAvg = []									#declaring list of fitness averages
	while (generation < numGenerations):
		generation = generation + 1
		genList.append(generation)
		fitnessAvg.append(fitnessTrack(population,fitnessPreference))
		print "generation #:",generation 			#showing current generation info
		#print population
		print "average fitness:",fitnessAvg[generation-1] #lists are indexed from zero
		print "***********"
		population = selectionTimestep(population,generation,oneOffSpringFloor,twoOffSpringFloor)

	null = fitnessPlot(genList,fitnessAvg)
	return population

#This function calculates the average proportion of desired traits in a population
def fitnessTrack(population,fitnessPreference):	
	total = 0
	for key in population:
		total = total + population[key][1]
	return total/len(population)		

#This function plots two vectors against eachother
def fitnessPlot(gen,fit):
	import matplotlib.pyplot as plt

	plt.plot(gen,fit)
	plt.ylabel('fitness [-]')
	plt.xlabel('generation [-]')
	plt.axis([0,max(gen)+1,0,1.2])
	plt.show()	

#This function collects user input for fitnessPreference and numGenerations
def userInput():
	fitnessPreference = raw_input("what nucleotide should we select for (A, C, T or G)?\n")
	numGenerations = int(raw_input("how many generations should we have?\n"))
	fitnessPreference = fitnessPreference[:1].upper() + fitnessPreference[1:]
	print "your fitness preference is:",fitnessPreference
	print "we'll run for this many generations:",numGenerations
	fromuser = []
	fromuser.append(fitnessPreference)
	fromuser.append(numGenerations)
	return fromuser

#This function estiamtes fitness level
def fitnessCalc(IdealCandidate,TestCandidate):
	"""Ideal Candidate is the reference fitness
	The test candidate is the generation sample. 
	The fitness is calculated for this candidate 
	relative to the IdealCandidate
    """
	if len(IdealCandidate)!=len(TestCandidate):
		print 'Your two inputs are strings of different lengths. You may have an error.'
	print 'Your test candidates are:'
	print ('Reference Candidate is:' + IdealCandidate)
	print ('Your Test Candidate is:' + TestCandidate)
	c=[]
	for i in xrange(len(IdealCandidate)):
		c.append(IdealCandidate[i]==TestCandidate[i]) #when characters match c is true == 1 when they are false c is false == 0
	return float(sum(c))/len(c)
	

#main code begins here


delineator = '='
oneOffSpringFloor = 0.1
twoOffSpringFloor = 0.15
infofromuser = userInput()
fitnessPreference = infofromuser[0]
numGenerations = infofromuser[1]
input_file_path = filename # was "/Users/tsacco/pythonwork/genetics/population.txt"

input_dict = readPopulation(delineator, input_file_path)
input_dict = runGenerations(numGenerations,input_dict,fitnessPreference,oneOffSpringFloor,twoOffSpringFloor)

# Example way to calculate fitness using fitnessCalc function above
a='ATFGJSA'
b='GNDHJSA'
c=fitnessCalc(a,b)
print c



