#!/Users/agray/anaconda/bin/python

import random
import math
import os
import string
from lxml import html
import requests

#this function takes a population, pairs off members, mates them, returns a random number of offspring\
#who either live or die based on their fitness level. The function then returns a population of surviving offspring.
def sexualReproduction(population,SurvivalMin,nChildren,FitnessPreference,GenNumber,MutationProbability):
	nPairs = int(round(len(population)/2,2)) #number of pairs
	pairCounter = 1
	children = {}	#initiliazing dictionary of children
	while pairCounter < nPairs+1:
		parents 		= random.sample(population,2)
		firstParent 	= parents[0]
		secondParent 	= parents[1]
		chCounter 		= 1
		while chCounter < nChildren+1:
			childTemp = parentMixer(population,firstParent,secondParent,FitnessPreference,MutationProbability)
			if random.random()*childTemp[2] > SurvivalMin: #if the product of the child's fitness and a random number exceeds survival threshold
				children[childTemp[0]+"_gen:"+str(GenNumber)+"_child:"+str(chCounter)] = [childTemp[1],childTemp[2]] #then we assign the child to the population
			chCounter = chCounter + 1
		del population[firstParent]
		del population[secondParent]
		pairCounter = pairCounter + 1

	return children

#this function reads in a text file to create an initial population dictionary
def readPopulation(delineator,InputFilePath,FitnessPreference):

	population = {} 						#making new dictionary for input file
	InputFile = open(InputFilePath)		#reading input file
	lines = InputFile.readlines() 			#reading input file lines

	for line in lines:
		details = line.split("=")
		name = details[0]
		name = name.strip() 				#stripping white space
		genSeq = details[1] 				#reading genetic sequence
		genSeq = genSeq.strip() 			#stripping genetic sequence whitespace
		subjectInfo = [genSeq,fitnessCalcRelative(FitnessPreference,genSeq)]#\
						
		#calculating % of desired trait and assigning to subject data
		population[name] = subjectInfo 		#assigning subject data to dictionary entry

	return population

def parentMixer(population,parent1,parent2,FitnessPreference,MutationProbability):

	"""We iterate through the genome and at
	each entry we either mutate and chose
	randomly between G,A,T or C, or we chose
	between the source genes of the parents"""

	combinedGenes = '' #declaring list that will hold genetic code
	i = 0 #index counter
	for c in population[parent1][0]:
		if random.random()>(1-MutationProbability): 
			MutationPicker = random.random()  
			if MutationPicker <=0.25:
				combinedGenes += "G"
			if MutationPicker >0.25 and MutationPicker<=0.5:
				combinedGenes += "A"
			if MutationPicker >0.5 and MutationPicker<=0.75:
				combinedGenes += "T"
			if MutationPicker >0.75:
			 	combinedGenes += "C"
		else:
			if random.random()>0.5: #50/50 shot for each parent at passing on code entry
				combinedGenes += population[parent1][0][i]
			else:
				combinedGenes += population[parent2][0][i]


		i = i+1

	parent1stripped = ''.join([j for j in parent1 if not j.isdigit()]) #stripping digits from names
	parent2stripped = ''.join([j for j in parent2 if not j.isdigit()])

	childName 	= parent1stripped[:3] + parent2stripped[:3]
	childFit	= fitnessCalcRelative(combinedGenes,FitnessPreference)

	child = []
	child.append(childName)
	child.append(combinedGenes)
	child.append(childFit)
	return child


#This function calls selectionTimestep to simulate a user-specified number of generations.
def runGenerations(nGenerations,population,FitnessPreference,SurvivalMin,nChildren,MutationProbability):
	
	generation = 0 									#generation counter
	genList = [] 									#list of generations for plotting
	fitnessAvg = []									#declaring list of fitness averages
	while (generation < nGenerations):
		generation = generation + 1
		genList.append(generation)
		fitnessAvg.append(fitnessTrack(population))
		print "generation #:",generation,"nGenerations",nGenerations			#showing current generation info
		print "population",len(population)
		print "generation #:",generation 			#showing current generation info
		print "average fitness:",fitnessAvg[generation-1] #lists are indexed from zero
		print "***********"
		population = sexualReproduction(population,SurvivalMin,nChildren,FitnessPreference,generation,MutationProbability)

	null = fitnessPlot(genList,fitnessAvg)
	return population

