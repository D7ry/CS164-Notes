class e: #edge
	def __init__(self, src, dest, cond = None): #cond = none for epsilon moves only
		self.src = src
		self.dest = dest
		self.cond = cond

class v: #vertex, edges are only outgoing
	def __init__(self, name, edges, is_start = False, is_final = False):
		self.name = name
		self.edges = edges #note that mutating this might lead to inaccurate epsilon edge counting
		self.is_start = is_start
		self.is_final = is_final
	def has_edge_on(self, cond):
		for e in self.edges:
			if e.cond == cond:
				return True
		return False

class graph:
	def __init__(self, name):
		self.vertices = dict()
		self.epsilon_edges = []
		self.name = name
		self.conds = []
	
	def add_vertex(self, vertex):
		if self.vertices.get(vertex.name) != None:
			print("Warning: vertex with name {} already exists".format(vertex.name))
			return
		for e in vertex.edges:
			if e.cond == None:
				self.epsilon_edges.append(e)
		self.vertices[vertex.name] = vertex
		#add action
		for e in vertex.edges:
			if e.cond != None and e.cond not in self.conds:
				self.conds.append(e.cond)

	def get_vertex(self, name):
		return self.vertices.get(name, None)

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
		edge_count = 0
		for v in self.vertices.values():
			print("vertex: " + v.name)
			print("start: " + str(v.is_start))
			print("final: " + str(v.is_final))
			print("edges:")
			for e in v.edges:
				print("edge: " + e.src + " -> " + e.dest + " on " + str(e.cond))
				edge_count += 1
			print("")
		print("done. Total vertices: {}, total edges: {}".format(len(self.vertices), edge_count))

	#print out a drawing data useful on https://csacademy.com/app/graph_editor/
	def print_drawing_data(self):
		#every vertex name with a new line
		for v in self.vertices.values():
			print(v.name)
		#edge src, edge dest, edge cond
		for v in self.vertices.values():
			for e in v.edges:
				print(e.src + " " + e.dest + " " + str(e.cond))


	#returns a dfa version of this graph, remove_epsilon must be called first
	def to_dfa(self):

		print("converting graph {} to dfa...".format(self.name))
		dfa_graph = graph("dfa_" + self.name)
		
		def add_vertex(states : list, name : str): #states is a list of this.vertices ready to be combined into a single DFA vertex
			is_start = True
			is_final = False
			for state in states:
				if not state.is_start: #if any of the states is not start, the new vertex is not start
					is_start = False
				if state.is_final: #if any of the states is final, the new vertex is final
					is_final = True
			nexts = [] #vector<pair<name, vector<vertices>>>
			dfa_edges = [] #outgoing edges
			for cond in self.conds: #for each condition, find all combinations of next states
				next = [] #vector<vertices>; these vertices are to be combined into a single DFA vertex
				next_name = ""
				for state in states:
					for edge in state.edges:
						if edge.cond == cond:
							vertex = self.get_vertex(edge.dest)
							if vertex not in next:
								next.append(vertex)
								next_name += edge.dest
				if next != []:
					dfa_edges.append(e(name, next_name, cond))
					print("adding edge: ", name + '->' + next_name + ' on ' + cond)
					nexts.append((next_name, next))
			print("adding vertex: " + name)
			dfa_graph.add_vertex(v(name, dfa_edges, is_start, is_final))
			#add all next vertices
			for next in nexts:
				if dfa_graph.get_vertex(next[0]) == None: #if this next state hasn't been added yet
					add_vertex(next[1], next[0])

		start_states = [v for v in self.vertices.values() if v.is_start]
		start_name = ""
		for state in start_states:
			start_name += state.name
		add_vertex(start_states, start_name)

		bad_state = None
		#complete the graph by adding all conditions to all vertices
		for dfa_vertex in dfa_graph.vertices.copy().values(): #make a copy of the keys because we're modifying the dict, this is fine since we're not modifying the keys
			for cond in self.conds:
				if not dfa_vertex.has_edge_on(cond):
					if bad_state == None:
						bad_state = v('bad', [], is_final=False) #create a bad state
						dfa_graph.add_vertex(bad_state)
					dfa_vertex.edges.append(e(dfa_vertex.name, bad_state.name, cond))

		print("...done converting to dfa")

		return dfa_graph