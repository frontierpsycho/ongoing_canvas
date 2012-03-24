class GridPlacementStrategy:
	def __init__(self, canvas_height, canvas_width, cell_height, cell_width, depth=3):
		self.canvas_width = canvas_width
		self.cell_width = cell_width
		self.canvas_height = canvas_height
		self.cell_height = cell_height
		self.depth = depth

		if self.width() == 0 or self.height() == 0:
			raise ArgumentException("At least one cell should fit in the canvas's width")
		self.grid = [[0 for d in range(self.height())] for e in range(self.width())]

	def place(self, shape):
		cell = self.find_place()
		depth = self.grid[cell[0]][cell[1]]
		if depth == 1:
			self.translate_to_cell(cell, shape)
		elif depth == 2:
			shape.scale(0.707)
			new_cell = (cell[0], cell[1]+1)
			self.translate_to_cell(new_cell, shape)
			shape.rotate_horizontally()
		elif depth == 3:
			shape.scale(0.5)
			#new_cell = (cell[0], cell[1]+1)
			self.translate_to_cell(cell, shape, "lr")
			shape.rotate_horizontally()
			
	def translate_to_cell(self, cell, shape, edge="ul"):
			translate_y = 2*cell[0]*self.cell_height
			if edge[0] == "l":
				translate_y += self.cell_height

			translate_x = cell[1]*self.cell_width
			if edge[1] == "r":
				translate_x += self.cell_width

			shape.translate(translate_x, translate_y)

	def find_place(self):
		for i in range(self.width()):
			for j in range(self.height()):
				if self.grid[i][j] < self.depth:
					self.grid[i][j] += 1
					return i,j

	def width(self):
		return int(self.canvas_width/self.cell_width)
	
	def height(self):
		return int(self.canvas_height/self.cell_height)
