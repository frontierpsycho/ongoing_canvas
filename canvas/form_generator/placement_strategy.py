import random

class GridPlacementStrategy:
	def __init__(self, canvas_height, canvas_width, cell_height, cell_width, grid=[], depth=3):
		self.canvas_width = canvas_width
		self.cell_width = cell_width
		self.canvas_height = canvas_height
		self.cell_height = cell_height
		self.depth = depth
		#self.depths = [1, 0.707, 0.5]
		self.depths = [1,1,1]
		
		if self.width() == 0 or self.height() == 0:
			raise ArgumentException("At least one cell should fit in the canvas's width")
		[grid.append([[] for d in range(self.width())]) for e in range(self.height())]
		self.grid = grid
		
	def place(self, fd_id, shape):
		coord_j, coord_i, remove_list = self.find_place(fd_id)
		coords = (coord_j, coord_i)
		depth = self.cell_depth(coords)

		rotated = False
		
		if self.chance() and depth > 1:
			rotated = True
		
		shape.scale(self.depths[depth-1])
		self.translate_to_cell(coords, shape)

		position = []
		if self.chance():
			position.append("u")
		else:
			position.append("l")
		if self.chance():
			position.append("r")
		else:
			position.append("l")
		
		self.move_to_corner(shape, position, depth, rotated)

		if rotated:
			# move one cell to the right
			shape.translate(self.cell_width, 0)
			shape.rotate_horizontally()

		return remove_list

	def cell_depth(self, coords):
		return len(self.grid[coords[0]][coords[1]])

	def number_of_cells(self):
		return self.width()*self.height()
			
	def translate_to_cell(self, cell, shape):
		translate_y = cell[0]*self.cell_height
		translate_x = cell[1]*self.cell_width

		shape.translate(translate_x, translate_y)

	def move_to_corner(self, shape, corner, depth, rotated):
		translate_x = 0
		translate_y = 0

		if corner[0] == "l":
			if rotated:
				ratio = self.depths[depth-1]*0.707
			else:
				ratio = self.depths[depth-1]
			translate_y = (1-ratio)*self.cell_height
		
		if corner[1] == "l":
			if rotated:
				ratio = self.depths[depth-1]/0.707
				translate_x = -(1-ratio)*self.cell_width
		
		if corner[1] == "r":
			if not rotated:
				ratio = self.depths[depth-1]
				translate_x = (1-ratio)*self.cell_width

		shape.translate(translate_x, translate_y)

	def find_place(self, fd_id):
		width = range(self.width())
		random.shuffle(width)
		height = range(self.height())
		random.shuffle(height)

		for i in width:
			for j in height:
				if self.cell_depth((j,i)) < self.depth:
					templist = self.grid[j] # grid is a managed sync object
					templist[i].append(fd_id)
					self.grid[j] = templist
					return j, i, None # return an empty remove list

		for i in width:
			for j in height:
				if self.cell_depth((j,i)) == self.depth:
					templist = self.grid[j]
					previous_list = templist[i]
					templist[i] = [fd_id]
					self.grid[j] = templist
					return j, i, previous_list

	def print_grid(self):
		for line in self.grid:
			print line

	def width(self):
		return int(self.canvas_width/self.cell_width)
	
	def height(self):
		return int(self.canvas_height/self.cell_height)

	def chance(self, parts=2):
		#return (random.random() < 0.5)
		return False
