import networkx as nx
from itertools import product
import numpy as np
from sage.groups.group import is_Group
'''
Functions for computing the Zig-Zag and Replacement products of graphs. 
'''
def flatten(t):
    for x in t:
        if isinstance(x, tuple):
            yield from flatten(x)
        else:
            yield x
def gen_cayley(G, generators):
	'''
	Given a group G and its group generators, return its Cayley graph.
	Kind of assumes the given generators make sense.
	'''
	if is_Group(G):
		return G.cayley_graph(generators=generators).to_undirected()

def group_generators(G):
	return[g for g in G.gens()]

def find_edge_in_list(Y, to_find):
	i = 0
	for edge in Y:
		if edge[0] == to_find[0] and edge[1] == to_find[1]:
			return i	
		else:
			i+=1
	return -1

def rotation_map(G):
	'''
	Get the rotation map of a d-regular graph G.
	This will determine the edges of the ZigZag product.
	'''
	G = G.to_directed()
	# First, build the vertex set of RotG.
	X = G.vertices()
	Y = G.edges()
	i = 1
	v = Y[0][0]
	for edge in Y:
		# starting vertex
		u = edge[0]
		if (u == v):
			G.set_edge_label(u, edge[1], i)
			i += 1
		else:
			v = u
			i = 1
			G.set_edge_label(u, edge[1], i)
			i+=1
	'''
	If (u,i) is on the path of v and (v,j) is on the path of (u,i) this corresponds to an element in RotG.
	E.g., an edge. Here, we'll take advantage of the directed graph structure:
	get (u,v) and (v,u). Grab the label i from (u,v) and the label j from (v,u). Then RotG(u,i) = (v,j).
	'''
	RotG = dict()
	
	for edge in Y:
		recip = (edge[1], edge[0])
		if G.has_edge(recip):
			index = find_edge_in_list(Y, recip)
			recip = Y[index]
			# put it into the RotG slot for edge.
			RotG[(edge[0], edge[2])] = (recip[0], recip[2])
	return RotG
def vertex_relabel(G):
	i=0
	for vertex in G.vertices():
		G.relabel({vertex: i})
		i+=1
	return G
def replacement_product(G1, G2):
	'''
	If G2 has size d, where G1 is a d-regular graph, then we can use this.
	Replace the vertices of G1 with copies of G2, preserving edges.
	'''
	# generate approximately |V(G1)| copies of G2. 
	clouds = [G2.copy() for i in range(0, G1.order())]
	
	# now, build out the edgeset based on the rotation map of G1
	RotG1 = rotation_map(G1)
	#print(RotG1)
	
	# connect each edge of the replacement product corresponding to the rotation maps.
	# So the rotation map specifies (u,v, 1) = (start vertex = u, end vertex = v, this is the 1st edge). The corresponding vertex of the 
	# resulting graph to build is (v,u, n), where n is the nth edge which leads to u. 
	# note that here, n is ACTUALLY just the label of the vertex of G2! So we want to build an edge
	# e = (u, n) <-- where u is the label of the "cloud" where the copy of G2 sits, and n is the specific vertex WITHIN that cloud!
	# in this code, we should index the clouds by cloud[i]. So u=i. 
	# Then we connect the vertex n to the vertex j corresponding to the rotation map of G1.
	# need to also draw edges between the interior clouds.
	H = Graph()
	for key in RotG1:
		H.add_edge(key, RotG1[key])
	for i in range(0, G1.order()):
		for edge in G2.edges():
			src = (i, edge[0]+1)
			dest = (i, edge[1]+1)
			H.add_edge(src, dest)
			
	return H
def zig_zag_product(X,Y):
	'''
	Admits 2 graphs, X and Y. From the "smaller" graph, we transform the vertices of the larger graph into "clouds" - that is, 
	copies of Y. The edges of the zig-zag product are determined by its rotation map.
	Naively written.
	'''
	#First edge the edge set of the replacement product between X and Y.
	Rep = replacement_product(X,Y)
	E_rep = Rep.edges()
	V_rep = Rep.vertices()
	'''
	An edge (a,b) is in the zigzag product IF:
		* The edge (a,x) is an edge in E_rep
		* The edge (x,y) is an edge in E_rep
		* The edge (y,b) is an edge in E_rep
	'''
	H = Graph()
	# this should also allow for self-loops
	for i in range(0, Rep.order()):
		for j in range(0, Rep.order()):
			u = V_rep[i]
			v = V_rep[j]
			cloud_1 = u[0]
			cloud_2 = v[0]
			subcloud_1 = u[1]
			subcloud_2 = v[1]
			if (u == v):
				continue
			else:
				for k in range(1, Y.order()+1):
					if (k != subcloud_1):
						x = (cloud_1, k)
					else:
						x = None
					for r in range(1, Y.order()+1):
						if (r != subcloud_2):
							y = (cloud_2, r)
							if (x is not None):
								if (u,x, None) in E_rep and (x,y, None) in E_rep and (y,v, None) in E_rep and (u,v,None) not in E_rep:
									if (cloud_1 == 0):
										'''
										print("Connecting " + str((u,v)) + ":")
										print("[1]: " + str((u,x)))
										print("[2]: " + str((x,y)))
										print("[3]: " + str((y,v)))
										'''
									H.add_edge((u,v))
	return H

# an example
G1 = Graph({0:[1,3,5], 1:[0,2,4], 2:[1,3,5], 3:[0,2,4], 4:[1,3,5], 5:[0,2,4]})
G2 = graphs.CompleteGraph(3)
R = replacement_product(G1, G2)
Z = zig_zag_product(G1, G2)
#R.show()
Z.show()
print(R.is_cayley())
print(Z.degree())
print("h(G1): " + str(G1.cheeger_constant()))
print("h(G2): " + str(G2.cheeger_constant()))
print("h(Z): " + str(Z.cheeger_constant()))

