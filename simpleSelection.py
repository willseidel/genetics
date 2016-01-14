#This script is an example of how to read a file into a dictionary
import random

def asexual(dictionary,target,generation,fecundity):
	speciesnumber=1
	while speciesnumber<fecundity+1:
		newspecies=target+str(generation)+str(speciesnumber)
		speciesnumber=speciesnumber+1
		dictionary[newspecies] = dictionary[target]
	return dictionary


def selectionTimestep(population,gen,oneFloor,twoFloor):
	
	for key, subjectInfo in population.items():
		subjectInfo = population[key] #getting subject info
		fitness = subjectInfo[1]*random.random() #assigning fitness with random
		if fitness > twoFloor:
			population = asexual(population,key,gen,2)
		if fitness > oneFloor and fitness < twoFloor:
			population = asexual(population,key,gen,1)
		del population[key] #killing last generation's people

	return population

#main code begins here

oneOffSpringFloor = 0.25
twoOffSpringFloor = 0.5

fitnessPreference = 'A'
numGenerations = 5

input_dict = {} #making new dictionary for input file
input_file = open("/Users/wseidel/Documents/python/genetics/population.txt") #path to text...
#... file to break into dictionary 

lines = input_file.readlines() #reading input file lines

for line in lines:
	details = line.split("=")
	name = details[0]
	name = name.strip() #stripping white space
	genSeq = details[1]
	genSeq = genSeq.strip()
	#input_dict[name] = genSeq

	subjectInfo = [details[1],float(genSeq.count(fitnessPreference))/len(genSeq)]
	#print "name:",name,subjectInfo[0],subjectInfo[1]
	input_dict[name] = subjectInfo


generation = 0
while (generation < numGenerations):
	generation = generation + 1
	print "generation #:",generation
	print input_dict
	print "***********"
	input_dict = selectionTimestep(input_dict,generation,oneOffSpringFloor,twoOffSpringFloor)
