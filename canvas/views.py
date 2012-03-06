import xml.etree.ElementTree as ET
import copy
import random

from django.views.generic import ListView,DetailView

from canvas.models import FeelingData
from canvas.form_generator.form_generator import *

form_generator = FormGenerator("canvas/form_data/colors.cfg", ShapeGenerator(), "fill")

class CanvasView(ListView):
	global form_generator
	context_object_name = "feelingdata"
	template_name="canvas/canvas.html"

	def get_queryset(self):
		queryset = FeelingData.objects.order_by("postdatetime")[:10]

		self.strokes = []

		for fd in queryset:
			self.strokes.append(form_generator.generate_svg(fd))

		return queryset

	def get_context_data(self, **kwargs):
		context = super(CanvasView, self).get_context_data(**kwargs)
		context["strokes"] = self.strokes
		return context

class FeelingDataDetailView(DetailView):
	global form_generator
	context_object_name = "feeling"
	queryset=FeelingData.objects.all()

	def get_object(self, **kwargs):
		object = super(FeelingDataDetailView, self).get_object()
		self.stroke = form_generator.generate_svg(object)
		
		return object

	def get_context_data(self, **kwargs):
		context = super(FeelingDataDetailView, self).get_context_data(**kwargs)
		context["stroke"] = self.stroke
		return context
