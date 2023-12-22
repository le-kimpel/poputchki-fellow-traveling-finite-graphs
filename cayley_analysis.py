import networkx as nx
import random
import numpy as np
import matplotlib.pyplot as plt
from sage.groups.group import is_Group
'''
Functions for analyzing automatic groups and properties relative to their Cayley graphs.
'''
def gen_cayley(G, generators, elements=None):
	'''
	Given a group G and its group generators, return its Cayley graph.
	Kind of assumes the given generators make sense.
	'''
	if is_Group(G):
		return G.cayley_graph(generators=generators, elements=elements)

def get_all_paths_from_origin(G):
	'''
	Given a graph G, starting from the origin point of G, (if it's a Cayley graph is the identity; if an ordinary graph it is just 		the first labeled vertex), compute all paths of length n emenating from the origin
	'''
	origin = min(G.vertices())
	all_paths_from_origin = {}
	for vertex in G.vertices():
		if vertex != origin:
			paths = G.all_paths(origin, vertex)
			# get the min length path
			#LENGTHS = [len(p) for p in paths]
			#MIN = min(LENGTHS)
			for path in paths:
				#print(path)
				if len(path)-1 not in all_paths_from_origin.keys():
					all_paths_from_origin[len(path)-1] = [path]
				else:
					all_paths_from_origin[len(path)-1].append(path)
	#print(all_paths_from_origin)
	return all_paths_from_origin
def k_fellow_traveler(G, exclude_non_disjoint_paths=False):
	'''
	Compute the maximum distance between vertices fellow-traveling paths.
	'''
	all_k = []
	all_paths_from_origin = get_all_paths_from_origin(G)
	#print(G.edges())
	#print(all_paths_from_origin)
	for length in all_paths_from_origin:
		paths = all_paths_from_origin[length]
		if len(paths) == 1:
			continue
		else:
			K = []
			# if a and b are equal length paths, compare d(a(i), b(i))
			for j in range(0, len(paths)):
				A = paths[j]
				for l in range(1, len(paths)):
					B = paths[l]
					if B!= A:
						if A[length] == B[length] or (A[length], B[length], None) in G.edges():
							if exclude_non_disjoint_paths == True:
								if set(A).intersection(B) == {0} or set(A).intersection(B) == {0, A[length]}:
									for i in range(0,length):
										u = A[i]
										v = B[i]
										p_prime = G.all_paths(u,v)
										m = [len(p) for p in p_prime]
										M = min(m)-1
										K.append(M)
										#if(M == 3):
										#print("A=: " + str(A))
										#print("B=: " + str(B))
										#print(M)
										#print(K)
							else:
								for i in range(0,length):
									u = A[i]
									v = B[i]
									p_prime = G.all_paths(u,v)
									m = [len(p) for p in p_prime]
									M = min(m)-1
									K.append(M)
									#if(M == 3):
									#print("A=: " + str(A))
									#print("B=: " + str(B))
									#print(M)
									#print(K)
		if (K != []):
			k = max(K)
			if k == G.diameter():
				return k
			all_k.append(k)
	#print(all_k)
	#print(G.diameter())
	max_k = max(all_k)
	return max_k
def group_generators(G):
	return[g for g in G.gens()]

'''
n=3
while n <= 50:
	G = graphs.CycleGraph(n)
	G.show()
	print("vertices: " + str(n))
	print(G.diameter())
	print(k_fellow_traveler(G))
	n+=1

n = 14
i=0
while i < 10:
	g = graphs.RandomRegular(3,n)
	while(g.is_vertex_transitive() == False):
		g = graphs.RandomRegular(3, n)
	g.show()
	print("Diameter: " + str(g.diameter()))
	k = k_fellow_traveler(g)
	print("fellow traveler constant: " + str(k))
	#n+=2
	i+=1
'''
