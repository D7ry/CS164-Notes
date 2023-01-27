class Vertex:
		def __init__(self, name: str, is_start: bool = False, is_final: bool = False):
			self.name = name
			self.is_start = False
			self.is_final = False
			self.__edges_out = []
			self.__edges_in = []
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
	def add_vertex(self, vertex_name : str):
		if self.__vertices.get(vertex_name) != None:
			print("Warning: vertex with name {} already exists".format(vertex_name))
			return
		new_vertex = Vertex(vertex_name)
		self.__vertices[vertex_name] = new_vertex

	def is_connected(self, src_name : str, dest_name : str, cond):
		src = self.__vertices[src_name]
		dest = self.__vertices[dest_name]
		if src == None or dest == None:
			raise Exception("Vertex {} or {} not found".format(src_name, dest_name))
		for edge in src._Vertex__edges_out:
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
		src._Vertex__edges_out.append(edge)
		dest._Vertex__edges_in.append(edge)
	
	def connect(self, src_name : str, dest_name : str, cond : str = None):
		src = self.__vertices[src_name]
		dest = self.__vertices[dest_name]
		if src == None or dest == None:
			raise Exception("Vertex {} or {} not found".format(src_name, dest_name))
		if self.is_connected(src_name, dest_name, cond):
			raise Exception("Edge {} -> {} already exists".format(src_name, dest_name))
		self.__connect(src, dest, cond)

	def __remove_edge(self, edge):
		src = edge.src
		dest = edge.dest
		src.__edges_out.remove(edge)
		dest.__edges_in.remove(edge)
		self.__edges.remove(edge)
	
	def remove_epsilon(self):
		while self.epsilon_edges:
			ee = self.epsilon_edges.pop()
			src = ee.src
			dest = ee.dest
			self.__remove_edge(ee)
			for destE in dest.__edges_out:
				__connect(src, destE.dest, destE.cond)
			dest.is_start = dest.is_start or src.is_start
			src.is_final = src.is_final or dest.is_final
	
	def print(self):
		print("Graph: {}".format(self.name))
		print("Vertices:")
		for v in self.__vertices:
			print("  {}".format(v))
		print("Edges:")
		for e in self.__edges:
			print("  {} -> {} : {}".format(e.src.name, e.dest.name, e.cond))
		print("Epsilon Edges:")
		for e in self.__epsilon_edges:
			print("  {} -> {}".format(e.src.name, e.dest.name))

test = Graph("test")
test.add_vertex("v1")
test.add_vertex("v2")
test.connect("v1", "v2")
test.connect("v2", "v1")
test.print()



# class e: #edge
# 	def __init__(self, src, dest, cond = None): #cond = none for epsilon moves only
# 		self.src = src
# 		self.dest = dest
# 		self.cond = cond

# class v: #vertex, edges are only outgoing
# 	def __init__(self, name, edges, is_start = False, is_final = False):
# 		self.name = name
# 		self.edges = edges #note that mutating this might lead to inaccurate epsilon edge counting
# 		self.is_start = is_start
# 		self.is_final = is_final
# 	def has_edge_on(self, cond):
# 		for e in self.edges:
# 			if e.cond == cond:
# 				return True
# 		return False

# class graph:
# 	def __init__(self, name):
# 		self.vertices = dict()
# 		self.epsilon_edges = []
# 		self.name = name
# 		self.conds = []
	
# 	def add_vertex(self, vertex):
# 		if self.vertices.get(vertex.name) != None:
# 			print("Warning: vertex with name {} already exists".format(vertex.name))
# 			return
# 		for e in vertex.edges:
# 			if e.cond == None:
# 				self.epsilon_edges.append(e)
# 		self.vertices[vertex.name] = vertex
# 		#add action
# 		for e in vertex.edges:
# 			if e.cond != None and e.cond not in self.conds:
# 				self.conds.append(e.cond)
	
# 	def add_edge(self, vertexName, edge):
# 		if self.vertices.get(vertexName) == None:
# 			print("Warning: vertex with name {} does not exist".format(vertexName))
# 			return
# 		if edge.cond == None:
# 			self.epsilon_edges.append(edge)
# 		self.vertices[vertexName].edges.append(edge)
# 		#add action
# 		if edge.cond != None and edge.cond not in self.conds:
# 			self.conds.append(edge.cond)
	
# 	def remove_edge(self, edge):
# 		if self.vertices.get(edge.src) == None:
# 			print("Warning: vertex with name {} does not exist".format(edge.src))
# 			return
# 		self.vertices[edge.src].edges.remove(edge)
# 		if edge.cond == None:
# 			self.epsilon_edges.remove(edge)
# 		#add action

# 	def get_vertex(self, name):
# 		return self.vertices.get(name, None)
	
# 	def reduce(self): #remove useless vertices whose outgoing edges are all epsilon
# 		toremove = []
# 		for vertex in self.vertices.values():
# 			out = []
# 			is_epsilon = True #if all outgoing edges are epsilon, this means the vertex is useless
# 			for edge in vertex.edges:
# 				if edge.cond != None:
# 					is_epsilon = False
# 				if edge.dest not in out:
# 					out.append(edge)
# 			if is_epsilon:
# 				print("removing vertex {} because it is useless".format(vertex.name))
# 				if vertex.is_start:
# 					for edge in out:
# 						self.vertices[edge.dest].is_start = True 
# 				edgesToVertex = []
# 				for other_vertex in self.vertices.values():
# 					if other_vertex == vertex:
# 						continue
# 					for edge in other_vertex.edges:
# 						if edge.dest == vertex.name:
# 							edgesToVertex.append(edge)
				
