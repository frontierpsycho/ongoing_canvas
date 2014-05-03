import random
import json
import re
import sys
import logging
import time
import datetime
import urllib
import urllib2
import os

import django.db

os.environ['DJANGO_SETTINGS_MODULE'] = 'ongoing_canvas.settings'
from ongoing_canvas import settings

from ongoing_canvas.canvas.models import FeelingData

logging.basicConfig()
logger = logging.getLogger("canvas.form_generator")

class FormGenerator:
	colour_matcher = re.compile("(H|S|V)(?P<rel>[iad]{2})?(\d+$|\d+-\d+$)")

	def __init__(self, settings_path, shapes_path, placement_strategy, cells=[], ongoing=False):
		self.settings = json.loads(open(settings_path).read())
		self.shapes = json.loads(open(shapes_path).read())
		self.placement_strategy = placement_strategy
		self.cells = cells
		self.feelingdata = list(FeelingData.objects.order_by("postdatetime")[:200])
		self.latest_postdatetime = self.feelingdata[-1].postdatetime if len(self.feelingdata) > 0 else datetime.datetime.min
		self.counter = 0
		self.blackwhite = False
		while(ongoing):
			self.add_feeling()
			time.sleep(2)
			django.db.close_connection()


	def add_feeling(self):
		if len(self.feelingdata) > self.counter:
			fd = self.feelingdata[self.counter]
			shape, remove_list = self.add_shape(fd)
			if shape:
				self.broadcast(fd.id, "shapes", remove_list)
			else:
				logger.warning("Invalid feeling found in database: %d, %s" % (fd.id, str(fd.feeling.name)) )
			self.counter += 1
		else:
			if len(self.feelingdata) > 0:
				self.latest_postdatetime = self.feelingdata[-1].postdatetime 
			self.feelingdata = list(FeelingData.objects.filter(postdatetime__gt = self.latest_postdatetime).order_by("postdatetime")[:200])
			self.counter = 0

	def broadcast(self, id, channel, remove_list=[]):
		try:
			url = "http://%s/refresh/" % settings.BROADCAST_URL

			data = { "id" : id, "remove": remove_list }
			req = urllib2.Request(url, urllib.urlencode(data))

			return urllib2.urlopen(req).read()
		except urllib2.HTTPError as e:
			logger.error("Error broadcasting: %s " % e)

	def get_feeling_coordinates(self, feeling_name):
		# could be much faster with indices if need be
		found = False
		for name,group in self.settings["Feeling groups"].items():
			if found:
				break
			subgroup_index = 0
			for subgroup in group:
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

	def expand_feeling_list(self, name_list, intensity_list=[0, 1, 2, 3]):
		"""Return a full list of feelings from a list of feelings or feeling group names.

		The list can contain group or subgroup names in the form
		'categoryname_subgroupnumber', or plain feeling names.
		"""
		if not intensity_list:
			intensity_list = range(4)  # in case an empty list is given
		if not name_list:
			name_list = self.settings["Feeling groups"].keys()

		result = []
		for name in name_list:
			if name in self.settings["Feeling groups"]:
				for intensity in intensity_list:
					for item in self.settings["Feeling groups"][name][intensity]:
						result.append(item)
			elif re.match(r'\w+_\d+', name):
				m = re.match(r'(\w+)_(\d+)', name)
				group = m.group(1)
				subgroup = int(m.group(2))
				if subgroup in intensity_list:
					try:
						result.extend(self.settings["Feeling groups"][group][subgroup])
					except KeyError, IndexError:
						# invalid name, pass
						pass
			else:
				# either a plain feeling or invalid input
				tupleOrNone = self.get_feeling_coordinates(name)
				if tupleOrNone is not None:
					result.append(name)

		return result

	def generate_shape(self, feeling_data):
		if feeling_data in self.cells:
			return self.cells[feeling_data.id], None

		shape = None
		tupleOrNone = self.get_feeling_coordinates(feeling_data.feeling.name)
		if tupleOrNone:
			(current_group_name, subgroup_index) = tupleOrNone
			try:
				shape = Shape(self.shapes[current_group_name][0], feeling_data)
			except KeyError:
				shape = Shape(self.shapes['default'][0], feeling_data)

			if self.blackwhite:
				shape.colour = FormGenerator.get_blackwhite()
			else:
				shape.colour = FormGenerator.get_colour(self.settings["Coloring schemes"][current_group_name][subgroup_index], in_hsl=True)

			remove_list = self.placement_strategy.place(feeling_data.id, shape)
			return shape, remove_list
		return None, None  # always return tuple


	def add_shape(self, feeling_data):
		shape, remove_list = self.generate_shape(feeling_data)
		if shape:
			self.cells[feeling_data.id] = shape

		return shape, remove_list

	def feeling_categories_to_json(self):
		jsonFeelings = []
		for category, subgroups in self.settings['Feeling groups'].items():
			newNode = {'data': category, 'attr': {'id': category+'_node' }, 'children': []}
			for i, subgroup in enumerate(subgroups):
				colour = FormGenerator.get_colour(self.settings["Coloring schemes"][category][i])
				# OH LORD WHAT AN UGLY HACK - but a necessary evil, my son
				newSubNode = { 'data': "<span class='subCategorySquare' style='background-color: hsl(%d, %d%%, %d%%) !important;'></span>" % colour[0], 'attr': {'id': "%s_%d_node" % (category, i)}, 'children': []}
				#for feeling in subgroup:
				#	newSubNode['children'].append({'data': feeling, 'attr': { 'id': feeling+"_node" } })
				newNode['children'].append(newSubNode)
			jsonFeelings.append(newNode)

		return json.dumps(jsonFeelings)

	def feelings_to_json(self):
		jsonFeelings = []
		for subgroups in self.settings['Feeling groups'].values():
			for subgroup in subgroups:
				for feeling in subgroup:
					tupleOrNone = self.get_feeling_coordinates(feeling)
					if tupleOrNone:
						(current_group_name, subgroup_index) = tupleOrNone
						colour = FormGenerator.get_colour(self.settings["Coloring schemes"][current_group_name][subgroup_index])
						jsonFeelings.append({ "label": "<span style=\"color: hsl(%d, %d%%, %d%%)\">%s</span>" % (colour[0][0], colour[0][1], colour[0][2], feeling), "value": feeling })
					else:
						jsonFeelings.append({ "label": feeling, "value": feeling })
		return json.dumps(jsonFeelings)

	@staticmethod
	def get_colour(scheme, in_hsl=False):
		colours = scheme["colors"]
		result = []
		for colour in colours:
			t = FormGenerator.generate_hsv(scheme[colour])
			hsl = FormGenerator.hsv_to_hsl(t[0], t[1], t[2])
			# print "HSL colour: %d, %d, %d" % (hsl[0], hsl[1], hsl[2])
			result.append(hsl)
		if in_hsl:
			return "hsl(%d, %d, %d)" % result[0]
		else:
			return result

	@staticmethod
	def get_blackwhite():
		return "hsl(%d, %d, %d)" % (0, 100, 0)

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
			if _l == 0:
				_s = 1
			else:
				_s /= _l
		else:
			if _l == 2:
				_s = 1
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
	def __init__(self, path, fd):
		self.path = path
		self.colour = ""
		self.transformation_matrix = [1,0,0,1,0,0]
		self.fd = fd

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

import threading

class RepeatTimer(threading.Thread):
	def __init__(self, interval, callable, *args, **kwargs):
		threading.Thread.__init__(self)
		self.interval = interval
		self.callable = callable
		self.args = args
		self.kwargs = kwargs
		self.event = threading.Event()
		self.event.set()

	def run(self):
		while self.event.is_set():
			t = threading.Timer(self.interval, self.callable,
					self.args, self.kwargs)
			t.start()
			t.join()

	def cancel(self):
		self.event.clear()
