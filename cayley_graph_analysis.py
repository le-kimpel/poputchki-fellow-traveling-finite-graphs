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

def compute_word_differences(G, u, v):
	'''
	Compute the number of possible shortest paths between fellow-traveling vertices (word metric)
	'''
	count=0
	d=G.diameter()
	G = G.networkx_graph()
	p = nx.all_simple_paths(G,u,v,cutoff=d)
	P = dict()
	for path in p:
		l = len(path)-1
		if l not in P.keys():
			P[l] = [path]
		else:
			P[l].append(path)
	min_length = min(P.keys())
	count = len(P[min_length])
	return count
def group_generators(G):
	return[g for g in G.gens()]

def toroidal(p,q):
	'''
	Builds a toroidal graph (Cartesian product of two cycles, Cp and Cq)
	'''
	G1=graphs.CycleGraph(p)
	G2=graphs.CycleGraph(q)
	print("G1 diameter: " + str(G1.diameter()))
	print("G2 diameter: " + str(G2.diameter()))  
	Z = G1.cartesian_product(G2)
	return Z

def generate_ladder_graph(n):
	'''
	Builds a graph consisting of many induced 4-cycles and connects the endpoints.
	This is a graph on 2n vertices.
	'''
	G = Graph()
	for i in range(0, n-1):
		G.add_edge(i, i+1)
	for i in range(n,2*n-1):
		G.add_edge(i,i+1)
	for i in range(0,n):
		G.add_edge(i,i+n)
	G.add_edge(0, 2*n-1)
	G.add_edge(n-1, n)
	G.show()
	print(G.is_vertex_transitive())
	print(G.is_cayley())
	print(G.edge_isoperimetric_number())
	return G
	
	
G = toroidal(4,5)
G = G.networkx_graph()
pos = nx.circular_layout(G)
nx.draw(G, pos, with_labels=true)


'''
diam = []
compare=[]
num_vertices = []
for i in range(2, 16):
	A = generate_ladder_graph(i)
	diam.append(A.diameter())
	num_vertices.append(2*i)
	compare.append(log(2*i))
plt.plot(num_vertices, diam)
plt.plot(num_vertices, compare)
plt.xlabel("Number of vertices")
plt.ylabel("Diameter")
plt.show()
'''
'''
Some Cayley expander graphs...
all we need to do is ensure that S is symmetric.
'''
'''
M = graphs.CubeGraph(5)
M.show()
G=SL(2,GF(3))
gens = group_generators(G)
print(G.list())
Z = gen_cayley(G, gens).to_undirected()
Z.show()
#print(Z.edge_isoperimetric_number())
#print(k_fellow_traveler(Z))
print(Z.diameter())
print(compute_word_differences(Z, G.list()[0], G.list()[5]))

u = G.list()[17]
v = G.list()[6]


for i in range(2,5):
	G = SymmetricGroup(i)
	gens = []
	for j in range(1, i):
		gens.append((j,j+1))
	CG = gen_cayley(G, gens).to_undirected()
	#print(compute_word_differences(CG,G.list()[0],G.list()[5]))
	print("Diam for n="+str(i) + ": " + str(CG.diameter()))
	CG.show()
'''
