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
		for e in vertex.edges:
			if e.cond == None:
				self.epsilon_edges.append(e)
		self.vertices[vertex.name] = vertex

	def remove_epsilon(self, verbose = False):
		print("proceeding to remove epsilon edges for graph: " + self.name)
		while self.epsilon_edges != []:
			epe = self.epsilon_edges.pop(0)
			print("processing epsilon edge: " + epe.src + " -> " + epe.dest) if verbose else None
			v1 = g.vertices[epe.src]
			v2 = g.vertices[epe.dest]
			if v1 == v2:
				continue
			for v2e in v2.edges:
				v1.edges.append(e(v1.name, v2e.dest, v2e.cond))
				print("added edge: {} -> {} on {}".format(v1.name, v2e.dest, v2e.cond)) if v2e.cond != None or verbose else None
			v1.edges.remove(epe)
			print("removed edge: " + epe.src + " -> " + epe.dest)
			if v1.is_start:
				v2.is_start = True
				print("vertex {} is now start".format(v2.name))
			if v2.is_final:
				v1.is_final = True
				print("vertex {} is now final".format(v1.name))

		print("done removing epsilon edges")



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

g.remove_epsilon()

