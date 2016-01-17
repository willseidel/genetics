#This script is an example of how to read a file into a dictionary
import random

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
	while (generation < nGenerations):
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

#This calls for user input for fitness preference and number of generations
fitnessPreference = raw_input("what nucleotide should we select for (A, C, T or G)?\n")
nGenerations = raw_input("how many generations should we run?\n")

#main code begins here

delineator = '='
oneOffSpringFloor = 0.15
twoOffSpringFloor = 0.3
input_file_path = "/Users/tsacco/pythonwork/genetics/population.txt"

input_dict = readPopulation(delineator, input_file_path)
input_dict = runGenerations(nGenerations,input_dict,fitnessPreference,oneOffSpringFloor,twoOffSpringFloor)
