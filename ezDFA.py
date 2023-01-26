class e: #edge
	def __init__(self, src, dest, cond = None): #cond = none for epsilon moves only
		self.src = src
		self.dest = dest
		self.cond = cond

class v: #vertex, edges are only outgoing
	def __init__(self, name, edges, is_start = False, is_final = False):
		self.name = name
		self.edges = edges
		self.is_start = is_start
		self.is_final = is_final

class graph:
	def __init__(self, name):
		self.vertices = dict()
		self.epsilon_edges = []
		self.name = name
	
	def add_vertex(self, vertex):
		if self.vertices.get(vertex.name) != None:
			print("Warning: vertex with name {} already exists".format(vertex.name))
			return
		for e in vertex.edges:
			if e.cond == None:
				self.epsilon_edges.append(e)
		self.vertices[vertex.name] = vertex

	#verbose mode prints out all the steps, including adding&removing additional epsilon edges
	def remove_epsilon(self, verbose = False):
		print("proceeding to remove epsilon edges for graph {}...".format(self.name))
		while self.epsilon_edges != []:
			epe = self.epsilon_edges.pop(0)
			print("processing epsilon edge: " + epe.src + " -> " + epe.dest) if verbose else None
			v1 = g.vertices[epe.src]
			v2 = g.vertices[epe.dest]
			if v1 == v2: #epsilon edge that transitions into itself, just delete it
				v1.edges.remove(epe)
				continue
			for v2e in v2.edges:
				new_edge = e(v1.name, v2e.dest, v2e.cond)
				v1.edges.append(new_edge)
				if v2e.cond == None:
					self.epsilon_edges.append(new_edge)
				print("added edge: {} -> {} on {}".format(v1.name, v2e.dest, v2e.cond)) if verbose else None
			v1.edges.remove(epe)
			if v1.is_start:
				v2.is_start = True
				print("vertex {} is now start".format(v2.name)) if verbose else None
			if v2.is_final:
				v1.is_final = True
				print("vertex {} is now final".format(v1.name)) if verbose else None

		print("...done removing epsilon edges")

	def print_graph(self):
		print("printing graph: " + self.name)
		for v in self.vertices.values():
			print("vertex: " + v.name)
			print("start: " + str(v.is_start))
			print("final: " + str(v.is_final))
			print("edges:")
			for e in v.edges:
				print("edge: " + e.src + " -> " + e.dest + " on " + str(e.cond))
			print("")



g = graph("q2")
g.add_vertex(v('A', [e('A', 'K'), e('A', 'B')], is_start=True))
g.add_vertex(v('B', [e('B', 'C'), e('B', 'J')]))
g.add_vertex(v('C', [e('C', 'E'), e('C', 'H')]))
g.add_vertex(v('D', [e('D', 'B')]))
g.add_vertex(v('E', [e('E', 'F', 'a')]))
g.add_vertex(v('F', [e('F', 'G', 'b')]))
g.add_vertex(v('G', [e('G', 'D', 'a')]))
g.add_vertex(v('H', [e('H', 'I', 'b')]))
g.add_vertex(v('I', [e('I', 'D', 'b')]))
g.add_vertex(v('J', [e('J', 'Z')]))
g.add_vertex(v('K', [e('K', 'N'), e('K', 'O')]))
g.add_vertex(v('L', [e('L', 'M', 'b')]))
g.add_vertex(v('M', [e('M', 'K')]))
g.add_vertex(v('N', [e('N', 'L', 'a')]))
g.add_vertex(v('O', [e('O', 'Z')]))
g.add_vertex(v('Z', [], is_final=True))

g.print_graph()

g.remove_epsilon(False)

g.print_graph()

