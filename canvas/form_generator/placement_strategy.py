class GridPlacementStrategy:
	def __init__(self, canvas_height, canvas_width, cell_height, cell_width, depth=3):
		self.canvas_width = canvas_width
		self.cell_width = cell_width
		self.canvas_height = canvas_height
		self.cell_height = cell_height
		self.depth = depth
		
		if self.width() == 0 or self.height() == 0:
			raise ArgumentException("At least one cell should fit in the canvas's width")
		self.grid = [[0 for d in range(self.width())] for e in range(self.height())]
		
	def place(self, shape):
		cell = self.find_place()
		depth = self.grid[cell[0]][cell[1]]
		if depth == 1:
			self.translate_to_cell(cell, shape)
		elif depth == 2:
			shape.scale(0.707)
			#shape.translate(self.cell_width, 0)
			#shape.rotate_horizontally()
			self.translate_to_cell(cell, shape)
		elif depth == 3:
			shape.scale(0.5)
			self.translate_to_cell(cell, shape)
			
			# move one cell to the right
			shape.translate(self.cell_width, 0)
			shape.rotate_horizontally()
			
	def translate_to_cell(self, cell, shape, edge="ur"):
			translate_y = cell[0]*self.cell_height
			if edge[0] == "l":
				translate_y += self.cell_height

			translate_x = cell[1]*self.cell_width
			if edge[1] == "l":
				translate_x -= self.cell_width

			shape.translate(translate_x, translate_y)

	def find_place(self):
		for i in range(self.width()):
			for j in range(self.height()):
				if self.grid[j][i] < self.depth:
					self.grid[j][i] += 1
					return j,i

	def width(self):
		return int(self.canvas_width/self.cell_width)
	
	def height(self):
		return int(self.canvas_height/self.cell_height)
