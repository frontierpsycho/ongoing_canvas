import random

class GridPlacementStrategy:
	def __init__(self, canvas_height, canvas_width, cell_height, cell_width, depth=3):
		self.canvas_width = canvas_width
		self.cell_width = cell_width
		self.canvas_height = canvas_height
		self.cell_height = cell_height
		self.depth = depth
		self.depths = [1, 0.707, 0.5]
		
		if self.width() == 0 or self.height() == 0:
			raise ArgumentException("At least one cell should fit in the canvas's width")
		self.grid = [[[] for d in range(self.width())] for e in range(self.height())]
		
	def place(self, shape):
		coords = self.find_place(id)
		depth = self.cell_depth(coords)

		rotated = False
		
		if self.chance() and depth > 1:
			rotated = True
		
		shape.scale(self.depths[depth-1])
		self.translate_to_cell(coords, shape)
		if self.chance():
			self.move_to_corner(shape, "lr", depth, rotated)

		if rotated:
			# move one cell to the right
			shape.translate(self.cell_width, 0)
			shape.rotate_horizontally()

	def cell_depth(self, coords):
		return len(self.grid[coords[0]][coords[1]])
			
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

	def find_place(self, id):
		width = range(self.width())
		random.shuffle(width)
		height = range(self.height())
		random.shuffle(height)

		for i in width:
			for j in height:
				if self.cell_depth((j,i)) < self.depth:
					self.grid[j][i].append(id)
					return j,i

		for i in width:
			for j in height:
				if self.cell_depth((j,i)) == self.depth:
					self.grid[j][i] = []
					return j,i

	def width(self):
		return int(self.canvas_width/self.cell_width)
	
	def height(self):
		return int(self.canvas_height/self.cell_height)

	def chance(self):
		return (random.random() < 0.5)
