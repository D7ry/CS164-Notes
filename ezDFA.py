def sortString(str):
    return ''.join(sorted(str))

class Vertex:
	def __init__(self, name: str, is_start: bool = False, is_final: bool = False):
		self.name = name
		self.is_start = is_start
		self.is_final = is_final
		self.edges_out = []
		self.edges_in = []

	def get_next(self, cond: str):
		for edge in self.edges_out:
			if edge.cond == cond:
				return edge.dest
		return None

class Edge:
	def __init__(self, src : Vertex, dest : Vertex, cond: str):
		self.src = src
		self.dest = dest
		self.cond = cond


class Graph:
	
	def __init__(self, name):
		self.name = name
		self.__vertices = {}
		self.__edges = []
		self.__epsilon_edges = []
		self.__transitions = set() # all conditions that can be used to transition between states
	def add_vertex(self, vertex_name : str, is_start : bool = False, is_final : bool = False):
		if self.has_vertex(vertex_name):
			raise Exception("Warning: vertex with name {} already exists".format(vertex_name))
		new_vertex = Vertex(vertex_name, is_start=is_start, is_final=is_final)
		self.__vertices[vertex_name] = new_vertex

	def __remove_vertex(self, vertex : Vertex):
		print("removing vertex: {}".format(vertex.name))
		for edge in vertex.edges_out.copy():
			self.__remove_edge(edge) if edge not in vertex.edges_in else None #avoid double removal
		for edge in vertex.edges_in.copy(): 
			self.__remove_edge(edge)
		self.__vertices.pop(vertex.name)

	def has_vertex(self, vertex_name : str):
		return self.__vertices.get(vertex_name) != None

	def add_vertices(self, vertex_names : list[str]):
		for name in vertex_names:
			self.add_vertex(name)

	def is_connected(self, src_name : str, dest_name : str, cond):
		src = self.__vertices[src_name]
		dest = self.__vertices[dest_name]
		if src == None or dest == None:
			raise Exception("Vertex {} or {} not found".format(src_name, dest_name))
		for edge in src.edges_out:
			if edge.dest.name == dest_name and edge.cond == cond:
				return True
		return False
	
	def __connect(self, src : Vertex, dest : Vertex, cond : str = None):
		if self.is_connected(src.name, dest.name, cond):
			raise Exception("Edge {} -> {} already exists".format(src.name, dest.name))
		edge = Edge(src, dest, cond)
		if cond == None:
			self.__epsilon_edges.append(edge)
		self.__edges.append(edge)
		src.edges_out.append(edge)
		dest.edges_in.append(edge)
	
	def connect(self, src_name : str, dest_name : str, cond : str = None):
		src = self.__vertices[src_name]
		dest = self.__vertices[dest_name]
		if src == None or dest == None:
			raise Exception("Vertex {} or {} not found".format(src_name, dest_name))
		if self.is_connected(src_name, dest_name, cond):
			raise Exception("Edge {} -> {} already exists".format(src_name, dest_name))
		self.__connect(src, dest, cond)
		if cond != None and cond not in self.__transitions:
			self.__transitions.add(cond)

	def __remove_edge(self, edge):
		src = edge.src
		dest = edge.dest
		src.edges_out.remove(edge)
		dest.edges_in.remove(edge)
		self.__edges.remove(edge)
		if edge in self.__epsilon_edges:
			self.__epsilon_edges.remove(edge)

	def remove_epsilon(self):
		while self.__epsilon_edges:
			ee = self.__epsilon_edges.pop()
			src = ee.src
			dest = ee.dest
			self.__remove_edge(ee)
			for destE in dest.edges_out:
				self.__connect(src, destE.dest, destE.cond)
			dest.is_start = dest.is_start or src.is_start
			src.is_final = src.is_final or dest.is_final
	
	def to_dfa(self): #return a DFA'd version of this graph
		dfa_graph = Graph(self.name + "_dfa")
		def add_to_dfa(vertices : set[Vertex], name : str): #vertices: group of vertices equivalent to a single vertex in the DFA
			print("adding to dfa: {}".format(name))
			if dfa_graph.has_vertex(name):
				return
			is_start = False
			is_final = False
			for v in vertices:
				is_start = is_start or v.is_start
				is_final = is_final or v.is_final
			dfa_graph.add_vertex(name, is_start=is_start, is_final=is_final)
			# find all vertices that can be reached from this group of vertices
			# by a transition with the given condition
			# and add them to the DFA
			for transition in self.__transitions:
				next_vertices = set()
				next_name = ""
				for vertex in vertices:
					next_vertex = vertex.get_next(transition)
					if next_vertex != None and next_vertex not in next_vertices:
						next_vertices.add(next_vertex)
						next_name += next_vertex.name
				next_name = sortString(next_name)
				print("for transition {}, next vertices are: {}".format(transition, next_name))
				if next_vertices:
					add_to_dfa(next_vertices, next_name)
				dfa_graph.connect(name, next_name, transition)

	
		start_states = {v for v in self.__vertices.values() if v.is_start}
		start_name = ""
		for s in start_states:
			start_name += s.name
		start_name = sortString(start_name)
		add_to_dfa(start_states, start_name)
		return dfa_graph


	# get rid of vertices whose outgoing edges are all epsilon edges
	def reduce_epsilon(self):
		toremove = []
		for vertex in self.__vertices.values():
			out = []
			should_remove = True #if all outgoing edges are epsilon, this means the vertex is useless
			for edge in vertex.edges_out:
				if edge.cond != None:
					should_remove = False
				if edge.dest not in out:
					out.append(edge)
			if should_remove:
				print("reducing vertex {} because all its edges are outgoing Epsilon".format(vertex.name))
				if vertex.is_start: #update start vertices
					for edge in out:
						edge.dest.is_start = True
				for edge in vertex.edges_in:
					for new_dest in out:
						print("changing edge {} to transition to {} on {}".format(edge.src.name, new_dest.dest.name, edge.cond))
						self.__connect(edge.src, new_dest.dest, edge.cond)
					self.__remove_edge(edge)
				toremove.append(vertex)
		for name in toremove:
			self.__remove_vertex(name)
	
	def print(self):
		print("Graph: {}".format(self.name))
		print("# of Vertices: {}; # of Edges: {}".format(len(self.__vertices), len(self.__edges)))
		print("Vertices:")
		for v in self.__vertices:
			print("  {} -> {}".format(v, [(e.cond, e.dest.name) for e in self.__vertices[v].edges_out]))
		print("Epsilon Edges:")
		for e in self.__epsilon_edges:
			print("  {} -> {}".format(e.src.name, e.dest.name))
		print("Start Vertices: {}".format([v for v in self.__vertices if self.__vertices[v].is_start]))
		print("Final Vertices: {}".format([v for v in self.__vertices if self.__vertices[v].is_final]))

	def print_drawing_data(self):
		#every vertex name with a new line
		for v in self.__vertices.values():
			print(v.name)
		#edge src, edge dest, edge cond
		for v in self.__vertices.values():
			for e in v.edges_out:
				print(v.name + " " + e.dest.name + " " + str(e.cond))

test = Graph("test")
test.add_vertex("A", is_start = True)
test.add_vertices([char for char in "BCDEFGHIJ"])
test.connect("A", "B")
test.connect("A", "C")
test.connect("A", "D")
test.connect("B", "B", "a2")
test.connect("B", "B", "a3")
test.connect("C", "C", "a1")
test.connect("C", "C", "a3")
test.connect("D", "D", "a1")
test.connect("D", "D", "a2")
test.connect("B", "E", "a1")
test.connect("C", "F", "a2")
test.connect("D", "G", "a3")
test.connect("E", "E", "a2")
test.connect("E", "E", "a3")
test.connect("E", "H", "a1")
test.connect("F", "I", "a2")
test.connect("F", "F", "a3")
test.connect("F", "F", "a1")
test.connect("G", "J", "a3")
test.connect("G", "G", "a1")
test.connect("G", "G", "a2")
test.connect("H", "B")
test.connect("I", "C")
test.connect("J", "D")
test.print()
test.reduce_epsilon()
#test.remove_epsilon()
test.print()

#test_dfa = test.to_dfa()
#test_dfa.print()
#test_dfa.print_drawing_data()

	
