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
		translate_y = cell[0]*self.cell_height
		translate_x = cell[1]*self.cell_width
		shape.translate(translate_x, translate_y)
		#print translate_x, translate_y

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
