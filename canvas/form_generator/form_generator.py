import random
from ConfigParser import ConfigParser

class FormGenerator:
	def __init__(self, settings_path, shape_generator, *effects):
		self.settings = ConfigParser()
		self.settings.read([settings_path])
		self.shape_generator = shape_generator
		self.effects = effects

	def generate_svg(self, feeling):
		svg = self.shape_generator.generate(feeling)
		for effect in self.effects:
			svg = self.apply_effect(effect, feeling, svg)
		print svg
		return svg

	def apply_effect(self, effect, feeling, svg):
		current_group = ""
		for groupblob in self.settings.items("Feeling groups"):
			group = groupblob[1].split(", ")
			if feeling.feeling.name in group:
				index = group.index(feeling.feeling.name)
				current_group = group
				current_group_name = groupblob[0]
				break

		# determine hue	
		hueblob = self.settings.get("Colors", current_group_name)
		hue = [int(bound) for bound in hueblob.split("-")]

		color = "hsl(%d, 100, %d)" % (random.randint(hue[0],hue[1]), 80-(index+1)*15)

		if effect == "fill":
			svg = svg.format(fill=color)	
		return svg

class ShapeGenerator:
	def generate(self, feeling):
		return '<?xml version="1.0" standalone="no"?><!DOCTYPE svg PUBLIC "-//W3C//DTD SVG 1.1//EN" "http://www.w3.org/Graphics/SVG/1.1/DTD/svg11.dtd"><svg xmlns="http://www.w3.org/2000/svg" version="1.1"><circle cx="50" cy="50" r="40" stroke="black" stroke-width="2" fill="{fill}" /></svg>'
