import random
import json
import re

class FormGenerator:
	colour_matcher = re.compile("(H|S|V)(?P<rel>[iad]{2})?(\d+$|\d+-\d+$)")
	def __init__(self, settings_path, shapes_path, placement_strategy, cells={}):
		self.settings = json.loads(open(settings_path).read())
		self.shapes = json.loads(open(shapes_path).read())
		self.placement_strategy = placement_strategy
		self.cells = cells

	def get_feeling_coordinates(self, feeling_name):
		# could be much faster with indices if need be
		found = False
		for name,group in self.settings["Feeling groups"].items():
			for subgroup in group:
				subgroup_index = 0
				if feeling_name in subgroup:
					found = True
					index = subgroup.index(feeling_name)
					current_group = group
					current_group_name = name
					break
				subgroup_index += 1
		if found:
			return current_group_name,subgroup_index
		else:
			return None

	def generate_shape(self, feeling_data):
		if feeling_data.id in self.cells:
			return self.cells[feeling_data.id]
		shape = None
		tupleOrNone = self.get_feeling_coordinates(feeling_data.feeling.name)
		if tupleOrNone:
			(current_group_name,subgroup_index) = tupleOrNone
			shape = Shape(self.shapes[current_group_name][subgroup_index])
			
			colour = FormGenerator.get_colour(self.settings["Coloring schemes"][current_group_name][subgroup_index])
			shape.colour = "hsl(%d, %d, %d)" % colour[0]
			# TODO change size
			# TODO add position
			self.placement_strategy.place(shape)
			self.cells[feeling_data.id] = shape

		return shape

	@staticmethod
	def get_colour(scheme):
		colours = scheme["colors"]
		result = []
		for colour in colours:
			t = FormGenerator.generate_hsv(scheme[colour])
			hsl = FormGenerator.hsv_to_hsl(t[0], t[1], t[2])
			# print "HSL colour: %d, %d, %d" % (hsl[0], hsl[1], hsl[2])
			result.append(hsl)
		return result

	@staticmethod
	def generate_hsv(colour_scheme):
		h,s,v = colour_scheme.split("|")

		# print "H: %s, S: %s, V: %s" % (h, s, v)

		h = FormGenerator.get_colour_value(h)
		s = FormGenerator.get_colour_value(s)
		v = FormGenerator.get_colour_value(v)
		# print "H: %s, S: %s, V: %s after" % (h, s, v)
		return (h,s,v)

	@staticmethod
	def get_colour_value(scheme):
		m = FormGenerator.colour_matcher.match(scheme)

		# print "Scheme: %s" % m.group(3)
		val_range = m.group(3).split("-")
		if len(val_range) == 1:
			# print "Single value: %s" % val_range[0]
			ret = int(val_range[0])
		elif len(val_range) == 2:
			# print "Range: from %s to %s" % (val_range[0], val_range[1])
			ret = random.randint(int(val_range[0]), int(val_range[1]))# FIXME deterministic
		else:
			ret = 0
		return ret

	@staticmethod
	def hsv_to_hsl(h, s, v):
		s /= 100.0
		v /= 100.0
		_h = h
		_l = (2 - s) * v
		_s = s * v
		if _l <= 1:
			_s /= _l
		else:
			if _l == 2:
				_s = 100
			else:
				_s /= 2 - _l
		_l /= 2
		return _h, int(_s*100), int(_l*100)

class Shape:
	A = 0
	B = 1
	C = 2
	D = 3
	E = 4
	F = 5
	def __init__(self, path):
		self.path = path
		self.colour = ""
		self.transformation_matrix = [1,0,0,1,0,0]

	def translate(self, x, y):
		self.transformation_matrix[self.E] += x
		self.transformation_matrix[self.F] += y

	def scale(self, scalex, scaley=None):
		if not scaley:
			scaley=scalex
		self.transformation_matrix[self.A]=scalex
		self.transformation_matrix[self.D]=scaley

	def rotate_horizontally(self):
		# MATRIX MULTIPLICATION BY HAND - do not try this at home
		tempA = self.transformation_matrix[self.A]
		self.transformation_matrix[self.A] = self.transformation_matrix[self.C]
		tempB = self.transformation_matrix[self.B]
		self.transformation_matrix[self.B] = self.transformation_matrix[self.D]
		self.transformation_matrix[self.C] = -tempA
		self.transformation_matrix[self.D] = -tempB
		# E and F do not change
