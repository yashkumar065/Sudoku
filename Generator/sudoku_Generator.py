from z3 import *
import math
import random
import copy
import glob

#Grid Size
grid_Size=int(input("Enter the grid size to be considered!\n"))

#Array of Vector Names
Array=['X'+str(i) for i in range(1,grid_Size+1)]

#Variables for Vectors for the grid size considered
for i in range(grid_Size):
	Array[i] = IntVector('x'+str(i+1), grid_Size)	

#Array of Vector Names
saveArray=['X'+str(i) for i in range(1,grid_Size+1)]

#Variables for Vectors for the grid size considered
for i in range(grid_Size):
	saveArray[i] = IntVector('x'+str(i+1), grid_Size)

#Array of Vector Names
NewArray=['X'+str(i) for i in range(1,grid_Size+1)]

#Variables for Vectors for the grid size considered
for i in range(grid_Size):
	NewArray[i] = IntVector('x'+str(i+1), grid_Size)

file_count=len(glob.glob("*.txt"))
print("Files: "+str(file_count))

if file_count!=0:
	print(grid_Size)
	list=[]
	for i in range(file_count):
		ac='your_file'+str(i+1)+'_'+str(grid_Size)+'.txt'
		file = open('your_file'+str(i+1)+'_'+str(grid_Size)+'.txt', 'r')
		Lines = file.readlines()
		for l in range(grid_Size):
			saveArray[l]=eval(Lines[l])
		break

k = Solver()
#Solver 
s = Solver()

#Backup_Solver
b = Solver()

#######Constraints

#All values Greater than 0

for arr in Array:	
	for i in range(grid_Size):
		s.add(0<arr[i])
		s.add(arr[i]<grid_Size+1)
		#s.add(And(arr[i]>=1, arr[i]<=grid_Size))
#s.push()

#Uniqueness of each Row,Column and sub-grids

#Row
for arr in Array:
	s.add(Distinct(arr))
#s.push()

#Column
for i in range(grid_Size):
	col=[arr[i] for arr in Array]
	s.add(Distinct(col))
#s.push()

#Sub-Grid

sub_Grid=int(math.sqrt(grid_Size))
for i in range(sub_Grid):
	Array_N=Array[i*sub_Grid:(i+1)*sub_Grid]
	for k in range(sub_Grid):
		grid_Sub_List=[]
		for j in range(k*sub_Grid,(k+1)*sub_Grid):
			temp=[arr[j] for arr in Array_N]
			grid_Sub_List=grid_Sub_List+temp			
		s.add(Distinct(grid_Sub_List))

k=copy.deepcopy(s)

prev_array_no = -1
prev_Element = -1

while True:
	count_Sol = 0

	NewArray=copy.deepcopy(saveArray)	
	
	array_Number = random.randint(1, grid_Size)
	element_Number = random.randint(1, grid_Size)

	while prev_array_no == array_Number and prev_Element ==element_Number:
		array_Number = random.randint(1, grid_Size)
		element_Number = random.randint(1, grid_Size)

	prev_array_no = array_Number
	prev_Element = element_Number
	saveArray[array_Number-1][element_Number-1] = 0

	instance_c = [ If(saveArray[i][j] == 0,
		          True,
		          Array[i][j] == saveArray[i][j])
		       for i in range(grid_Size) for j in range(grid_Size) ]

	
	s.add(instance_c)

	if s.check() == unsat:
		break

	while s.check() == sat and count_Sol <2:
		ls=[]
		count_Sol=count_Sol+1
		for i in range(grid_Size):
			for j in range(grid_Size):
				ls=ls+[Array[i][j]!=s.model()[Array[i][j]]]
		s.add(Or(ls))

	if count_Sol == 2:
		print("Got it!")
		saveArray=copy.deepcopy(NewArray)
		break
		
	
	s=copy.deepcopy(k)

	
print("\n*********************Generated Sudoku*******************\n")
i=0
j=0
for arr in saveArray:
	i=0
	j=j+1
	for a in arr:
		i=i+1
		#print("["+str(a)+"]", end='')
		print(" "+str(a)+ " ", end='')
		if i%sub_Grid==0 and i!=grid_Size:
			print(" | ", end='')
	print("\n", end='')
	if j%sub_Grid==0 and j!=grid_Size:
		print("--- "*grid_Size)

print("\n**********************Checking number of solutions again**********************\n")
s=copy.deepcopy(k)
instance_c = [ If(saveArray[i][j] == 0,
	          True,
	          Array[i][j] == saveArray[i][j])
	       for i in range(grid_Size) for j in range(grid_Size) ]
s.add(instance_c)
count=0
while s.check() == sat:
	ls=[]
	count=count+1
	print(s.model())
	for i in range(grid_Size):
		for j in range(grid_Size):
			ls=ls+[Array[i][j]!=s.model()[Array[i][j]]]
	s.add(Or(ls))

print("\nNumber of possible solutions: "+str(count))
	