#This function calculates the average proportion of desired traits in a population
def fitnessTrack(population):	
	total = 0
	for key in population:
		total = total + population[key][1]
	return total/len(population)		

#This function plots two vectors against eachother
def fitnessPlot(generation,fit):
	import matplotlib.pyplot as plt
	import numpy as np
	plt.rcParams['axes.color_cycle'] = ['b', 'grey', '#ff00ab'] #line color cycle
	plt.rcParams['lines.linewidth'] = 20.0 #line width
	plt.plot(generation,fit, ':') # third term ':' sets dots '--' for dashes
	plt.plot(generation,fit,'--') #testing a second plot
	plt.ylabel('fitness [-]')
	plt.xlabel('generation [-]')
	plt.grid(True) #add a grid
	plt.text(1, 1.2, 'The Champ Was Here') #puts text on graph at selected coordinates
	plt.fill(generation, fit, 'g') #fill the space with color
	plt.axis([0,max(generation)+1,0,1.5])
	plt.show()
	#Playing around with scatter plotting and varying color of points
	t = np.linspace(0, 2 * np.pi, 25) #creates a set of 25 numbers between 0 and 2*pi
	x = np.sin(t)
	y = np.cos(t)
	plt.scatter(t,x,c=y) #cmap='viridis' could be added to specify a colormap
	plt.show()	

#This function collects user input for fitnessPreference and numGenerations
def userInput():
	from string import whitespace
	FitnessPreference = raw_input("What genetic sequence represents ideal fitness? (combination of A, C, T or G)?\n")
	FitnessPreference = FitnessPreference.translate(None, whitespace) #strips whitespace from sequence
	FitnessPreference = FitnessPreference.upper() #uppercases the sequence	
	FitnessPreference = FitnessPreference.translate(None, '0123456789BDEFHIJKLMNOPQRSUVWXYZ!@#$%^&*()-_+=~`{[}]|\:;"<,>.?/') #removes non-ACTG characters
	FitnessPreference = FitnessPreference[:8] #truncates sequence to first 8 letters
	#FitnessPreference = raw_input("What genetic sequence represents ideal fitness? (combination of A, C, T or G)?\n")
	numGenerations = int(raw_input("how many generations should we have?\n"))
	#FitnessPreference = FitnessPreference[:1].upper() + FitnessPreference[1:]
	print "your fitness preference is:",FitnessPreference
	print "we'll run for this many generations:",numGenerations
	fromuser = []
	fromuser.append(FitnessPreference)
	fromuser.append(numGenerations)
	return fromuser

#This function estimates fitness level
def fitnessCalcRelative(IdealCandidate,TestCandidate):
	"""Ideal Candidate is the reference fitness
	The test candidate is the generation sample. 
	The fitness is calculated for this candidate 
	relative to the IdealCandidate
 	"""
	if len(IdealCandidate)!=len(TestCandidate):
		print 'Your two inputs are strings of different lengths. You may have an error.'
	c=[]
	for i in xrange(len(IdealCandidate)):
		c.append(IdealCandidate[i]==TestCandidate[i]) #when characters match c is true == 1 when they are false c is false == 0
	return float(sum(c))/len(c)


#main code begins here
#dynamic path  
directoryname 		= os.path.dirname(os.path.abspath('population.txt'))
filename 			= os.path.join(directoryname,'population.txt')
populationFilepath 	= filename # was "/Users/tsacco/pythonwork/genetics/population.txt"

userResponse 		= userInput()
FitnessPreference 	= userResponse[0]
nGenerations 		= userResponse[1]
delineator 			= '='
survivalThreshold 	= 0.2
nChildren 			= 10
MutationProbability = 0.001

populationFilepath 	= filename # was "/Users/tsacco/pythonwork/genetics/population.txt"

population 			= readPopulation(delineator,populationFilepath,FitnessPreference)
population 			= runGenerations(nGenerations,population,FitnessPreference,survivalThreshold,nChildren,MutationProbability)
print population
page 				= requests.get('http://results.tfmeetpro.com/Athletic_Timing/TrackTown_USA_High_Performance_Meet_2/results_28.html')
runners = tree.xpath('//td[@class="athlete"]/text()')
times = tree.xpath('//td[@class="time"]/text()')
print 'Runners: ', runners
print 'Times: ', times 