import xml.etree.ElementTree as ET
import copy
import random
from multiprocessing import Process,Manager
import datetime

from django.http import HttpResponse
from django.views.generic import ListView,DetailView
from django.conf import settings
from django.db.models import Q

from django_socketio import broadcast_channel, NoSocket

from canvas.models import FeelingData
from canvas.form_generator.form_generator import *
from canvas.form_generator.placement_strategy import GridPlacementStrategy
from canvas.forms import PlaygroundFilterForm

def start_generator(cells_manager):
	form_generator = FormGenerator("canvas/form_data/colors.json", "canvas/form_data/shapes.json", GridPlacementStrategy(settings.CANVAS_HEIGHT, settings.CANVAS_WIDTH, 72, 72, depth=1), cells_manager, ongoing=True)

manager = Manager()

cells = manager.list()

p = Process(target=start_generator, args=(cells,))
p.start()

class CanvasView(ListView):
	global cells
	context_object_name = "shapes"
	template_name="canvas/canvas.html"

	def get_queryset(self):
		shapes = [t[1] for t in cells] # unpack id, shape pairs
		return shapes
	
	def get_context_data(self, **kwargs):
		context = super(CanvasView, self).get_context_data(**kwargs)
		context["width"] = settings.CANVAS_WIDTH
		context["height"] = settings.CANVAS_HEIGHT
		context['ongoing'] = True
		return context

class PlaygroundView(CanvasView):
	context_object_name = "shapes"
	template_name = "canvas/playground.html"

	def get_queryset(self):
		filters = []
		if self.request.GET:
			self.form = PlaygroundFilterForm(self.request.GET)
			if self.form.is_valid(): # All validation rules pass
				date = self.form.cleaned_data['date']
				# ugly filter to get data from specific date
				filters.extend([Q(postdatetime__gte=datetime.datetime.combine(date, datetime.time.min)), Q(postdatetime__lte=datetime.datetime.combine(date, datetime.time.max)) ])
		else:
			self.form = PlaygroundFilterForm()

		form_generator = FormGenerator("canvas/form_data/colors.json", "canvas/form_data/shapes.json", GridPlacementStrategy(settings.CANVAS_HEIGHT, settings.CANVAS_WIDTH, 72, 72, depth=1))

		feelingdata = FeelingData.objects.filter(*filters).order_by("postdatetime")

		feelingdata = feelingdata[:200]

		shapes = []
		for fd in feelingdata:
			shape = form_generator.generate_shape(fd)
			if shape is not None: 
				shapes.append(shape)
		return shapes

	def get_context_data(self, **kwargs):
		context = super(PlaygroundView, self).get_context_data(**kwargs)
		context['ongoing'] = False
		context['form'] = self.form
		return context

class FeelingDataDetailView(DetailView):
	global form_generator
	context_object_name = "feeling"
	queryset=FeelingData.objects.all()

	def get_object(self, **kwargs):
		object = super(FeelingDataDetailView, self).get_object()
		self.stroke = form_generator.generate_shape(object)
		
		return object

	def get_context_data(self, **kwargs):
		context = super(FeelingDataDetailView, self).get_context_data(**kwargs)
		context["stroke"] = self.stroke
		return context

def broadcast(request, id):
	global cells
	if len(cells) > 0:
		shape = cells[-1][1]
		try:
			broadcast_channel({ 'shape': shape.path, 'colour': shape.colour, 'transform': shape.transformation_matrix } , "shapes")
		except NoSocket:
			logger.error("No subscribers on channel shapes")
	return HttpResponse()
