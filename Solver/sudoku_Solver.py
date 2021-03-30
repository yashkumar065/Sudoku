from z3 import *
import math
import time
import glob

#Initial File Count
file_count=0

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

#Array of Check repeat
checkArray=['X'+str(i) for i in range(1,grid_Size+1)]

#Variables for Vectors for the grid size considered
for i in range(grid_Size):
	checkArray[i] = IntVector('x'+str(i+1), grid_Size)

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

count=0
flag=0
while s.check()==sat:
	ls=[]
	m=s.model()
	#print(s.model())
	count=count+1
	print(str(count)+"\n")

	file_count=len(glob.glob("*_"+str(grid_Size)+".txt"))
#	print("Files: "+str(file_count))
	
	for j in range(grid_Size):
		checkArray[j] = IntVector('x'+str(j+1), grid_Size)

	for i in range(grid_Size):
		for j in range(grid_Size):
			#if(isinstance(index,'z3.z3.ArithRef')):
			if type(checkArray[i][j]) != type(1):
				#print("entered")
				#print(Array[i][j])
				checkArray[i][j]=m.evaluate(checkArray[i][j])

	if file_count!=0:
		for i in range(file_count):
			for j in range(grid_Size):
				saveArray[j] = IntVector('x'+str(j+1), grid_Size)
			file = open('your_file'+str(i+1)+'_'+str(grid_Size)+'.txt', 'r')
			Lines = file.readlines()
			for l in range(grid_Size):
				saveArray[l]=eval(Lines[l])	
			if checkArray==saveArray:
				#print("************Checking")
				#with open('your_file'+str(file_count+1)+'_'+str(grid_Size)+'.txt', 'w') as f:
				#	for item in checkArray:
				#		f.write("%s\n" % item)
				flag=1

	else:
		with open('your_file'+str(file_count+1)+'_'+str(grid_Size)+'.txt', 'w') as f:
			for item in checkArray:
				f.write("%s\n" % item)
		break

	if flag==1:
		flag=0
		for i in range(grid_Size):
			for j in range(grid_Size):
				ls=ls+[Array[i][j]!=s.model()[Array[i][j]]]
		s.add(Or(ls))

	else:
		with open('your_file'+str(file_count+1)+'_'+str(grid_Size)+'.txt', 'w') as f:
			for item in checkArray:
				f.write("%s\n" % item)
		break
			

#print("Final Count: "+str(count))

print("\n*********************Solved Sudoku*******************\n")
i=0
j=0
for arr in checkArray:
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

