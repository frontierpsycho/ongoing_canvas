import xml.etree.ElementTree as ET
import copy
import random

from django.views.generic import ListView,DetailView
from django.conf import settings
from django.db.models import Q

from canvas.models import FeelingData
from canvas.form_generator.form_generator import *
from canvas.form_generator.placement_strategy import GridPlacementStrategy

def start_generator(cells_manager):
	form_generator = FormGenerator("canvas/form_data/colors.json", "canvas/form_data/shapes.json", GridPlacementStrategy(settings.CANVAS_HEIGHT, settings.CANVAS_WIDTH, 136, 96, depth=3))

manager = Manager()

cells = manager.dict()

p = Process(target=start_generator, args=(cells))
p.start()

class CanvasView(ListView):
	global form_generator
	context_object_name = "shapes"
	template_name="canvas/canvas.html"

	def get_queryset(self):
		feelings_filter = self.request.GET.getlist("feelings")
		self.feelings_filter = feelings_filter

		feelingdata = FeelingData.objects.order_by("postdatetime")
		if len(feelings_filter) > 0:
			feelingdata = feelingdata.filter(feeling__name__in=feelings_filter)

		feelingdata = feelingdata[:200]

		all_feelings = []
		for group in form_generator.settings["Feeling groups"].values():
			for subgroup in group:
				all_feelings.extend(subgroup)
		self.all_feelings = sorted(all_feelings)

		shapes = []

		for fd in feelingdata:
			shape = form_generator.generate_shape(fd)
			if shape is not None: 
				shapes.append(shape)

		return shapes
	
	def get_context_data(self, **kwargs):
		context = super(CanvasView, self).get_context_data(**kwargs)
		context["width"] = settings.CANVAS_WIDTH
		context["height"] = settings.CANVAS_HEIGHT
		context["all_feelings"] = self.all_feelings
		context["feelings_filter"] = self.feelings_filter

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
