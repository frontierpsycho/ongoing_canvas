import xml.etree.ElementTree as ET
import copy
import random

from django.views.generic import ListView,DetailView

from canvas.models import FeelingData
from canvas.form_generator.form_generator import *

form_generator = FormGenerator("canvas/form_data/colors.json", "canvas/form_data/shapes.json")

class CanvasView(ListView):
	global form_generator
	context_object_name = "shapes"
	template_name="canvas/canvas.html"

	def get_queryset(self):
		feelingdata = FeelingData.objects.order_by("postdatetime")[:10]

		shapes = []

		for fd in feelingdata:
			shape = form_generator.generate_shape(fd)
			if shape is not None: 
				shapes.append(shape)

		return shapes

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
