import random
import json
import re

class FormGenerator:
	color_matcher = re.compile("(H|S|V)(?P<rel>[iad]{2})?(\d+$|\d+-\d+$)")
	def __init__(self, settings_path, shape_generator):
		self.settings = json.loads(open(settings_path).read())
		self.shape_generator = shape_generator

	def generate_svg(self, feeling):
		svg = self.shape_generator.generate(feeling)
		svg = self.apply_effects(feeling, svg)
		#print svg
		return svg

	def apply_effects(self, feeling, svg):
		found = False
		for name,group in self.settings["Feeling groups"].items():
			for subgroup in group:
				subgroup_index = 0
				if feeling.feeling.name in subgroup:
					found = True
					index = subgroup.index(feeling.feeling.name)
					current_group = group
					current_group_name = name
					break
				subgroup_index += 1
		print found
		if found:
			color = FormGenerator.get_color(self.settings["Coloring schemes"][current_group_name][subgroup_index])
			print color[0]
			first_color = "hsl(%d, %d, %d)" % (color[0][0], color[0][1], color[0][2])

			svg = svg.format(fill=first_color)
		return svg

	@staticmethod
	def get_color(scheme):
		colors = scheme["colors"]
		result = []
		for color in colors:
			t = FormGenerator.generate_hsv(scheme[color])
			hsl = FormGenerator.hsv_to_hsl(t[0], t[1], t[2])
			print "HSL color: %d, %d, %d" % (hsl[0], hsl[1], hsl[2])
			result.append(hsl)
		return result

	@staticmethod
	def generate_hsv(color_scheme):
		h,s,v = color_scheme.split("|")

		print "H: %s, S: %s, V: %s" % (h, s, v)

		h = FormGenerator.get_color_value(h)
		s = FormGenerator.get_color_value(s)
		v = FormGenerator.get_color_value(v)
		print "H: %s, S: %s, V: %s after" % (h, s, v)
		return (h,s,v)

	@staticmethod
	def get_color_value(scheme):
		m = FormGenerator.color_matcher.match(scheme)

		print "Scheme: %s" % m.group(3)
		val_range = m.group(3).split("-")
		if len(val_range) == 1:
			print "Single value: %s" % val_range[0]
			ret = int(val_range[0])
		elif len(val_range) == 2:
			print "Range: from %s to %s" % (val_range[0], val_range[1])
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
			_s /= 2 - _l
		_l /= 2
		return _h, int(_s*100), int(_l*100)

class ShapeGenerator:
	def generate(self, feeling):
		return '<?xml version="1.0" standalone="no"?><!DOCTYPE svg PUBLIC "-//W3C//DTD SVG 1.1//EN" "http://www.w3.org/Graphics/SVG/1.1/DTD/svg11.dtd"><svg xmlns="http://www.w3.org/2000/svg" version="1.1"><circle cx="50" cy="50" r="40" stroke="black" stroke-width="2" fill="{fill}" /></svg>'
