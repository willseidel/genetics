#This script is an example of how to read a file into a dictionary
import random
import math

#this function takes a population, pairs off members, mates them, returns a random number of offspring\
#who either live or die based on their fitness level. The function then returns a population of surviving offspring.
def sexualReproduction(population,survivalM,nChildren,fitnessPref,genNumber):
	nPairs = int(round(len(population)/2,2)) #number of pairs
	pairCounter = 1
	children = {}	#initiliazing dictionary of children
	while pairCounter < nPairs+1:
		parents 		= random.sample(population,2)
		firstParent 	= parents[0]
		secondParent 	= parents[1]
		chCounter 		= 1
		while chCounter < nChildren+1:
			childTemp = parentMixer(population,firstParent,secondParent,fitnessPref)
			if random.random()*childTemp[2] > survivalM: #if the product of the child's fitness and a random number exceeds survival threshold
				children[childTemp[0]+"_gen:"+str(genNumber)+"_child:"+str(chCounter)] = [childTemp[1],childTemp[2]] #then we assign the child to the population
			chCounter = chCounter + 1
		del population[firstParent]
		del population[secondParent]
		pairCounter = pairCounter + 1

	return children

#this function takes a name and a genetic code and makes a new population member
def fitnessCalc(gCode,fitPref):
	fitC = float(gCode.count(fitPref))/len(gCode)
	return fitC

#this function reads in a text file to create an initial population dictionary
def readPopulation(delineator, input_file_path,fPreference):

	input_dict = {} 						#making new dictionary for input file
	input_file = open(input_file_path)		#reading input file
	lines = input_file.readlines() 			#reading input file lines

	for line in lines:
		details = line.split("=")
		name = details[0]
		name = name.strip() 				#stripping white space
		genSeq = details[1] 				#reading genetic sequence
		genSeq = genSeq.strip() 			#stripping genetic sequence whitespace
		subjectInfo = [genSeq,float(genSeq.count(fPreference))/len(genSeq)]#\
		#calculating % of desired trait and assigning to subject data
		input_dict[name] = subjectInfo 		#assigning subject data to dictionary entry

	return input_dict

def parentMixer(population,parent1,parent2,fPref):

	combinedGenes = '' #declaring list that will hold genetic code
	i = 0 #index counter
	for c in population[parent1][0]:
		if random.random()>0.5: #50/50 shot for each parent at passing on code entry
			combinedGenes += population[parent1][0][i]
		else:
			combinedGenes += population[parent2][0][i]
		i = i+1

	parent1stripped = ''.join([j for j in parent1 if not j.isdigit()]) #stripping digits from names
	parent2stripped = ''.join([j for j in parent2 if not j.isdigit()])

	childName 	= parent1stripped[:3] + parent2stripped[:3]
	childFit 	= fitnessCalc(combinedGenes,fPref)

	child = []
	child.append(childName)
	child.append(combinedGenes)
	child.append(childFit)
	return child


#This function calls selectionTimestep to simulate a user-specified number of generations.
def runGenerations(numGenerations,population,fitnessPreference,survivalMin,nKids):
	
	generation = 0 									#generation counter
	genList = [] 									#list of generations for plotting
	fitnessAvg = []									#declaring list of fitness averages
	while (generation < numGenerations):
		generation = generation + 1
		genList.append(generation)
		fitnessAvg.append(fitnessTrack(population,fitnessPreference))
		print "generation #:",generation,"numGenerations",numGenerations			#showing current generation info
		print "population",len(population)
		print "average fitness:",fitnessAvg[generation-1] #lists are indexed from zero
		print "***********"
		population = sexualReproduction(population,survivalMin,nKids,fitnessPreference,generation)

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

#main code begins here
nGenerations = int(raw_input('number of generations?\n'))
fitnessPreference = raw_input('fitness preference?\n')
delineator = '='
survivalThreshold = 0.2
numberChildren = 5
input_file_path = "/Users/wseidel/Documents/python/genetics/population.txt"

input_dict = readPopulation(delineator, input_file_path,fitnessPreference)
input_dict = runGenerations(nGenerations,input_dict,fitnessPreference,survivalThreshold,numberChildren)
print input_dict