# 				for edge in edgesToVertex:
# 					for new_dest in out:
# 						print("changing edge {} to transition to {} on {}".format(edge.src, new_dest.dest, edge.cond))
# 						self.add_edge(edge.src, e(edge.src, new_dest.dest, edge.cond))
# 					self.remove_edge(edge)
# 				for out_edge in out:
# 					self.remove_edge(out_edge)
# 				toremove.append(vertex.name)
# 		for name in toremove:
# 			self.vertices.pop(name)


# 	#verbose mode prints out all the steps, including adding&removing additional epsilon edges
# 	def remove_epsilon(self, verbose = False, reduce = True):
# 		print("proceeding to remove epsilon edges for graph {}...".format(self.name))
# 		while self.epsilon_edges != []:
# 			epe = self.epsilon_edges.pop(0)
# 			print("processing epsilon edge: " + epe.src + " -> " + epe.dest) if verbose else None
# 			v1 = self.vertices[epe.src]
# 			v2 = self.vertices[epe.dest]
# 			if v1 == v2: #epsilon edge that transitions into itself, just delete it
# 				v1.edges.remove(epe)
# 				continue					

# 			for v2e in v2.edges:
# 				new_edge = e(v1.name, v2e.dest, v2e.cond)
# 				v1.edges.append(new_edge)
# 				if v2e.cond == None:
# 					self.epsilon_edges.append(new_edge)
# 				print("added edge: {} -> {} on {}".format(v1.name, v2e.dest, v2e.cond)) if verbose else None


# 			v1.edges.remove(epe)
# 			if v1.is_start:
# 				v2.is_start = True
# 				print("vertex {} is now start".format(v2.name)) if verbose else None
# 			if v2.is_final:
# 				v1.is_final = True
# 				print("vertex {} is now final".format(v1.name)) if verbose else None

# 		print("...done removing epsilon edges")

# 	def print_graph(self):
# 		print("printing graph: " + self.name)
# 		edge_count = 0
# 		for v in self.vertices.values():
# 			print("vertex: " + v.name)
# 			print("start: " + str(v.is_start))
# 			print("final: " + str(v.is_final))
# 			print("edges:")
# 			for e in v.edges:
# 				print("edge: " + e.src + " -> " + e.dest + " on " + str(e.cond))
# 				edge_count += 1
# 			print("")
# 		print("done. Total vertices: {}, total edges: {}".format(len(self.vertices), edge_count))

# 	#print out a drawing data useful on https://csacademy.com/app/graph_editor/
# 	def print_drawing_data(self):
# 		#every vertex name with a new line
# 		for v in self.vertices.values():
# 			print(v.name)
# 		#edge src, edge dest, edge cond
# 		for v in self.vertices.values():
# 			for e in v.edges:
# 				print(e.src + " " + e.dest + " " + str(e.cond))


# 	#returns a dfa version of this graph, remove_epsilon must be called first
# 	def to_dfa(self, add_bad_state = False):

# 		print("converting graph {} to dfa...".format(self.name))
# 		dfa_graph = graph("dfa_" + self.name)
		
# 		def add_vertex(states : list, name : str): #states is a list of this.vertices ready to be combined into a single DFA vertex
# 			is_start = True
# 			is_final = False
# 			for state in states:
# 				if not state.is_start: #if any of the states is not start, the new vertex is not start
# 					is_start = False
# 				if state.is_final: #if any of the states is final, the new vertex is final
# 					is_final = True
# 			nexts = [] #vector<pair<name, vector<vertices>>>
# 			dfa_edges = [] #outgoing edges
# 			for cond in self.conds: #for each condition, find all combinations of next states
# 				next = [] #vector<vertices>; these vertices are to be combined into a single DFA vertex
# 				next_name = ""
# 				for state in states:
# 					for edge in state.edges:
# 						if edge.cond == cond:
# 							vertex = self.get_vertex(edge.dest)
# 							if vertex not in next:
# 								next.append(vertex)
# 								next_name += edge.dest
# 				if next != []:
# 					dfa_edges.append(e(name, next_name, cond))
# 					print("adding edge: ", name + '->' + next_name + ' on ' + cond)
# 					nexts.append((next_name, next))
# 			print("adding vertex: " + name)
# 			dfa_graph.add_vertex(v(name, dfa_edges, is_start, is_final))
# 			#add all next vertices
# 			for next in nexts:
# 				if dfa_graph.get_vertex(next[0]) == None: #if this next state hasn't been added yet
# 					add_vertex(next[1], next[0])

# 		start_states = [v for v in self.vertices.values() if v.is_start]
# 		start_name = ""
# 		for state in start_states:
# 			start_name += state.name
# 		add_vertex(start_states, start_name)

# 		if add_bad_state:
# 			bad_state = None
# 			#complete the graph by adding all conditions to all vertices
# 			for dfa_vertex in dfa_graph.vertices.copy().values(): #make a copy of the keys because we're modifying the dict, this is fine since we're not modifying the keys
# 				for cond in self.conds:
# 					if not dfa_vertex.has_edge_on(cond):
# 						if bad_state == None:
# 							bad_state = v('bad', [], is_final=False) #create a bad state
# 							dfa_graph.add_vertex(bad_state)
# 						dfa_vertex.edges.append(e(dfa_vertex.name, bad_state.name, cond))

# 		print("...done converting to dfa")

# 		return dfa_graph
