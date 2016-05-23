from time import time
from mpi4py import MPI
import argparse
import sys

def primo(num):
	root=num**0.5
	i=3
	while i<=root:
		if num%i==0:
			return False
			break
		else:
			if i%10==3:
				i=i+4
			else:
				i=i+2
	return True
#cuantos y de donde a donde
cont=0
n=int(sys.argv[1])
last=10**n
first=10**(n-1)
size=last-first

highest=MPI.COMM_WORLD.Get_size()-1 #rank del ultimo proceso

comm=MPI.COMM_WORLD
my_size = size // comm.size + 1    # Every process computes a vector of lenth *my_size*
num=first+comm.rank*my_size + 1
my_offset=num
if comm.rank==highest:
	top=last-1
else:
	top=num+my_size-1

start=time()
if n!=1:
	while (num<top):
		if primo(num):
			cont=cont+1
		if num%10==3:
			num=num+4
		else:
			num=num+2	
else:
	cont=4
	
end=time()
tiempo=end-start
int total_primos
float total_tiempo
comm.Reduce(&cont,&total_primos,op=MPI.SUM,root=0)
comm.Reduce(&tiempo,&total_tiempo,op=MPI.SUM,root=0)
if comm.rank == 0:
	print total_primos," numeros primos con ",n," digitos en ",total_tiempo, " segundos"